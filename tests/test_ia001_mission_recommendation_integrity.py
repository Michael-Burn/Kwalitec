"""IA-001 Mission Recommendation Integrity regression tests.

Ensures dashboard recommendation, today's mission, and mission launch always
refer to the same active study plan. CS1 recommendations must never launch
CM1 missions (and vice versa).
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.extensions import db
from app.models.curriculum import Curriculum, Topic
from app.models.mission import Mission
from app.models.study_plan import StudyPlan, WeekPlan
from app.models.subject import Subject
from app.models.topic_progress import TopicProgress
from app.services.mission_service import MissionService
from app.services.planning_service import PlanningService
from app.services.study_plan_service import StudyPlanService


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


@pytest.mark.usefixtures("ctx")
class TestMissionRecommendationIntegrity:
    """Regression coverage for IA-001 acceptance scenarios."""

    def test_single_study_plan_recommendation_matches_mission(self, db, user):
        """Scenario 1: single plan — generated mission is bound to that plan."""
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["CS1 Topic 1.1", "CS1 Topic 1.2"]
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum, active=True
        )

        mission = PlanningService.generate_today_mission(user.id)

        assert mission is not None
        assert mission.study_plan_id == plan.id
        assert "CS1" in mission.title or topics[0].name in mission.title

        retrieved = MissionService.get_today_mission(user.id, study_plan_id=plan.id)
        assert retrieved is not None
        assert retrieved.id == mission.id
        assert retrieved.study_plan_id == plan.id

    def test_multiple_plans_switch_updates_mission(self, db, user):
        """Scenario 2: switching active plan regenerates the correct mission."""
        cs1, cs1_topics = _make_curriculum(
            "IFoA CS1", ["Sampling distributions", "Hypothesis tests"]
        )
        cm1, cm1_topics = _make_curriculum(
            "IFoA CM1", ["Generalised linear models", "Survival models"]
        )

        plan_cs1 = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=cs1, active=True
        )
        plan_cm1 = _make_active_plan(
            user.id, exam_name="IFoA CM1", curriculum=cm1, active=False
        )

        cs1_mission = PlanningService.generate_today_mission(user.id)
        assert cs1_mission is not None
        assert cs1_mission.study_plan_id == plan_cs1.id
        assert cm1_topics[0].name not in (cs1_mission.title or "")

        StudyPlanService.set_active_plan(plan_cm1.id, user.id)

        cm1_mission = PlanningService.generate_today_mission(user.id)
        assert cm1_mission is not None
        assert cm1_mission.study_plan_id == plan_cm1.id
        assert cm1_mission.id != cs1_mission.id

        today = MissionService.get_today_mission(user.id)
        assert today is not None
        assert today.id == cm1_mission.id
        assert today.study_plan_id == plan_cm1.id

        # Original CS1 mission remains available under its own plan id
        prior = MissionService.get_today_mission(
            user.id, study_plan_id=plan_cs1.id
        )
        assert prior is not None
        assert prior.id == cs1_mission.id

    def test_cs1_recommendation_never_returns_cm1_mission(self, db, user):
        """Negative: active CS1 plan must never surface a CM1 mission."""
        cs1, _ = _make_curriculum("IFoA CS1", ["CS1 Leaf A"])
        cm1, _ = _make_curriculum("IFoA CM1", ["CM1 Leaf A"])

        plan_cs1 = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=cs1, active=True
        )
        plan_cm1 = _make_active_plan(
            user.id, exam_name="IFoA CM1", curriculum=cm1, active=False
        )

        subject = Subject(user_id=user.id, name="Study Plan", active=True)
        db.session.add(subject)
        db.session.flush()

        # Pre-seed a CM1 mission for today (as if user studied CM1 earlier)
        cm1_mission = MissionService.create_mission(
            user_id=user.id,
            subject_id=subject.id,
            mission_date=date.today(),
            title="Study CM1 Leaf A",
            study_plan_id=plan_cm1.id,
            tasks=[{"title": "Read", "description": "CM1 material", "order": 0}],
        )

        # Active plan is CS1 — retrieval must ignore the CM1 row
        leaked = MissionService.get_today_mission(
            user.id, study_plan_id=plan_cs1.id
        )
        assert leaked is None or leaked.id != cm1_mission.id

        cs1_mission = PlanningService.generate_today_mission(user.id)
        assert cs1_mission is not None
        assert cs1_mission.study_plan_id == plan_cs1.id
        assert cs1_mission.id != cm1_mission.id
        assert "CM1 Leaf A" not in (cs1_mission.title or "")

        active_today = MissionService.get_today_mission(user.id)
        assert active_today is not None
        assert active_today.study_plan_id == plan_cs1.id
        assert active_today.id == cs1_mission.id

    def test_reload_keeps_plan_scoped_mission(self, db, user):
        """Scenario 4: repeated generate/get remain consistent for the active plan."""
        curriculum, _ = _make_curriculum("IFoA CS1", ["CS1 Topic Reload"])
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum, active=True
        )

        first = PlanningService.generate_today_mission(user.id)
        second = PlanningService.generate_today_mission(user.id)
        retrieved = MissionService.get_today_mission(user.id)

        assert first is not None
        assert first.id == second.id == retrieved.id
        assert retrieved.study_plan_id == plan.id

    def test_complete_mission_then_recommendation_stays_on_plan(self, db, user):
        """Scenario 3: completing today's mission does not switch study plans."""
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["CS1 Complete A", "CS1 Complete B"]
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum, active=True
        )

        mission = PlanningService.generate_today_mission(user.id)
        assert mission is not None

        for task in mission.tasks:
            MissionService.mark_task_complete(task.id, user.id, completed=True)
        MissionService.complete_mission(mission.id, user.id)

        after = MissionService.get_today_mission(user.id, study_plan_id=plan.id)
        assert after is not None
        assert after.id == mission.id
        assert after.status == "Completed"
        assert after.study_plan_id == plan.id

        # Idempotent regenerate must return the same completed plan-scoped row
        again = PlanningService.generate_today_mission(user.id)
        assert again is not None
        assert again.id == mission.id
        assert again.study_plan_id == plan.id

    def test_weak_topic_from_other_curriculum_cannot_win(self, db, user):
        """Cross-curriculum weak progress must not select today's topic."""
        cs1, cs1_topics = _make_curriculum("IFoA CS1", ["CS1 Fresh Topic"])
        cm1, cm1_topics = _make_curriculum("IFoA CM1", ["CM1 Weak Topic"])

        plan_cs1 = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=cs1, active=True
        )
        _make_active_plan(
            user.id, exam_name="IFoA CM1", curriculum=cm1, active=False
        )

        # Strong CM1 weakness that would previously win Priority 2 globally
        weak = TopicProgress(
            user_id=user.id,
            topic_id=cm1_topics[0].id,
            mastery_score=20.0,
            revision_count=3,
            current_stage=TopicProgress.STAGE_LEARNING,
            completed=False,
        )
        db.session.add(weak)
        db.session.commit()

        selected = PlanningService._select_topic_for_today(
            user_id=user.id,
            active_plan=plan_cs1,
            target_date=date.today(),
        )
        assert selected is not None
        assert selected.id == cs1_topics[0].id
        assert selected.curriculum_id == cs1.id

    def test_dashboard_and_mission_routes_agree(
        self, app, ctx, user, logged_in_client
    ):
        """HTTP: dashboard and mission launch expose the same plan-bound title."""
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Sampling distributions"]
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum, active=True
        )

        mission = PlanningService.generate_today_mission(user.id)
        assert mission is not None
        assert mission.study_plan_id == plan.id

        dash = logged_in_client.get("/dashboard/")
        assert dash.status_code == 200
        dash_body = dash.get_data(as_text=True)
        assert mission.title in dash_body
        assert "IFoA CS1" in dash_body

        mission_page = logged_in_client.get("/missions/")
        assert mission_page.status_code == 200
        mission_body = mission_page.get_data(as_text=True)
        assert mission.title in mission_body
        assert "IFoA CS1" in mission_body

    def test_legacy_orphan_mission_is_bound_not_cross_plan_leaked(self, db, user):
        """Pre-IA-001 unbound missions are adopted by the active plan only."""
        curriculum, _ = _make_curriculum("IFoA CS1", ["CS1 Orphan Topic"])
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum, active=True
        )
        subject = Subject(user_id=user.id, name="Study Plan", active=True)
        db.session.add(subject)
        db.session.flush()

        orphan = Mission(
            user_id=user.id,
            subject_id=subject.id,
            study_plan_id=None,
            mission_date=date.today(),
            title="Study CS1 Orphan Topic",
            status="Pending",
        )
        db.session.add(orphan)
        db.session.commit()

        mission = PlanningService.generate_today_mission(user.id)
        assert mission is not None
        assert mission.id == orphan.id
        assert mission.study_plan_id == plan.id
