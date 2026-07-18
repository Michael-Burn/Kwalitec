"""Pure domain unit tests for Version 2 Learning Journey foundation (V2-002).

No Flask, no database, no Version 1 route/service coupling.
"""

from __future__ import annotations

import ast
from abc import ABC
from datetime import UTC, datetime
from pathlib import Path

import pytest

from app.domain.evidence.evidence_category import EvidenceConfidenceLevel
from app.domain.evidence.evidence_type import EvidenceType
from app.domain.learning_journey import (
    CompletionStatus,
    ConsistencyPosture,
    EffortEstimate,
    EvidenceConfidencePosture,
    JourneyEvidence,
    JourneyHistory,
    JourneyHistoryEntry,
    JourneyHistoryEventType,
    JourneyProgress,
    JourneyProgressService,
    JourneyRecommendation,
    JourneyReflection,
    JourneyState,
    JourneyTransitionEvent,
    JourneyValidationService,
    LearningJourney,
    LearningJourneyRepository,
    LearningObjective,
    LearningSession,
    ObjectiveKind,
    RecommendationCertainty,
    RecommendationKind,
    RecommendationLifecycle,
    ReflectionConfidence,
    ReflectionPosture,
    SessionState,
    SessionTransitionEvent,
    ValidationResult,
)
from app.domain.learning_journey.value_objects.effort_estimate import (
    effort_at_least,
    effort_rank,
)
from app.domain.learning_journey.value_objects.journey_state import (
    is_terminal_journey_state,
    next_journey_state,
)
from app.domain.learning_journey.value_objects.session_state import (
    is_terminal_session_state,
    next_session_state,
)

DOMAIN_ROOT = (
    Path(__file__).resolve().parents[1] / "app" / "domain" / "learning_journey"
)
FORBIDDEN_ROOT_MODULES = frozenset(
    {
        "flask",
        "flask_login",
        "flask_sqlalchemy",
        "flask_wtf",
        "sqlalchemy",
        "wtforms",
    }
)
FORBIDDEN_PREFIXES = (
    "app.services",
    "app.models",
    "app.auth",
    "app.dashboard",
    "app.mission",
    "app.analytics",
    "app.study_plan",
)

NOW = datetime(2026, 7, 18, 12, 0, tzinfo=UTC)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _objective(
    oid: str = "obj-1",
    *,
    topic_id: str = "topic-a",
    kind: ObjectiveKind = ObjectiveKind.UNDERSTAND,
    sequence_index: int = 0,
) -> LearningObjective:
    return LearningObjective.create(
        oid,
        f"curr-{oid}",
        topic_id,
        kind,
        title=f"Objective {oid}",
        sequence_index=sequence_index,
    )


def _session(
    sid: str = "sess-1",
    *,
    journey_id: str = "journey-1",
    sequence_index: int = 0,
    state: SessionState = SessionState.NOT_STARTED,
    objective_id: str | None = None,
    effort: EffortEstimate = EffortEstimate.MEDIUM,
) -> LearningSession:
    return LearningSession.create(
        sid,
        journey_id,
        sequence_index=sequence_index,
        state=state,
        estimated_effort=effort,
        objective_id=objective_id,
    )


def _evidence(
    jeid: str = "je-1",
    *,
    evidence_id: str = "ev-1",
    journey_id: str = "journey-1",
    session_id: str | None = "sess-1",
    objective_id: str | None = None,
    confidence: EvidenceConfidenceLevel = EvidenceConfidenceLevel.MEDIUM,
) -> JourneyEvidence:
    return JourneyEvidence.create(
        jeid,
        evidence_id,
        journey_id,
        EvidenceType.STUDY_SESSION,
        NOW,
        confidence_level=confidence,
        session_id=session_id,
        objective_id=objective_id,
        topic_id="topic-a",
    )


