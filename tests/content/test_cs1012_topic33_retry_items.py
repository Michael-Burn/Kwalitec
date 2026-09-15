"""Load, score, and distractor-tag checks for CS1 topic 3.3 retry items.

cs1012-3.3.1-ar-02 closes the criterion-3 gap on remaining HT concepts
(simple/composite, sensitivity/specificity, test statistic, likelihood
ratio, critical region and significance level).
cs1012-3.3.2-ar-02 evaluates a one-sample Normal z-test.
cs1012-3.3.3-ar-02 evaluates an exact permutation p-value.
cs1012-3.3.4-ar-02 evaluates a chi-square goodness-of-fit.
cs1012-3.3.5-ar-02 evaluates a contingency independence test.
"""

from __future__ import annotations

import json
from pathlib import Path

from app.application.educational_packages.loader import (
    EducationalPackageLoader,
    reset_educational_package_cache,
)
from app.application.educational_packages.substance import substance_from_package
from app.application.learning_session.educational_flow import EducationalStage
from app.application.learning_session.scoreable_practice import score_practice_response

LIVE_ROOT = Path("app/curriculum/data/educational_packages")

_SPECS = (
    {
        "stem": "3.3.1-hypothesis-concepts-cs1012",
        "item_id": "cs1012-3.3.1-ar-02",
        "objective_id": "CS1-C-T03-LO01",
        "tags": {
            "b": "sens_spec_as_type_errors",
            "c": "composite_as_simple_and_software_region",
            "d": "alpha_as_posterior_and_lr_as_pvalue",
        },
    },
    {
        "stem": "3.3.2-basic-tests-cs1012",
        "item_id": "cs1012-3.3.2-ar-02",
        "objective_id": "CS1-C-T03-LO02",
        "tags": {
            "b": "drop_sqrt_n_in_z",
            "c": "permutation_as_basic_onesample",
            "d": "onesided_tail_as_twosided_p",
        },
    },
    {
        "stem": "3.3.3-permutation-tests-cs1012",
        "item_id": "cs1012-3.3.3-ar-02",
        "objective_id": "CS1-C-T03-LO03",
        "tags": {
            "b": "wrong_permutation_denominator",
            "c": "parametric_as_permutation",
            "d": "bootstrap_ci_as_permutation",
        },
    },
    {
        "stem": "3.3.4-chi-square-gof-cs1012",
        "item_id": "cs1012-3.3.4-ar-02",
        "objective_id": "CS1-C-T03-LO04",
        "tags": {
            "b": "gof_df_forget_minus_one",
            "c": "independence_as_gof",
            "d": "normal_z_as_chisquare_critical",
        },
    },
    {
        "stem": "3.3.5-contingency-independence-cs1012",
        "item_id": "cs1012-3.3.5-ar-02",
        "objective_id": "CS1-C-T03-LO05",
        "tags": {
            "b": "equal_cell_expectations",
            "c": "gof_as_independence",
            "d": "sum_margins_without_n",
        },
    },
)

_PRIOR_LO01_COVERED = (
    "null",
    "alternative",
    "type i",
    "type ii",
    "p-value",
    "power",
)

_CRITERION3_REQUIRED = (
    "simple",
    "composite",
    "sensitivity",
    "specificity",
    "test statistic",
    "likelihood ratio",
    "critical region",
)

# Phrases that must be absent from prior scored text entirely.
_CRITERION3_ABSENT_FROM_PRIOR = (
    "composite",
    "sensitivity",
    "specificity",
    "likelihood ratio",
    "critical region",
)


def setup_function() -> None:
    reset_educational_package_cache()


def _pack(stem: str):
    loader = EducationalPackageLoader(root=LIVE_ROOT)
    packs = [
        p
        for p in loader.all_approved()
        if p.source_path and Path(p.source_path).stem == stem
    ]
    assert packs, f"missing live package {stem}"
    return packs[0]


def _scoreable(stem: str, item_id: str):
    pack = _pack(stem)
    substance = substance_from_package(
        pack,
        curriculum_identity=f"CS1:topic33-retry:{stem}",
        topic_id=pack.topic_code,
    )
    for act in substance.activities:
        if (
            act.stage is EducationalStage.PRACTICE
            and act.scoreable is not None
            and act.scoreable.item_id == item_id
        ):
            return act.scoreable
    raise AssertionError(f"scoreable {item_id} not found in {stem}")


