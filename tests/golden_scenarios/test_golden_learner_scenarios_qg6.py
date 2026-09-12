"""Quality Gate item 6 — golden learner scenarios.

Synthetic but realistic learner histories with explicit expected behaviour
defined as executable specifications. Assertions are grounded in confirmed
current system behaviour (Twin, Spacing, arbitration, Evidence Authority,
coverage gates, student-selected sessions), not assumed ideals.

Finding notes (do not encode broken behaviour as golden success):
- Finding 4 (QG item 4): composer used to let ``memory_pack`` suppress
  due-review selection. Locked precedence is overdue > due > adaptive >
  sequential. Scenario 7 asserts due wins over an owed Memory /
  Publication Front pack (composer now matches arbitration law).
- Finding C (KNOWN_UNKNOWNS §2.6): version-mismatch soft fallback in
  ``map_runtime_syllabus_to_engine``. Scenario 9 asserts historical evidence
  retention and the honest fallback flag; it does not claim remapping is safe.
"""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from types import SimpleNamespace

import pytest

from app.application.adaptive_decision.arbitration import (
    REASON_ARBITRATION_DUE_PROTECTED,
    ArbitrationLabel,
    PrecedenceWinner,
    arbitrate_sitting_precedence,
)
from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.educational_experience import EducationalExperienceService
from app.application.educational_runtime_engine.selection_reasons import (
    SELECTION_REASON_SPACED_REVIEW,
)
from app.application.educational_runtime_engine.service import (
    EducationalRuntimeEngineService,
)
from app.application.learning_session.dto.candidate_observation import (
    CandidateObservation,
    RuntimeEvidenceType,
)
from app.application.learning_session.dto.evidence_package import (
    SessionEvidencePackage,
)
from app.application.learning_session.session_origin import (
    SESSION_ORIGIN_STUDENT_SELECTED,
)
from app.application.platform_integration.discovery import PUBLISHED_CATEGORY_CODE
from app.application.platform_integration.enrolment_bridge import (
    FounderStudentEnrolmentBridge,
)
from app.application.spacing_scheduler import (
    get_spacing_scheduler,
    reset_canonical_spacing_scheduler_for_tests,
)
from app.application.student_runtime import (
    OpenSessionReplacementRequired,
    StudentRuntimeCoordinator,
)
from app.application.student_runtime.syllabus_engine_map import (
    map_runtime_syllabus_to_engine,
)
from app.application.student_twin.policies.confidence_policy import ConfidencePolicy
from app.application.student_twin.policies.mastery_policy import MasteryPolicy
from app.application.student_twin.practiced_identity import (
    resolve_practiced_twin_keys,
)
from app.application.student_twin.session_evidence_consumer import (
    SessionTwinEvidenceConsumer,
)
from app.application.student_twin.twin_engine import StudentTwinEngine
from app.domain.spacing_scheduler.scheduler import SpacingScheduler
from app.domain.spacing_scheduler.types import SchedulingStatus
from app.domain.student_twin.confidence_band import ConfidenceBand
from app.domain.student_twin.evidence_type import EvidenceType
from app.infrastructure.adapters.learning_session.persistence import (
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.adapters.student_twin.daily_loop_persistence import (
    DailyLoopTwinPersistence,
)
from app.infrastructure.session.runtime_adapter import SessionRuntimeAdapter
from app.infrastructure.session.store import SessionDocumentStore
from app.services.educational_evidence_authority import EducationalEvidenceAuthority
from tests.application.educational_runtime_engine.helpers import (
    make_user,
    publish_subject,
)
from tests.application.platform_integration.helpers import (
    bridge_flags,
)
from tests.application.platform_integration.helpers import (
    make_user as make_platform_user,
)
from tests.application.platform_integration.helpers import (
    publish_subject as publish_platform_subject,
)
from tests.application.student_twin.helpers import make_engine
from tests.domain.student_twin.helpers import make_event

FIXED = datetime(2026, 9, 12, 12, 0, tzinfo=UTC)
TOPIC_A = "CS1-A-T01"
TOPIC_B = "CS1-A-T02"
CR_R1_PACKAGE = "CS1-EP001-PKG-REV-PUBLICATION-FRONT-RHO"
TIP_SURROGATE = "CS1-E-T01"


# ---------------------------------------------------------------------------
# Shared builders
# ---------------------------------------------------------------------------


def _practice_event(
    event_id: str,
    *,
    topic_id: str,
    correct: bool,
    day: int = 1,
):
    return make_event(
        event_id,
        EvidenceType.PRACTICE_RESULT,
        day=day,
        topic_id=topic_id,
        outcome="correct" if correct else "incorrect",
        score=1.0 if correct else 0.0,
    )


def _mastery_for(twin, topic_id: str) -> float:
    record = twin.mastery.record_for(topic_id)
    assert record is not None
    return float(record.mastery_score)


def _knowledge_for(twin, topic_id: str) -> float:
    record = twin.knowledge.record_for(topic_id)
    assert record is not None
    return float(record.knowledge_score)


def _session_package(
    *,
    student_id: str,
    session_id: str,
    topic_id: str,
    observations: tuple[CandidateObservation, ...],
    educational_package_id: str = "",
    finish_review_verdict: str = "yes",
) -> SessionEvidencePackage:
    metadata = {}
    if educational_package_id:
        metadata["educational_package_id"] = educational_package_id
    package = SessionEvidencePackage.create(
        student_id=student_id,
        session_id=session_id,
        mission_instance_id="mission-golden",
        topic_id=topic_id,
        topic_title=f"Topic {topic_id}",
        curriculum_identity="CS1:2026",
        learning_objectives=("Practice",),
        observations=observations,
        finish_review_verdict=finish_review_verdict,
        created_at=FIXED,
        session_metadata=metadata,
    )
    validation = EducationalEvidenceAuthority.validate_session_evidence_package(
        package
    )
    return package.with_validation(validation)


def _obs(
    *,
    observation_id: str,
    student_id: str,
    session_id: str,
    topic_id: str,
    correct: bool,
) -> CandidateObservation:
    return CandidateObservation.create(
        observation_id=observation_id,
        type_id=(
            RuntimeEvidenceType.PRACTICE_CORRECT
            if correct
            else RuntimeEvidenceType.PRACTICE_INCORRECT
        ),
        student_id=student_id,
        session_id=session_id,
        topic_id=topic_id,
        mission_instance_id="mission-golden",
        recorded_at=FIXED,
        payload={"scored_correct": correct},
    )


@pytest.fixture(autouse=True)
def _reset_spacing_store():
    reset_canonical_spacing_scheduler_for_tests()
    yield
    reset_canonical_spacing_scheduler_for_tests()


# ---------------------------------------------------------------------------
# 1. Consistently correct learner
# ---------------------------------------------------------------------------


def test_golden_01_consistently_correct_mastery_ceiling_and_spacing():
    """Correct practice raises mastery/EK to the ceiling; spacing from exposure."""
    engine = make_engine(fixed_time=FIXED)
    twin = engine.create_twin("golden-correct", twin_id="twin-g1", subject_code="CS1")

    # Several sittings of correct practice (enough to exceed the ceiling).
    events = [
        _practice_event(f"ok-{i}", topic_id=TOPIC_A, correct=True, day=1 + (i % 20))
        for i in range(15)
    ]
    twin = engine.ingest_many(twin, events)

    mastery = _mastery_for(twin, TOPIC_A)
    knowledge = _knowledge_for(twin, TOPIC_A)
    assert mastery == MasteryPolicy.MAX_MASTERY
    # Soft per-event nudges push EK to the ceiling alongside mastery.
    assert knowledge == MasteryPolicy.MAX_MASTERY
    assert twin.event_count == 15
    assert len(twin.history.events_for_topic(TOPIC_A)) == 15

    # Evidence gate: scored correct practice is Educational+ and advances coverage.
    package = _session_package(
        student_id="golden-correct",
        session_id="lsr-g1",
        topic_id=TOPIC_A,
        observations=(
            _obs(
                observation_id="g1-1",
                student_id="golden-correct",
                session_id="lsr-g1",
                topic_id=TOPIC_A,
                correct=True,
            ),
        ),
    )
    assert package.validation is not None
    assert package.validation.reason == "educational_practice_accepted"
    assert package.validation.may_complete_mission is True
    assert package.validation.may_advance_progress is True
    assert package.validation.may_update_twin is True

    # Spacing schedules the next review from the real completion date.
    scheduler = SpacingScheduler()
    completed_on = date(2026, 9, 1)
    state = scheduler.apply_completed_exposure(
        learner_id="golden-correct",
        unit_id="pkg-g1",
        completed_on=completed_on,
        prior=None,
    )
    assert state.last_completed_on == completed_on
    assert state.current_interval_days == 1
    assert state.next_due_on == completed_on + timedelta(days=1)
    on_due = scheduler.evaluate(
        learner_id="golden-correct",
        unit_id="pkg-g1",
        as_of=state.next_due_on,
        state=state,
    )
    assert on_due.status is SchedulingStatus.DUE


# ---------------------------------------------------------------------------
# 2. Consistently incorrect learner
# ---------------------------------------------------------------------------


def test_golden_02_consistently_incorrect_floor_and_coverage_still_advances():
    """Incorrect practice floors mastery; scored incorrect still gates coverage."""
    engine = make_engine(fixed_time=FIXED)
    twin = engine.create_twin("golden-wrong", twin_id="twin-g2", subject_code="CS1")

    # Seed near the middle, then drive toward the floor with incorrect answers.
    seed = [
        _practice_event(f"seed-{i}", topic_id=TOPIC_A, correct=True, day=1)
        for i in range(5)
    ]
    twin = engine.ingest_many(twin, seed)
    mid = _mastery_for(twin, TOPIC_A)
    assert mid == pytest.approx(0.40, abs=1e-9)

    wrong = [
        _practice_event(
            f"bad-{i}", topic_id=TOPIC_A, correct=False, day=2 + (i % 20)
        )
        for i in range(15)
    ]
    twin = engine.ingest_many(twin, wrong)
    mastery = _mastery_for(twin, TOPIC_A)
    assert mastery == MasteryPolicy.MIN_MASTERY
    assert 0.0 <= _knowledge_for(twin, TOPIC_A) <= 1.0
    assert twin.event_count == 20
    assert all(
        e.outcome == "incorrect" or e.outcome == "correct"
        for e in twin.history.events_for_topic(TOPIC_A)
    )

    # Scored PRACTICE_INCORRECT is Educational grade → educational_practice_accepted
    # (not behavioural-only practice_participation_accepted). Coverage advances;
    # Twin may update even though every answer is wrong.
    package = _session_package(
        student_id="golden-wrong",
        session_id="lsr-g2",
        topic_id=TOPIC_A,
        observations=(
            _obs(
                observation_id="g2-1",
                student_id="golden-wrong",
                session_id="lsr-g2",
                topic_id=TOPIC_A,
                correct=False,
            ),
            _obs(
                observation_id="g2-2",
                student_id="golden-wrong",
                session_id="lsr-g2",
                topic_id=TOPIC_A,
                correct=False,
            ),
        ),
    )
    assert package.validation is not None
    assert package.validation.reason == "educational_practice_accepted"
    assert package.validation.may_complete_mission is True
    assert package.validation.may_advance_progress is True
    assert package.validation.may_update_twin is True
    assert package.validation.highest_grade == "educational"


# ---------------------------------------------------------------------------
# 3. Alternating learner
# ---------------------------------------------------------------------------


def test_golden_03_alternating_correct_incorrect_bounded_and_attributed():
    """Mastery moves both ways within bounds; every submission stays attributed."""
    engine = make_engine(fixed_time=FIXED)
    twin = engine.create_twin("golden-alt", twin_id="twin-g3", subject_code="CS1")

    sequence = [True, False, True, False, True]
    expected = MasteryPolicy.INITIAL_MASTERY
    for i, correct in enumerate(sequence):
        twin = engine.ingest_evidence(
            twin,
            _practice_event(
                f"alt-{i}", topic_id=TOPIC_A, correct=correct, day=1 + i
            ),
        )
        delta = MasteryPolicy.weight_for(EvidenceType.PRACTICE_RESULT) * (
            1.0 if correct else -1.0
        )
        expected = MasteryPolicy.apply_delta(expected, delta)
        assert _mastery_for(twin, TOPIC_A) == pytest.approx(expected, abs=1e-9)
        assert MasteryPolicy.MIN_MASTERY <= _mastery_for(twin, TOPIC_A) <= (
            MasteryPolicy.MAX_MASTERY
        )

    # Final: +0.08 -0.08 +0.08 -0.08 +0.08 = 0.08
    assert _mastery_for(twin, TOPIC_A) == pytest.approx(0.08, abs=1e-9)
    events = twin.history.events_for_topic(TOPIC_A)
    assert len(events) == 5
    assert [e.outcome for e in events] == [
        "correct",
        "incorrect",
        "correct",
        "incorrect",
        "correct",
    ]
    assert all(e.topic_id == TOPIC_A for e in events)


# ---------------------------------------------------------------------------
# 4. Strong topic A / weak topic B (identity separation)
# ---------------------------------------------------------------------------


def test_golden_04_strong_a_weak_b_topics_stay_separate_and_attributed(
    ctx, monkeypatch
):
    """Correct on A and incorrect on B must not conflate Twin topic identity."""
    engine = make_engine(fixed_time=FIXED)
    twin = engine.create_twin("golden-ab", twin_id="twin-g4", subject_code="CS1")

    for i in range(6):
        twin = engine.ingest_evidence(
            twin,
            _practice_event(f"a-{i}", topic_id=TOPIC_A, correct=True, day=1 + i),
        )
    for i in range(6):
        twin = engine.ingest_evidence(
            twin,
            _practice_event(f"b-{i}", topic_id=TOPIC_B, correct=False, day=1 + i),
        )

    mastery_a = _mastery_for(twin, TOPIC_A)
    mastery_b = _mastery_for(twin, TOPIC_B)
    assert mastery_a == pytest.approx(0.48, abs=1e-9)
    assert mastery_b == MasteryPolicy.MIN_MASTERY
    assert mastery_a > mastery_b
    assert {r.topic_id for r in twin.mastery.topic_records} == {TOPIC_A, TOPIC_B}
    assert all(e.topic_id == TOPIC_A for e in twin.history.events_for_topic(TOPIC_A))
    assert all(e.topic_id == TOPIC_B for e in twin.history.events_for_topic(TOPIC_B))

    # Same identity class as tonight's tip-surrogate bugs: return_targets must
    # resolve away from the tip surrogate, never collapse A/B into tip 5.1.
    from tests.application.adaptive_decision.test_policy_v1 import _cs1_canonical

    canonical = _cs1_canonical()
    resolution = resolve_practiced_twin_keys(
        educational_package_id=CR_R1_PACKAGE,
        subject_code="CS1",
        canonical=canonical,
    )
    assert resolution.source == "return_targets"
    assert resolution.unresolved is False
    assert TIP_SURROGATE not in resolution.twin_keys
    assert TOPIC_A in resolution.twin_keys
    assert TOPIC_B in resolution.twin_keys

    # Consumer path with tip-surrogate mission topic + CR package id fans out
    # to return_targets, not the tip surrogate.
    flags = resolve_v2_feature_flags(environ={"SR_TWIN_DAILY_LOOP": "1"})
    store = SessionDocumentStore()
    twin_store = DailyLoopTwinPersistence(store=store)
    consumer = SessionTwinEvidenceConsumer(
        engine=StudentTwinEngine(clock=lambda: FIXED, id_factory=lambda: "g4"),
        store=twin_store,
        clock=lambda: FIXED,
        id_factory=lambda: "g4",
        flag_resolver=lambda: flags,
    )
    monkeypatch.setattr(
        consumer,
        "_practiced_twin_keys",
        lambda pkg: resolve_practiced_twin_keys(
            educational_package_id=CR_R1_PACKAGE,
            subject_code="CS1",
            canonical=canonical,
        ),
    )
    package = _session_package(
        student_id="42",
        session_id="lsr-g4",
        topic_id=TIP_SURROGATE,
        educational_package_id=CR_R1_PACKAGE,
        observations=(
            _obs(
                observation_id="g4-cr",
                student_id="42",
                session_id="lsr-g4",
                topic_id=TIP_SURROGATE,
                correct=True,
            ),
        ),
    )
    result = consumer.consume(package)
    assert result.twin_updated is True
    assert TIP_SURROGATE not in (result.estimated_mastery or {})
    assert TOPIC_A in (result.estimated_mastery or {})
    assert TOPIC_B in (result.estimated_mastery or {})


# ---------------------------------------------------------------------------
# 5. Sparse-evidence learner
# ---------------------------------------------------------------------------


def test_golden_05_sparse_evidence_produces_number_without_mastery_gate():
    """Thin evidence still yields a Twin number; no denser-evidence mastery gate.

    KNOWN_UNKNOWNS §2.3: sparse mastery is unproven and currently ungated.
    Assert the real mechanics honestly, including that volume confidence is
    low while a numeric EK still appears.
    """
    engine = make_engine(fixed_time=FIXED)
    twin = engine.create_twin("golden-sparse", twin_id="twin-g5", subject_code="CS1")
    twin = engine.ingest_evidence(
        twin,
        _practice_event("sparse-1", topic_id=TOPIC_A, correct=True, day=1),
    )

    mastery = _mastery_for(twin, TOPIC_A)
    knowledge = _knowledge_for(twin, TOPIC_A)
    record = twin.mastery.record_for(TOPIC_A)
    assert record is not None
    assert len(record.evidence_ids) == 1
    assert mastery == pytest.approx(0.08, abs=1e-9)
    topic_events = twin.history.events_for_topic(TOPIC_A)
    # EK = clamp(mastery * 0.95 + 0.02) plus a small per-event soft nudge.
    base_ek = mastery * 0.95 + 0.02
    soft_nudge = MasteryPolicy.delta_for(topic_events[0]) * 0.25 * 0.1
    assert knowledge == pytest.approx(
        max(0.0, min(1.0, base_ek + soft_nudge)), abs=1e-9
    )

    # Volume component is low (1/10 saturation). Consistency alone can still
    # lift the combined confidence score into MEDIUM; that is the ungated gap.
    volume = ConfidencePolicy.volume_score(len(topic_events))
    combined = ConfidencePolicy.score_for(topic_events)
    assert volume == pytest.approx(0.1, abs=1e-9)
    assert combined < 0.65  # below HIGH / VERY_HIGH thresholds
    assert record.confidence in {
        ConfidenceBand.VERY_LOW,
        ConfidenceBand.LOW,
        ConfidenceBand.MEDIUM,
    }
    # No refuse-mastery gate: a number exists despite thin evidence.
    assert mastery > 0.0
    assert knowledge > 0.0


# ---------------------------------------------------------------------------
# 6. Old evidence + newly due review
# ---------------------------------------------------------------------------


def test_golden_06_old_exposure_newly_due_wins_composer_precedence(ctx, monkeypatch):
    """Calendar due-day is DUE (not overdue, not still not-due) and wins composition."""
    user = make_user("golden-due@example.com")
    subject = publish_subject("GLDUE")
    runtime = EducationalRuntimeEngineService()
    runtime.enrol_student(user_id=user.id, subject_code=subject)

    package_due = "GOLDEN-DUE-PACK"
    package_seq = "GOLDEN-SEQ-PACK"

    class _Pack:
        def __init__(self, package_id: str, topic_code: str = "1.1") -> None:
            self.package_id = package_id
            self.subject_id = subject
            self.topic_code = topic_code
            self.mode = "learning"
            self.campaign_day = "D1"
            self.display_title = package_id
            self.task_descriptions = ("Read", "Practice")
            self.tomorrow = SimpleNamespace(next_topic_code="")

    due_pack = _Pack(package_due)
    seq_pack = _Pack(package_seq, topic_code="2.1")
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
        lambda pid: {package_due: due_pack, package_seq: seq_pack}.get(pid),
    )

    completed_on = date(2026, 9, 1)
    due_on = completed_on + timedelta(days=1)
    scheduler = get_spacing_scheduler()
    scheduler.record_completed_exposure(
        learner_id=str(user.id),
        package_id=package_due,
        completed_on=completed_on,
    )
    decision = scheduler.evaluate(
        learner_id=str(user.id),
        package_id=package_due,
        as_of=due_on,
    )
    assert decision.status is SchedulingStatus.DUE
    assert decision.days_until_due == 0
    # Day before due remains not-due; day after due becomes overdue.
    before = scheduler.evaluate(
        learner_id=str(user.id),
        package_id=package_due,
        as_of=completed_on,
    )
    assert before.status is SchedulingStatus.NOT_DUE
    after = scheduler.evaluate(
        learner_id=str(user.id),
        package_id=package_due,
        as_of=due_on + timedelta(days=1),
    )
    assert after.status is SchedulingStatus.OVERDUE

    # Locked arbitration: due beats adaptive and sequential labels.
    arb = arbitrate_sitting_precedence(
        protected_status=SchedulingStatus.DUE,
        has_adaptive_candidate=True,
    )
    assert arb.winner is PrecedenceWinner.DUE
    assert arb.reason_code == REASON_ARBITRATION_DUE_PROTECTED
    assert arb.composer_selection_reason == SELECTION_REASON_SPACED_REVIEW

    mission = runtime.generate_daily_mission(
        user_id=user.id,
        subject_code=subject,
        mission_date=due_on,
    )
    assert mission.educational_package_id == package_due
    assert mission.composer_selection_reason == SELECTION_REASON_SPACED_REVIEW


