"""Regression: two sampling-distributions content-quality fixes (cs1009).

1. cs1009-2.6.5-cp-01 refuse-target is a clean, quoted student-facing claim,
   consistent across prompt, correct choice, and model_answer (no authoring
   chrome such as LO / Chapter bleed).
2. cs1009-2.6.6-ar-01 states F has two degrees-of-freedom parameters
   (numerator and denominator), not a vague \"two degrees of freedom\".

Also asserts already-wired choice-aware feedback for both items stays
consistent with the corrected text.
"""

from __future__ import annotations

import json
from pathlib import Path

from app.application.learning_session.choice_aware_feedback_prototype import (
    PROTOTYPE_CHOICE_FEEDBACK,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGES = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"

_REFUSE_CLAIM = (
    'forming the t-statistic completes the F variance-ratio comparison'
)
_QUOTED_REFUSE_CLAIM = f'"{_REFUSE_CLAIM}"'

_ISSUE1_PROMPT = (
    "Closed-book. A Normal sample has unknown population standard deviation. "
    "Which statement gives the correct pivot for $\\mu$ and correctly refuses "
    f"the claim that {_QUOTED_REFUSE_CLAIM}?"
)
_ISSUE1_MODEL_ANSWER = (
    "Use ($\\bar{X}-\\mu$)/($\\frac{S}{\\sqrt{n}}$)~$t_{n-1}$; refuse the claim "
    f"that {_QUOTED_REFUSE_CLAIM}."
)
_ISSUE1_CHOICE = (
    "($\\bar{X}-\\mu$)/($\\frac{S}{\\sqrt{n}}$)~$t_{n-1}$. This supports "
    "inference for $\\mu$, but does not by itself give the F law for comparing "
    f"variances, so the claim that {_QUOTED_REFUSE_CLAIM} is false."
)

_ISSUE2_MODEL_ANSWER = (
    "Scaled ratio of independent Normal-sample variances; two "
    "degrees-of-freedom parameters (numerator and denominator)."
)
_ISSUE2_CHOICE = (
    "An F variable is a ratio of two independent chi-square variables, each "
    "divided by its degrees of freedom. It arises from a scaled ratio of "
    "independent sample variances from Normal populations and has two "
    "degrees-of-freedom parameters (numerator and denominator)."
)

_ISSUE1_CAF = {
    "b": (
        "That choice keeps an exact \\(N(0,1)\\) pivot after using S in place "
        "of \\(\\sigma\\). "
        "With unknown \\(\\sigma\\), \\((\\bar X-\\mu)/(S/\\sqrt{n})\\) is "
        "\\(t_{n-1}\\), not z."
    ),
    "c": (
        "That choice treats S itself as the standard error in "
        "\\((\\bar X-\\mu)/S\\). "
        "The standard error still divides by \\(\\sqrt{n}\\)."
    ),
    "d": (
        "That choice gives \\(S_1^2/S_2^2\\) a \\(t_{n-1}\\) law. "
        "Variance ratios use F, not t; t supports mean pivots."
    ),
}

_ISSUE2_CAF = {
    "b": (
        "That choice defines F as a two-sample mean difference over a pooled "
        "SE. "
        "That construction is a two-sample t pattern, not an F variance-ratio "
        "law."
    ),
    "c": (
        "That choice gives F a single degrees-of-freedom parameter because "
        "sample sizes must match. "
        "F has separate numerator and denominator df."
    ),
    "d": (
        "That choice claims any variance ratio is exactly F even under "
        "dependence or non-Normal parents. "
        "The exact F law needs independence and Normal-sample conditions."
    ),
}

_AUTHORING_CHROME_NEEDLES = (
    "F variance-ratio LO",
    "Chapter 3",
    "The t-statistic finished",
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


def test_issue1_refuse_target_quoted_consistent_across_fields() -> None:
    """Refuse-target is quoted, grammatical, and identical across three fields."""
    item = _kc("2.6.5-t-statistic-cs1009.json", "cs1009-2.6.5-cp-01")
    label = _correct_choice_label(item)

    assert item["prompt"] == _ISSUE1_PROMPT
    assert item["model_answer"] == _ISSUE1_MODEL_ANSWER
    assert label == _ISSUE1_CHOICE

    # Same quoted claim in all three student-facing fields.
    assert _QUOTED_REFUSE_CLAIM in item["prompt"]
    assert _QUOTED_REFUSE_CLAIM in item["model_answer"]
    assert _QUOTED_REFUSE_CLAIM in label
    assert item["prompt"].count(_QUOTED_REFUSE_CLAIM) == 1
    assert item["model_answer"].count(_QUOTED_REFUSE_CLAIM) == 1
    assert label.count(_QUOTED_REFUSE_CLAIM) == 1

    # Grammar: prompt/model_answer use refuse-the-claim; choice closes as false.
    assert 'refuses the claim that "' in item["prompt"]
    assert 'refuse the claim that "' in item["model_answer"]
    assert f'so the claim that {_QUOTED_REFUSE_CLAIM} is false.' in label

    # Underlying statistical content preserved.
    pivot = "($\\bar{X}-\\mu$)/($\\frac{S}{\\sqrt{n}}$)~$t_{n-1}$"
    assert pivot in item["model_answer"]
    assert pivot in label
    assert "does not by itself give the F law for comparing variances" in label

    # Authoring chrome must not bleed unquoted (or at all) into student text.
    for field in (item["prompt"], item["model_answer"], label):
        for needle in _AUTHORING_CHROME_NEEDLES:
            assert needle not in field


def test_issue2_f_distribution_states_two_df_parameters() -> None:
    """Correct choice and model_answer use precise df-parameter phrasing."""
    item = _kc("2.6.6-f-distribution-cs1009.json", "cs1009-2.6.6-ar-01")
    label = _correct_choice_label(item)

    assert item["model_answer"] == _ISSUE2_MODEL_ANSWER
    assert label == _ISSUE2_CHOICE

    precise = "two degrees-of-freedom parameters (numerator and denominator)"
    assert precise in item["model_answer"]
    assert precise in label
    assert "has two degrees of freedom" not in label
    assert "; two degrees of freedom." not in item["model_answer"]

    # Distractor (c) already used the clearer parameter wording; keep alignment.
    distractor_c = next(c for c in item["choices"] if c["id"] == "c")
    assert "degrees-of-freedom parameter" in distractor_c["label"]
    assert "degrees-of-freedom parameter" in label


def test_choice_aware_feedback_remains_consistent_with_corrected_text() -> None:
    """Wired CAF for both items still matches corrected statistical teaching."""
    # Issue 1: CAF never echoed authoring chrome; still teaches F vs t boundary.
    for choice_id, expected in _ISSUE1_CAF.items():
        text = PROTOTYPE_CHOICE_FEEDBACK[("cs1009-2.6.5-cp-01", choice_id)]
        assert text == expected
        for needle in _AUTHORING_CHROME_NEEDLES:
            assert needle not in text
    assert "Variance ratios use F, not t" in _ISSUE1_CAF["d"]

    # Issue 2: CAF (c) already uses degrees-of-freedom parameter language.
    for choice_id, expected in _ISSUE2_CAF.items():
        text = PROTOTYPE_CHOICE_FEEDBACK[("cs1009-2.6.6-ar-01", choice_id)]
        assert text == expected
        assert "has two degrees of freedom" not in text
    assert "degrees-of-freedom parameter" in _ISSUE2_CAF["c"]
    assert "separate numerator and denominator df" in _ISSUE2_CAF["c"]
