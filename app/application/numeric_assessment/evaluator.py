"""Public evaluate() entry point for the Numeric Assessment Framework.

Pure function of AnswerSpecification + raw response. Live cutover is owned by
``score_practice_response`` behind ``SR_NUMERIC_ASSESSMENT_FRAMEWORK``.
"""

from __future__ import annotations

from app.application.numeric_assessment.comparator import (
    precision_compliant,
    representation_accepted,
    values_match,
)
from app.application.numeric_assessment.feedback import assemble_feedback
from app.application.numeric_assessment.parser import parse_numeric_response
from app.application.numeric_assessment.results import (
    NumericEvaluationResult,
    ParseStatus,
)
from app.application.numeric_assessment.specs import AnswerSpecification


def evaluate(
    spec: AnswerSpecification, raw_response: str
) -> NumericEvaluationResult:
    """Evaluate a raw student response against an authored Answer Specification.

    Tracks value_correct and precision_compliant as distinct facts. Does not
    invent diagnostic certainty without authored Tier 2 rules.
    """
    parse = parse_numeric_response(raw_response, spec)
    rep_ok = representation_accepted(spec, parse)
    prec = precision_compliant(spec, parse)

    value_correct = False
    if (
        parse.status is ParseStatus.PARSED
        and parse.parsed_value is not None
        and rep_ok
    ):
        value_correct = values_match(spec, parse.parsed_value)

    tier, message, rule_id = assemble_feedback(
        spec,
        parse_status=parse.status,
        parsed_value=parse.parsed_value,
        value_correct=value_correct,
        precision_compliant=prec,
        representation_accepted=rep_ok,
    )

    return NumericEvaluationResult(
        item_id=spec.item_id,
        raw_response=parse.raw_response,
        parse_status=parse.status,
        parsed_value=parse.parsed_value,
        detected_form=parse.detected_form,
        value_correct=value_correct,
        precision_compliant=prec,
        representation_accepted=rep_ok,
        evaluation_policy=spec.evaluation_policy,
        matched_diagnostic_rule_id=rule_id,
        feedback_tier=tier,
        feedback_message=message,
    )
