"""Presentation helpers for Learning Session Experience."""

from __future__ import annotations

from app.presentation.session.factory import set_session_experience_service
from tests.application.session_experience.helpers import make_session_experience

SESSION_ROUTES = (
    ("session.overview", "/session/sess-1/overview"),
    ("session.activity", "/session/sess-1/activity"),
    ("session.reflection", "/session/sess-1/reflection"),
    ("session.summary", "/session/sess-1/summary"),
    ("session.complete", "/session/sess-1/complete"),
)

FORBIDDEN_TERMS = (
    "digital twin",
    "student twin",
    "adaptive decision",
    "learning orchestrator",
    "mission engine",
    "curriculum graph",
    "mastery score",
)


def wire_session_experience(app, **kwargs):
    service = make_session_experience(**kwargs)
    set_session_experience_service(service, app=app)
    return service
