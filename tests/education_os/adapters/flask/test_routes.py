"""Route tests for the Flask adapter layer (V4-002 / V4-004)."""

from __future__ import annotations

from adapters.flask.dashboard.routes import dashboard_bp
from adapters.flask.login.routes import login_bp
from adapters.flask.mission.routes import mission_bp
from adapters.flask.reflection.routes import reflection_bp
from adapters.flask.session.routes import session_bp

EXPECTED_ROUTES = {
    "/eos/login/",
    "/eos/dashboard/",
    "/eos/home/",
    "/eos/journey/",
    "/eos/readiness/",
    "/eos/coach/",
    "/eos/workspace/",
    "/eos/mission/",
    "/eos/session/",
    "/eos/session/<session_id>",
    "/eos/session/action",
    "/eos/reflection/",
}


def test_adapter_endpoints_are_registered(app) -> None:
    rules = {rule.rule for rule in app.url_map.iter_rules()}
    assert EXPECTED_ROUTES.issubset(rules)


def test_blueprint_names() -> None:
    assert login_bp.name == "eos_login"
    assert dashboard_bp.name == "eos_dashboard"
    assert mission_bp.name == "eos_mission"
    assert session_bp.name == "eos_session"
    assert reflection_bp.name == "eos_reflection"


def test_login_route_returns_ok(client) -> None:
    response = client.get("/eos/login/")
    assert response.status_code == 200
    assert b"Student Login" in response.data


def test_login_post_redirects_to_dashboard(client) -> None:
    response = client.post(
        "/eos/login/",
        data={"student_id": "student-ada"},
        follow_redirects=False,
    )
    assert response.status_code in {301, 302}
    assert "/eos/dashboard" in (response.headers.get("Location") or "")


def test_dashboard_route_returns_ok(client) -> None:
    response = client.get("/eos/dashboard/")
    assert response.status_code == 200
    assert b"Learning Dashboard" in response.data


def test_dashboard_route_accepts_student_id(client) -> None:
    response = client.get("/eos/dashboard/?student_id=student-ada")
    assert response.status_code == 200
    assert b'data-page="dashboard"' in response.data


def test_mission_route_returns_ok(client) -> None:
    response = client.get("/eos/mission/?student_id=student-ada")
    assert response.status_code == 200
    assert b'data-page="mission"' in response.data


def test_session_route_returns_ok(client) -> None:
    response = client.get("/eos/session/")
    assert response.status_code == 200
    assert b'data-page="session"' in response.data


def test_session_route_by_id(client) -> None:
    response = client.get("/eos/session/session-42?student_id=student-ada")
    assert response.status_code == 200
    assert b'data-page="session"' in response.data


def test_session_action_start(client) -> None:
    response = client.post(
        "/eos/session/action",
        data={
            "student_id": "student-ada",
            "session_id": "session-flow-1",
            "action": "start",
        },
    )
    assert response.status_code == 200
    assert b'data-stage="preparing"' in response.data


def test_reflection_get_returns_ok(client) -> None:
    response = client.get("/eos/reflection/")
    assert response.status_code == 200
    assert b"Reflection" in response.data
    assert b'data-page="reflection"' in response.data


def test_reflection_post_captures_and_rerenders(client, evidence_updates) -> None:
    response = client.post(
        "/eos/reflection/",
        data={
            "student_id": "student-ada",
            "session_id": "session-1",
            "confidence": "confident",
            "difficulty": "about_right",
            "weak_concept": "Variance",
            "student_notes": "Review examples",
            "mission_id": "mission-1",
        },
    )
    assert response.status_code == 200
    assert b"Reflection" in response.data
    assert len(evidence_updates) == 1


def test_reflection_post_optional_redirect(client) -> None:
    response = client.post(
        "/eos/reflection/",
        data={
            "student_id": "student-ada",
            "redirect": "true",
        },
        follow_redirects=False,
    )
    assert response.status_code in {301, 302}
    assert "/eos/dashboard" in (response.headers.get("Location") or "")
