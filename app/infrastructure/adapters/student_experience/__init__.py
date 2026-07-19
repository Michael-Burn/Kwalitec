"""Student Experience production adapter composition (V2-018).

Prefer explicit submodule imports to avoid circular adapter loading:
``app.infrastructure.adapters.student_experience.composition``
``app.infrastructure.adapters.student_experience.defaults``
"""

from __future__ import annotations

__all__ = [
    "ExperienceProjectionStore",
    "PersistedExperienceRegistry",
    "StudentExperienceComposition",
    "build_production_experience",
]


def __getattr__(name: str):
    if name == "ExperienceProjectionStore":
        from app.infrastructure.adapters.student_experience.projection_store import (
            ExperienceProjectionStore,
        )

        return ExperienceProjectionStore
    if name == "PersistedExperienceRegistry":
        from app.infrastructure.adapters.student_experience.registry import (
            PersistedExperienceRegistry,
        )

        return PersistedExperienceRegistry
    if name in {"StudentExperienceComposition", "build_production_experience"}:
        from app.infrastructure.adapters.student_experience import composition as mod

        return getattr(mod, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
