"""Route tests for Assessment Delivery."""

from __future__ import annotations

from application.assessment.commands.commands import (
    CommitAssessmentResponseCommand,
    CreateAssessmentSessionCommand,
)
from tests.presentation.assessment.helpers import wire_assessment_delivery


def test_entry_requires_login(client):
    response = client.get("/assessment/")
    assert response.status_code in {302, 401}


def test_full_delivery_flow(assessment_app, assessment_client, ctx, user):
    composition = wire_assessment_delivery(assessment_app)

    entry = assessment_client.get("/assessment/")
    assert entry.status_code == 200
    assert b"Learning Check" in entry.data
    assert b"No grades" in entry.data

    start = assessment_client.post("/assessment/start", follow_redirects=False)
    assert start.status_code == 302
    overview_url = start.headers["Location"]
    assert "/assessment/" in overview_url

    overview = assessment_client.get(overview_url)
    assert overview.status_code == 200
    assert b"Why this check" in overview.data

    # Location may be absolute or relative
    path = overview_url.split("://", 1)[-1]
    if "/" in path and not path.startswith("/"):
        path = "/" + path.split("/", 1)[-1]
    parts = [p for p in path.strip("/").split("/") if p]
    # assessment / <session_id> / overview
    session_id = parts[1] if len(parts) >= 2 else parts[-1]
    if session_id == "overview":
        session_id = parts[-2]

    begin = assessment_client.post(
        f"/assessment/{session_id}/begin",
        data={"session_id": session_id, "submit": "Begin"},
        follow_redirects=False,
    )
    assert begin.status_code == 302

    item = assessment_client.get(f"/assessment/{session_id}/item")
    assert item.status_code == 200
    assert b"force of mortality" in item.data.lower()

    respond = assessment_client.post(
        f"/assessment/{session_id}/respond",
        data={
            "session_id": session_id,
            "question_id": "q-mc-force",
            "selected_option": "a",
            "submit": "Save answer",
        },
        follow_redirects=False,
    )
    assert respond.status_code == 302

    pause = assessment_client.post(
        f"/assessment/{session_id}/pause",
        data={"session_id": session_id, "submit": "Pause"},
        follow_redirects=False,
    )
    assert pause.status_code == 302
    resume = assessment_client.post(
        f"/assessment/{session_id}/resume",
        data={"session_id": session_id, "submit": "Resume"},
        follow_redirects=False,
    )
    assert resume.status_code == 302

    sid = str(user.id)
    svc = composition.delivery_service
    for qid, payload in (
        ("q-numeric-mu", {"entered_value": "0.02"}),
        ("q-confidence-mu", {"confidence": 3}),
        ("q-reflection-mu", {"reflection_text": "Need examples"}),
    ):
        try:
            svc.commit_response(
                CommitAssessmentResponseCommand(
                    session_id=session_id,
                    question_id=qid,
                    response_payload=payload,
                    confidence=payload.get("confidence"),
                ),
                student_id=sid,
            )
        except Exception:
            pass

    complete = assessment_client.post(
        f"/assessment/{session_id}/complete",
        data={"session_id": session_id, "submit": "Finish check"},
        follow_redirects=True,
    )
    assert complete.status_code == 200
    assert b"Check complete" in complete.data
    assert b"support you" in complete.data.lower()


def test_ownership_forbidden(assessment_app, assessment_client, ctx):
    composition = wire_assessment_delivery(assessment_app)
    composition.delivery_service.create_session(
        CreateAssessmentSessionCommand(
            session_id="asess-foreign",
            student_id="someone-else",
            instrument_id=composition.default_instrument_id,
        )
    )
    response = assessment_client.get("/assessment/asess-foreign/overview")
    assert response.status_code == 403
