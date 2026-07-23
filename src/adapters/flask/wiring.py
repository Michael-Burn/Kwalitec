"""Wire the Flask HTML adapter layer onto an Education OS application.

Connects templates, dependency injection, and student-flow blueprints.
No educational logic. Does not import the web package (avoids cycles).
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from flask import Flask, session
from jinja2 import ChoiceLoader, FileSystemLoader

from adapters.flask.auth.dependency_provider import AuthAdapterDependencies
from adapters.flask.auth.routes import register_auth
from adapters.flask.checkpoint_store import (
    CheckpointStore,
    MappingCheckpointStore,
)
from adapters.flask.dashboard.dependency_provider import (
    AdapterDependencies,
    FlaskDependencyProvider,
    flask_student_id_resolver,
)
from adapters.flask.dashboard.routes import register_dashboard
from adapters.flask.experience.routes import register_experience
from adapters.flask.login.routes import register_login
from adapters.flask.mission.routes import register_mission
from adapters.flask.onboarding.dependency_provider import OnboardingAdapterDependencies
from adapters.flask.onboarding.routes import register_onboarding
from adapters.flask.reflection.routes import register_reflection
from adapters.flask.rendering import TEMPLATES_DIR
from adapters.flask.session.routes import register_session
from application.evidence_capture.captured_evidence import CapturedEvidence


def configure_adapter_templates(app: Flask) -> Path:
    """Point Flask Jinja at Design System + eos page templates."""
    adapter_loader = FileSystemLoader(str(TEMPLATES_DIR))
    existing = app.jinja_loader
    if existing is None:
        app.jinja_loader = adapter_loader
    else:
        app.jinja_loader = ChoiceLoader([adapter_loader, existing])
    return TEMPLATES_DIR


def build_adapter_dependencies(
    container: Any,
    *,
    request_builder: Callable[[str], Any] | None = None,
    update_evidence: Callable[[CapturedEvidence], Any] | None = None,
    checkpoint_store: CheckpointStore | None = None,
) -> AdapterDependencies:
    """Assemble adapter dependencies for HTML student-flow surfaces."""
    product = getattr(container, "product", None)
    resolved_store = checkpoint_store
    if resolved_store is None and product is not None:
        resolved_store = product.checkpoint_store
    return FlaskDependencyProvider.from_container(
        container,
        request_builder=request_builder,
        student_id_resolver=flask_student_id_resolver,
        update_evidence=update_evidence,
        checkpoint_store=resolved_store,
    )


def register_adapter_blueprints(
    app: object,
    *,
    auth_dependencies: AuthAdapterDependencies | None = None,
    onboarding_dependencies: OnboardingAdapterDependencies | None = None,
) -> None:
    """Register student-flow blueprints including auth and onboarding.

    Auth and onboarding blueprints register only when explicit dependencies are
    supplied. Production ``wire_adapter_layer`` always provides SQLAlchemy-backed
    collaborators; adapter unit tests may omit them.
    """
    if auth_dependencies is not None:
        register_auth(app, dependencies=auth_dependencies)
    if onboarding_dependencies is not None:
        register_onboarding(app, dependencies=onboarding_dependencies)
    register_login(app)
    register_dashboard(app)
    register_experience(app)
    register_mission(app)
    register_session(app)
    register_reflection(app)


def wire_adapter_layer(
    app: Flask,
    container: Any,
    *,
    request_builder: Callable[[str], Any] | None = None,
    update_evidence: Callable[[CapturedEvidence], Any] | None = None,
    checkpoint_store: CheckpointStore | None = None,
    auth_dependencies: AuthAdapterDependencies | None = None,
    onboarding_dependencies: OnboardingAdapterDependencies | None = None,
) -> AdapterDependencies:
    """Configure templates, bind dependencies, and register blueprints.

    When ``container.product`` is present (production composition), auth,
    onboarding, and checkpoints are taken from SqlAlchemyProductUnitOfWork
    wiring. Explicit overrides still win for tests.
    """
    configure_adapter_templates(app)
    builder = request_builder or app.extensions.get("eos_pipeline_request_builder")
    updater = update_evidence or app.extensions.get("eos_evidence_updater")
    product = getattr(container, "product", None)

    resolved_auth = auth_dependencies
    if resolved_auth is None and product is not None:
        resolved_auth = AuthAdapterDependencies(
            auth_service=product.authentication,  # type: ignore[arg-type]
        )
    if resolved_auth is None:
        raise TypeError(
            "auth_dependencies required when container.product is absent"
        )

    resolved_onboarding = onboarding_dependencies
    if resolved_onboarding is None and product is not None:
        resolved_onboarding = OnboardingAdapterDependencies(
            onboarding_service=product.onboarding,  # type: ignore[arg-type]
        )
    if resolved_onboarding is None:
        raise TypeError(
            "onboarding_dependencies required when container.product is absent"
        )

    resolved_store = checkpoint_store
    if resolved_store is None and product is not None:
        resolved_store = product.checkpoint_store

    deps = build_adapter_dependencies(
        container,
        request_builder=builder,
        update_evidence=updater,
        checkpoint_store=resolved_store,
    )
    FlaskDependencyProvider.bind(app, deps)
    register_adapter_blueprints(
        app,
        auth_dependencies=resolved_auth,
        onboarding_dependencies=resolved_onboarding,
    )
    return deps


def flask_session_checkpoint_store() -> MappingCheckpointStore:
    """Checkpoint store backed by the active Flask session mapping."""
    return MappingCheckpointStore(session)
