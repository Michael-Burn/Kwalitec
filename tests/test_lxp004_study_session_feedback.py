"""LXP-004 Study Session Feedback & Educational Explainability regression tests.

Covers practice / no-practice / partial / abandoned paths, truthfulness,
forbidden unsupported claims, and student-safe educational wording.
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
from app.services.educational_explainability_service import (
    EducationalExplainabilityService,
)
from app.services.study_session_service import (
    COMPLETION_NO,
    COMPLETION_PARTIAL,
    FEEDBACK_ABANDONED,
    FEEDBACK_NO_PRACTICE,
    FEEDBACK_PARTIAL,
    FEEDBACK_PRACTICE_RECORDED,
    StudySessionService,
)

FORBIDDEN_UNSUPPORTED_CLAIMS = (
    "knowledge increased",
    "mastery increased",
    "readiness improved",
    "your knowledge",
    "your mastery",
)

FORBIDDEN_ENGINEERING_TERMS = (
    "digital twin",
    "educational intelligence",
    "inference",
    "confidence score",
    "mastery calculation",
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


def _narrative_text(narrative) -> str:
    parts = (
        list(narrative.what_happened)
        + list(narrative.what_observed)
        + list(narrative.honest_conclusions)
        + [narrative.what_next]
    )
    return " ".join(parts).lower()


@pytest.mark.usefixtures("ctx")
class TestStudySessionFeedbackScenarios:
    def test_practice_recorded_narrative(self, db, user):
        narrative = EducationalExplainabilityService.build_study_session_feedback(
            topic_title="Topic 4.2",
            scenario=FEEDBACK_PRACTICE_RECORDED,
            questions_attempted=20,
            questions_correct=15,
            duration_minutes=30,
        )

        assert narrative.scenario == FEEDBACK_PRACTICE_RECORDED
        assert "You completed today's study session." in narrative.what_happened
        assert "Topic 4.2" in narrative.what_happened[1]
        assert "20 practice questions" in narrative.what_happened[2]
        assert "15 correctly" in narrative.what_happened[3]
        assert "Practice outcomes have been recorded." in narrative.honest_conclusions
        assert "Tomorrow's mission" in narrative.what_next

    def test_no_practice_narrative(self):
        narrative = EducationalExplainabilityService.build_study_session_feedback(
            topic_title="Topic 4.2",
            scenario=FEEDBACK_NO_PRACTICE,
        )

        assert narrative.scenario == FEEDBACK_NO_PRACTICE
        assert "No practice questions were recorded today." in narrative.what_happened
        assert "cannot yet update" in narrative.honest_conclusions[0].lower()

    def test_partial_session_narrative(self):
        narrative = EducationalExplainabilityService.build_study_session_feedback(
            topic_title="Topic 4.2",
            scenario=FEEDBACK_PARTIAL,
            study_progress_updated=False,
        )

        assert narrative.scenario == FEEDBACK_PARTIAL
        assert "partially completed" in narrative.what_happened[0].lower()
        assert "study progress was not advanced" in _narrative_text(narrative)

    def test_abandoned_session_narrative(self):
        narrative = EducationalExplainabilityService.build_study_session_feedback(
            topic_title="Topic 4.2",
            scenario=FEEDBACK_ABANDONED,
            mission_status="In Progress",
        )

        assert narrative.scenario == FEEDBACK_ABANDONED
        assert "was not completed" in narrative.what_happened[0].lower()
        assert "remains open" in _narrative_text(narrative)

    def test_resolve_scenario_from_persisted_state(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic 4.2"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )

        result = StudySessionService.record_practice_outcome(
            mission.id,
            user.id,
            questions_attempted=20,
            questions_correct=15,
            topic_id=topics[0].id,
        )
        db.session.refresh(mission)

        scenario = StudySessionService.resolve_feedback_scenario(
            mission, result.study_attempt
        )
        assert scenario == FEEDBACK_PRACTICE_RECORDED

    def test_resolve_partial_from_finish_session(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )

        finish = StudySessionService.finish_session(
            mission.id,
            user.id,
            COMPLETION_PARTIAL,
            topic_id=topics[0].id,
        )
        attempt = StudyAttempt.query.filter_by(mission_id=mission.id).one()
        scenario = StudySessionService.resolve_feedback_scenario(
            finish.mission, attempt
        )
        assert scenario == FEEDBACK_PARTIAL

    def test_resolve_abandoned_from_finish_session_no(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic A"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )

        finish = StudySessionService.finish_session(
            mission.id,
            user.id,
            COMPLETION_NO,
            topic_id=topics[0].id,
        )
        attempt = StudyAttempt.query.filter_by(mission_id=mission.id).one()
        scenario = StudySessionService.resolve_feedback_scenario(
            finish.mission, attempt
        )
        assert scenario == FEEDBACK_ABANDONED


@pytest.mark.usefixtures("ctx")
class TestStudySessionFeedbackTruthfulness:
    @pytest.mark.parametrize(
        "scenario,kwargs",
        [
            (
                FEEDBACK_PRACTICE_RECORDED,
                {
                    "questions_attempted": 10,
                    "questions_correct": 8,
                },
            ),
            (FEEDBACK_NO_PRACTICE, {}),
            (FEEDBACK_PARTIAL, {"study_progress_updated": False}),
            (FEEDBACK_ABANDONED, {"mission_status": "In Progress"}),
        ],
    )
    def test_no_unsupported_claims(self, scenario, kwargs):
        narrative = EducationalExplainabilityService.build_study_session_feedback(
            topic_title="Topic 4.2",
            scenario=scenario,
            **kwargs,
        )
        text = _narrative_text(narrative)
        for forbidden in FORBIDDEN_UNSUPPORTED_CLAIMS:
            assert forbidden not in text

    @pytest.mark.parametrize(
        "scenario,kwargs",
        [
            (
                FEEDBACK_PRACTICE_RECORDED,
                {
                    "questions_attempted": 5,
                    "questions_correct": 4,
                },
            ),
            (FEEDBACK_NO_PRACTICE, {}),
            (FEEDBACK_PARTIAL, {}),
            (FEEDBACK_ABANDONED, {"mission_status": "In Progress"}),
        ],
    )
    def test_no_engineering_jargon(self, scenario, kwargs):
        narrative = EducationalExplainabilityService.build_study_session_feedback(
            topic_title="Topic 4.2",
            scenario=scenario,
            **kwargs,
        )
        text = _narrative_text(narrative)
        for term in FORBIDDEN_ENGINEERING_TERMS:
            assert term not in text


@pytest.mark.usefixtures("ctx")
class TestStudySessionFeedbackHttpFlow:
    def test_practice_path_shows_four_question_feedback(
        self, logged_in_client, db, user
    ):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic 4.2"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )

        response = logged_in_client.post(
            f"/missions/{mission.id}/session/finish",
            data={
                "questions_attempted": "20",
                "questions_correct": "15",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Study Session Feedback" in body
        assert "What happened today?" in body
        assert "What did Kwalitec observe?" in body
        assert "What can Kwalitec honestly conclude?" in body
        assert "What happens next?" in body
        assert "20 practice questions" in body
        assert "15 correctly" in body
        assert "Practice outcomes have been recorded." in body
        assert 'data-lxp004-feedback="practice_recorded"' in body

        for forbidden in FORBIDDEN_UNSUPPORTED_CLAIMS + FORBIDDEN_ENGINEERING_TERMS:
            assert forbidden not in body.lower()

    def test_no_practice_skip_shows_honest_feedback(
        self, logged_in_client, db, user
    ):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic 4.2"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )

        response = logged_in_client.post(
            f"/missions/{mission.id}/session/finish",
            data={"skip_practice": "1"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Study Session Feedback" in body
        assert "No practice questions were recorded today." in body
        assert "cannot yet update" in body.lower()
        assert 'data-lxp004-feedback="no_practice"' in body

        db.session.refresh(mission)
        assert mission.status == "Completed"

    def test_completed_mission_feedback_from_recorded_route(
        self, logged_in_client, db, user
    ):
        curriculum, topics = _make_curriculum("IFoA CM1", ["Topic 4.2"])
        plan = _make_active_plan(user.id, exam_name="IFoA CM1", curriculum=curriculum)
        mission = _make_mission_for_topic(
            user.id,
            topic=topics[0],
            study_plan_id=plan.id,
            status="Completed",
        )
        db.session.add(
            StudyAttempt(
                user_id=user.id,
                mission_id=mission.id,
                topic_id=topics[0].id,
                study_date=date.today(),
                questions_attempted=6,
                questions_correct=5,
            )
        )
        db.session.commit()

        response = logged_in_client.get(
            f"/missions/{mission.id}/session/recorded",
        )
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Study Session Feedback" in body
        assert "6 practice questions" in body
