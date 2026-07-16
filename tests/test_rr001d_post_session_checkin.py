"""RR-001D Post-Session Check-in Reliability regression tests.

Founder observation (FC-001): the Settings check-in route worked, but the
post-session feedback invitation did not — selecting it bounced the student
back to the dashboard.

Root cause: the post-session invitation always carries the just-finished
``mission_id``, but eligibility re-derived "today's mission" via a
date + active-plan scoped lookup and ignored the explicit mission. Any
mismatch (date rollover, plan scoping) resolved to ``None`` and the student
was redirected away, while the Settings path skipped the gate entirely.

Fix: honour the explicit, owned ``mission_id`` with study activity so the
invitation deterministically opens the Product Check-in.

Acceptance: after completing a Study Session, selecting the feedback
invitation always opens the Product Check-in successfully.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.extensions import db
from app.models.curriculum import Curriculum, Topic
from app.models.mission import Mission, MissionTask
from app.models.study_plan import StudyPlan, WeekPlan
from app.models.subject import Subject
from app.services.research_feedback_service import ResearchFeedbackService


def _make_active_plan(user_id: int) -> StudyPlan:
    curriculum = Curriculum(exam_name="IFoA CS1", version="2025", active=True)
    db.session.add(curriculum)
    db.session.flush()
    topic = Topic(
        name="Data analysis",
        curriculum_id=curriculum.id,
        order=1,
        recommended_minutes=60,
        active=True,
    )
    db.session.add(topic)
    plan = StudyPlan(
        user_id=user_id,
        curriculum_id=curriculum.id,
        curriculum_version=curriculum.version,
        exam_name="IFoA CS1",
        exam_sitting="April 2027",
        exam_date=date.today() + timedelta(days=180),
        weekday_study_minutes=90,
        weekend_study_minutes=120,
        current_stage="Chapter 1",
        study_preference="Mixed",
        target_grade="A",
        preferred_session_minutes=60,
        active=True,
        curriculum_topic_code=None,
    )
    db.session.add(plan)
    db.session.flush()
    week = WeekPlan(
        study_plan_id=plan.id,
        week_number=1,
        start_date=date.today() - timedelta(days=2),
        end_date=date.today() + timedelta(days=4),
    )
    db.session.add(week)
    db.session.commit()
    return plan


def _make_completed_mission(
    user_id: int,
    *,
    study_plan_id: int | None,
    mission_date: date,
) -> Mission:
    subject = Subject(user_id=user_id, name="Exam Paper")
    db.session.add(subject)
    db.session.flush()
    mission = Mission(
        user_id=user_id,
        subject_id=subject.id,
        study_plan_id=study_plan_id,
        mission_date=mission_date,
        title="Study today",
        status="Completed",
    )
    mission.tasks.append(MissionTask(title="Focus study", order=0, completed=True))
    mission.tasks.append(MissionTask(title="Practice", order=1, completed=True))
    db.session.add(mission)
    db.session.commit()
    return mission


@pytest.mark.usefixtures("ctx")
class TestPostSessionEligibilityHonoursMission:
    def test_completed_mission_today_is_eligible_with_mission_id(self, user):
        plan = _make_active_plan(user.id)
        mission = _make_completed_mission(
            user.id, study_plan_id=plan.id, mission_date=date.today()
        )

        result = ResearchFeedbackService.is_eligible_for_invitation(
            user.id, mission_id=mission.id
        )
        assert result.eligible is True
        assert result.reason == "session_completed"
        assert result.mission is not None
        assert result.mission.id == mission.id

    def test_completed_mission_not_dated_today_still_eligible_with_mission_id(
        self, user
    ):
        """Reliability fix: a just-finished mission whose stored date is not
        today (e.g. date rollover) must still open the check-in when its id is
        carried by the invitation — the old date-scoped lookup returned None."""
        plan = _make_active_plan(user.id)
        yesterday = date.today() - timedelta(days=1)
        mission = _make_completed_mission(
            user.id, study_plan_id=plan.id, mission_date=yesterday
        )

        # Old behaviour (no mission_id) would resolve today's mission → None.
        without_id = ResearchFeedbackService.is_eligible_for_invitation(user.id)
        assert without_id.eligible is False
        assert without_id.reason == "no_mission_today"

        # With the explicit mission id, eligibility is honoured.
        with_id = ResearchFeedbackService.is_eligible_for_invitation(
            user.id, mission_id=mission.id
        )
        assert with_id.eligible is True
        assert with_id.mission is not None
        assert with_id.mission.id == mission.id

    def test_foreign_mission_id_is_ignored(self, user):
        """A mission id the student does not own must not grant eligibility."""
        result = ResearchFeedbackService.is_eligible_for_invitation(
            user.id, mission_id=999999
        )
        assert result.eligible is False
        assert result.reason == "no_mission_today"


@pytest.mark.usefixtures("ctx")
class TestPostSessionInvitationHttp:
    def test_invitation_link_opens_checkin(self, logged_in_client, user):
        plan = _make_active_plan(user.id)
        mission = _make_completed_mission(
            user.id, study_plan_id=plan.id, mission_date=date.today()
        )

        response = logged_in_client.get(
            f"/research/checkin?source=study_session&mission_id={mission.id}",
            follow_redirects=False,
        )
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert 'data-rip001-checkin="1"' in body
        assert "Daily Reflection" in body

    def test_invitation_link_opens_checkin_after_date_rollover(
        self, logged_in_client, user
    ):
        plan = _make_active_plan(user.id)
        yesterday = date.today() - timedelta(days=1)
        mission = _make_completed_mission(
            user.id, study_plan_id=plan.id, mission_date=yesterday
        )

        response = logged_in_client.get(
            f"/research/checkin?source=study_session&mission_id={mission.id}",
            follow_redirects=False,
        )
        assert response.status_code == 200
        assert 'data-rip001-checkin="1"' in response.get_data(as_text=True)

    def test_invitation_without_activity_still_gated(self, logged_in_client):
        """Direct study_session entry with no study activity keeps the soft gate."""
        response = logged_in_client.get(
            "/research/checkin?source=study_session",
            follow_redirects=True,
        )
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Product Check-in is available after some study activity" in body
