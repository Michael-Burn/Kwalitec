"""Version 2 Instructional Blueprint domain package.

Pure pedagogical structure objects describing HOW topics should be taught.
No curriculum content, no student-specific logic, no Flask / SQLAlchemy.

Prefer explicit imports such as
``app.domain.instructional_blueprint.blueprint.InstructionalBlueprint``.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "BlueprintProfile",
    "BlueprintRule",
    "BlueprintRuleKind",
    "BlueprintStep",
    "BlueprintType",
    "EffortBand",
    "InstructionalBlueprint",
    "effort_at_least",
    "effort_rank",
    "effort_units_for",
    "resolve_effort_band",
]

_EXPORT_MODULES = {
    "BlueprintProfile": "app.domain.instructional_blueprint.blueprint_profile",
    "BlueprintRule": "app.domain.instructional_blueprint.blueprint_rule",
    "BlueprintRuleKind": "app.domain.instructional_blueprint.blueprint_rule",
    "BlueprintStep": "app.domain.instructional_blueprint.blueprint_step",
    "BlueprintType": "app.domain.instructional_blueprint.blueprint_type",
    "EffortBand": "app.domain.instructional_blueprint.effort_band",
    "InstructionalBlueprint": "app.domain.instructional_blueprint.blueprint",
    "effort_at_least": "app.domain.instructional_blueprint.effort_band",
    "effort_rank": "app.domain.instructional_blueprint.effort_band",
    "effort_units_for": "app.domain.instructional_blueprint.effort_band",
    "resolve_effort_band": "app.domain.instructional_blueprint.effort_band",
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
