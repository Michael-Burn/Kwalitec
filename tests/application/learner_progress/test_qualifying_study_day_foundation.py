"""Qualifying study day index and streak foundation tests."""

from __future__ import annotations

import ast
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

from app.application.adaptive_decision.types import POLICY_V1_MIN_EVIDENCE
from app.application.learning_session.dto.candidate_observation import (
    CandidateObservation,
    RuntimeEvidenceType,
)
from app.application.learning_session.dto.evidence_package import (
    SessionEvidencePackage,
)
from app.application.learner_progress.index_document import merge_qualifying_date
from app.application.learner_progress.milestone_detector import (
    LearnerProgressMilestoneDetector,
)
from app.application.learner_progress.milestones import (
    MilestoneKind,
    SectionProgressSpec,
    detect_streak_milestones,
    is_ek_mastered,
)
from app.application.learner_progress.qualifying_package import (
    package_qualifies_for_study_day,
)
from app.application.learner_progress.streak import (
    current_streak_days,
    longest_streak_days,
)
from app.application.student_twin.query import TopicKnowledgeFact
from app.infrastructure.adapters.learner_progress.qualifying_study_day_persistence import (
    QualifyingStudyDayIndexPersistence,
)
from app.infrastructure.adapters.learner_progress.query_adapter import (
    QualifyingStudyDayQueryAdapter,
)
from app.infrastructure.adapters.learning_session.persistence import (
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.adapters.learning_session.runtime_engine import (
    LearningSessionRuntimeEngine,
)
from app.infrastructure.adapters.student_twin.daily_loop_persistence import (
    DailyLoopTwinPersistence,
)
from app.infrastructure.session.store import SessionDocumentStore
from app.services.educational_evidence_authority import EducationalEvidenceAuthority
from tests.application.learning_session.helpers import make_journey, make_objective

FIXED = datetime(2026, 8, 30, 14, 0, tzinfo=UTC)

FORBIDDEN_IMPORT_FRAGMENTS = (
    "educational_packages",
    "educational_campaigns",
    "curriculum.data",
    "curriculum/data",
    "app.curriculum.data",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _learner_progress_app_paths() -> list[Path]:
    root = _repo_root() / "app" / "application" / "learner_progress"
    return sorted(root.rglob("*.py"))


def _learner_progress_infra_paths() -> list[Path]:
    root = _repo_root() / "app" / "infrastructure" / "adapters" / "learner_progress"
    return sorted(root.rglob("*.py"))


def _validated_package(
    *,
    types: tuple[RuntimeEvidenceType, ...],
    created_at: datetime = FIXED,
    student_id: str = "42",
    session_id: str = "lsr-lp-1",
) -> SessionEvidencePackage:
    observations = tuple(
        CandidateObservation.create(
            observation_id=f"obs-{t.value}",
            type_id=t,
            student_id=student_id,
            session_id=session_id,
            topic_id="CS1-A-T01",
            mission_instance_id="m-1",
            recorded_at=created_at,
        )
        for t in types
    )
    package = SessionEvidencePackage.create(
        student_id=student_id,
        session_id=session_id,
        mission_instance_id="m-1",
        topic_id="CS1-A-T01",
        topic_title="Cash flows",
        curriculum_identity="CS1:test",
        learning_objectives=("Explain operating cash flow",),
        observations=observations,
        finish_review_verdict="yes",
        created_at=created_at,
    )
    validation = EducationalEvidenceAuthority.validate_session_evidence_package(
        package
    )
    return package.with_validation(validation)


def _active_engine(monkeypatch, *, twin: bool = True):
    monkeypatch.setenv("SR_EVIDENCE_GATE", "1")
    monkeypatch.setenv("SR_SESSION_COMPLETION_PRODUCT", "1")
    monkeypatch.setenv("SR_SESSION_SUBSTANCE", "1")
    monkeypatch.setenv("SR_SESSION_PRIMARY", "1")
    monkeypatch.setenv("SR_TWIN_DAILY_LOOP", "1" if twin else "0")
    store = SessionDocumentStore()
    persistence = LearningSessionPersistenceAdapter(store=store)
    from app.application.config.v2_flags import resolve_v2_feature_flags
    from app.application.learning_session.runtime import LearningSessionRuntime
    from app.application.student_twin.session_evidence_consumer import (
        SessionTwinEvidenceConsumer,
    )
    from app.application.student_twin.twin_engine import StudentTwinEngine

    lsr = LearningSessionRuntime()
    journey = make_journey(
        topic_id="CS1-A-T01",
        objectives=[make_objective("obj-cash", topic_id="CS1-A-T01")],
    )
    handle = lsr.create_session(journey, session_id="lsr-hold-1")
    handle = lsr.prepare_session(handle)
    handle = lsr.start_session(handle)
    persistence.save_binding(
        student_id="42",
        mission_instance_id="m-1",
        handle=handle,
        topic_title="Cash flows",
        topic_id="CS1-A-T01",
        curriculum_identity="CS1:test",
    )
    twin_store = DailyLoopTwinPersistence(store=store)
    twin_engine = StudentTwinEngine(clock=lambda: FIXED, id_factory=lambda: "eng01")
    consumer = SessionTwinEvidenceConsumer(
        engine=twin_engine,
        store=twin_store,
        clock=lambda: FIXED,
        flag_resolver=resolve_v2_feature_flags,
    )

    class _FakeMissionCompleter:
        def complete_mission(self, **_kwargs) -> None:
            return None

    engine = LearningSessionRuntimeEngine(
        runtime=lsr,
        persistence=persistence,
        mission_completer=_FakeMissionCompleter(),
        twin_consumer=consumer,
    )
    return engine, persistence, twin_store


def _engine_with_store(*, twin: bool, monkeypatch):
    return _active_engine(monkeypatch, twin=twin)


# ---------------------------------------------------------------------------
# Content-path import boundary
# ---------------------------------------------------------------------------


def test_learner_progress_modules_do_not_import_content_authoring_paths():
    offenders: list[str] = []
    for path in _learner_progress_app_paths() + _learner_progress_infra_paths():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            modules: list[str] = []
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                modules = [node.module or ""]
            for mod in modules:
                lowered = mod.replace("\\", "/")
                for frag in FORBIDDEN_IMPORT_FRAGMENTS:
                    if frag in lowered:
                        offenders.append(f"{path.name}:{mod}")
    assert offenders == [], offenders


# ---------------------------------------------------------------------------
# Qualifying day index
# ---------------------------------------------------------------------------


def test_educational_plus_package_indexes_qualifying_day():
    store = SessionDocumentStore()
    persistence = LearningSessionPersistenceAdapter(store=store)
    package = _validated_package(types=(RuntimeEvidenceType.PRACTICE_CORRECT,))
    assert package.validation is not None
    assert package.validation.may_update_twin is True

    persistence.save_evidence_package(
        session_id=package.session_id,
        package=package.to_opaque(),
    )

    index = persistence.qualifying_study_day_index
    doc = index.load_index(learner_id="42")
    assert doc is not None
    assert "2026-08-30" in doc["qualifying_dates"]


def test_behavioural_only_package_does_not_index_qualifying_day():
    store = SessionDocumentStore()
    persistence = LearningSessionPersistenceAdapter(store=store)
    package = _validated_package(types=(RuntimeEvidenceType.PRACTICE_ATTEMPTED,))
    assert package.validation is not None
    assert package.validation.may_update_twin is False
    assert package_qualifies_for_study_day(package.to_opaque()) is False

    persistence.save_evidence_package(
        session_id=package.session_id,
        package=package.to_opaque(),
    )

    doc = persistence.qualifying_study_day_index.load_index(learner_id="42")
    assert doc is None


def test_hold_period_direct_persistence_indexes_fixed_date():
    """Explicit Aug 30 2026 hold date: index records day without Twin involvement."""
    store = SessionDocumentStore()
    persistence = LearningSessionPersistenceAdapter(store=store)
    package = _validated_package(
        types=(RuntimeEvidenceType.PRACTICE_CORRECT,),
        created_at=FIXED,
        session_id="lsr-hold-direct",
    )
    persistence.save_evidence_package(
        session_id=package.session_id,
        package=package.to_opaque(),
    )
    query = QualifyingStudyDayQueryAdapter(index=persistence.qualifying_study_day_index)
    stats = query.streak_stats(
        user_id=42,
        as_of=date(2026, 8, 30),
        lookback_days=90,
    )
    assert date(2026, 8, 30) in stats.qualifying_dates
    assert stats.current_streak_days == 1


def test_flag_off_period_still_indexes_qualifying_day(monkeypatch):
    """Aug 30-31 hold: evidence persists, Twin off, index must still count the day."""
    engine, persistence, twin_store = _engine_with_store(twin=False, monkeypatch=monkeypatch)
    obs = CandidateObservation.create(
        observation_id="obs-hold-1",
        type_id=RuntimeEvidenceType.PRACTICE_CORRECT,
        student_id="42",
        session_id="lsr-hold-1",
        topic_id="CS1-A-T01",
        mission_instance_id="m-1",
        recorded_at=FIXED,
    )
    persistence.append_candidate(session_id="lsr-hold-1", observation=obs.to_opaque())
    result = engine.complete_session_opaque(
        "42",
        session_id="lsr-hold-1",
        finish_verdict="yes",
    )
    assert result is not None
    assert result["twin_updated"] is False
    assert twin_store.load_twin(learner_id="42", subject_code="CS1") is None

    package = persistence.load_evidence_package(session_id="lsr-hold-1")
    assert package is not None
    from app.application.learner_progress.qualifying_package import (
        study_date_from_package,
    )

    study_date = study_date_from_package(package)
    assert study_date is not None

    query = QualifyingStudyDayQueryAdapter(
        index=persistence.qualifying_study_day_index,
    )
    stats = query.streak_stats(
        user_id=42,
        as_of=study_date,
        lookback_days=90,
    )
    assert study_date in stats.qualifying_dates
    assert stats.current_streak_days >= 1


# ---------------------------------------------------------------------------
# Streak calculation
# ---------------------------------------------------------------------------


def test_streak_consecutive_days():
    days = {
        date(2026, 8, 28),
        date(2026, 8, 29),
        date(2026, 8, 30),
    }
    assert current_streak_days(days, as_of=date(2026, 8, 30)) == 3
    assert longest_streak_days(days) == 3


def test_streak_gap_resets_current_preserves_longest():
    days = {
        date(2026, 8, 20),
        date(2026, 8, 21),
        date(2026, 8, 22),
        date(2026, 8, 29),
        date(2026, 8, 30),
    }
    assert current_streak_days(days, as_of=date(2026, 8, 30)) == 2
    assert longest_streak_days(days) == 3

    store = SessionDocumentStore()
    index = QualifyingStudyDayIndexPersistence(store=store)
    doc = None
    for d in sorted(days):
        doc = merge_qualifying_date(doc, learner_id="42", study_date=d)
    index.save_index(learner_id="42", document=doc)

    query = QualifyingStudyDayQueryAdapter(index=index)
    stats = query.streak_stats(user_id=42, as_of=date(2026, 8, 30))
    assert stats.current_streak_days == 2
    assert stats.longest_streak_days == 3


def test_streak_yesterday_counts_when_today_empty():
    days = {date(2026, 8, 30)}
    assert current_streak_days(days, as_of=date(2026, 8, 31)) == 1


# ---------------------------------------------------------------------------
# Milestones
# ---------------------------------------------------------------------------


def test_ek_mastered_milestone_only_when_genuinely_earned():
    mastered = TopicKnowledgeFact(
        topic_id="CS1-A-T01",
        has_estimated_knowledge=True,
        estimated_knowledge=0.92,
        estimated_mastery=0.85,
        evidence_count=POLICY_V1_MIN_EVIDENCE,
        last_practised_at=FIXED,
    )
    insufficient = TopicKnowledgeFact(
        topic_id="CS1-A-T02",
        has_estimated_knowledge=True,
        estimated_knowledge=0.95,
        estimated_mastery=0.90,
        evidence_count=2,
        last_practised_at=FIXED,
    )
    assert is_ek_mastered(mastered) is True
    assert is_ek_mastered(insufficient) is False


def test_streak_milestones_fire_at_thresholds_only_once():
    first = detect_streak_milestones(
        longest_streak_days=7,
        previously_earned=frozenset(),
    )
    assert len(first) == 1
    assert first[0].kind == MilestoneKind.STREAK_DAYS
    assert first[0].milestone_id == "streak_7"

    repeat = detect_streak_milestones(
        longest_streak_days=10,
        previously_earned=frozenset({"streak_7"}),
    )
    assert repeat == ()

    thirty = detect_streak_milestones(
        longest_streak_days=30,
        previously_earned=frozenset({"streak_7"}),
    )
    assert len(thirty) == 1
    assert thirty[0].milestone_id == "streak_30"


def test_section_and_ek_milestones_via_detector():
    mastered_fact = TopicKnowledgeFact(
        topic_id="CS1-A-T01",
        has_estimated_knowledge=True,
        estimated_knowledge=0.92,
        estimated_mastery=0.88,
        evidence_count=POLICY_V1_MIN_EVIDENCE,
        last_practised_at=FIXED,
    )
    twin_adapter = _FakeTwinQuery(facts=(mastered_fact,))
    store = SessionDocumentStore()
    index = QualifyingStudyDayIndexPersistence(store=store)
    for offset in range(7):
        study_date = date(2026, 8, 24) + timedelta(days=offset)
        existing = index.load_index(learner_id="42")
        updated = merge_qualifying_date(
            existing,
            learner_id="42",
            study_date=study_date,
        )
        index.save_index(learner_id="42", document=updated)

    study_day_adapter = QualifyingStudyDayQueryAdapter(index=index)
    detector = LearnerProgressMilestoneDetector(
        twin_query=twin_adapter,
        study_day_query=study_day_adapter,
    )
    sections = (
        SectionProgressSpec(
            section_id="S1",
            title="Section 1",
            topic_ids=frozenset({"CS1-A-T01", "CS1-A-T02"}),
        ),
    )
    earned = detector.detect_new_milestones(
        user_id=42,
        subject_code="CS1",
        sections=sections,
        completed_topic_ids=frozenset({"CS1-A-T01", "CS1-A-T02"}),
        previously_earned=frozenset(),
        as_of=date(2026, 8, 30),
        topic_titles={"CS1-A-T01": "Cash flows"},
    )
    kinds = {m.kind for m in earned}
    assert MilestoneKind.TOPIC_EK_MASTERED in kinds
    assert MilestoneKind.SECTION_STUDY_COMPLETE in kinds
    assert MilestoneKind.STREAK_DAYS in kinds


class _FakeTwinQuery:
    def __init__(self, facts: tuple[TopicKnowledgeFact, ...]) -> None:
        self._facts = facts

    def knowledge_snapshot(self, *, user_id: int, subject_code: str):
        raise NotImplementedError

    def topic_knowledge(self, *, user_id: int, subject_code: str, topic_id: str):
        for fact in self._facts:
            if fact.topic_id == topic_id:
                return fact
        return TopicKnowledgeFact(
            topic_id=topic_id,
            has_estimated_knowledge=False,
            estimated_knowledge=None,
            estimated_mastery=None,
            evidence_count=0,
            last_practised_at=None,
        )

    def topics_with_estimated_knowledge(
        self, *, user_id: int, subject_code: str
    ) -> tuple[TopicKnowledgeFact, ...]:
        return self._facts

    def topic_covered(self, *, user_id: int, subject_code: str, topic_id: str) -> bool:
        return False
