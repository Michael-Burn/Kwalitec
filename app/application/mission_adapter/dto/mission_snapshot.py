"""Immutable structural mission snapshot for adapter routing / comparison.

Never contains generated educational content — only structural identifiers
and scheduling metadata that may be compared across engines.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True)
class MissionSnapshot:
    """Structural view of a mission produced by an engine port.

    Comparison may inspect journey / topic / session / effort / type /
    revision / ordering / explanation *keys*. It must never compare
    generated educational body text.
    """

    mission_id: str
    learner_id: str
    journey_id: str
    topic_id: str
    session_id: str
    effort: str
    mission_type: str
    is_revision: bool
    sequence_index: int
    explanation_keys: tuple[str, ...] = ()
    engine_id: str = ""
    engine_version: str = ""
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
