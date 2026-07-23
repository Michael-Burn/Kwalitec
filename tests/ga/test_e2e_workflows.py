"""GA-001 WS1/WS2 — release-candidate workflow validation and E2E paths."""

from __future__ import annotations

import json

import pytest

from tests.ga.helpers import (
    GA_CONSOLE_WORKFLOWS,
    GA_HEALTH_ENDPOINTS,
    GA_STUDENT_WORKFLOWS,
    login_as,
    make_founder,
    make_student,
    wire_session,
    wire_student,
    wire_studio,
)


@pytest.fixture
def student_client(app, client, ctx):
    make_student()
    wire_student(app)
    wire_session(app)
    login_as(client, "ga-student@kwalitec.example")
    return client


@pytest.fixture
def founder_client(app, client, ctx):
    make_founder()
    wire_studio(app)
    # Prefer RBAC over allowlist for GA verification.
    app.config["FOUNDER_EMAILS"] = ""
    login_as(client, "ga-founder@kwalitec.example")
    return client


class TestStudentCriticalPaths:
    def test_student_workflows_return_success(self, student_client) -> None:
        for name, path in GA_STUDENT_WORKFLOWS:
            response = student_client.get(path, follow_redirects=True)
            assert response.status_code == 200, (
                f"{name} {path} -> {response.status_code}"
            )
            assert b"Internal Server Error" not in response.data

    def test_mission_lifecycle_surfaces(self, student_client, app) -> None:
        from app.domain.session_experience.session_workspace import SessionSurface

        missions = student_client.get("/missions/")
        assert missions.status_code == 200

        service = wire_session(app)
        session_id = "ga-e2e-session"
        overview = student_client.get(f"/session/{session_id}/overview")
        assert overview.status_code == 200
        assert service.registry.get_workspace_for_session(session_id) is not None

        for suffix in ("activity", "reflection", "summary", "complete"):
            ws = service.registry.get_workspace_for_session(session_id)
            assert ws is not None
            surface = {
                "activity": SessionSurface.ACTIVITY,
                "reflection": SessionSurface.REFLECTION,
                "summary": SessionSurface.SUMMARY,
                "complete": SessionSurface.COMPLETE,
            }[suffix]
            service.registry.put_workspace(ws.navigate_to(surface))
            page = student_client.get(f"/session/{session_id}/{suffix}")
            assert page.status_code == 200, suffix

    def test_support_and_feedback_forms(self, student_client) -> None:
        help_page = student_client.get("/alpha/help")
        assert help_page.status_code == 200
        for path in (
            "/alpha/feedback/mission-helpful",
            "/alpha/feedback/explanation-clear",
            "/alpha/feedback/report-problem",
            "/alpha/feedback/suggest",
        ):
            response = student_client.get(path)
            assert response.status_code == 200, path


class TestFounderAndConsoleWorkflows:
    def test_console_workflows_return_success(self, founder_client) -> None:
        for name, path in GA_CONSOLE_WORKFLOWS:
            response = founder_client.get(path)
            assert response.status_code == 200, (
                f"{name} {path} -> {response.status_code}"
            )
            assert b"Internal Server Error" not in response.data

    def test_platform_intelligence_renders(self, founder_client) -> None:
        html = founder_client.get(
            "/console/alpha-observability"
        ).get_data(as_text=True)
        lowered = html.lower()
        assert (
            "observability" in lowered
            or "telemetry" in lowered
            or "Platform" in html
        )


class TestRbacSeparation:
    def test_student_cannot_access_console(self, client, ctx, app) -> None:
        make_student("ga-rbac-student@kwalitec.example")
        app.config["FOUNDER_EMAILS"] = "nobody@kwalitec.example"
        login_as(client, "ga-rbac-student@kwalitec.example")
        response = client.get("/console/")
        assert response.status_code == 403

    def test_founder_can_access_console(self, founder_client) -> None:
        assert founder_client.get("/console/").status_code == 200

    def test_unauthenticated_redirects_to_login(self, client) -> None:
        for _name, path in GA_STUDENT_WORKFLOWS[:3] + GA_CONSOLE_WORKFLOWS[:2]:
            response = client.get(path)
            assert response.status_code in {302, 401}, path
            if response.status_code == 302:
                assert "/auth/login" in response.headers.get("Location", "")


class TestHealthAndRegression:
    def test_health_endpoints(self, client) -> None:
        for path in GA_HEALTH_ENDPOINTS:
            response = client.get(path)
            assert response.status_code in {200, 503}, path
            payload = response.get_json()
            assert isinstance(payload, dict)
            assert "status" in payload

    def test_live_always_ok(self, client) -> None:
        response = client.get("/health/live")
        assert response.status_code == 200
        assert response.get_json()["status"] == "ok"

    def test_regression_brand_present_on_student_home(self, student_client) -> None:
        html = student_client.get("/student/").get_data(as_text=True)
        assert "Kwalitec" in html

    def test_settings_backup_export(self, student_client) -> None:
        response = student_client.get("/settings/export/backup")
        assert response.status_code == 200
        # JSON backup payload
        data = json.loads(response.get_data(as_text=True))
        assert isinstance(data, dict)
