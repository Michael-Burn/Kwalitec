"""End-to-end student flow through Flask adapter HTML surfaces (V4-004)."""

from __future__ import annotations

from application.session_runtime import SessionStage


def _advance_to_reflection(client, *, student_id: str, session_id: str) -> None:
    client.post(
        "/eos/session/action",
        data={
            "student_id": student_id,
            "session_id": session_id,
            "action": "start",
        },
    )
    # PREPARING → LEARNING → WORKED_EXAMPLE → NOTES → REFLECTION
    for _ in range(4):
        response = client.post(
            "/eos/session/action",
            data={
                "student_id": student_id,
                "session_id": session_id,
                "action": "advance",
            },
            follow_redirects=False,
        )
        if response.status_code in {301, 302}:
            assert "/eos/reflection" in (response.headers.get("Location") or "")
            return
    raise AssertionError("session never reached reflection")


def test_end_to_end_student_flow(client, evidence_updates) -> None:
    """Login → Dashboard → Mission → Session → Reflection → Evidence → Dashboard."""
    login = client.post(
        "/eos/login/",
        data={"student_id": "student-ada"},
        follow_redirects=True,
    )
    assert login.status_code == 200
    assert b'data-page="dashboard"' in login.data
    assert b"Learning Dashboard" in login.data

    mission = client.get("/eos/mission/?student_id=student-ada")
    assert mission.status_code == 200
    assert b'data-page="mission"' in mission.data
    assert b"Begin session" in mission.data

    session_page = client.get(
        "/eos/session/?student_id=student-ada&session_id=e2e-session-1"
    )
    assert session_page.status_code == 200
    assert b'data-page="session"' in session_page.data
    assert b'data-stage="not_started"' in session_page.data

    _advance_to_reflection(
        client, student_id="student-ada", session_id="e2e-session-1"
    )

    reflection = client.get(
        "/eos/reflection/?student_id=student-ada&session_id=e2e-session-1"
    )
    assert reflection.status_code == 200
    assert b'data-page="reflection"' in reflection.data

    submit = client.post(
        "/eos/reflection/",
        data={
            "student_id": "student-ada",
            "session_id": "e2e-session-1",
            "mission_id": "mission-e2e",
            "confidence": "confident",
            "difficulty": "about_right",
            "weak_concept": "Survival models",
            "student_notes": "Revisit worked examples",
            "redirect": "true",
        },
        follow_redirects=True,
    )
    assert submit.status_code == 200
    assert b'data-page="dashboard"' in submit.data
    assert len(evidence_updates) == 1
    assert evidence_updates[0].outcome.student_id == "student-ada"


def test_session_runtime_checkpoint_survives_requests(client) -> None:
    client.post(
        "/eos/session/action",
        data={
            "student_id": "student-ada",
            "session_id": "checkpoint-1",
            "action": "start",
        },
    )
    again = client.get(
        "/eos/session/checkpoint-1?student_id=student-ada"
    )
    assert b'data-stage="preparing"' in again.data
    assert SessionStage.PREPARING.value.encode() in again.data
