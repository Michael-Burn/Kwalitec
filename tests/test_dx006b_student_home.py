"""DX-006B Phase 4 — Student Home service unit tests."""

from __future__ import annotations

from dataclasses import replace

from app.application.student_experience.dto.home_snapshot import (
    HomeSnapshot,
    StartSessionActionSnapshot,
)
from app.extensions import db
from app.presentation.student.services.student_home_service import (
    StudentHomeService,
)
from app.presentation.student.view_models import (
    HistoryPageViewModel,
    HistorySessionViewModel,
    StudentPageViewModel,
    StudentShellViewModel,
    home_vm,
)


def _page(home_vm_obj, *, history=None, revision=None) -> StudentPageViewModel:
    return StudentPageViewModel(
        shell=StudentShellViewModel(
            active_surface="home",
            active_label="Home",
            navigation=(),
            page_title="Home",
        ),
        home=home_vm_obj,
        history=history,
        revision=revision,
    )


def test_empty_home(app):
    with app.test_request_context("/student/"):
        page = StudentHomeService().build_home(None)
    assert page.state == "empty"
    assert page.mission is None
    assert page.empty_action_label == "Choose Exam"
    assert page.page_title == "Home"


def test_resume_mission_is_continue_session(app, ctx):
    home = home_vm(
        HomeSnapshot(
            student_id="1",
            greeting="Welcome back",
            examination_label="CS1 FR",
            has_recommendation=True,
            recommendation_title="Lease liability",
            can_start_session=True,
            estimated_study_minutes=25,
            start_session=StartSessionActionSnapshot(
                label="Continue",
                enabled=True,
                can_start=True,
                mission_id="m1",
                session_id="sess-abc",
                estimated_minutes=25,
                topic_title="Lease liability",
            ),
        ),
        unified_journey=False,
    )
    with app.test_request_context("/student/"):
        page = StudentHomeService().build_home(_page(home))
    assert page.state == "mission"
    assert page.mission is not None
    assert page.mission.primary_label == "Continue"
    assert page.mission.primary_kind == "link"
    assert "/session/sess-abc/overview" in page.mission.primary_href
    assert "Open session" in page.mission.why_now


def test_start_mission_uses_start_form(app, ctx):
    home = home_vm(
        HomeSnapshot(
            student_id="1",
            examination_label="CS1 FR",
            has_recommendation=True,
            recommendation_title="Lease liability",
            can_start_session=True,
            estimated_study_minutes=25,
            start_session=StartSessionActionSnapshot(
                label="Start Session",
                enabled=True,
                can_start=True,
                mission_id="m1",
                session_id="",
                estimated_minutes=25,
                topic_title="Lease liability",
            ),
        ),
        unified_journey=False,
    )
    with app.test_request_context("/student/"):
        page = StudentHomeService().build_home(_page(home))
    assert page.mission is not None
    assert page.mission.primary_kind == "start_form"
    assert page.mission.primary_label == "Start Today's Session"
    assert page.mission.subject_name == "CS1 FR"
    assert "Lease liability" in page.mission.objective


def test_day_complete_has_no_primary(app, ctx):
    home = home_vm(
        HomeSnapshot(
            student_id="1",
            examination_label="CS1 FR",
            has_recommendation=True,
            recommendation_title="Done",
            can_start_session=False,
        ),
        unified_journey=False,
    )
    home = replace(home, day_complete=True)
    with app.test_request_context("/student/"):
        page = StudentHomeService().build_home(_page(home))
    assert page.state == "day_complete"
    assert page.mission is not None
    assert page.mission.primary_kind == "none"
    assert "tomorrow" in page.day_complete_message.lower()


def test_recent_progress_relocated_to_history(app, ctx):
    """SOP-001: session archives belong on History, not Home."""
    sessions = tuple(
        HistorySessionViewModel(
            session_id=f"s{i}",
            topic_title=f"Topic {i}",
            completed_at=f"Day {i}",
            outcome_label="Session",
        )
        for i in range(8)
    )
    history = HistoryPageViewModel(sessions=sessions, session_count=8)
    home = home_vm(
        HomeSnapshot(
            student_id="1",
            examination_label="CS1",
            has_recommendation=True,
            recommendation_title="Topic",
            can_start_session=True,
            start_session=StartSessionActionSnapshot(
                label="Start Session",
                enabled=True,
                can_start=True,
                mission_id="m1",
            ),
        ),
        unified_journey=False,
    )
    with app.test_request_context("/student/"):
        page = StudentHomeService().build_home(_page(home, history=history))
    assert page.recent_progress == ()


