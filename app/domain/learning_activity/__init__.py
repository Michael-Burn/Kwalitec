"""Version 2 Learning Activity domain package.

Pure educational domain objects for activity execution inside a Learning
Session. No Flask, SQLAlchemy, routes, or persistence.

Prefer explicit imports such as
``app.domain.learning_activity.entities.learning_activity``.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "ActivityProgress",
    "ActivityState",
    "ActivityTransitionEvent",
    "ActivityType",
    "LearningActivity",
]

_EXPORT_MODULES = {
    "ActivityProgress": "app.domain.learning_activity.entities.activity_progress",
    "ActivityState": "app.domain.learning_activity.value_objects.activity_state",
    "ActivityTransitionEvent": (
        "app.domain.learning_activity.value_objects.activity_state"
    ),
    "ActivityType": "app.domain.learning_activity.value_objects.activity_type",
    "LearningActivity": "app.domain.learning_activity.entities.learning_activity",
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
