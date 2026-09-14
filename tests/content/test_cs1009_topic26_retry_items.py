"""Load, score, and distractor-tag checks for CS1 topic 2.6 retry items.

cs1009-2.6.1-ar-02 classifies settlement-speed selection.
cs1009-2.6.2-ar-02 refuses equating a realised sample proportion with its
sampling distribution.
cs1009-2.6.3-ar-02 evaluates moment identities on new numbers.
cs1009-2.6.4-ar-02 names exact Normal-sample laws on new numbers.
cs1009-2.6.5-ar-02 evaluates the t-statistic on new numbers.
cs1009-2.6.6-ar-02 forms the variance-ratio F on new numbers.
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
        "stem": "2.6.1-random-samples-cs1009",
        "item_id": "cs1009-2.6.1-ar-02",
        "objective_id": "CS1-B-T06-LO01",
        "tags": {
            "b": "n_observations_as_sample",
            "c": "mean_match_proves_randomness",
            "d": "estimator_repairs_sampling",
        },
    },
    {
        "stem": "2.6.2-sampling-distribution-statistic-cs1009",
        "item_id": "cs1009-2.6.2-ar-02",
        "objective_id": "CS1-B-T06-LO02",
        "tags": {
            "b": "realised_is_distribution",
            "c": "n30_collapse",
            "d": "statistic_is_parameter",
        },
    },
    {
        "stem": "2.6.3-mean-var-sample-cs1009",
        "item_id": "cs1009-2.6.3-ar-02",
        "objective_id": "CS1-B-T06-LO03",
        "tags": {
            "b": "mean_divided_by_n",
            "c": "variance_not_divided_by_n",
            "d": "moments_imply_normality",
        },
    },
    {
        "stem": "2.6.4-normal-sample-mean-var-cs1009",
        "item_id": "cs1009-2.6.4-ar-02",
        "objective_id": "CS1-B-T06-LO04",
        "tags": {
            "b": "mean_variance_not_scaled",
            "c": "chi_square_scaling_missing",
            "d": "t_too_early",
        },
    },
    {
        "stem": "2.6.5-t-statistic-cs1009",
        "item_id": "cs1009-2.6.5-ar-02",
        "objective_id": "CS1-B-T06-LO05",
        "tags": {
            "b": "z_with_sample_sd",
            "c": "sd_as_standard_error",
            "d": "t_for_variance_ratio",
        },
    },
    {
        "stem": "2.6.6-f-distribution-cs1009",
        "item_id": "cs1009-2.6.6-ar-02",
        "objective_id": "CS1-B-T06-LO06",
        "tags": {
            "b": "t_for_variance_ratio",
            "c": "degrees_of_freedom_not_reduced",
            "d": "f_as_two_sample_t",
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
        curriculum_identity=f"CS1:topic26-retry:{stem}",
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
        assert tag not in bad.common_mistake


def test_lo01_settlement_speed_item_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_SPECS[0])


def test_lo02_sample_proportion_item_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_SPECS[1])


def test_lo03_moment_identities_item_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_SPECS[2])


def test_lo04_normal_sample_laws_item_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_SPECS[3])


def test_lo05_t_statistic_item_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_SPECS[4])


def test_lo06_f_ratio_item_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_SPECS[5])


def test_memory_front_twin_package_has_no_ar02() -> None:
    pack = _pack("cp-2.6.1-random-samples-cs1016")
    ids = [c.item_id for c in pack.knowledge_checks]
    assert ids == ["cs1016-2.6.1-ar-01", "cs1016-2.6.1-cp-01"]
    assert "cs1009-2.6.1-ar-02" not in ids
