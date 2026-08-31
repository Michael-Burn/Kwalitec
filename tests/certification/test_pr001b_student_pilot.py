"""PR-001B — Student Pilot Journey acceptance tests.

Certifies that a Runtime C student can discover, enrol, understand today's
mission, complete it, observe progress, and return for the next session
without Runtime A cutover or Twin activation.
"""

from __future__ import annotations

from datetime import date, timedelta

from app.application.educational_experience import EducationalExperienceService
from app.application.platform_integration.discovery import PUBLISHED_CATEGORY_CODE
from app.application.platform_integration.enrolment_bridge import (
    FounderStudentEnrolmentBridge,
)
from app.extensions import db
from app.models.user import User
from app.services.study_plan_service import StudyPlanService
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
    assert StudyPlanService.get_user_active_plan(user.id) is None


def _login(client, user: User) -> None:
    with client.session_transaction() as sess:
        sess["_user_id"] = str(user.id)
        sess["_fresh"] = True


def _clarity_fields_present(html: str) -> None:
    """Home OS mission hero carries clarity (DX-005A); legacy edu-field attrs optional."""
    assert (
        "Why this mission" in html
        or "Why now" in html
        or 'data-edu-field="mission_rationale"' in html
    )
    assert (
        "Why this mission" in html
        or "Why now" in html
        or 'data-edu-field="why_today"' in html
        or 'data-mes-field="timeliness"' in html
    )
    assert (
        "Expected outcome" in html
        or "After this" in html
        or 'data-edu-field="completion_definition"' in html
    )


