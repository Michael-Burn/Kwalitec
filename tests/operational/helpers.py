"""Shared helpers for ARP-005 operational readiness tests."""

from __future__ import annotations

from pathlib import Path

from flask import Flask

from app.application.config.v2_flags import Version2FeatureFlags
from app.presentation.curriculum_studio.factory import set_studio_service
from app.presentation.session.factory import set_session_experience_service
from app.presentation.student.factory import set_experience_service
from tests.application.curriculum_studio.helpers import make_studio_with_ports
from tests.application.session_experience.helpers import make_session_experience
from tests.application.student_experience.helpers import make_experience
from tests.presentation.curriculum_studio.helpers import login_founder

REPO_ROOT = Path(__file__).resolve().parents[2]

ALPHA_DUAL_RUN_ENV = {
    "KWALITEC_V2_STUDENT_EXPERIENCE": "1",
    "KWALITEC_V2_DURABLE_STORE": "1",
    "KWALITEC_V2_INJECT_ENGINES": "1",
    "KWALITEC_V2_SEED_DEMO": "0",
    "KWALITEC_V2_FOUNDER_INTELLIGENCE": "1",
}

REQUIRED_BLUEPRINTS = (
    "auth",
    "dashboard",
    "student",
    "session",
    "curriculum_studio",
    "founder_dashboard",
    "mission",
    "study_plan",
    "analytics",
    "settings",
    "calibration",
)

ALPHA_ENV_VARS = (
    "KWALITEC_V2_STUDENT_EXPERIENCE",
    "KWALITEC_V2_DURABLE_STORE",
    "KWALITEC_V2_INJECT_ENGINES",
    "KWALITEC_V2_SEED_DEMO",
    "KWALITEC_V2_FOUNDER_INTELLIGENCE",
    "KWALITEC_V2_SOLE_RUNTIME",
)

FOUNDER_SMOKE_PATHS = (
    "/founder/studio/",
    "/founder/intelligence",
    "/founder/evidence-gates",
)

STUDENT_SMOKE_PATHS = (
    "/student/",
    "/student/journey",
    "/student/revision",
    "/student/history",
    "/student/profile",
)

REQUIRED_STATIC_FILES = (
    "app/static/css/fonts.css",
    "app/static/css/brand.css",
    "app/static/css/tokens.css",
    "app/static/css/app.css",
    "app/static/css/student.css",
    "app/static/css/session.css",
    "app/static/fonts/inter/inter-latin-400-normal.woff2",
    "app/static/fonts/inter/inter-latin-500-normal.woff2",
    "app/static/fonts/inter/inter-latin-600-normal.woff2",
    "app/static/fonts/inter/inter-latin-700-normal.woff2",
    "app/founder/dashboard/static/css/founder_dashboard.css",
)

REQUIRED_TEMPLATES = (
    "app/templates/session/base.html",
    "app/templates/session/overview.html",
    "app/templates/session/activity.html",
    "app/templates/session/reflection.html",
    "app/templates/session/summary.html",
    "app/templates/session/complete.html",
    "app/templates/student/home.html",
    "app/templates/student/journey.html",
    "app/templates/student/revision.html",
    "app/templates/curriculum_studio/dashboard.html",
    "app/templates/partials/skeleton.html",
    "app/templates/partials/empty_state.html",
    "app/templates/curriculum_studio/workspace.html",
    "app/founder/dashboard/templates/founder_dashboard/founder_intelligence.html",
    "app/founder/dashboard/templates/founder_dashboard/evidence_gates.html",
    "app/templates/errors/403.html",
    "app/templates/errors/404.html",
    "app/templates/errors/500.html",
)

ALEMBIC_HEAD = "202607190002"

ALPHA_HTTP_ROUTES = (
    "/health",
    "/",
    "/student/",
    "/student/journey",
    "/student/revision",
    "/founder/studio/",
    "/founder/intelligence",
    "/founder/evidence-gates",
    "/dashboard/",
    "/auth/login",
)

SESSION_SURFACE_ROUTES = (
    "/session/<session_id>/overview",
    "/session/<session_id>/activity",
    "/session/<session_id>/reflection",
    "/session/<session_id>/summary",
    "/session/<session_id>/complete",
)


def alpha_flags(**overrides) -> Version2FeatureFlags:
    base = {
        "ENABLE_STUDENT_EXPERIENCE": True,
        "ENABLE_DURABLE_STORE": True,
        "SEED_DEMO_LEARNERS": False,
        "INJECT_PHASE_I_ENGINES": True,
        "SOLE_RUNTIME": False,
        "ENABLE_FOUNDER_INTELLIGENCE": True,
    }
    base.update(overrides)
    return Version2FeatureFlags(**base)


def wire_student(app: Flask, **kwargs):
    service = make_experience(**kwargs)
    set_experience_service(service, app=app)
    return service


def wire_session(app: Flask, **kwargs):
    service = make_session_experience(**kwargs)
    set_session_experience_service(service, app=app)
    return service


def wire_studio(app: Flask, **kwargs):
    studio, *_ = make_studio_with_ports(**kwargs)
    set_studio_service(studio, app=app)
    return studio


def login_student(client, *, email: str = "test@kwalitec.example") -> None:
    client.post(
        "/auth/login",
        data={"email": email, "password": "password123"},
        follow_redirects=True,
    )


def render_env_map() -> dict[str, str]:
    """Parse simple key/value pairs from render.yaml without PyYAML."""
    text = (REPO_ROOT / "render.yaml").read_text(encoding="utf-8")
    env: dict[str, str] = {}
    current_key: str | None = None
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("- key:"):
            current_key = line.split(":", 1)[1].strip()
        elif current_key and line.startswith("value:"):
            env[current_key] = line.split(":", 1)[1].strip().strip('"')
            current_key = None
        elif current_key and (
            line.startswith("generateValue:") or line.startswith("fromDatabase:")
        ):
            # Non-literal values — record presence without a string value.
            env.setdefault(current_key, f"<{line.split(':', 1)[0]}>")
            current_key = None
        elif current_key and line.startswith("sync:"):
            env.setdefault(current_key, f"<sync:{line.split(':', 1)[1].strip()}>")
            current_key = None
    return env


__all__ = [
    "ALEMBIC_HEAD",
    "ALPHA_DUAL_RUN_ENV",
    "ALPHA_ENV_VARS",
    "ALPHA_HTTP_ROUTES",
    "FOUNDER_SMOKE_PATHS",
    "REPO_ROOT",
    "REQUIRED_BLUEPRINTS",
    "REQUIRED_STATIC_FILES",
    "REQUIRED_TEMPLATES",
    "SESSION_SURFACE_ROUTES",
    "STUDENT_SMOKE_PATHS",
    "alpha_flags",
    "login_founder",
    "login_student",
    "render_env_map",
    "wire_session",
    "wire_student",
    "wire_studio",
]
