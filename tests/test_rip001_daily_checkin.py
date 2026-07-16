"""RIP-001 Daily Reflection & Product Check-in tests.

Covers eligibility, optional check-in, unlimited submissions, persistence,
contribution creation, thank-you page, settings entry, and educational
state isolation.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.extensions import db
from app.models.curriculum import Curriculum, Topic
from app.models.mission import Mission, MissionTask
from app.models.research_feedback import (
    ResearchContribution,
    ResearchFeedbackSubmission,
)
from app.models.study_plan import StudyPlan, WeekPlan
from app.models.subject import Subject
from app.models.topic_progress import TopicProgress
from app.services.research_feedback_service import (
    PRODUCT_VERSION,
    SOURCE_SETTINGS,
    SOURCE_STUDY_SESSION,
    ResearchFeedbackService,
)


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
    status: str = "Pending",
    task_completed: bool = False,
) -> Mission:
    subject = Subject(user_id=user_id, name="Exam Paper")
    db.session.add(subject)
    db.session.flush()
    # Completed missions must have all tasks done — MissionService reopens otherwise.
    all_done = status == "Completed"
    mission = Mission(
        user_id=user_id,
        subject_id=subject.id,
        study_plan_id=study_plan_id,
        mission_date=date.today(),
        title="Study today",
        status=status,
    )
    mission.tasks.append(
        MissionTask(
            title="Focus study",
            order=0,
            completed=all_done or task_completed,
        )
    )
    mission.tasks.append(
        MissionTask(title="Practice", order=1, completed=all_done)
    )
    db.session.add(mission)
    db.session.commit()
    return mission


def _valid_payload(**overrides) -> dict:
    data = {
        "experience_rating": "Good",
        "feature_helped_most": "Study Session",
        "friction_area": "Nothing",
        "confidence_rating": "High",
        "return_intent": "Probably",
        "submission_source": SOURCE_STUDY_SESSION,
        "free_text": "",
        "classification": "",
    }
    data.update(overrides)
    return data


@pytest.mark.usefixtures("ctx")
class TestCheckinEligibility:
    def test_not_eligible_without_mission(self, user):
        result = ResearchFeedbackService.is_eligible_for_invitation(user.id)
        assert result.eligible is False
        assert result.reason == "no_mission_today"

    def test_not_eligible_when_pending_with_no_tasks_done(self, user):
        curriculum, _topics = _make_curriculum("IFoA CS1", ["Topic A"])
        plan = _make_active_plan(user.id, curriculum=curriculum, exam_name="IFoA CS1")
        _make_mission(user.id, study_plan_id=plan.id, status="Pending")

        result = ResearchFeedbackService.is_eligible_for_invitation(user.id)
        assert result.eligible is False
        assert result.reason == "no_study_activity"

    def test_eligible_when_session_completed(self, user):
        curriculum, _topics = _make_curriculum("IFoA CS1", ["Topic A"])
        plan = _make_active_plan(user.id, curriculum=curriculum, exam_name="IFoA CS1")
        mission = _make_mission(
            user.id, study_plan_id=plan.id, status="Completed", task_completed=True
        )

        result = ResearchFeedbackService.is_eligible_for_invitation(user.id)
        assert result.eligible is True
        assert result.reason == "session_completed"
        assert result.mission is not None
        assert result.mission.id == mission.id

    def test_eligible_when_partial_mission_progress(self, user):
        curriculum, _topics = _make_curriculum("IFoA CS1", ["Topic A"])
        plan = _make_active_plan(user.id, curriculum=curriculum, exam_name="IFoA CS1")
        _make_mission(
            user.id,
            study_plan_id=plan.id,
            status="In Progress",
            task_completed=True,
        )

        result = ResearchFeedbackService.is_eligible_for_invitation(user.id)
        assert result.eligible is True
        assert result.reason == "mission_partial"


@pytest.mark.usefixtures("ctx")
class TestSubmitCheckinService:
    def test_persists_structured_answers_and_contribution(self, user):
        curriculum, _topics = _make_curriculum("IFoA CS1", ["Topic A"])
        plan = _make_active_plan(user.id, curriculum=curriculum, exam_name="IFoA CS1")
        mission = _make_mission(
            user.id, study_plan_id=plan.id, status="Completed", task_completed=True
        )

        result = ResearchFeedbackService.submit_checkin(
            user.id,
            experience_rating="Excellent",
            feature_helped_most="Today's Study Session",
            friction_area="Navigation",
            confidence_rating="Very High",
            return_intent="Definitely",
            submission_source=SOURCE_STUDY_SESSION,
            mission_id=mission.id,
            study_plan_id=plan.id,
        )

        submission = result.submission
        assert submission.user_id == user.id
        assert submission.product_version == PRODUCT_VERSION
        assert submission.study_plan_id == plan.id
        assert submission.mission_id == mission.id
        assert submission.experience_rating == "Excellent"
        assert submission.feature_helped_most == "Today's Study Session"
        assert submission.friction_area == "Navigation"
        assert submission.confidence_rating == "Very High"
        assert submission.return_intent == "Definitely"
        assert submission.free_text is None
        assert submission.classification is None
        assert submission.submission_source == SOURCE_STUDY_SESSION

        contribution = result.contribution
        assert contribution.user_id == user.id
        assert contribution.submission_id == submission.id
        assert ResearchContribution.query.count() == 1

    def test_optional_free_text_requires_classification(self, user):
        with pytest.raises(ValueError, match="classification is required"):
            ResearchFeedbackService.submit_checkin(
                user.id,
                experience_rating="Good",
                feature_helped_most="Dashboard",
                friction_area="Nothing",
                confidence_rating="Neutral",
                return_intent="Not Sure",
                submission_source=SOURCE_SETTINGS,
                free_text="The nav is unclear on mobile.",
            )

    def test_optional_free_text_with_classification(self, user):
        result = ResearchFeedbackService.submit_checkin(
            user.id,
            experience_rating="Okay",
            feature_helped_most="Analytics",
            friction_area="Terminology",
            confidence_rating="Low",
            return_intent="Probably Not",
            submission_source=SOURCE_SETTINGS,
            free_text="Terminology felt dense.",
            classification="Confusing",
        )
        assert result.submission.free_text == "Terminology felt dense."
        assert result.submission.classification == "Confusing"

    def test_unlimited_submissions_allowed(self, user):
        for _ in range(3):
            ResearchFeedbackService.submit_checkin(
                user.id,
                experience_rating="Good",
                feature_helped_most="Settings",
                friction_area="Nothing",
                confidence_rating="High",
                return_intent="Probably",
                submission_source=SOURCE_SETTINGS,
            )
        assert ResearchFeedbackSubmission.query.filter_by(user_id=user.id).count() == 3
        assert ResearchContribution.query.filter_by(user_id=user.id).count() == 3

    def test_does_not_mutate_educational_state(self, user):
        curriculum, topics = _make_curriculum("IFoA CS1", ["Topic A"])
        plan = _make_active_plan(user.id, curriculum=curriculum, exam_name="IFoA CS1")
        mission = _make_mission(
            user.id, study_plan_id=plan.id, status="Completed", task_completed=True
        )
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


@pytest.mark.usefixtures("ctx")
class TestCheckinHttpFlow:
    def test_invitation_on_session_recorded(self, logged_in_client, user):
        curriculum, _topics = _make_curriculum("IFoA CS1", ["Topic A"])
        plan = _make_active_plan(user.id, curriculum=curriculum, exam_name="IFoA CS1")
        mission = _make_mission(
            user.id, study_plan_id=plan.id, status="Completed", task_completed=True
        )

        response = logged_in_client.get(f"/missions/{mission.id}/session/recorded")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Study Session Feedback" in body
        assert 'data-rip001-invite="1"' in body
        assert "Continue" in body
        assert "/research/checkin" in body

    def test_checkin_optional_dismiss(self, logged_in_client):
        response = logged_in_client.get("/research/dismiss", follow_redirects=True)
        assert response.status_code == 200
        assert b"Dashboard" in response.data

    def test_study_session_source_requires_eligibility(self, logged_in_client, user):
        response = logged_in_client.get(
            "/research/checkin?source=study_session",
            follow_redirects=True,
        )
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Product Check-in is available after some study activity" in body

    def test_settings_entry_always_open(self, logged_in_client):
        response = logged_in_client.get(
            "/settings/share-feedback", follow_redirects=True
        )
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Daily Reflection" in body
        assert 'data-rip001-checkin="1"' in body

    def test_sidebar_share_feedback_link(self, logged_in_client):
        response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Share Feedback" in body
        assert "/research/checkin" in body

    def test_submit_checkin_creates_contribution_and_thank_you(
        self, logged_in_client, user
    ):
        curriculum, _topics = _make_curriculum("IFoA CS1", ["Topic A"])
        plan = _make_active_plan(user.id, curriculum=curriculum, exam_name="IFoA CS1")
        mission = _make_mission(
            user.id, study_plan_id=plan.id, status="Completed", task_completed=True
        )

        response = logged_in_client.post(
            "/research/checkin",
            data=_valid_payload(
                submission_source=SOURCE_STUDY_SESSION,
                mission_id=str(mission.id),
                study_plan_id=str(plan.id),
            ),
            follow_redirects=True,
        )
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Thank you for helping improve Kwalitec" in body
        assert 'data-rip001-thank-you="1"' in body
        assert "Return to Dashboard" in body

        submission = ResearchFeedbackSubmission.query.filter_by(user_id=user.id).one()
        assert submission.experience_rating == "Good"
        assert submission.feature_helped_most == "Study Session"
        assert submission.mission_id == mission.id
        assert submission.study_plan_id == plan.id
        assert ResearchContribution.query.filter_by(
            submission_id=submission.id
        ).count() == 1

    def test_free_text_optional_on_http(self, logged_in_client, user):
        response = logged_in_client.post(
            "/research/checkin",
            data=_valid_payload(submission_source=SOURCE_SETTINGS),
            follow_redirects=True,
        )
        assert response.status_code == 200
        submission = ResearchFeedbackSubmission.query.filter_by(user_id=user.id).one()
        assert submission.free_text is None
        assert submission.classification is None

    def test_unlimited_http_submissions(self, logged_in_client, user):
        for _ in range(2):
            response = logged_in_client.post(
                "/research/checkin",
                data=_valid_payload(submission_source=SOURCE_SETTINGS),
                follow_redirects=True,
            )
            assert response.status_code == 200
            assert b"Thank you for helping improve Kwalitec" in response.data
        assert ResearchFeedbackSubmission.query.filter_by(user_id=user.id).count() == 2
