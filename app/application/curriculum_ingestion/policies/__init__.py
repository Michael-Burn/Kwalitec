"""Policy package for Curriculum Ingestion."""

from __future__ import annotations

from typing import Any

__all__ = [
    "ExtractionPolicy",
    "NormalizationPolicy",
    "ValidationPolicy",
]

_EXPORT_MODULES = {
    "ExtractionPolicy": (
        "app.application.curriculum_ingestion.policies.extraction_policy"
    ),
    "NormalizationPolicy": (
        "app.application.curriculum_ingestion.policies.normalization_policy"
    ),
    "ValidationPolicy": (
        "app.application.curriculum_ingestion.policies.validation_policy"
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
