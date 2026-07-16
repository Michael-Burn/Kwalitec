"""LXP-003 Practice Outcome Capture regression tests.

Covers valid / invalid submissions, boundary values, StudyAttempt creation,
Evidence Authority invocation, and no unintended Study Progress / readiness /
recommendation mutations.
"""

from __future__ import annotations

from datetime import date, timedelta
from unittest.mock import patch

import pytest

from app.extensions import db
from app.models.curriculum import Curriculum, Topic
from app.models.learning import StudyAttempt
from app.models.mission import Mission, MissionTask
from app.models.study_plan import StudyPlan, WeekPlan
from app.models.subject import Subject
from app.models.topic_progress import TopicProgress
from app.services.educational_evidence_authority import EducationalEvidenceAuthority
from app.services.study_session_service import (
    PRACTICE_OUTCOME_SUCCESS_MESSAGE,
    StudySessionService,
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
    user_id: int,
    *,
    exam_name: str,
    curriculum: Curriculum,
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


def _make_mission_for_topic(
    user_id: int,
    *,
    topic: Topic,
    study_plan_id: int | None = None,
    status: str = "In Progress",
) -> Mission:
    subject = Subject(user_id=user_id, name="Exam Paper")
    db.session.add(subject)
    db.session.flush()
    mission = Mission(
        user_id=user_id,
        subject_id=subject.id,
        study_plan_id=study_plan_id,
        mission_date=date.today(),
        title=f"Study {topic.name}",
        status=status,
    )
    mission.tasks.append(MissionTask(title="Focus study", order=0, completed=False))
    mission.tasks.append(MissionTask(title="Practice", order=1, completed=False))
    db.session.add(mission)
    db.session.commit()
    return mission


@pytest.mark.usefixtures("ctx")
class TestPracticeOutcomeValidation:
    def test_valid_submission_service(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Equations of Value"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )

        result = StudySessionService.record_practice_outcome(
            mission.id,
            user.id,
            questions_attempted=10,
            questions_correct=7,
            duration_minutes=25,
            notes="ActEd Q&A pack",
            topic_id=topics[0].id,
        )

        assert result.mission_completed is True
        assert result.authorised_evidence is True
        assert result.study_attempt.questions_attempted == 10
        assert result.study_attempt.questions_correct == 7
        assert result.study_attempt.duration_minutes == 25
        assert result.study_attempt.notes == "ActEd Q&A pack"
        db.session.refresh(mission)
        assert mission.status == "Completed"

    def test_zero_attempted_rejected(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )

        with pytest.raises(ValueError, match="greater than zero"):
            StudySessionService.record_practice_outcome(
                mission.id,
                user.id,
                questions_attempted=0,
                questions_correct=0,
                topic_id=topics[0].id,
            )

        db.session.refresh(mission)
        assert mission.status == "In Progress"
        assert StudyAttempt.query.filter_by(mission_id=mission.id).count() == 0

    def test_correct_greater_than_attempted_rejected(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )

        with pytest.raises(ValueError, match="cannot exceed"):
            StudySessionService.record_practice_outcome(
                mission.id,
                user.id,
                questions_attempted=5,
                questions_correct=6,
                topic_id=topics[0].id,
            )

        db.session.refresh(mission)
        assert mission.status == "In Progress"

    def test_negative_correct_rejected(self, db, user):
        with pytest.raises(ValueError, match="zero or greater"):
            StudySessionService.validate_practice_outcome(5, -1)

    def test_boundary_all_correct(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )

        result = StudySessionService.record_practice_outcome(
            mission.id,
            user.id,
            questions_attempted=1,
            questions_correct=1,
            topic_id=topics[0].id,
        )
        assert result.study_attempt.questions_attempted == 1
        assert result.study_attempt.questions_correct == 1
        assert result.authorised_evidence is True

    def test_boundary_zero_correct(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )

        result = StudySessionService.record_practice_outcome(
            mission.id,
            user.id,
            questions_attempted=8,
            questions_correct=0,
            topic_id=topics[0].id,
        )
        assert result.study_attempt.questions_correct == 0
        assert result.authorised_evidence is True
        assert result.study_attempt.get_accuracy_percentage() == 0.0


@pytest.mark.usefixtures("ctx")
class TestStudyAttemptAndEvidenceAuthority:
    def test_creates_study_attempt_with_structured_results(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )

        StudySessionService.record_practice_outcome(
            mission.id,
            user.id,
            questions_attempted=12,
            questions_correct=9,
            topic_id=topics[0].id,
        )

        attempt = StudyAttempt.query.filter_by(
            user_id=user.id, mission_id=mission.id
        ).one()
        assert attempt.topic_id == topics[0].id
        assert attempt.confidence_before is None
        assert attempt.confidence_after is None
        has_results = (
            EducationalEvidenceAuthority.study_attempt_has_structured_question_results
        )
        assert has_results(attempt) is True
        assert (
            EducationalEvidenceAuthority.has_authorised_evidence_for_estimates([attempt])
            is True
        )

    def test_updates_existing_scoreless_attempt(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )
        existing = StudyAttempt(
            user_id=user.id,
            mission_id=mission.id,
            topic_id=topics[0].id,
            study_date=date.today(),
            notes="Session completion: Yes",
        )
        db.session.add(existing)
        db.session.commit()
        existing_id = existing.id

        result = StudySessionService.record_practice_outcome(
            mission.id,
            user.id,
            questions_attempted=4,
            questions_correct=3,
            topic_id=topics[0].id,
        )

        assert result.study_attempt.id == existing_id
        assert StudyAttempt.query.filter_by(mission_id=mission.id).count() == 1
        db.session.refresh(existing)
        assert existing.questions_attempted == 4
        assert existing.questions_correct == 3

    def test_invokes_mastery_update_via_evidence_path(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )

        with patch(
            "app.services.adaptive_learning_service.AdaptiveLearningService"
            ".update_mastery_after_attempt"
        ) as mock_update:
            StudySessionService.record_practice_outcome(
                mission.id,
                user.id,
                questions_attempted=10,
                questions_correct=8,
                topic_id=topics[0].id,
            )
            mock_update.assert_called_once_with(
                user_id=user.id,
                topic_id=topics[0].id,
            )

    def test_lawful_estimated_knowledge_may_update(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            mastery_score=0.0,
            confidence="Not Started",
            current_stage=TopicProgress.STAGE_LEARNING,
            average_accuracy=None,
        )
        db.session.add(progress)
        db.session.commit()

        StudySessionService.record_practice_outcome(
            mission.id,
            user.id,
            questions_attempted=10,
            questions_correct=9,
            topic_id=topics[0].id,
        )

        db.session.refresh(progress)
        assert progress.has_estimated_knowledge is True
        assert progress.mastery_score > 0.0
        assert progress.average_accuracy is not None
        # Study Progress coverage flag must not be written by LXP-003.
        assert progress.completed is False


@pytest.mark.usefixtures("ctx")
class TestNoUnintendedStateMutations:
    def test_does_not_write_study_progress(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A", "Topic B"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            mastery_score=12.0,
            current_stage=TopicProgress.STAGE_LEARNING,
        )
        db.session.add(progress)
        db.session.commit()

        StudySessionService.record_practice_outcome(
            mission.id,
            user.id,
            questions_attempted=5,
            questions_correct=4,
            topic_id=topics[0].id,
        )

        db.session.refresh(progress)
        assert progress.completed is False

    def test_does_not_call_recommendation_or_readiness_services(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )

        with (
            patch(
                "app.services.recommendation_service.RecommendationService"
                ".get_recommendations",
                create=True,
            ) as mock_rec,
            patch(
                "app.services.readiness_service.ReadinessService"
                ".calculate_readiness",
                create=True,
            ) as mock_ready,
        ):
            StudySessionService.record_practice_outcome(
                mission.id,
                user.id,
                questions_attempted=6,
                questions_correct=5,
                topic_id=topics[0].id,
            )
            mock_rec.assert_not_called()
            mock_ready.assert_not_called()

    def test_rejects_already_completed_mission(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id,
            topic=topics[0],
            study_plan_id=plan.id,
            status="Completed",
        )

        with pytest.raises(ValueError, match="already been recorded"):
            StudySessionService.record_practice_outcome(
                mission.id,
                user.id,
                questions_attempted=3,
                questions_correct=2,
                topic_id=topics[0].id,
            )


@pytest.mark.usefixtures("ctx")
class TestPracticeOutcomeHttpFlow:
    def test_finish_get_shows_practice_form(self, logged_in_client, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )

        response = logged_in_client.get(f"/missions/{mission.id}/session/finish")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Practice Outcome Capture" in body
        assert "Questions Attempted" in body
        assert "Questions Correct" in body
        assert "Record Study Session" in body
        assert "completion_status" not in body
        assert "Confidence" not in body
        assert "Mastery" not in body
        assert "Readiness" not in body

    def test_valid_http_submission(self, logged_in_client, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A", "Topic B"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            mastery_score=0.0,
            current_stage=TopicProgress.STAGE_LEARNING,
        )
        db.session.add(progress)
        db.session.commit()

        response = logged_in_client.post(
            f"/missions/{mission.id}/session/finish",
            data={
                "questions_attempted": "10",
                "questions_correct": "8",
                "duration_minutes": "30",
                "notes": "Worked Q1–Q10",
            },
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert "session/recorded" in response.headers["Location"]

        recorded = logged_in_client.get(response.headers["Location"])
        assert recorded.status_code == 200
        body = recorded.get_data(as_text=True)
        assert "Your practice results have been recorded" in body
        assert PRACTICE_OUTCOME_SUCCESS_MESSAGE.split(".")[0] in body

        db.session.refresh(mission)
        assert mission.status == "Completed"
        attempt = StudyAttempt.query.filter_by(mission_id=mission.id).one()
        assert attempt.questions_attempted == 10
        assert attempt.questions_correct == 8
        assert attempt.duration_minutes == 30

        db.session.refresh(progress)
        assert progress.completed is False
        assert progress.has_estimated_knowledge is True

    def test_http_rejects_zero_attempted(self, logged_in_client, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )

        response = logged_in_client.post(
            f"/missions/{mission.id}/session/finish",
            data={
                "questions_attempted": "0",
                "questions_correct": "0",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "greater than zero" in body.lower() or "Practice Outcome" in body
        db.session.refresh(mission)
        assert mission.status == "In Progress"
        assert StudyAttempt.query.filter_by(mission_id=mission.id).count() == 0

    def test_http_rejects_correct_exceeds_attempted(
        self, logged_in_client, db, user
    ):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )

        response = logged_in_client.post(
            f"/missions/{mission.id}/session/finish",
            data={
                "questions_attempted": "5",
                "questions_correct": "9",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "cannot exceed" in body.lower()
        db.session.refresh(mission)
        assert mission.status == "In Progress"

    def test_full_lifecycle_finish_to_practice(self, logged_in_client, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id,
            topic=topics[0],
            study_plan_id=plan.id,
            status="Pending",
        )

        start = logged_in_client.post(
            f"/missions/{mission.id}/session/start",
            follow_redirects=False,
        )
        assert start.status_code == 302

        session_page = logged_in_client.get(f"/missions/{mission.id}/session")
        assert session_page.status_code == 200
        assert b"Finish Study Session" in session_page.data

        finish_get = logged_in_client.get(f"/missions/{mission.id}/session/finish")
        assert b"Practice Outcome Capture" in finish_get.data

        finish_post = logged_in_client.post(
            f"/missions/{mission.id}/session/finish",
            data={
                "questions_attempted": "6",
                "questions_correct": "5",
            },
            follow_redirects=False,
        )
        assert finish_post.status_code == 302
        assert "practice=1" in finish_post.headers["Location"]
