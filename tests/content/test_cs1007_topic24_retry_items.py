"""Load, score, and distractor-tag checks for the CS1 topic 2.4 retry items.

cs1007-2.4.1-ar-02 forms Bernoulli MGF/CGF and refuses treating the mean as
the MGF. cs1007-2.4.2-ar-02 extracts Bernoulli mean and variance from the
MGF and refuses treating the written generating function as extraction.
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

_LO01 = {
    "stem": "2.4.1-mgf-cgf-cs1007",
    "item_id": "cs1007-2.4.1-ar-02",
    "objective_id": "CS1-B-T04-LO01",
    "tags": {
        "b": "moments_as_mgf",
        "c": "mgf_cgf_reversed",
        "d": "mean_only_mgf",
    },
}

_LO02 = {
    "stem": "2.4.2-moment-via-gf-cs1007",
    "item_id": "cs1007-2.4.2-ar-02",
    "objective_id": "CS1-B-T04-LO02",
    "tags": {
        "b": "mgf_value_as_mean",
        "c": "definition_finishes_extraction",
        "d": "derivative_at_one",
    },
}


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
        curriculum_identity=f"CS1:topic24-retry:{stem}",
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


def test_lo01_bernoulli_mgf_cgf_item_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_LO01)


def test_lo02_bernoulli_extraction_item_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_LO02)
