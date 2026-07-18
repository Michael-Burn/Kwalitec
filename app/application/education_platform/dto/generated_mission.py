"""Immutable GeneratedMission — structural mission from MissionPort."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True)
class GeneratedMission:
    """Deterministic mission structure produced by the mission port.

    Identifiers and scheduling fields only — no educational reasoning.
    """

    mission_id: str
    learner_id: str
    journey_id: str
    topic_id: str
    session_id: str
    mission_type: str = "today"
    effort: str | None = None
    sequence_index: int = 0
    is_revision: bool = False
    metadata: MappingProxyType | None = None

    def __post_init__(self) -> None:
        if self.metadata is None:
            object.__setattr__(self, "metadata", MappingProxyType({}))
        elif not isinstance(self.metadata, MappingProxyType):
            object.__setattr__(
                self,
                "metadata",
                MappingProxyType(dict(self.metadata)),
            )
