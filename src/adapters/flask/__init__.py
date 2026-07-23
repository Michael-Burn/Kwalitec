"""Flask adapter layer for the Educational Operating System.

Connects HTTP requests to application services and presentation presenters
without introducing Flask into domain or application cores.

Responsibilities: receive HTTP, resolve dependencies, invoke presenters /
application services, map view models to template context, render templates.

Forbidden: educational decisions, persistence, AI, business logic in routes.
"""

from __future__ import annotations

from adapters.flask.dashboard.controller import DashboardController
from adapters.flask.dashboard.dependency_provider import (
    AdapterDependencies,
    FlaskDependencyProvider,
    PipelineResultLoader,
)
from adapters.flask.dashboard.routes import dashboard_bp, register_dashboard
from adapters.flask.experience import (
    ExperienceGateway,
    ExperienceSurfaceController,
    experience_bp,
    register_experience,
)
from adapters.flask.login import login_bp, register_login
from adapters.flask.mission import MissionController, mission_bp, register_mission
from adapters.flask.page_renderer import PageRenderer
from adapters.flask.reflection.controller import ReflectionController
from adapters.flask.reflection.routes import reflection_bp, register_reflection
from adapters.flask.rendering import (
    AccessibilityRenderer,
    ComponentRenderer,
    StyleRenderer,
    TokenRenderer,
)
from adapters.flask.session.controller import SessionController
from adapters.flask.session.routes import register_session, session_bp
from adapters.flask.template_mapper import TemplateMapper
from adapters.flask.wiring import (
    configure_adapter_templates,
    register_adapter_blueprints,
    wire_adapter_layer,
)

# Auth symbols are re-exported lazily to avoid circular import during package load.


def __getattr__(name: str):
    if name in {
        "AuthAdapterDependencies",
        "AuthController",
        "auth_bp",
        "register_auth",
    }:
        from adapters.flask import auth as auth_package

        return getattr(auth_package, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "AccessibilityRenderer",
    "AdapterDependencies",
    "AuthAdapterDependencies",
    "AuthController",
    "ComponentRenderer",
    "DashboardController",
    "ExperienceGateway",
    "ExperienceSurfaceController",
    "FlaskDependencyProvider",
    "MissionController",
    "PageRenderer",
    "PipelineResultLoader",
    "ReflectionController",
    "SessionController",
    "StyleRenderer",
    "TemplateMapper",
    "TokenRenderer",
    "auth_bp",
    "configure_adapter_templates",
    "dashboard_bp",
    "experience_bp",
    "login_bp",
    "mission_bp",
    "reflection_bp",
    "register_adapter_blueprints",
    "register_auth",
    "register_dashboard",
    "register_experience",
    "register_login",
    "register_mission",
    "register_reflection",
    "register_session",
    "session_bp",
    "wire_adapter_layer",
]