# ---------------------------------------------------------------------------
# 7. Adaptive vs spaced conflict (+ due beats memory_pack)
# ---------------------------------------------------------------------------


def test_golden_07_due_spaced_beats_adaptive_and_memory_pack(ctx, monkeypatch):
    """Locked precedence: due spaced review beats adaptive and memory_pack."""
    with_adaptive = arbitrate_sitting_precedence(
        protected_status=SchedulingStatus.DUE,
        has_adaptive_candidate=True,
    )
    assert with_adaptive.winner is PrecedenceWinner.DUE
    assert with_adaptive.reason_code == REASON_ARBITRATION_DUE_PROTECTED
    assert ArbitrationLabel.DUE_PROTECTED in with_adaptive.labels

    overdue = arbitrate_sitting_precedence(
        protected_status=SchedulingStatus.OVERDUE,
        has_adaptive_candidate=True,
    )
    assert overdue.winner is PrecedenceWinner.OVERDUE

    adaptive_only = arbitrate_sitting_precedence(
        protected_status=None,
        has_adaptive_candidate=True,
    )
    assert adaptive_only.winner is PrecedenceWinner.ADAPTIVE

    user = make_user("golden-arb@example.com")
    subject = publish_subject("GLARB")
    runtime = EducationalRuntimeEngineService()
    runtime.enrol_student(user_id=user.id, subject_code=subject)

    package_due = "GOLDEN-ARB-DUE"
    package_seq = "GOLDEN-ARB-SEQ"

    class _Pack:
        def __init__(self, package_id: str, topic_code: str = "1.1") -> None:
            self.package_id = package_id
            self.subject_id = subject
            self.topic_code = topic_code
            self.mode = "learning"
            self.campaign_day = "D1"
            self.display_title = package_id
            self.task_descriptions = ("Read", "Practice")
            self.tomorrow = SimpleNamespace(next_topic_code="")

    due_pack = _Pack(package_due)
    seq_pack = _Pack(package_seq, topic_code="2.1")
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
        lambda pid: {package_due: due_pack, package_seq: seq_pack}.get(pid),
    )
    completed_on = date(2026, 8, 20)
    due_on = completed_on + timedelta(days=1)
    get_spacing_scheduler().record_completed_exposure(
        learner_id=str(user.id),
        package_id=package_due,
        completed_on=completed_on,
    )
    mission = runtime.generate_daily_mission(
        user_id=user.id,
        subject_code=subject,
        mission_date=due_on,
    )
    assert mission.educational_package_id == package_due
    assert mission.composer_selection_reason == SELECTION_REASON_SPACED_REVIEW

    # Finding 4 closed: owed memory_pack must not suppress a due review.
    memory_pack = _Pack("GOLDEN-MEMORY-PACK", topic_code="1.1")
    monkeypatch.setattr(
        "app.application.educational_packages.selection.pending_post_tip_front_package",
        lambda **kwargs: memory_pack,
    )
    monkeypatch.setattr(
        "app.application.educational_packages.loader.find_package_by_id",
        lambda pid: {
            package_due: due_pack,
            package_seq: seq_pack,
            memory_pack.package_id: memory_pack,
        }.get(pid),
    )
    still_due = get_spacing_scheduler().evaluate(
        learner_id=str(user.id),
        package_id=package_due,
        as_of=due_on,
    )
    assert still_due.status is SchedulingStatus.DUE
    memory_mission = runtime.generate_daily_mission(
        user_id=user.id,
        subject_code=subject,
        mission_date=due_on,
    )
    assert memory_mission.educational_package_id == package_due
    assert memory_mission.composer_selection_reason == SELECTION_REASON_SPACED_REVIEW


