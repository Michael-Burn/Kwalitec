"""Field provenance contracts for Adaptive Input Assembler (MS-003 A1).

Every AdaptiveInputBundle field exposes source service, source entity,
collection timestamp, and availability. Missing inputs are explicit
``unavailable`` entries with a documented reason — never estimated.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

AVAILABILITY_AVAILABLE = "available"
AVAILABILITY_UNAVAILABLE = "unavailable"

AVAILABILITY_STATUSES = frozenset(
    {AVAILABILITY_AVAILABLE, AVAILABILITY_UNAVAILABLE}
)

# Documented unavailable reasons (explicit contracts — no estimation).
REASON_NO_ACTIVE_PLAN = "NO_ACTIVE_PLAN"
REASON_NOT_FOUND = "NOT_FOUND"
REASON_UNAVAILABLE = "UNAVAILABLE"
REASON_COLLECTOR_ERROR = "COLLECTOR_ERROR"
REASON_INVALID_STUDENT_ID = "INVALID_STUDENT_ID"
REASON_NO_CURRICULUM = "NO_CURRICULUM"

FIELD_EVIDENCE = "evidence"
FIELD_TOPIC_PROGRESS = "topic_progress"
FIELD_STUDY_ATTEMPTS = "study_attempts"
FIELD_MISSION = "mission"
FIELD_READINESS = "readiness"
FIELD_CURRICULUM = "curriculum"
FIELD_STUDENT_GOALS = "student_goals"
FIELD_LIFECYCLE_STAGE = "lifecycle_stage"
# MS-004 T4 — optional Twin enrichment (not a Runtime A collector field).
FIELD_TWIN = "twin"

# Authoritative Runtime A Adaptive inputs (required provenance).
INPUT_FIELD_NAMES = (
    FIELD_EVIDENCE,
    FIELD_TOPIC_PROGRESS,
    FIELD_STUDY_ATTEMPTS,
    FIELD_MISSION,
    FIELD_READINESS,
    FIELD_CURRICULUM,
    FIELD_STUDENT_GOALS,
    FIELD_LIFECYCLE_STAGE,
)

# Optional enrichment fields (present in provenance only when Twin attached).
OPTIONAL_INPUT_FIELD_NAMES = (FIELD_TWIN,)


@dataclass(frozen=True)
class FieldProvenance:
    """Provenance annotation for one AdaptiveInputBundle field."""

    source_service: str
    source_entity: str
    collected_at: str
    availability: str
    unavailable_reason: str = ""

    def __post_init__(self) -> None:
        status = (self.availability or "").strip().lower()
        if status not in AVAILABILITY_STATUSES:
            raise ValueError(
                f"availability must be one of {sorted(AVAILABILITY_STATUSES)}"
            )
        object.__setattr__(self, "availability", status)
        reason = (self.unavailable_reason or "").strip()
        if status == AVAILABILITY_UNAVAILABLE and not reason:
            raise ValueError(
                "unavailable_reason is required when availability is unavailable"
            )
        if status == AVAILABILITY_AVAILABLE:
            reason = ""
        object.__setattr__(self, "unavailable_reason", reason)
        object.__setattr__(
            self, "source_service", (self.source_service or "").strip()
        )
        object.__setattr__(
            self, "source_entity", (self.source_entity or "").strip()
        )
        object.__setattr__(
            self, "collected_at", self.collected_at or ""
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "availability": self.availability,
            "collected_at": self.collected_at,
            "source_entity": self.source_entity,
            "source_service": self.source_service,
            "unavailable_reason": self.unavailable_reason,
        }


def freeze_provenance_map(
    value: Mapping[str, Mapping[str, Any] | FieldProvenance] | None,
) -> Mapping[str, Any]:
    """Freeze a field→provenance mapping for AdaptiveInputBundle."""
    if value is None:
        return MappingProxyType({})
    frozen: dict[str, Any] = {}
    for key in sorted(value.keys(), key=str):
        entry = value[key]
        if isinstance(entry, FieldProvenance):
            frozen[str(key)] = MappingProxyType(entry.to_canonical_dict())
        else:
            frozen[str(key)] = MappingProxyType(dict(entry))
    return MappingProxyType(frozen)


def available_provenance(
    *,
    source_service: str,
    source_entity: str,
    collected_at: str,
) -> FieldProvenance:
    """Build an available provenance annotation."""
    return FieldProvenance(
        source_service=source_service,
        source_entity=source_entity,
        collected_at=collected_at,
        availability=AVAILABILITY_AVAILABLE,
        unavailable_reason="",
    )


def unavailable_provenance(
    *,
    source_service: str,
    source_entity: str,
    collected_at: str,
    reason: str,
) -> FieldProvenance:
    """Build an unavailable provenance annotation with documented reason."""
    return FieldProvenance(
        source_service=source_service,
        source_entity=source_entity,
        collected_at=collected_at,
        availability=AVAILABILITY_UNAVAILABLE,
        unavailable_reason=reason,
    )
