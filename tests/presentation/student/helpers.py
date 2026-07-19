"""Shared helpers for Student Experience presentation tests."""

from __future__ import annotations

from app.presentation.student.factory import set_experience_service
from tests.application.student_experience.helpers import make_experience

STUDENT_ROUTES = (
    ("student.home", "/student/"),
    ("student.journey", "/student/journey"),
    ("student.revision", "/student/revision"),
    ("student.history", "/student/history"),
    ("student.profile", "/student/profile"),
)

FORBIDDEN_TERMS = (
    "digital twin",
    "student twin",
    "adaptive decision",
    "learning orchestrator",
    "mission engine",
    "curriculum graph",
)


def wire_experience(app, **kwargs):
    """Install a test StudentExperienceService on the app."""
    service = make_experience(**kwargs)
    set_experience_service(service, app=app)
    return service
