"""Load, score, and distractor-tag checks for CS1 topic 3.2 retry items.

cs1011-3.2.1-ar-02 evaluates a parameter z-interval and refuses prediction reading.
cs1011-3.2.2-ar-02 evaluates a prediction interval and refuses mean-CI-as-prediction.
cs1011-3.2.3-ar-02 inverts a given sampling distribution and refuses cookbook /√n.
cs1011-3.2.4-ar-02 evaluates a Normal mean t-interval and keeps the variance form.
cs1011-3.2.5-ar-02 evaluates binomial and Poisson Normal-approx CIs.
cs1011-3.2.6-ar-02 evaluates a two-sample CI and refuses equal-n-as-paired.
cs1011-3.2.7-ar-02 evaluates a paired-difference CI and refuses two-sample-on-paired.
cs1011-3.2.8-ar-02 reads percentile bootstrap endpoints and refuses SE-only.
"""

from __future__ import annotations

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
        "stem": "3.2.1-confidence-interval-parameter-cs1011",
        "item_id": "cs1011-3.2.1-ar-02",
        "objective_id": "CS1-C-T02-LO01",
        "tags": {
            "b": "forget_sqrt_n",
            "c": "prediction_as_ci",
            "d": "bayesian_reading",
        },
    },
    {
        "stem": "3.2.2-prediction-interval-cs1011",
        "item_id": "cs1011-3.2.2-ar-02",
        "objective_id": "CS1-C-T02-LO02",
        "tags": {
            "b": "mean_ci_as_prediction",
            "c": "drop_process_variance",
            "d": "targets_swapped",
        },
    },
    {
        "stem": "3.2.3-ci-given-sampling-distribution-cs1011",
        "item_id": "cs1011-3.2.3-ar-02",
        "objective_id": "CS1-C-T02-LO03",
        "tags": {
            "b": "normal_cookbook_always",
            "c": "invent_sqrt_n",
            "d": "drop_estimate",
        },
    },
    {
        "stem": "3.2.4-ci-normal-mean-variance-cs1011",
        "item_id": "cs1011-3.2.4-ar-02",
        "objective_id": "CS1-C-T02-LO04",
        "tags": {
            "b": "z_not_t_and_skip_var",
            "c": "same_interval",
            "d": "normal_se_for_variance",
        },
    },
    {
        "stem": "3.2.5-ci-binomial-poisson-cs1011",
        "item_id": "cs1011-3.2.5-ar-02",
        "objective_id": "CS1-C-T02-LO05",
        "tags": {
            "b": "reuse_bern_variance",
            "c": "variances_swapped",
            "d": "binomial_only",
        },
    },
    {
        "stem": "3.2.6-ci-two-sample-cs1011",
        "item_id": "cs1011-3.2.6-ar-02",
        "objective_id": "CS1-C-T02-LO06",
        "tags": {
            "b": "equal_n_as_paired",
            "c": "pool_to_one_sample",
            "d": "ignore_independence",
        },
    },
    {
        "stem": "3.2.7-ci-paired-means-cs1011",
        "item_id": "cs1011-3.2.7-ar-02",
        "objective_id": "CS1-C-T02-LO07",
        "tags": {
            "b": "two_sample_on_paired",
            "c": "separate_means_only",
            "d": "drop_se_scaling",
        },
    },
    {
        "stem": "3.2.8-bootstrap-confidence-interval-cs1011",
        "item_id": "cs1011-3.2.8-ar-02",
        "objective_id": "CS1-C-T02-LO08",
        "tags": {
            "b": "se_only_as_ci",
            "c": "ht_as_ci",
            "d": "always_full_range",
        },
    },
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
        curriculum_identity=f"CS1:topic32-retry:{stem}",
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


def test_cs1011_3_2_1_ar_02_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_SPECS[0])


def test_cs1011_3_2_2_ar_02_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_SPECS[1])


def test_cs1011_3_2_3_ar_02_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_SPECS[2])


def test_cs1011_3_2_4_ar_02_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_SPECS[3])


def test_cs1011_3_2_5_ar_02_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_SPECS[4])


def test_cs1011_3_2_6_ar_02_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_SPECS[5])


def test_cs1011_3_2_7_ar_02_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_SPECS[6])


def test_cs1011_3_2_8_ar_02_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_SPECS[7])


def test_twin_package_has_no_topic_3_2_retry_items() -> None:
    pack = _pack("cp-3.2.1-ci-sample-cs1016")
    ids = [c.item_id for c in pack.knowledge_checks]
    assert "cs1011-3.2.1-ar-02" not in ids
    assert not any(iid.endswith("-ar-02") for iid in ids)
