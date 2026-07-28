"""RR-001.1 / JR-01 — V2 session finish completes Mission commitment lifecycle."""

from __future__ import annotations

from datetime import datetime
from unittest.mock import patch

from app.application.student_experience.recommendation_commitment import (
    STATE_COMPLETED,
    STATE_IN_SESSION,
    RecommendationCommitmentService,
)
from app.domain.session_experience.session_workspace import SessionSurface
from app.models.recommendation_commitment import RecommendationCommitment
from tests.presentation.session.helpers import wire_session_experience


def _tip(**overrides):
    tip = {
        "title": "Cash flow statements",
        "category": "Revision",
        "priority": "High",
        "reason": "High educational return before the exam window.",
        "why_recommended": "Soft recall on cash flow.",
        "expected_benefit": "Strengthen exam readiness on cash flow analysis.",
        "review_point": "Reassess after tonight's practice set.",
        "suggested_next_action": "Start a 25-minute cash flow practice session.",
        "generated_at": datetime(2026, 7, 26, 10, 0, 0),
    }
    tip.update(overrides)
    return tip


def test_v2_session_finish_marks_commitment_completed(
    session_client, session_app, db, user
):
    """Canonical Alpha finish path must advance commitment to C3 (JR-01)."""
    tip = _tip()
    RecommendationCommitmentService.confirm_commitment(user.id, tip)
    RecommendationCommitmentService.mark_session_started(
        user.id, tip=tip, session_id="sess-1"
    )
    row = RecommendationCommitment.query.filter_by(user_id=user.id).one()
    assert row.state == STATE_IN_SESSION

    svc = wire_session_experience(session_app)
    svc.open_session(str(user.id), session_id="sess-1")
    ws = svc.registry.get_workspace_for_session("sess-1")
    assert ws is not None
    svc.registry.put_workspace(ws.navigate_to(SessionSurface.SUMMARY))

    with patch(
        "app.services.recommendation_service.RecommendationService"
        ".get_dashboard_today_recommendation",
        return_value=tip,
    ):
        response = session_client.post(
            "/session/sess-1/complete",
            data={"session_id": "sess-1", "submit": "Return Home"},
            follow_redirects=False,
        )

    assert response.status_code in {302, 303}
    assert "/student" in response.headers.get("Location", "")
    db.session.refresh(row)
    assert row.state == STATE_COMPLETED
    assert row.completed_at is not None
    assert row.session_id == "sess-1"


def test_v2_session_finish_fails_open_without_commitment(
    session_client, session_app, user
):
    """Finish still returns Home when no open commitment exists."""
    svc = wire_session_experience(session_app)
    svc.open_session(str(user.id), session_id="sess-1")
    ws = svc.registry.get_workspace_for_session("sess-1")
    assert ws is not None
    svc.registry.put_workspace(ws.navigate_to(SessionSurface.SUMMARY))

    response = session_client.post(
        "/session/sess-1/complete",
        data={"session_id": "sess-1", "submit": "Return Home"},
        follow_redirects=False,
    )
    assert response.status_code in {302, 303}
    assert "/student" in response.headers.get("Location", "")
