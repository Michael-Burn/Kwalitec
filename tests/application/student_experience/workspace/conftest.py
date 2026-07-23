"""Shared factories for Adaptive Study Workspace (XP-004) tests."""

from __future__ import annotations

from datetime import time, timedelta

import pytest

from application.education.mission_execution import (
    ExecutionId,
    ExecutionStatus,
    MissionExecution,
)
from application.education.mission_execution.models.confidence_record import (
    ConfidenceRecord,
)
from application.education.mission_generation import (
    MissionId,
    MissionPlan,
    MissionStep,
    MissionStepAction,
    MissionStepId,
    MissionType,
)
from application.education.revision_planner.enums import SessionStatus
from application.student_experience.home import StudentHomeService
from application.student_experience.home.ids import SnapshotId as HomeSnapshotId
from application.student_experience.progress import (
    JourneySnapshot,
    LearningJourneyService,
    TrajectoryLabel,
    TrendDirection,
)
from application.student_experience.progress.ids import JourneySnapshotId
from application.student_experience.readiness import (
    ExamReadinessService,
    ReadinessSnapshot,
)
from application.student_experience.readiness.ids import ReadinessSnapshotId
from application.student_experience.workspace import (
    StudyWorkspaceService,
    StudyWorkspaceViewModel,
    WorkspaceInputs,
    WorkspacePublisher,
    WorkspaceResource,
    WorkspaceResourceProvider,
    WorkspaceSnapshot,
)
from domain.education.foundation.enums import ConfidenceLevel
from tests.application.student_experience.home.conftest import (
    AS_OF,
    COMPETENCY_BAYES,
    STUDENT_ID,
    SUBJECT_ALGEBRA,
    SUBJECT_PROBABILITY,
    TODAY,
    make_exam_target,
    make_mission,
    make_plan,
    make_schedule,
    make_session,
)
from tests.application.student_experience.home.conftest import (
    make_full_inputs as make_home_inputs,
)
from tests.application.student_experience.progress.conftest import (
    make_rich_inputs as make_journey_inputs,
)
from tests.application.student_experience.readiness.conftest import (
    make_full_inputs as make_readiness_inputs,
)

__all__ = [
    "AS_OF",
    "COMPETENCY_BAYES",
    "STUDENT_ID",
    "SUBJECT_ALGEBRA",
    "SUBJECT_PROBABILITY",
    "TODAY",
]


@pytest.fixture
def as_of():
    return AS_OF


@pytest.fixture
def service() -> StudyWorkspaceService:
    return StudyWorkspaceService()


