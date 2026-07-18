"""Build an ordered ActivitySequence from an ActivityPlan.

Pure deterministic ordering. No educational AI. No study content generation.
"""

from __future__ import annotations

from app.application.learning_activity.dto.activity_plan import ActivityPlan
from app.application.learning_activity.dto.activity_sequence import ActivitySequence
from app.application.learning_activity.exceptions import PlanningError
from app.domain.learning_activity.entities.learning_activity import LearningActivity
from app.domain.learning_activity.value_objects.activity_state import ActivityState


class SequenceBuilder:
    """Produce an ordered ``ActivitySequence`` from an ``ActivityPlan``."""

    def __init__(self, *, id_factory=None) -> None:
        self._id_factory = id_factory or (lambda: "act")
        self._counter = 0

    def build(
        self,
        plan: ActivityPlan,
        *,
        sequence_id: str | None = None,
    ) -> ActivitySequence:
        """Materialise LearningActivity entities in plan order.

        Raises:
            PlanningError: When the plan has no items or duplicate requested ids.
        """
        if not plan.items:
            raise PlanningError("cannot build sequence from empty activity plan")

        activities: list[LearningActivity] = []
        seen_ids: set[str] = set()
        for index, item in enumerate(plan.items):
            activity_id = item.requested_id or self._next_id(plan.session_id, index)
            activity_id = activity_id.strip()
            if not activity_id:
                raise PlanningError("activity identity must be non-empty")
            if activity_id in seen_ids:
                raise PlanningError(f"duplicate activity identity: {activity_id!r}")
            seen_ids.add(activity_id)
            activities.append(
                LearningActivity.create(
                    activity_id,
                    plan.session_id,
                    item.activity_type,
                    sequence_index=index,
                    state=ActivityState.NOT_STARTED,
                    title=item.title,
                    objective_id=item.objective_id,
                    metadata=item.metadata,
                )
            )

        sid = sequence_id or f"seq-{plan.session_id}-{self._id_factory()}"
        return ActivitySequence(
            session_id=plan.session_id,
            sequence_id=sid,
            activities=tuple(activities),
            plan_rationale_tags=plan.rationale_tags,
        )

    def _next_id(self, session_id: str, index: int) -> str:
        self._counter += 1
        return f"act-{session_id}-{index}-{self._id_factory()}-{self._counter}"
