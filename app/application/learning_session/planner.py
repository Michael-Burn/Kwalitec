"""Constructs a Learning Session plan from journey / topic / objectives.

Framework-independent. Deterministic. Never generates study content or
estimates mastery.
"""

from __future__ import annotations

from app.application.learning_session.dto.learning_session_plan import (
    LearningSessionPlan,
)
from app.application.learning_session.exceptions import PlanningError
from app.application.learning_session.policies.planning_policy import PlanningPolicy
from app.domain.learning_journey.entities.journey_evidence import JourneyEvidence
from app.domain.learning_journey.entities.learning_journey import LearningJourney
from app.domain.learning_journey.entities.learning_objective import LearningObjective
from app.domain.learning_journey.entities.learning_session import LearningSession
from app.domain.learning_journey.value_objects.effort_estimate import EffortEstimate


class LearningSessionPlanner:
    """Build a deterministic ``LearningSessionPlan`` for session creation."""

    def __init__(self, *, id_factory=None) -> None:
        self._id_factory = id_factory or (lambda: "sess")

    def plan(
        self,
        *,
        journey: LearningJourney,
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
        """Construct a session plan from journey context and educational inputs.

        Args:
            journey: Parent Learning Journey aggregate.
            topic_id: Topic override (defaults to journey.topic_id).
            objectives: Objectives in focus (defaults to journey objectives
                subset or empty).
            estimated_effort: Explicit effort band override.
            previous_evidence: Prior evidence informing the plan.
            sequence_index: Explicit sequence; defaults to next available.
            session_id: Explicit session identity; otherwise generated.

        Returns:
            Immutable LearningSessionPlan.

        Raises:
            PlanningError: When required identities are missing.
        """
        tid = (topic_id or journey.topic_id or "").strip()
        if not tid:
            raise PlanningError("topic_id is required to plan a learning session")
        jid = journey.journey_id
        if not jid:
            raise PlanningError("journey_id is required to plan a learning session")

        objs = tuple(objectives) if objectives is not None else ()
        prior = tuple(previous_evidence or ())
        # Prefer journey-level evidence when caller does not supply prior.
        if previous_evidence is None and journey.evidence:
            prior = tuple(journey.evidence)

        effort = PlanningPolicy.estimate_effort(
            objs,
            explicit=estimated_effort,
            previous_evidence_count=len(prior),
        )
        activities = PlanningPolicy.activities_for(objs)
        rationale = PlanningPolicy.rationale_tags(
            topic_id=tid,
            objectives=objs,
            previous_evidence=prior,
            estimated_effort=effort,
        )
        seq = sequence_index
        if seq is None:
            seq = 0
            if journey.sessions:
                seq = max(s.sequence_index for s in journey.sessions) + 1
        if seq < 0:
            raise PlanningError("sequence_index must be non-negative")

        sid = session_id or f"sess-{self._id_factory()}"
        return LearningSessionPlan(
            session_id=sid,
            journey_id=jid,
            topic_id=tid,
            sequence_index=seq,
            objective_ids=PlanningPolicy.objective_ids(objs),
            estimated_effort=effort,
            recommended_activities=activities,
            previous_evidence_count=len(prior),
            rationale_tags=rationale,
        )

    def plan_from_session(
        self,
        session: LearningSession,
        *,
        topic_id: str,
        objectives: (
            list[LearningObjective] | tuple[LearningObjective, ...] | None
        ) = None,
        previous_evidence: (
            list[JourneyEvidence] | tuple[JourneyEvidence, ...] | None
        ) = None,
    ) -> LearningSessionPlan:
        """Rebuild a plan describing an existing session."""
        objs = tuple(objectives or ())
        prior = tuple(previous_evidence or ())
        effort = session.estimated_effort
        return LearningSessionPlan(
            session_id=session.session_id,
            journey_id=session.journey_id,
            topic_id=topic_id,
            sequence_index=session.sequence_index,
            objective_ids=(
                PlanningPolicy.objective_ids(objs)
                if objs
                else ((session.objective_id,) if session.objective_id else ())
            ),
            estimated_effort=effort,
            recommended_activities=PlanningPolicy.activities_for(objs),
            previous_evidence_count=len(prior),
            rationale_tags=PlanningPolicy.rationale_tags(
                topic_id=topic_id,
                objectives=objs,
                previous_evidence=prior,
                estimated_effort=effort,
            ),
        )
