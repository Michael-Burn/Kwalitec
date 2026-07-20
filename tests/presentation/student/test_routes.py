"""Route tests for Student Experience UI."""

from __future__ import annotations

import pytest
from flask import url_for

from app.application.student_experience.exceptions import PortUnavailable
from tests.application.student_experience.helpers import FakeMissionPort
from tests.presentation.student.helpers import STUDENT_ROUTES, wire_experience


@pytest.mark.parametrize(("endpoint", "path"), STUDENT_ROUTES)
def test_student_routes_require_login(client, endpoint, path):
    response = client.get(path)
    assert response.status_code in {302, 401}
    if response.status_code == 302:
        assert "/auth/login" in response.headers["Location"]


@pytest.mark.parametrize(("endpoint", "path"), STUDENT_ROUTES)
def test_student_routes_ok_when_logged_in(student_client, endpoint, path):
    response = student_client.get(path)
    assert response.status_code == 200
    assert b"Kwalitec" in response.data


@pytest.mark.parametrize(("endpoint", "path"), STUDENT_ROUTES)
def test_student_routes_render_nav(student_client, endpoint, path):
    response = student_client.get(path)
    html = response.get_data(as_text=True)
    for _ep, label_path in STUDENT_ROUTES:
        assert label_path.rstrip("/") in html or label_path in html
    assert "Home" in html
    assert "Journey" in html
    assert "Revision" in html
    assert "History" in html
    assert "Profile" in html


def test_home_shows_recommendation(student_client):
    response = student_client.get("/student/")
    html = response.get_data(as_text=True)
    assert "Today" in html or "Recommendation" in html
    assert "Start" in html


def test_journey_shows_topics(student_client):
    response = student_client.get("/student/journey")
    html = response.get_data(as_text=True)
    assert "Equity method" in html or "Current" in html or "Journey" in html
    assert "graph" not in html.lower() or "curriculum graph" not in html.lower()


def test_revision_shows_primary(student_client):
    response = student_client.get("/student/revision")
    html = response.get_data(as_text=True)
    assert "Revision" in html
    assert "Begin Revision" in html or "revision" in html.lower()


def test_history_shows_progress(student_client):
    response = student_client.get("/student/history")
    html = response.get_data(as_text=True)
    assert "History" in html or "sessions" in html.lower() or "Study" in html


def test_profile_shows_examination(student_client):
    response = student_client.get("/student/profile")
    html = response.get_data(as_text=True)
    assert "Profile" in html or "examination" in html.lower() or "CPA" in html


def test_start_session_post(student_client, experience_app):
    mission = FakeMissionPort()
    wire_experience(experience_app, mission=mission)
    response = student_client.post(
        "/student/session/start",
        data={
            "mission_id": "m1",
            "session_id": "sess-1",
            "submit": "Start Today's Session",
        },
        follow_redirects=False,
    )
    assert response.status_code in {302, 303}
    assert mission.start_calls
    location = response.headers.get("Location", "")
    assert "/session/sess-1" in location


def test_begin_revision_post(student_client, experience_app):
    mission = FakeMissionPort()
    wire_experience(experience_app, mission=mission)
    response = student_client.post(
        "/student/revision/begin",
        data={
            "option_id": "r1",
            "mission_id": "m1",
            "session_id": "sess-1",
            "submit": "Begin Revision",
        },
        follow_redirects=False,
    )
    assert response.status_code in {302, 303}
    location = response.headers.get("Location", "")
    assert "/session/" in location


def test_start_session_unavailable_port(student_client, experience_app):
    class BrokenMission(FakeMissionPort):
        def start_session(self, student_id, *, mission_id=None, session_id=None):
            raise PortUnavailable("mission port unavailable")

    wire_experience(experience_app, mission=BrokenMission())
    response = student_client.post(
        "/student/session/start",
        data={"mission_id": "m1", "submit": "Start"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    body = response.data.lower()
    assert b"unavailable" in body or b"could not" in body


def test_url_for_student_endpoints(experience_app):
    with experience_app.test_request_context():
        assert url_for("student.home") == "/student/"
        assert url_for("student.journey") == "/student/journey"
        assert url_for("student.revision") == "/student/revision"
        assert url_for("student.history") == "/student/history"
        assert url_for("student.profile") == "/student/profile"
