"""Regression: three confirmed GLM 4.2 correctness fixes (cs1003/cs1014 twins).

1. Deviance definition choice uses unambiguous parenthesized form.
2. Nested deviance comparison hedges with regularity / same-scale treatment.
3. Deviance residual is signed square root of the contribution (not the contribution).

Also asserts already-wired choice-aware feedback for the residual items stays
consistent with the corrected definition.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.application.learning_session.choice_aware_feedback_prototype import (
    PROTOTYPE_CHOICE_FEEDBACK,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGES = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"

# Issue 1: unambiguous parenthesized deviance formula in choice (a).
_ISSUE1_CHOICE = (
    "Deviance compares the fitted model's log-likelihood to a saturated model "
    "(2 times the quantity $\\ell$_sat minus $\\ell$_model). Scaled deviance "
    "divides by dispersion or scale when relevant. Parameters are typically "
    "estimated by maximum likelihood (often via IWLS). Mechanical p-value "
    "chopping is model-choice behaviour, not deviance definition."
)
_ISSUE1_MODEL_ANSWER = (
    "Deviance 2($\\ell$_sat - $\\ell$_model); scaled divides by scale; "
    "MLE/IWLS. Refuse p-chopping."
)

# Issue 2: regularity / same-scale hedges matching cs1014-cx-r1-cp-01 approach.
_ISSUE2_CHOICE = (
    "Under suitable regularity conditions (same response family and scale "
    "treatment), compare deviance (or $-2\\Delta\\ell$) between nested models "
    "against an asymptotic chi-squared reference on the degrees-of-freedom "
    "difference; also inspect whether added parameters are statistically and "
    "scientifically warranted. Residual plots are diagnostics, not nested "
    "model comparison. Model choice here uses analysis of deviance and "
    "parameter significance."
)
_ISSUE2_EXPLANATION = (
    "For appropriate nested GLMs with the same family and scale treatment, "
    "deviance difference is a likelihood-ratio statistic, often asymptotically "
    "chi-squared. Residual plotting and p-only rules do not replace analysis "
    "of deviance."
)

# Issue 3: signed square root of the deviance contribution.
_ISSUE3_CHOICE = (
    "Pearson residual uses observed minus fitted scaled by the variance "
    "structure: $(y - \\hat{\\mu})$ over $\\sqrt{\\widehat{\\operatorname{Var}}(Y)}$. "
    "Deviance residual is $\\operatorname{sign}(y - \\hat{\\mu})$ times the "
    "square root of observation i's contribution to deviance. Both help check "
    "fit, outliers, and patterns."
)
_ISSUE3_MODEL_ANSWER = (
    "Pearson: standardised $\\frac{y-\\hat{\\mu}}{\\sqrt{\\operatorname{Var}}}$; "
    "deviance: $\\operatorname{sign}(y-\\hat{\\mu})\\sqrt{d}$."
)

# CAF distractor (c) already states the precise signed-square-root definition.
_ISSUE3_CAF_C_NEEDLE = (
    "deviance residuals come from the signed square root of the "
    "observation’s deviance contribution."
)


def _load(name: str) -> dict:
    return json.loads((PACKAGES / name).read_text(encoding="utf-8"))


def _kc(package_file: str, item_id: str) -> dict:
    data = _load(package_file)
    for item in data["knowledge_checks"]:
        if item["item_id"] == item_id:
            return item
    raise KeyError(item_id)


def _correct_choice_label(item: dict) -> str:
    correct_id = item["correct_choice_id"]
    for choice in item["choices"]:
        if choice["id"] == correct_id:
            return choice["label"]
    raise KeyError(correct_id)


@pytest.mark.parametrize(
    ("package_file", "item_id"),
    [
        ("4.2.6-deviance-estimation-cs1003.json", "cs1003-4.2.6-cp-01"),
        ("4.2.6-deviance-estimation-cs1014.json", "cs1014-4.2.6-cp-01"),
    ],
)
def test_issue1_deviance_formula_choice_matches_model_answer(
    package_file: str, item_id: str
) -> None:
    item = _kc(package_file, item_id)
    label = _correct_choice_label(item)
    assert label == _ISSUE1_CHOICE
    assert "2 times the quantity $\\ell$_sat minus $\\ell$_model" in label
    assert "2 times $\\ell$_sat minus $\\ell$_model" not in label
    assert item["model_answer"] == _ISSUE1_MODEL_ANSWER
    assert "2($\\ell$_sat - $\\ell$_model)" in item["model_answer"]


@pytest.mark.parametrize(
    ("package_file", "item_id"),
    [
        ("4.2.7-model-choice-cs1003.json", "cs1003-4.2.7-cp-01"),
        ("4.2.7-model-choice-cs1014.json", "cs1014-4.2.7-cp-01"),
    ],
)
def test_issue2_nested_deviance_has_regularity_scale_hedge(
    package_file: str, item_id: str
) -> None:
    item = _kc(package_file, item_id)
    label = _correct_choice_label(item)
    assert label == _ISSUE2_CHOICE
    assert "Under suitable regularity conditions" in label
    assert "same response family and scale treatment" in label
    assert "asymptotic chi-squared reference" in label
    assert item["explanation"] == _ISSUE2_EXPLANATION
    assert "often asymptotically chi-squared" in item["explanation"]


@pytest.mark.parametrize(
    ("package_file", "item_id"),
    [
        ("4.2.8-residuals-cs1003.json", "cs1003-4.2.8-ar-01"),
        ("4.2.8-residuals-cs1014.json", "cs1014-4.2.8-ar-01"),
    ],
)
def test_issue3_deviance_residual_is_signed_square_root(
    package_file: str, item_id: str
) -> None:
    item = _kc(package_file, item_id)
    label = _correct_choice_label(item)
    assert label == _ISSUE3_CHOICE
    assert (
        "$\\operatorname{sign}(y - \\hat{\\mu})$ times the square root of "
        "observation i's contribution to deviance"
    ) in label
    assert "signed contribution of observation i to deviance" not in label
    assert item["model_answer"] == _ISSUE3_MODEL_ANSWER
    assert "$\\operatorname{sign}(y-\\hat{\\mu})\\sqrt{d}$" in item["model_answer"]
    assert "signed deviance contribution" not in item["model_answer"]


@pytest.mark.parametrize(
    "item_id",
    ["cs1003-4.2.8-ar-01", "cs1014-4.2.8-ar-01"],
)
def test_issue3_choice_aware_feedback_matches_signed_square_root(
    item_id: str,
) -> None:
    """Distractor (c) CAF already teaches the precise residual form."""
    feedback = PROTOTYPE_CHOICE_FEEDBACK[(item_id, "c")]
    assert _ISSUE3_CAF_C_NEEDLE in feedback
    assert "signed contribution of observation i to deviance" not in feedback
    # No CAF entry should still teach the imprecise residual-as-contribution form.
    for choice_id in ("b", "c", "d"):
        text = PROTOTYPE_CHOICE_FEEDBACK[(item_id, choice_id)]
        assert "signed contribution of observation i to deviance" not in text
        assert "signed deviance contribution" not in text