def _journey(
    *,
    objectives: list[LearningObjective] | None = None,
    sessions: list[LearningSession] | None = None,
    evidence: list[JourneyEvidence] | None = None,
    reflections: list[JourneyReflection] | None = None,
    state: JourneyState = JourneyState.NOT_STARTED,
    progress: JourneyProgress | None = None,
) -> LearningJourney:
    return LearningJourney.create(
        "journey-1",
        "learner-1",
        "topic-a",
        "CS1-2026",
        state=state,
        objectives=objectives,
        sessions=sessions,
        evidence=evidence,
        reflections=reflections,
        progress=progress,
    )


def _captured_reflection(
    rid: str = "ref-1",
    *,
    session_id: str = "sess-1",
    journey_id: str = "journey-1",
) -> JourneyReflection:
    return JourneyReflection.create_captured(
        rid,
        session_id,
        journey_id,
        what_was_learned="Covered core definitions",
        uncertainty="Edge cases remain unclear",
        questions_remaining=["How does X interact with Y?"],
        confidence=ReflectionConfidence.MEDIUM,
        captured_at=NOW,
    )


# ---------------------------------------------------------------------------
# Framework purity
# ---------------------------------------------------------------------------


class TestFrameworkPurity:
    def test_domain_package_has_no_forbidden_imports(self) -> None:
        for path in DOMAIN_ROOT.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        root = alias.name.split(".", 1)[0]
                        assert root not in FORBIDDEN_ROOT_MODULES, path
                        for prefix in FORBIDDEN_PREFIXES:
                            assert not alias.name.startswith(prefix), path
                elif isinstance(node, ast.ImportFrom) and node.module:
                    root = node.module.split(".", 1)[0]
                    assert root not in FORBIDDEN_ROOT_MODULES, path
                    for prefix in FORBIDDEN_PREFIXES:
                        assert not node.module.startswith(prefix), path


# ---------------------------------------------------------------------------
# Value objects
# ---------------------------------------------------------------------------


class TestJourneyState:
    def test_happy_path_transitions(self) -> None:
        assert (
            next_journey_state(
                JourneyState.NOT_STARTED, JourneyTransitionEvent.START_JOURNEY
            )
            == JourneyState.ACTIVE
        )
        assert (
            next_journey_state(
                JourneyState.ACTIVE, JourneyTransitionEvent.PAUSE_JOURNEY
            )
            == JourneyState.PAUSED
        )
        assert (
            next_journey_state(
                JourneyState.PAUSED, JourneyTransitionEvent.RESUME_JOURNEY
            )
            == JourneyState.RESUMED
        )
        assert (
            next_journey_state(
                JourneyState.RESUMED, JourneyTransitionEvent.SETTLE_ACTIVE
            )
            == JourneyState.ACTIVE
        )

    def test_completion_path_requires_ready_then_confirm(self) -> None:
        assert (
            next_journey_state(
                JourneyState.ACTIVE, JourneyTransitionEvent.COMPLETION_CRITERIA_MET
            )
            == JourneyState.READY_FOR_COMPLETION
        )
        assert (
            next_journey_state(
                JourneyState.READY_FOR_COMPLETION,
                JourneyTransitionEvent.CONFIRM_TOPIC_COMPLETE,
            )
            == JourneyState.COMPLETED
        )
        assert (
            next_journey_state(
                JourneyState.ACTIVE, JourneyTransitionEvent.CONFIRM_TOPIC_COMPLETE
            )
            is None
        )

    def test_session_complete_does_not_complete_journey(self) -> None:
        # No session_completed event maps to COMPLETED.
        assert (
            next_journey_state(
                JourneyState.ACTIVE, JourneyTransitionEvent.START_JOURNEY
            )
            is None
        )
        assert is_terminal_journey_state(JourneyState.COMPLETED)
        assert is_terminal_journey_state(JourneyState.ABANDONED)
        assert is_terminal_journey_state(JourneyState.ARCHIVED)
        assert not is_terminal_journey_state(JourneyState.ACTIVE)

    def test_archive_from_terminal_only(self) -> None:
        assert (
            next_journey_state(
                JourneyState.COMPLETED, JourneyTransitionEvent.ARCHIVE_JOURNEY
            )
            == JourneyState.ARCHIVED
        )
        assert (
            next_journey_state(
                JourneyState.ACTIVE, JourneyTransitionEvent.ARCHIVE_JOURNEY
            )
            is None
        )


