"""Prove Tier-2 diagnostic wiring for the 18 newly authored numeric rules.

Loads live Answer Specifications from package JSON. Asserts:
1. Each authored match_value yields Tier-2 with the expected rule and clause.
2. Each item's own correct answer stays Tier-1 with no diagnostic match.
3. Previously refused ambiguous values stay undiagnosed (no false Tier-2).
"""

from __future__ import annotations

import pytest

from app.application.numeric_assessment import (
    FeedbackTier,
    evaluate,
    load_live_answer_specifications,
    reset_live_answer_specification_cache,
)

# Primary rules wired in this milestone (one per item).
# Columns: item_id, match_value, match_absolute_tolerance, rule_id, consistent_with
TIER2_RULES: list[tuple[str, float, float, str, str]] = [
    (
        "cs1004-cgr1-cp-01",
        0.6020,
        0.0001,
        "used-u-not-one-minus-u",
        "using -ln(U)/lambda instead of -ln(1-U)/lambda at this U",
    ),
    (
        "cs1005-2.2.1-cp-01",
        0.4,
        0.001,
        "joint-without-normalising",
        "reporting the joint cell P(1,1) without dividing by P(X=1)",
    ),
    (
        "cs1005-2.2.3-cp-01",
        0.4,
        0.001,
        "exy-without-centring",
        "reporting E[XY] without subtracting E[X]E[Y]",
    ),
    (
        "cs1005-2.2.4-cp-01",
        25,
        0.5,
        "dropped-covariance",
        "dropping the covariance cross-term",
    ),
    (
        "cs1006-2.3.1-cp-01",
        0.4,
        0.001,
        "unnormalised-conditional-mean",
        "using the unnormalised X=1 slice instead of dividing by P(X=1)",
    ),
    (
        "cs1006-2.3.2-cp-01",
        15,
        0.5,
        "unweighted-conditional-means",
        "averaging the conditional means without probability weights",
    ),
    (
        "cs1008-2.5.1-cp-01",
        0.841,
        0.001,
        "reported-phi-of-plus-one",
        "reporting Phi(1) approximately 0.841 instead of the lower-tail "
        "value 1 minus Phi(1)",
    ),
    (
        "cs1010-3.1.1-cp-01",
        11000,
        0.5,
        "reported-sum-not-mean",
        "reporting the sum of observations instead of the sample mean",
    ),
    (
        "cs1010-3.1.2-cp-01",
        2.5,
        0.001,
        "reported-mean-not-rate",
        "reporting the sample mean instead of the rate lambda-hat equals n "
        "divided by the sum of x",
    ),
    (
        "cs1010-3.1.6-cp-01",
        9.618,
        0.001,
        "used-bessel-correction",
        "using 1 divided by (B minus 1) instead of 1 divided by B in the "
        "bootstrap standard error",
    ),
    (
        "cs1014-4.2.10-cp-01",
        0.2,
        0.001,
        "raw-coefficient",
        "reporting the log-link coefficient instead of the multiplicative "
        "factor e to the beta-hat",
    ),
    (
        "cs1015-5.1.7-cp-01",
        750,
        0.5,
        "swapped-weights",
        "swapping the credibility weights",
    ),
    (
        "cs1015-5.1.8-cp-01",
        633.33,
        0.01,
        "swapped-weights",
        "swapping the credibility weights",
    ),
    (
        "cs1016-2.1.3-cp-01",
        0.865,
        0.001,
        "cdf-instead-of-survival",
        "reporting the CDF instead of the survival probability",
    ),
    (
        "cs1016-2.2.1-cp-01",
        0.4,
        0.001,
        "joint-without-normalising",
        "reporting the joint cell P(1,1) without dividing by P(X=1)",
    ),
    (
        "cs1016-2.5.1-cp-01",
        0.841,
        0.001,
        "reported-phi-of-plus-one",
        "reporting Phi(1) approximately 0.841 instead of the lower-tail "
        "value 1 minus Phi(1)",
    ),
    (
        "cs1016-3.1.1-cp-01",
        12,
        0,
        "reported-sum-not-mean",
        "reporting the sum of counts instead of the sample mean",
    ),
    (
        "cs1016-5.1.1-cp-01",
        0.95,
        0.001,
        "sensitivity-as-posterior",
        "equating the posterior with the sensitivity P(positive given D)",
    ),
]

