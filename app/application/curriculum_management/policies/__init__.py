"""Policies package for Curriculum Management."""

from __future__ import annotations

from typing import Any

__all__ = [
    "ApprovalPolicy",
    "PublicationPolicy",
    "ValidationPolicy",
    "VersionPolicy",
]

_EXPORT_MODULES = {
    "ApprovalPolicy": (
        "app.application.curriculum_management.policies.approval_policy"
    ),
    "PublicationPolicy": (
        "app.application.curriculum_management.policies.publication_policy"
    ),
    "ValidationPolicy": (
        "app.application.curriculum_management.policies.validation_policy"
    ),
    "VersionPolicy": (
        "app.application.curriculum_management.policies.version_policy"
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
