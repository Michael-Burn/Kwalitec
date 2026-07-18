"""Domain tests for Instructional Blueprint types and effort bands."""

from __future__ import annotations

import pytest

from app.domain.instructional_blueprint import (
    BlueprintType,
    EffortBand,
    effort_at_least,
    effort_rank,
    effort_units_for,
    resolve_effort_band,
)
from app.domain.instructional_blueprint.blueprint_rule import BlueprintRuleKind


@pytest.mark.parametrize(
    "value,expected",
    [
        ("concept_mastery", BlueprintType.CONCEPT_MASTERY),
        ("Concept Mastery", BlueprintType.CONCEPT_MASTERY),
        ("CALCULATION_INTENSIVE", BlueprintType.CALCULATION_INTENSIVE),
        ("theory-heavy", BlueprintType.THEORY_HEAVY),
        ("revision", BlueprintType.REVISION),
        ("mixed practice", BlueprintType.MIXED_PRACTICE),
        ("exam_practice", BlueprintType.EXAM_PRACTICE),
        ("case_study", BlueprintType.CASE_STUDY),
        ("custom", BlueprintType.CUSTOM),
        ("unknown_future", BlueprintType.CUSTOM),
        ("", BlueprintType.CUSTOM),
        (BlueprintType.REVISION, BlueprintType.REVISION),
    ],
)
def test_blueprint_type_resolve(value, expected):
    assert BlueprintType.resolve(value) == expected


def test_blueprint_type_known_values_stable_order():
    values = BlueprintType.known_values()
    assert values[0] == "concept_mastery"
    assert "custom" in values
    assert len(values) == 8


def test_blueprint_type_known_members_count():
    assert len(BlueprintType.known_members()) == 8


@pytest.mark.parametrize(
    "value,expected",
    [
        ("low", EffortBand.LOW),
        ("MEDIUM", EffortBand.MEDIUM),
        ("high", EffortBand.HIGH),
        ("extensive", EffortBand.EXTENSIVE),
        ("", EffortBand.MEDIUM),
        ("nope", EffortBand.MEDIUM),
        (EffortBand.HIGH, EffortBand.HIGH),
    ],
)
def test_resolve_effort_band(value, expected):
    assert resolve_effort_band(value) == expected


@pytest.mark.parametrize(
    "band,rank",
    [
        (EffortBand.LOW, 1),
        (EffortBand.MEDIUM, 2),
        (EffortBand.HIGH, 3),
        (EffortBand.EXTENSIVE, 4),
    ],
)
def test_effort_rank(band, rank):
    assert effort_rank(band) == rank


@pytest.mark.parametrize(
    "band,units",
    [
        (EffortBand.LOW, 2),
        (EffortBand.MEDIUM, 4),
        (EffortBand.HIGH, 6),
        (EffortBand.EXTENSIVE, 9),
    ],
)
def test_effort_units_for(band, units):
    assert effort_units_for(band) == units


def test_effort_at_least():
    assert effort_at_least(EffortBand.HIGH, EffortBand.MEDIUM) is True
    assert effort_at_least(EffortBand.LOW, EffortBand.HIGH) is False
    assert effort_at_least(EffortBand.MEDIUM, EffortBand.MEDIUM) is True


@pytest.mark.parametrize(
    "value,expected",
    [
        ("require_activity", BlueprintRuleKind.REQUIRE_ACTIVITY),
        ("MAX_STEPS", BlueprintRuleKind.MAX_STEPS),
        ("bookend-summary", BlueprintRuleKind.BOOKEND_SUMMARY),
        ("unknown", BlueprintRuleKind.CUSTOM),
        ("", BlueprintRuleKind.CUSTOM),
        (BlueprintRuleKind.MIN_STEPS, BlueprintRuleKind.MIN_STEPS),
    ],
)
def test_rule_kind_resolve(value, expected):
    assert BlueprintRuleKind.resolve(value) == expected


def test_domain_package_lazy_exports():
    import app.domain.instructional_blueprint as pkg

    for name in pkg.__all__:
        assert getattr(pkg, name) is not None


def test_domain_package_dir_includes_exports():
    import app.domain.instructional_blueprint as pkg

    names = dir(pkg)
    assert "InstructionalBlueprint" in names
    assert "BlueprintType" in names
