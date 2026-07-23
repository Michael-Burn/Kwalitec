"""WorkspaceInputs — caller-supplied Education OS artefacts for workspace."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.education.mission_execution.models.mission_execution import (
    MissionExecution,
)
from application.education.mission_generation.models.mission_plan import MissionPlan
from application.education.revision_planner.models.study_schedule import StudySchedule
from application.education.revision_planner.models.study_session import StudySession
from application.student_experience.home.models.home_snapshot import HomeSnapshot
from application.student_experience.progress.models.journey_snapshot import (
    JourneySnapshot,
)
from application.student_experience.readiness.models.readiness_snapshot import (
    ReadinessSnapshot,
)
from application.student_experience.workspace.errors import (
    WorkspaceInvariantViolation,
)


@dataclass(frozen=True, slots=True)
class WorkspaceInputs:
    """Immutable bundle of Education OS outputs for Study Workspace composition.

    Educational artefacts are optional so the workspace degrades gracefully.
    ``student_id`` and ``as_of`` are always required. ``as_of`` is
    caller-supplied — never wall clock.

    ``home_snapshot``, ``readiness_snapshot``, and ``journey_snapshot`` are
    compact Student Experience projections — never raw Education OS aggregates.
    """

    student_id: str
    as_of: datetime
    schedule: StudySchedule | None = None
    current_session: StudySession | None = None
    mission_execution: MissionExecution | None = None
    mission_plan: MissionPlan | None = None
    home_snapshot: HomeSnapshot | None = None
    readiness_snapshot: ReadinessSnapshot | None = None
    journey_snapshot: JourneySnapshot | None = None

    def __post_init__(self) -> None:
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise WorkspaceInvariantViolation(
                "student_id must be a non-empty string",
                invariant="WorkspaceInputs.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        if not isinstance(self.as_of, datetime):
            raise WorkspaceInvariantViolation(
                "as_of must be a datetime",
                invariant="WorkspaceInputs.as_of.type",
            )
        if self.schedule is not None and not isinstance(self.schedule, StudySchedule):
            raise WorkspaceInvariantViolation(
                "schedule must be a StudySchedule when provided",
                invariant="WorkspaceInputs.schedule.type",
            )
        if self.current_session is not None and not isinstance(
            self.current_session, StudySession
        ):
            raise WorkspaceInvariantViolation(
                "current_session must be a StudySession when provided",
                invariant="WorkspaceInputs.current_session.type",
            )
        if self.mission_execution is not None and not isinstance(
            self.mission_execution, MissionExecution
        ):
            raise WorkspaceInvariantViolation(
                "mission_execution must be a MissionExecution when provided",
                invariant="WorkspaceInputs.mission_execution.type",
            )
        if self.mission_plan is not None and not isinstance(
            self.mission_plan, MissionPlan
        ):
            raise WorkspaceInvariantViolation(
                "mission_plan must be a MissionPlan when provided",
                invariant="WorkspaceInputs.mission_plan.type",
            )
        if self.home_snapshot is not None and not isinstance(
            self.home_snapshot, HomeSnapshot
        ):
            raise WorkspaceInvariantViolation(
                "home_snapshot must be a HomeSnapshot when provided",
                invariant="WorkspaceInputs.home_snapshot.type",
            )
        if self.readiness_snapshot is not None and not isinstance(
            self.readiness_snapshot, ReadinessSnapshot
        ):
            raise WorkspaceInvariantViolation(
                "readiness_snapshot must be a ReadinessSnapshot when provided",
                invariant="WorkspaceInputs.readiness_snapshot.type",
            )
        if self.journey_snapshot is not None and not isinstance(
            self.journey_snapshot, JourneySnapshot
        ):
            raise WorkspaceInvariantViolation(
                "journey_snapshot must be a JourneySnapshot when provided",
                invariant="WorkspaceInputs.journey_snapshot.type",
            )
        # Prefer execution-embedded plan when caller omitted mission_plan.
        if self.mission_plan is None and self.mission_execution is not None:
            object.__setattr__(self, "mission_plan", self.mission_execution.plan)
        # Prefer schedule session when current_session omitted.
        if self.current_session is None and self.schedule is not None:
            object.__setattr__(
                self,
                "current_session",
                _resolve_current_session(self.schedule, self.as_of),
            )


def _resolve_current_session(
    schedule: StudySchedule, as_of: datetime
) -> StudySession | None:
    """Pick today's earliest active session when one exists."""
    today = as_of.date()
    candidates = [
        session
        for session in schedule.sessions
        if session.session_date == today and session.is_active()
    ]
    if not candidates:
        return None
    return sorted(
        candidates, key=lambda session: (session.start_time, session.sequence_index)
    )[0]
