"""Readiness Intelligence consumer package (EP-001.3).

Projects EP-001.1 CanonicalLearnerState (+ optional EP-001.2 planner outputs)
into readiness evaluation artefacts. Extends Runtime A ReadinessService —
does not replace it or duplicate Twin / Planner ownership.
"""

from __future__ import annotations

from app.infrastructure.adapters.readiness_intelligence.assessment import (
    ReadinessAssessmentAssembler,
    build_readiness_assessment_assembler,
)
from app.infrastructure.adapters.readiness_intelligence.consumer import (
    CanonicalReadinessConsumer,
    build_canonical_readiness_consumer,
)
from app.infrastructure.adapters.readiness_intelligence.contracts import (
    CONFIDENCE_HIGH,
    CONFIDENCE_LEVELS,
    CONFIDENCE_LOW,
    CONFIDENCE_MEDIUM,
    CONFIDENCE_VERY_LOW,
    READINESS_INTELLIGENCE_VERSION,
    REASON_INVALID_STUDENT_ID,
    REASON_PLANNER_UNAVAILABLE,
    REASON_STATE_UNAVAILABLE,
    REASON_TWIN_FLAG_OFF,
    SOURCE_SERVICE_READINESS_INTELLIGENCE,
    ReadinessDriver,
    ReadinessIntelligenceAssessment,
    ReadinessIntelligenceInputs,
    RecommendedNextAction,
    TopicArea,
)

__all__ = [
    "CONFIDENCE_HIGH",
    "CONFIDENCE_LEVELS",
    "CONFIDENCE_LOW",
    "CONFIDENCE_MEDIUM",
    "CONFIDENCE_VERY_LOW",
    "READINESS_INTELLIGENCE_VERSION",
    "REASON_INVALID_STUDENT_ID",
    "REASON_PLANNER_UNAVAILABLE",
    "REASON_STATE_UNAVAILABLE",
    "REASON_TWIN_FLAG_OFF",
    "SOURCE_SERVICE_READINESS_INTELLIGENCE",
    "CanonicalReadinessConsumer",
    "ReadinessAssessmentAssembler",
    "ReadinessDriver",
    "ReadinessIntelligenceAssessment",
    "ReadinessIntelligenceInputs",
    "RecommendedNextAction",
    "TopicArea",
    "build_canonical_readiness_consumer",
    "build_readiness_assessment_assembler",
]
