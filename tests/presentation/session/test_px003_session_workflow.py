"""PX-003 Phase 1 — session finish confirm + profile exam chrome."""

from __future__ import annotations

from pathlib import Path


def test_session_finish_uses_confirm_trigger():
    """PX-B-016 — Finish CTAs require shared confirm modal wiring."""
    body = Path("app/templates/session/partials/session_body.html").read_text(
        encoding="utf-8"
    )
    assert "data-confirm-trigger" in body
    assert "Finish today's study session?" in body
    base = Path("app/templates/session/base.html").read_text(encoding="utf-8")
    assert "confirm_modal.html" in base
    assert "confirm-modal.js" in base


def test_login_recovery_messaging_present(client):
    """PX-B-017 — honest lockout / recovery posture on sign-in."""
    resp = client.get("/auth/login")
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert "password reset" in html.lower() or "coordinator" in html.lower()
    assert "self-service" in html.lower() or "recovery" in html.lower()


def test_profile_examination_avoids_hardcoded_not_set():
    """PX-B-054 — Examination card must not hardcode 'Not set'."""
    html = Path("app/templates/student/profile.html").read_text(encoding="utf-8")
    assert "profile.examination_label or 'Not set'" not in html
    assert "Choose an exam in your study plan" in html


def test_phantom_complete_still_hidden_from_chrome():
    """PX-B-015 — Complete remains off the step indicator (Sitting Report stays)."""
    from app.domain.session_experience.session_workspace import SessionSurface
    from app.presentation.session.navigation import build_session_steps

    steps = build_session_steps(SessionSurface.ACTIVITY, session_id="s1")
    labels = [s.label.lower() for s in steps]
    assert "complete" not in labels
