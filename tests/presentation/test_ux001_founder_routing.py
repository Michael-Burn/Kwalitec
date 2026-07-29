"""UX-001 — Founder-first landing and role routing matrix."""

from __future__ import annotations

from unittest.mock import patch

from app.extensions import db
from app.models import User
from app.presentation.consolidation import (
    CANONICAL_HOME_ENDPOINT,
    CONSOLE_HOME_ENDPOINT,
    canonical_home_endpoint,
)
from app.security.roles import Role
from app.services.identity_service import IdentityService
from tests.presentation.workflows.helpers import dual_run_flags


def _make_user(email: str) -> User:
    user = User(email=email, is_active_user=True)
    user.set_password("password123")
    user.alpha_onboarding_completed = True
    db.session.add(user)
    db.session.commit()
    return user


def _login_post(client, email: str):
    return client.post(
        "/auth/login",
        data={"email": email, "password": "password123"},
        follow_redirects=False,
    )


def _assert_lands_on_console(response) -> None:
    assert response.status_code in {302, 303}
    location = response.headers.get("Location", "")
    assert "/console/" in location
    assert "/student" not in location


def _assert_lands_on_student_os(response) -> None:
    assert response.status_code in {302, 303}
    location = response.headers.get("Location", "")
    assert "/console/" not in location
    assert any(
        token in location for token in ("/student", "study-plan", "alpha/onboarding")
    )


def test_founder_login_lands_on_console(app, client, ctx):
    user = _make_user("ux001-founder@kwalitec.example")
    IdentityService.grant_role(user, Role.FOUNDER)
    _assert_lands_on_console(_login_post(client, user.email))


def test_administrator_login_lands_on_console_without_capabilities(app, client, ctx):
    """Administrator role alone (no UserCapability rows) → Console."""
    user = _make_user("ux001-admin@kwalitec.example")
    IdentityService.grant_role(user, Role.ADMINISTRATOR)
    db.session.refresh(user)
    assert not user.get_capabilities()
    _assert_lands_on_console(_login_post(client, user.email))


def test_student_only_login_lands_on_student_os(app, client, ctx):
    user = _make_user("ux001-student@kwalitec.example")
    IdentityService.ensure_student_defaults(user)
    _assert_lands_on_student_os(_login_post(client, user.email))


def test_founder_plus_student_lands_on_console(app, client, ctx):
    user = _make_user("ux001-founder-student@kwalitec.example")
    IdentityService.grant_role(user, Role.FOUNDER)
    IdentityService.grant_role(user, Role.STUDENT)
    _assert_lands_on_console(_login_post(client, user.email))


def test_administrator_plus_student_lands_on_console(app, client, ctx):
    user = _make_user("ux001-admin-student@kwalitec.example")
    IdentityService.grant_role(user, Role.ADMINISTRATOR)
    IdentityService.grant_role(user, Role.STUDENT)
    _assert_lands_on_console(_login_post(client, user.email))


def test_canonical_home_endpoint_role_matrix(app, client, ctx):
    """Authenticated home endpoint follows Console vs Student OS rules."""
    founder = _make_user("ux001-home-founder@kwalitec.example")
    IdentityService.grant_role(founder, Role.FOUNDER)
    admin = _make_user("ux001-home-admin@kwalitec.example")
    IdentityService.grant_role(admin, Role.ADMINISTRATOR)
    student = _make_user("ux001-home-student@kwalitec.example")
    IdentityService.ensure_student_defaults(student)

    with patch(
        "app.presentation.consolidation.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=True),
    ):
        for user, expected in (
            (founder, CONSOLE_HOME_ENDPOINT),
            (admin, CONSOLE_HOME_ENDPOINT),
            (student, CANONICAL_HOME_ENDPOINT),
        ):
            client.post(
                "/auth/login",
                data={"email": user.email, "password": "password123"},
                follow_redirects=True,
            )
            with client:
                client.get("/")
                assert canonical_home_endpoint() == expected, user.email
            client.post("/auth/logout")


def test_console_exposes_enter_student_experience(app, client, ctx):
    user = _make_user("ux001-entry@kwalitec.example")
    IdentityService.ensure_founder_admin(user)
    client.post(
        "/auth/login",
        data={"email": user.email, "password": "password123"},
        follow_redirects=True,
    )
    response = client.get("/console/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Enter Student Experience" in html
    assert 'data-testid="enter-student-experience"' in html
    assert "/student/" in html
