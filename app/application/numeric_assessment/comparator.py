"""Evaluation-policy comparison, precision, and representation checks.

No universal tolerance. Every comparison uses the authored ComparisonPolicy.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from decimal import ROUND_HALF_UP, Decimal

from app.application.numeric_assessment.parser import count_decimal_places
from app.application.numeric_assessment.results import ParseResult, ParseStatus
from app.application.numeric_assessment.specs import (
    AnswerSpecification,
    EvaluationPolicy,
    PrecisionRequirement,
    RoundingPolicy,
)

CustomRulePredicate = Callable[[float, float, AnswerSpecification], bool]

# Named custom domain rules registered for this standalone pass.
# Migration may extend this registry; free-form code in specs is forbidden.
_CUSTOM_RULES: dict[str, CustomRulePredicate] = {}


def register_custom_domain_rule(
    rule_id: str, predicate: CustomRulePredicate
) -> None:
    """Test / extension hook for CUSTOM_DOMAIN_RULE policies."""
    _CUSTOM_RULES[rule_id] = predicate


def clear_custom_domain_rules() -> None:
    """Clear the custom-rule registry (tests)."""
    _CUSTOM_RULES.clear()


def _round_half_up(value: float, places: int) -> float:
    quant = Decimal("1").scaleb(-places)
    return float(Decimal(str(value)).quantize(quant, rounding=ROUND_HALF_UP))


def _significant_figures_match(
    candidate: float, canonical: float, sig_figs: int
) -> bool:
    if candidate == 0 and canonical == 0:
        return True
    if candidate == 0 or canonical == 0:
        # Compare absolute magnitude at the canonical order when one is zero.
        return abs(candidate - canonical) < 10 ** (
            math.floor(math.log10(abs(canonical or candidate))) - sig_figs + 1
        )

    def _round_sig(x: float) -> float:
        if x == 0:
            return 0.0
        order = math.floor(math.log10(abs(x)))
        factor = 10 ** (sig_figs - 1 - order)
        return round(x * factor) / factor

    return _round_sig(candidate) == _round_sig(canonical)


def values_match(spec: AnswerSpecification, candidate: float) -> bool:
    """Return whether ``candidate`` matches under the authored comparison policy."""
    policy = spec.comparison_policy
    canonical = spec.canonical_value
    kind = policy.policy

    if kind is EvaluationPolicy.EXACT:
        return Decimal(str(candidate)) == Decimal(str(canonical))

    if kind is EvaluationPolicy.ABSOLUTE_TOLERANCE:
        assert policy.absolute_tolerance is not None
        # Decimal comparison so authored decimal boundaries are inclusive
        # without binary float noise (e.g. 0.3297 + 0.001).
        delta = abs(Decimal(str(candidate)) - Decimal(str(canonical)))
        return delta <= Decimal(str(policy.absolute_tolerance))

    if kind is EvaluationPolicy.RELATIVE_TOLERANCE:
        assert policy.relative_tolerance is not None
        if canonical == 0:
            # Authored absolute fallback: relative policy at zero uses exactness.
            return candidate == 0
        return abs(candidate - canonical) <= policy.relative_tolerance * abs(
            canonical
        )

    if kind is EvaluationPolicy.DECIMAL_PRECISION:
        assert policy.decimal_places is not None
        places = policy.decimal_places
        if spec.rounding_policy is RoundingPolicy.HALF_UP:
            return _round_half_up(candidate, places) == _round_half_up(
                canonical, places
            )
        scale = 10 ** places
        return round(candidate * scale) == round(canonical * scale)

    if kind is EvaluationPolicy.SIGNIFICANT_FIGURES:
        assert policy.significant_figures is not None
        return _significant_figures_match(
            candidate, canonical, policy.significant_figures
        )

    if kind is EvaluationPolicy.INTERVAL_RANGE:
        assert policy.interval_low is not None and policy.interval_high is not None
        return policy.interval_low <= candidate <= policy.interval_high

    if kind is EvaluationPolicy.CUSTOM_DOMAIN_RULE:
        rule_id = (policy.custom_rule_id or "").strip()
        predicate = _CUSTOM_RULES.get(rule_id)
        if predicate is None:
            raise ValueError(f"Unknown custom_domain_rule id: {rule_id!r}")
        return bool(predicate(candidate, canonical, spec))

    raise ValueError(f"Unsupported evaluation policy: {kind!r}")


def precision_compliant(
    spec: AnswerSpecification, parse: ParseResult
) -> bool | None:
    """Check authored precision policy against the raw numeric lexeme.

    Returns None when precision is not applicable or the response was not parsed.
    """
    if parse.status is not ParseStatus.PARSED:
        return None
    req = spec.precision_policy.requirement
    if req is PrecisionRequirement.NONE:
        return None
    places = count_decimal_places(parse.numeric_lexeme)
    if places is None:
        # Scientific notation: cannot judge decimal-place display compliance.
        return False
    expected = spec.precision_policy.decimal_places
    assert expected is not None
    if req is PrecisionRequirement.EXACT_DECIMAL_PLACES:
        return places == expected
    if req is PrecisionRequirement.AT_LEAST_DECIMAL_PLACES:
        return places >= expected
    if req is PrecisionRequirement.AT_MOST_DECIMAL_PLACES:
        return places <= expected
    raise ValueError(f"Unsupported precision requirement: {req!r}")


def representation_accepted(
    spec: AnswerSpecification, parse: ParseResult
) -> bool:
    """True when parse succeeded with an authored accepted form."""
    if parse.status is not ParseStatus.PARSED or parse.detected_form is None:
        return False
    return parse.detected_form in spec.accepted_forms
