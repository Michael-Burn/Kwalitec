"""Regression: Learning Objective description must store full official text.

Description is unbounded TEXT so IFoA papers with long LOs import intact.
"""

from __future__ import annotations

from datetime import date, timedelta

from app.extensions import db
from app.models.curriculum import Curriculum, Topic
from app.models.learning import LearningObjective
from app.models.study_plan import WeekPlan
from app.models.topic_progress import TopicProgress
from app.services.curriculum_engine_service import CurriculumEngineService
from app.services.curriculum_service import CurriculumService
from app.services.planning_service import PlanningService
from app.services.recommendation_service import RecommendationService
from app.services.study_plan_service import StudyPlanService


def _longest_prefixed_lo(
    organisation: str, paper: str, version: str
) -> tuple[str, str]:
    """Return (code, '[code] description') for the longest LO on disk."""
    engine = CurriculumEngineService()
    curriculum = engine.load_auto(organisation, paper, version)
    longest_code = ""
    longest_text = ""
    for section in getattr(curriculum, "sections", ()):
        for topic in section.topics:
            for lo in topic.learning_objectives:
                text = f"[{lo.code}] {lo.description}"
                if len(text) > len(longest_text):
                    longest_code = lo.code
                    longest_text = text
    assert longest_text, f"No learning objectives for {organisation}/{paper}/{version}"
    return longest_code, longest_text


def _create_plan(user_id: int, exam_name: str, version: str, topic_code: str = "1.1"):
    sp = StudyPlanService.create_study_plan(
        user_id=user_id,
        exam_name=exam_name,
        exam_sitting="April 2027",
        exam_date=date.today() + timedelta(days=180),
        weekday_study_minutes=60,
        weekend_study_minutes=120,
        current_stage="Learning",
        study_preference="Mixed",
        target_grade="B",
        curriculum_version=version,
        curriculum_topic_code=topic_code,
    )
    wp = WeekPlan(
        study_plan_id=sp.id,
        week_number=1,
        start_date=date.today() - timedelta(days=2),
        end_date=date.today() + timedelta(days=4),
    )
    db.session.add(wp)
    db.session.commit()
    return sp


class TestLearningObjectiveDescriptionStorage:
    """Official syllabus LO text must persist without length truncation."""

    def test_model_accepts_descriptions_longer_than_legacy_varchar_500(
        self, ctx, db
    ) -> None:
        """Guard: LearningObjective.description remains unbounded TEXT."""
        curriculum = Curriculum(
            exam_name="IFoA CS1", version="2099-lo-storage", active=True
        )
        db.session.add(curriculum)
        db.session.flush()
        topic = Topic(
            curriculum_id=curriculum.id,
            name="LO storage probe",
            order=1,
            recommended_minutes=30,
            syllabus_weight=0.0,
        )
        db.session.add(topic)
        db.session.flush()
        long_text = "[" + ("x" * 40) + "] " + ("y" * 500)
        assert len(long_text) > 500
        lo = LearningObjective(
            topic_id=topic.id,
            description=long_text,
            order=1,
        )
        db.session.add(lo)
        db.session.commit()

        stored = LearningObjective.query.filter_by(description=long_text).one()
        assert stored.description == long_text
        assert len(stored.description) > 500

    def test_import_preserves_full_cs1_lo(self, ctx, db) -> None:
        code, expected = _longest_prefixed_lo("ifoa", "cs1", "2026")

        imported = CurriculumService.import_curricula()
        assert imported >= 1

        row = Curriculum.query.filter_by(
            exam_name="IFoA CS1", version="2026"
        ).one()
        assert row.active is True
        assert Topic.query.filter_by(curriculum_id=row.id).count() >= 1
        assert (
            LearningObjective.query.join(Topic)
            .filter(Topic.curriculum_id == row.id)
            .count()
            >= 1
        )
        assert Curriculum.query.filter_by(exam_name="IFoA CB2").first() is None
        assert Curriculum.query.filter_by(exam_name="IFoA CM1").first() is None

        stored = LearningObjective.query.filter_by(description=expected).one()
        assert stored.description == expected
        assert len(stored.description) == len(expected)
        assert stored.description.startswith(f"[{code}]")

    def test_cs1_study_plan_progress_recommendation_and_mission(
        self, ctx, db, user
    ) -> None:
        CurriculumService.import_curricula()
        plan = _create_plan(user.id, "IFoA CS1", "2026", topic_code="1.1")

        assert plan.curriculum_id is not None
        assert plan.curriculum.exam_name == "IFoA CS1"
        topic_count = Topic.query.filter_by(
            curriculum_id=plan.curriculum_id
        ).count()
        assert topic_count >= 1
        assert TopicProgress.query.filter_by(user_id=user.id).count() == topic_count

        recommendations = RecommendationService.generate_recommendations(
            user.id, limit=5
        )
        assert len(recommendations) >= 1

        mission = PlanningService.generate_today_mission(user.id)
        assert mission is not None
        assert mission.tasks