def _assert_item_loads_scores_and_tags(spec: dict) -> None:
    stem = str(spec["stem"])
    item_id = str(spec["item_id"])
    objective_id = str(spec["objective_id"])
    tags = spec["tags"]
    assert isinstance(tags, dict)

    pack = _pack(stem)
    check = next((c for c in pack.knowledge_checks if c.item_id == item_id), None)
    assert check is not None, f"{item_id} did not load from {stem}"
    assert check.response_type == "mcq"
    assert (check.objective_id or "").strip() == objective_id
    assert check.correct_choice_id == "a"
    assert [c.id for c in check.choices] == ["a", "b", "c", "d"]
    assert check.choices[0].misconception_tag == ""
    for choice_id, tag in tags.items():
        match = next(c for c in check.choices if c.id == choice_id)
        assert match.misconception_tag == tag

    item = _scoreable(stem, item_id)
    ok = score_practice_response(item, "a")
    assert ok.scored is True
    assert ok.correct is True
    assert ok.selected_misconception_tag == ""

    for choice_id, tag in tags.items():
        bad = score_practice_response(item, choice_id)
        assert bad.scored is True
        assert bad.correct is False
        assert bad.selected_misconception_tag == tag


def test_cs1012_3_3_1_ar_02_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_SPECS[0])


def test_cs1012_3_3_2_ar_02_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_SPECS[1])


def test_cs1012_3_3_3_ar_02_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_SPECS[2])


def test_cs1012_3_3_4_ar_02_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_SPECS[3])


def test_cs1012_3_3_5_ar_02_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_SPECS[4])


def test_cs1012_3_3_1_ar_02_covers_previously_untested_named_concepts() -> None:
    """Criterion-3 proof: ar-02 scores the named remainder, not ar-01/cp-01 depth."""
    stem = "3.3.1-hypothesis-concepts-cs1012"
    pack = _pack(stem)
    by_id = {c.item_id: c for c in pack.knowledge_checks}

    prior_blob = json.dumps(
        [
            {
                "prompt": by_id["cs1012-3.3.1-ar-01"].prompt,
                "choices": [c.label for c in by_id["cs1012-3.3.1-ar-01"].choices],
                "explanation": by_id["cs1012-3.3.1-ar-01"].explanation,
            },
            {
                "prompt": by_id["cs1012-3.3.1-cp-01"].prompt,
                "choices": [c.label for c in by_id["cs1012-3.3.1-cp-01"].choices],
                "explanation": by_id["cs1012-3.3.1-cp-01"].explanation,
            },
        ]
    ).lower()
    for phrase in _PRIOR_LO01_COVERED:
        assert phrase in prior_blob, f"prior items should still cover {phrase!r}"

    for phrase in _CRITERION3_ABSENT_FROM_PRIOR:
        assert phrase not in prior_blob, (
            f"prior scored items unexpectedly already cover {phrase!r}"
        )

    # "simple" and "test statistic" may appear incidentally in prior distractors
    # or wording; they must still be affirmatively scored on ar-02's correct choice.
    ar02 = by_id["cs1012-3.3.1-ar-02"]
    ar02_blob = json.dumps(
        {
            "prompt": ar02.prompt,
            "choices": [c.label for c in ar02.choices],
            "explanation": ar02.explanation,
        }
    ).lower()
    for phrase in _CRITERION3_REQUIRED:
        assert phrase in ar02_blob, f"ar-02 must score named concept {phrase!r}"

    correct = next(c for c in ar02.choices if c.id == "a").label.lower()
    for phrase in _CRITERION3_REQUIRED:
        assert phrase in correct, (
            f"correct choice must affirmatively name {phrase!r}, not only distractors"
        )

    # Distinct from the already-covered null/alt/Type I/II/p-value/power cluster:
    # ar-02's prompt must ask for the remaining named parts, not restate ar-01.
    prompt_l = ar02.prompt.lower()
    assert "simple" in prompt_l and "composite" in prompt_l
    assert "sensitivity" in prompt_l and "specificity" in prompt_l
    assert "likelihood ratio" in prompt_l
    assert "critical region" in prompt_l
    assert "significance level" in prompt_l
    assert "type i" not in prompt_l
    assert "p-value" not in prompt_l
    assert "power" not in prompt_l
