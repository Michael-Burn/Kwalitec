"""IntegrationInputs — caller-supplied artefacts for continuous journey composition."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.education.mission_execution.models.mission_execution import (
    MissionExecution,
)
from application.education.mission_generation.models.mission_plan import MissionPlan
from application.education.orchestration.dto.educational_evaluation import (
    EducationalEvaluation,
)
from application.education.revision_planner.models.study_schedule import StudySchedule
from application.student_experience.home.home_inputs import HomeInputs
from application.student_experience.integration.errors import (
    IntegrationInvariantViolation,
)
from application.student_experience.progress.journey_inputs import JourneyInputs
from application.student_experience.readiness.models.readiness_snapshot import (
    ReadinessSnapshot,
)
from application.student_experience.readiness.readiness_inputs import ReadinessInputs
from application.student_experience.workspace.workspace_inputs import WorkspaceInputs


@dataclass(frozen=True, slots=True)
class IntegrationInputs:
    """Immutable bundle coordinating Student Experience module inputs.

    Holds already-validated module inputs. The orchestrator never invents
    educational artefacts — it only chains existing XP composers.

    ``prior_readiness_snapshot`` enables natural readiness-change notices
    without isolated dashboards.
    """

    home: HomeInputs
    journey: JourneyInputs
    readiness: ReadinessInputs
    workspace: WorkspaceInputs
    evaluation: EducationalEvaluation | None = None
    mission_plan: MissionPlan | None = None
    schedule: StudySchedule | None = None
    mission_execution: MissionExecution | None = None
    prior_readiness_snapshot: ReadinessSnapshot | None = None
    evidence_recorded: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.home, HomeInputs):
            raise IntegrationInvariantViolation(
                "home must be a HomeInputs",
                invariant="IntegrationInputs.home.type",
            )
        if not isinstance(self.journey, JourneyInputs):
            raise IntegrationInvariantViolation(
                "journey must be a JourneyInputs",
                invariant="IntegrationInputs.journey.type",
            )
        if not isinstance(self.readiness, ReadinessInputs):
            raise IntegrationInvariantViolation(
                "readiness must be a ReadinessInputs",
                invariant="IntegrationInputs.readiness.type",
            )
        if not isinstance(self.workspace, WorkspaceInputs):
            raise IntegrationInvariantViolation(
                "workspace must be a WorkspaceInputs",
                invariant="IntegrationInputs.workspace.type",
            )
        if self.home.student_id != self.journey.student_id:
            raise IntegrationInvariantViolation(
                "module inputs must share student_id",
                invariant="IntegrationInputs.student_id.aligned",
            )
        if self.home.student_id != self.readiness.student_id:
            raise IntegrationInvariantViolation(
                "module inputs must share student_id",
                invariant="IntegrationInputs.student_id.aligned",
            )
        if self.home.student_id != self.workspace.student_id:
            raise IntegrationInvariantViolation(
                "module inputs must share student_id",
                invariant="IntegrationInputs.student_id.aligned",
            )
        if not isinstance(self.home.as_of, datetime):
            raise IntegrationInvariantViolation(
                "as_of must be a datetime",
                invariant="IntegrationInputs.as_of.type",
            )
        if self.prior_readiness_snapshot is not None and not isinstance(
            self.prior_readiness_snapshot, ReadinessSnapshot
        ):
            raise IntegrationInvariantViolation(
                "prior_readiness_snapshot must be a ReadinessSnapshot when provided",
                invariant="IntegrationInputs.prior_readiness_snapshot.type",
            )
        # Prefer home artefacts when coach extras omitted.
        if self.mission_plan is None and self.home.mission_plan is not None:
            object.__setattr__(self, "mission_plan", self.home.mission_plan)
        if self.schedule is None and self.home.schedule is not None:
            object.__setattr__(self, "schedule", self.home.schedule)
        if self.mission_execution is None and self.home.current_execution is not None:
            object.__setattr__(self, "mission_execution", self.home.current_execution)
        if self.evaluation is None and self.home.evaluation is not None:
            object.__setattr__(self, "evaluation", self.home.evaluation)

    @property
    def student_id(self) -> str:
        return self.home.student_id

    @property
    def as_of(self) -> datetime:
        return self.home.as_of
