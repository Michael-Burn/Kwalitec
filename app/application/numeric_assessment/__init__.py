"""Numeric Assessment Framework (standalone; unwired from live scoring).

Authored Answer Specifications drive parsing, evaluation-policy comparison,
precision/representation checks, and three-tier feedback. Does not wire into
scoreable_practice, routes, Twin, Policy V1, OEA, Spacing, VP-001, or
Progression Readiness.
"""

from app.application.numeric_assessment.catalogue import (
    BANKED_PRECISION_TOLERANCE_ITEM_IDS,
    LIVE_NUMERIC_CHECKPOINT_COUNT,
    get_live_answer_specification,
    load_live_answer_specifications,
    reset_live_answer_specification_cache,
)
from app.application.numeric_assessment.evaluator import evaluate
from app.application.numeric_assessment.feedback import assemble_feedback
from app.application.numeric_assessment.parser import parse_numeric_response
from app.application.numeric_assessment.results import (
    FeedbackTier,
    NumericEvaluationResult,
    ParseStatus,
)
from app.application.numeric_assessment.specs import (
    AnswerSpecification,
    AssessmentIntent,
    ComparisonPolicy,
    DiagnosticRule,
    EvaluationPolicy,
    FeedbackPolicy,
    PrecisionPolicy,
    PrecisionRequirement,
    QuantityType,
    RepresentationForm,
    RepresentationPolicy,
    RoundingPolicy,
)

__all__ = (
    "BANKED_PRECISION_TOLERANCE_ITEM_IDS",
    "LIVE_NUMERIC_CHECKPOINT_COUNT",
    "AnswerSpecification",
    "AssessmentIntent",
    "ComparisonPolicy",
    "DiagnosticRule",
    "EvaluationPolicy",
    "FeedbackPolicy",
    "FeedbackTier",
    "NumericEvaluationResult",
    "ParseStatus",
    "PrecisionPolicy",
    "PrecisionRequirement",
    "QuantityType",
    "RepresentationForm",
    "RepresentationPolicy",
    "RoundingPolicy",
    "assemble_feedback",
    "evaluate",
    "get_live_answer_specification",
    "load_live_answer_specifications",
    "parse_numeric_response",
    "reset_live_answer_specification_cache",
)
