"""Advisory Evaluation Framework contracts (P2-MS012).

Immutable DTOs for scoring and analysing simulated recommendation differences
without modifying Runtime A behaviour.

Evaluation answers: **"Do advisory-informed simulations appear beneficial
enough to warrant further review?"**
Runtime A answers: **"What should the student do next?"** (unchanged)

All evaluation artefacts are operational / review-only. No student identifiers.
No ranking decisions. No student-facing use.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import date, datetime
from types import MappingProxyType
from typing import Any

UNAVAILABLE = "UNAVAILABLE"
INVALID_STATE = "INVALID_STATE"

EVALUATION_ERROR_CODES = frozenset({UNAVAILABLE, INVALID_STATE})

AUTHORITY_ADVISORY_EVALUATION = "advisory_evaluation"
AUTHORITY_DECISION_SIMULATION = "decision_simulation"
AUTHORITY_RUNTIME_A = "runtime_a"

EVALUATION_VERSION = "p2.ms012.1"

# Difference taxonomy — operational classification only (no ranking).
DIFFERENCE_UNCHANGED = "unchanged"
DIFFERENCE_RATIONALE_ANNOTATION = "rationale_annotation"
DIFFERENCE_PRIORITY = "priority"
DIFFERENCE_TITLE = "title"
DIFFERENCE_CATEGORY = "category"
DIFFERENCE_MULTI_FIELD = "multi_field"
DIFFERENCE_STRUCTURAL = "structural"
DIFFERENCE_UNKNOWN = "unknown"

DIFFERENCE_TYPES = frozenset(
    {
        DIFFERENCE_UNCHANGED,
        DIFFERENCE_RATIONALE_ANNOTATION,
        DIFFERENCE_PRIORITY,
        DIFFERENCE_TITLE,
        DIFFERENCE_CATEGORY,
        DIFFERENCE_MULTI_FIELD,
        DIFFERENCE_STRUCTURAL,
        DIFFERENCE_UNKNOWN,
    }
)


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
        f"Unsupported advisory evaluation contract value type: {type(value)!r}"
    )


def serialize_canonical(value: Any) -> str:
    """Deterministic JSON serialization (sorted keys, compact separators)."""
    return json.dumps(_canonical(value), sort_keys=True, separators=(",", ":"))


def snapshot_mapping(value: Any | None) -> Mapping[str, Any] | None:
    """Freeze a DTO or mapping into a canonical snapshot."""
    if value is None:
        return None
    if hasattr(value, "to_canonical_dict"):
        return _freeze_mapping(value.to_canonical_dict())
    if isinstance(value, Mapping):
        return _freeze_mapping(value)
    raise TypeError("value must be a Mapping, DTO with to_canonical_dict, or None")


@dataclass(frozen=True)
class RecommendationComparison:
    """Immutable production-vs-simulated comparison (P2-MS012).

    Operational evaluation artefact only. No ranking decisions. No student
    identifiers.
    """

    comparison_id: str = ""
    production_recommendation: Mapping[str, Any] = field(default_factory=dict)
    simulated_recommendation: Mapping[str, Any] = field(default_factory=dict)
    differs: bool = False
    difference_type: str = DIFFERENCE_UNCHANGED
    advisory_sources: tuple[str, ...] = ()
    generated_at: str | None = None
    simulation_id: str = ""
    recommendation_id: str = ""
    provenance: Mapping[str, Any] = field(default_factory=dict)
    operational_only: bool = True
    authority: str = AUTHORITY_ADVISORY_EVALUATION
    evaluation_version: str = EVALUATION_VERSION

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
        object.__setattr__(
            self,
            "production_recommendation",
            _freeze_mapping(self.production_recommendation),
        )
        object.__setattr__(
            self,
            "simulated_recommendation",
            _freeze_mapping(self.simulated_recommendation),
        )
        object.__setattr__(
            self,
            "advisory_sources",
            tuple(str(item) for item in (self.advisory_sources or ())),
        )
        diff_type = (self.difference_type or DIFFERENCE_UNCHANGED).strip()
        if diff_type not in DIFFERENCE_TYPES:
            diff_type = DIFFERENCE_UNKNOWN
        object.__setattr__(self, "difference_type", diff_type)
        # Binding: differs must align with difference_type taxonomy.
        if not self.differs:
            object.__setattr__(self, "difference_type", DIFFERENCE_UNCHANGED)
        elif self.difference_type == DIFFERENCE_UNCHANGED:
            object.__setattr__(self, "difference_type", DIFFERENCE_STRUCTURAL)
        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))
        object.__setattr__(self, "operational_only", True)
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError("generated_at must be an ISO string or None")
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_ADVISORY_EVALUATION).strip(),
        )
        object.__setattr__(
            self,
            "evaluation_version",
            (self.evaluation_version or EVALUATION_VERSION).strip(),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "advisory_sources": list(self.advisory_sources),
            "authority": self.authority,
            "comparison_id": self.comparison_id,
            "difference_type": self.difference_type,
            "differs": self.differs,
            "evaluation_version": self.evaluation_version,
            "generated_at": self.generated_at,
            "operational_only": self.operational_only,
            "production_recommendation": dict(self.production_recommendation),
            "provenance": dict(self.provenance),
            "recommendation_id": self.recommendation_id,
            "simulated_recommendation": dict(self.simulated_recommendation),
            "simulation_id": self.simulation_id,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class EvaluationMetrics:
    """Immutable operational evaluation metrics (P2-MS012).

    Rates are floats in ``[0.0, 1.0]``. Empty cohorts yield ``0.0`` rates.
    """

    comparison_count: int = 0
    difference_rate: float = 0.0
    unchanged_rate: float = 0.0
    advisory_usage_frequency: float = 0.0
    explainability_completeness: float = 0.0
    difference_type_counts: Mapping[str, int] = field(default_factory=dict)
    advisory_source_counts: Mapping[str, int] = field(default_factory=dict)
    generated_at: str | None = None
    operational_only: bool = True
    authority: str = AUTHORITY_ADVISORY_EVALUATION
    evaluation_version: str = EVALUATION_VERSION

    def __post_init__(self) -> None:
        count = max(0, int(self.comparison_count or 0))
        object.__setattr__(self, "comparison_count", count)

        def _clamp_rate(value: float) -> float:
            try:
                number = float(value)
            except (TypeError, ValueError):
                return 0.0
            if number < 0.0:
                return 0.0
            if number > 1.0:
                return 1.0
            return number

        object.__setattr__(self, "difference_rate", _clamp_rate(self.difference_rate))
        object.__setattr__(self, "unchanged_rate", _clamp_rate(self.unchanged_rate))
        object.__setattr__(
            self,
            "advisory_usage_frequency",
            _clamp_rate(self.advisory_usage_frequency),
        )
        object.__setattr__(
            self,
            "explainability_completeness",
            _clamp_rate(self.explainability_completeness),
        )
        object.__setattr__(
            self,
            "difference_type_counts",
            _freeze_mapping(
                {
                    str(k): int(v)
                    for k, v in dict(self.difference_type_counts or {}).items()
                }
            ),
        )
        object.__setattr__(
            self,
            "advisory_source_counts",
            _freeze_mapping(
                {
                    str(k): int(v)
                    for k, v in dict(self.advisory_source_counts or {}).items()
                }
            ),
        )
        object.__setattr__(self, "operational_only", True)
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError("generated_at must be an ISO string or None")
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_ADVISORY_EVALUATION).strip(),
        )
        object.__setattr__(
            self,
            "evaluation_version",
            (self.evaluation_version or EVALUATION_VERSION).strip(),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "advisory_source_counts": dict(self.advisory_source_counts),
            "advisory_usage_frequency": self.advisory_usage_frequency,
            "authority": self.authority,
            "comparison_count": self.comparison_count,
            "difference_rate": self.difference_rate,
            "difference_type_counts": dict(self.difference_type_counts),
            "evaluation_version": self.evaluation_version,
            "explainability_completeness": self.explainability_completeness,
            "generated_at": self.generated_at,
            "operational_only": self.operational_only,
            "unchanged_rate": self.unchanged_rate,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class DomainReviewExport:
    """Immutable actuarial / educational review export (P2-MS012).

    Contains production vs simulated rationale, provenance, and explanation.
    Never student-facing.
    """

    export_id: str = ""
    comparison_id: str = ""
    production_rationale: str = ""
    simulated_rationale: str = ""
    provenance: Mapping[str, Any] = field(default_factory=dict)
    explanation: str = ""
    difference_type: str = DIFFERENCE_UNCHANGED
    differs: bool = False
    advisory_sources: tuple[str, ...] = ()
    production_recommendation: Mapping[str, Any] = field(default_factory=dict)
    simulated_recommendation: Mapping[str, Any] = field(default_factory=dict)
    generated_at: str | None = None
    review_only: bool = True
    student_facing: bool = False
    authority: str = AUTHORITY_ADVISORY_EVALUATION
    evaluation_version: str = EVALUATION_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "export_id", (self.export_id or "").strip())
        object.__setattr__(
            self, "comparison_id", (self.comparison_id or "").strip()
        )
        object.__setattr__(
            self, "production_rationale", str(self.production_rationale or "")
        )
        object.__setattr__(
            self, "simulated_rationale", str(self.simulated_rationale or "")
        )
        object.__setattr__(self, "explanation", (self.explanation or "").strip())
        object.__setattr__(
            self,
            "advisory_sources",
            tuple(str(item) for item in (self.advisory_sources or ())),
        )
        diff_type = (self.difference_type or DIFFERENCE_UNCHANGED).strip()
        if diff_type not in DIFFERENCE_TYPES:
            diff_type = DIFFERENCE_UNKNOWN
        object.__setattr__(self, "difference_type", diff_type)
        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))
        object.__setattr__(
            self,
            "production_recommendation",
            _freeze_mapping(self.production_recommendation),
        )
        object.__setattr__(
            self,
            "simulated_recommendation",
            _freeze_mapping(self.simulated_recommendation),
        )
        # Binding invariants — review artefacts never become student-facing.
        object.__setattr__(self, "review_only", True)
        object.__setattr__(self, "student_facing", False)
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError("generated_at must be an ISO string or None")
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_ADVISORY_EVALUATION).strip(),
        )
        object.__setattr__(
            self,
            "evaluation_version",
            (self.evaluation_version or EVALUATION_VERSION).strip(),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "advisory_sources": list(self.advisory_sources),
            "authority": self.authority,
            "comparison_id": self.comparison_id,
            "difference_type": self.difference_type,
            "differs": self.differs,
            "evaluation_version": self.evaluation_version,
            "explanation": self.explanation,
            "export_id": self.export_id,
            "generated_at": self.generated_at,
            "production_rationale": self.production_rationale,
            "production_recommendation": dict(self.production_recommendation),
            "provenance": dict(self.provenance),
            "review_only": self.review_only,
            "simulated_rationale": self.simulated_rationale,
            "simulated_recommendation": dict(self.simulated_recommendation),
            "student_facing": self.student_facing,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class EvaluationSummary:
    """Immutable evaluation summary for ops / architecture review (P2-MS012)."""

    summary_id: str = ""
    metrics: EvaluationMetrics | None = None
    comparisons: tuple[RecommendationComparison, ...] = ()
    exports: tuple[DomainReviewExport, ...] = ()
    notes: tuple[str, ...] = ()
    generated_at: str | None = None
    operational_only: bool = True
    authority: str = AUTHORITY_ADVISORY_EVALUATION
    evaluation_version: str = EVALUATION_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "summary_id", (self.summary_id or "").strip())
        if self.metrics is not None and not isinstance(self.metrics, EvaluationMetrics):
            raise TypeError("metrics must be EvaluationMetrics or None")
        object.__setattr__(self, "comparisons", tuple(self.comparisons or ()))
        for item in self.comparisons:
            if not isinstance(item, RecommendationComparison):
                raise TypeError(
                    "comparisons must contain RecommendationComparison values"
                )
        object.__setattr__(self, "exports", tuple(self.exports or ()))
        for item in self.exports:
            if not isinstance(item, DomainReviewExport):
                raise TypeError("exports must contain DomainReviewExport values")
        object.__setattr__(
            self, "notes", tuple(str(item) for item in (self.notes or ()))
        )
        object.__setattr__(self, "operational_only", True)
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError("generated_at must be an ISO string or None")
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_ADVISORY_EVALUATION).strip(),
        )
        object.__setattr__(
            self,
            "evaluation_version",
            (self.evaluation_version or EVALUATION_VERSION).strip(),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "authority": self.authority,
            "comparisons": [item.to_canonical_dict() for item in self.comparisons],
            "evaluation_version": self.evaluation_version,
            "exports": [item.to_canonical_dict() for item in self.exports],
            "generated_at": self.generated_at,
            "metrics": (
                None if self.metrics is None else self.metrics.to_canonical_dict()
            ),
            "notes": list(self.notes),
            "operational_only": self.operational_only,
            "summary_id": self.summary_id,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class AdvisoryEvaluationResult:
    """Result envelope for AdvisoryEvaluationService calls."""

    ok: bool
    comparison: RecommendationComparison | None = None
    metrics: EvaluationMetrics | None = None
    summary: EvaluationSummary | None = None
    export: DomainReviewExport | None = None
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
            "export": (
                None if self.export is None else self.export.to_canonical_dict()
            ),
            "message": self.message,
            "metrics": (
                None if self.metrics is None else self.metrics.to_canonical_dict()
            ),
            "ok": self.ok,
            "summary": (
                None if self.summary is None else self.summary.to_canonical_dict()
            ),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


__all__ = [
    "AUTHORITY_ADVISORY_EVALUATION",
    "AUTHORITY_DECISION_SIMULATION",
    "AUTHORITY_RUNTIME_A",
    "DIFFERENCE_CATEGORY",
    "DIFFERENCE_MULTI_FIELD",
    "DIFFERENCE_PRIORITY",
    "DIFFERENCE_RATIONALE_ANNOTATION",
    "DIFFERENCE_STRUCTURAL",
    "DIFFERENCE_TITLE",
    "DIFFERENCE_TYPES",
    "DIFFERENCE_UNCHANGED",
    "DIFFERENCE_UNKNOWN",
    "EVALUATION_ERROR_CODES",
    "EVALUATION_VERSION",
    "INVALID_STATE",
    "UNAVAILABLE",
    "AdvisoryEvaluationResult",
    "DomainReviewExport",
    "EvaluationMetrics",
    "EvaluationSummary",
    "RecommendationComparison",
    "serialize_canonical",
    "snapshot_mapping",
]
