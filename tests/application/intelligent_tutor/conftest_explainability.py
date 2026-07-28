"""Shared fixtures for AP-002D6 Tutor explainability tests."""

from __future__ import annotations

from datetime import UTC, datetime

from app.application.mission_engine.planning.mission_planning_service import (
    MissionPlanningService,
)
from app.domain.mission.planning.plan import StudyMissionPlan
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin
from tests.application.mission_engine.conftest_planning import (  # noqa: F401
    FIXED_AT,
    make_decision,
    make_decision_context,
    make_decision_set,
    make_graph,
    make_twin,
)

EXPLAIN_FIXED_AT = datetime(2026, 7, 28, 15, 0, 0, tzinfo=UTC).replace(tzinfo=None)


def make_study_mission_plan(
    *,
    twin: StudentDigitalTwin | None = None,
    planned_at: datetime = EXPLAIN_FIXED_AT,
) -> StudyMissionPlan:
    twin = twin or make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    result = MissionPlanningService().plan(
        twin,
        decision_set,
        learning_graph=make_graph(twin=twin),
        planned_at=planned_at,
        persist=False,
    )
    return result.study_mission_plan
