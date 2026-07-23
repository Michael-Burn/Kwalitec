"""GA-001 WS3 — load and performance soft budgets for hot surfaces."""

from __future__ import annotations

import pytest

from app.extensions import db
from app.infrastructure.diagnostics.query_profiling import count_queries
from tests.ga.helpers import (
    GA_PERF_BUDGETS_MS,
    GA_SQL_BUDGETS,
    login_as,
    make_founder,
    make_student,
    time_call,
    wire_session,
    wire_student,
    wire_studio,
)


@pytest.fixture
def student_client(app, client, ctx):
    make_student("ga-perf-student@kwalitec.example")
    wire_student(app)
    wire_session(app)
    login_as(client, "ga-perf-student@kwalitec.example")
    return client


@pytest.fixture
def founder_client(app, client, ctx):
    make_founder("ga-perf-founder@kwalitec.example")
    wire_studio(app)
    app.config["FOUNDER_EMAILS"] = ""
    login_as(client, "ga-perf-founder@kwalitec.example")
    return client


def _assert_http_budget(
    label: str,
    client,
    path: str,
    *,
    allowed_statuses: set[int] | None = None,
) -> None:
    budget = GA_PERF_BUDGETS_MS[label]
    ok_statuses = allowed_statuses or {200}

    def _run():
        return client.get(path)

    result = time_call(label, _run, budget)
    response = result.value
    print(
        f"[ga-perf] {label} path={path} duration_ms={result.duration_ms:.1f} "
        f"budget_ms={budget:.0f} status={response.status_code}"
    )
    assert response.status_code in ok_statuses, path
    assert result.within_budget, (
        f"{label} exceeded budget: {result.duration_ms:.1f}ms > {budget}ms"
    )


def _assert_sql_budget(
    label: str,
    client,
    path: str,
    *,
    app,
    allowed_statuses: set[int] | None = None,
) -> None:
    budget = GA_SQL_BUDGETS[label]
    ok_statuses = allowed_statuses or {200}
    with app.app_context():
        with count_queries(db.engine) as profile:
            response = client.get(path)
    print(
        f"[ga-sql] {label} path={path} statements={profile.statements} "
        f"budget={budget} status={response.status_code}"
    )
    assert response.status_code in ok_statuses, path
    assert profile.statements <= budget, (
        f"{label} SQL budget exceeded: {profile.statements} > {budget}"
    )


class TestHttpPerformanceBudgets:
    def test_student_dashboard_budget(self, student_client) -> None:
        _assert_http_budget("student_dashboard", student_client, "/student/")

    def test_workspace_session_budget(self, student_client) -> None:
        _assert_http_budget(
            "workspace_session", student_client, "/session/ga-perf-session/overview"
        )

    def test_journey_budget(self, student_client) -> None:
        _assert_http_budget("journey", student_client, "/student/journey")

    def test_console_home_budget(self, founder_client) -> None:
        _assert_http_budget("console_home", founder_client, "/console/")

    def test_platform_intelligence_budget(self, founder_client) -> None:
        _assert_http_budget(
            "platform_intelligence",
            founder_client,
            "/console/alpha-observability",
        )

    def test_health_live_budget(self, client) -> None:
        _assert_http_budget("health_live", client, "/health/live")

    def test_health_ready_budget(self, client) -> None:
        # Test harness uses create_all without Alembic stamp → ready may be 503.
        _assert_http_budget(
            "health_ready",
            client,
            "/health/ready",
            allowed_statuses={200, 503},
        )


class TestSqlQueryBudgets:
    def test_student_dashboard_sql(self, student_client, app) -> None:
        _assert_sql_budget(
            "student_dashboard", student_client, "/student/", app=app
        )

    def test_journey_sql(self, student_client, app) -> None:
        _assert_sql_budget("journey", student_client, "/student/journey", app=app)

    def test_console_home_sql(self, founder_client, app) -> None:
        _assert_sql_budget("console_home", founder_client, "/console/", app=app)

    def test_platform_intelligence_sql(self, founder_client, app) -> None:
        _assert_sql_budget(
            "platform_intelligence",
            founder_client,
            "/console/alpha-observability",
            app=app,
        )

    def test_health_ready_sql(self, client, app) -> None:
        _assert_sql_budget(
            "health_ready",
            client,
            "/health/ready",
            app=app,
            allowed_statuses={200, 503},
        )


class TestBudgetCatalogue:
    def test_perf_budgets_documented(self) -> None:
        expected = {
            "student_dashboard",
            "workspace_session",
            "journey",
            "console_home",
            "platform_intelligence",
            "health_live",
            "health_ready",
        }
        assert set(GA_PERF_BUDGETS_MS) == expected
