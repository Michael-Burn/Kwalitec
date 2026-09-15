"""Load, score, and distractor-tag checks for CS1 topic 4.1 retry items.

cs1003-4.1.1-ar-02 assigns EL severity response/explanatory roles.
cs1003-4.1.2-ar-02 evaluates simple vs multiple fitted values.
cs1003-4.1.3-ar-02 computes OLS slope, intercept, and residual.
cs1003-4.1.4-ar-02 applies Wald z, slope CI, and mean vs prediction intervals.
cs1003-4.1.5-ar-02 selects nested models by adjusted R-squared.
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
        "stem": "4.1.1-response-explanatory-cs1003",
        "item_id": "cs1003-4.1.1-ar-02",
        "objective_id": "CS1-D-T01-LO01",
        "tags": {
            "b": "roles_reversed_column_soup",
            "c": "written_premium_as_auto_x",
            "d": "model_form_first",
        },
    },
    {
        "stem": "4.1.2-simple-multiple-cs1003",
        "item_id": "cs1003-4.1.2-ar-02",
        "objective_id": "CS1-D-T01-LO02",
        "tags": {
            "b": "forms_swapped",
            "c": "drop_second_x",
            "d": "least_squares_finishes",
        },
    },
    {
        "stem": "4.1.3-least-squares-cs1003",
        "item_id": "cs1003-4.1.3-ar-02",
        "objective_id": "CS1-D-T01-LO03",
        "tags": {
            "b": "corr_as_slope",
            "c": "residual_sign_flipped",
            "d": "lad_as_ols",
        },
    },
    {
        "stem": "4.1.4-software-inference-cs1003",
        "item_id": "cs1003-4.1.4-ar-02",
        "objective_id": "CS1-D-T01-LO04",
        "tags": {
            "b": "intervals_identical",
            "c": "fit_finishes_inference",
            "d": "wald_multiply_se",
        },
    },
    {
        "stem": "4.1.5-variable-selection-cs1003",
        "item_id": "cs1003-4.1.5-ar-02",
        "objective_id": "CS1-D-T01-LO05",
        "tags": {
            "b": "fewer_always_wins",
            "c": "raw_r2_penalty",
            "d": "p_value_chopping",
        },
    },
)

_TWIN_STEMS = (
    "4.1.1-response-explanatory-cs1013",
    "cp-4.1.1-linear-regression-cs1016",
    "4.1.2-simple-multiple-cs1013",
    "4.1.3-least-squares-cs1013",
    "4.1.4-software-fit-cs1013",
    "4.1.5-variable-selection-cs1013",
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
        curriculum_identity=f"CS1:{pack.package_id}",
        topic_id=pack.topic_code,
    )
    for activity in substance.activities:
        if activity.stage is not EducationalStage.PRACTICE:
            continue
        assert activity.scoreable is not None
        if activity.scoreable.item_id == item_id:
            return activity.scoreable
    raise AssertionError(f"missing practice item {item_id} in {stem}")


def test_topic41_retry_items_load_with_correct_objective_and_tags() -> None:
    for spec in _SPECS:
        pack = _pack(spec["stem"])
        check = next(
            (c for c in pack.knowledge_checks if c.item_id == spec["item_id"]),
            None,
        )
        assert check is not None, f"{spec['item_id']} did not load"
        assert check.response_type == "mcq"
        assert (check.objective_id or "").strip() == spec["objective_id"]
        assert check.correct_choice_id == "a"
        assert [c.id for c in check.choices] == ["a", "b", "c", "d"]
        assert check.choices[0].misconception_tag == ""
        for choice_id, tag in spec["tags"].items():
            match = next(c for c in check.choices if c.id == choice_id)
            assert match.misconception_tag == tag


def test_topic41_retry_items_score_correct_and_distractors() -> None:
    for spec in _SPECS:
        item = _scoreable(spec["stem"], spec["item_id"])
        assert score_practice_response(item, "a").correct is True
        for cid in spec["tags"]:
            scored = score_practice_response(item, cid)
            assert scored.correct is False


def test_topic41_retry_items_absent_from_twin_packages() -> None:
    loader = EducationalPackageLoader(root=LIVE_ROOT)
    retry_ids = {spec["item_id"] for spec in _SPECS}
    for stem in _TWIN_STEMS:
        packs = [
            p
            for p in loader.all_approved()
            if p.source_path and Path(p.source_path).stem == stem
        ]
        assert packs, f"missing twin package {stem}"
        twin_ids = {c.item_id for c in packs[0].knowledge_checks}
        assert retry_ids.isdisjoint(twin_ids)


def test_topic41_retry_items_present_only_in_named_live_packages() -> None:
    root = Path("app/curriculum/data/educational_packages/cs1")
    expected = {spec["item_id"]: spec["stem"] for spec in _SPECS}
    found: dict[str, str] = {}
    for path in root.glob("*.json"):
        data = json.loads(path.read_text())
        for check in data.get("knowledge_checks") or []:
            item_id = check.get("item_id")
            if item_id in expected:
                found[item_id] = path.stem
    assert found == expected
