"""Shared helpers for ARP-003 workflow validation tests."""

from __future__ import annotations

from flask import Flask

from app.application.config.v2_flags import Version2FeatureFlags
from app.domain.session_experience.session_workspace import SessionSurface
from app.founder.dashboard.nav import COMMAND_CENTRE_NAV
from app.presentation.session.factory import set_session_experience_service
from tests.application.session_experience.helpers import (
    FakeActivityEnginePort,
    make_session_experience,
)
from tests.presentation.curriculum_studio.helpers import (
    login_founder,
    make_founder_user,
    wire_studio,
)

FOUNDER_WORKFLOW_STAGES = (
    "Subject",
    "Content Sources",
    "Validation",
    "Preview",
    "Approval",
    "Publish",
)

STUDENT_SESSION_FLOW = (
    SessionSurface.OVERVIEW,
    SessionSurface.ACTIVITY,
    SessionSurface.REFLECTION,
    SessionSurface.SUMMARY,
    SessionSurface.COMPLETE,
)

ALPHA_PRIMARY_NAV = ("Studio", "Intelligence", "Evidence Gates")


def wire_session(app: Flask, **kwargs):
    service = make_session_experience(**kwargs)
    set_session_experience_service(service, app=app)
    return service


def login_student(client, *, email: str = "test@kwalitec.example") -> None:
    client.post(
        "/auth/login",
        data={"email": email, "password": "password123"},
        follow_redirects=True,
    )


def advance_workspace_to(service, session_id: str, surface: SessionSurface):
    ws = service.registry.get_workspace_for_session(session_id)
    assert ws is not None
    for step in STUDENT_SESSION_FLOW:
        ws = ws.navigate_to(step)
        service.registry.put_workspace(ws)
        if step is surface:
            break
    return ws


def dual_run_flags(**overrides) -> Version2FeatureFlags:
    base = {
        "ENABLE_STUDENT_EXPERIENCE": True,
        "ENABLE_DURABLE_STORE": False,
        "SEED_DEMO_LEARNERS": False,
        "INJECT_PHASE_I_ENGINES": False,
        "SOLE_RUNTIME": False,
        "ENABLE_FOUNDER_INTELLIGENCE": True,
    }
    base.update(overrides)
    return Version2FeatureFlags(**base)


def primary_nav_labels() -> list[str]:
    return [item.label for item in COMMAND_CENTRE_NAV]


def surface_path(session_id: str, surface: SessionSurface) -> str:
    suffix = {
        SessionSurface.OVERVIEW: "overview",
        SessionSurface.ACTIVITY: "activity",
        SessionSurface.REFLECTION: "reflection",
        SessionSurface.SUMMARY: "summary",
        SessionSurface.COMPLETE: "complete",
    }[surface]
    return f"/session/{session_id}/{suffix}"


__all__ = [
    "ALPHA_PRIMARY_NAV",
    "FOUNDER_WORKFLOW_STAGES",
    "STUDENT_SESSION_FLOW",
    "FakeActivityEnginePort",
    "advance_workspace_to",
    "dual_run_flags",
    "login_founder",
    "login_student",
    "make_founder_user",
    "primary_nav_labels",
    "surface_path",
    "wire_session",
    "wire_studio",
]