def test_template_mission_first_no_legacy_chrome(app, ctx):
    from flask import render_template

    home_vm_obj = home_vm(
        HomeSnapshot(
            student_id="1",
            examination_label="CS1 FR",
            has_recommendation=True,
            recommendation_title="Lease liability",
            can_start_session=True,
            start_session=StartSessionActionSnapshot(
                label="Continue",
                enabled=True,
                can_start=True,
                mission_id="m1",
                session_id="sess-1",
                topic_title="Lease liability",
            ),
        ),
        unified_journey=False,
    )
    page = _page(home_vm_obj)
    with app.test_request_context("/student/"):
        home = StudentHomeService().build_home(page)
        html = render_template(
            "student/home.html",
            page=page,
            home=home,
            form=None,
        )
    assert (
        "Today&#39;s Mission" in html
        or "Continue Session" in html
        or ">Continue<" in html
    )
    assert "Continue" in html
    assert html.count("ds-btn--primary") == 1
    assert "student-hero-greeting" not in html
    assert "Study Sensei" not in html
    assert 'data-dashboard-panel="quick-actions"' not in html
    assert 'data-dashboard-panel="readiness"' not in html
    assert "welcome_modal" not in html
    assert "ds-mission-hero" in html or "ds-mission-panel" in html
    assert "design_system.css" in html or "ds-page" in html
    assert (
        "What should I do now?" in html
        or "What should I do next?" in html
        or "Ready for today's mission?" in html
        or "Welcome back" in html
        or "Good morning" in html
        or "Good afternoon" in html
        or "Good evening" in html
        or "Where you stand" in html
        or "Where you are, what to do today" in html
    )
    assert (
        "Today's Session" in html
        or "Today's Mission" in html
        or "Today&#39;s Mission" in html
        or "Continue Session" in html
        or ">Continue<" in html
    )
    assert "CS1 FR" in html


def test_mission_without_exam_label_is_not_empty(app, ctx):
    """RC-2026.07.29-06: live mission with topic must never render empty-exam."""
    home = home_vm(
        HomeSnapshot(
            student_id="1",
            examination_label="",
            has_recommendation=False,
            recommendation_title="",
            can_start_session=True,
            start_session=StartSessionActionSnapshot(
                label="Start Session",
                enabled=True,
                can_start=True,
                mission_id="23",
                session_id="",
                topic_title="Today's study focus",
            ),
        ),
        unified_journey=False,
    )
    # Simulate Twin empty examination while mission bridge is live.
    home = replace(home, examination_label="")
    with app.test_request_context("/student/"):
        page = StudentHomeService().build_home(_page(home))
    assert page.state == "mission"
    assert page.mission is not None
    assert page.mission.primary_kind == "start_form"
    assert "No exam selected" not in page.empty_reason


def test_demo_mission_stub_without_topic_stays_empty(app, ctx):
    """Bare Experience demo mission ids must not suppress the empty state."""
    home = home_vm(
        HomeSnapshot(
            student_id="1",
            examination_label="",
            has_recommendation=False,
            recommendation_title="",
            can_start_session=True,
            start_session=StartSessionActionSnapshot(
                label="Start Session",
                enabled=True,
                can_start=True,
                mission_id="mission-1",
                session_id="sess-1",
                topic_title="",
            ),
        ),
        unified_journey=False,
    )
    home = replace(home, examination_label="")
    with app.test_request_context("/student/"):
        page = StudentHomeService().build_home(_page(home))
    assert page.state == "empty"
    assert "No exam selected" in page.empty_reason


def test_plan_signal_without_ready_mission_is_quiet(app, ctx):
    """Active plan / mission id without a startable CTA → quiet, not empty."""
    home = home_vm(
        HomeSnapshot(
            student_id="1",
            examination_label="IFoA CM1",
            has_recommendation=False,
            recommendation_title="",
            can_start_session=False,
        ),
        unified_journey=False,
    )
    with app.test_request_context("/student/"):
        page = StudentHomeService().build_home(_page(home))
    assert page.state == "quiet"
    assert "No exam selected" not in page.empty_reason
    assert "session will be ready" in page.empty_reason.lower()


def test_known_mission_title_without_cta_is_mission_not_quiet(app, ctx):
    """Real mission chrome with CTA off must still show the hero (not preparing)."""
    home = home_vm(
        HomeSnapshot(
            student_id="1",
            examination_label="IFoA CM1",
            has_recommendation=True,
            recommendation_title="Study CM1 Leaf",
            can_start_session=False,
        ),
        unified_journey=False,
    )
    home = replace(
        home,
        primary_cta_enabled=False,
        primary_mission_title="Study CM1 Leaf",
        mission_id="42",
        completion_status_label="Ready to study",
    )
    with app.test_request_context("/student/"):
        page = StudentHomeService().build_home(_page(home))
    assert page.state == "mission"
    assert page.mission is not None
    assert "CM1 Leaf" in page.mission.title
    assert page.preparing_mission is False


