"""Learning Session Runtime — public application interface.

Execution layer for a student's interaction with an individual Learning
Session. Bridges Curriculum Graph → Learning Journey Engine → Session →
Evidence → Reflection → Recommendation consumers.

Framework-independent: no Flask, SQLAlchemy, UI, or persistence.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from app.application.learning_session.activity_scheduler import ActivityScheduler
from app.application.learning_session.completion_evaluator import CompletionEvaluator
from app.application.learning_session.dto.completion_result import CompletionResult
from app.application.learning_session.dto.evidence_summary import EvidenceSummary
from app.application.learning_session.dto.learning_session_plan import (
    LearningSessionPlan,
)
from app.application.learning_session.dto.reflection_summary import ReflectionSummary
from app.application.learning_session.dto.runtime_snapshot import RuntimeSnapshot
from app.application.learning_session.evidence_collector import EvidenceCollector
from app.application.learning_session.exceptions import (
    InvalidSessionState,
    SessionAlreadyArchived,
    SessionAlreadyCompleted,
)
from app.application.learning_session.lifecycle_manager import LifecycleManager
from app.application.learning_session.planner import LearningSessionPlanner
from app.application.learning_session.policies.scheduling_policy import NextAction
from app.application.learning_session.reflection_manager import ReflectionManager
from app.application.learning_session.runtime_phase import RuntimePhase
from app.domain.evidence.evidence_category import EvidenceConfidenceLevel
from app.domain.evidence.evidence_type import EvidenceType
from app.domain.evidence.learning_evidence import LearningEvidence
from app.domain.learning_journey.entities.journey_evidence import JourneyEvidence
from app.domain.learning_journey.entities.journey_reflection import (
    ReflectionConfidence,
)
from app.domain.learning_journey.entities.learning_journey import LearningJourney
from app.domain.learning_journey.entities.learning_objective import LearningObjective
from app.domain.learning_journey.entities.learning_session import LearningSession
from app.domain.learning_journey.value_objects.effort_estimate import EffortEstimate
from app.domain.learning_journey.value_objects.session_state import SessionState


@dataclass(frozen=True)
class SessionHandle:
    """In-memory handle pairing a domain session with runtime phase and plan.

    Callers remain responsible for persistence. The runtime never saves.
    """

    session: LearningSession
    phase: RuntimePhase
    plan: LearningSessionPlan | None = None


class LearningSessionRuntime:
    """Public facade for Learning Session educational execution.

    Coordinates planner, lifecycle, evidence, reflection, completion, and
    scheduling. Never manipulates persistence or UI. Never completes journeys.
    """

    def __init__(
        self,
        *,
        planner: LearningSessionPlanner | None = None,
        lifecycle: LifecycleManager | None = None,
        evidence_collector: EvidenceCollector | None = None,
        reflection_manager: ReflectionManager | None = None,
        completion_evaluator: CompletionEvaluator | None = None,
        activity_scheduler: ActivityScheduler | None = None,
        clock=None,
        id_factory=None,
    ) -> None:
        self._clock = clock or (lambda: datetime.now(tz=UTC))
        self._id_factory = id_factory or (lambda: uuid4().hex[:12])
        self._planner = planner or LearningSessionPlanner(id_factory=self._id_factory)
        self._lifecycle = lifecycle or LifecycleManager()
        self._evidence = evidence_collector or EvidenceCollector(
            clock=self._clock,
            id_factory=self._id_factory,
        )
        self._reflection = reflection_manager or ReflectionManager(
            clock=self._clock,
            id_factory=self._id_factory,
        )
        self._completion = completion_evaluator or CompletionEvaluator()
        self._scheduler = activity_scheduler or ActivityScheduler()

    # ------------------------------------------------------------------
    # Create / plan
    # ------------------------------------------------------------------

    def create_session(
        self,
        journey: LearningJourney,
        *,
        topic_id: str | None = None,
        objectives: (
            list[LearningObjective] | tuple[LearningObjective, ...] | None
        ) = None,
        estimated_effort: EffortEstimate | None = None,
        previous_evidence: (
            list[JourneyEvidence] | tuple[JourneyEvidence, ...] | None
        ) = None,
        sequence_index: int | None = None,
        session_id: str | None = None,
    ) -> SessionHandle:
        """Create a PLANNED Learning Session from journey context.

        Does not persist. Does not start the session.
        """
        plan = self._planner.plan(
            journey=journey,
            topic_id=topic_id,
            objectives=objectives,
            estimated_effort=estimated_effort,
            previous_evidence=previous_evidence,
            sequence_index=sequence_index,
            session_id=session_id,
        )
        primary_objective = plan.objective_ids[0] if plan.objective_ids else None
        session = LearningSession.create(
            plan.session_id,
            plan.journey_id,
            sequence_index=plan.sequence_index,
            state=SessionState.NOT_STARTED,
            estimated_effort=plan.estimated_effort,
            objective_id=primary_objective,
        )
        return SessionHandle(
            session=session,
            phase=self._lifecycle.initial_phase(),
            plan=plan,
        )

    def plan_session(
        self,
        journey: LearningJourney,
        *,
        topic_id: str | None = None,
        objectives: (
            list[LearningObjective] | tuple[LearningObjective, ...] | None
        ) = None,
        estimated_effort: EffortEstimate | None = None,
        previous_evidence: (
            list[JourneyEvidence] | tuple[JourneyEvidence, ...] | None
        ) = None,
        sequence_index: int | None = None,
        session_id: str | None = None,
    ) -> LearningSessionPlan:
        """Build a plan without creating a session entity."""
        return self._planner.plan(
            journey=journey,
            topic_id=topic_id,
            objectives=objectives,
            estimated_effort=estimated_effort,
            previous_evidence=previous_evidence,
            sequence_index=sequence_index,
            session_id=session_id,
        )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def prepare_session(self, handle: SessionHandle) -> SessionHandle:
        """Mark a PLANNED session READY for start."""
        result = self._lifecycle.prepare(handle.session, phase=handle.phase)
        return SessionHandle(
            session=result.session,
            phase=result.phase,
            plan=handle.plan,
        )

    def start_session(self, handle: SessionHandle) -> SessionHandle:
        """Start a PLANNED or READY session (→ ACTIVE)."""
        result = self._lifecycle.start(handle.session, phase=handle.phase)
        return SessionHandle(
            session=result.session,
            phase=result.phase,
            plan=handle.plan,
        )

    def pause_session(self, handle: SessionHandle) -> SessionHandle:
        """Pause an ACTIVE session."""
        result = self._lifecycle.pause(handle.session, phase=handle.phase)
        return SessionHandle(
            session=result.session,
            phase=result.phase,
            plan=handle.plan,
        )

    def resume_session(self, handle: SessionHandle) -> SessionHandle:
        """Resume a PAUSED session."""
        result = self._lifecycle.resume(handle.session, phase=handle.phase)
        return SessionHandle(
            session=result.session,
            phase=result.phase,
            plan=handle.plan,
        )

    def complete_session(
        self,
        handle: SessionHandle,
        *,
        actual_duration_minutes: int | None = None,
        attach_pending_reflection: bool = True,
    ) -> SessionHandle:
        """Finish an ACTIVE or PAUSED session (→ COMPLETED).

        Optionally attaches a PENDING reflection artefact. Never completes
        the parent journey.
        """
        result = self._lifecycle.complete(
            handle.session,
            phase=handle.phase,
            actual_duration_minutes=actual_duration_minutes,
        )
        session = result.session
        if attach_pending_reflection:
            session = self._reflection.attach_pending(session)
        return SessionHandle(
            session=session,
            phase=result.phase,
            plan=handle.plan,
        )

    def archive_session(self, handle: SessionHandle) -> SessionHandle:
        """Archive a COMPLETED session (→ ARCHIVED)."""
        result = self._lifecycle.archive(handle.session, phase=handle.phase)
        return SessionHandle(
            session=result.session,
            phase=result.phase,
            plan=handle.plan,
        )

    # ------------------------------------------------------------------
    # Evidence / reflection / completion / next action
    # ------------------------------------------------------------------

    def collect_evidence(
        self,
        handle: SessionHandle,
        *,
        evidence_type: EvidenceType | str = EvidenceType.STUDY_SESSION,
        evidence_id: str | None = None,
        confidence_level: EvidenceConfidenceLevel
        | str = EvidenceConfidenceLevel.UNKNOWN,
        objective_id: str | None = None,
        topic_id: str | None = None,
        learning_evidence: LearningEvidence | None = None,
    ) -> tuple[SessionHandle, JourneyEvidence, EvidenceSummary]:
        """Collect educational evidence onto the session."""
        session, journey_evidence = self._evidence.collect(
            handle.session,
            phase=handle.phase,
            evidence_type=evidence_type,
            evidence_id=evidence_id,
            confidence_level=confidence_level,
            objective_id=objective_id,
            topic_id=topic_id or (handle.plan.topic_id if handle.plan else None),
            learning_evidence=learning_evidence,
        )
        updated = SessionHandle(
            session=session,
            phase=handle.phase,
            plan=handle.plan,
        )
        return updated, journey_evidence, self._evidence.summarise(session)

    def collect_reflection(
        self,
        handle: SessionHandle,
        *,
        summary: str,
        challenges: str,
        questions_remaining: list[str] | tuple[str, ...] | None = None,
        confidence: ReflectionConfidence | str = ReflectionConfidence.UNSURE,
        next_intention: str | None = None,
        user_id: int | None = None,
    ) -> tuple[SessionHandle, ReflectionSummary]:
        """Capture structured student reflection onto a completed session.

        ``user_id`` is optional analytics identity only — when provided,
        passive reflection events are observed after successful capture.
        """
        if handle.phase == RuntimePhase.ARCHIVED:
            raise SessionAlreadyArchived(
                f"Session {handle.session.session_id} is archived"
            )
        if handle.session.state != SessionState.COMPLETED:
            raise InvalidSessionState(
                "Reflection capture requires a COMPLETED session"
            )
        session, reflection_summary = self._reflection.capture(
            handle.session,
            summary=summary,
            challenges=challenges,
            questions_remaining=questions_remaining,
            confidence=confidence,
            next_intention=next_intention,
            user_id=user_id,
        )
        return (
            SessionHandle(session=session, phase=handle.phase, plan=handle.plan),
            reflection_summary,
        )

    def defer_reflection(self, handle: SessionHandle) -> SessionHandle:
        """Defer PENDING reflection under explicit policy."""
        session = self._reflection.defer(handle.session)
        return SessionHandle(
            session=session,
            phase=handle.phase,
            plan=handle.plan,
        )

    def evaluate_completion(self, handle: SessionHandle) -> CompletionResult:
        """Evaluate whether the Learning Session itself is complete."""
        return self._completion.evaluate(handle.session)

    def generate_next_action(self, handle: SessionHandle) -> NextAction:
        """Generate a deterministic next-action recommendation."""
        completion = self._completion.evaluate(handle.session)
        return self._scheduler.next_action(
            handle.session,
            phase=handle.phase,
            completion=completion,
            actual_duration_minutes=handle.session.actual_duration_minutes,
        )

    def generate_runtime_snapshot(self, handle: SessionHandle) -> RuntimeSnapshot:
        """Generate an immutable educational snapshot for consumers."""
        completion = self._completion.evaluate(handle.session)
        next_action = self._scheduler.next_action(
            handle.session,
            phase=handle.phase,
            completion=completion,
            actual_duration_minutes=handle.session.actual_duration_minutes,
        )
        return RuntimeSnapshot(
            session_id=handle.session.session_id,
            journey_id=handle.session.journey_id,
            topic_id=handle.plan.topic_id if handle.plan else None,
            phase=handle.phase.value,
            session_state=handle.session.state,
            objective_id=handle.session.objective_id,
            plan=handle.plan,
            evidence_summary=self._evidence.summarise(handle.session),
            reflection_summary=self._reflection.summarise(handle.session),
            completion=completion,
            next_action=next_action.value,
            actual_duration_minutes=handle.session.actual_duration_minutes,
        )

    def rehydrate(
        self,
        session: LearningSession,
        *,
        plan: LearningSessionPlan | None = None,
        prepared: bool = False,
        archived: bool = False,
    ) -> SessionHandle:
        """Rebuild a SessionHandle from a domain session (no persistence)."""
        if archived and session.state == SessionState.COMPLETED:
            phase = RuntimePhase.ARCHIVED
        elif session.state == SessionState.COMPLETED:
            phase = RuntimePhase.COMPLETED
        elif session.is_terminal:
            phase = RuntimePhase.ARCHIVED
        else:
            phase = self._lifecycle.derive_phase(
                session,
                prepared=prepared,
                archived=False,
            )
        if session.state == SessionState.COMPLETED and archived is False:
            # Completed sessions are never "prepared" PLANNED.
            pass
        return SessionHandle(session=session, phase=phase, plan=plan)

    @staticmethod
    def rejects_completed_mutation(handle: SessionHandle) -> None:
        """Guard helper for callers — raises if session is closed."""
        if handle.phase == RuntimePhase.ARCHIVED:
            raise SessionAlreadyArchived(
                f"Session {handle.session.session_id} is archived"
            )
        if handle.phase == RuntimePhase.COMPLETED:
            raise SessionAlreadyCompleted(
                f"Session {handle.session.session_id} is already completed"
            )
