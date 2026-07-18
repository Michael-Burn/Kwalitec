"""Instructional Blueprint Engine — public application interface.

Reusable pedagogical engine responsible for defining HOW topics should be
taught. Contains no curriculum content and no student-specific logic.

Owns: register, select, validate, compile, generate activity sequence,
estimate effort, return instructional structure.

Does NOT: generate questions, explanations, PDFs, or study prose.
Framework-independent: no Flask, SQLAlchemy, UI, or persistence.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.instructional_blueprint.blueprint_compiler import (
    BlueprintCompiler,
)
from app.application.instructional_blueprint.blueprint_registry import (
    BlueprintRegistry,
)
from app.application.instructional_blueprint.blueprint_selector import (
    BlueprintSelector,
    SelectionResult,
)
from app.application.instructional_blueprint.blueprint_validator import (
    BlueprintValidator,
    ValidationResult,
)
from app.application.instructional_blueprint.dto.blueprint_plan import (
    BlueprintPlan,
    SessionSkeleton,
)
from app.application.instructional_blueprint.dto.blueprint_snapshot import (
    BlueprintSnapshot,
    InstructionalStructure,
)
from app.application.instructional_blueprint.dto.compiled_blueprint import (
    CompiledBlueprint,
)
from app.application.instructional_blueprint.sequence_generator import (
    SequenceGenerator,
)
from app.domain.instructional_blueprint.blueprint import InstructionalBlueprint
from app.domain.instructional_blueprint.blueprint_step import BlueprintStep
from app.domain.instructional_blueprint.blueprint_type import BlueprintType
from app.domain.instructional_blueprint.effort_band import EffortBand


@dataclass(frozen=True)
class BlueprintHandle:
    """In-memory handle for instructional blueprint processing.

    Callers remain responsible for persistence. The engine never saves.
    """

    blueprint: InstructionalBlueprint
    compiled: CompiledBlueprint | None = None
    plan: BlueprintPlan | None = None
    selection_rationale: tuple[str, ...] = ()


class InstructionalBlueprintEngine:
    """Public facade for Instructional Blueprint pedagogical structure.

    Coordinates registry, selection, validation, compilation, and sequence
    generation. Never generates educational content. Never uses student state.
    """

    ENGINE_ID = "instructional_blueprint"
    ENGINE_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        registry: BlueprintRegistry | None = None,
        selector: BlueprintSelector | None = None,
        validator: BlueprintValidator | None = None,
        compiler: BlueprintCompiler | None = None,
        sequence_generator: SequenceGenerator | None = None,
        seed_defaults: bool = True,
    ) -> None:
        self._registry = registry or BlueprintRegistry(seed_defaults=seed_defaults)
        self._selector = selector or BlueprintSelector(self._registry)
        self._validator = validator or BlueprintValidator()
        self._compiler = compiler or BlueprintCompiler(validator=self._validator)
        self._sequences = sequence_generator or SequenceGenerator()

    @property
    def engine_id(self) -> str:
        return self.ENGINE_ID

    @property
    def engine_version(self) -> str:
        return self.ENGINE_VERSION

    @property
    def registry(self) -> BlueprintRegistry:
        return self._registry

    # ------------------------------------------------------------------
    # Register
    # ------------------------------------------------------------------

    def register_blueprint(
        self,
        blueprint: InstructionalBlueprint,
        *,
        overwrite: bool = False,
    ) -> InstructionalBlueprint:
        """Register a blueprint in the in-memory registry."""
        return self._registry.register(blueprint, overwrite=overwrite)

    def list_blueprints(self) -> tuple[InstructionalBlueprint, ...]:
        """Return all registered blueprints."""
        return self._registry.list_blueprints()

    def get_blueprint(self, blueprint_id: str) -> InstructionalBlueprint:
        """Return a registered blueprint by identity."""
        return self._registry.get(blueprint_id)

    def get_blueprint_by_type(
        self, blueprint_type: BlueprintType | str
    ) -> InstructionalBlueprint:
        """Return a registered blueprint by catalogue type."""
        return self._registry.get_by_type(blueprint_type)

    # ------------------------------------------------------------------
    # Select
    # ------------------------------------------------------------------

    def select_blueprint(
        self,
        *,
        blueprint_type: BlueprintType | str | None = None,
        blueprint_id: str | None = None,
        intent_tags: list[str] | tuple[str, ...] | None = None,
        objective_kinds: list[str] | tuple[str, ...] | None = None,
    ) -> SelectionResult:
        """Select a blueprint from structural signals only."""
        return self._selector.select(
            blueprint_type=blueprint_type,
            blueprint_id=blueprint_id,
            intent_tags=intent_tags,
            objective_kinds=objective_kinds,
        )

    # ------------------------------------------------------------------
    # Validate
    # ------------------------------------------------------------------

    def validate_blueprint(
        self, blueprint: InstructionalBlueprint
    ) -> ValidationResult:
        """Validate blueprint structure."""
        return self._validator.validate(blueprint)

    def assert_valid(self, blueprint: InstructionalBlueprint) -> None:
        """Raise when blueprint structure is invalid."""
        self._validator.assert_valid(blueprint)

    # ------------------------------------------------------------------
    # Compile
    # ------------------------------------------------------------------

    def compile_blueprint(
        self,
        blueprint: InstructionalBlueprint,
        *,
        extra_steps: list[BlueprintStep] | tuple[BlueprintStep, ...] | None = None,
        validate: bool = True,
    ) -> CompiledBlueprint:
        """Compile a blueprint into instructional structure."""
        return self._compiler.compile(
            blueprint, extra_steps=extra_steps, validate=validate
        )

    # ------------------------------------------------------------------
    # Generate sequence / plan / effort / structure
    # ------------------------------------------------------------------

    def generate_plan(
        self,
        compiled: CompiledBlueprint,
        *,
        objective_ids: list[str] | tuple[str, ...] | None = None,
    ) -> BlueprintPlan:
        """Generate an activity plan / session skeleton / learning sequence."""
        return self._sequences.generate(compiled, objective_ids=objective_ids)

    def generate_sequence(
        self,
        *,
        blueprint_type: BlueprintType | str | None = None,
        blueprint_id: str | None = None,
        intent_tags: list[str] | tuple[str, ...] | None = None,
        objective_kinds: list[str] | tuple[str, ...] | None = None,
        objective_ids: list[str] | tuple[str, ...] | None = None,
        extra_steps: list[BlueprintStep] | tuple[BlueprintStep, ...] | None = None,
        validate: bool = True,
    ) -> BlueprintHandle:
        """Select → compile → generate in one deterministic pipeline."""
        selection = self.select_blueprint(
            blueprint_type=blueprint_type,
            blueprint_id=blueprint_id,
            intent_tags=intent_tags,
            objective_kinds=objective_kinds,
        )
        compiled = self.compile_blueprint(
            selection.blueprint, extra_steps=extra_steps, validate=validate
        )
        plan = self.generate_plan(compiled, objective_ids=objective_ids)
        return BlueprintHandle(
            blueprint=selection.blueprint,
            compiled=compiled,
            plan=plan,
            selection_rationale=selection.rationale_tags,
        )

    def estimate_effort(
        self,
        blueprint: InstructionalBlueprint,
        *,
        extra_steps: list[BlueprintStep] | tuple[BlueprintStep, ...] | None = None,
    ) -> tuple[EffortBand, int]:
        """Estimate effort band and relative units for a blueprint."""
        compiled = self.compile_blueprint(
            blueprint, extra_steps=extra_steps, validate=False
        )
        return compiled.estimated_effort_band, compiled.estimated_effort_units

    def instructional_structure(
        self, handle: BlueprintHandle
    ) -> InstructionalStructure:
        """Return condensed instructional structure from a handle."""
        compiled = handle.compiled
        plan = handle.plan
        if compiled is None or plan is None:
            compiled = self.compile_blueprint(handle.blueprint)
            plan = self.generate_plan(compiled)
        return InstructionalStructure(
            blueprint_type=compiled.blueprint_type,
            activity_kinds=compiled.activity_kinds,
            step_count=compiled.step_count,
            estimated_effort_band=compiled.estimated_effort_band,
            estimated_effort_units=compiled.estimated_effort_units,
            phase_labels=plan.session_skeleton.phase_labels,
            rationale_tags=compiled.rationale_tags + plan.rationale_tags,
        )

    def session_skeleton(self, handle: BlueprintHandle) -> SessionSkeleton:
        """Return the session skeleton for a handle."""
        if handle.plan is not None:
            return handle.plan.session_skeleton
        compiled = handle.compiled or self.compile_blueprint(handle.blueprint)
        return self._sequences.session_skeleton(compiled)

    def snapshot(self, handle: BlueprintHandle) -> BlueprintSnapshot:
        """Generate an immutable instructional snapshot."""
        validation = self.validate_blueprint(handle.blueprint)
        structure = self.instructional_structure(handle)
        return BlueprintSnapshot(
            blueprint=handle.blueprint,
            compiled=handle.compiled,
            plan=handle.plan,
            structure=structure,
            is_valid=validation.is_valid,
            validation_codes=validation.codes,
        )

    def rehydrate(
        self,
        blueprint: InstructionalBlueprint,
        *,
        compiled: CompiledBlueprint | None = None,
        plan: BlueprintPlan | None = None,
        validate: bool = True,
    ) -> BlueprintHandle:
        """Rebuild a BlueprintHandle from existing artefacts."""
        if validate:
            self.assert_valid(blueprint)
        return BlueprintHandle(
            blueprint=blueprint, compiled=compiled, plan=plan
        )
