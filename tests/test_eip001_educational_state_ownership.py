"""EIP-001 Educational State Ownership & Authority regression tests.

Negative tests prove Forbidden Writers never mutate owned states.
Positive tests prove Permitted Writers still update their authorised states.

Governing refs:
- Constitution Articles III, IV, V, VIII
- EL-001, EL-002, EL-003, EL-005, EL-006, EL-007, EL-009
- EDUCATIONAL_STATE_AUTHORITY_MATRIX.md
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.extensions import db
from app.mission.routes import _apply_mission_topic_progress
from app.models.curriculum import Curriculum, Topic
from app.models.mission import Mission, MissionTask
from app.models.study_plan import StudyPlan, WeekPlan
from app.models.subject import Subject
from app.models.topic_progress import TopicProgress
from app.services.adaptive_learning_service import AdaptiveLearningService
from app.services.learning_service import LearningService
from app.services.planning_service import PlanningService
from app.services.recommendation_service import RecommendationService


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
    topic_code: str | None = None,
) -> StudyPlan:
    plan = StudyPlan(
        user_id=user_id,
        curriculum_id=curriculum.id,
        curriculum_version=curriculum.version,
        exam_name=exam_name,
        exam_sitting="April 2027",
        exam_date=date.today() + timedelta(days=180),
        weekday_study_minutes=120,
        weekend_study_minutes=180,
        current_stage="Chapter 1",
        study_preference="Mixed",
        target_grade="A",
        preferred_session_minutes=60,
        active=True,
        curriculum_topic_code=topic_code,
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


def _make_subject(user_id: int) -> Subject:
    subject = Subject(user_id=user_id, name="Study Plan", active=True)
    db.session.add(subject)
    db.session.flush()
    return subject


def _make_mission(user_id: int, *, study_plan_id: int, title: str) -> Mission:
    subject = _make_subject(user_id)
    mission = Mission(
        user_id=user_id,
        subject_id=subject.id,
        study_plan_id=study_plan_id,
        title=title,
        mission_date=date.today(),
        status="In Progress",
    )
    db.session.add(mission)
    db.session.flush()
    db.session.add(
        MissionTask(mission_id=mission.id, title="Study", order=0, completed=True)
    )
    db.session.commit()
    return mission


@pytest.mark.usefixtures("ctx")
class TestNegativeOwnershipRegressions:
    """Forbidden Writers must never mutate educational states they do not own."""

    def test_mission_completion_must_not_modify_estimated_mastery(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Ownership Topic A", "Ownership Topic B"]
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            mastery_score=18.0,
            average_accuracy=None,
            confidence="Low",
            current_stage=TopicProgress.STAGE_LEARNING,
            revision_count=1,
        )
        db.session.add(progress)
        db.session.commit()
        prior_mastery = progress.mastery_score

        mission = _make_mission(
            user.id,
            study_plan_id=plan.id,
            title=f"Study {topics[0].name}",
        )
        LearningService.create_study_attempt(
            user_id=user.id,
            mission_id=mission.id,
            topic_id=topics[0].id,
            study_date=date.today(),
        )
        _apply_mission_topic_progress(user.id, topics[0])

        updated = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert updated.mastery_score == prior_mastery
        assert updated.average_accuracy is None
        assert updated.has_estimated_mastery is False

    def test_mission_completion_must_not_modify_estimated_knowledge(self, db, user):
        """Product estimated-knowledge store is mastery_score until Twin separates."""
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Knowledge Topic A", "Knowledge Topic B"]
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            mastery_score=22.5,
            confidence="Medium",
            current_stage=TopicProgress.STAGE_LEARNING,
        )
        db.session.add(progress)
        db.session.commit()
        prior = progress.mastery_score

        mission = _make_mission(
            user.id,
            study_plan_id=plan.id,
            title=f"Study {topics[0].name}",
        )
        LearningService.create_study_attempt(
            user_id=user.id,
            mission_id=mission.id,
            topic_id=topics[0].id,
            study_date=date.today(),
        )
        _apply_mission_topic_progress(user.id, topics[0])

        updated = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert updated.mastery_score == prior

    def test_student_confidence_must_not_modify_estimated_mastery(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Confidence Topic"]
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            mastery_score=40.0,
            confidence="Low",
            current_stage=TopicProgress.STAGE_LEARNING,
            revision_count=2,
        )
        db.session.add(progress)
        db.session.commit()
        prior_mastery = progress.mastery_score

        mission = _make_mission(
            user.id,
            study_plan_id=plan.id,
            title=f"Study {topics[0].name}",
        )
        LearningService.create_study_attempt(
            user_id=user.id,
            mission_id=mission.id,
            topic_id=topics[0].id,
            study_date=date.today(),
            confidence_after="Mastered",
        )

        updated = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert updated.confidence == "Mastered"
        assert updated.mastery_score == prior_mastery

        # EIP-002: no authorised question results ⇒ correct silence.
        AdaptiveLearningService.update_mastery_after_attempt(
            user_id=user.id, topic_id=topics[0].id
        )
        after_recalc = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert after_recalc.mastery_score == prior_mastery
        assert after_recalc.average_accuracy is None

    def test_student_confidence_must_not_modify_study_progress(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Coverage Protected Topic"]
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            mastery_score=0.0,
            confidence="Not Started",
            current_stage=TopicProgress.STAGE_LEARNING,
        )
        db.session.add(progress)
        db.session.commit()

        mission = _make_mission(
            user.id,
            study_plan_id=plan.id,
            title=f"Study {topics[0].name}",
        )
        LearningService.create_study_attempt(
            user_id=user.id,
            mission_id=mission.id,
            topic_id=topics[0].id,
            study_date=date.today(),
            confidence_after="High",
        )

        updated = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert updated.confidence == "High"
        assert updated.completed is False
        assert updated.current_stage == TopicProgress.STAGE_LEARNING

    def test_study_progress_must_not_modify_educational_evidence(self, db, user):
        """Coverage writes must not fabricate attempt/assessment evidence rows."""
        from app.models.learning import StudyAttempt

        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Evidence Isolation Topic", "Next"]
        )
        _make_active_plan(user.id, exam_name="IFoA CS1", curriculum=curriculum)

        before_count = StudyAttempt.query.filter_by(user_id=user.id).count()
        _apply_mission_topic_progress(user.id, topics[0])
        after_count = StudyAttempt.query.filter_by(user_id=user.id).count()

        progress = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert progress.completed is True
        assert after_count == before_count
        assert progress.average_accuracy is None
        assert progress.has_estimated_mastery is False

    def test_recommendation_generation_must_not_modify_current_learning(
        self, db, user
    ):
        curriculum, topics = _make_curriculum(
            "IFoA CS1",
            ["Done Topic", "Current Learning Topic", "Future Topic"],
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum, topic_code="2"
        )
        db.session.add(
            TopicProgress(
                user_id=user.id,
                topic_id=topics[0].id,
                completed=True,
                current_stage=TopicProgress.STAGE_COMPLETED,
            )
        )
        db.session.add(
            TopicProgress(
                user_id=user.id,
                topic_id=topics[1].id,
                completed=False,
                current_stage=TopicProgress.STAGE_LEARNING,
                mastery_score=15.0,
                revision_count=1,
            )
        )
        db.session.commit()
        pointer_before = plan.curriculum_topic_code

        RecommendationService.generate_recommendations(user.id, limit=5)
        RecommendationService.generate_today_recommendation(user.id)

        db.session.refresh(plan)
        assert plan.curriculum_topic_code == pointer_before

    def test_recommendation_generation_must_not_modify_todays_mission(
        self, db, user
    ):
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Mission Anchor Topic", "Other Topic"]
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum
        )
        mission = _make_mission(
            user.id,
            study_plan_id=plan.id,
            title=f"Study {topics[0].name}",
        )
        mission_id = mission.id
        mission_title = mission.title
        mission_status = mission.status

        RecommendationService.generate_recommendations(user.id, limit=5)
        RecommendationService.generate_today_recommendation(user.id)

        unchanged = Mission.query.get(mission_id)
        assert unchanged is not None
        assert unchanged.title == mission_title
        assert unchanged.status == mission_status
        assert Mission.query.filter_by(
            user_id=user.id, mission_date=date.today()
        ).count() == 1

    def test_digital_twin_mastery_update_must_not_modify_study_progress(
        self, db, user
    ):
        """Estimate authority must never mint Study Progress (FINDING-001)."""
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Twin Boundary Topic"]
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            mastery_score=10.0,
            confidence="Low",
            current_stage=TopicProgress.STAGE_LEARNING,
            revision_count=4,
        )
        db.session.add(progress)
        db.session.commit()

        mission = _make_mission(
            user.id,
            study_plan_id=plan.id,
            title=f"Study {topics[0].name}",
        )
        LearningService.create_study_attempt(
            user_id=user.id,
            mission_id=mission.id,
            topic_id=topics[0].id,
            study_date=date.today(),
            questions_attempted=10,
            questions_correct=10,
            confidence_after="Mastered",
        )

        AdaptiveLearningService.update_mastery_after_attempt(
            user_id=user.id, topic_id=topics[0].id
        )

        updated = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert updated.mastery_score >= 70.0
        assert updated.completed is False
        assert updated.current_stage != TopicProgress.STAGE_COMPLETED


@pytest.mark.usefixtures("ctx")
class TestPositiveOwnershipBehaviours:
    """Permitted Writers still update their authorised educational states."""

    def test_mission_completion_updates_study_progress(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Coverage Topic", "Next Learning Topic"]
        )
        _make_active_plan(user.id, exam_name="IFoA CS1", curriculum=curriculum)

        _apply_mission_topic_progress(user.id, topics[0])

        progress = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert progress.completed is True
        assert progress.current_stage == TopicProgress.STAGE_COMPLETED

        nxt = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[1].id
        ).one()
        assert nxt.completed is False
        assert nxt.current_stage == TopicProgress.STAGE_LEARNING

    def test_learning_mode_updates_current_learning(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["First Topic", "Second Topic", "Third Topic"]
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum
        )
        db.session.add(
            TopicProgress(
                user_id=user.id,
                topic_id=topics[0].id,
                completed=True,
                current_stage=TopicProgress.STAGE_COMPLETED,
            )
        )
        db.session.add(
            TopicProgress(
                user_id=user.id,
                topic_id=topics[1].id,
                completed=False,
                current_stage=TopicProgress.STAGE_LEARNING,
            )
        )
        db.session.commit()

        selected = PlanningService._select_topic_for_today(
            user_id=user.id,
            active_plan=plan,
            target_date=date.today(),
        )
        assert selected is not None
        assert selected.id == topics[1].id

        # After completing the current learning topic, Learning Mode advances.
        _apply_mission_topic_progress(user.id, topics[1])
        advanced = PlanningService._select_topic_for_today(
            user_id=user.id,
            active_plan=plan,
            target_date=date.today(),
        )
        assert advanced is not None
        assert advanced.id == topics[2].id

    def test_learning_mode_generates_todays_mission(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Mission Topic A", "Mission Topic B"]
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum
        )
        db.session.add(
            TopicProgress(
                user_id=user.id,
                topic_id=topics[0].id,
                completed=False,
                current_stage=TopicProgress.STAGE_LEARNING,
            )
        )
        db.session.commit()

        mission = PlanningService.generate_today_mission(user.id)
        assert mission is not None
        assert mission.user_id == user.id
        assert mission.study_plan_id == plan.id
        assert topics[0].name in (mission.title or "")

    def test_educational_evidence_updates_twin_owned_states_only(self, db, user):
        """Accuracy-backed mastery update may change estimates, never coverage."""
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Evidence Path Topic"]
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            mastery_score=0.0,
            confidence="Low",
            current_stage=TopicProgress.STAGE_LEARNING,
            revision_count=1,
        )
        db.session.add(progress)
        db.session.commit()

        mission = _make_mission(
            user.id,
            study_plan_id=plan.id,
            title=f"Study {topics[0].name}",
        )
        LearningService.create_study_attempt(
            user_id=user.id,
            mission_id=mission.id,
            topic_id=topics[0].id,
            study_date=date.today(),
            questions_attempted=8,
            questions_correct=7,
            confidence_after="High",
        )

        AdaptiveLearningService.update_mastery_after_attempt(
            user_id=user.id, topic_id=topics[0].id
        )

        updated = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert updated.mastery_score > 0.0
        assert updated.average_accuracy is not None
        assert updated.has_estimated_mastery is True
        assert updated.completed is False
        assert updated.confidence == "High"  # felt confidence preserved, not estimate
