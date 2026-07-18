"""Immutable ComparisonResult — structural dual-engine comparison."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True)
class DimensionMatch:
    """Outcome for a single structural comparison dimension."""

    name: str
    matched: bool
    v1_value: str
    v2_value: str


@dataclass(frozen=True)
class ComparisonResult:
    """Result of comparing V1 and V2 structural mission snapshots.

    Never stores generated educational content. Dimensions are structural
    only (journey, topic, session, effort, type, revision, ordering,
    explanation metadata keys).
    """

    comparison_id: str
    matched: bool
    dimensions: tuple[DimensionMatch, ...]
    v1_mission_id: str | None
    v2_mission_id: str | None
    divergence_count: int
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
