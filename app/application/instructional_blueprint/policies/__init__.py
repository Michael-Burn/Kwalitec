"""Policy package for the Instructional Blueprint Engine."""

from __future__ import annotations

from typing import Any

__all__ = [
    "CompilationPolicy",
    "SelectionPolicy",
]

_EXPORT_MODULES = {
    "CompilationPolicy": (
        "app.application.instructional_blueprint.policies.compilation_policy"
    ),
    "SelectionPolicy": (
        "app.application.instructional_blueprint.policies.selection_policy"
    ),
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
