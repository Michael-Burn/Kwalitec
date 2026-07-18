"""Immutable PlatformSnapshot — read-only view of composed platform state."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

from app.application.education_platform.dto.generated_mission import GeneratedMission
from app.application.education_platform.dto.generated_session import GeneratedSession
from app.application.education_platform.dto.subject_plan import SubjectPlan


@dataclass(frozen=True)
class PlatformSnapshot:
    """Aggregated structural snapshot of the composed Educational Core.

    Assembled by coordinating registered ports. Never mutates engines.
    """

    platform_version: str
    learner_id: str
    curriculum_id: str | None = None
    subject_plan: SubjectPlan | None = None
    journey_id: str | None = None
    sessions: tuple[GeneratedSession, ...] = ()
    missions: tuple[GeneratedMission, ...] = ()
    registered_ports: tuple[str, ...] = ()
    missing_ports: tuple[str, ...] = ()
    workflow_readiness: MappingProxyType | None = None
    metadata: MappingProxyType | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "sessions", tuple(self.sessions))
        object.__setattr__(self, "missions", tuple(self.missions))
        object.__setattr__(self, "registered_ports", tuple(self.registered_ports))
        object.__setattr__(self, "missing_ports", tuple(self.missing_ports))
        if self.workflow_readiness is None:
            object.__setattr__(self, "workflow_readiness", MappingProxyType({}))
        elif not isinstance(self.workflow_readiness, MappingProxyType):
            object.__setattr__(
                self,
                "workflow_readiness",
                MappingProxyType(dict(self.workflow_readiness)),
            )
        if self.metadata is None:
            object.__setattr__(self, "metadata", MappingProxyType({}))
        elif not isinstance(self.metadata, MappingProxyType):
            object.__setattr__(
                self,
                "metadata",
                MappingProxyType(dict(self.metadata)),
            )
