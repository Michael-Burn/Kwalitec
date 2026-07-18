"""Immutable plan describing activities to execute inside a Learning Session."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.learning_activity.value_objects.activity_type import ActivityType


@dataclass(frozen=True)
class ActivityPlanItem:
    """One planned activity step (structural; not study content).

    Attributes:
        activity_type: Structural activity kind.
        title: Optional structural label.
        objective_id: Optional objective this step addresses.
        metadata: Immutable structural tags.
        requested_id: Optional caller-supplied activity identity.
    """

    activity_type: ActivityType
    title: str | None = None
    objective_id: str | None = None
    metadata: tuple[str, ...] = ()
    requested_id: str | None = None


@dataclass(frozen=True)
class ActivityPlan:
    """Deterministic activity plan produced by the Activity Planner.

    Attributes:
        session_id: Parent Learning Session identity.
        journey_id: Parent Learning Journey identity when known.
        items: Ordered planned activity steps.
        rationale_tags: Explainable planning rationale tags.
    """

    session_id: str
    journey_id: str | None
    items: tuple[ActivityPlanItem, ...]
    rationale_tags: tuple[str, ...]
