"""Advisory Decision Simulation contracts (P2-MS011).

Immutable DTOs for a parallel simulation path that evaluates how Runtime A
recommendations would differ if advisory inputs were considered.

Simulation answers: **"What would change if advisory inputs influenced
ranking?"**
Runtime A answers: **"What should the student do next?"** (unchanged)

All simulated outputs are ``simulation_only=True``. Simulation must never
modify production recommendations returned to the student.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date, datetime
from types import MappingProxyType
from typing import Any

UNAVAILABLE = "UNAVAILABLE"
INVALID_STATE = "INVALID_STATE"

SIMULATION_ERROR_CODES = frozenset({UNAVAILABLE, INVALID_STATE})

AUTHORITY_DECISION_SIMULATION = "decision_simulation"
AUTHORITY_RUNTIME_A = "runtime_a"

SIMULATION_VERSION = "p2.ms011.1"


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if value is None:
        return MappingProxyType({})
    if isinstance(value, MappingProxyType):
        return value
    frozen: dict[str, Any] = {}
    for key, item in dict(value).items():
        if isinstance(item, Mapping):
            frozen[str(key)] = dict(item)
        elif isinstance(item, list | tuple):
            frozen[str(key)] = list(item)
        else:
            frozen[str(key)] = item
    return MappingProxyType(frozen)


def _freeze_mapping_tuple(
    value: Sequence[Mapping[str, Any]] | None,
) -> tuple[Mapping[str, Any], ...]:
    if not value:
        return ()
    return tuple(_freeze_mapping(item) for item in value)


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
    raise TypeError(
        f"Unsupported decision simulation contract value type: {type(value)!r}"
    )


def serialize_canonical(value: Any) -> str:
    """Deterministic JSON serialization (sorted keys, compact separators)."""
    return json.dumps(_canonical(value), sort_keys=True, separators=(",", ":"))


def snapshot_mapping(value: Any | None) -> Mapping[str, Any] | None:
    """Freeze an advisory DTO or mapping into a canonical snapshot."""
    if value is None:
        return None
    if hasattr(value, "to_canonical_dict"):
        return _freeze_mapping(value.to_canonical_dict())
    if isinstance(value, Mapping):
        return _freeze_mapping(value)
    raise TypeError("value must be a Mapping, DTO with to_canonical_dict, or None")


def snapshot_mapping_tuple(
    value: Sequence[Any] | None,
) -> tuple[Mapping[str, Any], ...]:
    """Freeze a sequence of advisory DTOs / mappings."""
    if not value:
        return ()
    out: list[Mapping[str, Any]] = []
    for item in value:
        snap = snapshot_mapping(item)
        if snap is None:
            continue
        out.append(snap)
    return tuple(out)


@dataclass(frozen=True)
class DecisionSimulationContext:
    """Immutable inputs for advisory decision simulation (P2-MS011).

    Carries production Runtime A inputs plus optional advisory snapshots.
    Does not authorise recommendation changes.
    """

    simulation_id: str = ""
    recommendation_id: str = ""
    evidence_advisory: Mapping[str, Any] | None = None
    recovery_candidates: tuple[Mapping[str, Any], ...] = ()
    runtime_inputs: Mapping[str, Any] = field(default_factory=dict)
    generated_at: str | None = None
    student_id: str = ""
    authority: str = AUTHORITY_DECISION_SIMULATION
    simulation_version: str = SIMULATION_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "simulation_id", (self.simulation_id or "").strip()
        )
        object.__setattr__(
            self, "recommendation_id", (self.recommendation_id or "").strip()
        )
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        if self.evidence_advisory is not None:
            object.__setattr__(
                self, "evidence_advisory", snapshot_mapping(self.evidence_advisory)
            )
        object.__setattr__(
            self,
            "recovery_candidates",
            snapshot_mapping_tuple(self.recovery_candidates),
        )
        object.__setattr__(
            self, "runtime_inputs", _freeze_mapping(self.runtime_inputs)
        )
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError("generated_at must be an ISO string or None")
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_DECISION_SIMULATION).strip(),
        )
        object.__setattr__(
            self,
            "simulation_version",
            (self.simulation_version or SIMULATION_VERSION).strip(),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "authority": self.authority,
            "evidence_advisory": (
                None
                if self.evidence_advisory is None
                else dict(self.evidence_advisory)
            ),
            "generated_at": self.generated_at,
            "recommendation_id": self.recommendation_id,
            "recovery_candidates": [
                dict(item) for item in self.recovery_candidates
            ],
            "runtime_inputs": dict(self.runtime_inputs),
            "simulation_id": self.simulation_id,
            "simulation_version": self.simulation_version,
            "student_id": self.student_id,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class SimulatedRecommendation:
    """Immutable simulated recommendation output (P2-MS011).

    Always ``simulation_only=True``. Must never be served to students as a
    production recommendation.
    """

    simulation_id: str = ""
    simulated_priority: str = ""
    simulated_rationale: str = ""
    advisory_sources: tuple[str, ...] = ()
    differs_from_runtime: bool = False
    provenance: Mapping[str, Any] = field(default_factory=dict)
    simulation_only: bool = True
    recommendation_id: str = ""
    simulated_title: str = ""
    simulated_category: str = ""
    student_id: str = ""
    generated_at: str | None = None
    authority: str = AUTHORITY_DECISION_SIMULATION
    simulation_version: str = SIMULATION_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "simulation_id", (self.simulation_id or "").strip()
        )
        object.__setattr__(
            self, "recommendation_id", (self.recommendation_id or "").strip()
        )
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(
            self, "simulated_priority", (self.simulated_priority or "").strip()
        )
        object.__setattr__(
            self, "simulated_rationale", (self.simulated_rationale or "").strip()
        )
        object.__setattr__(
            self, "simulated_title", (self.simulated_title or "").strip()
        )
        object.__setattr__(
            self, "simulated_category", (self.simulated_category or "").strip()
        )
        object.__setattr__(
            self,
            "advisory_sources",
            tuple(str(item) for item in (self.advisory_sources or ())),
        )
        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))
        # Binding invariant — simulated outputs never become production.
        object.__setattr__(self, "simulation_only", True)
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError("generated_at must be an ISO string or None")
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_DECISION_SIMULATION).strip(),
        )
        object.__setattr__(
            self,
            "simulation_version",
            (self.simulation_version or SIMULATION_VERSION).strip(),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "advisory_sources": list(self.advisory_sources),
            "authority": self.authority,
            "differs_from_runtime": self.differs_from_runtime,
            "generated_at": self.generated_at,
            "provenance": dict(self.provenance),
            "recommendation_id": self.recommendation_id,
            "simulated_category": self.simulated_category,
            "simulated_priority": self.simulated_priority,
            "simulated_rationale": self.simulated_rationale,
            "simulated_title": self.simulated_title,
            "simulation_id": self.simulation_id,
            "simulation_only": self.simulation_only,
            "simulation_version": self.simulation_version,
            "student_id": self.student_id,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class DecisionDifference:
    """One explainable field-level difference between production and simulated."""

    field_name: str = ""
    production_value: str = ""
    simulated_value: str = ""
    explanation: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "field_name", (self.field_name or "").strip())
        if not self.field_name:
            raise ValueError("field_name is required")
        object.__setattr__(
            self, "production_value", str(self.production_value or "")
        )
        object.__setattr__(
            self, "simulated_value", str(self.simulated_value or "")
        )
        object.__setattr__(self, "explanation", (self.explanation or "").strip())

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "explanation": self.explanation,
            "field_name": self.field_name,
            "production_value": self.production_value,
            "simulated_value": self.simulated_value,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class DecisionComparisonRecord:
    """Immutable operational comparison artefact (P2-MS011).

    Documents production vs simulated recommendation for validation and
    explainability. Never served to students. Never mutates Runtime A.
    """

    comparison_id: str = ""
    simulation_id: str = ""
    recommendation_id: str = ""
    production_recommendation: Mapping[str, Any] = field(default_factory=dict)
    simulated_recommendation: SimulatedRecommendation | None = None
    differences: tuple[DecisionDifference, ...] = ()
    advisory_sources_considered: tuple[str, ...] = ()
    provenance: Mapping[str, Any] = field(default_factory=dict)
    generated_at: str | None = None
    student_id: str = ""
    operational_only: bool = True
    authority: str = AUTHORITY_DECISION_SIMULATION
    simulation_version: str = SIMULATION_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "comparison_id", (self.comparison_id or "").strip()
        )
        object.__setattr__(
            self, "simulation_id", (self.simulation_id or "").strip()
        )
        object.__setattr__(
            self, "recommendation_id", (self.recommendation_id or "").strip()
        )
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(
            self,
            "production_recommendation",
            _freeze_mapping(self.production_recommendation),
        )
        if self.simulated_recommendation is not None and not isinstance(
            self.simulated_recommendation, SimulatedRecommendation
        ):
            raise TypeError(
                "simulated_recommendation must be SimulatedRecommendation or None"
            )
        object.__setattr__(self, "differences", tuple(self.differences or ()))
        for diff in self.differences:
            if not isinstance(diff, DecisionDifference):
                raise TypeError("differences must contain DecisionDifference values")
        object.__setattr__(
            self,
            "advisory_sources_considered",
            tuple(str(item) for item in (self.advisory_sources_considered or ())),
        )
        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))
        object.__setattr__(self, "operational_only", True)
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError("generated_at must be an ISO string or None")
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_DECISION_SIMULATION).strip(),
        )
        object.__setattr__(
            self,
            "simulation_version",
            (self.simulation_version or SIMULATION_VERSION).strip(),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "advisory_sources_considered": list(self.advisory_sources_considered),
            "authority": self.authority,
            "comparison_id": self.comparison_id,
            "differences": [item.to_canonical_dict() for item in self.differences],
            "generated_at": self.generated_at,
            "operational_only": self.operational_only,
            "production_recommendation": dict(self.production_recommendation),
            "provenance": dict(self.provenance),
            "recommendation_id": self.recommendation_id,
            "simulated_recommendation": (
                None
                if self.simulated_recommendation is None
                else self.simulated_recommendation.to_canonical_dict()
            ),
            "simulation_id": self.simulation_id,
            "simulation_version": self.simulation_version,
            "student_id": self.student_id,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class DecisionSimulationResult:
    """Result envelope for DecisionSimulationService calls."""

    ok: bool
    simulated: SimulatedRecommendation | None = None
    comparison: DecisionComparisonRecord | None = None
    error_code: str | None = None
    message: str | None = None

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "comparison": (
                None
                if self.comparison is None
                else self.comparison.to_canonical_dict()
            ),
            "error_code": self.error_code,
            "message": self.message,
            "ok": self.ok,
            "simulated": (
                None if self.simulated is None else self.simulated.to_canonical_dict()
            ),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())