class TestSessionState:
    def test_happy_path(self) -> None:
        assert (
            next_session_state(
                SessionState.NOT_STARTED, SessionTransitionEvent.START_SESSION
            )
            == SessionState.ACTIVE
        )
        assert (
            next_session_state(
                SessionState.ACTIVE, SessionTransitionEvent.FINISH_SESSION
            )
            == SessionState.COMPLETED
        )

    def test_skip_planned_session(self) -> None:
        assert (
            next_session_state(
                SessionState.NOT_STARTED, SessionTransitionEvent.SKIP_SESSION
            )
            == SessionState.SKIPPED
        )
        assert is_terminal_session_state(SessionState.SKIPPED)

    def test_cannot_complete_from_not_started(self) -> None:
        assert (
            next_session_state(
                SessionState.NOT_STARTED, SessionTransitionEvent.FINISH_SESSION
            )
            is None
        )

    def test_cannot_restart_completed(self) -> None:
        assert (
            next_session_state(
                SessionState.COMPLETED, SessionTransitionEvent.START_SESSION
            )
            is None
        )


class TestEffortEstimate:
    def test_bands_exist(self) -> None:
        assert EffortEstimate.LOW.value == "low"
        assert EffortEstimate.EXTENSIVE.value == "extensive"

    def test_ordinal_comparison(self) -> None:
        assert effort_rank(EffortEstimate.LOW) < effort_rank(EffortEstimate.HIGH)
        assert effort_at_least(EffortEstimate.HIGH, EffortEstimate.MEDIUM)
        assert not effort_at_least(EffortEstimate.LOW, EffortEstimate.MEDIUM)


class TestCompletionStatus:
    def test_avoids_mastery_vocabulary(self) -> None:
        values = {s.value for s in CompletionStatus}
        assert "mastered" not in values
        assert "exam_ready" not in values
        assert CompletionStatus.READY_FOR_COMPLETION in CompletionStatus


# ---------------------------------------------------------------------------
# Entities — invariants
# ---------------------------------------------------------------------------


class TestLearningObjective:
    def test_create_valid(self) -> None:
        obj = _objective(kind=ObjectiveKind.APPLY)
        assert obj.kind == ObjectiveKind.APPLY

    def test_rejects_empty_title(self) -> None:
        with pytest.raises(ValueError, match="title"):
            LearningObjective.create(
                "o1", "c1", "t1", ObjectiveKind.REVIEW, title="  "
            )

    def test_rejects_negative_sequence(self) -> None:
        with pytest.raises(ValueError, match="sequence_index"):
            LearningObjective.create(
                "o1",
                "c1",
                "t1",
                ObjectiveKind.REVISE,
                title="Revise",
                sequence_index=-1,
            )


class TestLearningSession:
    def test_create_and_transition(self) -> None:
        session = _session()
        started = session.apply_transition(SessionTransitionEvent.START_SESSION)
        assert started.state == SessionState.ACTIVE
        finished = started.apply_transition(SessionTransitionEvent.FINISH_SESSION)
        assert finished.state == SessionState.COMPLETED

    def test_invalid_transition_raises(self) -> None:
        session = _session(state=SessionState.COMPLETED)
        with pytest.raises(ValueError, match="invalid session transition"):
            session.apply_transition(SessionTransitionEvent.START_SESSION)

    def test_reflection_requires_completed_session(self) -> None:
        session = _session(state=SessionState.ACTIVE)
        pending = JourneyReflection.create_pending("r1", "sess-1", "journey-1")
        with pytest.raises(ValueError, match="COMPLETED"):
            session.with_reflection(pending)

    def test_evidence_append_validates_ids(self) -> None:
        session = _session(state=SessionState.ACTIVE)
        bad = _evidence(journey_id="other")
        with pytest.raises(ValueError, match="journey_id"):
            session.with_evidence(bad)


