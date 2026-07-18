"""Immutable GeneratedSession — structural session plan from SessionPort."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True)
class GeneratedSession:
    """Deterministic session structure produced by the session port.

    Identifiers and ordering only — no content generation.
    """

    session_id: str
    journey_id: str
    topic_id: str
    sequence_index: int = 0
    effort: str | None = None
    activity_ids: tuple[str, ...] = ()
    metadata: MappingProxyType | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "activity_ids", tuple(self.activity_ids))
        if self.metadata is None:
            object.__setattr__(self, "metadata", MappingProxyType({}))
        elif not isinstance(self.metadata, MappingProxyType):
            object.__setattr__(
                self,
                "metadata",
                MappingProxyType(dict(self.metadata)),
            )
