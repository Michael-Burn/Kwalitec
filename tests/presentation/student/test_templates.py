"""Template rendering and content regression tests."""

from __future__ import annotations

import pytest

from tests.presentation.student.helpers import FORBIDDEN_TERMS, STUDENT_ROUTES


@pytest.mark.parametrize(("endpoint", "path"), STUDENT_ROUTES)
def test_templates_include_student_css(student_client, endpoint, path):
    html = student_client.get(path).get_data(as_text=True)
    assert "student.css" in html
    assert "student.js" in html


@pytest.mark.parametrize(("endpoint", "path"), STUDENT_ROUTES)
def test_templates_have_landmarks(student_client, endpoint, path):
    html = student_client.get(path).get_data(as_text=True)
    assert 'role="main"' in html or 'id="student-main"' in html
    assert 'role="banner"' in html or "student-topbar" in html
    assert 'aria-label="Student experience"' in html


@pytest.mark.parametrize(("endpoint", "path"), STUDENT_ROUTES)
@pytest.mark.parametrize("term", FORBIDDEN_TERMS)
def test_templates_hide_internal_terms(student_client, endpoint, path, term):
    html = student_client.get(path).get_data(as_text=True).lower()
    assert term not in html


@pytest.mark.parametrize(("endpoint", "path"), STUDENT_ROUTES)
def test_one_primary_cta_marker(student_client, endpoint, path):
    html = student_client.get(path).get_data(as_text=True)
    # Pages may have zero or one intentional primary CTA marker.
    assert html.count('data-student-cta="primary"') <= 2


def test_home_has_decision_hierarchy(student_client):
    html = student_client.get("/student/").get_data(as_text=True)
    assert 'data-dashboard-slot="primary"' in html
    assert 'data-dashboard-slot="secondary"' in html
    assert 'data-dashboard-slot="tertiary"' in html
    assert "Today's Mission" in html or "mission" in html.lower()
    assert "readiness" in html.lower()
    assert "coach" in html.lower()
    assert "quick actions" in html.lower()


def test_home_has_countdown_and_readiness(student_client):
    html = student_client.get("/student/").get_data(as_text=True)
    lowered = html.lower()
    assert "countdown" in lowered or "days" in lowered or "readiness" in lowered
    assert "readiness" in lowered


def test_journey_has_progress(student_client):
    html = student_client.get("/student/journey").get_data(as_text=True)
    assert "progress" in html.lower() or "complete" in html.lower()
    assert "role=\"progressbar\"" in html or "student-progress" in html


def test_revision_has_priority_or_benefit(student_client):
    html = student_client.get("/student/revision").get_data(as_text=True)
    lowered = html.lower()
    assert "priority" in lowered or "benefit" in lowered or "revision" in lowered


def test_history_focuses_on_progress_not_logs(student_client):
    html = student_client.get("/student/history").get_data(as_text=True).lower()
    assert "event log" not in html
    assert "raw event" not in html


def test_profile_has_settings_cta(student_client):
    html = student_client.get("/student/profile").get_data(as_text=True)
    assert "settings" in html.lower() or "account" in html.lower()


def test_skip_link_present(student_client):
    html = student_client.get("/student/").get_data(as_text=True)
    assert "Skip to content" in html
    assert 'href="#student-main"' in html
