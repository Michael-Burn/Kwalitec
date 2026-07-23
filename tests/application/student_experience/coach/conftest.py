"""Shared factories for AI Learning Coach (XP-005) tests."""

from __future__ import annotations

from datetime import time, timedelta

import pytest

from application.education.mission_generation import MissionType
from application.education.revision_planner.enums import SessionStatus
from application.student_experience.coach import (
    CoachContext,
    CoachContextPublisher,
    CoachInputs,
    CoachPublisher,
    CoachSnapshot,
    ConversationContext,
    LearningCoachService,
    ReflectionPrompts,
)
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
    WorkspaceSnapshot,
)
from application.student_experience.workspace.ids import WorkspaceSnapshotId
from tests.application.student_experience.home.conftest import (
    AS_OF,
    COMPETENCY_BAYES,
    STUDENT_ID,
    SUBJECT_ALGEBRA,
    SUBJECT_PROBABILITY,
    TODAY,
    make_evaluation,
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
from tests.application.student_experience.workspace.conftest import (
    make_active_execution,
    make_multi_step_mission,
)
from tests.application.student_experience.workspace.conftest import (
    make_full_inputs as make_workspace_inputs,
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
def service() -> LearningCoachService:
    return LearningCoachService()


def make_home_snapshot():
    home_service = StudentHomeService()
    home = home_service.build_home(make_home_inputs(), home_id="home-for-coach")
    return home_service.build_snapshot(home, snapshot_id=HomeSnapshotId("hsnap-c001"))


def make_journey_snapshot(*, streak: int = 7) -> JourneySnapshot:
    return JourneySnapshot(
        snapshot_id=JourneySnapshotId("jsnap-c001"),
        student_id=STUDENT_ID,
        captured_at=AS_OF,
        trajectory=TrajectoryLabel.BUILDING,
        trajectory_message="You're building a steady study rhythm.",
        timeline_event_count=6,
        milestone_count=2,
        current_streak_days=streak,
        longest_streak_days=max(streak, 7),
        weekly_missions_completed=4,
        monthly_missions_completed=10,
        mastery_trend=TrendDirection.IMPROVING,
        consistency_message="Your study consistency is encouraging.",
        habits_message="You tend to study in the morning.",
    )


def make_rich_journey_snapshot() -> JourneySnapshot:
    journey_service = LearningJourneyService()
    journey = journey_service.build_journey(
        make_journey_inputs(), journey_id="journey-for-coach"
    )
    return journey_service.build_snapshot(
        journey, snapshot_id=JourneySnapshotId("jsnap-c-rich")
    )


def make_readiness_snapshot() -> ReadinessSnapshot:
    readiness_service = ExamReadinessService()
    readiness = readiness_service.build_readiness(
        make_readiness_inputs(), readiness_id="readiness-for-coach"
    )
    return readiness_service.build_snapshot(
        readiness, snapshot_id=ReadinessSnapshotId("rsnap-c001")
    )


def make_workspace_snapshot() -> WorkspaceSnapshot:
    workspace_service = StudyWorkspaceService()
    workspace = workspace_service.build_workspace(
        make_workspace_inputs(), workspace_id="workspace-for-coach"
    )
    return workspace_service.build_snapshot(
        workspace, snapshot_id=WorkspaceSnapshotId("wsnap-c001")
    )


def make_empty_inputs(**overrides) -> CoachInputs:
    base = {
        "student_id": STUDENT_ID,
        "as_of": AS_OF,
    }
    base.update(overrides)
    return CoachInputs(**base)


def make_full_inputs(**overrides) -> CoachInputs:
    prereq = make_mission(
        "mission-prereq",
        mission_type=MissionType.REVISE_PREREQUISITE,
        rank=1,
        subject=SUBJECT_PROBABILITY,
        competency="foundations",
    )
    primary = make_multi_step_mission("mission-001", steps=3, rank=2)
    plan = make_plan((prereq, primary), plan_id="plan-coach-001")
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
        plan_id="plan-coach-001",
    )
    base = {
        "student_id": STUDENT_ID,
        "as_of": AS_OF,
        "home_snapshot": make_home_snapshot(),
        "journey_snapshot": make_journey_snapshot(streak=7),
        "readiness_snapshot": make_readiness_snapshot(),
        "workspace_snapshot": make_workspace_snapshot(),
        "evaluation": make_evaluation(),
        "mission_plan": plan,
        "schedule": schedule,
        "mission_execution": execution,
    }
    base.update(overrides)
    return CoachInputs(**base)


class RecordingCoachPublisher(CoachPublisher):
    def __init__(self) -> None:
        self.conversations: list[ConversationContext] = []
        self.reflections: list[ReflectionPrompts] = []
        self.snapshots: list[CoachSnapshot] = []

    def publish_conversation(self, conversation: ConversationContext) -> None:
        self.conversations.append(conversation)

    def publish_reflection(self, reflection: ReflectionPrompts) -> None:
        self.reflections.append(reflection)

    def publish_snapshot(self, snapshot: CoachSnapshot) -> None:
        self.snapshots.append(snapshot)


class RecordingCoachContextPublisher(CoachContextPublisher):
    def __init__(self) -> None:
        self.contexts: list[CoachContext] = []
        self.snapshots: list[CoachSnapshot] = []

    def publish_context(self, context: CoachContext) -> None:
        self.contexts.append(context)

    def publish_snapshot(self, snapshot: CoachSnapshot) -> None:
        self.snapshots.append(snapshot)
