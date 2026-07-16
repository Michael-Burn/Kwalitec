"""RIP-002 Contributor Recognition tests.

Covers automatic badge thresholds, journey progress, Founder manual awards,
thank-you and profile display, educational state isolation, and absence of
leaderboards.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.extensions import db
from app.models.curriculum import Curriculum, Topic
from app.models.mission import Mission, MissionTask
from app.models.research_feedback import (
    ResearchContributorBadge,
    ResearchFeedbackReview,
    ResearchFeedbackSubmission,
)
from app.models.study_plan import StudyPlan, WeekPlan
from app.models.subject import Subject
from app.models.topic_progress import TopicProgress
from app.models.user import User
from app.services.contributor_recognition_service import (
    BADGE_CORE_CONTRIBUTOR,
    BADGE_EXPLORER,
    BADGE_FOUNDERS_CIRCLE,
    BADGE_PRODUCT_SHAPER,
    BADGE_RESEARCH_PARTNER,
    ContributorRecognitionService,
)
from app.services.research_feedback_service import (
    SOURCE_SETTINGS,
    SOURCE_STUDY_SESSION,
    ResearchFeedbackService,
)


def _make_user(email: str) -> User:
    user = User(email=email, is_active_user=True)
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user


def _make_curriculum(
    exam_name: str, topic_names: list[str]
) -> tuple[Curriculum, list[Topic]]:
    curriculum = Curriculum(exam_name=exam_name, version="2025", active=True)
    db.session.add(curriculum)
    db.session.flush()
    topics: list[Topic] = []
    for index, name in enumerate(topic_names, start=1):
        topic = Topic(
            name=name,
            curriculum_id=curriculum.id,
            order=index,
            recommended_minutes=60,
            active=True,
        )
        db.session.add(topic)
        topics.append(topic)
    db.session.flush()
    return curriculum, topics


def _make_active_plan(
    user_id: int, *, curriculum: Curriculum, exam_name: str
) -> StudyPlan:
    plan = StudyPlan(
        user_id=user_id,
        curriculum_id=curriculum.id,
        curriculum_version=curriculum.version,
        exam_name=exam_name,
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


def _make_mission(
    user_id: int,
    *,
    study_plan_id: int | None = None,
    status: str = "Completed",
) -> Mission:
    subject = Subject(user_id=user_id, name="Exam Paper")
    db.session.add(subject)
    db.session.flush()
    mission = Mission(
        user_id=user_id,
        subject_id=subject.id,
        study_plan_id=study_plan_id,
        mission_date=date.today(),
        title="Study today",
        status=status,
    )
    mission.tasks.append(MissionTask(title="Focus study", order=0, completed=True))
    mission.tasks.append(MissionTask(title="Practice", order=1, completed=True))
    db.session.add(mission)
    db.session.commit()
    return mission


def _submit_checkin(user_id: int) -> None:
    ResearchFeedbackService.submit_checkin(
        user_id,
        experience_rating="Good",
        feature_helped_most="Dashboard",
        friction_area="Nothing",
        confidence_rating="High",
        return_intent="Probably",
        submission_source=SOURCE_SETTINGS,
    )


@pytest.mark.usefixtures("ctx")
class TestAutomaticBadges:
    def test_explorer_on_first_checkin(self, user):
        _submit_checkin(user.id)
        badges = ResearchContributorBadge.query.filter_by(user_id=user.id).all()
        slugs = {b.badge_slug for b in badges}
        assert BADGE_EXPLORER in slugs
        assert len(slugs) == 1

    def test_research_partner_at_ten_checkins(self, user):
        for _ in range(10):
            _submit_checkin(user.id)
        slugs = {
            b.badge_slug
            for b in ResearchContributorBadge.query.filter_by(user_id=user.id)
        }
        assert BADGE_EXPLORER in slugs
        assert BADGE_RESEARCH_PARTNER in slugs
        assert BADGE_CORE_CONTRIBUTOR not in slugs

    def test_core_contributor_at_twenty_five_checkins(self, user):
        for _ in range(25):
            _submit_checkin(user.id)
        slugs = {
            b.badge_slug
            for b in ResearchContributorBadge.query.filter_by(user_id=user.id)
        }
        assert BADGE_CORE_CONTRIBUTOR in slugs

    def test_badges_not_re_awarded(self, user):
        for _ in range(3):
            _submit_checkin(user.id)
        count = ResearchContributorBadge.query.filter_by(
            user_id=user.id, badge_slug=BADGE_EXPLORER
        ).count()
        assert count == 1


@pytest.mark.usefixtures("ctx")
class TestJourneySummary:
    def test_progress_before_first_badge(self, user):
        journey = ContributorRecognitionService.get_journey_summary(user.id)
        assert journey.contribution_count == 0
        assert journey.current_badge is None
        assert journey.next_badge is not None
        assert journey.next_badge.slug == BADGE_EXPLORER
        assert journey.progress_target == 1

    def test_progress_after_explorer(self, user):
        _submit_checkin(user.id)
        journey = ContributorRecognitionService.get_journey_summary(user.id)
        assert journey.contribution_count == 1
        assert journey.current_badge.slug == BADGE_EXPLORER
        assert journey.next_badge.slug == BADGE_RESEARCH_PARTNER
        assert journey.progress_current == 1
        assert journey.progress_target == 10

    def test_progress_toward_core_contributor(self, user):
        for _ in range(12):
            _submit_checkin(user.id)
        journey = ContributorRecognitionService.get_journey_summary(user.id)
        assert journey.current_badge.slug == BADGE_RESEARCH_PARTNER
        assert journey.next_badge.slug == BADGE_CORE_CONTRIBUTOR
        assert journey.progress_current == 12
        assert journey.progress_target == 25


@pytest.mark.usefixtures("ctx")
class TestFounderAwards:
    def test_implemented_awards_product_shaper(self, user):
        _submit_checkin(user.id)
        submission = ResearchFeedbackSubmission.query.filter_by(user_id=user.id).one()
        founder = _make_user("founder@kwalitec.example")

        result = ContributorRecognitionService.founder_review_submission(
            submission.id,
            founder.id,
            implemented=True,
        )
        assert result.newly_earned_badges == (BADGE_PRODUCT_SHAPER,)
        review = ResearchFeedbackReview.query.filter_by(
            submission_id=submission.id
        ).one()
        assert review.is_implemented is True
        assert review.is_helpful is False

    def test_helpful_and_insightful_do_not_award_product_shaper(self, user):
        _submit_checkin(user.id)
        submission = ResearchFeedbackSubmission.query.filter_by(user_id=user.id).one()
        founder = _make_user("founder@kwalitec.example")

        result = ContributorRecognitionService.founder_review_submission(
            submission.id,
            founder.id,
            helpful=True,
            insightful=True,
        )
        assert result.newly_earned_badges == ()
        assert ResearchContributorBadge.query.filter_by(
            user_id=user.id, badge_slug=BADGE_PRODUCT_SHAPER
        ).count() == 0

    def test_founders_circle_invitation_only(self, user):
        founder = _make_user("founder@kwalitec.example")
        badge = ContributorRecognitionService.award_founders_circle(user.id, founder.id)
        assert badge is not None
        assert badge.badge_slug == BADGE_FOUNDERS_CIRCLE
        assert ContributorRecognitionService.award_founders_circle(
            user.id, founder.id
        ) is None


@pytest.mark.usefixtures("ctx")
class TestEducationalIsolation:
    def test_recognition_does_not_mutate_educational_state(self, user):
        curriculum, topics = _make_curriculum("IFoA CS1", ["Topic A"])
        plan = _make_active_plan(user.id, curriculum=curriculum, exam_name="IFoA CS1")
        mission = _make_mission(user.id, study_plan_id=plan.id)
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            mastery_score=40.0,
            current_stage=TopicProgress.STAGE_LEARNING,
            revision_count=1,
            average_accuracy=50.0,
            next_review_date=date.today() + timedelta(days=3),
            completed=False,
        )
        db.session.add(progress)
        db.session.commit()

        before_status = mission.status
        before_mastery = progress.mastery_score

        for _ in range(3):
            ResearchFeedbackService.submit_checkin(
                user.id,
                experience_rating="Good",
                feature_helped_most="Study Plan",
                friction_area="Nothing",
                confidence_rating="High",
                return_intent="Definitely",
                submission_source=SOURCE_STUDY_SESSION,
                mission_id=mission.id,
            )

        db.session.refresh(mission)
        db.session.refresh(progress)
        assert mission.status == before_status
        assert progress.mastery_score == before_mastery
        assert ResearchContributorBadge.query.filter_by(user_id=user.id).count() >= 1


@pytest.mark.usefixtures("ctx")
class TestRecognitionHttp:
    def test_thank_you_shows_journey(self, logged_in_client, user):
        _submit_checkin(user.id)
        response = logged_in_client.get("/research/thank-you")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert 'data-rip002-thank-you="1"' in body
        assert "Check-ins completed" in body
        assert "Explorer" in body
        assert "your rank" not in body.lower()
        assert "top contributor" not in body.lower()

    def test_profile_shows_research_journey(self, logged_in_client, user):
        _submit_checkin(user.id)
        response = logged_in_client.get("/settings/profile")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert 'data-rip002-profile="1"' in body
        assert "Research Journey" in body
        assert "1 check-ins" in body
        assert "your rank" not in body.lower()
        assert "top contributor" not in body.lower()

    def test_first_checkin_celebrates_new_badge(self, logged_in_client, user):
        response = logged_in_client.post(
            "/research/checkin",
            data={
                "experience_rating": "Good",
                "feature_helped_most": "Dashboard",
                "friction_area": "Nothing",
                "confidence_rating": "High",
                "return_intent": "Probably",
                "submission_source": SOURCE_SETTINGS,
                "free_text": "",
                "classification": "",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "You earned the" in body
        assert "Explorer" in body

    def test_founder_review_forbidden_for_student(self, client, ctx, app, user):
        app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
        _submit_checkin(user.id)
        submission = ResearchFeedbackSubmission.query.filter_by(user_id=user.id).one()
        client.post(
            "/auth/login",
            data={"email": user.email, "password": "password123"},
            follow_redirects=True,
        )
        response = client.post(
            f"/research/founder/review/{submission.id}",
            data={"helpful": "y"},
        )
        assert response.status_code == 403

    def test_founder_review_awards_product_shaper(self, client, ctx, app, user):
        app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
        founder = _make_user("founder@kwalitec.example")
        _submit_checkin(user.id)
        submission = ResearchFeedbackSubmission.query.filter_by(user_id=user.id).one()

        client.post(
            "/auth/login",
            data={"email": founder.email, "password": "password123"},
            follow_redirects=True,
        )
        response = client.post(
            f"/research/founder/review/{submission.id}",
            data={"implemented": "y"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert ResearchContributorBadge.query.filter_by(
            user_id=user.id, badge_slug=BADGE_PRODUCT_SHAPER
        ).count() == 1
