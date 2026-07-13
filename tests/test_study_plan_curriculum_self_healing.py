"""Capability 4.6 — Study Plan curriculum self-healing.

Legacy unbound plans (missing curriculum_id / curriculum_version) must repair
transparently through StudyPlanService accessors — not via PlanningService or
RecommendationService. Dashboard load is the primary Internal Alpha surface.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.extensions import db
from app.models.curriculum import Curriculum, Topic
from app.models.study_plan import WeekPlan
from app.models.topic_progress import TopicProgress
from app.services.curriculum_service import CurriculumService
from app.services.planning_service import PlanningService
from app.services.recommendation_service import RecommendationService
from app.services.study_plan_service import StudyPlanService


def _create_unbound_plan(user_id: int, exam_name: str):
    """Create an active study plan with no curriculum binding (legacy shape)."""
    plan = StudyPlanService.create_study_plan(
        user_id=user_id,
        exam_name=exam_name,
        exam_sitting="April 2027",
        exam_date=date.today() + timedelta(days=180),
        weekday_study_minutes=60,
        weekend_study_minutes=120,
        current_stage="Learning",
        study_preference="Mixed",
        target_grade="B",
        curriculum_version=None,
        curriculum_topic_code=None,
    )
    assert plan.curriculum_id is None
    assert plan.curriculum_version is None
    wp = WeekPlan(
        study_plan_id=plan.id,
        week_number=1,
        start_date=date.today() - timedelta(days=2),
        end_date=date.today() + timedelta(days=4),
    )
    db.session.add(wp)
    db.session.commit()
    return plan


@pytest.mark.parametrize(
    "exam_name,topic_fragment",
    [
        ("IFoA CS1", "data analysis"),
        ("IFoA CB2", "economics and business"),
        ("IFoA CM1", "interest rates"),
    ],
)
class TestStudyPlanCurriculumSelfHealing:
    """Every supported syllabus repairs through the same StudyPlanService path."""

    def test_get_user_active_plan_binds_legacy_plan(
        self, db, user, exam_name, topic_fragment
    ):
        CurriculumService.import_curricula()
        curriculum = Curriculum.query.filter_by(exam_name=exam_name).one()
        topic_count = Topic.query.filter_by(curriculum_id=curriculum.id).count()
        assert topic_count >= 1

        plan = _create_unbound_plan(user.id, exam_name)
        assert TopicProgress.query.filter_by(user_id=user.id).count() == 0

        loaded = StudyPlanService.get_user_active_plan(user.id)
        assert loaded is not None
        assert loaded.id == plan.id
        assert loaded.curriculum_id == curriculum.id
        assert loaded.curriculum_version == "2026"
        assert TopicProgress.query.filter_by(user_id=user.id).count() == topic_count

        # Idempotent — second load does not duplicate progress.
        again = StudyPlanService.get_user_active_plan(user.id)
        assert again.curriculum_id == curriculum.id
        assert TopicProgress.query.filter_by(user_id=user.id).count() == topic_count

    def test_dashboard_repairs_then_mission_and_recommendation_use_syllabus(
        self, logged_in_client, db, user, exam_name, topic_fragment
    ):
        CurriculumService.import_curricula()
        curriculum = Curriculum.query.filter_by(exam_name=exam_name).one()
        topic_count = Topic.query.filter_by(curriculum_id=curriculum.id).count()
        first_topic = CurriculumService.get_all_topics_ordered(curriculum)[0]

        plan = _create_unbound_plan(user.id, exam_name)
        assert plan.curriculum_id is None
        assert TopicProgress.query.filter_by(user_id=user.id).count() == 0

        # Dashboard is the Internal Alpha surface that loads the active plan.
        response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200

        db.session.refresh(plan)
        assert plan.curriculum_id == curriculum.id
        assert plan.curriculum_version == "2026"
        assert TopicProgress.query.filter_by(user_id=user.id).count() == topic_count

        selected = PlanningService._select_topic_for_today(
            user_id=user.id,
            active_plan=plan,
            target_date=date.today(),
        )
        assert selected is not None
        assert topic_fragment in selected.name.lower()

        mission = PlanningService.generate_today_mission(user.id)
        assert mission is not None
        code = PlanningService._resolve_official_topic_code(plan, selected)
        assert code is not None
        assert (
            code in mission.title
            or first_topic.name.lower() in mission.title.lower()
            or topic_fragment in mission.title.lower()
        )
        assert not mission.title.lower().startswith("daily study")
        assert mission.tasks
        lead = mission.tasks[0].description.lower()
        assert not lead.startswith("read the core reading for today's section")

        recs = RecommendationService.generate_recommendations(user.id, limit=5)
        assert len(recs) >= 1
        blob = " ".join(
            f"{r.get('title', '')} {r.get('reason', '')}" for r in recs
        ).lower()
        assert (
            topic_fragment in blob
            or (code or "").lower() in blob
            or first_topic.name.lower() in blob
            or "topic" in blob
            or "curriculum" in blob
        )

    def test_get_plan_and_list_heal_without_planning_service(
        self, db, user, exam_name, topic_fragment
    ):
        CurriculumService.import_curricula()
        curriculum = Curriculum.query.filter_by(exam_name=exam_name).one()
        plan = _create_unbound_plan(user.id, exam_name)

        loaded = StudyPlanService.get_plan(plan.id, user_id=user.id)
        assert loaded is not None
        assert loaded.curriculum_id == curriculum.id
        assert loaded.curriculum_version == "2026"

        # New unbound active plan — list accessor must heal it.
        unbound = _create_unbound_plan(user.id, exam_name)
        assert unbound.curriculum_id is None
        plans = StudyPlanService.get_user_plans(user.id)
        assert any(p.id == unbound.id for p in plans)
        db.session.refresh(unbound)
        assert unbound.curriculum_id == curriculum.id
        assert unbound.curriculum_version == "2026"


def test_non_curriculum_exam_stays_unbound(db, user):
    """Exams without on-disk syllabi must not invent a curriculum binding."""
    plan = _create_unbound_plan(user.id, "CFA Level I")
    loaded = StudyPlanService.get_user_active_plan(user.id)
    assert loaded is not None
    assert loaded.id == plan.id
    assert loaded.curriculum_id is None
    assert loaded.curriculum_version is None
    assert TopicProgress.query.filter_by(user_id=user.id).count() == 0


def test_planning_service_does_not_call_ensure_directly(db, user, monkeypatch):
    """Curriculum repair must live only in StudyPlanService accessors."""
    CurriculumService.import_curricula()
    plan = _create_unbound_plan(user.id, "IFoA CB2")

    calls: list[int] = []
    original = StudyPlanService.ensure_curriculum_binding

    def _tracking(sp):
        calls.append(sp.id)
        return original(sp)

    monkeypatch.setattr(StudyPlanService, "ensure_curriculum_binding", _tracking)

    # Accessor heals once.
    StudyPlanService.get_user_active_plan(user.id)
    assert len(calls) == 1

    # Planning selection assumes the plan is already valid — no extra repair.
    calls.clear()
    db.session.refresh(plan)
    PlanningService._select_topic_for_today(
        user_id=user.id,
        active_plan=plan,
        target_date=date.today(),
    )
    assert calls == []


class TestCS1Topic11ProgressPersistence:
    """CS1 topic 1.1 must stay completed across heal/refresh once earned."""

    def test_heal_preserves_completed_11_and_advances_pointer(self, db, user):
        CurriculumService.import_curricula()
        plan = StudyPlanService.create_study_plan(
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
        assert plan.curriculum_topic_code == "1.1"

        topic_11 = Topic.query.filter_by(
            curriculum_id=plan.curriculum_id,
            name="Describe the purpose and function of data analysis",
        ).one()
        progress = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topic_11.id
        ).one()
        progress.completed = True
        progress.current_stage = TopicProgress.STAGE_COMPLETED
        progress.mastery_score = 70.0
        progress.confidence = "High"
        # Simulate a partially unbound plan that still has a stale 1.1 pointer.
        plan.curriculum_id = None
        db.session.commit()

        healed = StudyPlanService.get_user_active_plan(user.id)
        assert healed is not None
        db.session.refresh(progress)
        assert progress.completed is True
        assert progress.current_stage == TopicProgress.STAGE_COMPLETED
        assert healed.curriculum_topic_code == "1.2"

    def test_reconcile_advances_pointer_after_11_completed(self, db, user):
        CurriculumService.import_curricula()
        plan = StudyPlanService.create_study_plan(
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
        topic_11 = Topic.query.filter_by(
            curriculum_id=plan.curriculum_id,
            name="Describe the purpose and function of data analysis",
        ).one()
        progress = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topic_11.id
        ).one()
        progress.completed = True
        progress.current_stage = TopicProgress.STAGE_COMPLETED
        db.session.flush()

        StudyPlanService.reconcile_current_topic_pointer(plan)
        db.session.commit()

        assert plan.curriculum_topic_code == "1.2"
        topic_12 = Topic.query.filter_by(
            curriculum_id=plan.curriculum_id,
            name="Complete exploratory data analysis",
        ).one()
        next_progress = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topic_12.id
        ).one()
        assert next_progress.current_stage == TopicProgress.STAGE_LEARNING
        assert next_progress.completed is False
