"""Selection policy and BlueprintSelector tests."""

from __future__ import annotations

import pytest

from app.application.instructional_blueprint.blueprint_selector import (
    BlueprintSelector,
)
from app.application.instructional_blueprint.exceptions import (
    BlueprintNotFound,
    BlueprintSelectionError,
)
from app.application.instructional_blueprint.policies.selection_policy import (
    SelectionPolicy,
)
from app.domain.instructional_blueprint.blueprint_type import BlueprintType
from tests.application.instructional_blueprint.helpers import make_registry


@pytest.mark.parametrize(
    "tag,expected",
    [
        ("concept", BlueprintType.CONCEPT_MASTERY),
        ("mastery", BlueprintType.CONCEPT_MASTERY),
        ("understand", BlueprintType.CONCEPT_MASTERY),
        ("calculation", BlueprintType.CALCULATION_INTENSIVE),
        ("apply", BlueprintType.CALCULATION_INTENSIVE),
        ("theory", BlueprintType.THEORY_HEAVY),
        ("revision", BlueprintType.REVISION),
        ("revise", BlueprintType.REVISION),
        ("review", BlueprintType.REVISION),
        ("mixed", BlueprintType.MIXED_PRACTICE),
        ("practice", BlueprintType.MIXED_PRACTICE),
        ("exam", BlueprintType.EXAM_PRACTICE),
        ("assessment", BlueprintType.EXAM_PRACTICE),
        ("case", BlueprintType.CASE_STUDY),
        ("analyse", BlueprintType.CASE_STUDY),
        ("analyze", BlueprintType.CASE_STUDY),
        ("custom", BlueprintType.CUSTOM),
    ],
)
def test_intent_tag_mapping(tag, expected):
    assert SelectionPolicy.type_from_intent(tag) == expected


@pytest.mark.parametrize(
    "kind,expected",
    [
        ("understand", BlueprintType.CONCEPT_MASTERY),
        ("apply", BlueprintType.CALCULATION_INTENSIVE),
        ("analyse", BlueprintType.CASE_STUDY),
        ("analyze", BlueprintType.CASE_STUDY),
        ("review", BlueprintType.REVISION),
        ("revise", BlueprintType.REVISION),
    ],
)
def test_objective_kind_mapping(kind, expected):
    assert SelectionPolicy.type_from_objective_kind(kind) == expected


def test_unknown_intent_returns_none():
    assert SelectionPolicy.type_from_intent("totally_unknown") is None
    assert SelectionPolicy.type_from_intent("") is None


def test_resolve_type_explicit_wins():
    resolved = SelectionPolicy.resolve_type(
        blueprint_type="exam_practice",
        intent_tags=("revision",),
        objective_kinds=("understand",),
    )
    assert resolved == BlueprintType.EXAM_PRACTICE


def test_resolve_type_intent_before_objective():
    resolved = SelectionPolicy.resolve_type(
        intent_tags=("exam",),
        objective_kinds=("understand",),
    )
    assert resolved == BlueprintType.EXAM_PRACTICE


def test_resolve_type_objective_fallback():
    resolved = SelectionPolicy.resolve_type(objective_kinds=("revise",))
    assert resolved == BlueprintType.REVISION


def test_resolve_type_default():
    assert SelectionPolicy.resolve_type() == BlueprintType.CONCEPT_MASTERY


def test_selection_rationale_explicit():
    tags = SelectionPolicy.rationale_tags(
        resolved=BlueprintType.REVISION,
        blueprint_type="revision",
    )
    assert "source=explicit_type" in tags
    assert "no_student_state" in tags
    assert "no_ai" in tags


def test_selection_rationale_intent():
    tags = SelectionPolicy.rationale_tags(
        resolved=BlueprintType.EXAM_PRACTICE,
        intent_tags=("exam",),
    )
    assert "source=intent_tags" in tags


def test_selection_rationale_objective():
    tags = SelectionPolicy.rationale_tags(
        resolved=BlueprintType.CASE_STUDY,
        objective_kinds=("analyse",),
    )
    assert "source=objective_kinds" in tags


def test_selection_rationale_default():
    tags = SelectionPolicy.rationale_tags(
        resolved=BlueprintType.CONCEPT_MASTERY,
    )
    assert "source=default" in tags


def test_selection_policy_rejects_flags():
    assert SelectionPolicy.rejects_student_state() is True
    assert SelectionPolicy.rejects_content_generation() is True
    assert SelectionPolicy.rejects_ai() is True


def test_selector_by_id():
    selector = BlueprintSelector(make_registry())
    result = selector.select(blueprint_id="bp-revision")
    assert result.blueprint_type == BlueprintType.REVISION
    assert "source=explicit_id" in result.rationale_tags


def test_selector_blank_id_raises():
    selector = BlueprintSelector(make_registry())
    with pytest.raises(BlueprintSelectionError):
        selector.select(blueprint_id="  ")


def test_selector_missing_id_raises():
    selector = BlueprintSelector(make_registry())
    with pytest.raises(BlueprintNotFound):
        selector.select(blueprint_id="missing-bp")


def test_selector_by_type():
    selector = BlueprintSelector(make_registry())
    result = selector.select(blueprint_type=BlueprintType.CASE_STUDY)
    assert result.blueprint.name == "Case Study"


def test_selector_by_intent_tags():
    selector = BlueprintSelector(make_registry())
    result = selector.select(intent_tags=("calculation", "other"))
    assert result.blueprint_type == BlueprintType.CALCULATION_INTENSIVE


def test_selector_by_objective_kinds():
    selector = BlueprintSelector(make_registry())
    result = selector.select(objective_kinds=("understand",))
    assert result.blueprint_type == BlueprintType.CONCEPT_MASTERY


def test_selector_default():
    selector = BlueprintSelector(make_registry())
    result = selector.select()
    assert result.blueprint_type == BlueprintType.CONCEPT_MASTERY


def test_selector_resolve_type_without_fetch():
    selector = BlueprintSelector(make_registry())
    assert selector.resolve_type(intent_tags=("theory",)) == BlueprintType.THEORY_HEAVY


def test_selector_unregistered_type_raises():
    registry = make_registry(seed_defaults=False)
    selector = BlueprintSelector(registry)
    with pytest.raises(BlueprintSelectionError):
        selector.select(blueprint_type=BlueprintType.REVISION)