# ---------------------------------------------------------------------------
# 8. Student-selected start mid-mission
# ---------------------------------------------------------------------------


def _enrol_runtime_c(user, subject: str) -> None:
    bridge = FounderStudentEnrolmentBridge(flags=bridge_flags())
    result = bridge.enrol(
        user_id=user.id,
        category_code=PUBLISHED_CATEGORY_CODE,
        subject_code=subject,
        exam_date=date.today() + timedelta(days=120),
    )
    assert result.runtime_authority == "published_curriculum"


def _coordinator(store: SessionDocumentStore | None = None):
    store = store or SessionDocumentStore()
    persistence = LearningSessionPersistenceAdapter(store=store)
    overview = SessionRuntimeAdapter(store=store, auto_provision=False)
    flags = resolve_v2_feature_flags(environ={"SR_SESSION_PRIMARY": "1"})
    coordinator = StudentRuntimeCoordinator(
        persistence=persistence,
        session_overview_writer=overview,
        flags=flags,
    )
    return coordinator, persistence


def test_golden_08_student_selected_mid_mission_requires_replace_confirm(
    ctx, monkeypatch
):
    """Open system sitting blocks student-selected start unless replace confirmed.

    Intended design: continue-studying / student-selected is an honest separate
    origin that does not silently steal the open mission pointer. Without
    ``replace_unfinished=True``, raise OpenSessionReplacementRequired and leave
    the system sitting open. With confirmation, launch student-selected with
    empty mission_instance_id (cannot complete today's recommended mission).
    """
    monkeypatch.setenv("SR_SESSION_PRIMARY", "1")
    subject = publish_platform_subject("GLSEL", title="Golden Select")
    user = make_platform_user("golden-select@example.com")
    _enrol_runtime_c(user, subject)
    snap = EducationalExperienceService().load_for_user(user.id)
    assert snap is not None and snap.mission is not None

    progress = EducationalRuntimeEngineService().get_study_progress(
        user_id=user.id, subject_code=subject
    )
    current = progress.current_topic_id
    assert current

    coordinator, persistence = _coordinator()
    system_binding = coordinator.accept_and_start_session(
        user_id=user.id,
        mission_instance_id=snap.mission.mission_instance_id,
        topic_title=snap.mission.topic_title,
        estimated_minutes=30,
    )
    assert system_binding.session_id
    assert str(system_binding.mission_instance_id or "").strip()

    with pytest.raises(OpenSessionReplacementRequired) as raised:
        coordinator.start_student_selected_session(
            user_id=user.id,
            topic_id=current,
            subject_code=subject,
            replace_unfinished=False,
        )
    assert raised.value.session_id == system_binding.session_id
    still = coordinator.find_open_session(str(user.id))
    assert still is not None
    assert still.session_id == system_binding.session_id

    replaced = coordinator.start_student_selected_session(
        user_id=user.id,
        topic_id=current,
        subject_code=subject,
        replace_unfinished=True,
    )
    assert replaced.session_origin == SESSION_ORIGIN_STUDENT_SELECTED
    assert replaced.mission_instance_id == ""
    assert replaced.session_id != system_binding.session_id
    record = persistence.load(session_id=replaced.session_id)
    assert record is not None
    assert record.get("session_origin") == SESSION_ORIGIN_STUDENT_SELECTED
    assert not str(record.get("mission_instance_id") or "").strip()


