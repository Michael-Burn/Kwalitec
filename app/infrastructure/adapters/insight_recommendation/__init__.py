"""Insight & Recommendation Layer consumer package (EP-001.4).

Projects EP-001.1 CanonicalLearnerState, EP-001.2 planner outputs, and
EP-001.3 readiness intelligence into student-facing study guidance.
Extends Runtime A RecommendationService — does not replace it or duplicate
Twin / Planner / Readiness ownership.
"""

from __future__ import annotations

from app.infrastructure.adapters.insight_recommendation.assembler import (
    StudyInsightAssembler,
    build_study_insight_assembler,
)
from app.infrastructure.adapters.insight_recommendation.consumer import (
    CanonicalInsightConsumer,
    build_canonical_insight_consumer,
)
from app.infrastructure.adapters.insight_recommendation.contracts import (
    INSIGHT_LAYER_VERSION,
    REASON_INVALID_STUDENT_ID,
    REASON_PLANNER_UNAVAILABLE,
    REASON_READINESS_UNAVAILABLE,
    REASON_STATE_UNAVAILABLE,
    REASON_TWIN_FLAG_OFF,
    SOURCE_SERVICE_INSIGHT_RECOMMENDATION,
    InsightField,
    StudyInsightGuidance,
    StudyInsightInputs,
)

__all__ = [
    "INSIGHT_LAYER_VERSION",
    "REASON_INVALID_STUDENT_ID",
    "REASON_PLANNER_UNAVAILABLE",
    "REASON_READINESS_UNAVAILABLE",
    "REASON_STATE_UNAVAILABLE",
    "REASON_TWIN_FLAG_OFF",
    "SOURCE_SERVICE_INSIGHT_RECOMMENDATION",
    "CanonicalInsightConsumer",
    "InsightField",
    "StudyInsightAssembler",
    "StudyInsightGuidance",
    "StudyInsightInputs",
    "build_canonical_insight_consumer",
    "build_study_insight_assembler",
]
