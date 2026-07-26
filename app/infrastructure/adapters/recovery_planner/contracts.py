"""Study Recovery Planner contracts (P2-MS010).

Immutable DTOs and the public ``RecoveryPlannerPort``. This milestone
establishes Recovery Planning as an advisory architectural capability only.

Recovery answers: **"What disruption facts are known, and what structural
recovery options exist as advisory placeholders?"**
Runtime A answers: **"What should the student do next?"**

No recovery algorithms, schedule optimisation, recommendation changes, or
educational authority transfer. All candidates are ``advisory_only=True``.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import date, datetime
from types import MappingProxyType
from typing import Any, Protocol, runtime_checkable

UNAVAILABLE = "UNAVAILABLE"
NOT_FOUND = "NOT_FOUND"
FORBIDDEN = "FORBIDDEN"
INVALID_STATE = "INVALID_STATE"

RECOVERY_ERROR_CODES = frozenset(
    {UNAVAILABLE, NOT_FOUND, FORBIDDEN, INVALID_STATE}
)

AUTHORITY_RECOVERY_PLANNER = "recovery_planner"
AUTHORITY_RUNTIME_A = "runtime_a"

AVAILABILITY_AVAILABLE = "available"
AVAILABILITY_UNAVAILABLE = "unavailable"
AVAILABILITY_VALUES = frozenset(
    {AVAILABILITY_AVAILABLE, AVAILABILITY_UNAVAILABLE, ""}
)

RECOVERY_VERSION = "p2.ms010.1"

# Structural placeholder only — no optimisation / schedule algorithms.
STRATEGY_STRUCTURAL_PLACEHOLDER = "structural_placeholder"

STRATEGY_TYPES = frozenset(
    {
        STRATEGY_STRUCTURAL_PLACEHOLDER,
        "",
    }
)


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if value is None:
        return MappingProxyType({})
    if isinstance(value, MappingProxyType):
        return value
    return MappingProxyType(dict(value))


def _freeze_str_tuple(value: list[str] | tuple[str, ...] | None) -> tuple[str, ...]:
    if not value:
        return ()
    return tuple(str(item) for item in value)


def _canonical(value: Any) -> Any:
    """Recursively convert values into JSON-stable plain data."""
    if value is None or isinstance(value, bool | int | float | str):
        return value
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {
            str(k): _canonical(v)
            for k, v in sorted(value.items(), key=lambda i: str(i[0]))
        }
    if isinstance(value, list | tuple):
        return [_canonical(item) for item in value]
    if hasattr(value, "to_canonical_dict"):
        return value.to_canonical_dict()
    raise TypeError(f"Unsupported recovery contract value type: {type(value)!r}")


def serialize_canonical(value: Any) -> str:
    """Deterministic JSON serialization (sorted keys, compact separators)."""
    return json.dumps(_canonical(value), sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class MissedSessionFact:
    """One factual missed planned session (traceable; no recommendations)."""

    session_ref: str = ""
    planned_at: str | None = None
    status: str = "missed"
    source_description: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "session_ref", (self.session_ref or "").strip())
        if not self.session_ref:
            raise ValueError("session_ref is required")
        if self.planned_at is not None and not isinstance(self.planned_at, str):
            raise TypeError("planned_at must be an ISO string or None")
        status = (self.status or "missed").strip() or "missed"
        object.__setattr__(self, "status", status)
        object.__setattr__(
            self, "source_description", (self.source_description or "").strip()
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "planned_at": self.planned_at,
            "session_ref": self.session_ref,
            "source_description": self.source_description,
            "status": self.status,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class StudyCapacityFact:
    """Factual available study capacity (minutes / slots). No optimisation."""

    available_minutes: int = 0
    available_slots: int = 0
    source_description: str = ""

    def __post_init__(self) -> None:
        for label, value in (
            ("available_minutes", self.available_minutes),
            ("available_slots", self.available_slots),
        ):
            if not isinstance(value, int):
                raise TypeError(f"{label} must be an int")
            if value < 0:
                raise ValueError(f"{label} must be >= 0")
        object.__setattr__(
            self, "source_description", (self.source_description or "").strip()
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "available_minutes": self.available_minutes,
            "available_slots": self.available_slots,
            "source_description": self.source_description,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class DisruptionSummary:
    """Factual disruption summary derived from recorded miss / gap signals."""

    summary: str = ""
    disruption_kind: str = ""
    missed_count: int = 0
    source_description: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "summary", (self.summary or "").strip())
        object.__setattr__(
            self, "disruption_kind", (self.disruption_kind or "").strip()
        )
        if not isinstance(self.missed_count, int):
            raise TypeError("missed_count must be an int")
        if self.missed_count < 0:
            raise ValueError("missed_count must be >= 0")
        object.__setattr__(
            self, "source_description", (self.source_description or "").strip()
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "disruption_kind": self.disruption_kind,
            "missed_count": self.missed_count,
            "source_description": self.source_description,
            "summary": self.summary,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class RecoveryContext:
    """Immutable factual context for recovery planning (P2-MS010).

    Every field must be factual and traceable. Contains no recovery
    recommendations and no optimisation outputs.
    """

    recovery_id: str = ""
    reporting_period: str = "this_week"
    disruption_summary: DisruptionSummary = field(
        default_factory=DisruptionSummary
    )
    missed_sessions: tuple[MissedSessionFact, ...] = ()
    available_study_capacity: StudyCapacityFact = field(
        default_factory=StudyCapacityFact
    )
    current_plan_version: str = ""
    evidence_provenance: Mapping[str, Any] = field(default_factory=dict)
    generated_at: str | None = None
    student_id: str = ""
    authority: str = AUTHORITY_RECOVERY_PLANNER
    availability: str = AVAILABILITY_AVAILABLE
    unavailable_reason: str = ""
    recovery_version: str = RECOVERY_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "recovery_id", (self.recovery_id or "").strip())
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(
            self,
            "reporting_period",
            (self.reporting_period or "this_week").strip().lower() or "this_week",
        )
        if not isinstance(self.disruption_summary, DisruptionSummary):
            raise TypeError("disruption_summary must be a DisruptionSummary")
        object.__setattr__(
            self, "missed_sessions", tuple(self.missed_sessions or ())
        )
        for session in self.missed_sessions:
            if not isinstance(session, MissedSessionFact):
                raise TypeError(
                    "missed_sessions must contain MissedSessionFact values"
                )
        if not isinstance(self.available_study_capacity, StudyCapacityFact):
            raise TypeError(
                "available_study_capacity must be a StudyCapacityFact"
            )
        object.__setattr__(
            self, "current_plan_version", (self.current_plan_version or "").strip()
        )
        object.__setattr__(
            self, "evidence_provenance", _freeze_mapping(self.evidence_provenance)
        )
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError("generated_at must be an ISO string or None")
        availability = (self.availability or "").strip().lower()
        if availability not in AVAILABILITY_VALUES:
            raise ValueError(
                "availability must be 'available', 'unavailable', or empty"
            )
        object.__setattr__(self, "availability", availability)
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_RECOVERY_PLANNER).strip(),
        )
        object.__setattr__(
            self, "unavailable_reason", (self.unavailable_reason or "").strip()
        )
        object.__setattr__(
            self,
            "recovery_version",
            (self.recovery_version or RECOVERY_VERSION).strip(),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "authority": self.authority,
            "availability": self.availability,
            "available_study_capacity": (
                self.available_study_capacity.to_canonical_dict()
            ),
            "current_plan_version": self.current_plan_version,
            "disruption_summary": self.disruption_summary.to_canonical_dict(),
            "evidence_provenance": dict(self.evidence_provenance),
            "generated_at": self.generated_at,
            "missed_sessions": [
                item.to_canonical_dict() for item in self.missed_sessions
            ],
            "recovery_id": self.recovery_id,
            "recovery_version": self.recovery_version,
            "reporting_period": self.reporting_period,
            "student_id": self.student_id,
            "unavailable_reason": self.unavailable_reason,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class RecoveryPlanCandidate:
    """Immutable structural recovery option placeholder (P2-MS010).

    Advisory only — must not influence Runtime A decisions in this milestone.
    ``advisory_only`` is always ``True``.
    """

    candidate_id: str = ""
    strategy_type: str = STRATEGY_STRUCTURAL_PLACEHOLDER
    affected_period: str = ""
    rationale: str = ""
    provenance: Mapping[str, Any] = field(default_factory=dict)
    advisory_only: bool = True
    recovery_id: str = ""
    student_id: str = ""
    generated_at: str | None = None
    authority: str = AUTHORITY_RECOVERY_PLANNER
    availability: str = AVAILABILITY_AVAILABLE
    unavailable_reason: str = ""
    recovery_version: str = RECOVERY_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "candidate_id", (self.candidate_id or "").strip())
        object.__setattr__(self, "recovery_id", (self.recovery_id or "").strip())
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        strategy = (self.strategy_type or STRATEGY_STRUCTURAL_PLACEHOLDER).strip()
        if strategy not in STRATEGY_TYPES:
            raise ValueError(
                "strategy_type must be a known structural type or empty "
                f"(got {strategy!r})"
            )
        object.__setattr__(
            self,
            "strategy_type",
            strategy or STRATEGY_STRUCTURAL_PLACEHOLDER,
        )
        object.__setattr__(
            self, "affected_period", (self.affected_period or "").strip()
        )
        object.__setattr__(self, "rationale", (self.rationale or "").strip())
        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))
        # Binding invariant for this milestone — candidates never drive decisions.
        object.__setattr__(self, "advisory_only", True)
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError("generated_at must be an ISO string or None")
        availability = (self.availability or "").strip().lower()
        if availability not in AVAILABILITY_VALUES:
            raise ValueError(
                "availability must be 'available', 'unavailable', or empty"
            )
        object.__setattr__(self, "availability", availability)
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_RECOVERY_PLANNER).strip(),
        )
        object.__setattr__(
            self, "unavailable_reason", (self.unavailable_reason or "").strip()
        )
        object.__setattr__(
            self,
            "recovery_version",
            (self.recovery_version or RECOVERY_VERSION).strip(),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "advisory_only": self.advisory_only,
            "affected_period": self.affected_period,
            "authority": self.authority,
            "availability": self.availability,
            "candidate_id": self.candidate_id,
            "generated_at": self.generated_at,
            "provenance": dict(self.provenance),
            "rationale": self.rationale,
            "recovery_id": self.recovery_id,
            "recovery_version": self.recovery_version,
            "strategy_type": self.strategy_type,
            "student_id": self.student_id,
            "unavailable_reason": self.unavailable_reason,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class RecoveryResult:
    """Result envelope for Recovery Planner Adapter calls."""

    ok: bool
    value: RecoveryPlanCandidate | None = None
    error_code: str | None = None
    message: str | None = None
    fallback_used: bool = False

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "error_code": self.error_code,
            "fallback_used": self.fallback_used,
            "message": self.message,
            "ok": self.ok,
            "value": None if self.value is None else self.value.to_canonical_dict(),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@runtime_checkable
class RecoveryPlannerPort(Protocol):
    """Public Recovery Planning surface for Runtime A (P2-MS010).

    Accepts ``RecoveryContext`` and returns an immutable
    ``RecoveryPlanCandidate``. Structural placeholder only in this milestone —
    must not influence Runtime A educational decisions.
    Must not write Runtime A, Twin, Adaptive, Strategy, or Experience state.
    Must not run recovery algorithms, schedule optimisation, or scoring.
    """

    @property
    def port_id(self) -> str:
        """Stable RecoveryPlannerPort identity."""

    def is_available(self) -> bool:
        """Whether the recovery planner port is enabled and wired."""

    def plan_recovery(self, context: RecoveryContext) -> RecoveryResult:
        """Return a RecoveryPlanCandidate for the context (or error envelope)."""
