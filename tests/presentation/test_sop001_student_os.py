"""SOP-001 — Student Operating System premium experience contracts."""

from __future__ import annotations

from pathlib import Path

from flask import render_template

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.history_snapshot import (
    AchievementSnapshot,
    CompletedSessionSnapshot,
    HistorySnapshot,
    ReadinessPointSnapshot,
)
from app.application.student_experience.dto.home_snapshot import (
    HomeSnapshot,
    StartSessionActionSnapshot,
)
from app.application.student_experience.dto.journey_snapshot import (
    JourneySnapshot,
    JourneyTopicSnapshot,
)
from app.application.student_experience.dto.revision_snapshot import (
    RevisionOptionSnapshot,
    RevisionSnapshot,
)
from app.presentation.student.services.student_home_service import (
    StudentHomeService,
)
from app.presentation.student.view_models import (
    StudentPageViewModel,
    StudentShellViewModel,
    history_vm,
    home_vm,
    journey_vm,
    revision_vm,
)

ROOT = Path(__file__).resolve().parents[2]


def _shell(title: str, surface: str, question: str) -> StudentShellViewModel:
    return StudentShellViewModel(
        active_surface=surface,
        active_label=title,
        navigation=(),
        page_title=title,
        page_description=question,
    )


def test_home_command_centre_sections(app, ctx):
    snap = HomeSnapshot(
        student_id="stu-sop",
        greeting="Welcome back",
        examination_label="IFoA CM1",
        exam_countdown_days=42,
        exam_readiness=0.42,
        exam_readiness_label="Building",
        recommendation_title="Cash flows",
        recommendation_summary="Practice cash flows.",
        estimated_study_minutes=25,
        has_recommendation=True,
        can_start_session=True,
        start_session=StartSessionActionSnapshot(
            label="Start Session",
            enabled=True,
            can_start=True,
            mission_id="m1",
            topic_title="Cash flows",
            estimated_minutes=25,
        ),
    )
    page = StudentPageViewModel(
        shell=_shell("Home", "home", "What should I do next?"),
        home=home_vm(snap, unified_journey=False),
    )
    with app.test_request_context("/student/"):
        home = StudentHomeService().build_home(page)
        html = render_template(
            "student/home.html",
            page=page,
            home=home,
            form=None,
        )
    assert home.examination is not None
    assert home.examination.label == "IFoA CM1"
    assert home.study_health is not None
    assert home.recent_progress == ()
    assert home.signals is not None
    assert home.signals.countdown_label or home.deadlines
    assert "What should I do next?" in html
    assert "Today's Session" in html or "Today's Mission" in html or "ds-mission-panel" in html
    assert "Study Health" in html
    assert "Exam countdown" in html or "Upcoming" in html
    assert "Today&#39;s Mission" in html or "Continue Session" in html
    assert "ds-os-home" in html
    assert 'data-dashboard-panel="readiness"' not in html
    assert html.count("ds-btn--primary") <= 1


def test_journey_answers_where_am_i(app, ctx):
    snap = JourneySnapshot(
        student_id="stu-sop",
        examination_label="IFoA CM1",
        progress_percent=35,
        current_topic=JourneyTopicSnapshot(
            topic_id="t1",
            title="Cash flows",
            status_label="In progress",
        ),
        completed_topics=(
            JourneyTopicSnapshot(
                topic_id="t0",
                title="Time value",
                status_label="Complete",
            ),
        ),
        upcoming_topics=(
            JourneyTopicSnapshot(topic_id="t2", title="Annuities"),
            JourneyTopicSnapshot(topic_id="t3", title="Loans"),
        ),
    )
    page = StudentPageViewModel(
        shell=_shell("Journey", "journey", "Where am I?"),
        journey=journey_vm(snap),
    )
    with app.test_request_context("/student/journey"):
        html = render_template("student/journey.html", page=page)
    assert "Where am I?" in html
    assert "Cash flows" in html
    assert "Annuities" in html
    assert "Completed work" in html
    assert "ds-os-journey" in html
    assert "ds-os-progress" in html


def test_history_is_definitive_archive(app, ctx):
    snap = HistorySnapshot(
        student_id="stu-sop",
        total_study_minutes=120,
        session_count=2,
        completed_sessions=(
            CompletedSessionSnapshot(
                session_id="s1",
                topic_title="Cash flows",
                completed_at="Yesterday",
                study_minutes=45,
            ),
        ),
        readiness_progression=(
            ReadinessPointSnapshot(
                recorded_at="Week 1",
                exam_readiness=0.3,
                label="30%",
            ),
        ),
        mastered_topics=("Time value",),
        recent_achievements=(
            AchievementSnapshot(
                achievement_id="a1",
                title="First session",
                description="Completed your first study session.",
                earned_at="Yesterday",
            ),
        ),
    )
    page = StudentPageViewModel(
        shell=_shell("History", "history", "What have I accomplished?"),
        history=history_vm(snap),
    )
    with app.test_request_context("/student/history"):
        html = render_template("student/history.html", page=page)
    assert "What have I accomplished?" in html
    assert "Study time" in html
    assert "Sessions" in html
    assert "Completed Topics" in html
    assert "Milestones" in html
    assert "Readiness Trends" in html
    assert "ds-os-history" in html


def test_revision_recommends_rather_than_lists(app, ctx):
    snap = RevisionSnapshot(
        student_id="stu-sop",
        has_revision=True,
        option_count=2,
        primary=RevisionOptionSnapshot(
            option_id="r1",
            topic_title="Discounting",
            priority_label="Weak topic",
            estimated_study_minutes=20,
            expected_benefit="Restore exam-critical fluency",
            is_primary=True,
            explanation=ExplanationSnapshot(
                summary="Revise discounting",
                why_recommended="Recent practice showed forgotten concepts.",
                confidence_label="Suggested",
                expected_benefit="Restore exam-critical fluency",
                is_complete=True,
            ),
        ),
        alternatives=(
            RevisionOptionSnapshot(
                option_id="r2",
                topic_title="Annuities",
                priority_label="Overdue review",
                estimated_study_minutes=15,
                expected_benefit="Prevent decay",
            ),
        ),
    )
    page = StudentPageViewModel(
        shell=_shell("Revision", "revision", "What deserves my attention?"),
        revision=revision_vm(snap),
    )
    with app.test_request_context("/student/revision"):
        html = render_template(
            "student/revision.html",
            page=page,
            form=None,
        )
    assert "What deserves my attention?" in html
    assert "Revision support" in html
    assert "Discounting" in html
    assert "Also deserves attention" in html
    assert "ds-os-revision" in html


def test_design_system_os_styles_use_semantic_tokens():
    css = (ROOT / "app/static/css/design_system.css").read_text(encoding="utf-8")
    assert ".ds-os-exam" in css
    assert ".ds-os-health" in css
    assert ".ds-os-path" in css
    assert ".ds-os-recommend" in css
    sop_block = css.split("SOP-001 Student OS", 1)[1]
    assert "var(--primary)" in sop_block
    assert "#" not in sop_block.split("@media", 1)[0]
