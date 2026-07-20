"""Session ownership hardening tests."""

from __future__ import annotations

from app.application.session_experience.exceptions import SessionOwnershipError
from app.domain.session_experience.session_workspace import (
    SessionSurface,
    SessionWorkspace,
)
from app.presentation.session import views


def test_assert_session_owned_allows_matching_workspace(app, monkeypatch):
    class _Reg:
        def get_workspace_for_session(self, session_id):
            return SessionWorkspace.create(
                "ws-1",
                "42",
                session_id,
                active_surface=SessionSurface.OVERVIEW,
            )

    class _Svc:
        registry = _Reg()

    monkeypatch.setattr(views, "student_id", lambda: "42")
    monkeypatch.setattr(views, "service", lambda: _Svc())
    views.assert_session_owned("sess-1")


def test_assert_session_owned_rejects_foreign_workspace(app, monkeypatch):
    class _Reg:
        def get_workspace_for_session(self, session_id):
            return SessionWorkspace.create(
                "ws-1",
                "99",
                session_id,
                active_surface=SessionSurface.OVERVIEW,
            )

    class _Svc:
        registry = _Reg()

    monkeypatch.setattr(views, "student_id", lambda: "42")
    monkeypatch.setattr(views, "service", lambda: _Svc())
    try:
        views.assert_session_owned("sess-1")
        raise AssertionError("expected SessionOwnershipError")
    except SessionOwnershipError:
        pass