CORRECT_ANSWERS: dict[str, str] = {
    "cs1004-cgr1-cp-01": "0.1783",
    "cs1005-2.2.1-cp-01": "0.571",
    "cs1005-2.2.3-cp-01": "0.05",
    "cs1005-2.2.4-cp-01": "17",
    "cs1006-2.3.1-cp-01": "0.571",
    "cs1006-2.3.2-cp-01": "14",
    "cs1008-2.5.1-cp-01": "0.159",
    "cs1010-3.1.1-cp-01": "2200",
    "cs1010-3.1.2-cp-01": "0.4",
    "cs1010-3.1.6-cp-01": "8.602",
    "cs1014-4.2.10-cp-01": "1.2214",
    "cs1015-5.1.7-cp-01": "800",
    "cs1015-5.1.8-cp-01": "566.67",
    "cs1016-2.1.3-cp-01": "0.135",
    "cs1016-2.2.1-cp-01": "0.571",
    "cs1016-2.5.1-cp-01": "0.159",
    "cs1016-3.1.1-cp-01": "2",
    "cs1016-5.1.1-cp-01": "0.0876",
}

# Values the adversarial draft explicitly declined to author.
REFUSED_AMBIGUOUS: list[tuple[str, str]] = [
    ("cs1005-2.2.1-cp-01", "0.667"),
    ("cs1006-2.3.1-cp-01", "0.667"),
    ("cs1016-2.2.1-cp-01", "0.667"),
    ("cs1005-2.2.4-cp-01", "9"),
    ("cs1008-2.5.1-cp-01", "0.434"),
    ("cs1016-2.5.1-cp-01", "0.434"),
    ("cs1016-5.1.1-cp-01", "0.0868"),
]


@pytest.fixture(autouse=True)
def _reset_catalogue_cache() -> None:
    reset_live_answer_specification_cache()


@pytest.mark.parametrize(
    ("item_id", "match_value", "match_tol", "rule_id", "consistent_with"),
    TIER2_RULES,
    ids=[row[0] for row in TIER2_RULES],
)
def test_tier2_match_value_produces_authored_diagnostic(
    item_id: str,
    match_value: float,
    match_tol: float,
    rule_id: str,
    consistent_with: str,
) -> None:
    specs = load_live_answer_specifications()
    spec = specs[item_id]
    assert len(spec.diagnostic_rules) == 1
    rule = spec.diagnostic_rules[0]
    assert rule.rule_id == rule_id
    assert rule.match_value == pytest.approx(match_value)
    assert rule.match_absolute_tolerance == pytest.approx(match_tol)
    assert rule.consistent_with == consistent_with

    result = evaluate(spec, f"{match_value}")
    assert result.value_correct is False
    assert result.feedback_tier is FeedbackTier.TIER_2
    assert result.matched_diagnostic_rule_id == rule_id
    assert "Consistent with" in result.feedback_message
    assert consistent_with in result.feedback_message
    assert "you did" not in result.feedback_message.lower()


@pytest.mark.parametrize(
    ("item_id", "match_value", "match_tol", "rule_id", "consistent_with"),
    TIER2_RULES,
    ids=[row[0] for row in TIER2_RULES],
)
def test_correct_answer_stays_tier1_without_diagnostic(
    item_id: str,
    match_value: float,
    match_tol: float,
    rule_id: str,
    consistent_with: str,
) -> None:
    del match_value, match_tol, rule_id, consistent_with
    specs = load_live_answer_specifications()
    spec = specs[item_id]
    accepted = CORRECT_ANSWERS[item_id]
    result = evaluate(spec, accepted)
    assert result.value_correct is True
    assert result.fully_correct is True
    assert result.feedback_tier is FeedbackTier.TIER_1
    assert result.matched_diagnostic_rule_id is None
    assert "Consistent with" not in result.feedback_message


@pytest.mark.parametrize(
    ("item_id", "refused_value"),
    REFUSED_AMBIGUOUS,
    ids=[f"{item}-{value}" for item, value in REFUSED_AMBIGUOUS],
)
def test_refused_ambiguous_values_do_not_false_diagnose(
    item_id: str,
    refused_value: str,
) -> None:
    """Declined candidates must never match a Tier-2 rule.

    Most are incorrect and must fall through to Tier-3. The Bayes near-miss
    0.0868 may score correct under absolute_tolerance 0.001; either way it
    must not trigger a false diagnostic.
    """
    specs = load_live_answer_specifications()
    spec = specs[item_id]
    result = evaluate(spec, refused_value)
    assert result.matched_diagnostic_rule_id is None
    assert "Consistent with" not in result.feedback_message
    if result.value_correct:
        assert result.feedback_tier is FeedbackTier.TIER_1
    else:
        assert result.feedback_tier is FeedbackTier.TIER_3
        assert "cannot determine the specific calculation error" in (
            result.feedback_message
        )
