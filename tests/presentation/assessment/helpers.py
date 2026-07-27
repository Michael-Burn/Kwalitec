"""Presentation helpers for Assessment Delivery tests."""

from __future__ import annotations

from app.presentation.assessment.factory import set_assessment_delivery_service
from infrastructure.assessment.composition import build_assessment_delivery

FORBIDDEN_TERMS = (
    "digital twin",
    "mastery score",
    "mission engine",
    "pass/fail",
    "failed",
)


def wire_assessment_delivery(app, **kwargs):
    composition = build_assessment_delivery(seed=True)
    set_assessment_delivery_service(composition.delivery_service, app=app)
    return composition
