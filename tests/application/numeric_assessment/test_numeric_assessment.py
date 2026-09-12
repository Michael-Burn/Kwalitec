"""Standalone Numeric Assessment Framework harness.

Uses representative contracts drawn from the 30 live CS1 numeric checkpoints.
Does not wire into live scoring. Does not migrate package JSON.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from app.application.numeric_assessment import (
    AnswerSpecification,
    AssessmentIntent,
    ComparisonPolicy,
    DiagnosticRule,
    EvaluationPolicy,
    FeedbackTier,
    ParseStatus,
    PrecisionPolicy,
    PrecisionRequirement,
    QuantityType,
    RepresentationForm,
    RepresentationPolicy,
    RoundingPolicy,
    evaluate,
)
from app.application.numeric_assessment.comparator import (
    clear_custom_domain_rules,
    register_custom_domain_rule,
    values_match,
)

PKG = Path("app/application/numeric_assessment")
FORBIDDEN_IMPORT_PREFIXES = (
    "app.application.student_twin",
    "app.application.student_digital_twin",
    "app.domain.student_twin",
    "app.domain.student_digital_twin",
    "app.application.spacing_scheduler",
    "app.domain.spacing_scheduler",
    "app.application.adaptive_decision",
    "app.domain.decision",
    "app.application.progression_readiness",
    "app.presentation",
    "app.application.learning_session.scoreable_practice",
)


def _abs_spec(
    item_id: str,
    canonical: float,
    tol: float,
    *,
    quantity: QuantityType = QuantityType.SCALAR,
    intent: AssessmentIntent = AssessmentIntent.CALCULATE_VALUE,
    precision: PrecisionPolicy | None = None,
    forms: tuple[RepresentationForm, ...] = (RepresentationForm.DECIMAL,),
    diagnostics: tuple[DiagnosticRule, ...] = (),
    rounding: RoundingPolicy = RoundingPolicy.NONE,
) -> AnswerSpecification:
    return AnswerSpecification(
        item_id=item_id,
        canonical_value=canonical,
        quantity_type=quantity,
        assessment_intent=intent,
        comparison_policy=ComparisonPolicy(
            policy=EvaluationPolicy.ABSOLUTE_TOLERANCE,
            absolute_tolerance=tol,
        ),
        representation_policy=RepresentationPolicy(accepted_forms=forms),
        precision_policy=precision or PrecisionPolicy(),
        rounding_policy=rounding,
        diagnostic_rules=diagnostics,
    )


# Representative contracts from the live 30 (migration source; not wired).
SPEC_QUANTILE = _abs_spec(
    "cs1004-2.1c-cp-01",
    0.3297,
    0.001,
    quantity=QuantityType.PROBABILITY,
    forms=(RepresentationForm.DECIMAL,),
    diagnostics=(
        DiagnosticRule(
            rule_id="survival-instead-of-cdf",
            match_value=0.6703,
            match_absolute_tolerance=0.001,
            consistent_with="reporting the survival probability instead of the CDF",
            rationale="e^{-0.4} vs 1-e^{-0.4}",
        ),
    ),
)

SPEC_CONDITIONAL = _abs_spec(
    "cs1006-2.3.1-cp-01",
    0.571,
    0.001,
    quantity=QuantityType.PROBABILITY,
)

SPEC_LINEAR_COMB = _abs_spec(
    "cs1005-2.2.4-cp-01",
    17.0,
    0.5,
    forms=(RepresentationForm.DECIMAL, RepresentationForm.INTEGER),
)

SPEC_RESIDUAL = _abs_spec(
    "cs1003-4.2.8-cp-01",
    -1.2247,
    0.001,
    quantity=QuantityType.RESIDUAL,
    precision=PrecisionPolicy(
        requirement=PrecisionRequirement.EXACT_DECIMAL_PLACES,
        decimal_places=4,
    ),
    diagnostics=(
        DiagnosticRule(
            rule_id="dropped-sign",
            match_value=1.2247,
            match_absolute_tolerance=0.001,
            consistent_with="dropping the sign on the residual",
        ),
    ),
)

SPEC_BOOTSTRAP = _abs_spec(
    "cs1010-3.1.6-cp-01",
    8.602,
    0.001,
    precision=PrecisionPolicy(
        requirement=PrecisionRequirement.EXACT_DECIMAL_PLACES,
        decimal_places=3,
    ),
)

SPEC_EMPIRICAL_BAYES = _abs_spec(
    "cs1015-5.1.8-cp-01",
    566.67,
    0.005,
    precision=PrecisionPolicy(
        requirement=PrecisionRequirement.EXACT_DECIMAL_PLACES,
        decimal_places=2,
    ),
)

SPEC_PREMIUM = _abs_spec(
    "cs1003-5.1.6-cp-01",
    1110.0,
    0.5,
    forms=(RepresentationForm.DECIMAL, RepresentationForm.INTEGER),
    diagnostics=(
        DiagnosticRule(
            rule_id="swapped-weights",
            match_value=1090.0,
            match_absolute_tolerance=0.5,
            consistent_with="swapping the credibility weights",
        ),
    ),
)

SPEC_FACTOR_PCT = AnswerSpecification(
    item_id="cs1014-4.2.10-cp-01",
    canonical_value=1.2214,
    quantity_type=QuantityType.FACTOR,
    assessment_intent=AssessmentIntent.INTERPRET_RESULT,
    comparison_policy=ComparisonPolicy(
        policy=EvaluationPolicy.ABSOLUTE_TOLERANCE,
        absolute_tolerance=0.001,
    ),
    representation_policy=RepresentationPolicy(
        accepted_forms=(RepresentationForm.DECIMAL, RepresentationForm.PERCENTAGE),
    ),
)


# ---------------------------------------------------------------------------
# Isolation / package discipline
# ---------------------------------------------------------------------------


def test_package_does_not_import_forbidden_modules() -> None:
    for path in PKG.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            else:
                continue
            for name in names:
                for prefix in FORBIDDEN_IMPORT_PREFIXES:
                    assert not name.startswith(prefix), (
                        f"{path} imports forbidden module {name}"
                    )


def test_spec_rejects_missing_absolute_tolerance() -> None:
    with pytest.raises(ValueError, match="absolute_tolerance"):
        AnswerSpecification(
            item_id="bad",
            canonical_value=1.0,
            quantity_type=QuantityType.SCALAR,
            assessment_intent=AssessmentIntent.CALCULATE_VALUE,
            comparison_policy=ComparisonPolicy(
                policy=EvaluationPolicy.ABSOLUTE_TOLERANCE
            ),
        )


def test_no_universal_tolerance_constant_in_package() -> None:
    """Package must not reintroduce a silent 1e-6 (or similar) default."""
    for path in PKG.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "1e-6" not in text
        assert "1e-06" not in text
        assert "0.000001" not in text


# ---------------------------------------------------------------------------
# Exact / accepted / boundary cases from real questions
# ---------------------------------------------------------------------------


def test_exact_correct_quantile() -> None:
    result = evaluate(SPEC_QUANTILE, "0.3297")
    assert result.parse_status is ParseStatus.PARSED
    assert result.value_correct is True
    assert result.precision_compliant is None
    assert result.fully_correct is True
    assert result.feedback_tier is FeedbackTier.TIER_1


def test_accepted_percentage_representation_for_factor_question() -> None:
    # Canonical factor 1.2214; if an author accepts percentage form of the
    # uplift, 22.14% normalizes to 0.2214, which is NOT the factor. For a
    # true equivalent on the same scale, use a probability-style example.
    prob_spec = AnswerSpecification(
        item_id="cs1004-2.1c-cp-01-pct",
        canonical_value=0.3297,
        quantity_type=QuantityType.PROBABILITY,
        assessment_intent=AssessmentIntent.CALCULATE_VALUE,
        comparison_policy=ComparisonPolicy(
            policy=EvaluationPolicy.ABSOLUTE_TOLERANCE,
            absolute_tolerance=0.001,
        ),
        representation_policy=RepresentationPolicy(
            accepted_forms=(
                RepresentationForm.DECIMAL,
                RepresentationForm.PERCENTAGE,
            ),
        ),
    )
    result = evaluate(prob_spec, "32.97%")
    assert result.parse_status is ParseStatus.PARSED
    assert result.detected_form is RepresentationForm.PERCENTAGE
    assert result.value_correct is True
    assert result.representation_accepted is True


def test_percentage_rejected_when_not_in_accepted_forms() -> None:
    result = evaluate(SPEC_QUANTILE, "32.97%")
    assert result.parse_status is ParseStatus.INVALID
    assert result.value_correct is False
    assert result.feedback_tier is FeedbackTier.TIER_1


def test_just_outside_tolerance() -> None:
    # 0.3297 + 0.001 + a touch
    result = evaluate(SPEC_QUANTILE, "0.3308")
    assert result.value_correct is False
    assert result.feedback_tier is FeedbackTier.TIER_3
    assert "cannot determine the specific calculation error" in result.feedback_message


def test_at_absolute_tolerance_boundary_inclusive() -> None:
    result = evaluate(SPEC_QUANTILE, "0.3307")  # |0.3307 - 0.3297| == 0.001
    assert result.value_correct is True


def test_substantially_wrong_without_diagnostic() -> None:
    result = evaluate(SPEC_CONDITIONAL, "0.100")
    assert result.value_correct is False
    assert result.matched_diagnostic_rule_id is None
    assert result.feedback_tier is FeedbackTier.TIER_3


def test_tier2_diagnostic_when_authored_rule_matches() -> None:
    result = evaluate(SPEC_QUANTILE, "0.6703")
    assert result.value_correct is False
    assert result.feedback_tier is FeedbackTier.TIER_2
    assert result.matched_diagnostic_rule_id == "survival-instead-of-cdf"
    assert "Consistent with" in result.feedback_message
    assert "you did" not in result.feedback_message.lower()


def test_negative_residual_correct() -> None:
    result = evaluate(SPEC_RESIDUAL, "-1.2247")
    assert result.value_correct is True
    assert result.precision_compliant is True
    assert result.fully_correct is True


def test_negative_residual_dropped_sign_tier2() -> None:
    result = evaluate(SPEC_RESIDUAL, "1.2247")
    assert result.value_correct is False
    assert result.feedback_tier is FeedbackTier.TIER_2
    assert result.matched_diagnostic_rule_id == "dropped-sign"


def test_insufficient_precision_value_still_correct() -> None:
    # Canonical -1.2247; -1.225 is within tol=0.001 but has 3 dp, not 4.
    result = evaluate(SPEC_RESIDUAL, "-1.225")
    assert result.value_correct is True
    assert result.precision_compliant is False
    assert result.fully_correct is False
    assert "numerically correct" in result.feedback_message
    assert "requested precision" in result.feedback_message


def test_excessive_precision_fails_exact_decimal_places() -> None:
    result = evaluate(SPEC_BOOTSTRAP, "8.6020")
    assert result.value_correct is True
    assert result.precision_compliant is False


def test_trailing_zeros_satisfy_exact_decimal_places() -> None:
    result = evaluate(SPEC_EMPIRICAL_BAYES, "566.67")
    assert result.value_correct is True
    assert result.precision_compliant is True
    # Trailing zero required for 2 dp when author writes 566.70-style:
    two_dp = _abs_spec(
        "trail-zeros",
        566.70,
        0.005,
        precision=PrecisionPolicy(
            requirement=PrecisionRequirement.EXACT_DECIMAL_PLACES,
            decimal_places=2,
        ),
    )
    ok = evaluate(two_dp, "566.70")
    assert ok.precision_compliant is True
    thin = evaluate(two_dp, "566.7")
    assert thin.value_correct is True
    assert thin.precision_compliant is False


def test_integer_premium_accepted() -> None:
    result = evaluate(SPEC_PREMIUM, "1110")
    assert result.value_correct is True
    assert result.detected_form is RepresentationForm.INTEGER


def test_premium_swapped_weights_tier2() -> None:
    result = evaluate(SPEC_PREMIUM, "1090")
    assert result.feedback_tier is FeedbackTier.TIER_2
    assert result.matched_diagnostic_rule_id == "swapped-weights"


def test_malformed_fraction_invalid() -> None:
    result = evaluate(SPEC_CONDITIONAL, "1/2")
    assert result.parse_status is ParseStatus.INVALID
    assert result.value_correct is False


def test_malformed_units_invalid() -> None:
    result = evaluate(SPEC_LINEAR_COMB, "17 units")
    assert result.parse_status is ParseStatus.INVALID


def test_locale_ambiguous_comma_uninterpretable() -> None:
    result = evaluate(SPEC_CONDITIONAL, "0,571")
    assert result.parse_status is ParseStatus.UNINTERPRETABLE
    assert result.value_correct is False
    assert "unambiguously" in result.feedback_message


def test_european_thousands_decimal_uninterpretable() -> None:
    result = evaluate(SPEC_PREMIUM, "1.110,5")
    assert result.parse_status is ParseStatus.UNINTERPRETABLE


def test_us_thousands_separator_ok() -> None:
    result = evaluate(SPEC_PREMIUM, "1,110")
    assert result.parse_status is ParseStatus.PARSED
    assert result.value_correct is True


# ---------------------------------------------------------------------------
# Other evaluation policies
# ---------------------------------------------------------------------------


def test_exact_policy() -> None:
    spec = AnswerSpecification(
        item_id="exact-1",
        canonical_value=2.0,
        quantity_type=QuantityType.RATE,
        assessment_intent=AssessmentIntent.APPLY_FORMULA,
        comparison_policy=ComparisonPolicy(policy=EvaluationPolicy.EXACT),
    )
    assert evaluate(spec, "2").value_correct is True
    assert evaluate(spec, "2.0000001").value_correct is False


def test_decimal_precision_policy_half_up() -> None:
    spec = AnswerSpecification(
        item_id="dec-1",
        canonical_value=8.6025,
        quantity_type=QuantityType.SCALAR,
        assessment_intent=AssessmentIntent.ROUND_VALUE,
        comparison_policy=ComparisonPolicy(
            policy=EvaluationPolicy.DECIMAL_PRECISION,
            decimal_places=3,
        ),
        rounding_policy=RoundingPolicy.HALF_UP,
    )
    assert evaluate(spec, "8.603").value_correct is True
    assert evaluate(spec, "8.602").value_correct is False


def test_relative_tolerance_policy() -> None:
    spec = AnswerSpecification(
        item_id="rel-1",
        canonical_value=2200.0,
        quantity_type=QuantityType.SCALAR,
        assessment_intent=AssessmentIntent.CALCULATE_VALUE,
        comparison_policy=ComparisonPolicy(
            policy=EvaluationPolicy.RELATIVE_TOLERANCE,
            relative_tolerance=0.01,
        ),
    )
    assert evaluate(spec, "2220").value_correct is True  # 20/2200 < 0.01? 20/2200≈0.009
    assert evaluate(spec, "2300").value_correct is False


def test_interval_range_policy() -> None:
    spec = AnswerSpecification(
        item_id="int-1",
        canonical_value=0.5,
        quantity_type=QuantityType.PROBABILITY,
        assessment_intent=AssessmentIntent.CALCULATE_VALUE,
        comparison_policy=ComparisonPolicy(
            policy=EvaluationPolicy.INTERVAL_RANGE,
            interval_low=0.15,
            interval_high=0.16,
        ),
    )
    # Interval policies judge membership, not distance to canonical.
    assert values_match(spec, 0.159) is True
    assert values_match(spec, 0.14) is False


def test_significant_figures_policy() -> None:
    spec = AnswerSpecification(
        item_id="sig-1",
        canonical_value=0.159,
        quantity_type=QuantityType.PROBABILITY,
        assessment_intent=AssessmentIntent.CALCULATE_VALUE,
        comparison_policy=ComparisonPolicy(
            policy=EvaluationPolicy.SIGNIFICANT_FIGURES,
            significant_figures=3,
        ),
    )
    assert evaluate(spec, "0.159").value_correct is True
    assert evaluate(spec, "0.158").value_correct is False


def test_custom_domain_rule_policy() -> None:
    clear_custom_domain_rules()

    def _even_near_canonical(
        candidate: float, canonical: float, _spec: AnswerSpecification
    ) -> bool:
        return abs(candidate - canonical) < 1e-9 and candidate % 2 == 0

    register_custom_domain_rule("even-exact", _even_near_canonical)
    try:
        spec = AnswerSpecification(
            item_id="custom-1",
            canonical_value=14.0,
            quantity_type=QuantityType.SCALAR,
            assessment_intent=AssessmentIntent.CALCULATE_VALUE,
            comparison_policy=ComparisonPolicy(
                policy=EvaluationPolicy.CUSTOM_DOMAIN_RULE,
                custom_rule_id="even-exact",
            ),
            representation_policy=RepresentationPolicy(
                accepted_forms=(
                    RepresentationForm.DECIMAL,
                    RepresentationForm.INTEGER,
                ),
            ),
        )
        assert evaluate(spec, "14").value_correct is True
        assert evaluate(spec, "15").value_correct is False
    finally:
        clear_custom_domain_rules()


# ---------------------------------------------------------------------------
# Cross-question invariant
# ---------------------------------------------------------------------------


def test_cross_question_identical_boundary_behaviour_for_shared_policy() -> None:
    """Two questions with the same evaluation policy share boundary behaviour.

    Drawn from live items that both use absolute_tolerance=0.001:
    cs1004-2.1c-cp-01 (0.3297) and cs1006-2.3.1-cp-01 (0.571).
    """
    a = SPEC_QUANTILE
    b = SPEC_CONDITIONAL
    assert a.evaluation_policy is b.evaluation_policy
    assert (
        a.comparison_policy.absolute_tolerance
        == b.comparison_policy.absolute_tolerance
    )

    tol = a.comparison_policy.absolute_tolerance
    assert tol is not None

    # At the inclusive boundary: both must accept.
    assert evaluate(a, f"{a.canonical_value + tol:.10g}").value_correct is True
    assert evaluate(b, f"{b.canonical_value + tol:.10g}").value_correct is True

    # Just outside the same distance: both must reject.
    epsilon = tol * 1e-6 + 1e-12
    assert (
        evaluate(a, f"{a.canonical_value + tol + epsilon:.12g}").value_correct
        is False
    )
    assert (
        evaluate(b, f"{b.canonical_value + tol + epsilon:.12g}").value_correct
        is False
    )

    # Symmetric negative side.
    assert evaluate(a, f"{a.canonical_value - tol:.10g}").value_correct is True
    assert evaluate(b, f"{b.canonical_value - tol:.10g}").value_correct is True
    assert (
        evaluate(a, f"{a.canonical_value - tol - epsilon:.12g}").value_correct
        is False
    )
    assert (
        evaluate(b, f"{b.canonical_value - tol - epsilon:.12g}").value_correct
        is False
    )


def test_cross_question_half_tolerance_premiums() -> None:
    """Shared absolute_tolerance=0.5 boundary invariant across premium items."""
    a = SPEC_PREMIUM
    b = _abs_spec(
        "cs1015-5.1.6-cp-01",
        680.0,
        0.5,
        forms=(RepresentationForm.DECIMAL, RepresentationForm.INTEGER),
    )
    tol = 0.5
    assert evaluate(a, "1110.5").value_correct is True
    assert evaluate(b, "680.5").value_correct is True
    assert evaluate(a, "1110.500001").value_correct is False
    assert evaluate(b, "680.500001").value_correct is False
    assert a.comparison_policy.policy is b.comparison_policy.policy
    assert a.comparison_policy.absolute_tolerance == tol
    assert b.comparison_policy.absolute_tolerance == tol


def test_linear_combination_near_miss() -> None:
    result = evaluate(SPEC_LINEAR_COMB, "16.6")
    assert result.value_correct is True  # |16.6-17| = 0.4 <= 0.5
    result_out = evaluate(SPEC_LINEAR_COMB, "16.4")
    assert result_out.value_correct is False
