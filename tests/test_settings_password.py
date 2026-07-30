"""Tests for authenticated password change (settings)."""

from __future__ import annotations

from app.extensions import db
from app.models.user import User


def test_change_password_page_requires_login(client):
    response = client.get("/settings/password", follow_redirects=False)
    assert response.status_code in {302, 303}
    assert "/auth/login" in (response.headers.get("Location") or "")


def test_change_password_page_renders(logged_in_client):
    response = logged_in_client.get("/settings/password")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Change password" in body
    assert 'name="current_password"' in body
    assert 'name="new_password"' in body
    assert 'name="confirm_password"' in body


def test_student_profile_links_to_change_password(logged_in_client):
    response = logged_in_client.get("/student/profile")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "/settings/password" in body
    assert "Change your sign-in password" in body


def test_change_password_success(logged_in_client, ctx):
    response = logged_in_client.post(
        "/settings/password",
        data={
            "current_password": "password123",
            "new_password": "FamiliarPass1",
            "confirm_password": "FamiliarPass1",
            "submit": "Update password",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Password updated" in response.data

    user = User.query.filter_by(email="test@kwalitec.example").one()
    assert user.check_password("FamiliarPass1")
    assert not user.check_password("password123")


def test_change_password_rejects_wrong_current(logged_in_client, ctx):
    response = logged_in_client.post(
        "/settings/password",
        data={
            "current_password": "wrong-password",
            "new_password": "FamiliarPass1",
            "confirm_password": "FamiliarPass1",
            "submit": "Update password",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Current password is incorrect" in response.data

    user = User.query.filter_by(email="test@kwalitec.example").one()
    assert user.check_password("password123")


def test_change_password_rejects_mismatch(logged_in_client, ctx):
    response = logged_in_client.post(
        "/settings/password",
        data={
            "current_password": "password123",
            "new_password": "FamiliarPass1",
            "confirm_password": "DifferentPass1",
            "submit": "Update password",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"must match" in response.data

    user = User.query.filter_by(email="test@kwalitec.example").one()
    assert user.check_password("password123")


def test_change_password_rejects_too_short(logged_in_client, ctx):
    response = logged_in_client.post(
        "/settings/password",
        data={
            "current_password": "password123",
            "new_password": "short",
            "confirm_password": "short",
            "submit": "Update password",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"at least 8 characters" in response.data

    user = User.query.filter_by(email="test@kwalitec.example").one()
    assert user.check_password("password123")


def test_change_password_rejects_same_as_current(logged_in_client, ctx):
    response = logged_in_client.post(
        "/settings/password",
        data={
            "current_password": "password123",
            "new_password": "password123",
            "confirm_password": "password123",
            "submit": "Update password",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"differs from your current" in response.data
    db.session.expire_all()
    user = User.query.filter_by(email="test@kwalitec.example").one()
    assert user.check_password("password123")


def test_change_password_then_logout_then_login(client, ctx):
    """After change + logout, only the new password grants access."""
    user = User(email="roundtrip@kwalitec.example", is_active_user=True)
    user.set_password("OldPassword1")
    user.alpha_onboarding_completed = True
    db.session.add(user)
    db.session.commit()

    login = client.post(
        "/auth/login",
        data={"email": "roundtrip@kwalitec.example", "password": "OldPassword1"},
        follow_redirects=False,
    )
    assert login.status_code in {200, 302, 303}

    change = client.post(
        "/settings/password",
        data={
            "current_password": "OldPassword1",
            "new_password": "NewFamiliar2",
            "confirm_password": "NewFamiliar2",
            "submit": "Update password",
        },
        follow_redirects=True,
    )
    assert change.status_code == 200
    assert b"Password updated" in change.data

    logout = client.post("/auth/logout", follow_redirects=False)
    assert logout.status_code in {200, 302, 303}

    bad = client.post(
        "/auth/login",
        data={"email": "roundtrip@kwalitec.example", "password": "OldPassword1"},
        follow_redirects=True,
    )
    assert bad.status_code == 200
    assert b"Invalid email or password" in bad.data

    good = client.post(
        "/auth/login",
        data={"email": "roundtrip@kwalitec.example", "password": "NewFamiliar2"},
        follow_redirects=False,
    )
    assert good.status_code in {302, 303}
    assert "/auth/login" not in (good.headers.get("Location") or "")

    probe = client.get("/settings/password", follow_redirects=False)
    assert probe.status_code == 200
