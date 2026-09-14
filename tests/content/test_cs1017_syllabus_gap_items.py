"""Load, score, and distractor-tag checks for two CS1-017 syllabus-gap items.

cs1017-1.1.3-ar-02 covers extremely large data sets.
cs1017-1.1.4-ar-02 covers the value of reproducible research.
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

_LO03 = {
    "stem": "cr-1.1.3-data-sources-cs1017",
    "item_id": "cs1017-1.1.3-ar-02",
    "objective_id": "CS1-A-T01-LO03",
    "tags": {
        "b": "must_use_every_row",
        "c": "volume_implies_ready",
        "d": "velocity_irrelevant_rowcount_wins",
    },
}
_LO04 = {
    "stem": "cr-1.1.4-reproducible-cs1017",
    "item_id": "cs1017-1.1.4-ar-02",
    "objective_id": "CS1-A-T01-LO04",
    "tags": {
        "b": "bureaucracy_only",
        "c": "verbal_handover_enough",
        "d": "speed_over_artefacts",
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
        curriculum_identity=f"CS1:syllabus-gap:{stem}",
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


def _assert_item_loads_scores_and_tags(spec: dict[str, object]) -> None:
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


def test_lo03_telematics_scale_item_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_LO03)


def test_lo04_value_of_reproducibility_item_loads_scores_and_tags() -> None:
    _assert_item_loads_scores_and_tags(_LO04)
