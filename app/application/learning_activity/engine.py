"""Learning Activity Engine — public application interface.

Owns execution structure INSIDE a Learning Session:
activity sequencing, transitions, completion, evidence routing, and
reflection hooks.

Does NOT own session lifecycle, journey progression, or mission scheduling.
Framework-independent: no Flask, SQLAlchemy, UI, or persistence.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from app.application.learning_activity.completion_manager import CompletionManager
from app.application.learning_activity.dto.activity_plan import (
    ActivityPlan,
    ActivityPlanItem,
)
from app.application.learning_activity.dto.activity_result import ActivityResult
from app.application.learning_activity.dto.activity_sequence import ActivitySequence
from app.application.learning_activity.dto.activity_snapshot import ActivitySnapshot
from app.application.learning_activity.dto.activity_transition import (
    ActivityTransition,
)
from app.application.learning_activity.evidence_router import EvidenceRouter
from app.application.learning_activity.exceptions import (
    ActivityNotFound,
    InvalidActivityState,
)
from app.application.learning_activity.planner import ActivityPlanner
from app.application.learning_activity.progression_manager import ProgressionManager
from app.application.learning_activity.reflection_router import ReflectionRouter
from app.application.learning_activity.sequence_builder import SequenceBuilder
from app.application.learning_activity.transition_manager import TransitionManager
from app.application.learning_activity.validator import ActivityValidator
from app.domain.learning_activity.entities.learning_activity import LearningActivity
from app.domain.learning_activity.value_objects.activity_state import ActivityState
from app.domain.learning_activity.value_objects.activity_type import ActivityType


@dataclass(frozen=True)
class ActivityHandle:
    """In-memory handle for activity execution inside a session.

    Callers remain responsible for persistence. The engine never saves.
    """

    sequence: ActivitySequence
    plan: ActivityPlan | None = None


class LearningActivityEngine:
    """Public facade for Learning Activity educational execution.

    Coordinates planner, sequence builder, transitions, progression,
    completion, evidence routing, and reflection routing. Never completes
    Learning Sessions, Journeys, or Missions.
    """

    def __init__(
        self,
        *,
        planner: ActivityPlanner | None = None,
        sequence_builder: SequenceBuilder | None = None,
        progression: ProgressionManager | None = None,
        transitions: TransitionManager | None = None,
        completion: CompletionManager | None = None,
        evidence_router: EvidenceRouter | None = None,
        reflection_router: ReflectionRouter | None = None,
        validator: ActivityValidator | None = None,
        id_factory=None,
    ) -> None:
        self._id_factory = id_factory or (lambda: uuid4().hex[:12])
        self._planner = planner or ActivityPlanner()
        self._builder = sequence_builder or SequenceBuilder(
            id_factory=self._id_factory
        )
        self._progression = progression or ProgressionManager()
        self._transitions = transitions or TransitionManager()
        self._completion = completion or CompletionManager()
        self._evidence = evidence_router or EvidenceRouter()
        self._reflection = reflection_router or ReflectionRouter()
        self._validator = validator or ActivityValidator()

    # ------------------------------------------------------------------
    # Create sequence
    # ------------------------------------------------------------------

    def create_sequence(
        self,
        *,
        session_id: str,
        journey_id: str | None = None,
        activity_types: (
            list[ActivityType | str] | tuple[ActivityType | str, ...] | None
        ) = None,
        activity_tags: list[str] | tuple[str, ...] | None = None,
        items: list[ActivityPlanItem] | tuple[ActivityPlanItem, ...] | None = None,
        require_introduction: bool = False,
        require_summary: bool = False,
        require_reflection: bool = False,
        preserve_input_order: bool = True,
        sequence_id: str | None = None,
        validate: bool = True,
    ) -> ActivityHandle:
        """Create an activity sequence from structural inputs.

        Does not persist. Does not start any activity.
        """
        plan = self._planner.plan(
            session_id=session_id,
            journey_id=journey_id,
            activity_types=activity_types,
            activity_tags=activity_tags,
            items=items,
            require_introduction=require_introduction,
            require_summary=require_summary,
            require_reflection=require_reflection,
            preserve_input_order=preserve_input_order,
        )
        sequence = self._builder.build(plan, sequence_id=sequence_id)
        if validate:
            self._validator.assert_valid(sequence)
        return ActivityHandle(sequence=sequence, plan=plan)

    def plan_activities(
        self,
        *,
        session_id: str,
        journey_id: str | None = None,
        activity_types: (
            list[ActivityType | str] | tuple[ActivityType | str, ...] | None
        ) = None,
        activity_tags: list[str] | tuple[str, ...] | None = None,
        items: list[ActivityPlanItem] | tuple[ActivityPlanItem, ...] | None = None,
        require_introduction: bool = False,
        require_summary: bool = False,
        require_reflection: bool = False,
        preserve_input_order: bool = True,
    ) -> ActivityPlan:
        """Build a plan without materialising a sequence."""
        return self._planner.plan(
            session_id=session_id,
            journey_id=journey_id,
            activity_types=activity_types,
            activity_tags=activity_tags,
            items=items,
            require_introduction=require_introduction,
            require_summary=require_summary,
            require_reflection=require_reflection,
            preserve_input_order=preserve_input_order,
        )

    # ------------------------------------------------------------------
    # Advance / navigation
    # ------------------------------------------------------------------

    def advance_activity(self, handle: ActivityHandle) -> ActivityHandle:
        """Complete the current activity (if open) and start the next.

        If nothing is ACTIVE/PAUSED, starts the first NOT_STARTED activity.
        If current is ACTIVE/PAUSED, completes it then starts the next remaining.
        """
        sequence = handle.sequence
        current = self._progression.current(sequence)

        if current is None:
            remaining = self._progression.remaining(sequence)
            if not remaining:
                return handle
            result = self._transitions.start(sequence, remaining[0].activity_id)
            self._validator.assert_valid(result.sequence)
            return ActivityHandle(sequence=result.sequence, plan=handle.plan)

        if current.state == ActivityState.NOT_STARTED:
            result = self._transitions.start(sequence, current.activity_id)
            self._validator.assert_valid(result.sequence)
            return ActivityHandle(sequence=result.sequence, plan=handle.plan)

        # Complete current then start next.
        completed = self._transitions.complete(sequence, current.activity_id)
        sequence = completed.sequence
        nxt = self._progression.next(sequence, after=completed.activity)
        if nxt is None:
            self._validator.assert_valid(sequence)
            return ActivityHandle(sequence=sequence, plan=handle.plan)
        started = self._transitions.start(sequence, nxt.activity_id)
        self._validator.assert_valid(started.sequence)
        return ActivityHandle(sequence=started.sequence, plan=handle.plan)

    def skip_activity(
        self,
        handle: ActivityHandle,
        *,
        activity_id: str | None = None,
        start_next: bool = True,
    ) -> tuple[ActivityHandle, ActivityTransition]:
        """Skip the current (or named) activity."""
        activity = self._resolve_activity(handle.sequence, activity_id)
        result = self._transitions.skip(handle.sequence, activity.activity_id)
        sequence = result.sequence
        if start_next:
            nxt = self._progression.next(sequence, after=result.activity)
            if nxt is not None and nxt.state == ActivityState.NOT_STARTED:
                started = self._transitions.start(sequence, nxt.activity_id)
                sequence = started.sequence
        self._validator.assert_valid(sequence)
        return (
            ActivityHandle(sequence=sequence, plan=handle.plan),
            result.transition,
        )

    def pause_activity(
        self,
        handle: ActivityHandle,
        *,
        activity_id: str | None = None,
    ) -> tuple[ActivityHandle, ActivityTransition]:
        """Pause the current (or named) ACTIVE activity."""
        activity = self._resolve_activity(handle.sequence, activity_id)
        result = self._transitions.pause(handle.sequence, activity.activity_id)
        self._validator.assert_valid(result.sequence)
        return (
            ActivityHandle(sequence=result.sequence, plan=handle.plan),
            result.transition,
        )

    def resume_activity(
        self,
        handle: ActivityHandle,
        *,
        activity_id: str | None = None,
    ) -> tuple[ActivityHandle, ActivityTransition]:
        """Resume the current (or named) PAUSED activity."""
        activity = self._resolve_activity(handle.sequence, activity_id)
        result = self._transitions.resume(handle.sequence, activity.activity_id)
        self._validator.assert_valid(result.sequence)
        return (
            ActivityHandle(sequence=result.sequence, plan=handle.plan),
            result.transition,
        )

    def complete_activity(
        self,
        handle: ActivityHandle,
        *,
        activity_id: str | None = None,
        start_next: bool = False,
    ) -> tuple[ActivityHandle, ActivityTransition, ActivityResult]:
        """Complete the current (or named) activity.

        Never completes the Learning Session.
        """
        activity = self._resolve_activity(handle.sequence, activity_id)
        result = self._transitions.complete(handle.sequence, activity.activity_id)
        sequence = result.sequence
        if start_next:
            nxt = self._progression.next(sequence, after=result.activity)
            if nxt is not None and nxt.state == ActivityState.NOT_STARTED:
                started = self._transitions.start(sequence, nxt.activity_id)
                sequence = started.sequence
        self._validator.assert_valid(sequence)
        evaluation = self._completion.evaluate_activity(sequence, result.activity)
        return (
            ActivityHandle(sequence=sequence, plan=handle.plan),
            result.transition,
            evaluation,
        )

    def start_activity(
        self,
        handle: ActivityHandle,
        *,
        activity_id: str | None = None,
    ) -> tuple[ActivityHandle, ActivityTransition]:
        """Start the current (or named) NOT_STARTED activity."""
        activity = self._resolve_activity(handle.sequence, activity_id)
        result = self._transitions.start(handle.sequence, activity.activity_id)
        self._validator.assert_valid(result.sequence)
        return (
            ActivityHandle(sequence=result.sequence, plan=handle.plan),
            result.transition,
        )

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def current_activity(
        self, handle: ActivityHandle
    ) -> LearningActivity | None:
        """Return the activity currently in focus."""
        return self._progression.current(handle.sequence)

    def next_activity(self, handle: ActivityHandle) -> LearningActivity | None:
        """Return the next remaining activity after current."""
        return self._progression.next(handle.sequence)

    def previous_activity(
        self, handle: ActivityHandle
    ) -> LearningActivity | None:
        """Return the previous activity before current."""
        return self._progression.previous(handle.sequence)

    def snapshot(self, handle: ActivityHandle) -> ActivitySnapshot:
        """Generate an immutable educational snapshot."""
        sequence = handle.sequence
        current = self._progression.current(sequence)
        progress = self._progression.summarise(sequence)
        result = self._completion.evaluate_sequence(sequence)
        return ActivitySnapshot(
            session_id=sequence.session_id,
            sequence_id=sequence.sequence_id,
            current_activity=current,
            current_state=current.state if current else None,
            progress=progress,
            sequence=sequence,
            result=result,
            ready_for_session_completion=result.ready_for_session_completion,
            next_activity=self._progression.next(sequence),
            previous_activity=self._progression.previous(sequence),
        )

    def evaluate_completion(self, handle: ActivityHandle) -> ActivityResult:
        """Evaluate sequence completion and session-ready signal."""
        return self._completion.evaluate_sequence(handle.sequence)

    def ready_for_session_completion(self, handle: ActivityHandle) -> bool:
        """True when Session Runtime may consider completing the session.

        Never completes the session.
        """
        return self._completion.ready_for_session_completion(handle.sequence)

    # ------------------------------------------------------------------
    # Evidence / reflection
    # ------------------------------------------------------------------

    def route_evidence(
        self,
        handle: ActivityHandle,
        *,
        evidence_id: str,
        activity_id: str | None = None,
        require_active: bool = True,
    ) -> ActivityHandle:
        """Route evidence to an activity. No persistence. No scoring."""
        result = self._evidence.route(
            handle.sequence,
            evidence_id=evidence_id,
            activity_id=activity_id,
            require_active=require_active,
        )
        return ActivityHandle(sequence=result.sequence, plan=handle.plan)

    def associate_reflection(
        self,
        handle: ActivityHandle,
        *,
        reflection_id: str,
        activity_id: str | None = None,
        prefer_reflection_type: bool = True,
    ) -> ActivityHandle:
        """Associate a reflection with an activity (not the session)."""
        result = self._reflection.associate(
            handle.sequence,
            reflection_id=reflection_id,
            activity_id=activity_id,
            prefer_reflection_type=prefer_reflection_type,
        )
        return ActivityHandle(sequence=result.sequence, plan=handle.plan)

    def validate(self, handle: ActivityHandle) -> None:
        """Assert sequence integrity; raise ValidationError if invalid."""
        self._validator.assert_valid(handle.sequence)

    def rehydrate(
        self,
        sequence: ActivitySequence,
        *,
        plan: ActivityPlan | None = None,
        validate: bool = True,
    ) -> ActivityHandle:
        """Rebuild an ActivityHandle from an existing sequence."""
        if validate:
            self._validator.assert_valid(sequence)
        return ActivityHandle(sequence=sequence, plan=plan)

    def _resolve_activity(
        self,
        sequence: ActivitySequence,
        activity_id: str | None,
    ) -> LearningActivity:
        if activity_id is not None:
            activity = sequence.activity_by_id(activity_id)
            if activity is None:
                raise ActivityNotFound(
                    f"Activity {activity_id!r} not found in sequence"
                )
            return activity
        current = self._progression.current(sequence)
        if current is None:
            raise InvalidActivityState(
                "No current activity available for this operation"
            )
        return current
