"""PX-001 — Educational Experience Integration acceptance tests."""

from __future__ import annotations

from datetime import date, timedelta

from app.application.educational_experience import EducationalExperienceService
from app.application.platform_integration.discovery import PUBLISHED_CATEGORY_CODE
from app.application.platform_integration.enrolment_bridge import (
    FounderStudentEnrolmentBridge,
)
from app.extensions import db
from app.models.user import User
from app.presentation.student.educational_view_models import (
    page_from_educational_experience,
)
from tests.application.platform_integration.helpers import (
    bridge_flags,
    make_user,
    publish_subject,
)


def _enrol_runtime_c(user: User, subject: str) -> None:
    bridge = FounderStudentEnrolmentBridge(flags=bridge_flags())
    result = bridge.enrol(
        user_id=user.id,
        category_code=PUBLISHED_CATEGORY_CODE,
        subject_code=subject,
        exam_date=date.today() + timedelta(days=120),
    )
    assert result.runtime_authority == "published_curriculum"


def test_educational_experience_surfaces_eq001_fields(ctx):
    """Runtime C student snapshot exposes all PX-001 acceptance fields."""
    subject = publish_subject("PXE1", title="Experience Subject")
    user = make_user("px001-edu@example.com")
    _enrol_runtime_c(user, subject)

    snap = EducationalExperienceService().load_for_user(user.id)
    assert snap is not None
    assert snap.is_runtime_c
    assert snap.curriculum_position.topic_title
    assert snap.curriculum_position.position_label
    assert "of" in snap.curriculum_position.position_label

    assert snap.mission is not None
    mission = snap.mission
    assert mission.title
    assert mission.learning_objectives
    assert mission.estimated_duration_minutes > 0
    assert mission.estimated_duration_label
    assert mission.completion_definition
    assert mission.educational_rationale or mission.why_this_mission
    assert mission.prerequisite_status_label
    assert mission.supporting_evidence

    assert snap.journey.why_today
    assert snap.journey.unlocks_next

    assert snap.pacing.pacing_summary
    assert snap.pacing.feasibility_label
    assert snap.pacing.exam_date_aware


def test_runtime_a_student_has_no_educational_experience(ctx):
    """Students without Runtime C enrolment keep the Runtime A default path."""
    user = make_user("px001-runtime-a@example.com")
    snap = EducationalExperienceService().load_for_user(user.id)
    assert snap is None


def test_page_view_model_carries_educational_panel(ctx):
    """Home / Journey pages include educational view-model fields."""
    subject = publish_subject("PXE2", title="Panel Subject")
    user = make_user("px001-page@example.com")
    _enrol_runtime_c(user, subject)

    snap = EducationalExperienceService().load_for_user(user.id)
    assert snap is not None
    page = page_from_educational_experience(snap, surface="home")
    assert page.educational is not None
    assert page.educational.active
    assert page.educational.today_topic_title
    assert page.educational.position_label
    assert page.educational.learning_objectives
    assert page.educational.mission_rationale or page.educational.why_this_mission
    assert page.educational.estimated_duration_label
    assert page.educational.completion_definition
    assert page.educational.why_today
    assert page.educational.progress_label
    assert page.educational.pacing_summary
    assert page.home is not None
    assert page.home.recommendation.has_recommendation
    assert page.home.explanation is not None
    assert page.home.explanation.why_recommended


def test_home_and_journey_http_render_educational_fields(ctx, client, app):
    """Acceptance: Runtime C student sees coherent educational mission chrome.

    MISSION-002: Home projects the mission panel (ds_mission_panel) rather than
    the legacy educational_experience data-edu-field strip. Assert student-visible
    educational language and zero node-id leakage.
    """
    subject = publish_subject("PXE3", title="HTTP Subject")
    user = make_user("px001-http@example.com")
    _enrol_runtime_c(user, subject)

    with client.session_transaction() as sess:
        sess["_user_id"] = str(user.id)
        sess["_fresh"] = True

    home = client.get("/student/")
    assert home.status_code == 200
    body = home.get_data(as_text=True)
    assert "ds-mission-panel" in body or "Today" in body
    assert "Study" in body
    assert "Why this mission" in body or "why this mission" in body.lower()
    assert "node-" not in body.lower()
    assert "Core concepts" in body or "1.1" in body

    journey = client.get("/student/journey")
    assert journey.status_code == 200
    jbody = journey.get_data(as_text=True)
    assert journey.status_code == 200
    assert "node-" not in jbody.lower()
    # Journey may still include the educational strip or topic list.
    assert "Core concepts" in jbody or "1.1" in jbody or "Journey" in jbody


def test_coexistence_runtime_a_home_unchanged_without_runtime_c(ctx, client):
    """Runtime A students do not see the Runtime C educational panel."""
    user = User(email="px001-a-only@example.com", is_active_user=True)
    user.set_password("password123")
    user.alpha_onboarding_completed = True
    db.session.add(user)
    db.session.commit()

    with client.session_transaction() as sess:
        sess["_user_id"] = str(user.id)
        sess["_fresh"] = True

    response = client.get("/student/", follow_redirects=True)
    body = response.get_data(as_text=True)
    assert 'data-educational-experience="runtime-c"' not in body