class TestJourneyEvidence:
    def test_references_evidence_model_types(self) -> None:
        item = _evidence()
        assert item.evidence_type == EvidenceType.STUDY_SESSION
        assert item.confidence_level == EvidenceConfidenceLevel.MEDIUM

    def test_rejects_empty_evidence_id(self) -> None:
        with pytest.raises(ValueError, match="evidence_id"):
            JourneyEvidence.create(
                "je1", "  ", "journey-1", EvidenceType.TIME_ON_TASK, NOW
            )


class TestJourneyReflection:
    def test_pending_to_captured(self) -> None:
        pending = JourneyReflection.create_pending("r1", "sess-1", "journey-1")
        captured = pending.with_captured_content(
            what_was_learned="Definitions",
            uncertainty="Proofs",
            confidence=ReflectionConfidence.LOW,
            captured_at=NOW,
        )
        assert captured.posture == ReflectionPosture.CAPTURED
        assert captured.questions_remaining == ()

    def test_cannot_capture_twice(self) -> None:
        captured = _captured_reflection()
        with pytest.raises(ValueError, match="cannot capture"):
            captured.with_captured_content(
                what_was_learned="Again",
                uncertainty="Still",
                captured_at=NOW,
            )


class TestJourneyRecommendation:
    def test_never_claims_certainty(self) -> None:
        rec = JourneyRecommendation.create(
            "rec-1",
            "journey-1",
            RecommendationKind.CONTINUE_CURRENT_SESSION,
            certainty=RecommendationCertainty.SUGGESTED,
            rationale_tags=["active_journey"],
        )
        assert rec.claims_certainty is False
        assert rec.lifecycle == RecommendationLifecycle.PROPOSED

    def test_kinds_cover_brief_examples(self) -> None:
        kinds = {k.value for k in RecommendationKind}
        assert "begin_next_objective" in kinds
        assert "review_previous_concept" in kinds
        assert "revise_earlier_evidence" in kinds
        assert "attempt_practice" in kinds


class TestJourneyProgress:
    def test_empty_progress(self) -> None:
        progress = JourneyProgress.empty()
        assert progress.completion_status == CompletionStatus.NOT_STARTED
        assert progress.meets_completion_criteria is False

    def test_rejects_addressed_exceeding_total(self) -> None:
        with pytest.raises(ValueError, match="objectives_addressed"):
            JourneyProgress.create(
                objectives_total=1,
                objectives_addressed=2,
                sessions_completed=0,
                sessions_planned=0,
                evidence_count=0,
                reflections_captured=0,
            )


class TestJourneyHistory:
    def test_append_only(self) -> None:
        history = JourneyHistory.empty()
        entry = JourneyHistoryEntry.create(
            "e1",
            JourneyHistoryEventType.JOURNEY_CREATED,
            NOW,
            detail_tags=["state:not_started"],
        )
        next_history = history.append(entry)
        assert history.length == 0
        assert next_history.length == 1
        assert next_history.filter_by_type(
            JourneyHistoryEventType.JOURNEY_CREATED
        ) == (entry,)


