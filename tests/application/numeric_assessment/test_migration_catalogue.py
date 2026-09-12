"""Prove migration of all 30 live numeric checkpoints onto Answer Specifications.

Standalone: does not wire into score_practice_response. Compares framework
verdicts against the known correct accepted answers from the live catalogue,
and confirms the four banked precision-tolerance mismatches are fixed.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from app.application.educational_packages.loader import (
    EducationalPackageLoader,
    reset_educational_package_cache,
)
from app.application.educational_packages.substance import substance_from_package
from app.application.learning_session.educational_flow import EducationalStage
from app.application.learning_session.scoreable_practice import (
    score_practice_response,
)
from app.application.numeric_assessment import (
    BANKED_PRECISION_TOLERANCE_ITEM_IDS,
    LIVE_NUMERIC_CHECKPOINT_COUNT,
    EvaluationPolicy,
    PrecisionRequirement,
    evaluate,
    load_live_answer_specifications,
    reset_live_answer_specification_cache,
)

PKG_ROOT = Path("app/application/numeric_assessment")


@pytest.fixture(autouse=True)
def _reset_caches() -> None:
    reset_educational_package_cache()
    reset_live_answer_specification_cache()


def _live_numeric_accepted() -> dict[str, tuple[str, float]]:
    """item_id -> (accepted string, legacy numeric_tolerance)."""
    found: dict[str, tuple[str, float]] = {}
    for pack in EducationalPackageLoader().all_approved():
        for check in pack.knowledge_checks:
            if check.kind == "checkpoint" and check.response_type == "numeric":
                found[check.item_id] = (
                    check.accepted_keywords[0],
                    float(check.numeric_tolerance),
                )
    return found


def _all_item_ids() -> list[str]:
    reset_educational_package_cache()
    return sorted(_live_numeric_accepted().keys())


def _scoreable(item_id: str):
    for pack in EducationalPackageLoader().all_approved():
        substance = substance_from_package(
            pack,
            curriculum_identity=f"CS1:{pack.topic_code}",
            topic_id=pack.topic_code,
        )
        for act in substance.activities:
            if (
                act.stage is EducationalStage.PRACTICE
                and act.scoreable is not None
                and act.scoreable.item_id == item_id
            ):
                return act.scoreable
    raise AssertionError(f"missing scoreable {item_id}")


def test_catalogue_has_exactly_thirty_migrated_specs() -> None:
    specs = load_live_answer_specifications()
    live = _live_numeric_accepted()
    assert len(live) == LIVE_NUMERIC_CHECKPOINT_COUNT
    assert len(specs) == LIVE_NUMERIC_CHECKPOINT_COUNT
    assert set(specs) == set(live)


@pytest.mark.parametrize("item_id", _all_item_ids())
def test_known_correct_answer_matches_old_and_new(item_id: str) -> None:
    """Known accepted answer is Correct under old scorer and value_correct under new."""
    live = _live_numeric_accepted()
    accepted, _tol = live[item_id]
    specs = load_live_answer_specifications()
    spec = specs[item_id]

    assert float(accepted) == pytest.approx(spec.canonical_value)

    old = score_practice_response(_scoreable(item_id), accepted)
    assert old.scored is True
    assert old.correct is True

    new = evaluate(spec, accepted)
    assert new.value_correct is True
    assert new.fully_correct is True
    assert bool(old.correct) == bool(new.value_correct)


@pytest.mark.parametrize(
    "item_id",
    sorted(BANKED_PRECISION_TOLERANCE_ITEM_IDS),
)
def test_banked_precision_tolerance_fixed_under_decimal_precision(
    item_id: str,
) -> None:
    """Stem asks for 4dp; old abs tol 0.001 accepted 3dp rounding; new does not."""
    live = _live_numeric_accepted()
    accepted, legacy_tol = live[item_id]
    assert legacy_tol == pytest.approx(0.001)

    spec = load_live_answer_specifications()[item_id]
    assert spec.comparison_policy.policy is EvaluationPolicy.DECIMAL_PRECISION
    assert spec.comparison_policy.decimal_places == 4
    assert (
        spec.precision_policy.requirement
        is PrecisionRequirement.EXACT_DECIMAL_PLACES
    )
    assert spec.precision_policy.decimal_places == 4

    assert evaluate(spec, accepted).fully_correct is True
    assert score_practice_response(_scoreable(item_id), accepted).correct is True

    three_dp = f"{round(float(accepted), 3):.3f}"
    assert three_dp != accepted
    old_three = score_practice_response(_scoreable(item_id), three_dp)
    new_three = evaluate(spec, three_dp)
    assert old_three.correct is True
    assert new_three.value_correct is False
    assert new_three.fully_correct is False


def test_stated_precision_items_use_decimal_precision_policy() -> None:
    """Every stem that states N decimal places uses decimal_precision N."""
    expected = {
        "cs1003-4.2.5-cp-01": 4,
        "cs1003-4.2.8-cp-01": 4,
        "cs1004-cgr1-cp-01": 4,
        "cs1014-4.2.5-cp-01": 4,
        "cs1010-3.1.6-cp-01": 3,
        "cs1016-2.1.3-cp-01": 3,
        "cs1015-5.1.8-cp-01": 2,
    }
    specs = load_live_answer_specifications()
    for item_id, places in expected.items():
        spec = specs[item_id]
        assert spec.comparison_policy.policy is EvaluationPolicy.DECIMAL_PRECISION
        assert spec.comparison_policy.decimal_places == places


def test_catalogue_loader_does_not_import_live_scorer() -> None:
    path = PKG_ROOT / "catalogue.py"
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            names = [node.module or ""]
        else:
            continue
        for name in names:
            assert "scoreable_practice" not in name
            assert not name.startswith("app.application.learning_session")
