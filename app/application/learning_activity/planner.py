"""Constructs an ActivityPlan for execution inside a Learning Session.

Framework-independent. Deterministic. Never generates study content or
estimates mastery.
"""

from __future__ import annotations

from app.application.learning_activity.dto.activity_plan import (
    ActivityPlan,
    ActivityPlanItem,
)
from app.application.learning_activity.exceptions import PlanningError
from app.application.learning_activity.policies.sequencing_policy import (
    SequencingPolicy,
)
from app.domain.learning_activity.value_objects.activity_type import ActivityType


class ActivityPlanner:
    """Build a deterministic ``ActivityPlan`` for activity sequencing."""

    def plan(
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
        """Construct an activity plan from structural inputs.

        Args:
            session_id: Parent Learning Session identity.
            journey_id: Parent journey identity when known.
            activity_types: Explicit activity types to sequence.
            activity_tags: Structural planner tags mapped to types.
            items: Fully specified plan items (overrides types/tags).
            require_introduction: Optionally bookend with INTRODUCTION.
            require_summary: Optionally bookend with SUMMARY.
            require_reflection: Optionally bookend with REFLECTION.
            preserve_input_order: Keep caller order vs priority-sort.

        Returns:
            Immutable ActivityPlan.

        Raises:
            PlanningError: When session_id is missing.
        """
        sid = (session_id or "").strip()
        if not sid:
            raise PlanningError("session_id is required to plan activities")

        if items is not None:
            plan_items = tuple(items)
            if not plan_items:
                raise PlanningError("activity plan items must not be empty")
            rationale = (
                "source=explicit_items",
                f"count={len(plan_items)}",
                "no_content_generation",
                "no_ai",
            )
            return ActivityPlan(
                session_id=sid,
                journey_id=_optional_id(journey_id),
                items=plan_items,
                rationale_tags=rationale,
            )

        if activity_types is not None:
            types = tuple(ActivityType.resolve(t) for t in activity_types)
            source = "explicit_types"
        elif activity_tags is not None:
            types = SequencingPolicy.types_from_tags(activity_tags)
            source = "activity_tags"
        else:
            types = SequencingPolicy.default_types()
            source = "default_arc"

        types = SequencingPolicy.order_types(
            types, preserve_input_order=preserve_input_order
        )
        types = SequencingPolicy.ensure_bookends(
            types,
            require_introduction=require_introduction,
            require_summary=require_summary,
            require_reflection=require_reflection,
        )
        if not types:
            raise PlanningError("activity plan resolved to zero types")

        plan_items = tuple(
            ActivityPlanItem(activity_type=activity_type) for activity_type in types
        )
        rationale = (
            f"source={source}",
            f"count={len(plan_items)}",
            f"preserve_order={preserve_input_order}",
            "no_content_generation",
            "no_ai",
        )
        return ActivityPlan(
            session_id=sid,
            journey_id=_optional_id(journey_id),
            items=plan_items,
            rationale_tags=rationale,
        )


def _optional_id(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None
