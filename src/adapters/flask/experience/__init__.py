"""Live Experience Wiring adapters (R1-001).

Connects ``ExperienceIntegrationService`` to Flask student-flow surfaces via
dependency injection. Projection / wiring only — no educational reasoning.
"""

from __future__ import annotations

from adapters.flask.experience.gateway import (
    EXPERIENCE_CACHE_G_KEY,
    ExperienceGateway,
    MappingPriorReadinessStore,
)
from adapters.flask.experience.inputs_builder import (
    build_home_inputs,
    build_integration_inputs,
)
from adapters.flask.experience.surface_presenter import (
    ExperienceSurfacePresenter,
    ExperienceSurfaceView,
)

__all__ = [
    "EXPERIENCE_CACHE_G_KEY",
    "ExperienceGateway",
    "ExperienceSurfaceController",
    "ExperienceSurfacePresenter",
    "ExperienceSurfaceView",
    "MappingPriorReadinessStore",
    "build_home_inputs",
    "build_integration_inputs",
    "experience_bp",
    "register_experience",
]


def __getattr__(name: str):
    if name == "ExperienceSurfaceController":
        from adapters.flask.experience.controller import ExperienceSurfaceController

        return ExperienceSurfaceController
    if name in {"experience_bp", "register_experience"}:
        from adapters.flask.experience import routes as experience_routes

        return getattr(experience_routes, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name}")
