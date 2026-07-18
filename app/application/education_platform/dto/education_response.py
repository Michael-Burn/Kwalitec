"""Immutable EducationResponse — output of every EducationPlatform workflow."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

from app.application.education_platform.dto.generated_mission import GeneratedMission
from app.application.education_platform.dto.generated_session import GeneratedSession
from app.application.education_platform.dto.platform_snapshot import PlatformSnapshot
from app.application.education_platform.dto.subject_plan import SubjectPlan
from app.application.education_platform.dto.workflow_result import WorkflowResult


@dataclass(frozen=True)
class EducationResponse:
    """Unified response envelope for Education Platform workflows.

    Carries structural artefacts produced by port coordination. Never
    invents educational content or mastery conclusions.
    """

    workflow: str
    success: bool
    request_correlation_id: str | None = None
    subject_plan: SubjectPlan | None = None
    journey_id: str | None = None
    blueprint_id: str | None = None
    sessions: tuple[GeneratedSession, ...] = ()
    activity_ids: tuple[str, ...] = ()
    missions: tuple[GeneratedMission, ...] = ()
    snapshot: PlatformSnapshot | None = None
    workflow_result: WorkflowResult | None = None
    validation_passed: bool | None = None
    validation_issues: tuple[str, ...] = ()
    error: str | None = None
    metadata: MappingProxyType | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "sessions", tuple(self.sessions))
        object.__setattr__(self, "activity_ids", tuple(self.activity_ids))
        object.__setattr__(self, "missions", tuple(self.missions))
        object.__setattr__(self, "validation_issues", tuple(self.validation_issues))
        if self.metadata is None:
            object.__setattr__(self, "metadata", MappingProxyType({}))
        elif not isinstance(self.metadata, MappingProxyType):
            object.__setattr__(
                self,
                "metadata",
                MappingProxyType(dict(self.metadata)),
            )
