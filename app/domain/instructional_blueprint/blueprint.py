"""Instructional Blueprint — reusable pedagogical structure aggregate.

Defines HOW topics should be taught as ordered activity flows.
Contains no curriculum content and no student-specific logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.instructional_blueprint.blueprint_profile import BlueprintProfile
from app.domain.instructional_blueprint.blueprint_rule import BlueprintRule
from app.domain.instructional_blueprint.blueprint_step import BlueprintStep
from app.domain.instructional_blueprint.blueprint_type import BlueprintType
from app.domain.instructional_blueprint.effort_band import EffortBand


@dataclass(frozen=True)
class InstructionalBlueprint:
    """Reusable instructional strategy (structure without educational content).

    Attributes:
        blueprint_id: Stable blueprint identity.
        blueprint_type: Catalogue type.
        name: Operational structural label (not generated study content).
        steps: Ordered instructional steps.
        rules: Structural compilation / validation rules.
        profile: Pedagogical balance profile.
        version: Blueprint edition token.
        metadata: Immutable structural tags.
    """

    blueprint_id: str
    blueprint_type: BlueprintType
    name: str
    steps: tuple[BlueprintStep, ...] = field(default_factory=tuple)
    rules: tuple[BlueprintRule, ...] = field(default_factory=tuple)
    profile: BlueprintProfile | None = None
    version: str = "1.0.0"
    metadata: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        blueprint_id: str,
        blueprint_type: BlueprintType | str,
        name: str,
        *,
        steps: list[BlueprintStep] | tuple[BlueprintStep, ...] | None = None,
        rules: list[BlueprintRule] | tuple[BlueprintRule, ...] | None = None,
        profile: BlueprintProfile | None = None,
        version: str = "1.0.0",
        metadata: list[str] | tuple[str, ...] | None = None,
        allow_empty_steps: bool = False,
    ) -> InstructionalBlueprint:
        """Construct an InstructionalBlueprint after validating invariants.

        Raises:
            ValueError: On empty identity/name, duplicate step/rule ids, or
                empty steps when not explicitly allowed.
        """
        bid = _require_non_empty(blueprint_id, "blueprint_id")
        label = _require_non_empty(name, "name")
        version_token = _require_non_empty(version, "version")
        type_value = BlueprintType.resolve(blueprint_type)
        steps_t = tuple(steps or ())
        rules_t = tuple(rules or ())

        if not steps_t and not allow_empty_steps and type_value != BlueprintType.CUSTOM:
            raise ValueError("steps must not be empty for non-custom blueprints")

        seen_steps: set[str] = set()
        for step in steps_t:
            if step.step_id in seen_steps:
                raise ValueError(f"duplicate step_id: {step.step_id!r}")
            seen_steps.add(step.step_id)

        seen_rules: set[str] = set()
        for rule in rules_t:
            if rule.rule_id in seen_rules:
                raise ValueError(f"duplicate rule_id: {rule.rule_id!r}")
            seen_rules.add(rule.rule_id)

        indices = [step.sequence_index for step in steps_t]
        if indices and sorted(indices) != list(range(len(indices))):
            raise ValueError("step sequence_index values must be contiguous from 0")
        ordered = [step.sequence_index for step in steps_t]
        if ordered != sorted(ordered):
            raise ValueError("steps must be ordered by ascending sequence_index")

        resolved_profile = profile or BlueprintProfile.create(
            f"profile-{bid}",
            default_effort_band=EffortBand.MEDIUM,
        )

        return cls(
            blueprint_id=bid,
            blueprint_type=type_value,
            name=label,
            steps=steps_t,
            rules=rules_t,
            profile=resolved_profile,
            version=version_token,
            metadata=tuple(metadata or ()),
        )

    @property
    def step_count(self) -> int:
        """Number of instructional steps."""
        return len(self.steps)

    @property
    def activity_kinds(self) -> tuple[str, ...]:
        """Ordered activity kind tokens."""
        return tuple(step.activity_kind for step in self.steps)

    @property
    def default_effort_band(self) -> EffortBand:
        """Baseline effort band from the profile."""
        if self.profile is None:
            return EffortBand.MEDIUM
        return self.profile.default_effort_band

    def step_by_id(self, step_id: str) -> BlueprintStep | None:
        """Return a step by identity, or None."""
        token = (step_id or "").strip()
        if not token:
            return None
        for step in self.steps:
            if step.step_id == token:
                return step
        return None

    def with_steps(
        self,
        steps: list[BlueprintStep] | tuple[BlueprintStep, ...],
    ) -> InstructionalBlueprint:
        """Return a copy with replacement steps (re-validated)."""
        return InstructionalBlueprint.create(
            self.blueprint_id,
            self.blueprint_type,
            self.name,
            steps=steps,
            rules=self.rules,
            profile=self.profile,
            version=self.version,
            metadata=self.metadata,
            allow_empty_steps=self.blueprint_type == BlueprintType.CUSTOM,
        )


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
