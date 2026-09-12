"""Numeric Assessment Framework (standalone; unwired from live scoring).

Authored Answer Specifications drive parsing, evaluation-policy comparison,
precision/representation checks, and three-tier feedback. Does not wire into
scoreable_practice, routes, Twin, Policy V1, OEA, Spacing, VP-001, or
Progression Readiness.
"""

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
    "parse_numeric_response",
)
