"""PTP-002 Single Source of Truth regression tests.

Covers one authoritative student workflow, legacy redirect/delegate behaviour,
no duplicate educational state updates from retired paths, and no LXP
behavioural regressions on the Study Session path.
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
from app.services.study_session_service import StudySessionService


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


def _make_active_plan(user_id: int, *, exam_name: str, curriculum: Curriculum):
    plan = StudyPlan(
        user_id=user_id,
        exam_name=exam_name,
        exam_sitting="Apr 2027",
        exam_date=date.today() + timedelta(days=90),
        target_grade="Pass",
        weekday_study_minutes=60,
        weekend_study_minutes=90,
        current_stage="Learning",
        study_preference="Mixed",
        preferred_session_minutes=45,
        active=True,
        curriculum_id=curriculum.id,
        curriculum_version=curriculum.version,
        curriculum_topic_code=None,
    )
    db.session.add(plan)
    db.session.flush()
    db.session.add(
        WeekPlan(
            study_plan_id=plan.id,
            week_number=1,
            start_date=date.today() - timedelta(days=2),
            end_date=date.today() + timedelta(days=4),
        )
    )
    db.session.commit()
    return plan


def _make_mission_for_topic(
    user_id: int,
    *,
    topic: Topic,
    study_plan_id: int | None = None,
    status: str = "Pending",
) -> Mission:
    subject = Subject(user_id=user_id, name=topic.name[:40] or "Subject")
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


def _login(client, user):
    with client.session_transaction() as sess:
        sess["_user_id"] = str(user.id)
        sess["_fresh"] = True


@pytest.mark.usefixtures("ctx")
class TestAuthoritativeSingleWorkflow:
    def test_daily_mission_cta_is_study_session_only(
        self, logged_in_client, db, user
    ):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        _make_mission_for_topic(user.id, topic=topics[0], study_plan_id=plan.id)

        response = logged_in_client.get("/missions/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Start Study Session" in body
        assert "Reflect on Your Learning" not in body
        assert "Mark Session Complete" not in body
        assert "/missions/" in body

    def test_full_closure_records_one_attempt(
        self, logged_in_client, db, user
    ):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )

        logged_in_client.post(f"/missions/{mission.id}/session/start")
        finish_get = logged_in_client.get(f"/missions/{mission.id}/session/finish")
        assert finish_get.status_code == 200
        assert b"Practice Outcome Capture" in finish_get.data

        finish_post = logged_in_client.post(
            f"/missions/{mission.id}/session/finish",
            data={
                "questions_attempted": 10,
                "questions_correct": 7,
                "duration_minutes": 25,
                "notes": "Past paper set A",
            },
            follow_redirects=False,
        )
        assert finish_post.status_code == 302
        assert f"/missions/{mission.id}/session/recorded" in finish_post.headers[
            "Location"
        ]

        db.session.refresh(mission)
        assert mission.status == "Completed"
        attempts = StudyAttempt.query.filter_by(
            user_id=user.id, mission_id=mission.id
        ).all()
        assert len(attempts) == 1
        assert attempts[0].questions_attempted == 10
        assert attempts[0].questions_correct == 7

        feedback = logged_in_client.get(f"/missions/{mission.id}/session/recorded")
        assert feedback.status_code == 200
        body = feedback.data
        assert b"Study Session Feedback" in body or b"What happened" in body


@pytest.mark.usefixtures("ctx")
class TestLegacyRedirectBehaviour:
    def test_legacy_complete_json_delegates_without_writing_state(
        self, app, ctx, user
    ):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id,
            topic=topics[0],
            study_plan_id=plan.id,
            status="In Progress",
        )
        for task in mission.tasks:
            task.completed = True
        db.session.commit()

        client = app.test_client()
        _login(client, user)
        resp = client.post(
            f"/missions/{mission.id}/complete",
            json={},
            headers={"Content-Type": "application/json"},
        )
        assert resp.status_code == 200
        payload = resp.get_json()
        assert payload["success"] is True
        assert payload["delegated"] is True
        assert f"/missions/{mission.id}/session/finish" in payload["redirect_url"]

        db.session.refresh(mission)
        assert mission.status == "In Progress"
        assert (
            StudyAttempt.query.filter_by(
                user_id=user.id, mission_id=mission.id
            ).count()
            == 0
        )

    def test_legacy_complete_html_redirects_to_finish(
        self, logged_in_client, db, user
    ):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id, status="In Progress"
        )

        resp = logged_in_client.post(
            f"/missions/{mission.id}/complete",
            follow_redirects=False,
        )
        assert resp.status_code == 302
        assert f"/missions/{mission.id}/session/finish" in resp.headers["Location"]
        db.session.refresh(mission)
        assert mission.status == "In Progress"

    def test_legacy_review_get_redirects_open_mission_to_finish(
        self, logged_in_client, db, user
    ):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id, status="In Progress"
        )

        resp = logged_in_client.get(
            f"/missions/review/{mission.id}", follow_redirects=False
        )
        assert resp.status_code == 302
        assert f"/missions/{mission.id}/session/finish" in resp.headers["Location"]

    def test_legacy_review_get_redirects_completed_to_feedback(
        self, logged_in_client, db, user
    ):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id, status="In Progress"
        )
        StudySessionService.record_practice_outcome(
            mission_id=mission.id,
            user_id=user.id,
            questions_attempted=5,
            questions_correct=4,
            topic_id=topics[0].id,
        )
        db.session.refresh(mission)
        assert mission.status == "Completed"

        resp = logged_in_client.get(
            f"/missions/review/{mission.id}", follow_redirects=False
        )
        assert resp.status_code == 302
        assert f"/missions/{mission.id}/session/recorded" in resp.headers["Location"]

    def test_legacy_review_post_does_not_create_attempt(
        self, logged_in_client, db, user
    ):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id, status="In Progress"
        )

        resp = logged_in_client.post(
            f"/missions/review/{mission.id}",
            data={
                "duration_minutes": 40,
                "questions_attempted": 8,
                "questions_correct": 6,
                "confidence_before": "Low",
                "confidence_after": "High",
                "notes": "Should be ignored",
            },
            follow_redirects=False,
        )
        assert resp.status_code == 302
        assert f"/missions/{mission.id}/session/finish" in resp.headers["Location"]
        assert (
            StudyAttempt.query.filter_by(
                user_id=user.id, mission_id=mission.id
            ).count()
            == 0
        )
        db.session.refresh(mission)
        assert mission.status == "In Progress"


@pytest.mark.usefixtures("ctx")
class TestNoDuplicateEducationalState:
    def test_legacy_complete_after_practice_does_not_add_attempt(
        self, app, ctx, user
    ):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id, status="In Progress"
        )
        StudySessionService.record_practice_outcome(
            mission_id=mission.id,
            user_id=user.id,
            questions_attempted=6,
            questions_correct=5,
            topic_id=topics[0].id,
        )
        assert (
            StudyAttempt.query.filter_by(
                user_id=user.id, mission_id=mission.id
            ).count()
            == 1
        )

        client = app.test_client()
        _login(client, user)
        resp = client.post(
            f"/missions/{mission.id}/complete",
            json={},
            headers={"Content-Type": "application/json"},
        )
        assert resp.status_code == 200
        payload = resp.get_json()
        assert payload["delegated"] is True
        assert f"/missions/{mission.id}/session/recorded" in payload["redirect_url"]
        assert (
            StudyAttempt.query.filter_by(
                user_id=user.id, mission_id=mission.id
            ).count()
            == 1
        )

    def test_second_practice_submit_rejected(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id, status="In Progress"
        )
        StudySessionService.record_practice_outcome(
            mission_id=mission.id,
            user_id=user.id,
            questions_attempted=6,
            questions_correct=5,
            topic_id=topics[0].id,
        )
        with pytest.raises(ValueError, match="already been recorded"):
            StudySessionService.record_practice_outcome(
                mission_id=mission.id,
                user_id=user.id,
                questions_attempted=10,
                questions_correct=10,
                topic_id=topics[0].id,
            )
        assert (
            StudyAttempt.query.filter_by(
                user_id=user.id, mission_id=mission.id
            ).count()
            == 1
        )


@pytest.mark.usefixtures("ctx")
class TestNoBehaviouralRegressions:
    def test_practice_capture_still_works(self, logged_in_client, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )
        logged_in_client.post(f"/missions/{mission.id}/session/start")
        page = logged_in_client.get(f"/missions/{mission.id}/session/finish")
        assert page.status_code == 200
        body = page.get_data(as_text=True)
        assert "Questions Attempted" in body
        assert "I didn" in body and "practise" in body.lower()

    def test_skip_practice_still_closes_session(self, logged_in_client, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )
        logged_in_client.post(f"/missions/{mission.id}/session/start")
        resp = logged_in_client.post(
            f"/missions/{mission.id}/session/finish",
            data={"skip_practice": "1"},
            follow_redirects=False,
        )
        assert resp.status_code == 302
        assert f"/missions/{mission.id}/session/recorded" in resp.headers["Location"]
        db.session.refresh(mission)
        assert mission.status == "Completed"
