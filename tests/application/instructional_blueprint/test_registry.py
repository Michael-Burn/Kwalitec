"""Registry and default catalogue tests."""

from __future__ import annotations

import pytest

from app.application.instructional_blueprint.blueprint_registry import (
    BlueprintRegistry,
)
from app.application.instructional_blueprint.exceptions import (
    BlueprintAlreadyRegistered,
    BlueprintNotFound,
    RegistryError,
)
from app.domain.instructional_blueprint.blueprint_type import BlueprintType
from tests.application.instructional_blueprint.helpers import (
    make_blueprint,
    make_registry,
    make_steps,
)


def test_registry_seeds_eight_defaults():
    registry = make_registry()
    assert registry.count() == 8
    assert set(registry.list_types()) == set(BlueprintType)


@pytest.mark.parametrize("blueprint_type", list(BlueprintType))
def test_registry_has_each_default_type(blueprint_type):
    registry = make_registry()
    assert registry.has_type(blueprint_type)
    bp = registry.get_by_type(blueprint_type)
    assert bp.blueprint_type == blueprint_type
    assert bp.name


@pytest.mark.parametrize(
    "blueprint_type,expected_name",
    [
        (BlueprintType.CONCEPT_MASTERY, "Concept Mastery"),
        (BlueprintType.CALCULATION_INTENSIVE, "Calculation Intensive"),
        (BlueprintType.THEORY_HEAVY, "Theory Heavy"),
        (BlueprintType.REVISION, "Revision"),
        (BlueprintType.MIXED_PRACTICE, "Mixed Practice"),
        (BlueprintType.EXAM_PRACTICE, "Exam Practice"),
        (BlueprintType.CASE_STUDY, "Case Study"),
        (BlueprintType.CUSTOM, "Custom"),
    ],
)
def test_default_blueprint_names(blueprint_type, expected_name):
    bp = make_registry().get_by_type(blueprint_type)
    assert bp.name == expected_name


def test_default_non_custom_have_steps():
    registry = make_registry()
    for blueprint_type in BlueprintType:
        bp = registry.get_by_type(blueprint_type)
        if blueprint_type == BlueprintType.CUSTOM:
            assert bp.step_count == 0
        else:
            assert bp.step_count >= 5


def test_register_and_get():
    registry = make_registry(seed_defaults=False)
    bp = make_blueprint(blueprint_id="bp-a")
    registry.register(bp)
    assert registry.get("bp-a") is bp
    assert registry.has("bp-a")


def test_register_duplicate_raises():
    registry = make_registry(seed_defaults=False)
    bp = make_blueprint(blueprint_id="bp-a")
    registry.register(bp)
    with pytest.raises(BlueprintAlreadyRegistered):
        registry.register(bp)


def test_register_overwrite():
    registry = make_registry(seed_defaults=False)
    bp1 = make_blueprint(blueprint_id="bp-a", name="One")
    bp2 = make_blueprint(blueprint_id="bp-a", name="Two")
    registry.register(bp1)
    registry.register(bp2, overwrite=True)
    assert registry.get("bp-a").name == "Two"


def test_get_missing_raises():
    registry = make_registry(seed_defaults=False)
    with pytest.raises(BlueprintNotFound):
        registry.get("missing")


def test_get_by_type_missing_raises():
    registry = make_registry(seed_defaults=False)
    with pytest.raises(BlueprintNotFound):
        registry.get_by_type(BlueprintType.REVISION)


def test_unregister():
    registry = make_registry()
    removed = registry.unregister("bp-revision")
    assert removed.blueprint_type == BlueprintType.REVISION
    assert not registry.has_type(BlueprintType.REVISION)
    assert registry.count() == 7


def test_unregister_missing_raises():
    registry = make_registry(seed_defaults=False)
    with pytest.raises(BlueprintNotFound):
        registry.unregister("missing")


def test_clear():
    registry = make_registry()
    registry.clear()
    assert registry.count() == 0
    assert registry.list_ids() == ()


def test_list_ids_sorted():
    registry = make_registry()
    ids = registry.list_ids()
    assert ids == tuple(sorted(ids))


def test_list_blueprints_matches_ids():
    registry = make_registry()
    blueprints = registry.list_blueprints()
    assert tuple(bp.blueprint_id for bp in blueprints) == registry.list_ids()


def test_register_rejects_non_blueprint():
    registry = make_registry(seed_defaults=False)
    with pytest.raises(RegistryError):
        registry.register("not-a-blueprint")  # type: ignore[arg-type]


def test_overwrite_type_mapping_replaces_previous():
    registry = make_registry(seed_defaults=False)
    first = make_blueprint(
        blueprint_id="bp-1",
        blueprint_type=BlueprintType.REVISION,
        name="First",
        steps=make_steps("review"),
    )
    second = make_blueprint(
        blueprint_id="bp-2",
        blueprint_type=BlueprintType.REVISION,
        name="Second",
        steps=make_steps("review", "summary"),
    )
    registry.register(first)
    registry.register(second, overwrite=True)
    assert registry.get_by_type(BlueprintType.REVISION).blueprint_id == "bp-2"
    assert not registry.has("bp-1")


def test_empty_registry_without_seed():
    registry = BlueprintRegistry(seed_defaults=False)
    assert registry.count() == 0


def test_has_false_for_blank_id():
    registry = make_registry()
    assert registry.has("") is False
    assert registry.has("   ") is False
