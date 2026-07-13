"""Regression: Learning Objective description must store full official text.

Internal Alpha hotfix — CM1 LO storage. VARCHAR(500) blocked CM1 import;
description is unbounded TEXT so any IFoA paper with long LOs imports intact.
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

    def test_cm1_longest_lo_exceeds_legacy_varchar_500(self, ctx) -> None:
        """Guard: CM1 still has LO text that would break VARCHAR(500)."""
        _, longest = _longest_prefixed_lo("ifoa", "cm1", "2026")
        assert len(longest) > 500

    def test_import_preserves_full_cm1_lo_and_cs1_cb2(
        self, ctx, db
    ) -> None:
        code, expected = _longest_prefixed_lo("ifoa", "cm1", "2026")
        assert len(expected) > 500

        imported = CurriculumService.import_curricula()
        assert imported >= 1

        for exam_name in ("IFoA CS1", "IFoA CB2", "IFoA CM1"):
            row = Curriculum.query.filter_by(
                exam_name=exam_name, version="2026"
            ).one()
            assert row.active is True
            assert Topic.query.filter_by(curriculum_id=row.id).count() >= 1
            assert (
                LearningObjective.query.join(Topic)
                .filter(Topic.curriculum_id == row.id)
                .count()
                >= 1
            )

        stored = LearningObjective.query.filter_by(description=expected).one()
        assert stored.description == expected
        assert len(stored.description) == len(expected)
        assert len(stored.description) > 500
        assert stored.description.startswith(f"[{code}]")

    def test_cm1_study_plan_progress_recommendation_and_mission(
        self, ctx, db, user
    ) -> None:
        CurriculumService.import_curricula()
        plan = _create_plan(user.id, "IFoA CM1", "2026", topic_code="1.1")

        assert plan.curriculum_id is not None
        assert plan.curriculum.exam_name == "IFoA CM1"
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