# ---------------------------------------------------------------------------
# 9. Content version change after evidence
# ---------------------------------------------------------------------------


def test_golden_09_prior_evidence_retained_version_mismatch_fallback_honest(ctx):
    """Prior Twin evidence keeps write-time topic identity; version fallback flagged.

    There is no automatic invalidation of historical practice when curriculum
    version labels drift. ``map_runtime_syllabus_to_engine`` soft-falls back to
    the latest engine version and sets ``version_mismatch_fallback`` (Finding C
    class risk). Golden assertion: retention + honest flag, not safe remapping.
    """
    engine = make_engine(fixed_time=FIXED)
    twin = engine.create_twin("golden-ver", twin_id="twin-g9", subject_code="CS1")
    twin = engine.ingest_evidence(
        twin,
        _practice_event("ver-1", topic_id=TOPIC_A, correct=True, day=1),
    )
    before_ids = [e.event_id for e in twin.history.events_for_topic(TOPIC_A)]
    before_topics = {e.topic_id for e in twin.history.events}
    assert before_ids == ["ver-1"]
    assert before_topics == {TOPIC_A}

    # Later practice on the same recorded identity does not rewrite history.
    twin = engine.ingest_evidence(
        twin,
        _practice_event("ver-2", topic_id=TOPIC_A, correct=True, day=2),
    )
    history = twin.history.events_for_topic(TOPIC_A)
    assert [e.event_id for e in history] == ["ver-1", "ver-2"]
    assert all(e.topic_id == TOPIC_A for e in history)
    assert _mastery_for(twin, TOPIC_A) == pytest.approx(0.16, abs=1e-9)

    # Version label that cannot match on-disk engine years → soft fallback.
    mapped = map_runtime_syllabus_to_engine("CS1", "2099.9-nonexistent")
    assert mapped is not None
    assert mapped.version_mismatch_fallback is True
    assert mapped.paper.upper() == "CS1"
    # Exact matching version (when present) must not set the fallback flag.
    exact = map_runtime_syllabus_to_engine("CS1", mapped.version)
    assert exact is not None
    assert exact.version_mismatch_fallback is False
    assert exact.version == mapped.version
