"""CoachInputs — caller-supplied artefacts for AI Learning Coach composition."""

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
from application.student_experience.coach.errors import CoachInvariantViolation
from application.student_experience.home.models.home_snapshot import HomeSnapshot
from application.student_experience.progress.models.journey_snapshot import (
    JourneySnapshot,
)
from application.student_experience.readiness.models.readiness_snapshot import (
    ReadinessSnapshot,
)
from application.student_experience.workspace.models.workspace_snapshot import (
    WorkspaceSnapshot,
)


@dataclass(frozen=True, slots=True)
class CoachInputs:
    """Immutable bundle of Student Experience + Education OS artefacts.

    All educational artefacts are optional so coaching degrades gracefully.
    ``student_id`` and ``as_of`` are always required. ``as_of`` is
    caller-supplied — never wall clock.

    Snapshots are compact Student Experience projections. Raw Education OS
    aggregates (evaluation, plan, schedule, execution) supply attribution
    the coach may narrate — never invent.
    """

    student_id: str
    as_of: datetime
    home_snapshot: HomeSnapshot | None = None
    journey_snapshot: JourneySnapshot | None = None
    readiness_snapshot: ReadinessSnapshot | None = None
    workspace_snapshot: WorkspaceSnapshot | None = None
    evaluation: EducationalEvaluation | None = None
    mission_plan: MissionPlan | None = None
    schedule: StudySchedule | None = None
    mission_execution: MissionExecution | None = None

    def __post_init__(self) -> None:
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise CoachInvariantViolation(
                "student_id must be a non-empty string",
                invariant="CoachInputs.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        if not isinstance(self.as_of, datetime):
            raise CoachInvariantViolation(
                "as_of must be a datetime",
                invariant="CoachInputs.as_of.type",
            )
        _require_optional_type(
            self.home_snapshot, HomeSnapshot, "home_snapshot", "CoachInputs"
        )
        _require_optional_type(
            self.journey_snapshot,
            JourneySnapshot,
            "journey_snapshot",
            "CoachInputs",
        )
        _require_optional_type(
            self.readiness_snapshot,
            ReadinessSnapshot,
            "readiness_snapshot",
            "CoachInputs",
        )
        _require_optional_type(
            self.workspace_snapshot,
            WorkspaceSnapshot,
            "workspace_snapshot",
            "CoachInputs",
        )
        _require_optional_type(
            self.evaluation, EducationalEvaluation, "evaluation", "CoachInputs"
        )
        _require_optional_type(
            self.mission_plan, MissionPlan, "mission_plan", "CoachInputs"
        )
        _require_optional_type(
            self.schedule, StudySchedule, "schedule", "CoachInputs"
        )
        _require_optional_type(
            self.mission_execution,
            MissionExecution,
            "mission_execution",
            "CoachInputs",
        )
        # Prefer execution-embedded plan when caller omitted mission_plan.
        if self.mission_plan is None and self.mission_execution is not None:
            object.__setattr__(self, "mission_plan", self.mission_execution.plan)


def _require_optional_type(
    value: object,
    expected: type,
    name: str,
    owner: str,
) -> None:
    if value is not None and not isinstance(value, expected):
        raise CoachInvariantViolation(
            f"{name} must be a {expected.__name__} when provided",
            invariant=f"{owner}.{name}.type",
        )
