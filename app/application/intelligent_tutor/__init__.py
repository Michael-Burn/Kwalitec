"""Application layer for the Evidence-Backed Intelligent Tutor (TUTOR-001)."""

from __future__ import annotations

from typing import Any

__all__ = [
    "DeterministicTutorGeneration",
    "IntelligentTutorService",
    "TutorGenerationPort",
    "TutorGenerationRequest",
    "TutorGenerationResult",
]

_EXPORT_MODULES = {
    "TutorGenerationPort": (
        "app.application.intelligent_tutor.ports.tutor_generation_port"
    ),
    "TutorGenerationRequest": (
        "app.application.intelligent_tutor.ports.tutor_generation_port"
    ),
    "TutorGenerationResult": (
        "app.application.intelligent_tutor.ports.tutor_generation_port"
    ),
    "DeterministicTutorGeneration": (
        "app.application.intelligent_tutor.ports.deterministic_tutor_generation"
    ),
    "IntelligentTutorService": (
        "app.application.intelligent_tutor.intelligent_tutor_service"
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
