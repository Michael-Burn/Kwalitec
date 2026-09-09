"""Same-day sitting arbitration: overdue > due > adaptive > sequential."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

import pytest

from app.application.adaptive_decision.arbitration import (
    REASON_ARBITRATION_ADAPTIVE_SELECTED,
    REASON_ARBITRATION_DUE_PROTECTED,
    REASON_ARBITRATION_OVERDUE_PROTECTED,
    REASON_ARBITRATION_SEQUENTIAL,
    ArbitrationLabel,
    PrecedenceWinner,
    arbitrate_sitting_precedence,
)
from app.application.adaptive_decision.policy_v0 import (
    PolicyV0AdaptiveDecisionEngine,
)
from app.application.adaptive_decision.policy_v1 import (
    PolicyV1AdaptiveDecisionEngine,
)
from app.application.adaptive_decision.types import (
    DailySittingRequest,
    DecisionOutcome,
)
from app.application.educational_packages.loader import (
    packages_for_subject,
    reset_educational_package_cache,
)
from app.application.educational_runtime_engine.selection_reasons import (
    SELECTION_REASON_SPACED_REVIEW,
)
from app.application.educational_runtime_engine.service import (
    EducationalRuntimeEngineService,
)
from app.application.spacing_scheduler import (
    get_spacing_scheduler,
    reset_canonical_spacing_scheduler_for_tests,
)
from app.application.student_twin.query import (
    LearnerKnowledgeSnapshot,
    TopicKnowledgeFact,
)
from app.domain.spacing_scheduler.types import SchedulingStatus
from tests.application.educational_runtime_engine.helpers import (
    make_user,
    publish_subject,
)


@pytest.fixture(autouse=True)
def _reset_spacing():
    reset_canonical_spacing_scheduler_for_tests()
    yield
    reset_canonical_spacing_scheduler_for_tests()


def test_arbitration_precedence_is_owned_outside_scheduler_and_policy_v1_scoring():
    """Requirement 2: orchestration layer owns overdue > due > adaptive > sequential."""
    overdue = arbitrate_sitting_precedence(
        protected_status=SchedulingStatus.OVERDUE,
        has_adaptive_candidate=True,
    )
    assert overdue.winner is PrecedenceWinner.OVERDUE
    assert overdue.reason_code == REASON_ARBITRATION_OVERDUE_PROTECTED

    due = arbitrate_sitting_precedence(
        protected_status=SchedulingStatus.DUE,
        has_adaptive_candidate=True,
    )
    assert due.winner is PrecedenceWinner.DUE
    assert due.reason_code == REASON_ARBITRATION_DUE_PROTECTED

    adaptive = arbitrate_sitting_precedence(
        protected_status=None,
        has_adaptive_candidate=True,
    )
    assert adaptive.winner is PrecedenceWinner.ADAPTIVE
    assert adaptive.reason_code == REASON_ARBITRATION_ADAPTIVE_SELECTED

    sequential = arbitrate_sitting_precedence(
        protected_status=None,
        has_adaptive_candidate=False,
    )
    assert sequential.winner is PrecedenceWinner.SEQUENTIAL
    assert sequential.reason_code == REASON_ARBITRATION_SEQUENTIAL

    # No exceptions / partial preemption: protected always wins when present.
    for status in (SchedulingStatus.OVERDUE, SchedulingStatus.DUE):
        result = arbitrate_sitting_precedence(
            protected_status=status,
            has_adaptive_candidate=True,
        )
        assert result.winner.value == status.value
        assert result.composer_selection_reason == SELECTION_REASON_SPACED_REVIEW


def test_arbitration_observability_labels_cover_each_outcome():
    """Requirement 5: internal labels for each arbitration outcome."""
    overdue = arbitrate_sitting_precedence(
        protected_status=SchedulingStatus.OVERDUE,
        has_adaptive_candidate=True,
    )
    assert set(overdue.labels) >= {
        ArbitrationLabel.OVERDUE_PROTECTED,
        ArbitrationLabel.SPACED_OVERDUE,
        ArbitrationLabel.ADAPTIVE_PREEMPTED_OVERDUE,
        ArbitrationLabel.ADAPTIVE_DEFERRED,
    }

    due = arbitrate_sitting_precedence(
        protected_status=SchedulingStatus.DUE,
        has_adaptive_candidate=True,
    )
    assert set(due.labels) >= {
        ArbitrationLabel.DUE_PROTECTED,
        ArbitrationLabel.SPACED_DUE,
        ArbitrationLabel.ADAPTIVE_PREEMPTED_DUE,
        ArbitrationLabel.ADAPTIVE_DEFERRED,
    }

    adaptive = arbitrate_sitting_precedence(
        protected_status=None,
        has_adaptive_candidate=True,
    )
    assert adaptive.labels == (ArbitrationLabel.ADAPTIVE_CANDIDATE,)

    sequential = arbitrate_sitting_precedence(
        protected_status=None,
        has_adaptive_candidate=False,
    )
    assert sequential.labels == (ArbitrationLabel.SEQUENTIAL_FALLBACK,)


@dataclass
class _StubTwin:
    facts: dict[str, TopicKnowledgeFact]
    covered: set[str]

    def knowledge_snapshot(
        self, *, user_id: int, subject_code: str
    ) -> LearnerKnowledgeSnapshot:
        return LearnerKnowledgeSnapshot(
            user_id=user_id,
            subject_code=subject_code,
            curriculum_identity=None,
            overall_estimated_knowledge=None,
            topics=tuple(self.facts.values()),
        )

    def topic_knowledge(
        self, *, user_id: int, subject_code: str, topic_id: str
    ) -> TopicKnowledgeFact:
        tid = (topic_id or "").strip()
        return self.facts.get(
            tid,
            TopicKnowledgeFact(
                topic_id=tid,
                has_estimated_knowledge=False,
                estimated_knowledge=None,
                estimated_mastery=None,
                evidence_count=0,
                last_practised_at=None,
            ),
        )

    def topics_with_estimated_knowledge(
        self, *, user_id: int, subject_code: str
    ) -> tuple[TopicKnowledgeFact, ...]:
        return tuple(
            f for f in self.facts.values() if f.has_estimated_knowledge
        )

    def topic_covered(
        self, *, user_id: int, subject_code: str, topic_id: str
    ) -> bool:
        return (topic_id or "").strip() in self.covered


def _fact(topic_id: str, *, ek: float, evidence: int) -> TopicKnowledgeFact:
    return TopicKnowledgeFact(
        topic_id=topic_id,
        has_estimated_knowledge=True,
        estimated_knowledge=ek,
        estimated_mastery=ek,
        evidence_count=evidence,
        last_practised_at=datetime(2026, 8, 1),
    )


@pytest.fixture
def runtime(ctx):
    return EducationalRuntimeEngineService()


def test_overdue_protected_always_wins_over_adaptive(ctx, runtime, monkeypatch):
    """Requirement 3: genuinely overdue item always beats adaptive candidate."""
    reset_educational_package_cache()
    monkeypatch.setattr(
        "app.application.adaptive_decision.policy_v1.packages_for_subject",
        lambda subject_id, mode=None: packages_for_subject("CS1", mode=mode),
    )
    user = make_user("arb-overdue@example.com")
    subject = publish_subject("ARBOV")
    journey = runtime.enrol_student(
        user_id=user.id,
        subject_code=subject,
        exam_date=date(2026, 8, 20),
    )
    due_pack_id = "FAKE-ARB-OVERDUE-PACK"
    seq_pack_id = "FAKE-ARB-SEQ-PACK"

    class _Pack:
        def __init__(self, package_id: str, topic_code: str = "1.1") -> None:
            self.package_id = package_id
            self.subject_id = subject
            self.topic_code = topic_code
            self.mode = "learning"
            self.campaign_day = "D1"
            self.display_title = package_id
            self.task_descriptions = ("Read", "Practice")
            self.tomorrow = type("T", (), {"next_topic_code": ""})()

    due_pack = _Pack(due_pack_id)
    seq_pack = _Pack(seq_pack_id, topic_code="2.1")
    monkeypatch.setattr(
        "app.application.educational_packages.guard.certified_guidance_enforced",
        lambda subject_id: True,
    )
    monkeypatch.setattr(
        "app.application.educational_packages.selection.pending_post_tip_front_package",
        lambda **kwargs: None,
    )
    monkeypatch.setattr(
        "app.application.educational_packages.selection.resolve_active_educational_package",
        lambda **kwargs: seq_pack,
    )
    monkeypatch.setattr(
        "app.application.educational_packages.loader.find_package_by_id",
        lambda pid: {due_pack_id: due_pack, seq_pack_id: seq_pack}.get(pid),
    )

    # Completed 2026-07-28 -> due 2026-07-29; as_of 2026-08-01 is overdue.
    get_spacing_scheduler().record_completed_exposure(
        learner_id=str(user.id),
        package_id=due_pack_id,
        completed_on=date(2026, 7, 28),
    )
    twin = _StubTwin(
        facts={
            "2.6.1": _fact("2.6.1", ek=0.410, evidence=5),
            "2.6.2": _fact("2.6.2", ek=0.092, evidence=4),
            "2.6.3": _fact("2.6.3", ek=0.254, evidence=3),
        },
        covered={"2.6.1", "2.6.2", "2.6.3"},
    )
    v1 = PolicyV1AdaptiveDecisionEngine(
        runtime=runtime,
        twin=twin,
        v0=PolicyV0AdaptiveDecisionEngine(runtime=runtime),
    )
    v1._topics_since_last_review = lambda request: 10  # type: ignore[method-assign]
    decision = v1.decide_daily_sitting(
        DailySittingRequest(
            user_id=user.id,
            subject_code=subject,
            mission_date=date(2026, 8, 1),
            curriculum_identity=journey.enrolment.curriculum_identity,
            exam_date=journey.enrolment.exam_date,
        )
    )
    assert decision.outcome == DecisionOutcome.SAFE_FALLBACK
    assert decision.composer_selection_reason == SELECTION_REASON_SPACED_REVIEW
    assert REASON_ARBITRATION_OVERDUE_PROTECTED in decision.reason_codes
    assert decision.educational_package_id == due_pack_id
    labels = decision.selection_trace.get("arbitration_labels") or []
    assert "overdue_protected" in labels
    assert "adaptive_preempted_overdue" in labels
    assert decision.selection_trace.get("spacing_status") == "overdue"


def test_due_protected_always_wins_over_adaptive_in_v1(ctx, runtime, monkeypatch):
    """Requirement 4: merely-due item always beats adaptive; no partial preemption."""
    reset_educational_package_cache()
    monkeypatch.setattr(
        "app.application.adaptive_decision.policy_v1.packages_for_subject",
        lambda subject_id, mode=None: packages_for_subject("CS1", mode=mode),
    )
    user = make_user("arb-due@example.com")
    subject = publish_subject("ARBDUE")
    journey = runtime.enrol_student(
        user_id=user.id,
        subject_code=subject,
        exam_date=date(2026, 8, 20),
    )
    due_pack_id = "FAKE-ARB-DUE-PACK"
    seq_pack_id = "FAKE-ARB-DUE-SEQ"

    class _Pack:
        def __init__(self, package_id: str, topic_code: str = "1.1") -> None:
            self.package_id = package_id
            self.subject_id = subject
            self.topic_code = topic_code
            self.mode = "learning"
            self.campaign_day = "D1"
            self.display_title = package_id
            self.task_descriptions = ("Read", "Practice")
            self.tomorrow = type("T", (), {"next_topic_code": ""})()

    due_pack = _Pack(due_pack_id)
    seq_pack = _Pack(seq_pack_id, topic_code="2.1")
    monkeypatch.setattr(
        "app.application.educational_packages.guard.certified_guidance_enforced",
        lambda subject_id: True,
    )
    monkeypatch.setattr(
        "app.application.educational_packages.selection.pending_post_tip_front_package",
        lambda **kwargs: None,
    )
    monkeypatch.setattr(
        "app.application.educational_packages.selection.resolve_active_educational_package",
        lambda **kwargs: seq_pack,
    )
    monkeypatch.setattr(
        "app.application.educational_packages.loader.find_package_by_id",
        lambda pid: {due_pack_id: due_pack, seq_pack_id: seq_pack}.get(pid),
    )

    # Completed 2026-07-31 -> due exactly on 2026-08-01.
    get_spacing_scheduler().record_completed_exposure(
        learner_id=str(user.id),
        package_id=due_pack_id,
        completed_on=date(2026, 7, 31),
    )
    twin = _StubTwin(
        facts={
            "2.6.1": _fact("2.6.1", ek=0.410, evidence=5),
            "2.6.2": _fact("2.6.2", ek=0.092, evidence=4),
            "2.6.3": _fact("2.6.3", ek=0.254, evidence=3),
        },
        covered={"2.6.1", "2.6.2", "2.6.3"},
    )
    v1 = PolicyV1AdaptiveDecisionEngine(
        runtime=runtime,
        twin=twin,
        v0=PolicyV0AdaptiveDecisionEngine(runtime=runtime),
    )
    v1._topics_since_last_review = lambda request: 10  # type: ignore[method-assign]
    decision = v1.decide_daily_sitting(
        DailySittingRequest(
            user_id=user.id,
            subject_code=subject,
            mission_date=date(2026, 8, 1),
            curriculum_identity=journey.enrolment.curriculum_identity,
            exam_date=journey.enrolment.exam_date,
        )
    )
    assert decision.outcome == DecisionOutcome.SAFE_FALLBACK
    assert decision.composer_selection_reason == SELECTION_REASON_SPACED_REVIEW
    assert REASON_ARBITRATION_DUE_PROTECTED in decision.reason_codes
    assert decision.educational_package_id == due_pack_id
    labels = decision.selection_trace.get("arbitration_labels") or []
    assert "due_protected" in labels
    assert "adaptive_preempted_due" in labels
    assert "adaptive_candidate" not in labels
    assert decision.selection_trace.get("spacing_status") == "due"
