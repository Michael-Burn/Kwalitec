"""Regression: three aims/EDA-cluster content-quality fixes.

1. ep001-1.1-cp-01 scores stage order + EDA placement only (not fused
   source-trust / reproducibility warrants).
2. ep001-ca-r1-ar-01 scores three aims with examples only (not fused
   reproducibility), aligned with sibling ep001-1.1-ar-01.
3. cs1017-1.1.3-cp-01 correct choice opens as a complete statement.

Also asserts already-wired choice-aware feedback stays consistent with
the restructured distractors.
"""

from __future__ import annotations

import json
from pathlib import Path

from app.application.learning_session.choice_aware_feedback_prototype import (
    PROTOTYPE_CHOICE_FEEDBACK,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGES = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"

_ISSUE1_CORRECT = (
    "A sensible order is define aim, obtain data, clean/explore, analyse or "
    "predict, then communicate, with EDA in clean/explore."
)
_ISSUE1_DISTRACTORS = {
    "b": (
        "Stages need not be ordered because exploratory work can sit anywhere "
        "in the analysis path."
    ),
    "c": (
        "EDA belongs only after final communication; earlier stages are "
        "optional once results are written up."
    ),
    "d": (
        "The only required stage is software fitting; communication can be "
        "skipped once the model converges."
    ),
}
_ISSUE1_TAGS = {
    "b": "stages_unordered",
    "c": "eda_after_communicate",
    "d": "skip_communicate",
}
_ISSUE1_CAF = {
    "b": (
        "That choice treats stages as unordered so exploratory work can sit "
        "anywhere. "
        "Keep a sensible order and place EDA in clean/explore."
    ),
    "c": (
        "That choice parks EDA after final communication and treats earlier "
        "stages as optional. "
        "EDA sits in clean/explore, before analysis and communication."
    ),
    "d": (
        "That choice makes software fitting the only required stage and skips "
        "communication. "
        "Fitting is one stage; the path still runs through to communicating "
        "results."
    ),
}

_ISSUE2_CORRECT = (
    "Descriptive: summarise claim sizes in a portfolio year. Inferential: "
    "estimate mean claim severity for a population of similar risks. "
    "Predictive: forecast next year's claim count for pricing."
)
_ISSUE2_DISTRACTORS = {
    "b": (
        "The three aims are plotting, computing means, and using software, "
        "illustrated by making a histogram, a sample mean, and an R call."
    ),
    "c": (
        "All three aims collapse into looking at data carefully, so one "
        "example such as 'inspect claims' covers descriptive, inferential, "
        "and predictive work."
    ),
    "d": (
        "Descriptive forecasts next year's claims, inferential summarises "
        "the sample only, and predictive estimates a population mean without "
        "prediction."
    ),
}
_ISSUE2_TAGS = {
    "b": "tools_as_aims",
    "c": "aims_collapsed",
    "d": "aims_swapped",
}
_ISSUE2_CAF = {
    "b": (
        "That choice lists plotting, means, and software as the three aims. "
        "Aims are descriptive, inferential, and predictive purposes; tools "
        "are how you pursue them."
    ),
    "c": (
        "That choice collapses all three aims into one vague inspect-the-data "
        "example. "
        "The three aims stay distinct: summarise a sample, make a population "
        "claim, and forecast unseen outcomes."
    ),
    "d": (
        "That choice swaps the aims: descriptive as forecast, inferential as "
        "sample-only summary, predictive as population mean without "
        "prediction. "
        "Keep each aim matched to its actuarial job."
    ),
}

_ISSUE3_OPENING = "Compare the sources on traits such as"
_ISSUE3_CHOICE = (
    "Compare the sources on traits such as selection or response bias "
    "(survey versus administrative coverage), completeness or granularity of "
    "fields, and measurement error. Large scale may still require sampling "
    "or distributed tooling and does not fix representativeness by itself. "
    "Volume alone is not automatically better data."
)
_ISSUE3_CAF = {
    "b": (
        "That choice crowns the administrative extract for having more rows "
        "and skips source comparison. "
        "Bias and coverage still differ by mechanism; row count is not a "
        "quality certificate."
    ),
    "c": (
        "That choice treats both sources as equally trustworthy in EDA "
        "because trust waits for the final model. "
        "Compare selection, response bias, completeness, and measurement "
        "error up front."
    ),
    "d": (
        "That choice claims a large survey file removes bias because every "
        "respondent row is present. "
        "Including every row in a voluntary file does not fix selection or "
        "response bias."
    ),
}

_FUSED_SOURCE_REPRO_NEEDLES = (
    "sampling bias",
    "granularity",
    "versioned data",
    "scripted",
    "reproducibility",
    "be careful with data",
)
_FUSED_AIMS_REPRO_NEEDLES = (
    "Reproducibility needs",
    "saving the final chart",
    "versioned data and a scripted",
)


def _load(name: str) -> dict:
    return json.loads((PACKAGES / name).read_text(encoding="utf-8"))


def _kc(package_file: str, item_id: str) -> dict:
    data = _load(package_file)
    for item in data["knowledge_checks"]:
        if item["item_id"] == item_id:
            return item
    raise KeyError(item_id)


def _choice(item: dict, choice_id: str) -> dict:
    for choice in item["choices"]:
        if choice["id"] == choice_id:
            return choice
    raise KeyError(choice_id)


def _correct_choice_label(item: dict) -> str:
    return _choice(item, item["correct_choice_id"])["label"]


def test_issue1_stage_order_single_diagnosable_hinge() -> None:
    """ep001-1.1-cp-01 scores stage order + EDA only; one misconception each."""
    item = _kc("1.1-purpose-function-ep001.json", "ep001-1.1-cp-01")
    label = _correct_choice_label(item)

    assert item["prompt"].startswith(
        "Closed-book. Which statement correctly orders the main stages"
    )
    assert "EDA" in item["prompt"]
    assert label == _ISSUE1_CORRECT
    assert "with EDA in clean/explore" in label
    assert "define aim" in label
    assert "communicate" in label

    # Scored choice must not fuse source-trust or reproducibility warrants.
    for needle in _FUSED_SOURCE_REPRO_NEEDLES:
        assert needle not in label

    # Supporting prose may still carry those ideas outside the scored hinge.
    supporting = f"{item['explanation']} {item['model_answer']}"
    assert "sampling bias" in supporting or "granularity" in supporting
    assert "versioned data" in supporting or "reproducibility" in supporting.lower()

    tags = []
    for choice_id, expected_label in _ISSUE1_DISTRACTORS.items():
        choice = _choice(item, choice_id)
        assert choice["label"] == expected_label
        assert choice["misconception_tag"] == _ISSUE1_TAGS[choice_id]
        tags.append(choice["misconception_tag"])
        for needle in _FUSED_SOURCE_REPRO_NEEDLES:
            assert needle not in choice["label"]

    assert len(tags) == len(set(tags))
    assert "need not be ordered" in _ISSUE1_DISTRACTORS["b"]
    assert "after final communication" in _ISSUE1_DISTRACTORS["c"]
    assert "communication can be skipped" in _ISSUE1_DISTRACTORS["d"]


def test_issue2_aims_single_diagnosable_hinge_matches_sibling() -> None:
    """ep001-ca-r1-ar-01 scores aims-with-examples only; matches sibling AR."""
    item = _kc("revision-purpose-eda-ep001.json", "ep001-ca-r1-ar-01")
    sibling = _kc("1.1-purpose-function-ep001.json", "ep001-1.1-ar-01")
    label = _correct_choice_label(item)

    assert "reproducibility element" not in item["prompt"].lower()
    assert label == _ISSUE2_CORRECT
    for needle in _FUSED_AIMS_REPRO_NEEDLES:
        assert needle not in label

    # Supporting prose may still mention reproducibility outside the hinge.
    supporting = f"{item['explanation']} {item['model_answer']}"
    assert "reproducibility" in supporting.lower()

    for choice_id, expected_label in _ISSUE2_DISTRACTORS.items():
        choice = _choice(item, choice_id)
        assert choice["label"] == expected_label
        assert choice["misconception_tag"] == _ISSUE2_TAGS[choice_id]
        for needle in _FUSED_AIMS_REPRO_NEEDLES:
            assert needle not in choice["label"]

    # Sibling topic AR already used the correct single-hinge design.
    assert label == _correct_choice_label(sibling)
    for choice_id in ("b", "c", "d"):
        assert _choice(item, choice_id)["label"] == _choice(sibling, choice_id)["label"]
        assert (
            _choice(item, choice_id)["misconception_tag"]
            == _choice(sibling, choice_id)["misconception_tag"]
        )


def test_issue3_correct_choice_is_complete_grammatical_statement() -> None:
    """cs1017-1.1.3-cp-01 choice a opens with a complete clause, not Examples:."""
    item = _kc("cr-1.1.3-data-sources-cs1017.json", "cs1017-1.1.3-cp-01")
    label = _correct_choice_label(item)

    assert label == _ISSUE3_CHOICE
    assert label.startswith(_ISSUE3_OPENING)
    assert not label.startswith("Examples:")
    assert "selection or response bias" in label
    assert "completeness or granularity" in label
    assert "measurement error" in label
    assert "does not fix representativeness" in label
    assert "Volume alone is not automatically better data" in label


def test_choice_aware_feedback_consistent_with_restructured_hinges() -> None:
    """Wired CAF for all three items matches the restructured misconceptions."""
    for choice_id, expected in _ISSUE1_CAF.items():
        text = PROTOTYPE_CHOICE_FEEDBACK[("ep001-1.1-cp-01", choice_id)]
        assert text == expected
        for needle in ("source traits", "reproducibility", "be careful with data"):
            assert needle not in text

    for choice_id, expected in _ISSUE2_CAF.items():
        text = PROTOTYPE_CHOICE_FEEDBACK[("ep001-ca-r1-ar-01", choice_id)]
        assert text == expected
        assert "reproducibility" not in text.lower()
        assert "final chart" not in text

    for choice_id, expected in _ISSUE3_CAF.items():
        text = PROTOTYPE_CHOICE_FEEDBACK[("cs1017-1.1.3-cp-01", choice_id)]
        assert text == expected
