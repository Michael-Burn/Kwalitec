"""Shared factories for Experience Integration (PX-002) tests."""

from __future__ import annotations

from application.student_experience.coach import (
    CoachContext,
    CoachContextPublisher,
    CoachSnapshot,
    LearningCoachService,
)
from application.student_experience.home import (
    HomePublisher,
    HomeSnapshot,
    HomeViewModel,
)
from application.student_experience.integration import (
    ExperienceIntegrationPublisher,
    ExperienceIntegrationService,
    ExperienceJourneyViewModel,
    ExperienceSnapshotBundle,
    IntegrationInputs,
)
from application.student_experience.integration.integration_composer import (
    aligned_module_inputs,
)
from application.student_experience.progress import (
    JourneyPublisher,
    JourneySnapshot,
    LearningJourneyService,
    LearningJourneyViewModel,
)
from application.student_experience.readiness import (
    ExamReadinessService,
    ExamReadinessViewModel,
    ReadinessPublisher,
    ReadinessSnapshot,
)
from application.student_experience.workspace import (
    StudyWorkspaceService,
    StudyWorkspaceViewModel,
    WorkspacePublisher,
    WorkspaceSnapshot,
)
from tests.application.student_experience.home.conftest import (
    AS_OF,
    STUDENT_ID,
)
from tests.application.student_experience.home.conftest import (
    make_full_inputs as make_home_inputs,
)

__all__ = [
    "AS_OF",
    "STUDENT_ID",
    "RecordingIntegrationPublisher",
    "RecordingCoachContextPublisher",
    "make_integration_inputs",
    "make_service",
]


class RecordingIntegrationPublisher(ExperienceIntegrationPublisher):
    def __init__(self) -> None:
        self.journeys: list[ExperienceJourneyViewModel] = []
        self.bundles: list[ExperienceSnapshotBundle] = []

    def publish_journey(self, journey: ExperienceJourneyViewModel) -> None:
        self.journeys.append(journey)

    def publish_bundle(self, bundle: ExperienceSnapshotBundle) -> None:
        self.bundles.append(bundle)


class RecordingCoachContextPublisher(CoachContextPublisher):
    def __init__(self) -> None:
        self.contexts: list[CoachContext] = []
        self.snapshots: list[CoachSnapshot] = []

    def publish_context(self, context: CoachContext) -> None:
        self.contexts.append(context)

    def publish_snapshot(self, snapshot: CoachSnapshot) -> None:
        self.snapshots.append(snapshot)


class RecordingHomePublisher(HomePublisher):
    def __init__(self) -> None:
        self.homes: list[HomeViewModel] = []
        self.snapshots: list[HomeSnapshot] = []

    def publish_home(self, home: HomeViewModel) -> None:
        self.homes.append(home)

    def publish_snapshot(self, snapshot: HomeSnapshot) -> None:
        self.snapshots.append(snapshot)


class RecordingJourneyPublisher(JourneyPublisher):
    def __init__(self) -> None:
        self.journeys: list[LearningJourneyViewModel] = []
        self.snapshots: list[JourneySnapshot] = []

    def publish_journey(self, journey: LearningJourneyViewModel) -> None:
        self.journeys.append(journey)

    def publish_snapshot(self, snapshot: JourneySnapshot) -> None:
        self.snapshots.append(snapshot)


class RecordingReadinessPublisher(ReadinessPublisher):
    def __init__(self) -> None:
        self.readiness: list[ExamReadinessViewModel] = []
        self.snapshots: list[ReadinessSnapshot] = []

    def publish_readiness(self, readiness: ExamReadinessViewModel) -> None:
        self.readiness.append(readiness)

    def publish_snapshot(self, snapshot: ReadinessSnapshot) -> None:
        self.snapshots.append(snapshot)


class RecordingWorkspacePublisher(WorkspacePublisher):
    def __init__(self) -> None:
        self.workspaces: list[StudyWorkspaceViewModel] = []
        self.snapshots: list[WorkspaceSnapshot] = []

    def publish_workspace(self, workspace: StudyWorkspaceViewModel) -> None:
        self.workspaces.append(workspace)

    def publish_snapshot(self, snapshot: WorkspaceSnapshot) -> None:
        self.snapshots.append(snapshot)


def make_integration_inputs(**home_overrides) -> IntegrationInputs:
    home = make_home_inputs(**home_overrides)
    journey, readiness, workspace = aligned_module_inputs(home)
    return IntegrationInputs(
        home=home,
        journey=journey,
        readiness=readiness,
        workspace=workspace,
    )


def make_service(
    *,
    publisher: ExperienceIntegrationPublisher | None = None,
    coach_context_publisher: CoachContextPublisher | None = None,
    home_publisher: HomePublisher | None = None,
    journey_publisher: JourneyPublisher | None = None,
    readiness_publisher: ReadinessPublisher | None = None,
    workspace_publisher: WorkspacePublisher | None = None,
) -> ExperienceIntegrationService:
    from application.student_experience.home import StudentHomeService

    return ExperienceIntegrationService(
        home_service=StudentHomeService(home_publisher=home_publisher),
        journey_service=LearningJourneyService(journey_publisher=journey_publisher),
        readiness_service=ExamReadinessService(
            readiness_publisher=readiness_publisher
        ),
        workspace_service=StudyWorkspaceService(
            workspace_publisher=workspace_publisher
        ),
        coach_service=LearningCoachService(
            coach_context_publisher=coach_context_publisher
        ),
        publisher=publisher,
    )
