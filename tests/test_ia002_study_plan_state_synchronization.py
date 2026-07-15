"""IA-002 Study Plan State Synchronization regression tests.

Switching the active study plan must immediately synchronize dashboard,
today's mission, and launch surfaces without a manual browser refresh.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.extensions import db
from app.models.curriculum import Curriculum, Topic
from app.models.mission import Mission
from app.models.study_plan import StudyPlan, WeekPlan
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


def _make_plan(
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
class TestStudyPlanStateSynchronization:
    """Regression coverage for IA-002 acceptance scenarios."""

    def test_single_plan_unchanged(self, db, user):
        """Scenario 1: single active plan — generate remains plan-bound."""
        curriculum, _ = _make_curriculum("IFoA CS1", ["CS1 Sync Topic"])
        plan = _make_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum, active=True
        )

        mission = PlanningService.generate_today_mission(user.id)
        assert mission is not None
        assert mission.study_plan_id == plan.id

        # Re-activating the same plan must not invent a second mission
        StudyPlanService.set_active_plan(plan.id, user.id)
        again = MissionService.get_today_mission(user.id)
        assert again is not None
        assert again.id == mission.id
        assert again.study_plan_id == plan.id

    def test_switch_cs1_to_cm1_updates_immediately(self, db, user, logged_in_client):
        """Scenario 2: HTTP switch lands on dashboard with CM1 mission."""
        cs1, _ = _make_curriculum("IFoA CS1", ["CS1 Leaf"])
        cm1, _ = _make_curriculum("IFoA CM1", ["CM1 Leaf"])
        plan_cs1 = _make_plan(
            user.id, exam_name="IFoA CS1", curriculum=cs1, active=True
        )
        plan_cm1 = _make_plan(
            user.id, exam_name="IFoA CM1", curriculum=cm1, active=False
        )

        cs1_mission = PlanningService.generate_today_mission(user.id)
        assert cs1_mission is not None
        assert cs1_mission.study_plan_id == plan_cs1.id

        # Single POST — no extra refresh — must show CM1 on the dashboard
        response = logged_in_client.post(
            f"/study-plan/{plan_cm1.id}/set-active",
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert response.request.path.rstrip("/").endswith("dashboard")

        body = response.get_data(as_text=True)
        assert "IFoA CM1" in body
        assert "active study plan" in body.lower()

        cm1_mission = MissionService.get_today_mission(user.id)
        assert cm1_mission is not None
        assert cm1_mission.study_plan_id == plan_cm1.id
        assert cm1_mission.id != cs1_mission.id
        assert cm1_mission.title in body

        mission_page = logged_in_client.get("/missions/")
        assert mission_page.status_code == 200
        mission_body = mission_page.get_data(as_text=True)
        assert cm1_mission.title in mission_body
        assert "IFoA CM1" in mission_body

    def test_back_and_forth_preserves_plan_missions(self, db, user, logged_in_client):
        """Scenario 3: CS1 → CM1 → CS1 restores original CS1 mission."""
        cs1, _ = _make_curriculum("IFoA CS1", ["Sampling distributions"])
        cm1, _ = _make_curriculum("IFoA CM1", ["Generalised linear models"])
        plan_cs1 = _make_plan(
            user.id, exam_name="IFoA CS1", curriculum=cs1, active=True
        )
        plan_cm1 = _make_plan(
            user.id, exam_name="IFoA CM1", curriculum=cm1, active=False
        )

        cs1_mission = PlanningService.generate_today_mission(user.id)
        assert cs1_mission is not None
        assert cs1_mission.study_plan_id == plan_cs1.id

        StudyPlanService.set_active_plan(plan_cm1.id, user.id)
        cm1_mission = MissionService.get_today_mission(user.id)
        assert cm1_mission is not None
        assert cm1_mission.study_plan_id == plan_cm1.id
        assert cm1_mission.id != cs1_mission.id

        # Switch back — original CS1 mission must remain the authority
        response = logged_in_client.post(
            f"/study-plan/{plan_cs1.id}/set-active",
            follow_redirects=True,
        )
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "IFoA CS1" in body
        assert cs1_mission.title in body

        restored = MissionService.get_today_mission(user.id)
        assert restored is not None
        assert restored.id == cs1_mission.id
        assert restored.study_plan_id == plan_cs1.id

        # CM1 mission remains addressable under its own plan id — no overwrite
        other = MissionService.get_today_mission(
            user.id, study_plan_id=plan_cm1.id
        )
        assert other is not None
        assert other.id == cm1_mission.id

        mission_page = logged_in_client.get("/missions/")
        mission_body = mission_page.get_data(as_text=True)
        assert cs1_mission.title in mission_body
        assert "IFoA CS1" in mission_body

    def test_reload_keeps_synchronized_state(self, db, user, logged_in_client):
        """Scenario 4: after switch, reload still shows the active plan."""
        cs1, _ = _make_curriculum("IFoA CS1", ["CS1 Reload"])
        cm1, _ = _make_curriculum("IFoA CM1", ["CM1 Reload"])
        _make_plan(user.id, exam_name="IFoA CS1", curriculum=cs1, active=True)
        plan_cm1 = _make_plan(
            user.id, exam_name="IFoA CM1", curriculum=cm1, active=False
        )

        logged_in_client.post(
            f"/study-plan/{plan_cm1.id}/set-active",
            follow_redirects=True,
        )
        mission = MissionService.get_today_mission(user.id)
        assert mission is not None
        assert mission.study_plan_id == plan_cm1.id

        reload = logged_in_client.get("/dashboard/")
        assert reload.status_code == 200
        body = reload.get_data(as_text=True)
        assert "IFoA CM1" in body
        assert mission.title in body

        again = MissionService.get_today_mission(user.id)
        assert again is not None
        assert again.id == mission.id

    def test_mission_completion_after_switch_stays_on_plan(
        self, db, user, logged_in_client
    ):
        """Scenario 5: complete after switch; surfaces stay on new plan."""
        cs1, _ = _make_curriculum("IFoA CS1", ["CS1 Before Switch"])
        cm1, cm1_topics = _make_curriculum("IFoA CM1", ["CM1 After Switch"])
        _make_plan(user.id, exam_name="IFoA CS1", curriculum=cs1, active=True)
        plan_cm1 = _make_plan(
            user.id, exam_name="IFoA CM1", curriculum=cm1, active=False
        )

        PlanningService.generate_today_mission(user.id)
        StudyPlanService.set_active_plan(plan_cm1.id, user.id)

        mission = MissionService.get_today_mission(user.id)
        assert mission is not None
        assert mission.study_plan_id == plan_cm1.id

        for task in mission.tasks:
            MissionService.mark_task_complete(task.id, user.id, completed=True)
        MissionService.complete_mission(mission.id, user.id)

        after = MissionService.get_today_mission(user.id, study_plan_id=plan_cm1.id)
        assert after is not None
        assert after.status == "Completed"
        assert after.study_plan_id == plan_cm1.id

        dash = logged_in_client.get("/dashboard/")
        assert dash.status_code == 200
        body = dash.get_data(as_text=True)
        assert "IFoA CM1" in body
        assert after.title in body
        # Must not resurrect the prior CS1 mission as today's card
        assert StudyPlanService.get_user_active_plan(user.id).id == plan_cm1.id

    def test_synchronize_student_surfaces_binds_mission(self, db, user):
        """Service helper generates the active plan's mission immediately."""
        curriculum, _ = _make_curriculum("IFoA CS1", ["CS1 Sync Helper"])
        plan = _make_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum, active=True
        )

        assert MissionService.get_today_mission(user.id) is None
        StudyPlanService.synchronize_student_surfaces(user.id)
        mission = MissionService.get_today_mission(user.id)
        assert mission is not None
        assert mission.study_plan_id == plan.id

    def test_activate_does_not_cache_foreign_plan_mission(self, db, user):
        """Negative: activating CS1 never surfaces a CM1 mission row."""
        cs1, _ = _make_curriculum("IFoA CS1", ["CS1 Only"])
        cm1, _ = _make_curriculum("IFoA CM1", ["CM1 Foreign"])
        plan_cs1 = _make_plan(
            user.id, exam_name="IFoA CS1", curriculum=cs1, active=False
        )
        plan_cm1 = _make_plan(
            user.id, exam_name="IFoA CM1", curriculum=cm1, active=True
        )

        cm1_mission = PlanningService.generate_today_mission(user.id)
        assert cm1_mission is not None
        assert cm1_mission.study_plan_id == plan_cm1.id

        StudyPlanService.set_active_plan(plan_cs1.id, user.id)
        today = MissionService.get_today_mission(user.id)
        assert today is not None
        assert today.study_plan_id == plan_cs1.id
        assert today.id != cm1_mission.id
        assert Mission.query.get(cm1_mission.id).study_plan_id == plan_cm1.id