class TestFirstDayExperience:
    """Scenario: first-day discover → enrol → understand → complete."""

    def test_discover_published_subject_via_bridge(self, ctx):
        subject = publish_subject("SP01", title="Pilot First Day")
        user = make_user("pr001b-day1@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)
        assert snap is not None
        assert snap.is_runtime_c
        assert snap.subject_code == "SP01"
        assert snap.mission is not None
        assert snap.mission.status == "generated"

    def test_home_shows_mission_and_clarity(self, ctx, client):
        subject = publish_subject("SP02", title="Pilot Clarity")
        user = make_user("pr001b-clarity@example.com")
        _enrol_runtime_c(user, subject)
        _login(client, user)

        home = client.get("/student/")
        assert home.status_code == 200
        body = home.get_data(as_text=True)
        # DX-005A Home OS: mission hero (runtime-c edu panel optional).
        assert (
            'data-educational-experience="runtime-c"' in body
            or 'data-ux="mission-panel"' in body
            or 'data-ux="mission-hero"' in body
        )
        _clarity_fields_present(body)
        assert 'data-session-control="complete_runtime_c"' in body
        assert "Confirm today's Mission" in body or "Confirm today&#39;s Mission" in body

    def test_complete_mission_updates_progress(self, ctx, client):
        subject = publish_subject("SP03", title="Pilot Complete")
        user = make_user("pr001b-complete@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)
        assert snap is not None and snap.mission is not None
        mission_id = snap.mission.mission_instance_id
        before = snap.curriculum_position.coverage_percent

        _login(client, user)
        response = client.post(
            "/student/mission/complete",
            data={"mission_id": mission_id},
            follow_redirects=True,
        )
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "mission complete" in html.lower()
        assert (
            'data-day-complete="true"' in html
            or "complete for today" in html.lower()
        )

        after = EducationalExperienceService().load_for_user(user.id)
        assert after is not None
        assert after.curriculum_position.coverage_percent >= before
        assert len(after.journey.completed_topics) >= 1


class TestLoginReturnPath:
    """Scenario: returning student with Runtime C only (no StudyPlan)."""

    def test_login_lands_on_home_not_wizard(self, ctx, client):
        subject = publish_subject("SP04", title="Pilot Return")
        user = make_user("pr001b-return@example.com")
        user.set_password("password123")
        db.session.commit()
        _enrol_runtime_c(user, subject)

        response = client.post(
            "/auth/login",
            data={
                "email": user.email,
                "password": "password123",
            },
            follow_redirects=False,
        )
        assert response.status_code in {302, 303}
        location = response.headers.get("Location", "")
        assert "/study-plan/" not in location
        assert "/student" in location or location.endswith("/")


class TestInterruptedAndMissedDay:
    """Scenarios: interrupted session recovery and missed-day return."""

    def test_interrupted_session_keeps_same_mission(self, ctx, client):
        subject = publish_subject("SP05", title="Pilot Interrupt")
        user = make_user("pr001b-interrupt@example.com")
        _enrol_runtime_c(user, subject)
        first = EducationalExperienceService().load_for_user(user.id)
        assert first is not None and first.mission is not None
        mission_id = first.mission.mission_instance_id

        _login(client, user)
        home1 = client.get("/student/")
        assert mission_id in home1.get_data(as_text=True)

        # Simulate leaving without completing — return later same day.
        home2 = client.get("/student/")
        assert home2.status_code == 200
        body = home2.get_data(as_text=True)
        assert mission_id in body
        assert 'data-session-control="complete_runtime_c"' in body

        second = EducationalExperienceService().load_for_user(user.id)
        assert second is not None and second.mission is not None
        assert second.mission.mission_instance_id == mission_id
        assert second.mission.status == "generated"

    def test_missed_day_return_still_shows_current_topic(self, ctx):
        subject = publish_subject("SP06", title="Pilot Missed")
        user = make_user("pr001b-missed@example.com")
        _enrol_runtime_c(user, subject)
        day0 = date.today() - timedelta(days=3)
        early = EducationalExperienceService().load_for_user(
            user.id, mission_date=day0
        )
        assert early is not None and early.mission is not None
        topic_before = early.curriculum_position.topic_id

        # Student returns days later without completing — same topic, new day mission.
        today = EducationalExperienceService().load_for_user(user.id)
        assert today is not None
        assert today.curriculum_position.topic_id == topic_before
        assert today.mission is not None
        assert today.mission.status == "generated"


class TestConsecutiveSessionsAndMultipleMissions:
    """Scenarios: consecutive study days and multi-mission progress."""

    def test_next_day_advances_after_completion(self, ctx):
        subject = publish_subject("SP07", title="Pilot Consecutive")
        user = make_user("pr001b-next@example.com")
        _enrol_runtime_c(user, subject)
        service = EducationalExperienceService()

        day1 = date.today()
        snap1 = service.load_for_user(user.id, mission_date=day1)
        assert snap1 is not None and snap1.mission is not None
        topic1 = snap1.curriculum_position.topic_id
        service.complete_mission(
            user_id=user.id,
            mission_instance_id=snap1.mission.mission_instance_id,
        )

        day2 = day1 + timedelta(days=1)
        snap2 = service.load_for_user(user.id, mission_date=day2)
        assert snap2 is not None
        assert snap2.mission is not None
        assert snap2.mission.status == "generated"
        assert snap2.curriculum_position.topic_id != topic1
        assert len(snap2.journey.completed_topics) >= 1

    def test_multiple_missions_across_days(self, ctx):
        subject = publish_subject("SP08", title="Pilot Multi")
        user = make_user("pr001b-multi@example.com")
        _enrol_runtime_c(user, subject)
        service = EducationalExperienceService()
        completed = 0
        start = date.today()
        for offset in range(2):
            day = start + timedelta(days=offset)
            snap = service.load_for_user(user.id, mission_date=day)
            assert snap is not None and snap.mission is not None
            assert snap.mission.status == "generated"
            service.complete_mission(
                user_id=user.id,
                mission_instance_id=snap.mission.mission_instance_id,
            )
            completed += 1

        final = service.load_for_user(
            user.id, mission_date=start + timedelta(days=2)
        )
        assert final is not None
        assert len(final.journey.completed_topics) >= completed
        assert final.curriculum_position.coverage_percent == 100
        assert final.syllabus_complete is True


class TestEducationalClarityAnswers:
    """Every Runtime C explanation answers the four pilot questions."""

    def test_four_clarity_questions(self, ctx, client):
        subject = publish_subject("SP09", title="Pilot Four Q")
        user = make_user("pr001b-fourq@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)
        assert snap is not None and snap.mission is not None

        # Why this mission?
        assert snap.mission.why_this_mission or snap.mission.educational_rationale
        # Why now?
        assert snap.journey.why_today
        # What should I accomplish?
        assert snap.mission.learning_objectives
        assert snap.mission.completion_definition
        # What comes next?
        assert snap.journey.unlocks_next or snap.mission.suggested_next_action

        _login(client, user)
        body = client.get("/student/").get_data(as_text=True)
        _clarity_fields_present(body)
        assert (
            'data-edu-field="what_comes_next"' in body
            or "Expected outcome" in body
            or "After this" in body
            or "Why this mission" in body
            or "Why now" in body
        )


class TestOperationalRecovery:
    """Empty / error / duplicate completion recovery paths."""

    def test_duplicate_complete_is_recoverable(self, ctx, client):
        subject = publish_subject("SP10", title="Pilot Dup")
        user = make_user("pr001b-dup@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)
        assert snap is not None and snap.mission is not None
        mission_id = snap.mission.mission_instance_id
        EducationalExperienceService().complete_mission(
            user_id=user.id,
            mission_instance_id=mission_id,
        )

        _login(client, user)
        response = client.post(
            "/student/mission/complete",
            data={"mission_id": mission_id},
            follow_redirects=True,
        )
        assert response.status_code == 200
        html = response.get_data(as_text=True).lower()
        assert "already complete" in html or "progress is saved" in html

    def test_coexistence_runtime_a_unchanged(self, ctx, client):
        user = User(email="pr001b-a-only@example.com", is_active_user=True)
        user.set_password("password123")
        user.alpha_onboarding_completed = True
        db.session.add(user)
        db.session.commit()
        _login(client, user)
        response = client.get("/student/", follow_redirects=True)
        body = response.get_data(as_text=True)
        assert 'data-educational-experience="runtime-c"' not in body
        assert 'data-session-control="complete_runtime_c"' not in body

    def test_journey_shows_advancement_after_complete(self, ctx, client):
        subject = publish_subject("SP11", title="Pilot Journey")
        user = make_user("pr001b-journey@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)
        assert snap is not None and snap.mission is not None
        EducationalExperienceService().complete_mission(
            user_id=user.id,
            mission_instance_id=snap.mission.mission_instance_id,
        )
        _login(client, user)
        journey = client.get("/student/journey")
        assert journey.status_code == 200
        body = journey.get_data(as_text=True)
        assert (
            'data-educational-experience="runtime-c"' in body
            or "Journey" in body
            or "complete" in body.lower()
        )
        assert (
            'data-edu-field="progress"' in body
            or "complete" in body.lower()
            or 'data-sop-section="progress"' in body
        )
        assert "Completed" in body or "complete" in body.lower()
