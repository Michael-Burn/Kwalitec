"""Policy V1 activation path proofs (roadmap item 6).

Proves the evidence-to-experience path, not merely that the flag exists:
1. Founder-equivalent evidence posture → SAFE_FALLBACK with plain explanation
2. Evidence-sufficient scenario → real ADAPTIVE decision with adaptive_review
3. Decision durability across process restart (DECISION_RECORDED + mission)
4. Due is never reinterpreted as weak; four selection reasons stay distinct
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

import pytest

from app.application.adaptive_decision import (
    DecisionOutcome,
    PolicyV0AdaptiveDecisionEngine,
    PolicyV1AdaptiveDecisionEngine,
    SittingDecisionOrchestrator,
)
from app.application.adaptive_decision.types import (
    POLICY_V1_ID,
    POLICY_V1_MIN_EVIDENCE,
    REASON_ARBITRATION_DUE_PROTECTED,
    REASON_POLICY_V1_BLOCK_WEAKNESS,
    REASON_POLICY_V1_INSUFFICIENT_EVIDENCE,
    DailySittingRequest,
)
from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.educational_packages.loader import (
    packages_for_subject,
    reset_educational_package_cache,
)
from app.application.educational_runtime_engine.selection_reasons import (
    COMPOSER_SELECTION_REASONS,
    SELECTION_REASON_ADAPTIVE_REVIEW,
    SELECTION_REASON_SEQUENTIAL,
    SELECTION_REASON_SPACED_REVIEW,
    SELECTION_REASON_STUDENT_SELECTED,
)
from app.application.educational_runtime_engine.service import (
    EducationalRuntimeEngineService,
)
from app.application.spacing_scheduler import get_spacing_scheduler
from app.application.student_twin.query import (
    LearnerKnowledgeSnapshot,
    TopicKnowledgeFact,
)
from app.domain.educational_runtime_engine.events import EducationalEventType
from app.domain.spacing_scheduler.types import FORBIDDEN_SIGNAL_NAMES
from app.models.educational_runtime_engine import RuntimeEducationalEvent
from tests.application.educational_runtime_engine.helpers import (
    make_user,
    publish_subject,
)


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


def _fact(topic_id: str, *, ek: float | None, evidence: int) -> TopicKnowledgeFact:
    return TopicKnowledgeFact(
        topic_id=topic_id,
        has_estimated_knowledge=ek is not None,
        estimated_knowledge=ek,
        estimated_mastery=ek,
        evidence_count=evidence,
        last_practised_at=datetime(2026, 8, 1) if evidence else None,
    )


@pytest.fixture()
def runtime(ctx):
    return EducationalRuntimeEngineService()


def test_policy_v1_flag_local_only_absent_from_render():
    """Production must not enable Policy V1; local env may."""
    assert resolve_v2_feature_flags(environ={}).ADR027_POLICY_V1 is False
    assert (
        resolve_v2_feature_flags(
            environ={"KWALITEC_ADR027_POLICY_V1": "1"}
        ).ADR027_POLICY_V1
        is True
    )
    render = Path("render.yaml").read_text(encoding="utf-8")
    assert "KWALITEC_ADR027_POLICY_V1" not in render
    assert "ADR027_POLICY_V1" not in render


def test_founder_equivalent_posture_safe_fallback_with_plain_explanation(
    ctx, runtime
):
    """Mirror founder local reality: no syllabus return_target meets the bar.

    Local observation (instance/kwalitec.sqlite3, user_id=4): Twin document
    holds only synthetic topic CS1-DURABLE-E2E-T01 (not a revision
    return_target). No MISSION_COMPLETED. SAFE_FALLBACK is the only honest
    Policy V1 outcome until real syllabus evidence accumulates.
    """
    user = make_user("founder-equiv-v1@example.com")
    subject = publish_subject("FV1EQ")
    journey = runtime.enrol_student(
        user_id=user.id,
        subject_code=subject,
        exam_date=date(2026, 12, 22),
    )
    # Synthetic non-syllabus evidence only (founder durable e2e leftover shape).
    twin = _StubTwin(
        facts={
            "CS1-DURABLE-E2E-T01": _fact(
                "CS1-DURABLE-E2E-T01", ek=0.254, evidence=3
            )
        },
        covered=set(),
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
            mission_date=date(2026, 9, 9),
            curriculum_identity=journey.enrolment.curriculum_identity,
            exam_date=journey.enrolment.exam_date,
        )
    )
    assert decision.outcome == DecisionOutcome.SAFE_FALLBACK
    assert decision.outcome != DecisionOutcome.ADAPTIVE
    assert decision.policy_id == POLICY_V1_ID
    assert REASON_POLICY_V1_INSUFFICIENT_EVIDENCE in decision.reason_codes
    assert decision.decision_explanation
    assert "Fell back" in decision.decision_explanation
    assert str(POLICY_V1_MIN_EVIDENCE) in decision.decision_explanation
    assert "0 of" in decision.decision_explanation or "only 0 of" in (
        decision.decision_explanation
    )
    assert decision.composer_selection_reason in (
        "",
        SELECTION_REASON_SEQUENTIAL,
    )


def test_evidence_sufficient_produces_explainable_adaptive_decision(
    ctx, runtime, monkeypatch
):
    """Constructed evidence at/above the real threshold yields ADAPTIVE."""
    reset_educational_package_cache()
    monkeypatch.setattr(
        "app.application.adaptive_decision.policy_v1.packages_for_subject",
        lambda subject_id, mode=None: packages_for_subject("CS1", mode=mode),
    )
    user = make_user("v1-adapt-path@example.com")
    subject = publish_subject("V1ADP")
    journey = runtime.enrol_student(
        user_id=user.id,
        subject_code=subject,
        exam_date=date(2026, 8, 20),
    )
    facts = {
        "2.6.1": _fact("2.6.1", ek=0.410, evidence=5),
        "2.6.2": _fact("2.6.2", ek=0.092, evidence=4),
        "2.6.3": _fact("2.6.3", ek=0.254, evidence=3),
    }
    twin = _StubTwin(facts=facts, covered={"2.6.1", "2.6.2", "2.6.3"})
    engine = PolicyV1AdaptiveDecisionEngine(
        runtime=runtime,
        twin=twin,
        v0=PolicyV0AdaptiveDecisionEngine(runtime=runtime),
    )
    engine._topics_since_last_review = lambda request: 10  # type: ignore[method-assign]
    orch = SittingDecisionOrchestrator(runtime=runtime, engine=engine)
    mission = orch.ensure_todays_sitting(
        user_id=user.id,
        subject_code=subject,
        mission_date=date(2026, 8, 1),
    )
    assert (
        mission.educational_package_id
        == "CS1-EP001-PKG-REV-SAMPLING-DISTRIBUTIONS"
    )
    assert mission.composer_selection_reason == SELECTION_REASON_ADAPTIVE_REVIEW
    assert mission.selection_explanation
    assert "adaptive review" in mission.selection_explanation.lower()
    assert "reliable Twin evidence" in mission.selection_explanation

    rows = RuntimeEducationalEvent.query.filter_by(
        user_id=user.id,
        event_type=EducationalEventType.DECISION_RECORDED.value,
    ).all()
    assert rows
    payload = json.loads(rows[-1].payload_json or "{}")
    assert payload["outcome"] == DecisionOutcome.ADAPTIVE.value
    assert payload["policy_id"] == POLICY_V1_ID
    assert payload["composer_selection_reason"] == (
        SELECTION_REASON_ADAPTIVE_REVIEW
    )
    assert payload["decision_explanation"]
    assert REASON_POLICY_V1_BLOCK_WEAKNESS in payload["reason_codes"]
    assert journey.enrolment.enrolment_id


def test_adaptive_decision_survives_process_restart(
    ctx, runtime, monkeypatch
):
    """DECISION_RECORDED + mission identity remain readable after restart."""
    reset_educational_package_cache()
    monkeypatch.setattr(
        "app.application.adaptive_decision.policy_v1.packages_for_subject",
        lambda subject_id, mode=None: packages_for_subject("CS1", mode=mode),
    )
    user = make_user("v1-dur@example.com")
    subject = publish_subject("V1DUR")
    runtime.enrol_student(
        user_id=user.id,
        subject_code=subject,
        exam_date=date(2026, 8, 20),
    )
    twin = _StubTwin(
        facts={
            "2.6.1": _fact("2.6.1", ek=0.410, evidence=5),
            "2.6.2": _fact("2.6.2", ek=0.092, evidence=4),
            "2.6.3": _fact("2.6.3", ek=0.254, evidence=3),
        },
        covered={"2.6.1", "2.6.2", "2.6.3"},
    )
    engine = PolicyV1AdaptiveDecisionEngine(
        runtime=runtime,
        twin=twin,
        v0=PolicyV0AdaptiveDecisionEngine(runtime=runtime),
    )
    engine._topics_since_last_review = lambda request: 10  # type: ignore[method-assign]
    orch = SittingDecisionOrchestrator(runtime=runtime, engine=engine)
    day = date(2026, 8, 1)
    mission = orch.ensure_todays_sitting(
        user_id=user.id, subject_code=subject, mission_date=day
    )
    mission_id = mission.mission_instance_id
    package_id = mission.educational_package_id
    reason = mission.composer_selection_reason
    explanation = mission.selection_explanation

    # Simulate process restart: discard engines, rebuild from durable SQL.
    del orch
    del engine
    del twin
    fresh_runtime = EducationalRuntimeEngineService()
    reloaded = fresh_runtime.try_return_existing_daily_mission(
        user_id=user.id,
        subject_code=subject,
        mission_date=day,
    )
    assert reloaded is not None
    assert reloaded.mission_instance_id == mission_id
    assert reloaded.educational_package_id == package_id
    assert reloaded.composer_selection_reason == reason
    assert reloaded.selection_explanation == explanation

    rows = RuntimeEducationalEvent.query.filter_by(
        user_id=user.id,
        event_type=EducationalEventType.DECISION_RECORDED.value,
    ).all()
    assert rows
    payload = json.loads(rows[-1].payload_json or "{}")
    assert payload["outcome"] == DecisionOutcome.ADAPTIVE.value
    assert payload["educational_package_id"] == package_id
    assert payload["decision_explanation"] == explanation


def test_policy_v1_never_treats_due_as_weak_and_keeps_reasons_distinct(
    ctx, runtime, monkeypatch
):
    """Due (spaced_review) is preserved; adaptive does not consume due as weak."""
    reset_educational_package_cache()
    monkeypatch.setattr(
        "app.application.adaptive_decision.policy_v1.packages_for_subject",
        lambda subject_id, mode=None: packages_for_subject("CS1", mode=mode),
    )
    user = make_user("v1-due-guard@example.com")
    subject = publish_subject("V1DUE")
    journey = runtime.enrol_student(
        user_id=user.id,
        subject_code=subject,
        exam_date=date(2026, 8, 20),
    )

    due_pack_id = "FAKE-V1-DUE-PACK"
    seq_pack_id = "FAKE-V1-SEQ-PACK"

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

    due_pack = _Pack(due_pack_id, topic_code="1.1")
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
    # Due wins: SAFE_FALLBACK with spaced_review, not ADAPTIVE/weak.
    assert decision.outcome == DecisionOutcome.SAFE_FALLBACK
    assert decision.composer_selection_reason == SELECTION_REASON_SPACED_REVIEW
    assert REASON_ARBITRATION_DUE_PROTECTED in decision.reason_codes
    assert "due" in decision.decision_explanation.lower()
    assert "not treated as weak" in decision.decision_explanation.lower()
    assert decision.educational_package_id == due_pack_id
    labels = decision.selection_trace.get("arbitration_labels") or []
    assert "due_protected" in labels
    assert "spaced_due" in labels
    assert "adaptive_preempted_due" in labels
    assert "adaptive_deferred" in labels

    # Four locked reasons remain distinct and non-interchangeable.
    assert COMPOSER_SELECTION_REASONS == {
        SELECTION_REASON_SEQUENTIAL,
        SELECTION_REASON_SPACED_REVIEW,
        SELECTION_REASON_ADAPTIVE_REVIEW,
        SELECTION_REASON_STUDENT_SELECTED,
    }
    assert len(COMPOSER_SELECTION_REASONS) == 4
    from app.application.adaptive_decision.policy_v1 import block_weakness_score

    sig_params = set(block_weakness_score.__code__.co_varnames)
    for forbidden in FORBIDDEN_SIGNAL_NAMES:
        assert forbidden not in sig_params


def test_below_threshold_evidence_explains_partial_count(
    ctx, runtime, monkeypatch
):
    """Honest partial-count explanation when evidence exists but below floor."""
    reset_educational_package_cache()
    monkeypatch.setattr(
        "app.application.adaptive_decision.policy_v1.packages_for_subject",
        lambda subject_id, mode=None: packages_for_subject("CS1", mode=mode),
    )
    user = make_user("v1-partial@example.com")
    subject = publish_subject("V1PART")
    journey = runtime.enrol_student(
        user_id=user.id,
        subject_code=subject,
        exam_date=date(2026, 8, 20),
    )
    twin = _StubTwin(
        facts={
            "2.6.1": _fact("2.6.1", ek=0.2, evidence=1),
            "2.6.2": _fact("2.6.2", ek=0.3, evidence=2),
        },
        covered={"2.6.1", "2.6.2"},
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
    assert "2 of 3" in decision.decision_explanation
    assert decision.selection_trace.get("max_covered_return_target_evidence") == 2
