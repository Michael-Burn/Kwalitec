"""Advisory Evaluation Service (P2-MS012).

Consumes Decision Simulation outputs, aggregates operational comparison
metrics, and generates evaluation summaries / domain review exports.

Never modifies Runtime A recommendations. Never influences student-facing
behaviour. No Adaptive / Strategy / Recovery optimisation.
"""

from __future__ import annotations

import hashlib
import logging
from collections.abc import Mapping, Sequence
from typing import Any

from .contracts import (
    AUTHORITY_ADVISORY_EVALUATION,
    AUTHORITY_DECISION_SIMULATION,
    AUTHORITY_RUNTIME_A,
    DIFFERENCE_CATEGORY,
    DIFFERENCE_MULTI_FIELD,
    DIFFERENCE_PRIORITY,
    DIFFERENCE_RATIONALE_ANNOTATION,
    DIFFERENCE_STRUCTURAL,
    DIFFERENCE_TITLE,
    DIFFERENCE_UNCHANGED,
    EVALUATION_VERSION,
    INVALID_STATE,
    UNAVAILABLE,
    AdvisoryEvaluationResult,
    DomainReviewExport,
    EvaluationMetrics,
    EvaluationSummary,
    RecommendationComparison,
    serialize_canonical,
)

logger = logging.getLogger(__name__)

SERVICE_ID = "advisory_evaluation_service"
SOURCE_SERVICE = "advisory_evaluation"

# Preferred field names when extracting rationales from recommendation snapshots.
_RATIONALE_KEYS = ("reason", "rationale", "simulated_rationale", "explanation")


