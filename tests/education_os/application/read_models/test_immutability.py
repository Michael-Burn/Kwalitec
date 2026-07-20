"""Immutability tests for application read models (WEB-003)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, is_dataclass

import pytest

from application.read_models import (
    DashboardReadModel,
    MissionTaskReadModel,
    ProgressSummaryReadModel,
    RecommendationReadModel,
    TimelineEventReadModel,
    TimelineReadModel,
    TodaysMissionReadModel,
)

READ_MODEL_FACTORIES = [
    lambda: RecommendationReadModel(
        title="Continue studying",
        subtitle=None,
        primary_action="Start Session",
        reason_summary=None,
        estimated_minutes=25,
        can_start=True,
    ),
    lambda: MissionTaskReadModel(
        task_id="task-1",
        headline="Explanation",
        sequence_index=0,
        status="pending",
    ),
    lambda: TodaysMissionReadModel(
        title="Today's Session",
        summary="1 task",
        task_count=1,
        tasks=(
            MissionTaskReadModel(
                task_id="task-1",
                headline="Explanation",
                sequence_index=0,
                status="pending",
            ),
        ),
        estimated_minutes=25,
        can_open=True,
    ),
    lambda: ProgressSummaryReadModel(
        student_id="student-ada",
        activity_status="engaged",
        twin_status="active",
        concept_count=2,
        evidence_count=3,
        intervention_count=0,
        progress_cues=("activity:engaged",),
    ),
    lambda: TimelineEventReadModel(sequence=0, kind="created", label="Twin created"),
    lambda: TimelineReadModel(
        student_id="student-ada",
        events=(
            TimelineEventReadModel(sequence=0, kind="created", label="Twin created"),
        ),
    ),
    lambda: DashboardReadModel(
        student_id="student-ada",
        recommendation=None,
        todays_mission=None,
        progress=None,
        timeline=None,
    ),
]


@pytest.mark.parametrize("factory", READ_MODEL_FACTORIES)
def test_read_models_are_frozen_dataclasses(factory) -> None:
    model = factory()
    assert is_dataclass(model)
    assert model.__dataclass_params__.frozen  # type: ignore[attr-defined]
    field_name = next(iter(model.__dataclass_fields__))
    with pytest.raises(FrozenInstanceError):
        setattr(model, field_name, "mutated")


def test_nested_collections_are_tuples() -> None:
    mission = TodaysMissionReadModel(
        title="Today's Session",
        summary=None,
        task_count=0,
        tasks=(),
        estimated_minutes=None,
        can_open=False,
    )
    assert isinstance(mission.tasks, tuple)

    progress = ProgressSummaryReadModel(
        student_id="student-ada",
        activity_status="engaged",
        twin_status="active",
        concept_count=0,
        evidence_count=0,
        intervention_count=0,
        progress_cues=(),
    )
    assert isinstance(progress.progress_cues, tuple)