def test_stage_a_ready_mission_surfaces_on_home(app, ctx, user):
    """Stage A MissionService row must win over quiet/preparing when VM is empty."""
    from datetime import date, timedelta

    from flask_login import login_user

    from app.models.curriculum import Curriculum, Topic
    from app.models.study_plan import StudyPlan, WeekPlan
    from app.services.planning_service import PlanningService

    curriculum = Curriculum(exam_name="IFoA CM1", version="2025", active=True)
    db.session.add(curriculum)
    db.session.flush()
    db.session.add(
        Topic(
            name="CM1 Leaf",
            curriculum_id=curriculum.id,
            order=1,
            recommended_minutes=60,
            active=True,
        )
    )
    plan = StudyPlan(
        user_id=user.id,
        curriculum_id=curriculum.id,
        curriculum_version=curriculum.version,
        exam_name="IFoA CM1",
        exam_sitting="April 2027",
        exam_date=date.today() + timedelta(days=180),
        weekday_study_minutes=120,
        weekend_study_minutes=180,
        current_stage="Chapter 1",
        study_preference="Mixed",
        target_grade="A",
        preferred_session_minutes=60,
        active=True,
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
    stage_a = PlanningService.generate_today_mission(user.id)
    assert stage_a is not None
    assert "CM1 Leaf" in stage_a.title

    # Experience chrome empty / CTA off — the historical quiet/preparing bug.
    home = home_vm(
        HomeSnapshot(
            student_id=str(user.id),
            examination_label="IFoA CM1",
            has_recommendation=False,
            recommendation_title="",
            can_start_session=False,
        ),
        unified_journey=False,
    )
    with app.test_request_context("/student/"):
        login_user(user)
        page = StudentHomeService().build_home(_page(home))
    assert page.state == "mission"
    assert page.mission is not None
    assert "CM1 Leaf" in page.mission.title
    assert page.mission.primary_kind == "start_form"
    assert page.preparing_mission is False


def test_stage_a_title_wins_over_polluted_experience_chrome(app, ctx, user):
    """Stale Experience title must not hide Stage A's ready mission title."""
    from datetime import date, timedelta

    from flask_login import login_user

    from app.models.curriculum import Curriculum, Topic
    from app.models.study_plan import StudyPlan, WeekPlan
    from app.services.planning_service import PlanningService

    curriculum = Curriculum(exam_name="IFoA CM1", version="2025", active=True)
    db.session.add(curriculum)
    db.session.flush()
    db.session.add(
        Topic(
            name="CM1 Leaf",
            curriculum_id=curriculum.id,
            order=1,
            recommended_minutes=60,
            active=True,
        )
    )
    plan = StudyPlan(
        user_id=user.id,
        curriculum_id=curriculum.id,
        curriculum_version=curriculum.version,
        exam_name="IFoA CM1",
        exam_sitting="April 2027",
        exam_date=date.today() + timedelta(days=180),
        weekday_study_minutes=120,
        weekend_study_minutes=180,
        current_stage="Chapter 1",
        study_preference="Mixed",
        target_grade="A",
        preferred_session_minutes=60,
        active=True,
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
    stage_a = PlanningService.generate_today_mission(user.id)
    assert stage_a is not None

    home = home_vm(
        HomeSnapshot(
            student_id=str(user.id),
            examination_label="IFoA CM1",
            has_recommendation=True,
            recommendation_title="Stale CS1 Topic From Store",
            can_start_session=True,
            start_session=StartSessionActionSnapshot(
                label="Start Session",
                enabled=True,
                can_start=True,
                mission_id="stale-demo",
                topic_title="Stale CS1 Topic From Store",
            ),
        ),
        unified_journey=False,
    )
    home = replace(
        home,
        primary_cta_enabled=True,
        primary_mission_title="Stale CS1 Topic From Store",
        mission_id="stale-demo",
    )
    with app.test_request_context("/student/"):
        login_user(user)
        page = StudentHomeService().build_home(_page(home))
    assert page.state == "mission"
    assert page.mission is not None
    assert "CM1 Leaf" in page.mission.title
    assert "Stale CS1" not in page.mission.title
    assert page.mission.mission_id == str(stage_a.id)


def test_runtime_c_complete_control_is_actionable_mission(app, ctx):
    """Runtime C home with complete_runtime_c must not fall into quiet."""
    home = home_vm(
        HomeSnapshot(
            student_id="1",
            examination_label="CS1 (CS1)",
            has_recommendation=True,
            recommendation_title="Study first topic",
            can_start_session=False,
        ),
        unified_journey=False,
    )
    home = replace(
        home,
        primary_cta_enabled=True,
        primary_cta_label="Confirm today's Mission",
        session_control="complete_runtime_c",
        session_control_label="Confirm today's Mission",
        mission_id="msn_test_runtime_c",
        primary_mission_title="Study first topic",
        completion_status_label="Ready to study",
        estimated_duration_label="30 min",
    )
    with app.test_request_context("/student/"):
        page = StudentHomeService().build_home(_page(home))
    assert page.state == "mission"
    assert page.mission is not None
    assert page.mission.primary_kind == "complete_runtime_c"
    assert page.mission.mission_id == "msn_test_runtime_c"
    assert "Confirm today's Mission" in page.mission.primary_label
