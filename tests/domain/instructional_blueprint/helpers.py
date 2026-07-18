"""Shared helpers for Instructional Blueprint Engine tests."""

from __future__ import annotations

from app.application.instructional_blueprint.blueprint_registry import (
    BlueprintRegistry,
)
from app.application.instructional_blueprint.engine import (
    InstructionalBlueprintEngine,
)
from app.domain.instructional_blueprint.blueprint import InstructionalBlueprint
from app.domain.instructional_blueprint.blueprint_profile import BlueprintProfile
from app.domain.instructional_blueprint.blueprint_rule import BlueprintRule
from app.domain.instructional_blueprint.blueprint_step import BlueprintStep
from app.domain.instructional_blueprint.blueprint_type import BlueprintType


def make_step(
    step_id: str = "step-0",
    activity_kind: str = "concept_learning",
    *,
    sequence_index: int = 0,
    role: str | None = "core",
    effort_weight: int = 1,
    required: bool = True,
    metadata: tuple[str, ...] | None = None,
) -> BlueprintStep:
    return BlueprintStep.create(
        step_id,
        activity_kind,
        sequence_index=sequence_index,
        role=role,
        effort_weight=effort_weight,
        required=required,
        metadata=metadata,
    )


def make_steps(*kinds: str) -> tuple[BlueprintStep, ...]:
    return tuple(
        make_step(f"s{i}", kind, sequence_index=i) for i, kind in enumerate(kinds)
    )


def make_profile(
    profile_id: str = "profile-test",
    **kwargs,
) -> BlueprintProfile:
    return BlueprintProfile.create(profile_id, **kwargs)


def make_rule(
    rule_id: str = "rule-1",
    kind: str = "min_steps",
    **kwargs,
) -> BlueprintRule:
    return BlueprintRule.create(rule_id, kind, **kwargs)


def make_blueprint(
    blueprint_id: str = "bp-test",
    blueprint_type: BlueprintType | str = BlueprintType.CONCEPT_MASTERY,
    name: str = "Test Blueprint",
    *,
    steps: tuple[BlueprintStep, ...] | None = None,
    rules: tuple[BlueprintRule, ...] | None = None,
    profile: BlueprintProfile | None = None,
    allow_empty_steps: bool = False,
    **kwargs,
) -> InstructionalBlueprint:
    if steps is None:
        steps = make_steps("introduction", "concept_learning", "summary")
    return InstructionalBlueprint.create(
        blueprint_id,
        blueprint_type,
        name,
        steps=steps,
        rules=rules,
        profile=profile or make_profile(),
        allow_empty_steps=allow_empty_steps
        or BlueprintType.resolve(blueprint_type) == BlueprintType.CUSTOM,
        **kwargs,
    )


def make_engine(*, seed_defaults: bool = True) -> InstructionalBlueprintEngine:
    return InstructionalBlueprintEngine(seed_defaults=seed_defaults)


def make_registry(*, seed_defaults: bool = True) -> BlueprintRegistry:
    return BlueprintRegistry(seed_defaults=seed_defaults)


def all_default_types() -> tuple[BlueprintType, ...]:
    return tuple(
        t for t in BlueprintType if t != BlueprintType.CUSTOM
    ) + (BlueprintType.CUSTOM,)
