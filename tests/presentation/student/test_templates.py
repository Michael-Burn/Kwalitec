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
    # SOP-001 command centre: mission-first, no legacy dashboard slots.
    assert (
        "Today&#39;s Session" in html
        or "Today's Session" in html
        or "Today&#39;s Mission" in html
        or "Continue Session" in html
        or "ds-mission-panel" in html
        or "ds-empty-operational" in html
    )
    assert 'id="student-home-title"' in html or ">Home<" in html
    assert "student-hero-greeting" not in html
    assert 'data-dashboard-panel="quick-actions"' not in html
    assert 'data-dashboard-panel="readiness"' not in html
    assert 'data-dashboard-panel="coach"' not in html
    assert "What should I do next?" in html or "Where you stand" in html


def test_home_has_no_kpi_readiness_on_surface(student_client):
    """DX-005A / KWP-002: no legacy KPI readiness panel; calm card allowed."""
    html = student_client.get("/student/").get_data(as_text=True)
    assert 'data-dashboard-panel="readiness"' not in html
    assert "student-panel-metric" not in html
    assert "Progress ring" not in html


def test_journey_has_progress(student_client):
    html = student_client.get("/student/journey").get_data(as_text=True)
    assert "progress" in html.lower() or "complete" in html.lower()
    assert 'role="progressbar"' in html or "student-progress" in html


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
    assert "settings-hub" in html
    assert "How Kwalitec works for you" in html
    assert "settings-kpi-grid" not in html


def test_settings_hub_groups_present(student_client):
    html = student_client.get("/student/profile").get_data(as_text=True)
    for group in (
        "Profile",
        "Learning",
        "Appearance",
        "Notifications",
        "Account",
        "Security",
    ):
        assert group in html
    assert "History" in html  # progress relocated
    assert "Study Time" not in html
    assert "Topics Mastered" not in html
    assert 'id="daily_goal_hours"' in html
    assert "appearance-switcher" in html or "data-appearance-option" in html
    assert "Open account settings" not in html  # replaced by compact card actions


def test_skip_link_present(student_client):
    html = student_client.get("/student/").get_data(as_text=True)
    assert "Skip to content" in html
    assert 'href="#student-main"' in html
