"""Runtime A evidence bag for Twin Facet Synthesis (MS-004 T1).

Immutable view of authoritative Runtime A fields. Facet builders read from
this bag only — never from other derived facets, Adaptive outputs, or Twin
recursion.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from app.infrastructure.adapters.digital_twin.provenance import RUNTIME_A_FIELD_NAMES


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if value is None:
        return MappingProxyType({})
    if isinstance(value, MappingProxyType):
        return value
    return MappingProxyType(dict(value))


def _freeze_rows(
    value: list[Mapping[str, Any]] | tuple[Mapping[str, Any], ...] | None,
) -> tuple[Mapping[str, Any], ...]:
    if not value:
        return ()
    return tuple(MappingProxyType(dict(row)) for row in value)


@dataclass(frozen=True)
class TwinRuntimeEvidence:
    """Immutable Runtime A evidence consumed by Twin facet builders.

    Availability flags mirror collector results: ``True`` means the collector
    succeeded (payload may be empty for new learners); ``False`` means the
    field is Unavailable and must not be treated as educational content.
    """

    student_id: str = ""
    as_of: str | None = None
    evidence: Mapping[str, Any] = field(default_factory=dict)
    topic_progress: tuple[Mapping[str, Any], ...] = ()
    study_attempts: tuple[Mapping[str, Any], ...] = ()
    mission: Mapping[str, Any] = field(default_factory=dict)
    readiness: Mapping[str, Any] = field(default_factory=dict)
    curriculum: Mapping[str, Any] = field(default_factory=dict)
    student_goals: Mapping[str, Any] = field(default_factory=dict)
    lifecycle_stage: str = ""
    field_available: Mapping[str, bool] = field(default_factory=dict)
    field_reasons: Mapping[str, str] = field(default_factory=dict)
    field_sources: Mapping[str, Mapping[str, str]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(self, "evidence", _freeze_mapping(self.evidence))
        object.__setattr__(
            self, "topic_progress", _freeze_rows(list(self.topic_progress))
        )
        object.__setattr__(
            self, "study_attempts", _freeze_rows(list(self.study_attempts))
        )
        object.__setattr__(self, "mission", _freeze_mapping(self.mission))
        object.__setattr__(self, "readiness", _freeze_mapping(self.readiness))
        object.__setattr__(self, "curriculum", _freeze_mapping(self.curriculum))
        object.__setattr__(
            self, "student_goals", _freeze_mapping(self.student_goals)
        )
        object.__setattr__(
            self, "lifecycle_stage", (self.lifecycle_stage or "").strip()
        )
        object.__setattr__(
            self, "field_available", _freeze_mapping(self.field_available)
        )
        object.__setattr__(
            self, "field_reasons", _freeze_mapping(self.field_reasons)
        )
        sources: dict[str, Any] = {}
        for key, entry in (self.field_sources or {}).items():
            sources[str(key)] = MappingProxyType(dict(entry))
        object.__setattr__(self, "field_sources", MappingProxyType(sources))

    def is_available(self, field_name: str) -> bool:
        """Return True when the named Runtime A field collector succeeded."""
        return bool(self.field_available.get(field_name, False))

    def unavailable_reason(self, field_name: str) -> str:
        """Return the documented unavailable reason for a Runtime A field."""
        return str(self.field_reasons.get(field_name) or "")

    def source_service(self, field_name: str, *, default: str = "") -> str:
        entry = self.field_sources.get(field_name) or {}
        return str(entry.get("source_service") or default)

    def source_entity(self, field_name: str, *, default: str = "") -> str:
        entry = self.field_sources.get(field_name) or {}
        return str(entry.get("source_entity") or default)

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of,
            "curriculum": dict(self.curriculum),
            "evidence": dict(self.evidence),
            "field_available": {
                name: bool(self.field_available.get(name, False))
                for name in RUNTIME_A_FIELD_NAMES
            },
            "field_reasons": {
                name: str(self.field_reasons.get(name) or "")
                for name in RUNTIME_A_FIELD_NAMES
            },
            "field_sources": {
                name: dict(self.field_sources.get(name) or {})
                for name in RUNTIME_A_FIELD_NAMES
            },
            "lifecycle_stage": self.lifecycle_stage,
            "mission": dict(self.mission),
            "readiness": dict(self.readiness),
            "student_goals": dict(self.student_goals),
            "student_id": self.student_id,
            "study_attempts": [dict(row) for row in self.study_attempts],
            "topic_progress": [dict(row) for row in self.topic_progress],
        }
