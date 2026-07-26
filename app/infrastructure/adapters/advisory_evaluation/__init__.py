"""Advisory Evaluation Framework package (P2-MS012).

Scores and analyses simulated recommendation differences without modifying
Runtime A behaviour. Feature flag ``KWALITEC_ADVISORY_EVALUATION`` /
``ENABLE_ADVISORY_EVALUATION`` defaults OFF.

Never modifies production recommendations. Never writes educational state.
No Adaptive / Strategy / Recovery optimisation / automatic rollout.
"""

from __future__ import annotations

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
    DIFFERENCE_TYPES,
    DIFFERENCE_UNCHANGED,
    DIFFERENCE_UNKNOWN,
    EVALUATION_ERROR_CODES,
    EVALUATION_VERSION,
    INVALID_STATE,
    UNAVAILABLE,
    AdvisoryEvaluationResult,
    DomainReviewExport,
    EvaluationMetrics,
    EvaluationSummary,
    RecommendationComparison,
    serialize_canonical,
    snapshot_mapping,
)
from .service import (
    SERVICE_ID,
    SOURCE_SERVICE,
    AdvisoryEvaluationService,
    build_advisory_evaluation_service,
    classify_difference_type,
    deterministic_evaluation_comparison_id,
    deterministic_export_id,
    deterministic_summary_id,
)

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
    "SERVICE_ID",
    "SOURCE_SERVICE",
    "UNAVAILABLE",
    "AdvisoryEvaluationResult",
    "AdvisoryEvaluationService",
    "DomainReviewExport",
    "EvaluationMetrics",
    "EvaluationSummary",
    "RecommendationComparison",
    "build_advisory_evaluation_service",
    "classify_difference_type",
    "deterministic_evaluation_comparison_id",
    "deterministic_export_id",
    "deterministic_summary_id",
    "serialize_canonical",
    "snapshot_mapping",
]
