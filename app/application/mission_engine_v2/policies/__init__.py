"""Stateless scheduling / workload / dispatch / lifecycle policies."""

from __future__ import annotations

from typing import Any

__all__ = [
    "DispatchPolicy",
    "LifecyclePolicy",
    "SchedulingPolicy",
    "WorkloadPolicy",
]

_EXPORT_MODULES = {
    "DispatchPolicy": "app.application.mission_engine_v2.policies.dispatch_policy",
    "LifecyclePolicy": "app.application.mission_engine_v2.policies.lifecycle_policy",
    "SchedulingPolicy": (
        "app.application.mission_engine_v2.policies.scheduling_policy"
    ),
    "WorkloadPolicy": "app.application.mission_engine_v2.policies.workload_policy",
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
