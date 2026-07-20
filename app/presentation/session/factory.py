"""Factory for Learning Session Experience application service used by the UI.

Presentation wires production adapters into ``SessionExperienceService``.
It does not implement educational logic. Tests may replace the service via
``set_session_experience_service``.
"""

from __future__ import annotations

from flask import Flask, current_app, g, has_app_context

from app.application.session_experience.facade import SessionExperienceService
from app.application.session_experience.ports.activity_engine_port import (
    ActivityEnginePort,
)
from app.application.session_experience.ports.adaptive_decision_port import (
    AdaptiveDecisionPort,
)
from app.application.session_experience.ports.mission_port import MissionPort
from app.application.session_experience.ports.session_runtime_port import (
    SessionRuntimePort,
)
from app.application.session_experience.ports.student_twin_port import (
    StudentTwinPort,
)
from app.infrastructure.session.composition import (
    SessionExperienceComposition,
    build_production_session_experience,
)

_CONFIG_KEY = "SESSION_EXPERIENCE_SERVICE"
_COMPOSITION_KEY = "SESSION_EXPERIENCE_COMPOSITION"
_G_KEY = "session_experience_service"
_G_COMPOSITION_KEY = "session_experience_composition"


def _register_production_builder() -> None:
    """Ensure the facade can construct production adapters without imports."""

    def _builder() -> SessionExperienceService:
        _, service = build_production_session_experience(seed_demo_learners=True)
        return service

    SessionExperienceService.set_production_builder(_builder)


def build_session_experience_service(
    *,
    session_runtime: SessionRuntimePort | None = None,
    activity_engine: ActivityEnginePort | None = None,
    mission: MissionPort | None = None,
    student_twin: StudentTwinPort | None = None,
    adaptive_decision: AdaptiveDecisionPort | None = None,
    composition: SessionExperienceComposition | None = None,
    use_production_adapters: bool = True,
) -> SessionExperienceService:
    """Construct a SessionExperienceService for the presentation layer.

    Production adapters are the default (V2-020A). Explicit port overrides
    win when provided. Pass ``use_production_adapters=False`` only for
    isolated unit tests that inject fakes without infrastructure.
    """
    _register_production_builder()
    if any(
        port is not None
        for port in (
            session_runtime,
            activity_engine,
            mission,
            student_twin,
            adaptive_decision,
        )
    ):
        return SessionExperienceService.create(
            session_runtime=session_runtime,
            activity_engine=activity_engine,
            mission=mission,
            student_twin=student_twin,
            adaptive_decision=adaptive_decision,
            use_production_adapters=False,
        )

    if not use_production_adapters:
        return SessionExperienceService.create(use_production_adapters=False)

    if composition is not None:
        return composition.build_service()

    _composition, service = build_production_session_experience()
    return service


def init_session_experience(
    flask_app: Flask,
    *,
    session_runtime: SessionRuntimePort | None = None,
    activity_engine: ActivityEnginePort | None = None,
    mission: MissionPort | None = None,
    student_twin: StudentTwinPort | None = None,
    adaptive_decision: AdaptiveDecisionPort | None = None,
    use_production_adapters: bool = True,
) -> SessionExperienceService:
    """Register the session experience service on the Flask app."""
    if any(
        port is not None
        for port in (
            session_runtime,
            activity_engine,
            mission,
            student_twin,
            adaptive_decision,
        )
    ):
        service = build_session_experience_service(
            session_runtime=session_runtime,
            activity_engine=activity_engine,
            mission=mission,
            student_twin=student_twin,
            adaptive_decision=adaptive_decision,
            use_production_adapters=False,
        )
        flask_app.config[_CONFIG_KEY] = service
        return service

    if not use_production_adapters:
        service = build_session_experience_service(use_production_adapters=False)
        flask_app.config[_CONFIG_KEY] = service
        return service

    from app.application.config.v2_flags import resolve_v2_feature_flags
    from app.infrastructure.composition import (
        build_experience_projection_store,
        build_session_document_store,
    )

    flags = resolve_v2_feature_flags()
    shared = flask_app.config.get("EXPERIENCE_PROJECTION_STORE")
    if shared is None:
        shared = build_experience_projection_store(flags=flags)
        flask_app.config["EXPERIENCE_PROJECTION_STORE"] = shared
    session_store = build_session_document_store(
        flags=flags, experience_store=shared
    )
    composition, service = build_production_session_experience(
        store=session_store,
        experience_store=shared,
        flags=flags,
    )
    _register_production_builder()
    flask_app.config[_COMPOSITION_KEY] = composition
    flask_app.config[_CONFIG_KEY] = service
    return service


def get_session_experience_composition() -> SessionExperienceComposition | None:
    """Return the production composition root when wired."""
    if has_app_context() and _G_COMPOSITION_KEY in g:
        return g.get(_G_COMPOSITION_KEY)
    if not has_app_context():
        return None
    composition = current_app.config.get(_COMPOSITION_KEY)
    if composition is not None and has_app_context():
        setattr(g, _G_COMPOSITION_KEY, composition)
    return composition


def set_session_experience_service(
    service: SessionExperienceService, *, app: Flask | None = None
) -> None:
    """Replace the session experience service (used by tests)."""
    target = app
    if target is None:
        if not has_app_context():
            raise RuntimeError(
                "set_session_experience_service requires an app or app context"
            )
        target = current_app._get_current_object()  # type: ignore[attr-defined]
        g.pop(_G_KEY, None)
    target.config[_CONFIG_KEY] = service


def get_session_experience_service() -> SessionExperienceService:
    """Return the request/app SessionExperienceService instance."""
    if has_app_context() and _G_KEY in g:
        return g.get(_G_KEY)  # type: ignore[return-value]
    flask_app = current_app
    service = flask_app.config.get(_CONFIG_KEY)
    if service is None:
        service = init_session_experience(flask_app)
    if has_app_context():
        setattr(g, _G_KEY, service)
    return service
