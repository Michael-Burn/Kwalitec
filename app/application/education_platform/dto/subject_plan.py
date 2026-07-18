"""Immutable SubjectPlan — structural subject outline from CurriculumPort."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True)
class SubjectPlan:
    """Deterministic subject outline produced by the curriculum port.

    Contains identifiers and ordering only — no instructional content.
    """

    subject_id: str
    curriculum_id: str
    topic_ids: tuple[str, ...] = ()
    module_ids: tuple[str, ...] = ()
    title: str | None = None
    metadata: MappingProxyType | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "topic_ids", tuple(self.topic_ids))
        object.__setattr__(self, "module_ids", tuple(self.module_ids))
        if self.metadata is None:
            object.__setattr__(self, "metadata", MappingProxyType({}))
        elif not isinstance(self.metadata, MappingProxyType):
            object.__setattr__(
                self,
                "metadata",
                MappingProxyType(dict(self.metadata)),
            )