def deterministic_evaluation_comparison_id(
    *,
    simulation_id: str = "",
    recommendation_id: str = "",
    source_comparison_id: str = "",
) -> str:
    """Deterministic evaluation comparison id from simulation artefacts."""
    material = {
        "recommendation_id": (recommendation_id or "").strip(),
        "simulation_id": (simulation_id or "").strip(),
        "source_comparison_id": (source_comparison_id or "").strip(),
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()[:16]
    return f"adveval-{digest}"


def deterministic_export_id(comparison_id: str) -> str:
    """Deterministic domain review export id."""
    material = {"comparison_id": (comparison_id or "").strip()}
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()[:16]
    return f"advexp-{digest}"


def deterministic_summary_id(
    *,
    comparison_ids: Sequence[str],
    generated_at: str | None = None,
) -> str:
    """Deterministic evaluation summary id."""
    material = {
        "comparison_ids": sorted(str(item) for item in comparison_ids),
        "generated_at": generated_at,
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()[:16]
    return f"advsum-{digest}"


def _as_mapping(value: Any) -> Mapping[str, Any]:
    if value is None:
        return {}
    if hasattr(value, "to_canonical_dict"):
        payload = value.to_canonical_dict()
        return payload if isinstance(payload, Mapping) else {}
    if isinstance(value, Mapping):
        return value
    return {}


def _extract_rationale(snapshot: Mapping[str, Any]) -> str:
    for key in _RATIONALE_KEYS:
        if key in snapshot and snapshot[key] is not None:
            text = str(snapshot[key]).strip()
            if text:
                return text
    return ""


def _field_names_from_differences(differences: Sequence[Any]) -> tuple[str, ...]:
    names: list[str] = []
    for item in differences or ():
        if isinstance(item, Mapping):
            name = str(item.get("field_name") or "").strip()
        else:
            name = str(getattr(item, "field_name", "") or "").strip()
        if name:
            names.append(name)
    # Preserve order, drop duplicates.
    seen: set[str] = set()
    ordered: list[str] = []
    for name in names:
        if name in seen:
            continue
        seen.add(name)
        ordered.append(name)
    return tuple(ordered)


def classify_difference_type(
    *,
    differs: bool,
    field_names: Sequence[str] | None = None,
) -> str:
    """Classify an operational difference type (no ranking)."""
    if not differs:
        return DIFFERENCE_UNCHANGED
    names = [str(item).strip().lower() for item in (field_names or ()) if item]
    if not names:
        return DIFFERENCE_STRUCTURAL
    unique = tuple(dict.fromkeys(names))
    if len(unique) > 1:
        return DIFFERENCE_MULTI_FIELD
    single = unique[0]
    if single in {"rationale", "reason", "simulated_rationale"}:
        return DIFFERENCE_RATIONALE_ANNOTATION
    if single == "priority":
        return DIFFERENCE_PRIORITY
    if single == "title":
        return DIFFERENCE_TITLE
    if single == "category":
        return DIFFERENCE_CATEGORY
    return DIFFERENCE_STRUCTURAL


def _strip_student_identifiers(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    """Remove student identifiers from evaluation artefacts."""
    blocked = {
        "student_id",
        "user_id",
        "learner_id",
        "opaque_student_id",
        "email",
    }
    return {
        str(key): value
        for key, value in dict(snapshot or {}).items()
        if str(key) not in blocked
    }


def _is_explainable(comparison: RecommendationComparison) -> bool:
    """Operational completeness: provenance present; explanation when differs."""
    if not comparison.provenance:
        return False
    if comparison.differs and comparison.difference_type == DIFFERENCE_UNCHANGED:
        return False
    if comparison.differs and not comparison.difference_type:
        return False
    return True


def _simulation_record_fields(record: Any) -> dict[str, Any]:
    """Normalise a DecisionComparisonRecord / mapping into evaluation inputs."""
    if hasattr(record, "to_canonical_dict") and not isinstance(record, Mapping):
        payload = record.to_canonical_dict()
    elif isinstance(record, Mapping):
        payload = dict(record)
    else:
        raise TypeError(
            "simulation output must be a DecisionComparisonRecord-like mapping or DTO"
        )

    production = _as_mapping(payload.get("production_recommendation"))
    simulated_raw = payload.get("simulated_recommendation")
    simulated = _as_mapping(simulated_raw)

    advisory_sources = payload.get("advisory_sources_considered")
    if advisory_sources is None:
        advisory_sources = simulated.get("advisory_sources") or ()
    if isinstance(advisory_sources, str):
        advisory_sources = (advisory_sources,)
    sources = tuple(str(item) for item in (advisory_sources or ()))

    differences = payload.get("differences") or ()
    field_names = _field_names_from_differences(differences)

    differs_flag = bool(payload.get("differs"))
    if "differs" not in payload and "differs_from_runtime" not in simulated:
        differs_flag = bool(field_names) or bool(
            simulated.get("differs_from_runtime")
        )
    elif "differs_from_runtime" in simulated and "differs" not in payload:
        differs_flag = bool(simulated.get("differs_from_runtime"))

    provenance = _as_mapping(payload.get("provenance"))
    simulated_provenance = _as_mapping(simulated.get("provenance"))
    merged_provenance = {
        **dict(simulated_provenance),
        **dict(provenance),
        "authority_chain": {
            "evaluation": AUTHORITY_ADVISORY_EVALUATION,
            "production": AUTHORITY_RUNTIME_A,
            "simulation": AUTHORITY_DECISION_SIMULATION,
        },
        "source_service": SOURCE_SERVICE,
    }

    return {
        "advisory_sources": sources,
        "differs": differs_flag,
        "field_names": field_names,
        "generated_at": payload.get("generated_at") or simulated.get("generated_at"),
        "production": _strip_student_identifiers(production),
        "provenance": merged_provenance,
        "recommendation_id": str(
            payload.get("recommendation_id")
            or simulated.get("recommendation_id")
            or ""
        ).strip(),
        "simulation_id": str(
            payload.get("simulation_id") or simulated.get("simulation_id") or ""
        ).strip(),
        "simulated": _strip_student_identifiers(simulated),
        "source_comparison_id": str(payload.get("comparison_id") or "").strip(),
    }


class AdvisoryEvaluationService:
    """Evaluate simulated recommendation differences (ops / review only).

    Rules:
    - MAY consume Decision Simulation comparison artefacts
    - MAY aggregate EvaluationMetrics and DomainReviewExport
    - MUST NEVER modify production recommendation outputs
    - MUST NOT write Runtime A / Adaptive / Strategy / Twin educational state
    - MUST NOT include student identifiers on evaluation artefacts
    """

    SERVICE_VERSION = "1.0.0-p2.ms012"

    def __init__(self, *, enabled: bool = True) -> None:
        self._enabled = bool(enabled)
        self._last_result: AdvisoryEvaluationResult | None = None
        self._comparisons: list[RecommendationComparison] = []

    @property
    def service_id(self) -> str:
        return SERVICE_ID

    @property
    def service_version(self) -> str:
        return self.SERVICE_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    @property
    def last_result(self) -> AdvisoryEvaluationResult | None:
        return self._last_result

    @property
    def comparisons(self) -> tuple[RecommendationComparison, ...]:
        """Operational comparison artefacts accumulated this process (in-memory)."""
        return tuple(self._comparisons)

    def clear_comparisons(self) -> None:
        """Clear in-memory operational comparison buffer."""
        self._comparisons.clear()

    def ingest_simulation(
        self,
        simulation_output: Any,
    ) -> AdvisoryEvaluationResult:
        """Consume one simulation comparison into a RecommendationComparison."""
        if not self._enabled:
            result = AdvisoryEvaluationResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_ADVISORY_EVALUATION is OFF",
            )
            self._last_result = result
            return result
        try:
            comparison = self._build_comparison(simulation_output)
        except Exception as exc:
            logger.warning(
                "advisory_evaluation_ingest_failed error=%s",
                exc,
                exc_info=True,
            )
            result = AdvisoryEvaluationResult(
                ok=False,
                error_code=INVALID_STATE,
                message=str(exc) or "advisory evaluation ingest failed",
            )
            self._last_result = result
            return result
        self._comparisons.append(comparison)
        result = AdvisoryEvaluationResult(ok=True, comparison=comparison)
        self._last_result = result
        logger.debug(
            "advisory_evaluation_ingested comparison_id=%s differs=%s type=%s",
            comparison.comparison_id,
            comparison.differs,
            comparison.difference_type,
        )
        return result

    def ingest_simulations(
        self,
        simulation_outputs: Sequence[Any],
    ) -> tuple[RecommendationComparison, ...]:
        """Ingest many simulation outputs; skip failures; never mutate inputs."""
        if not self._enabled:
            return ()
        records: list[RecommendationComparison] = []
        for item in simulation_outputs or ():
            result = self.ingest_simulation(item)
            if result.ok and result.comparison is not None:
                records.append(result.comparison)
        return tuple(records)

    def aggregate_metrics(
        self,
        comparisons: Sequence[RecommendationComparison] | None = None,
        *,
        generated_at: str | None = None,
    ) -> AdvisoryEvaluationResult:
        """Aggregate operational EvaluationMetrics from comparisons."""
        if not self._enabled:
            result = AdvisoryEvaluationResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_ADVISORY_EVALUATION is OFF",
            )
            self._last_result = result
            return result
        cohort = tuple(comparisons) if comparisons is not None else self.comparisons
        for item in cohort:
            if not isinstance(item, RecommendationComparison):
                result = AdvisoryEvaluationResult(
                    ok=False,
                    error_code=INVALID_STATE,
                    message="comparisons must contain RecommendationComparison values",
                )
                self._last_result = result
                return result
        metrics = self._compute_metrics(cohort, generated_at=generated_at)
        result = AdvisoryEvaluationResult(ok=True, metrics=metrics)
        self._last_result = result
        return result

    def generate_export(
        self,
        comparison: RecommendationComparison,
    ) -> AdvisoryEvaluationResult:
        """Build a DomainReviewExport for actuarial / educational review."""
        if not self._enabled:
            result = AdvisoryEvaluationResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_ADVISORY_EVALUATION is OFF",
            )
            self._last_result = result
            return result
        if not isinstance(comparison, RecommendationComparison):
            result = AdvisoryEvaluationResult(
                ok=False,
                error_code=INVALID_STATE,
                message="comparison must be a RecommendationComparison",
            )
            self._last_result = result
            return result
        export = self._build_export(comparison)
        result = AdvisoryEvaluationResult(ok=True, export=export, comparison=comparison)
        self._last_result = result
        return result

    def generate_summary(
        self,
        comparisons: Sequence[RecommendationComparison] | None = None,
        *,
        include_exports: bool = True,
        generated_at: str | None = None,
        notes: Sequence[str] | None = None,
    ) -> AdvisoryEvaluationResult:
        """Generate an EvaluationSummary with metrics (and optional exports)."""
        if not self._enabled:
            result = AdvisoryEvaluationResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_ADVISORY_EVALUATION is OFF",
            )
            self._last_result = result
            return result
        cohort = tuple(comparisons) if comparisons is not None else self.comparisons
        for item in cohort:
            if not isinstance(item, RecommendationComparison):
                result = AdvisoryEvaluationResult(
                    ok=False,
                    error_code=INVALID_STATE,
                    message="comparisons must contain RecommendationComparison values",
                )
                self._last_result = result
                return result
        metrics = self._compute_metrics(cohort, generated_at=generated_at)
        exports: tuple[DomainReviewExport, ...] = ()
        if include_exports:
            exports = tuple(self._build_export(item) for item in cohort)
        summary_notes = tuple(str(item) for item in (notes or ()))
        if not summary_notes:
            summary_notes = (
                "Operational evaluation only — Runtime A behaviour unchanged.",
                "No student identifiers included in evaluation artefacts.",
                (
                    "Await architecture review before advisory-informed "
                    "Runtime A decisions."
                ),
            )
        summary = EvaluationSummary(
            summary_id=deterministic_summary_id(
                comparison_ids=[item.comparison_id for item in cohort],
                generated_at=generated_at,
            ),
            metrics=metrics,
            comparisons=cohort,
            exports=exports,
            notes=summary_notes,
            generated_at=generated_at,
            operational_only=True,
        )
        result = AdvisoryEvaluationResult(
            ok=True,
            metrics=metrics,
            summary=summary,
        )
        self._last_result = result
        return result

    def evaluate_simulation_batch(
        self,
        simulation_outputs: Sequence[Any],
        *,
        include_exports: bool = True,
        generated_at: str | None = None,
    ) -> AdvisoryEvaluationResult:
        """Ingest simulation outputs then return a full evaluation summary."""
        if not self._enabled:
            result = AdvisoryEvaluationResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_ADVISORY_EVALUATION is OFF",
            )
            self._last_result = result
            return result
        comparisons = self.ingest_simulations(simulation_outputs)
        return self.generate_summary(
            comparisons,
            include_exports=include_exports,
            generated_at=generated_at,
        )

    def _build_comparison(self, simulation_output: Any) -> RecommendationComparison:
        fields = _simulation_record_fields(simulation_output)
        difference_type = classify_difference_type(
            differs=fields["differs"],
            field_names=fields["field_names"],
        )
        comparison_id = deterministic_evaluation_comparison_id(
            simulation_id=fields["simulation_id"],
            recommendation_id=fields["recommendation_id"],
            source_comparison_id=fields["source_comparison_id"],
        )
        provenance = {
            **dict(fields["provenance"]),
            "difference_type": difference_type,
            "evaluation_version": EVALUATION_VERSION,
            "field_names": list(fields["field_names"]),
            "service_id": self.service_id,
            "service_version": self.SERVICE_VERSION,
            "source_comparison_id": fields["source_comparison_id"],
        }
        return RecommendationComparison(
            comparison_id=comparison_id,
            production_recommendation=fields["production"],
            simulated_recommendation=fields["simulated"],
            differs=fields["differs"],
            difference_type=difference_type,
            advisory_sources=fields["advisory_sources"],
            generated_at=fields["generated_at"],
            simulation_id=fields["simulation_id"],
            recommendation_id=fields["recommendation_id"],
            provenance=provenance,
            operational_only=True,
        )

    def _compute_metrics(
        self,
        comparisons: Sequence[RecommendationComparison],
        *,
        generated_at: str | None = None,
    ) -> EvaluationMetrics:
        count = len(comparisons)
        if count == 0:
            return EvaluationMetrics(
                comparison_count=0,
                difference_rate=0.0,
                unchanged_rate=0.0,
                advisory_usage_frequency=0.0,
                explainability_completeness=0.0,
                generated_at=generated_at,
                operational_only=True,
            )
        differs_n = sum(1 for item in comparisons if item.differs)
        unchanged_n = count - differs_n
        advisory_n = sum(1 for item in comparisons if item.advisory_sources)
        explainable_n = sum(1 for item in comparisons if _is_explainable(item))

        type_counts: dict[str, int] = {}
        source_counts: dict[str, int] = {}
        for item in comparisons:
            type_counts[item.difference_type] = (
                type_counts.get(item.difference_type, 0) + 1
            )
            for source in item.advisory_sources:
                # Count family prefixes once (evidence_advisory / recovery_candidate).
                family = source.split(":", 1)[0]
                source_counts[family] = source_counts.get(family, 0) + 1

        return EvaluationMetrics(
            comparison_count=count,
            difference_rate=differs_n / count,
            unchanged_rate=unchanged_n / count,
            advisory_usage_frequency=advisory_n / count,
            explainability_completeness=explainable_n / count,
            difference_type_counts=type_counts,
            advisory_source_counts=source_counts,
            generated_at=generated_at,
            operational_only=True,
        )

    def _build_export(
        self,
        comparison: RecommendationComparison,
    ) -> DomainReviewExport:
        production = dict(comparison.production_recommendation)
        simulated = dict(comparison.simulated_recommendation)
        production_rationale = _extract_rationale(production)
        simulated_rationale = _extract_rationale(simulated)
        if comparison.differs:
            explanation = (
                f"Simulated recommendation differs from production "
                f"(difference_type={comparison.difference_type}). "
                "Production remains authoritative for students; this export is "
                "for actuarial / educational review only."
            )
            if comparison.advisory_sources:
                joined = ", ".join(comparison.advisory_sources)
                explanation = f"{explanation} Advisory sources: {joined}."
        else:
            explanation = (
                "Simulated recommendation matches production snapshot "
                "(difference_type=unchanged). No advisory-informed divergence "
                "observed for this comparison."
            )
        provenance = {
            **dict(comparison.provenance),
            "export_authority": AUTHORITY_ADVISORY_EVALUATION,
            "review_only": True,
            "student_facing": False,
        }
        return DomainReviewExport(
            export_id=deterministic_export_id(comparison.comparison_id),
            comparison_id=comparison.comparison_id,
            production_rationale=production_rationale,
            simulated_rationale=simulated_rationale,
            provenance=provenance,
            explanation=explanation,
            difference_type=comparison.difference_type,
            differs=comparison.differs,
            advisory_sources=comparison.advisory_sources,
            production_recommendation=production,
            simulated_recommendation=simulated,
            generated_at=comparison.generated_at,
            review_only=True,
            student_facing=False,
        )


def build_advisory_evaluation_service(
    *,
    enabled: bool,
) -> AdvisoryEvaluationService | None:
    """DI helper — construct service only when ENABLE_ADVISORY_EVALUATION is ON."""
    if not enabled:
        return None
    return AdvisoryEvaluationService(enabled=True)


__all__ = [
    "SERVICE_ID",
    "SOURCE_SERVICE",
    "AdvisoryEvaluationService",
    "build_advisory_evaluation_service",
    "classify_difference_type",
    "deterministic_evaluation_comparison_id",
    "deterministic_export_id",
    "deterministic_summary_id",
]
