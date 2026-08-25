"""DX-006B Phase 5 — Choose Exam discovery tests."""

from __future__ import annotations

import re
from datetime import date, timedelta

from app.presentation.student.services.choose_exam_service import ChooseExamService


def test_choose_exam_page_renders_discovery(logged_in_client):
    resp = logged_in_client.get("/study-plan/wizard/1")
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert "Choose Exam" in html
    assert "Ready to begin" in html
    assert "ds-btn--primary" in html
    assert "Continue" in html
    assert "wizard-option-grid" not in html
    assert "Study Plan wizard progress" not in html
    assert html.lower().count("<h1") == 1


def test_choose_exam_post_continues_to_exam_date(logged_in_client):
    get = logged_in_client.get("/study-plan/wizard/1")
    assert get.status_code == 200
    html = get.get_data(as_text=True)
    match = re.search(r'name="subject_key"[^>]*value="([^"]+)"', html)
    assert match is not None, "expected at least one Ready subject"
    subject_key = match.group(1)
    resp = logged_in_client.post(
        "/study-plan/wizard/1",
        data={"subject_key": subject_key},
        follow_redirects=False,
    )
    assert resp.status_code in (302, 303)
    assert "/wizard/2" in (resp.headers.get("Location") or "")


def test_choose_exam_service_separates_ready_and_soon():
    page = ChooseExamService().build()
    for row in page.ready_offerings:
        assert row.availability_label == "Ready"
    for row in page.coming_soon:
        assert row.availability_label == "Coming Soon"
        assert row.selectable is False
    assert page.page_title == "Choose Exam"
    assert page.primary_label == "Continue"


def test_choose_exam_nav_label(logged_in_client):
    resp = logged_in_client.get("/student/")
    html = resp.get_data(as_text=True)
    assert "Choose Exam" in html


def test_confirm_is_begin_learning_only(logged_in_client):
    get = logged_in_client.get("/study-plan/wizard/1")
    html = get.get_data(as_text=True)
    match = re.search(r'name="subject_key"[^>]*value="([^"]+)"', html)
    assert match is not None
    subject_key = match.group(1)
    logged_in_client.post("/study-plan/wizard/1", data={"subject_key": subject_key})
    step2 = logged_in_client.get("/study-plan/wizard/2")
    assert step2.status_code == 200
    s2 = step2.get_data(as_text=True)
    sitting_match = re.search(r'<option[^>]+value="([^"]+)"', s2)
    assert sitting_match is not None
    exam_date = (date.today() + timedelta(days=90)).isoformat()
    logged_in_client.post(
        "/study-plan/wizard/2",
        data={
            "exam_sitting": sitting_match.group(1),
            "exam_date": exam_date,
        },
    )
    logged_in_client.post(
        "/study-plan/wizard/3",
        data={
            "weekday_study_minutes": 60,
            "weekend_study_minutes": 90,
            "preferred_session_minutes": 60,
        },
    )
    # SB-001A: review is no longer a confirm page — Begin Learning enters Baseline.
    review = logged_in_client.get("/study-plan/review", follow_redirects=False)
    assert review.status_code == 302
    location = review.headers.get("Location") or ""
    assert "/baseline" in location
    # Wizard must not re-collect position / learning-style on this path.
    with logged_in_client.session_transaction() as sess:
        wizard = sess.get("wizard_data") or {}
        assert wizard.get("current_position") == "not_started"
        assert "completed_curriculum_topics" not in wizard
