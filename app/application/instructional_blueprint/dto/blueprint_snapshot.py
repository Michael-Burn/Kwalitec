"""Immutable snapshot of Instructional Blueprint Engine posture."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.instructional_blueprint.dto.blueprint_plan import BlueprintPlan
from app.application.instructional_blueprint.dto.compiled_blueprint import (
    CompiledBlueprint,
)
from app.domain.instructional_blueprint.blueprint import InstructionalBlueprint
from app.domain.instructional_blueprint.blueprint_type import BlueprintType
from app.domain.instructional_blueprint.effort_band import EffortBand


@dataclass(frozen=True)
class InstructionalStructure:
    """Read-only instructional structure summary (no educational content).

    Attributes:
        blueprint_type: Selected / compiled type.
        activity_kinds: Ordered activity kind tokens.
        step_count: Number of instructional steps.
        estimated_effort_band: Relative effort band.
        estimated_effort_units: Relative effort units.
        phase_labels: Session skeleton phase labels.
        rationale_tags: Explainable structure tags.
    """

    blueprint_type: BlueprintType
    activity_kinds: tuple[str, ...]
    step_count: int
    estimated_effort_band: EffortBand
    estimated_effort_units: int
    phase_labels: tuple[str, ...]
    rationale_tags: tuple[str, ...]


@dataclass(frozen=True)
class BlueprintSnapshot:
    """Read-only snapshot of blueprint selection / compilation / planning.

    Attributes:
        blueprint: Source instructional blueprint when available.
        compiled: Compiled blueprint when available.
        plan: Generated blueprint plan when available.
        structure: Condensed instructional structure.
        is_valid: True when validation passed for the source blueprint.
        validation_codes: Validation issue codes when invalid.
    """

    blueprint: InstructionalBlueprint | None
    compiled: CompiledBlueprint | None
    plan: BlueprintPlan | None
    structure: InstructionalStructure
    is_valid: bool
    validation_codes: tuple[str, ...] = ()
