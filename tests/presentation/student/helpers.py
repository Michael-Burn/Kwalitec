"""Shared helpers for Student Experience presentation tests."""

from __future__ import annotations

from flask import render_template

from app.presentation.student.factory import set_experience_service
from app.presentation.student.services.student_home_service import (
    StudentHomeService,
)
from app.presentation.student.view_models import (
    HomePageViewModel,
    StudentPageViewModel,
    StudentShellViewModel,
)
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


def render_student_home(
    app,
    page_home: HomePageViewModel | None,
    *,
    form=None,
    **template_kwargs,
):
    """Render student/home.html with DX-005A ``home`` DTO projection."""
    page = StudentPageViewModel(
        shell=StudentShellViewModel(
            active_surface="home",
            active_label="Home",
            navigation=(),
            page_title="Home",
        ),
        home=page_home,
        educational=None,
    )
    with app.test_request_context("/student/"):
        home = StudentHomeService().build_home(page)
        return render_template(
            "student/home.html",
            page=page,
            home=home,
            form=form,
            **template_kwargs,
        )
