"""Factory for Assessment Delivery service used by the UI."""

from __future__ import annotations

from flask import Flask, current_app, g, has_app_context

from application.assessment.delivery.delivery_service import AssessmentDeliveryService

_CONFIG_KEY = "ASSESSMENT_DELIVERY_SERVICE"
_COMPOSITION_KEY = "ASSESSMENT_DELIVERY_COMPOSITION"
_G_KEY = "assessment_delivery_service"


def build_assessment_delivery_service(
    *, seed: bool = True
) -> AssessmentDeliveryService:
    """Construct a delivery service with in-memory adapters + catalogue seed."""
    from infrastructure.assessment.composition import build_assessment_delivery

    composition = build_assessment_delivery(seed=seed)
    return composition.delivery_service


def init_assessment_delivery(
    flask_app: Flask, *, seed: bool = True
) -> AssessmentDeliveryService:
    """Register the assessment delivery service on the Flask app."""
    from infrastructure.assessment.composition import build_assessment_delivery

    composition = build_assessment_delivery(seed=seed)
    flask_app.config[_COMPOSITION_KEY] = composition
    flask_app.config[_CONFIG_KEY] = composition.delivery_service
    return composition.delivery_service


def set_assessment_delivery_service(
    service: AssessmentDeliveryService, *, app: Flask | None = None
) -> None:
    """Replace the delivery service (used by tests)."""
    target = app
    if target is None:
        if not has_app_context():
            raise RuntimeError(
                "set_assessment_delivery_service requires an app or app context"
            )
        target = current_app._get_current_object()  # type: ignore[attr-defined]
        g.pop(_G_KEY, None)
    target.config[_CONFIG_KEY] = service


def get_assessment_delivery_service() -> AssessmentDeliveryService:
    """Return the request/app AssessmentDeliveryService instance."""
    if has_app_context() and _G_KEY in g:
        return g.get(_G_KEY)  # type: ignore[return-value]
    flask_app = current_app
    service = flask_app.config.get(_CONFIG_KEY)
    if service is None:
        service = init_assessment_delivery(flask_app)
    if has_app_context():
        setattr(g, _G_KEY, service)
    return service
