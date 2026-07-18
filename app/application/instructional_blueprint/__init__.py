"""Version 2 Instructional Blueprint Engine — application layer.

Reusable pedagogical engine defining HOW topics should be taught as
structured activity flows. No curriculum content. No student-specific logic.

Framework-independent: no Flask, SQLAlchemy, UI, migrations, or persistence.

Prefer explicit imports such as
``app.application.instructional_blueprint.engine.InstructionalBlueprintEngine``.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "ActivityPlanSlot",
    "BlueprintAlreadyRegistered",
    "BlueprintCompilationError",
    "BlueprintCompiler",
    "BlueprintHandle",
    "BlueprintNotFound",
    "BlueprintPlan",
    "BlueprintRegistry",
    "BlueprintSelectionError",
    "BlueprintSelector",
    "BlueprintSnapshot",
    "BlueprintValidationError",
    "BlueprintValidator",
    "CompilationPolicy",
    "CompiledBlueprint",
    "InstructionalBlueprintEngine",
    "InstructionalBlueprintEngineError",
    "InstructionalStructure",
    "LearningSequenceEntry",
    "RegistryError",
    "SelectionPolicy",
    "SelectionResult",
    "SequenceGenerationError",
    "SequenceGenerator",
    "SessionSkeleton",
    "ValidationIssue",
    "ValidationResult",
]

_EXPORT_MODULES = {
    "ActivityPlanSlot": "app.application.instructional_blueprint.dto.blueprint_plan",
    "BlueprintAlreadyRegistered": "app.application.instructional_blueprint.exceptions",
    "BlueprintCompilationError": "app.application.instructional_blueprint.exceptions",
    "BlueprintCompiler": "app.application.instructional_blueprint.blueprint_compiler",
    "BlueprintHandle": "app.application.instructional_blueprint.engine",
    "BlueprintNotFound": "app.application.instructional_blueprint.exceptions",
    "BlueprintPlan": "app.application.instructional_blueprint.dto.blueprint_plan",
    "BlueprintRegistry": "app.application.instructional_blueprint.blueprint_registry",
    "BlueprintSelectionError": "app.application.instructional_blueprint.exceptions",
    "BlueprintSelector": "app.application.instructional_blueprint.blueprint_selector",
    "BlueprintSnapshot": (
        "app.application.instructional_blueprint.dto.blueprint_snapshot"
    ),
    "BlueprintValidationError": "app.application.instructional_blueprint.exceptions",
    "BlueprintValidator": (
        "app.application.instructional_blueprint.blueprint_validator"
    ),
    "CompilationPolicy": (
        "app.application.instructional_blueprint.policies.compilation_policy"
    ),
    "CompiledBlueprint": (
        "app.application.instructional_blueprint.dto.compiled_blueprint"
    ),
    "InstructionalBlueprintEngine": (
        "app.application.instructional_blueprint.engine"
    ),
    "InstructionalBlueprintEngineError": (
        "app.application.instructional_blueprint.exceptions"
    ),
    "InstructionalStructure": (
        "app.application.instructional_blueprint.dto.blueprint_snapshot"
    ),
    "LearningSequenceEntry": (
        "app.application.instructional_blueprint.dto.blueprint_plan"
    ),
    "RegistryError": "app.application.instructional_blueprint.exceptions",
    "SelectionPolicy": (
        "app.application.instructional_blueprint.policies.selection_policy"
    ),
    "SelectionResult": "app.application.instructional_blueprint.blueprint_selector",
    "SequenceGenerationError": "app.application.instructional_blueprint.exceptions",
    "SequenceGenerator": (
        "app.application.instructional_blueprint.sequence_generator"
    ),
    "SessionSkeleton": "app.application.instructional_blueprint.dto.blueprint_plan",
    "ValidationIssue": "app.application.instructional_blueprint.blueprint_validator",
    "ValidationResult": "app.application.instructional_blueprint.blueprint_validator",
}


def __getattr__(name: str) -> Any:
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from importlib import import_module

    module = import_module(module_name)
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
