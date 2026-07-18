"""Shared helpers for Learning Activity Engine application tests."""

from __future__ import annotations

from app.application.learning_activity.dto.activity_plan import (
    ActivityPlan,
    ActivityPlanItem,
)
from app.application.learning_activity.dto.activity_sequence import ActivitySequence
from app.application.learning_activity.engine import (
    ActivityHandle,
    LearningActivityEngine,
)
from app.domain.learning_activity.entities.learning_activity import LearningActivity
from app.domain.learning_activity.value_objects.activity_state import ActivityState
from app.domain.learning_activity.value_objects.activity_type import ActivityType

SESSION_ID = "sess-1"
JOURNEY_ID = "journey-1"


def make_engine() -> LearningActivityEngine:
    return LearningActivityEngine(id_factory=lambda: "fixed")


def make_activity(
    activity_id: str = "act-1",
    *,
    session_id: str = SESSION_ID,
    activity_type: ActivityType = ActivityType.CONCEPT_LEARNING,
    sequence_index: int = 0,
    state: ActivityState = ActivityState.NOT_STARTED,
    title: str | None = None,
    objective_id: str | None = "obj-1",
    metadata: tuple[str, ...] = (),
    evidence_ids: tuple[str, ...] = (),
    reflection_ids: tuple[str, ...] = (),
) -> LearningActivity:
    return LearningActivity.create(
        activity_id,
        session_id,
        activity_type,
        sequence_index=sequence_index,
        state=state,
        title=title,
        objective_id=objective_id,
        metadata=list(metadata),
        evidence_ids=list(evidence_ids),
        reflection_ids=list(reflection_ids),
    )


def make_sequence(
    *,
    session_id: str = SESSION_ID,
    sequence_id: str = "seq-1",
    types: tuple[ActivityType, ...] | None = None,
    states: tuple[ActivityState, ...] | None = None,
) -> ActivitySequence:
    type_list = types or (
        ActivityType.INTRODUCTION,
        ActivityType.CONCEPT_LEARNING,
        ActivityType.REFLECTION,
    )
    state_list = states or tuple(
        ActivityState.NOT_STARTED for _ in type_list
    )
    activities = tuple(
        make_activity(
            f"act-{i}",
            session_id=session_id,
            activity_type=t,
            sequence_index=i,
            state=state_list[i],
        )
        for i, t in enumerate(type_list)
    )
    return ActivitySequence(
        session_id=session_id,
        sequence_id=sequence_id,
        activities=activities,
        plan_rationale_tags=("test",),
    )


def make_plan(
    *,
    session_id: str = SESSION_ID,
    journey_id: str | None = JOURNEY_ID,
    types: tuple[ActivityType, ...] | None = None,
) -> ActivityPlan:
    type_list = types or (
        ActivityType.INTRODUCTION,
        ActivityType.CONCEPT_LEARNING,
        ActivityType.SUMMARY,
    )
    return ActivityPlan(
        session_id=session_id,
        journey_id=journey_id,
        items=tuple(ActivityPlanItem(activity_type=t) for t in type_list),
        rationale_tags=("test",),
    )


def make_handle(
    engine: LearningActivityEngine | None = None,
    *,
    types: tuple[ActivityType, ...] | None = None,
    start_first: bool = False,
) -> ActivityHandle:
    eng = engine or make_engine()
    handle = eng.create_sequence(
        session_id=SESSION_ID,
        journey_id=JOURNEY_ID,
        activity_types=types
        or (
            ActivityType.INTRODUCTION,
            ActivityType.CONCEPT_LEARNING,
            ActivityType.WORKED_EXAMPLE,
            ActivityType.REFLECTION,
            ActivityType.SUMMARY,
        ),
        sequence_id="seq-test",
    )
    if start_first:
        handle, _ = eng.start_activity(handle)
    return handle
