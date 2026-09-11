"""Regression: Bayesian credibility AR twins attribute Z correctly.

mu and k come from the prior/structural model; Z = n/(n+k) also depends
on the amount of individual experience. Choice-aware feedback for the
same items must stay consistent with that attribution.
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

_CS1003_CHOICE = (
    "Specify a prior or structural distribution for risk parameters; "
    "update with data to a posterior; in a simple case the credibility "
    "premium takes the form Z times $\\bar{X}$ + (1 minus Z) times "
    "$\\mu$ with $\\mu$ and $k$ from the prior structure; "
    "$Z = n/(n+k)$ from that structure together with the amount of "
    "individual experience."
)
_CS1003_MODEL_ANSWER = (
    "Prior, update to posterior, credibility premium Z $\\bar{X}$ + "
    "(1-Z) $\\mu$ with $\\mu$ and $k$ from structure; $Z = n/(n+k)$."
)

_CS1015_CHOICE = (
    "Bayesian credibility uses an explicit prior or structural "
    "distribution for risk parameters. The premium object is Z times "
    "$\\bar{X}$ + (1 minus Z) times $\\mu$ with mu and k from the "
    "prior structure; Z = n/(n+k) from that structure together with "
    "the amount of individual experience in simple cases."
)
_CS1015_MODEL_ANSWER = (
    "Prior structure supplies $\\mu$ and $k$; $Z = n/(n+k)$ with "
    "individual experience; premium $Z\\bar{X} + (1 - Z)\\mu$."
)

_OLD_PHRASES = (
    "determined from the prior structure",
    "determined theoretically from the prior structure",
    "supplies mu and Z",
    "Z and mu from the prior structure",
)

_CAF_KEYS: tuple[tuple[str, str], ...] = (
    ("cs1003-5.1.7-ar-01", "d"),
    ("cs1015-5.1.7-ar-01", "c"),
    ("cs1015-5.1.7-ar-01", "d"),
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
    ("package_file", "item_id", "expected_label", "expected_model"),
    [
        (
            "5.1.7-bayesian-credibility-cs1003.json",
            "cs1003-5.1.7-ar-01",
            _CS1003_CHOICE,
            _CS1003_MODEL_ANSWER,
        ),
        (
            "5.1.7-bayesian-credibility-cs1015.json",
            "cs1015-5.1.7-ar-01",
            _CS1015_CHOICE,
            _CS1015_MODEL_ANSWER,
        ),
    ],
)
def test_correct_choice_attributes_z_to_structure_plus_experience(
    package_file: str,
    item_id: str,
    expected_label: str,
    expected_model: str,
) -> None:
    item = _kc(package_file, item_id)
    label = _correct_choice_label(item)
    assert label == expected_label
    assert "from the prior structure" in label
    assert "Z = n/(n+k)" in label or "$Z = n/(n+k)$" in label
    assert "individual experience" in label
    for phrase in _OLD_PHRASES[:2]:
        assert phrase not in label
    assert item["model_answer"] == expected_model
    assert "Z = n/(n+k)" in item["model_answer"] or (
        "$Z = n/(n+k)$" in item["model_answer"]
    )


def test_choice_aware_feedback_consistent_with_z_attribution() -> None:
    for key in _CAF_KEYS:
        text = PROTOTYPE_CHOICE_FEEDBACK[key]
        assert "mu and k" in text
        assert "Z = n/(n+k)" in text
        assert "individual experience" in text
        for phrase in _OLD_PHRASES[2:]:
            assert phrase not in text
        assert "supplies mu and Z" not in text
        assert "Z and mu from the prior structure" not in text
        assert "determined from the prior structure" not in text
        assert "determined theoretically from the prior structure" not in text
