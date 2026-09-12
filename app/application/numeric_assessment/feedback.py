"""Three-tier feedback assembly for numeric assessment.

Tier 1: deterministic evaluation facts (always).
Tier 2: authored diagnostic rules only when unambiguously matched.
Tier 3: honest uncertainty when incorrect and no Tier 2 rule applies.
"""

from __future__ import annotations

from decimal import Decimal

from app.application.numeric_assessment.results import (
    FeedbackTier,
    ParseStatus,
)
from app.application.numeric_assessment.specs import (
    AnswerSpecification,
    DiagnosticRule,
)


def match_diagnostic_rule(
    spec: AnswerSpecification,
    *,
    parsed_value: float,
    value_correct: bool,
) -> DiagnosticRule | None:
    """Return the first authored rule the observed value unambiguously satisfies.

    Never infers a mistake from the number alone. Only authored rules may match.
    """
    if value_correct:
        return None
    observed = Decimal(str(parsed_value))
    for rule in spec.diagnostic_rules:
        delta = abs(observed - Decimal(str(rule.match_value)))
        if delta <= Decimal(str(rule.match_absolute_tolerance)):
            return rule
    return None


def _tier1_message(
    *,
    parse_status: ParseStatus,
    value_correct: bool,
    precision_compliant: bool | None,
    representation_accepted: bool,
) -> str:
    if parse_status is ParseStatus.UNINTERPRETABLE:
        return (
            "This response could not be interpreted unambiguously "
            "(for example, locale-dependent comma usage)."
        )
    if parse_status is ParseStatus.INVALID:
        return "This response could not be parsed as an accepted numeric form."
    if not representation_accepted:
        return (
            "This response used a representation that is not accepted "
            "for this question."
        )
    if value_correct and precision_compliant is False:
        return (
            "The value is numerically correct, but it does not match "
            "the requested precision."
        )
    if value_correct:
        if precision_compliant is True:
            return "Correct value and requested precision."
        return "Correct value."
    return "The value does not match the accepted answer under the evaluation policy."


def assemble_feedback(
    spec: AnswerSpecification,
    *,
    parse_status: ParseStatus,
    parsed_value: float | None,
    value_correct: bool,
    precision_compliant: bool | None,
    representation_accepted: bool,
) -> tuple[FeedbackTier, str, str | None]:
    """Assemble feedback tier, message, and optional matched diagnostic rule id.

    Returns:
        (tier, message, matched_rule_id)
    """
    tier1 = _tier1_message(
        parse_status=parse_status,
        value_correct=value_correct,
        precision_compliant=precision_compliant,
        representation_accepted=representation_accepted,
    )

    # Parse / representation failures stay on Tier 1 only.
    if parse_status is not ParseStatus.PARSED or not representation_accepted:
        return FeedbackTier.TIER_1, tier1, None

    # Correct path: Tier 1 only (precision note already in message).
    if value_correct:
        return FeedbackTier.TIER_1, tier1, None

    # Incorrect numeric value: try Tier 2, else Tier 3.
    assert parsed_value is not None
    rule = match_diagnostic_rule(
        spec, parsed_value=parsed_value, value_correct=False
    )
    if rule is not None:
        message = f"{tier1} Consistent with {rule.consistent_with}."
        return FeedbackTier.TIER_2, message, rule.rule_id

    message = f"{tier1} {spec.feedback_policy.tier3_message}"
    return FeedbackTier.TIER_3, message, None
