"""DTO package for the Instructional Blueprint Engine."""

from __future__ import annotations

from typing import Any

__all__ = [
    "ActivityPlanSlot",
    "BlueprintPlan",
    "BlueprintSnapshot",
    "CompiledBlueprint",
    "InstructionalStructure",
    "LearningSequenceEntry",
    "SessionSkeleton",
]

_EXPORT_MODULES = {
    "ActivityPlanSlot": "app.application.instructional_blueprint.dto.blueprint_plan",
    "BlueprintPlan": "app.application.instructional_blueprint.dto.blueprint_plan",
    "BlueprintSnapshot": (
        "app.application.instructional_blueprint.dto.blueprint_snapshot"
    ),
    "CompiledBlueprint": (
        "app.application.instructional_blueprint.dto.compiled_blueprint"
    ),
    "InstructionalStructure": (
        "app.application.instructional_blueprint.dto.blueprint_snapshot"
    ),
    "LearningSequenceEntry": (
        "app.application.instructional_blueprint.dto.blueprint_plan"
    ),
    "SessionSkeleton": "app.application.instructional_blueprint.dto.blueprint_plan",
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