def make_multi_step_mission(
    mission_id: str = "mission-001",
    *,
    steps: int = 3,
    duration_minutes: int = 45,
    mission_type: MissionType = MissionType.PRACTICE_QUESTIONS,
    rank: int = 1,
) -> object:
    per_step = max(1, duration_minutes // steps)
    step_items: list[MissionStep] = []
    actions = (
        MissionStepAction.PRACTICE,
        MissionStepAction.REVIEW,
        MissionStepAction.CONSOLIDATE,
    )
    for index in range(1, steps + 1):
        step_items.append(
            MissionStep(
                step_id=MissionStepId(f"{mission_id}:s{index}"),
                action=actions[(index - 1) % len(actions)],
                order=index,
                estimated_minutes=per_step,
                subject_id=SUBJECT_PROBABILITY,
                competency_id=COMPETENCY_BAYES,
            )
        )
    from application.education.mission_generation import (
        Mission,
        MissionEstimate,
        MissionObjective,
        MissionObjectiveCode,
        MissionOrdering,
    )

    return Mission(
        mission_id=MissionId(mission_id),
        mission_type=mission_type,
        objective=MissionObjective(
            code=MissionObjectiveCode.COMPLETE_PRACTICE,
            subject_id=SUBJECT_PROBABILITY,
            competency_id=COMPETENCY_BAYES,
        ),
        estimate=MissionEstimate(duration_minutes=duration_minutes),
        ordering=MissionOrdering(rank=rank, priority_magnitude=0.80),
        steps=tuple(step_items),
        subject_id=SUBJECT_PROBABILITY,
        competency_id=COMPETENCY_BAYES,
    )


def make_active_execution(
    plan: MissionPlan,
    *,
    mission_id: str = "mission-001",
    execution_id: str = "exec-ws-001",
    status: ExecutionStatus = ExecutionStatus.STARTED,
    elapsed_seconds: float = 600.0,
    completed_step_indexes: tuple[int, ...] = (1,),
) -> MissionExecution:
    execution = MissionExecution.plan_execution(
        execution_id=ExecutionId(execution_id),
        mission_plan=plan,
        mission_id=MissionId(mission_id),
    )
    steps = execution.mission.steps
    completed = tuple(
        steps[index - 1].step_id
        for index in completed_step_indexes
        if 1 <= index <= len(steps)
    )
    next_index = len(completed)
    current = steps[next_index].step_id if next_index < len(steps) else None
    return execution.with_updates(
        status=status,
        started_at=AS_OF - timedelta(minutes=10),
        last_active_at=AS_OF,
        elapsed_study_time_seconds=elapsed_seconds,
        completed_step_ids=completed,
        current_step_id=current,
        confidence_history=(
            ConfidenceRecord(
                level=ConfidenceLevel.MEDIUM,
                recorded_at=AS_OF - timedelta(minutes=5),
            ),
        ),
    )


def make_home_snapshot():
    home_service = StudentHomeService()
    home = home_service.build_home(make_home_inputs(), home_id="home-for-workspace")
    return home_service.build_snapshot(home, snapshot_id=HomeSnapshotId("hsnap-w001"))


def make_journey_snapshot() -> JourneySnapshot:
    journey_service = LearningJourneyService()
    journey = journey_service.build_journey(
        make_journey_inputs(), journey_id="journey-for-workspace"
    )
    return journey_service.build_snapshot(
        journey, snapshot_id=JourneySnapshotId("jsnap-w001")
    )


def make_minimal_journey_snapshot() -> JourneySnapshot:
    return JourneySnapshot(
        snapshot_id=JourneySnapshotId("jsnap-w-min"),
        student_id=STUDENT_ID,
        captured_at=AS_OF,
        trajectory=TrajectoryLabel.BUILDING,
        trajectory_message="You're building a steady study rhythm.",
        timeline_event_count=4,
        milestone_count=2,
        current_streak_days=3,
        longest_streak_days=5,
        weekly_missions_completed=3,
        monthly_missions_completed=8,
        mastery_trend=TrendDirection.IMPROVING,
        consistency_message="Your study consistency is encouraging.",
        habits_message="You tend to study in the morning.",
    )


def make_readiness_snapshot() -> ReadinessSnapshot:
    readiness_service = ExamReadinessService()
    readiness = readiness_service.build_readiness(
        make_readiness_inputs(), readiness_id="readiness-for-workspace"
    )
    return readiness_service.build_snapshot(
        readiness, snapshot_id=ReadinessSnapshotId("rsnap-w001")
    )


def make_empty_inputs(**overrides) -> WorkspaceInputs:
    base = {
        "student_id": STUDENT_ID,
        "as_of": AS_OF,
    }
    base.update(overrides)
    return WorkspaceInputs(**base)


def make_full_inputs(**overrides) -> WorkspaceInputs:
    prereq = make_mission(
        "mission-prereq",
        mission_type=MissionType.REVISE_PREREQUISITE,
        rank=1,
        subject=SUBJECT_PROBABILITY,
        competency="foundations",
    )
    primary = make_multi_step_mission("mission-001", steps=3, rank=2)
    plan = make_plan((prereq, primary), plan_id="plan-ws-001")
    execution = make_active_execution(plan, mission_id="mission-001")
    current = make_session(
        session_id="session-today",
        session_date=TODAY,
        mission_ids=("mission-001",),
        status=SessionStatus.IN_PROGRESS,
        duration=45,
        start=time(9, 0),
        end=time(9, 45),
    )
    schedule = make_schedule(
        sessions=(
            current,
            make_session(
                session_id="session-next",
                session_date=TODAY + timedelta(days=1),
                mission_ids=("mission-prereq",),
                status=SessionStatus.PLANNED,
                start=time(10, 0),
                end=time(10, 30),
                duration=30,
            ),
        ),
        exam_target=make_exam_target(exam_date=TODAY + timedelta(days=20)),
        plan_id="plan-ws-001",
    )
    base = {
        "student_id": STUDENT_ID,
        "as_of": AS_OF,
        "schedule": schedule,
        "current_session": current,
        "mission_execution": execution,
        "mission_plan": plan,
        "home_snapshot": make_home_snapshot(),
        "readiness_snapshot": make_readiness_snapshot(),
        "journey_snapshot": make_minimal_journey_snapshot(),
    }
    base.update(overrides)
    return WorkspaceInputs(**base)


class RecordingWorkspacePublisher(WorkspacePublisher):
    def __init__(self) -> None:
        self.workspaces: list[StudyWorkspaceViewModel] = []
        self.snapshots: list[WorkspaceSnapshot] = []

    def publish_workspace(self, workspace: StudyWorkspaceViewModel) -> None:
        self.workspaces.append(workspace)

    def publish_snapshot(self, snapshot: WorkspaceSnapshot) -> None:
        self.snapshots.append(snapshot)


class FakeWorkspaceResourceProvider(WorkspaceResourceProvider):
    def __init__(
        self, resources: tuple[WorkspaceResource, ...] | None = None
    ) -> None:
        self._resources = resources or (
            WorkspaceResource(
                resource_id="res-001",
                title="Practice sheet",
                detail="Complete the attached practice questions.",
                kind="task",
                estimated_minutes=15,
            ),
            WorkspaceResource(
                resource_id="res-002",
                title="Concept summary",
                detail="Skim the concept summary before practice.",
                kind="reference",
                estimated_minutes=5,
            ),
        )

    def list_resources(
        self,
        student_id: str,
        *,
        mission_id: str | None = None,
        session_id: str | None = None,
        limit: int = 10,
    ) -> tuple[WorkspaceResource, ...]:
        return self._resources[:limit]
