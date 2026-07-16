"""LXP-002 Study Session Experience regression tests.

Covers lifecycle, completion behaviour, no unintended estimate / Evidence
writes, and preservation of the Mission flow.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.extensions import db
from app.models.curriculum import Curriculum, Topic
from app.models.learning import StudyAttempt
from app.models.mission import Mission, MissionTask
from app.models.study_plan import StudyPlan, WeekPlan
from app.models.subject import Subject
from app.models.topic_progress import TopicProgress
from app.services.educational_evidence_authority import EducationalEvidenceAuthority
from app.services.mission_service import MissionService
from app.services.study_session_service import (
    COMPLETION_NO,
    COMPLETION_PARTIAL,
    COMPLETION_YES,
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
    status: str = "Pending",
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
class TestStudySessionLifecycle:
    """Mission → Start → Session → Finish → Recorded."""

    def test_start_session_moves_pending_to_in_progress(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Equations of Value"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )

        updated = StudySessionService.start_session(mission.id, user.id)
        assert updated.status == "In Progress"

    def test_mission_landing_shows_start_cta(self, logged_in_client, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Equations of Value"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        _make_mission_for_topic(user.id, topic=topics[0], study_plan_id=plan.id)

        response = logged_in_client.get("/missions/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Start Study Session" in body
        assert "What success looks like today" in body
        assert "Read today" in body and "topic" in body
        assert "Mark Session Complete" not in body

    def test_full_http_lifecycle_yes_completion(
        self, logged_in_client, db, user
    ):
        """LXP-002 start/session still works; Finish now opens LXP-003 capture."""
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A", "Topic B"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )
        prior = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            mastery_score=18.0,
            confidence="Low",
            current_stage=TopicProgress.STAGE_LEARNING,
        )
        db.session.add(prior)
        db.session.commit()
        prior_completed = prior.completed

        start = logged_in_client.post(
            f"/missions/{mission.id}/session/start",
            follow_redirects=False,
        )
        assert start.status_code == 302
        assert f"/missions/{mission.id}/session" in start.headers["Location"]

        session_page = logged_in_client.get(f"/missions/{mission.id}/session")
        assert session_page.status_code == 200
        session_body = session_page.get_data(as_text=True)
        assert "Finish Study Session" in session_body
        assert "Learning objective" in session_body
        assert "Attempt practice questions" in session_body

        finish_get = logged_in_client.get(f"/missions/{mission.id}/session/finish")
        assert finish_get.status_code == 200
        finish_body = finish_get.get_data(as_text=True)
        assert "Practice Outcome Capture" in finish_body
        assert "questions_attempted" in finish_body
        assert "Record Study Session" in finish_body

        # Completion-only review remains available at service layer (unit tests).
        result = StudySessionService.finish_session(
            mission.id,
            user.id,
            COMPLETION_YES,
            notes="Worked Core Reading examples",
            topic_id=topics[0].id,
        )
        assert result.mission_completed is True

        db.session.refresh(mission)
        assert mission.status == "Completed"

        attempt = StudyAttempt.query.filter_by(
            user_id=user.id, mission_id=mission.id
        ).one()
        assert attempt.questions_attempted is None
        assert attempt.questions_correct is None
        assert attempt.confidence_after is None
        assert "Session completion: Yes" in (attempt.notes or "")
        has_results = (
            EducationalEvidenceAuthority.study_attempt_has_structured_question_results
        )
        assert not has_results(attempt)

        db.session.refresh(prior)
        assert prior.completed is prior_completed
        assert prior.mastery_score == 18.0


@pytest.mark.usefixtures("ctx")
class TestStudySessionCompletionBehaviour:
    def test_partial_completes_mission_without_study_progress(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A", "Topic B"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id, status="In Progress"
        )
        db.session.add(
            TopicProgress(
                user_id=user.id,
                topic_id=topics[0].id,
                completed=False,
                mastery_score=5.0,
                current_stage=TopicProgress.STAGE_LEARNING,
            )
        )
        db.session.commit()

        applied = {"called": False}

        def _apply() -> None:
            applied["called"] = True

        result = StudySessionService.finish_session(
            mission.id,
            user.id,
            COMPLETION_PARTIAL,
            notes="Only half the chapter",
            topic_id=topics[0].id,
            apply_study_progress=_apply,
        )

        assert result.mission_completed is True
        assert result.study_progress_updated is False
        assert applied["called"] is False
        db.session.refresh(mission)
        assert mission.status == "Completed"
        progress = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert progress.completed is False

    def test_no_keeps_mission_open(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id, status="In Progress"
        )

        result = StudySessionService.finish_session(
            mission.id,
            user.id,
            COMPLETION_NO,
            notes="Could not study today",
            topic_id=topics[0].id,
        )

        assert result.mission_completed is False
        assert result.study_progress_updated is False
        db.session.refresh(mission)
        assert mission.status == "In Progress"
        assert not any(task.completed for task in mission.tasks)

    def test_finish_rejects_already_completed(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id, status="In Progress"
        )
        for task in mission.tasks:
            task.completed = True
        db.session.commit()
        MissionService.complete_mission(mission.id, user.id)

        with pytest.raises(ValueError, match="already been recorded"):
            StudySessionService.finish_session(
                mission.id, user.id, COMPLETION_YES, topic_id=topics[0].id
            )


@pytest.mark.usefixtures("ctx")
class TestNoUnintendedEstimateOrEvidenceWrites:
    def test_yes_completion_does_not_write_estimates_or_evidence(self, db, user):
        """LXP-002 finish_session without scores leaves estimates unchanged."""
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A", "Topic B"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id, status="In Progress"
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            mastery_score=22.5,
            confidence="Medium",
            current_stage=TopicProgress.STAGE_LEARNING,
            average_accuracy=None,
        )
        db.session.add(progress)
        db.session.commit()
        prior_score = progress.mastery_score
        prior_confidence = progress.confidence

        StudySessionService.finish_session(
            mission.id,
            user.id,
            COMPLETION_YES,
            notes="",
            topic_id=topics[0].id,
        )

        db.session.refresh(progress)
        assert progress.completed is False
        assert progress.mastery_score == prior_score
        assert progress.confidence == prior_confidence
        assert progress.average_accuracy is None
        assert progress.has_estimated_knowledge is False

        attempt = StudyAttempt.query.filter_by(mission_id=mission.id).one()
        assert attempt.questions_attempted is None
        assert attempt.questions_correct is None
        assert attempt.confidence_before is None
        assert attempt.confidence_after is None
        assert (
            EducationalEvidenceAuthority.has_authorised_evidence_for_estimates(
                [attempt]
            )
            is False
        )


@pytest.mark.usefixtures("ctx")
class TestMissionFlowPreserved:
    def test_legacy_complete_endpoint_delegates_to_session_finish(
        self, app, ctx, user
    ):
        """PTP-002: legacy complete no longer writes state; it delegates."""
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id, status="In Progress"
        )
        for task in mission.tasks:
            task.completed = True
        db.session.commit()

        client = app.test_client()
        with client.session_transaction() as sess:
            sess["_user_id"] = str(user.id)
            sess["_fresh"] = True

        resp = client.post(
            f"/missions/{mission.id}/complete",
            json={},
            headers={"Content-Type": "application/json"},
        )
        assert resp.status_code == 200
        payload = resp.get_json()
        assert payload["success"] is True
        assert payload.get("delegated") is True
        assert f"/missions/{mission.id}/session/finish" in payload["redirect_url"]
        db.session.refresh(mission)
        assert mission.status == "In Progress"

    def test_other_user_cannot_open_session(self, logged_in_client, db, user):
        from app.models.user import User

        other = User(email="other@kwalitec.example", is_active_user=True)
        other.set_password("password123")
        db.session.add(other)
        db.session.flush()
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(other.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            other.id, topic=topics[0], study_plan_id=plan.id
        )

        response = logged_in_client.get(
            f"/missions/{mission.id}/session", follow_redirects=True
        )
        assert response.status_code == 200
        assert (
            b"own study sessions" in response.data
            or b"Today's Study Session" in response.data
        )
