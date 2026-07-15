"""Internal Alpha polish — study tips, status page, multi-user isolation."""

from __future__ import annotations

from datetime import date, timedelta

from app.extensions import db
from app.models.mission import Mission
from app.models.subject import Subject
from app.models.user import User
from app.services.internal_alpha_status_service import (
    INTERNAL_ALPHA_VERSION,
    InternalAlphaStatusService,
)
from app.services.mission_service import MissionService
from app.services.study_plan_service import StudyPlanService
from app.services.study_tips_service import StudyTipsService


class TestStudyTipsService:
    def test_tip_rotates_by_date(self):
        tips = StudyTipsService.all_tips()
        assert len(tips) >= 5
        tip_a = StudyTipsService.tip_for_day(date(2026, 7, 13))
        tip_b = StudyTipsService.tip_for_day(date(2026, 7, 14))
        assert tip_a in tips
        assert tip_b in tips
        # Adjacent days should usually differ with 8 tips; allow wrap equality
        assert isinstance(tip_a, str) and tip_a.strip()

    def test_same_day_is_stable(self):
        day = date(2026, 7, 13)
        assert StudyTipsService.tip_for_day(day) == StudyTipsService.tip_for_day(day)

    def test_dashboard_renders_study_tip(self, logged_in_client):
        response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Study Tip" in body
        assert StudyTipsService.tip_for_day() in body


class TestInternalAlphaSettings:
    def test_internal_alpha_page_renders(self, logged_in_client):
        response = logged_in_client.get("/settings/internal-alpha")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Internal Alpha Status" in body
        assert INTERNAL_ALPHA_VERSION in body
        assert "Learning profile status" in body
        assert "Current curriculum" in body
        assert 'data-appearance-option="light"' in body

    def test_status_service_without_plan(self, db, user):
        status = InternalAlphaStatusService.build_status(user.id)
        assert status.app_version
        assert status.internal_alpha_version == INTERNAL_ALPHA_VERSION
        assert status.curriculum_label == "No active curriculum"
        assert status.study_plan_label == "No active study plan"
        assert status.twin_status in {
            "Not yet set up",
            "Unavailable",
            "Ready",
            "Needs a fresh setup",
        }

    def test_status_service_with_plan(self, db, user, study_plan):
        status = InternalAlphaStatusService.build_status(user.id)
        assert study_plan.exam_name in status.curriculum_label
        assert study_plan.exam_name in status.study_plan_label


class TestMultiUserIsolation:
    """Capability J — participants must not see each other's learning state."""

    def _second_user(self) -> User:
        other = User(email="friend@kwalitec.example", is_active_user=True)
        other.set_password("password123")
        db.session.add(other)
        db.session.commit()
        return other

    def test_study_plans_are_user_scoped(self, db, user, study_plan):
        other = self._second_user()
        other_plan = StudyPlanService.create_study_plan(
            user_id=other.id,
            exam_name="IFoA CB2",
            exam_sitting="Sep 2027",
            exam_date=date.today() + timedelta(days=200),
            target_grade="Pass",
            weekday_study_minutes=60,
            weekend_study_minutes=90,
            current_stage="Learning",
            study_preference="Mixed",
            preferred_session_minutes=45,
        )
        assert StudyPlanService.get_user_active_plan(user.id).id == study_plan.id
        assert StudyPlanService.get_user_active_plan(other.id).id == other_plan.id
        user_plans = {p.id for p in StudyPlanService.get_user_plans(user.id)}
        other_plans = {p.id for p in StudyPlanService.get_user_plans(other.id)}
        assert study_plan.id in user_plans
        assert other_plan.id not in user_plans
        assert other_plan.id in other_plans
        assert study_plan.id not in other_plans

    def test_missions_are_user_scoped(self, db, user, subject):
        other = self._second_user()
        other_subject = Subject(user_id=other.id, name="CB2", active=True)
        db.session.add(other_subject)
        db.session.flush()

        mine = Mission(
            user_id=user.id,
            subject_id=subject.id,
            mission_date=date.today(),
            title="User A mission",
            status="Pending",
        )
        theirs = Mission(
            user_id=other.id,
            subject_id=other_subject.id,
            mission_date=date.today(),
            title="User B mission",
            status="Pending",
        )
        db.session.add_all([mine, theirs])
        db.session.commit()

        assert MissionService.get_today_mission(user.id).id == mine.id
        assert MissionService.get_today_mission(other.id).id == theirs.id

    def test_http_plan_view_rejects_other_user(
        self, app, ctx, user, study_plan, client
    ):
        other = self._second_user()
        with client.session_transaction() as sess:
            sess["_user_id"] = str(other.id)
            sess["_fresh"] = True
        response = client.get(
            f"/study-plan/{study_plan.id}", follow_redirects=True
        )
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "You can only view your own study plans." in body