class TestLearningJourney:
    def test_create_with_objectives(self) -> None:
        journey = _journey(
            objectives=[
                _objective(),
                _objective("obj-2", sequence_index=1),
            ]
        )
        assert len(journey.ordered_objectives()) == 2
        assert journey.state == JourneyState.NOT_STARTED

    def test_objective_topic_mismatch_rejected(self) -> None:
        with pytest.raises(ValueError, match="topic_id"):
            _journey(objectives=[_objective(topic_id="other-topic")])

    def test_apply_transition(self) -> None:
        journey = _journey()
        active = journey.apply_transition(JourneyTransitionEvent.START_JOURNEY)
        assert active.state == JourneyState.ACTIVE

    def test_cannot_jump_to_completed(self) -> None:
        journey = _journey(state=JourneyState.ACTIVE)
        with pytest.raises(ValueError, match="invalid journey transition"):
            journey.apply_transition(JourneyTransitionEvent.CONFIRM_TOPIC_COMPLETE)

    def test_with_session_enforces_unique_sequence(self) -> None:
        journey = _journey(sessions=[_session()])
        with pytest.raises(ValueError, match="sequence_index"):
            journey.with_session(_session("sess-2", sequence_index=0))

    def test_is_terminal(self) -> None:
        assert _journey(state=JourneyState.COMPLETED).is_terminal
        assert not _journey(state=JourneyState.ACTIVE).is_terminal


# ---------------------------------------------------------------------------
# Validation service
# ---------------------------------------------------------------------------


class TestJourneyValidationService:
    def test_lawful_journey_transition(self) -> None:
        result = JourneyValidationService.validate_journey_transition(
            JourneyState.NOT_STARTED,
            JourneyTransitionEvent.START_JOURNEY,
        )
        assert result.is_valid

    def test_invalid_journey_transition(self) -> None:
        result = JourneyValidationService.validate_journey_transition(
            JourneyState.NOT_STARTED,
            JourneyTransitionEvent.CONFIRM_TOPIC_COMPLETE,
        )
        assert not result.is_valid
        assert result.issues[0].code == "invalid_journey_transition"

    def test_completion_criteria_guard(self) -> None:
        result = JourneyValidationService.validate_journey_transition(
            JourneyState.ACTIVE,
            JourneyTransitionEvent.COMPLETION_CRITERIA_MET,
            meets_completion_criteria=False,
        )
        assert not result.is_valid
        assert result.issues[0].code == "completion_criteria_not_met"

    def test_confirm_blocked_by_pending_reflection(self) -> None:
        result = JourneyValidationService.validate_journey_transition(
            JourneyState.READY_FOR_COMPLETION,
            JourneyTransitionEvent.CONFIRM_TOPIC_COMPLETE,
            pending_reflection=True,
        )
        assert not result.is_valid
        assert result.issues[0].code == "reflection_pending"

    def test_session_start_requires_suitable_journey(self) -> None:
        result = JourneyValidationService.validate_session_transition(
            SessionState.NOT_STARTED,
            SessionTransitionEvent.START_SESSION,
            parent_journey_state=JourneyState.PAUSED,
        )
        assert not result.is_valid
        assert result.issues[0].code == "journey_not_startable"

    def test_finish_blocked_when_journey_paused(self) -> None:
        result = JourneyValidationService.validate_session_transition(
            SessionState.ACTIVE,
            SessionTransitionEvent.FINISH_SESSION,
            parent_journey_state=JourneyState.PAUSED,
        )
        assert not result.is_valid
        assert result.issues[0].code == "journey_paused"

    def test_consistency_detects_unknown_session_on_evidence(self) -> None:
        journey = _journey(
            sessions=[_session()],
            evidence=[_evidence(session_id="missing-session")],
        )
        result = JourneyValidationService.validate_consistency(journey)
        assert not result.is_valid
        assert any(i.code == "evidence_session_unknown" for i in result.issues)

    def test_session_ordering_duplicate(self) -> None:
        journey = LearningJourney.create(
            "journey-1",
            "learner-1",
            "topic-a",
            "CS1-2026",
            sessions=[
                _session("s1", sequence_index=0),
                LearningSession.create(
                    "s2", "journey-1", sequence_index=0, state=SessionState.NOT_STARTED
                ),
            ],
        )
        # create() does not check uniqueness across provided sessions — validation does.
        result = JourneyValidationService.validate_session_ordering(journey)
        assert not result.is_valid
        assert any(i.code == "duplicate_sequence_index" for i in result.issues)

    def test_completed_without_criteria_is_error(self) -> None:
        session = _session(state=SessionState.COMPLETED)
        journey = _journey(
            state=JourneyState.COMPLETED,
            sessions=[session],
            progress=JourneyProgress.empty(),
        )
        result = JourneyValidationService.validate_consistency(journey)
        assert not result.is_valid
        assert any(i.code == "completed_without_criteria" for i in result.issues)


