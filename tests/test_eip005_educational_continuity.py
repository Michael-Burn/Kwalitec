"""EIP-005 Educational Continuity regression tests.

Negative tests prove deleting a Study Plan never destroys learner-owned
educational history.

Positive tests prove planning artefacts are disposable and that new plans /
Learning Mode surfaces can continue preserved history.

Governing refs:
- Constitution Articles II §1.8, IV, VIII.15, IX §4
- EL-001, EL-011
- EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md §4–5
- EDUCATIONAL_CONTINUITY_STANDARD.md
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.extensions import db
from app.models.curriculum import Curriculum, Topic
from app.models.decision import Decision
from app.models.learning import StudyAttempt
from app.models.mission import Mission, MissionTask
from app.models.study_plan import StudyPlan, WeekPlan
from app.models.subject import Subject
from app.models.topic_progress import TopicProgress
from app.services.educational_continuity_service import EducationalContinuityService
from app.services.planning_service import PlanningService
from app.services.recommendation_service import RecommendationService
from app.services.study_plan_service import StudyPlanService


def _make_curriculum(
    exam_name: str,
    topic_names: list[str],
    *,
    version: str = "2025",
) -> tuple[Curriculum, list[Topic]]:
    curriculum = Curriculum(exam_name=exam_name, version=version, active=True)
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


def _make_plan(
    user_id: int,
    *,
    exam_name: str,
    curriculum: Curriculum,
    topic_code: str | None = None,
    active: bool = True,
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
        active=active,
        curriculum_topic_code=topic_code,
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
        status="Completed",
    )
    db.session.add(mission)
    db.session.flush()
    db.session.add(
        MissionTask(mission_id=mission.id, title="Study", order=0, completed=True)
    )
    db.session.commit()
    return mission


@pytest.mark.usefixtures("ctx")
class TestNegativeContinuityRegressions:
    """Deleting a Study Plan must not silently destroy educational history."""

    def test_delete_study_plan_does_not_delete_study_progress(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1 Continuity", ["Cont Topic A", "Cont Topic B"]
        )
        plan = _make_plan(
            user.id, exam_name="IFoA CS1 Continuity", curriculum=curriculum
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            confidence="Medium",
            completed=True,
            mastery_score=0.0,
            current_stage=TopicProgress.STAGE_COMPLETED,
        )
        db.session.add(progress)
        db.session.commit()

        StudyPlanService.delete_study_plan(plan.id, user.id)

        preserved = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert preserved.completed is True
        assert preserved.current_stage == TopicProgress.STAGE_COMPLETED

    def test_delete_study_plan_does_not_delete_study_attempts(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1 Continuity", ["Attempt Topic"]
        )
        plan = _make_plan(
            user.id, exam_name="IFoA CS1 Continuity", curriculum=curriculum
        )
        mission = _make_mission(user.id, study_plan_id=plan.id, title="Attempt Mission")
        attempt = StudyAttempt(
            user_id=user.id,
            mission_id=mission.id,
            topic_id=topics[0].id,
            study_date=date.today(),
            duration_minutes=40,
            questions_attempted=5,
            questions_correct=4,
        )
        db.session.add(attempt)
        db.session.commit()
        attempt_id = attempt.id

        StudyPlanService.delete_study_plan(plan.id, user.id)

        assert StudyAttempt.query.get(attempt_id) is not None
        assert Mission.query.get(mission.id) is not None
        assert Mission.query.get(mission.id).study_plan_id is None

    def test_delete_study_plan_does_not_delete_educational_evidence(self, db, user):
        """Evidence posture lives on TopicProgress / attempts — must survive."""
        curriculum, topics = _make_curriculum(
            "IFoA CS1 Continuity", ["Evidence Topic"]
        )
        plan = _make_plan(
            user.id, exam_name="IFoA CS1 Continuity", curriculum=curriculum
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            confidence="High",
            completed=True,
            mastery_score=72.0,
            average_accuracy=80.0,
            current_stage=TopicProgress.STAGE_PRACTISING,
        )
        db.session.add(progress)
        db.session.commit()

        StudyPlanService.delete_study_plan(plan.id, user.id)

        preserved = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert preserved.average_accuracy == 80.0

    def test_delete_study_plan_does_not_delete_estimated_knowledge(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1 Continuity", ["Knowledge Topic"]
        )
        plan = _make_plan(
            user.id, exam_name="IFoA CS1 Continuity", curriculum=curriculum
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            confidence="Medium",
            completed=False,
            mastery_score=55.5,
            average_accuracy=60.0,
            current_stage=TopicProgress.STAGE_PRACTISING,
        )
        db.session.add(progress)
        db.session.commit()

        StudyPlanService.delete_study_plan(plan.id, user.id)

        preserved = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert preserved.mastery_score == 55.5

    def test_delete_study_plan_does_not_delete_estimated_mastery(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1 Continuity", ["Mastery Topic"]
        )
        plan = _make_plan(
            user.id, exam_name="IFoA CS1 Continuity", curriculum=curriculum
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            confidence="High",
            completed=True,
            mastery_score=88.0,
            average_accuracy=90.0,
            current_stage=TopicProgress.STAGE_MASTERED,
        )
        db.session.add(progress)
        db.session.commit()

        StudyPlanService.delete_study_plan(plan.id, user.id)

        preserved = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert preserved.mastery_score == 88.0
        assert preserved.current_stage == TopicProgress.STAGE_MASTERED
        assert preserved.has_estimated_mastery is True


@pytest.mark.usefixtures("ctx")
class TestPositiveContinuityRegressions:
    """Planning is disposable; educational history continues lawfully."""

    def test_delete_removes_planning_metadata_and_week_plans(self, db, user):
        curriculum, _topics = _make_curriculum(
            "IFoA CS1 Continuity", ["Plan Topic"]
        )
        plan = _make_plan(
            user.id, exam_name="IFoA CS1 Continuity", curriculum=curriculum
        )
        plan_id = plan.id
        assert WeekPlan.query.filter_by(study_plan_id=plan_id).count() == 1

        StudyPlanService.delete_study_plan(plan_id, user.id)

        assert StudyPlan.query.get(plan_id) is None
        assert WeekPlan.query.filter_by(study_plan_id=plan_id).count() == 0

    def test_new_study_plan_continues_existing_educational_history(self, db, user):
        sp = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="1.1",
            completed_curriculum_topics=["1.1"],
        )
        first_progress = TopicProgress.query.filter_by(user_id=user.id).all()
        assert any(tp.completed for tp in first_progress)
        completed_ids = {tp.topic_id for tp in first_progress if tp.completed}
        progress_count = len(first_progress)

        # Stamp estimate evidence on a completed unit.
        sample = TopicProgress.query.filter(
            TopicProgress.user_id == user.id,
            TopicProgress.topic_id.in_(completed_ids),
        ).first()
        assert sample is not None
        sample.average_accuracy = 75.0
        sample.mastery_score = 70.0
        db.session.commit()
        sample_topic_id = sample.topic_id

        StudyPlanService.delete_study_plan(sp.id, user.id)
        assert TopicProgress.query.filter_by(user_id=user.id).count() == progress_count

        new_plan = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="September 2027",
            exam_date=date.today() + timedelta(days=240),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="1.2",
        )

        continued = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=sample_topic_id
        ).one()
        assert continued.completed is True
        assert continued.average_accuracy == 75.0
        assert continued.mastery_score == 70.0
        assert new_plan.curriculum_id == sp.curriculum_id or new_plan.curriculum_id

    def test_current_learning_recalculates_from_preserved_progress(self, db, user):
        sp = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="1.1",
            completed_curriculum_topics=["1.1"],
        )
        StudyPlanService.delete_study_plan(sp.id, user.id)

        new_plan = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="September 2027",
            exam_date=date.today() + timedelta(days=240),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="1.1",
        )
        StudyPlanService.set_active_plan(new_plan.id, user.id)
        StudyPlanService.reconcile_current_topic_pointer(new_plan)
        db.session.refresh(new_plan)

        # Preserved completion of 1.1 advances Current Learning past 1.1.
        assert new_plan.curriculum_topic_code != "1.1"
        assert new_plan.curriculum_topic_code is not None

    def test_mission_regenerates_correctly_after_plan_recreation(self, db, user):
        first = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="1.1",
            completed_curriculum_topics=["1.1"],
        )
        StudyPlanService.set_active_plan(first.id, user.id)
        StudyPlanService.delete_study_plan(first.id, user.id)

        second = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="September 2027",
            exam_date=date.today() + timedelta(days=240),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="1.1",
        )
        StudyPlanService.set_active_plan(second.id, user.id)
        StudyPlanService.reconcile_current_topic_pointer(second)
        db.session.refresh(second)

        mission = PlanningService.generate_today_mission(user.id)
        assert mission is not None
        assert mission.study_plan_id == second.id

    def test_recommendations_regenerate_correctly_after_plan_recreation(
        self, db, user
    ):
        first = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="1.1",
        )
        StudyPlanService.set_active_plan(first.id, user.id)
        StudyPlanService.delete_study_plan(first.id, user.id)

        second = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="September 2027",
            exam_date=date.today() + timedelta(days=240),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="1.1",
        )
        StudyPlanService.set_active_plan(second.id, user.id)

        recommendations = RecommendationService.generate_recommendations(user.id)
        assert recommendations is not None
        assert isinstance(recommendations, list)

    def test_decision_journal_survives_plan_delete(self, db, user):
        curriculum, _topics = _make_curriculum(
            "IFoA CS1 Continuity", ["Decision Topic"]
        )
        plan = _make_plan(
            user.id, exam_name="IFoA CS1 Continuity", curriculum=curriculum
        )
        decision = Decision(
            user_id=user.id,
            recommendation_title="Practise topic",
            recommendation_category="Practice",
            recommendation_priority="High",
            recommendation_reason="coverage lag",
            recommendation_expected_benefit="stronger retention",
            accepted=True,
        )
        db.session.add(decision)
        db.session.commit()
        decision_id = decision.id

        StudyPlanService.delete_study_plan(plan.id, user.id)
        assert Decision.query.get(decision_id) is not None

    def test_curriculum_remap_by_official_topic_code(
        self, db, user, monkeypatch
    ):
        """Objective code matches may continue history; unknown identity is retained."""
        prior, prior_topics = _make_curriculum(
            "IFoA REMAP", ["Alpha Unit", "Orphan Unit"], version="2024"
        )
        target, target_topics = _make_curriculum(
            "IFoA REMAP", ["Alpha Unit", "Beta Unit"], version="2025"
        )

        prior_progress = TopicProgress(
            user_id=user.id,
            topic_id=prior_topics[0].id,
            confidence="High",
            completed=True,
            mastery_score=66.0,
            average_accuracy=70.0,
            current_stage=TopicProgress.STAGE_COMPLETED,
        )
        orphan_progress = TopicProgress(
            user_id=user.id,
            topic_id=prior_topics[1].id,
            confidence="Low",
            completed=True,
            mastery_score=40.0,
            average_accuracy=45.0,
            current_stage=TopicProgress.STAGE_COMPLETED,
        )
        db.session.add_all([prior_progress, orphan_progress])
        db.session.commit()

        codes = {
            prior_topics[0].id: "A.1",
            prior_topics[1].id: "LEGACY.9",
            target_topics[0].id: "A.1",
            target_topics[1].id: "B.1",
        }

        def _fake_resolve(db_topic, *, exam_name, curriculum_version):
            return codes.get(db_topic.id)

        monkeypatch.setattr(
            EducationalContinuityService,
            "resolve_official_topic_code",
            staticmethod(_fake_resolve),
        )

        result = EducationalContinuityService.remap_study_progress_to_curriculum(
            user.id, target, exam_name="IFoA REMAP"
        )

        assert target_topics[0].id in result.remapped_topic_ids
        remapped = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=target_topics[0].id
        ).one()
        assert remapped.completed is True
        assert remapped.mastery_score == 66.0
        assert remapped.average_accuracy == 70.0

        # Unmapped prior unit remains as historical learner history.
        retained = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=prior_topics[1].id
        ).one()
        assert retained.completed is True
        assert prior_topics[1].id in result.retained_unmapped_topic_ids
