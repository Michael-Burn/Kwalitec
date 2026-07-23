"""StudyWorkspaceViewModel — composed Adaptive Study Workspace surface."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.student_experience.workspace.errors import WorkspaceInvariantViolation
from application.student_experience.workspace.ids import WorkspaceId
from application.student_experience.workspace.models.completion_card import (
    CompletionCard,
)
from application.student_experience.workspace.models.current_session_card import (
    CurrentSessionCard,
)
from application.student_experience.workspace.models.focus_card import FocusCard
from application.student_experience.workspace.models.mission_card import MissionCard
from application.student_experience.workspace.models.objectives_card import (
    ObjectivesCard,
)
from application.student_experience.workspace.models.progress_card import ProgressCard
from application.student_experience.workspace.models.reflection_card import (
    ReflectionCard,
)
from application.student_experience.workspace.models.resources_card import ResourcesCard
from application.student_experience.workspace.models.session_timer_card import (
    SessionTimerCard,
)


@dataclass(frozen=True, slots=True)
class StudyWorkspaceViewModel:
    """Immutable composed Adaptive Study Workspace experience.

    Focused, distraction-free projection of the current StudySession.
    Never exposes Education OS type names or internal architecture.
    """

    workspace_id: WorkspaceId
    student_id: str
    composed_at: datetime
    current_session: CurrentSessionCard
    mission: MissionCard
    objectives: ObjectivesCard
    resources: ResourcesCard
    progress: ProgressCard
    focus: FocusCard
    session_timer: SessionTimerCard
    reflection: ReflectionCard
    completion: CompletionCard

    def __post_init__(self) -> None:
        if not isinstance(self.workspace_id, WorkspaceId):
            raise WorkspaceInvariantViolation(
                "workspace_id must be a WorkspaceId",
                invariant="StudyWorkspaceViewModel.workspace_id.type",
            )
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise WorkspaceInvariantViolation(
                "student_id must be a non-empty string",
                invariant="StudyWorkspaceViewModel.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        if not isinstance(self.composed_at, datetime):
            raise WorkspaceInvariantViolation(
                "composed_at must be a datetime",
                invariant="StudyWorkspaceViewModel.composed_at.type",
            )
        expected = {
            "current_session": CurrentSessionCard,
            "mission": MissionCard,
            "objectives": ObjectivesCard,
            "resources": ResourcesCard,
            "progress": ProgressCard,
            "focus": FocusCard,
            "session_timer": SessionTimerCard,
            "reflection": ReflectionCard,
            "completion": CompletionCard,
        }
        for name, expected_type in expected.items():
            value = getattr(self, name)
            if not isinstance(value, expected_type):
                raise WorkspaceInvariantViolation(
                    f"{name} must be a {expected_type.__name__}",
                    invariant=f"StudyWorkspaceViewModel.{name}.type",
                )
