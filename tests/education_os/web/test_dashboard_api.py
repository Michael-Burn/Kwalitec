"""Dashboard API endpoint tests (WEB-004)."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from application.errors import NotFoundError
from application.queries.get_dashboard import GetDashboard
from application.queries.get_progress_summary import GetProgressSummary
from application.queries.get_recommendations import GetRecommendations
from application.queries.get_timeline import GetTimeline
from application.queries.get_todays_mission import GetTodaysMission
from application.read_models import (
    DashboardReadModel,
    MissionTaskReadModel,
    ProgressSummaryReadModel,
    RecommendationReadModel,
    TimelineEventReadModel,
    TimelineReadModel,
    TodaysMissionReadModel,
)
from web.blueprints.dashboard import schemas

DASHBOARD_ROUTES = {
    "/dashboard",
    "/dashboard/today",
    "/dashboard/progress",
    "/dashboard/recommendations",
    "/dashboard/timeline",
}


@pytest.fixture
def services(client):
    """Replace request-scoped application services with mocks."""
    mock_services = MagicMock()
    mock_services.dashboard = MagicMock()

    @client.application.before_request
    def _bind_mocks() -> None:
        from flask import g

        from web.lifecycle import REQUEST_SCOPE_KEY, RequestScope

        scope = getattr(g, REQUEST_SCOPE_KEY, None)
        if scope is None:
            return
        setattr(
            g,
            REQUEST_SCOPE_KEY,
            RequestScope(unit_of_work=scope.unit_of_work, services=mock_services),
        )

    return mock_services


def test_dashboard_endpoints_are_registered(app) -> None:
    rules = {rule.rule for rule in app.url_map.iter_rules()}
    assert DASHBOARD_ROUTES.issubset(rules)


def test_get_dashboard_requires_student_id(client, services) -> None:
    response = client.get("/dashboard")

    assert response.status_code == 400
    assert response.get_json() == {"error": "missing or invalid field: student_id"}
    services.dashboard.get_dashboard.assert_not_called()


def test_get_dashboard_serializes_read_model(client, services) -> None:
    services.dashboard.get_dashboard.return_value = DashboardReadModel(
        student_id="student-ada",
        recommendation=RecommendationReadModel(
            title="Continue studying",
            subtitle="Repair confusion",
            primary_action="Start Session",
            reason_summary=None,
            estimated_minutes=None,
            can_start=True,
            recommendation_id="plan-001",
        ),
        todays_mission=TodaysMissionReadModel(
            title="Today's Session",
            summary="1 task",
            task_count=1,
            tasks=(
                MissionTaskReadModel(
                    task_id="step-1",
                    headline="Explanation",
                    sequence_index=0,
                    status="pending",
                ),
            ),
            estimated_minutes=None,
            can_open=True,
            episode_id="episode-001",
        ),
        progress=ProgressSummaryReadModel(
            student_id="student-ada",
            activity_status="engaged",
            twin_status="active",
            concept_count=2,
            evidence_count=3,
            intervention_count=0,
            progress_cues=("activity:engaged",),
            twin_id="twin-001",
        ),
        timeline=TimelineReadModel(
            student_id="student-ada",
            events=(
                TimelineEventReadModel(
                    sequence=0,
                    kind="created",
                    label="Twin created",
                ),
            ),
            twin_id="twin-001",
        ),
        empty_states=(),
        composed_at="2026-07-20T10:00:00+00:00",
    )

    response = client.get(
        "/dashboard",
        query_string={"student_id": "student-ada", "episode_id": "episode-001"},
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["student_id"] == "student-ada"
    assert body["recommendation"]["title"] == "Continue studying"
    assert body["todays_mission"]["tasks"][0]["headline"] == "Explanation"
    assert body["progress"]["concept_count"] == 2
    assert body["timeline"]["events"][0]["kind"] == "created"
    assert body["warnings"] == []
    query = services.dashboard.get_dashboard.call_args.args[0]
    assert isinstance(query, GetDashboard)
    assert query.student_id == "student-ada"
    assert query.episode_id == "episode-001"


def test_get_today_requires_episode_id(client, services) -> None:
    response = client.get(
        "/dashboard/today",
        query_string={"student_id": "student-ada"},
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "missing or invalid field: episode_id"}
    services.dashboard.get_todays_mission.assert_not_called()


def test_get_today_serializes_mission(client, services) -> None:
    services.dashboard.get_todays_mission.return_value = TodaysMissionReadModel(
        title="Today's Session",
        summary="No tasks in this session",
        task_count=0,
        tasks=(),
        estimated_minutes=None,
        can_open=False,
        episode_id="episode-001",
        status="planned",
    )

    response = client.get(
        "/dashboard/today",
        query_string={"student_id": "student-ada", "episode_id": "episode-001"},
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "title": "Today's Session",
        "summary": "No tasks in this session",
        "task_count": 0,
        "tasks": [],
        "estimated_minutes": None,
        "can_open": False,
        "mission_id": None,
        "episode_id": "episode-001",
        "status": "planned",
    }
    query = services.dashboard.get_todays_mission.call_args.args[0]
    assert isinstance(query, GetTodaysMission)
    assert query.episode_id == "episode-001"


def test_get_progress_invokes_service(client, services) -> None:
    services.dashboard.get_progress.return_value = ProgressSummaryReadModel(
        student_id="student-ada",
        activity_status="engaged",
        twin_status="active",
        concept_count=1,
        evidence_count=2,
        intervention_count=0,
        progress_cues=("activity:engaged", "twin:active"),
        twin_id="twin-001",
    )

    response = client.get(
        "/dashboard/progress",
        query_string={"student_id": "student-ada"},
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["student_id"] == "student-ada"
    assert body["progress_cues"] == ["activity:engaged", "twin:active"]
    query = services.dashboard.get_progress.call_args.args[0]
    assert isinstance(query, GetProgressSummary)


def test_get_recommendations_serializes_null(client, services) -> None:
    services.dashboard.get_recommendations.return_value = None

    response = client.get(
        "/dashboard/recommendations",
        query_string={"student_id": "student-ada"},
    )

    assert response.status_code == 200
    assert response.get_json() is None
    query = services.dashboard.get_recommendations.call_args.args[0]
    assert isinstance(query, GetRecommendations)
    assert query.episode_id is None


def test_get_recommendations_serializes_card(client, services) -> None:
    services.dashboard.get_recommendations.return_value = RecommendationReadModel(
        title="Continue studying",
        subtitle="Repair confusion",
        primary_action="Start Session",
        reason_summary=None,
        estimated_minutes=None,
        can_start=True,
        recommendation_id="plan-001",
    )

    response = client.get(
        "/dashboard/recommendations",
        query_string={"student_id": "student-ada", "episode_id": "episode-001"},
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["title"] == "Continue studying"
    assert body["can_start"] is True
    query = services.dashboard.get_recommendations.call_args.args[0]
    assert query.episode_id == "episode-001"


def test_get_timeline_serializes_events(client, services) -> None:
    services.dashboard.get_timeline.return_value = TimelineReadModel(
        student_id="student-ada",
        events=(
            TimelineEventReadModel(sequence=0, kind="created", label="Twin created"),
            TimelineEventReadModel(sequence=1, kind="evidence", label="Evidence"),
        ),
        twin_id="twin-001",
    )

    response = client.get(
        "/dashboard/timeline",
        query_string={"student_id": "student-ada"},
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["student_id"] == "student-ada"
    assert len(body["events"]) == 2
    assert body["events"][1]["kind"] == "evidence"
    query = services.dashboard.get_timeline.call_args.args[0]
    assert isinstance(query, GetTimeline)


def test_not_found_maps_to_404(client, services) -> None:
    services.dashboard.get_progress.side_effect = NotFoundError(
        "EducationalDigitalTwin",
        "student-ada",
    )

    response = client.get(
        "/dashboard/progress",
        query_string={"student_id": "student-ada"},
    )

    assert response.status_code == 404
    assert response.get_json() == {
        "error": "EducationalDigitalTwin not found: student-ada",
    }


def test_schema_parse_dashboard_optional_episode() -> None:
    query = schemas.parse_get_dashboard({"student_id": " student-ada "})
    assert query.student_id == "student-ada"
    assert query.episode_id is None


def test_serialize_read_model_none() -> None:
    assert schemas.serialize_read_model(None) is None