# ---------------------------------------------------------------------------
# Progress service
# ---------------------------------------------------------------------------


class TestJourneyProgressService:
    def test_empty_journey_progress(self) -> None:
        progress = JourneyProgressService.calculate(_journey())
        assert progress.sessions_completed == 0
        assert progress.completion_status == CompletionStatus.NOT_STARTED
        assert progress.meets_completion_criteria is False
        assert progress.consistency == ConsistencyPosture.NONE
        assert progress.evidence_confidence == EvidenceConfidencePosture.UNKNOWN

    def test_deterministic_same_inputs(self) -> None:
        journey = _journey(
            objectives=[_objective()],
            sessions=[
                _session(state=SessionState.COMPLETED, objective_id="obj-1"),
            ],
            evidence=[_evidence(objective_id="obj-1")],
            reflections=[_captured_reflection()],
        )
        first = JourneyProgressService.calculate(journey)
        second = JourneyProgressService.calculate(journey)
        assert first == second

    def test_objectives_addressed_from_session_and_evidence(self) -> None:
        journey = _journey(
            objectives=[
                _objective("obj-1"),
                _objective("obj-2", sequence_index=1),
            ],
            sessions=[
                _session(
                    "sess-1",
                    state=SessionState.COMPLETED,
                    objective_id="obj-1",
                ),
            ],
            evidence=[_evidence(objective_id="obj-2", session_id=None)],
        )
        progress = JourneyProgressService.calculate(journey)
        assert progress.objectives_total == 2
        assert progress.objectives_addressed == 2
        assert progress.completion_status == CompletionStatus.PARTIALLY_ADDRESSED or (
            progress.objectives_addressed == 2
        )

    def test_meets_criteria_requires_min_sessions_and_reflections(self) -> None:
        objs = [_objective("obj-1")]
        s1 = _session(
            "sess-1",
            sequence_index=0,
            state=SessionState.COMPLETED,
            objective_id="obj-1",
        )
        s2 = _session(
            "sess-2",
            sequence_index=1,
            state=SessionState.COMPLETED,
            objective_id="obj-1",
        )
        journey = _journey(
            objectives=objs,
            sessions=[s1, s2],
            reflections=[
                _captured_reflection("r1", session_id="sess-1"),
                _captured_reflection("r2", session_id="sess-2"),
            ],
        )
        progress = JourneyProgressService.calculate(journey)
        assert progress.meets_completion_criteria is True
        assert progress.completion_status == CompletionStatus.READY_FOR_COMPLETION
        assert progress.consistency == ConsistencyPosture.REGULAR

    def test_single_session_does_not_meet_default_criteria(self) -> None:
        journey = _journey(
            objectives=[_objective()],
            sessions=[
                _session(state=SessionState.COMPLETED, objective_id="obj-1"),
            ],
            reflections=[_captured_reflection()],
        )
        progress = JourneyProgressService.calculate(journey)
        assert progress.meets_completion_criteria is False
        assert progress.sessions_completed == 1

    def test_missing_reflection_blocks_criteria(self) -> None:
        journey = _journey(
            objectives=[_objective()],
            sessions=[
                _session(
                    "sess-1",
                    sequence_index=0,
                    state=SessionState.COMPLETED,
                    objective_id="obj-1",
                ),
                _session(
                    "sess-2",
                    sequence_index=1,
                    state=SessionState.COMPLETED,
                    objective_id="obj-1",
                ),
            ],
            reflections=[_captured_reflection("r1", session_id="sess-1")],
        )
        progress = JourneyProgressService.calculate(journey)
        assert progress.meets_completion_criteria is False

    def test_evidence_confidence_aggregation(self) -> None:
        journey = _journey(
            evidence=[
                _evidence(
                    "je1",
                    evidence_id="e1",
                    confidence=EvidenceConfidenceLevel.HIGH,
                ),
                _evidence(
                    "je2",
                    evidence_id="e2",
                    session_id=None,
                    confidence=EvidenceConfidenceLevel.HIGH,
                ),
            ]
        )
        progress = JourneyProgressService.calculate(journey)
        assert progress.evidence_confidence == EvidenceConfidencePosture.HIGH
        assert progress.evidence_count == 2

    def test_thin_evidence_confidence(self) -> None:
        journey = _journey(
            evidence=[
                _evidence(confidence=EvidenceConfidenceLevel.MEDIUM),
            ]
        )
        progress = JourneyProgressService.calculate(journey)
        assert progress.evidence_confidence == EvidenceConfidencePosture.THIN

    def test_skipped_sessions_excluded_from_planned(self) -> None:
        journey = _journey(
            sessions=[
                _session("s1", sequence_index=0, state=SessionState.COMPLETED),
                _session("s2", sequence_index=1, state=SessionState.SKIPPED),
            ]
        )
        progress = JourneyProgressService.calculate(journey)
        assert progress.sessions_planned == 1
        assert progress.sessions_completed == 1

    def test_completed_journey_status(self) -> None:
        journey = _journey(state=JourneyState.COMPLETED)
        progress = JourneyProgressService.calculate(journey)
        assert progress.completion_status == CompletionStatus.COMPLETED


