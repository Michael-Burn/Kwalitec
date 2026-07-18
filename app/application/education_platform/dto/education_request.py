"""Immutable EducationRequest — input to every EducationPlatform workflow."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True)
class EducationRequest:
    """Caller context for an Education Platform workflow invocation.

    Contains stable internal identifiers only. The composition layer never
    performs educational reasoning from these fields — it only routes them
    to registered ports in deterministic workflow order.
    """

    workflow: str
    learner_id: str
    curriculum_id: str | None = None
    subject_id: str | None = None
    topic_id: str | None = None
    journey_id: str | None = None
    session_id: str | None = None
    mission_id: str | None = None
    organisation_id: str | None = None
    correlation_id: str | None = None
    context: MappingProxyType | None = None

    def __post_init__(self) -> None:
        if self.context is None:
            object.__setattr__(self, "context", MappingProxyType({}))
        elif not isinstance(self.context, MappingProxyType):
            object.__setattr__(
                self,
                "context",
                MappingProxyType(dict(self.context)),
            )
