"""Factory for Student Experience application service used by the UI.

Presentation wires production adapters into ``StudentExperienceService``.
It does not implement educational logic. Tests may replace the service via
``set_experience_service``.
"""

from __future__ import annotations

from flask import Flask, current_app, g, has_app_context

from app.application.student_experience.ports.adaptive_decision_port import (
    AdaptiveDecisionPort,
)
from app.application.student_experience.ports.learning_journey_port import (
    LearningJourneyPort,
)
from app.application.student_experience.ports.learning_orchestrator_port import (
    LearningOrchestratorPort,
)
from app.application.student_experience.ports.mission_port import MissionPort
from app.application.student_experience.ports.student_twin_port import (
    StudentTwinPort,
)
from app.application.student_experience.student_experience_service import (
    StudentExperienceService,
)
from app.infrastructure.adapters.student_experience.composition import (
    StudentExperienceComposition,
    build_production_experience,
)

_CONFIG_KEY = "STUDENT_EXPERIENCE_SERVICE"
_COMPOSITION_KEY = "STUDENT_EXPERIENCE_COMPOSITION"
_G_KEY = "student_experience_service"
_G_COMPOSITION_KEY = "student_experience_composition"


def build_experience_service(
    *,
    student_twin: StudentTwinPort | None = None,
    adaptive_decision: AdaptiveDecisionPort | None = None,
    mission: MissionPort | None = None,
    learning_journey: LearningJourneyPort | None = None,
    learning_orchestrator: LearningOrchestratorPort | None = None,
    composition: StudentExperienceComposition | None = None,
    use_production_adapters: bool = True,
) -> StudentExperienceService:
    """Construct a StudentExperienceService for the presentation layer.

    Production adapters are the default (V2-018). Explicit port overrides
    win when provided. Pass ``use_production_adapters=False`` only for
    isolated unit tests that inject fakes without infrastructure.
    """
    if any(
        port is not None
        for port in (
            student_twin,
            adaptive_decision,
            mission,
            learning_journey,
            learning_orchestrator,
        )
    ):
        return StudentExperienceService(
            student_twin=student_twin,
            adaptive_decision=adaptive_decision,
            mission=mission,
            learning_journey=learning_journey,
            learning_orchestrator=learning_orchestrator,
        )

    if not use_production_adapters:
        return StudentExperienceService()

    if composition is not None:
        return composition.build_service()

    _composition, service = build_production_experience()
    return service


def init_student_experience(flask_app: Flask) -> StudentExperienceService:
    """Register the production experience service on the Flask app."""
    from app.application.config.v2_flags import resolve_v2_feature_flags
    from app.infrastructure.composition import build_experience_projection_store

    flags = resolve_v2_feature_flags()
    store = build_experience_projection_store(flags=flags)
    flask_app.config["EXPERIENCE_PROJECTION_STORE"] = store
    composition, service = build_production_experience(store=store, flags=flags)
    flask_app.config[_COMPOSITION_KEY] = composition
    flask_app.config[_CONFIG_KEY] = service
    return service


def get_experience_composition() -> StudentExperienceComposition | None:
    """Return the production composition root when wired."""
    if has_app_context() and _G_COMPOSITION_KEY in g:
        return g.get(_G_COMPOSITION_KEY)
    if not has_app_context():
        return None
    composition = current_app.config.get(_COMPOSITION_KEY)
    if composition is not None and has_app_context():
        setattr(g, _G_COMPOSITION_KEY, composition)
    return composition


def set_experience_service(
    service: StudentExperienceService, *, app: Flask | None = None
) -> None:
    """Replace the experience service (used by tests)."""
    target = app
    if target is None:
        if not has_app_context():
            raise RuntimeError(
                "set_experience_service requires an app or app context"
            )
        target = current_app._get_current_object()  # type: ignore[attr-defined]
        g.pop(_G_KEY, None)
    target.config[_CONFIG_KEY] = service


def get_experience_service() -> StudentExperienceService:
    """Return the request/app StudentExperienceService instance."""
    if has_app_context() and _G_KEY in g:
        return g.get(_G_KEY)  # type: ignore[return-value]
    flask_app = current_app
    service = flask_app.config.get(_CONFIG_KEY)
    if service is None:
        service = init_student_experience(flask_app)
    if has_app_context():
        setattr(g, _G_KEY, service)
    return service