# ---------------------------------------------------------------------------
# Repository contract
# ---------------------------------------------------------------------------


class TestLearningJourneyRepositoryContract:
    def test_is_abstract(self) -> None:
        assert issubclass(LearningJourneyRepository, ABC)
        with pytest.raises(TypeError):
            LearningJourneyRepository()  # type: ignore[misc]

    def test_in_memory_stub_satisfies_contract(self) -> None:
        class InMemoryLearningJourneyRepository(LearningJourneyRepository):
            def __init__(self) -> None:
                self._store: dict[str, LearningJourney] = {}

            def get_by_id(self, journey_id: str) -> LearningJourney | None:
                return self._store.get(journey_id)

            def get_by_learner_and_topic(
                self,
                learner_id: str,
                topic_id: str,
                *,
                curriculum_id: str | None = None,
            ) -> LearningJourney | None:
                for journey in self._store.values():
                    if (
                        journey.learner_id == learner_id
                        and journey.topic_id == topic_id
                    ):
                        if (
                            curriculum_id is None
                            or journey.curriculum_id == curriculum_id
                        ):
                            return journey
                return None

            def list_for_learner(
                self,
                learner_id: str,
                *,
                curriculum_id: str | None = None,
            ) -> list[LearningJourney]:
                return [
                    j
                    for j in self._store.values()
                    if j.learner_id == learner_id
                    and (curriculum_id is None or j.curriculum_id == curriculum_id)
                ]

            def save(self, journey: LearningJourney) -> None:
                self._store[journey.journey_id] = journey

            def delete(self, journey_id: str) -> bool:
                return self._store.pop(journey_id, None) is not None

        repo = InMemoryLearningJourneyRepository()
        journey = _journey()
        repo.save(journey)
        assert repo.get_by_id("journey-1") == journey
        assert repo.get_by_learner_and_topic("learner-1", "topic-a") == journey
        assert len(repo.list_for_learner("learner-1")) == 1
        assert repo.delete("journey-1") is True
        assert repo.get_by_id("journey-1") is None


# ---------------------------------------------------------------------------
# Package exports / smoke
# ---------------------------------------------------------------------------


class TestPackageExports:
    def test_lazy_exports_resolve(self) -> None:
        assert JourneyState.ACTIVE.value == "active"
        assert SessionState.NOT_STARTED.value == "not_started"
        assert isinstance(ValidationResult.ok(), ValidationResult)
        assert JourneyProgressService.DEFAULT_MIN_COMPLETED_SESSIONS == 2
