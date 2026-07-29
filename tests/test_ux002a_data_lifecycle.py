"""UX-002A — Study Plan delete lifecycle hardening."""

from __future__ import annotations

from datetime import date, timedelta

from app.extensions import db
from app.models.mission import Mission
from app.models.research_feedback import ResearchFeedbackSubmission
from app.models.study_plan import StudyPlan, WeekPlan
from app.models.subject import Subject
from app.services.educational_continuity_service import EducationalContinuityService
from app.services.study_plan_service import StudyPlanService


def _make_plan_with_feedback(user) -> StudyPlan:
    plan = StudyPlan(
        user_id=user.id,
        exam_name="IFoA CM1",
        exam_sitting="September 2026",
        exam_date=date.today() + timedelta(days=90),
        weekday_study_minutes=60,
        weekend_study_minutes=90,
        current_stage="Learning",
        study_preference="Mixed",
        target_grade="Strong Pass",
        preferred_session_minutes=60,
        active=True,
    )
    db.session.add(plan)
    db.session.flush()

    week = WeekPlan(
        study_plan_id=plan.id,
        week_number=1,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=6),
    )
    db.session.add(week)

    subject = Subject(user_id=user.id, name="CM1", colour="#007bff", active=True)
    db.session.add(subject)
    db.session.flush()

    mission = Mission(
        user_id=user.id,
        subject_id=subject.id,
        mission_date=date.today(),
        title="Study CM1",
        status="Pending",
        study_plan_id=plan.id,
    )
    db.session.add(mission)
    db.session.flush()

    feedback = ResearchFeedbackSubmission(
        user_id=user.id,
        product_version="2.0.0",
        study_plan_id=plan.id,
        mission_id=mission.id,
        experience_rating="good",
        feature_helped_most="study_plan",
        friction_area="none",
        confidence_rating="medium",
        return_intent="yes",
        submission_source="test",
    )
    db.session.add(feedback)
    db.session.commit()
    return plan


class TestUx002AStudyPlanDeleteLifecycle:
    """Study Plan deletion must never 500 on research-feedback FKs."""

    def test_release_clears_research_feedback_plan_pointers(self, ctx, user):
        plan = _make_plan_with_feedback(user)
        detached = EducationalContinuityService.release_plan_planning_artifacts(plan)
        db.session.flush()

        assert detached >= 2
        assert Mission.query.filter_by(study_plan_id=plan.id).count() == 0
        assert (
            ResearchFeedbackSubmission.query.filter_by(study_plan_id=plan.id).count()
            == 0
        )
        # History rows retained with cleared plan pointer.
        assert ResearchFeedbackSubmission.query.count() == 1
        assert Mission.query.count() == 1

    def test_delete_study_plan_with_research_feedback_succeeds(self, ctx, user):
        plan = _make_plan_with_feedback(user)
        plan_id = plan.id
        feedback_id = ResearchFeedbackSubmission.query.one().id
        mission_id = Mission.query.one().id

        StudyPlanService.delete_study_plan(plan_id, user.id)

        assert StudyPlan.query.get(plan_id) is None
        assert WeekPlan.query.filter_by(study_plan_id=plan_id).count() == 0
        feedback = db.session.get(ResearchFeedbackSubmission, feedback_id)
        assert feedback is not None
        assert feedback.study_plan_id is None
        mission = db.session.get(Mission, mission_id)
        assert mission is not None
        assert mission.study_plan_id is None

    def test_delete_route_returns_redirect_not_500(self, logged_in_client, ctx, user):
        plan = _make_plan_with_feedback(user)
        response = logged_in_client.post(
            f"/study-plan/{plan.id}/delete",
            follow_redirects=False,
        )
        assert response.status_code in {302, 303}
        assert StudyPlan.query.get(plan.id) is None
        assert ResearchFeedbackSubmission.query.one().study_plan_id is None
