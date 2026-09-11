"""Regression: five SME-confirmed precision wording fixes (final audit close-out).

A/B. Independence check is unrestricted (for all pairs), not joint-support-only.
C. Continuous-safe conditional: joint probability or density over conditioning marginal.
D. General quantile: smallest x with F(x) at least p (generalized inverse).
E. Discrete inverse transform: CDF first at least U (non-strict).

Also asserts already-wired choice-aware feedback stays consistent with the
corrected teaching lines.
"""

from __future__ import annotations

import json
from pathlib import Path

from app.application.learning_session.choice_aware_feedback_prototype import (
    PROTOTYPE_CHOICE_FEEDBACK,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGES = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"

_SIBLING_CONDITIONAL_FRAGMENT = (
    "dividing the relevant joint probability or density by the marginal "
    "of the conditioning value"
)

_ISSUE_A_CHOICE = (
    "X and Y are independent if the joint equals the product of the "
    "marginals for all (x, y) (or an equivalent form such as conditional "
    "equals marginal)."
)
_ISSUE_A_MODEL_ANSWER = (
    "Joint equals product of marginals for all (x, y) "
    "(or equivalent conditional-equals-marginal form)."
)

_ISSUE_B_CHOICE = "pX,Y(x, y) = pX(x)pY(y) for all possible pairs."
_ISSUE_B_MODEL_ANSWER = (
    "Verify pX,Y(x,y) = pX(x)pY(y) for all possible pairs."
)

_ISSUE_C_CHOICE = (
    "A marginal sums or integrates the joint over the other variable(s). "
    "A conditional renormalises the joint on the given condition, "
    "dividing the relevant joint probability or density by the marginal "
    "of the conditioning value."
)
_ISSUE_C_EXPLANATION = (
    "Marginals sum/integrate out partners; conditionals divide the relevant "
    "joint probability or density by the marginal of the conditioning value. "
    "Skipping extraction or omitting normalisation confuses joint with "
    "margin or conditional."
)
_ISSUE_C_MODEL_ANSWER = (
    "Marginal: sum/integrate joint; conditional: joint probability or "
    "density divided by the conditioning marginal."
)

_ISSUE_D_CHOICE = (
    "For a placed univariate family, evaluate a probability such as "
    "$P(X > x)$ from the CDF or survival function, and evaluate a quantile "
    "as the smallest x such that F(x) is at least p (which reduces to "
    "solving F(x) = p when the CDF is continuous)."
)
_ISSUE_D_MODEL_ANSWER = (
    "Use CDF/survival for probabilities; quantile is the smallest x with "
    "F(x) at least p (generalized inverse) on a named univariate family."
)

_ISSUE_E_CHOICE = (
    "Draw U ~ Uniform(0,1) and assign the discrete value whose CDF is "
    "first at least U (inverse CDF or threshold rule). Software sampling "
    "can implement the draw, but the learning objective requires "
    "understanding inverse transform, not only calling a black box."
)

_ISSUE_A_CAF_D = (
    "That choice stops once each marginal exists and drops the "
    "joint-factorisation requirement. "
    "Independence still needs the joint to equal the product of those "
    "marginals for all (x, y)."
)
_ISSUE_B_CAF_B = (
    "That choice treats Cov(X,Y) = 0 as independence in every case. "
    "Independence needs joint factorisation everywhere; zero covariance "
    "is generally insufficient."
)
_ISSUE_C_CAF_D = (
    "That choice forms every marginal and conditional by dividing each "
    "joint cell by the grand total. "
    "A marginal sums over partners; a conditional divides by the marginal "
    "of the conditioning value, not by a single grand-total rescaling "
    "rule for both."
)

_SUPPORT_BANLIST = (
    "in the support",
    "on the support",
    "joint support",
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


def test_issues_a_and_b_unrestricted_independence_check() -> None:
    """A/B: unrestricted joint=product check; choice/explanation/model_answer agree."""
    item_a = _kc("2.2.2-independence-cs1005.json", "cs1005-2.2.2-ar-01")
    label_a = _correct_choice_label(item_a)
    assert label_a == _ISSUE_A_CHOICE
    assert item_a["model_answer"] == _ISSUE_A_MODEL_ANSWER
    assert "for all (x, y)" in label_a
    assert "for all (x, y)" in item_a["model_answer"]
    for field in (label_a, item_a["model_answer"], item_a["explanation"]):
        for needle in _SUPPORT_BANLIST:
            assert needle not in field

    item_b = _kc(
        "revision-joint-distributions-cs1005.json", "cs1005-ce-r1-ar-01"
    )
    label_b = _correct_choice_label(item_b)
    assert label_b == _ISSUE_B_CHOICE
    assert item_b["model_answer"] == _ISSUE_B_MODEL_ANSWER
    assert "for all possible pairs" in label_b
    assert "for all possible pairs" in item_b["model_answer"]
    assert "everywhere" in item_b["explanation"]
    for field in (label_b, item_b["model_answer"], item_b["explanation"]):
        for needle in _SUPPORT_BANLIST:
            assert needle not in field


def test_issue_c_conditional_allows_probability_or_density() -> None:
    """C: sibling phrasing for joint probability or density / conditioning marginal."""
    sibling = _kc(
        "2.2.1-marginal-conditional-cs1005.json", "cs1005-2.2.1-ar-01"
    )
    sibling_label = _correct_choice_label(sibling)
    assert _SIBLING_CONDITIONAL_FRAGMENT in sibling_label

    item = _kc(
        "cp-2.2.1-marginal-conditional-cs1016.json", "cs1016-2.2.1-ar-01"
    )
    label = _correct_choice_label(item)
    assert label == _ISSUE_C_CHOICE
    assert item["explanation"] == _ISSUE_C_EXPLANATION
    assert item["model_answer"] == _ISSUE_C_MODEL_ANSWER
    assert _SIBLING_CONDITIONAL_FRAGMENT in label
    assert (
        "divide the relevant joint probability or density by the marginal "
        "of the conditioning value"
    ) in item["explanation"]
    assert "joint probability or density" in item["model_answer"]
    assert "conditioning marginal" in item["model_answer"]
    assert "marginal probability of that condition" not in label
    assert "conditioning event's probability" not in item["explanation"]
    assert "$P(condition)$" not in item["model_answer"]


def test_issue_d_general_quantile_definition() -> None:
    """D: generalized inverse (smallest x with F(x) at least p)."""
    item = _kc("cp-2.1.3-prob-quantiles-cs1016.json", "cs1016-2.1.3-ar-01")
    label = _correct_choice_label(item)
    assert label == _ISSUE_D_CHOICE
    assert item["model_answer"] == _ISSUE_D_MODEL_ANSWER
    assert "smallest x such that F(x) is at least p" in label
    assert "smallest x with F(x) at least p" in item["model_answer"]
    assert "generalized inverse" in item["model_answer"]
    assert "inverting the CDF to solve F(x) = p for x" not in label
    assert "invert CDF for quantiles" not in item["model_answer"]


def test_issue_e_discrete_inverse_transform_non_strict() -> None:
    """E: first CDF value at least U (non-strict), not first exceeds."""
    item = _kc("2.1.5-inverse-transform-cs1004.json", "cs1004-2.1e-cp-01")
    label = _correct_choice_label(item)
    assert label == _ISSUE_E_CHOICE
    assert "CDF is first at least U" in label
    assert "first exceeds U" not in label


def test_choice_aware_feedback_remains_consistent_with_corrected_text() -> None:
    """Wired CAF for these five items stays aligned with corrected teaching."""
    assert (
        PROTOTYPE_CHOICE_FEEDBACK[("cs1005-2.2.2-ar-01", "d")] == _ISSUE_A_CAF_D
    )
    assert "on the support" not in PROTOTYPE_CHOICE_FEEDBACK[
        ("cs1005-2.2.2-ar-01", "d")
    ]
    assert "for all (x, y)" in PROTOTYPE_CHOICE_FEEDBACK[
        ("cs1005-2.2.2-ar-01", "d")
    ]

    assert (
        PROTOTYPE_CHOICE_FEEDBACK[("cs1005-ce-r1-ar-01", "b")] == _ISSUE_B_CAF_B
    )
    assert "on the support" not in PROTOTYPE_CHOICE_FEEDBACK[
        ("cs1005-ce-r1-ar-01", "b")
    ]
    assert "everywhere" in PROTOTYPE_CHOICE_FEEDBACK[
        ("cs1005-ce-r1-ar-01", "b")
    ]

    assert (
        PROTOTYPE_CHOICE_FEEDBACK[("cs1016-2.2.1-ar-01", "d")] == _ISSUE_C_CAF_D
    )
    assert "conditioning event" not in PROTOTYPE_CHOICE_FEEDBACK[
        ("cs1016-2.2.1-ar-01", "d")
    ]
    assert "marginal of the conditioning value" in PROTOTYPE_CHOICE_FEEDBACK[
        ("cs1016-2.2.1-ar-01", "d")
    ]

    for choice_id in ("b", "c", "d"):
        text = PROTOTYPE_CHOICE_FEEDBACK[("cs1016-2.1.3-ar-01", choice_id)]
        assert "solve F(x) = p for x" not in text
        assert "inverting the CDF to solve" not in text

    for choice_id in ("b", "c", "d"):
        text = PROTOTYPE_CHOICE_FEEDBACK[("cs1004-2.1e-cp-01", choice_id)]
        assert "first exceeds" not in text
