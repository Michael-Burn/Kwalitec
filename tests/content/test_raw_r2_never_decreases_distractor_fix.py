"""Regression: raw R-squared distractor states the true monotonic fact.

cs1003-4.1.5-cp-01 and twin cs1013-4.1.5-cp-01 distractor (d) previously
claimed raw R-squared "never increases" when variables are added. The correct
fact is that raw R-squared never decreases (it stays the same or increases),
which is why it is a poor complexity penalty on its own.

Choice-aware feedback for (d) already taught "never decreases"; this fix
brings the visible option text into agreement with that feedback.
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

_CORRECTED_DISTRACTOR_D = (
    "Raw R-squared alone decides between M1 and M2 because it never decreases "
    "when variables are added."
)

_CAF_D = (
    "That choice lets raw R-squared alone decide because it never decreases "
    "when variables are added. "
    "Raw R-squared never decreases when you add variables, which is why it is "
    "a poor complexity penalty; prefer adjusted R², AIC, or BIC."
)

_ITEMS = (
    ("4.1.5-variable-selection-cs1003.json", "cs1003-4.1.5-cp-01"),
    ("4.1.5-variable-selection-cs1013.json", "cs1013-4.1.5-cp-01"),
)


def _load(name: str) -> dict:
    return json.loads((PACKAGES / name).read_text(encoding="utf-8"))


def _choice_label(package_file: str, item_id: str, choice_id: str) -> str:
    data = _load(package_file)
    for item in data["knowledge_checks"]:
        if item["item_id"] == item_id:
            for choice in item["choices"]:
                if choice["id"] == choice_id:
                    return choice["label"]
            raise KeyError(choice_id)
    raise KeyError(item_id)


@pytest.mark.parametrize(("package_file", "item_id"), _ITEMS)
def test_distractor_d_states_raw_r2_never_decreases(
    package_file: str, item_id: str
) -> None:
    """Corrected option text states the true fact, not the inverted one."""
    label = _choice_label(package_file, item_id, "d")
    assert label == _CORRECTED_DISTRACTOR_D
    assert "never decreases when variables are added" in label
    assert "never increases when variables are added" not in label


@pytest.mark.parametrize(("package_file", "item_id"), _ITEMS)
def test_distractor_d_option_and_choice_aware_feedback_agree(
    package_file: str, item_id: str
) -> None:
    """Option (d) and wired CAF (d) both hinge on never decreases."""
    label = _choice_label(package_file, item_id, "d")
    feedback = PROTOTYPE_CHOICE_FEEDBACK[(item_id, "d")]
    assert label == _CORRECTED_DISTRACTOR_D
    assert feedback == _CAF_D
    assert "never decreases" in label
    assert "never decreases" in feedback
    assert "never increases" not in label
    assert "never increases" not in feedback
    # Option premise and feedback restatement share the same true fact.
    assert "never decreases when variables are added" in label
    assert "never decreases when variables are added" in feedback
