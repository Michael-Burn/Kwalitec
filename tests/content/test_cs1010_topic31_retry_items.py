"""Load, score, and distractor-tag checks for CS1 topic 3.1 retry items.

cs1010-3.1.3-ar-02 evaluates bias/MSE on new numbers.
cs1010-3.1.4-ar-02 compares estimators by MSE on new numbers.
cs1010-3.1.5-ar-02 states asymptotic SE on new numbers.
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
        "stem": "3.1.3-efficiency-bias-consistency-mse-cs1010",
        "item_id": "cs1010-3.1.3-ar-02",
        "objective_id": "CS1-C-T01-LO03",
        "tags": {
            "b": "unbiased_always_wins",
            "c": "drop_variance",
            "d": "consistency_as_unbiased",
        },
    },
    {
        "stem": "3.1.4-comparison-mse-cs1010",
        "item_id": "cs1010-3.1.4-ar-02",
        "objective_id": "CS1-C-T01-LO04",
        "tags": {
            "b": "drop_bias_term",
            "c": "unbiased_always_wins",
            "d": "asymptotics_as_comparison",
        },
    },
    {
        "stem": "3.1.5-asymptotic-mle-cs1010",
        "item_id": "cs1010-3.1.5-ar-02",
        "objective_id": "CS1-C-T01-LO05",
        "tags": {
            "b": "finite_exact_info",
            "c": "bootstrap_replaces_asymptotics",
            "d": "drop_sqrt_n",
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
        curriculum_identity=f"CS1:topic31-retry:{stem}",
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


def test_cs1010_3_1_3_ar_02_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_SPECS[0])


def test_cs1010_3_1_4_ar_02_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_SPECS[1])


def test_cs1010_3_1_5_ar_02_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_SPECS[2])


def test_topic_3_1_retry_items_leave_lo01_lo02_lo06_and_twin_untouched() -> None:
    """Regression: LO01/LO02/LO06 packages and the LO01 twin stay at 2 KCs."""
    loader = EducationalPackageLoader(root=LIVE_ROOT)
    by_stem = {
        Path(p.source_path).stem: p
        for p in loader.all_approved()
        if p.source_path
    }
    for stem, count in (
        ("3.1.1-method-of-moments-cs1010", 2),
        ("3.1.2-maximum-likelihood-cs1010", 2),
        ("3.1.6-bootstrap-estimator-cs1010", 2),
        ("cp-3.1.1-estimators-cs1016", 2),
    ):
        pack = by_stem[stem]
        assert len(pack.knowledge_checks) == count
        ids = {c.item_id for c in pack.knowledge_checks}
        assert not any(iid.endswith("-ar-02") for iid in ids)
