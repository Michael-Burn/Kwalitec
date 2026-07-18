"""Immutable compiled form of an Instructional Blueprint."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.instructional_blueprint.blueprint_step import BlueprintStep
from app.domain.instructional_blueprint.blueprint_type import BlueprintType
from app.domain.instructional_blueprint.effort_band import EffortBand


@dataclass(frozen=True)
class CompiledBlueprint:
    """Result of compiling an Instructional Blueprint into executable structure.

    Attributes:
        blueprint_id: Source blueprint identity.
        blueprint_type: Source blueprint type.
        steps: Ordered compiled instructional steps.
        applied_rule_ids: Rules considered during compilation.
        estimated_effort_band: Relative effort band.
        estimated_effort_units: Relative effort units.
        practice_ratio: Fraction of practice-oriented steps.
        theory_ratio: Fraction of theory-oriented steps.
        rationale_tags: Explainable compilation rationale tags.
        version: Source blueprint version token.
    """

    blueprint_id: str
    blueprint_type: BlueprintType
    steps: tuple[BlueprintStep, ...]
    applied_rule_ids: tuple[str, ...]
    estimated_effort_band: EffortBand
    estimated_effort_units: int
    practice_ratio: float
    theory_ratio: float
    rationale_tags: tuple[str, ...]
    version: str = "1.0.0"

    @property
    def step_count(self) -> int:
        """Number of compiled steps."""
        return len(self.steps)

    @property
    def activity_kinds(self) -> tuple[str, ...]:
        """Ordered compiled activity kinds."""
        return tuple(step.activity_kind for step in self.steps)
