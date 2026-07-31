"""KWP-006 — Exam Week Briefing & Home Experience tests.

Presentation packaging only — no Progress / Twin / Evidence / Mission redesign.
"""

from __future__ import annotations

from dataclasses import replace

from app.application.student_experience.dto.history_snapshot import (
    AchievementSnapshot,
)
from app.application.student_experience.dto.home_snapshot import (
    HomeSnapshot,
    StartSessionActionSnapshot,
)
from app.presentation.product_language import APPROVED_TERMS
from app.presentation.student.exam_week_briefing import (
    build_exam_week_briefing,
    build_home_insights,
    readiness_stage_label,
)
from app.presentation.student.services.student_home_service import (
    StudentHomeService,
)
from app.presentation.student.view_models import (
    HistoryPageViewModel,
    HistorySessionViewModel,
    JourneyPageViewModel,
    JourneyTopicViewModel,
    ProfilePageViewModel,
    ReadinessCardViewModel,
    RevisionOptionViewModel,
    RevisionPageViewModel,
    StudentPageViewModel,
    StudentShellViewModel,
    home_vm,
)


def _page(home_vm_obj, *, history=None, journey=None, revision=None, profile=None):
    return StudentPageViewModel(
        shell=StudentShellViewModel(
            active_surface="home",
            active_label="Home",
            navigation=(),
            page_title="Home",
        ),
        home=home_vm_obj,
        history=history,
        journey=journey,
        revision=revision,
        profile=profile,
    )


def _start_home(**kwargs):
    defaults = dict(
        student_id="1",
        examination_label="CS1 FR",
        has_recommendation=True,
        recommendation_title="Present Value",
        can_start_session=True,
        exam_readiness=0.45,
        exam_countdown_days=42,
        start_session=StartSessionActionSnapshot(
            label="Start Session",
            enabled=True,
            can_start=True,
            mission_id="m1",
            session_id="",
            estimated_minutes=25,
            topic_title="Present Value",
        ),
    )
    defaults.update(kwargs)
    return home_vm(HomeSnapshot(**defaults), unified_journey=False)


# --- Readiness stage language -------------------------------------------------


class TestReadinessStageLanguage:
    def test_stage_bands(self):
        assert readiness_stage_label(0.05) == "Building"
        assert readiness_stage_label(0.25) == "Developing"
        assert readiness_stage_label(0.45) == "Strengthening"
        assert readiness_stage_label(0.70) == "Ready for Revision"
        assert readiness_stage_label(0.90) == "Ready for Assessment"

    def test_percent_inputs(self):
        assert readiness_stage_label(45.0) == "Strengthening"
        assert readiness_stage_label(None) == "Building"

    def test_home_vm_prefers_stage_over_generic_label(self):
        vm = _start_home(exam_readiness=0.45, exam_readiness_label="Exam Readiness")
        assert vm.readiness.readiness_label == "Strengthening"
        assert vm.readiness.readiness_percent_label == "45%"


# --- Exam Week Briefing ------------------------------------------------------


class TestExamWeekBriefing:
    def test_briefing_from_history_and_revision(self):
        home = _start_home()
        history = HistoryPageViewModel(
            sessions=(
                HistorySessionViewModel(
                    session_id="s1",
                    topic_title="Discount Factors",
                    completed_at="Yesterday",
                ),
            ),
            mastered_topics=("Present Value", "Discount Factors"),
            revision_history=("Annuities",),
            session_count=5,
            mastered_count=2,
        )
        revision = RevisionPageViewModel(
            primary=RevisionOptionViewModel(
                option_id="r1",
                topic_title="Annuities",
                priority_label="Strengthen",
                expected_benefit="Reinforce cash-flow timing",
                is_primary=True,
            ),
            has_revision=True,
            option_count=1,
            primary_cta_enabled=True,
        )
        profile = ProfilePageViewModel(streak_label="6 days")
        briefing = build_exam_week_briefing(
            home=home,
            history=history,
            revision=revision,
            profile=profile,
        )
        assert briefing.has_briefing is True
        assert "Present Value" in briefing.strengthened
        assert "Annuities" in briefing.needs_reinforcement
        assert briefing.consistency_label == "Excellent"
        assert briefing.recommended_focus == "Annuities"
        assert "CMP" not in briefing.summary_line
        assert "question text" not in briefing.summary_line.lower()

    def test_empty_when_no_signal(self):
        home = home_vm(
            HomeSnapshot(student_id="1"),
            unified_journey=False,
        )
        briefing = build_exam_week_briefing(home=home)
        assert briefing.has_briefing is False

    def test_home_service_surfaces_briefing(self, app, ctx):
        home = _start_home()
        home = replace(
            home,
            readiness=ReadinessCardViewModel(
                readiness_label="Strengthening",
                readiness_percent_label="45%",
                has_readiness=True,
            ),
        )
        history = HistoryPageViewModel(
            mastered_topics=("Present Value",),
            sessions=(
                HistorySessionViewModel(
                    session_id="s1",
                    topic_title="Present Value",
                    completed_at="Mon",
                ),
            ),
            session_count=3,
        )
        journey = JourneyPageViewModel(
            examination_label="CS1 FR",
            current=JourneyTopicViewModel(
                topic_id="t1",
                title="Present Value",
                status_label="Current",
            ),
            progress_percent=40,
            progress_label="40% through your syllabus",
            needs_attention=(
                JourneyTopicViewModel(
                    topic_id="t2",
                    title="Annuities",
                    status_label="Strengthen",
                ),
            ),
            up_next=JourneyTopicViewModel(
                topic_id="t3",
                title="Chapter 12",
                status_label="Upcoming",
            ),
        )
        with app.test_request_context("/student/"):
            page = StudentHomeService().build_home(
                _page(home, history=history, journey=journey)
            )
        assert page.briefing is not None
        assert page.briefing.has_briefing is True
        assert "Present Value" in page.briefing.strengthened
        assert "Annuities" in page.briefing.needs_reinforcement
        assert page.syllabus_position
        assert "Present Value" in page.syllabus_position
        assert page.page_question.startswith("Where you are")
        kinds = {i.kind for i in page.insights}
        assert "position" in kinds or page.syllabus_position
        assert "changed" in kinds or "next" in kinds or "weak" in kinds
        # KWP-013 — Adaptive Study Workspace attaches without dropping briefing.
        assert page.workspace is not None
        assert page.workspace.enabled is True


# --- Home Insights -----------------------------------------------------------


class TestHomeInsights:
    def test_insights_cover_command_centre_questions(self):
        home = _start_home()
        history = HistoryPageViewModel(
            sessions=(
                HistorySessionViewModel(
                    session_id="s1",
                    topic_title="Discount Factors",
                    completed_at="Yesterday",
                ),
            ),
            mastered_topics=("Present Value",),
            achievements=(
                AchievementSnapshot(
                    achievement_id="a1",
                    title="Three Sessions complete",
                    description="Consistent study this week",
                ),
            ),
            session_count=3,
        )
        journey = JourneyPageViewModel(
            current=JourneyTopicViewModel(
                topic_id="t1",
                title="Present Value",
                status_label="Current",
            ),
            up_next=JourneyTopicViewModel(
                topic_id="t2",
                title="Annuities",
                status_label="Upcoming",
            ),
            progress_label="Building coverage",
            needs_attention=(
                JourneyTopicViewModel(
                    topic_id="t3",
                    title="Annuities",
                    status_label="Strengthen",
                ),
            ),
        )
        briefing = build_exam_week_briefing(
            home=home, history=history, journey=journey
        )
        insights = build_home_insights(
            home=home,
            history=history,
            journey=journey,
            briefing=briefing,
        )
        labels = {c.label for c in insights}
        assert "Where you are" in labels
        assert "Since last Session" in labels
        assert "Needs attention" in labels
        assert "Recent achievement" in labels
        assert any(c.kind == "next" for c in insights)

    def test_template_renders_briefing_and_insights(self, app, ctx):
        from flask import render_template

        home = _start_home()
        history = HistoryPageViewModel(
            mastered_topics=("Present Value", "Discount Factors"),
            sessions=(
                HistorySessionViewModel(
                    session_id="s1",
                    topic_title="Present Value",
                    completed_at="Tue",
                ),
            ),
            session_count=4,
        )
        journey = JourneyPageViewModel(
            current=JourneyTopicViewModel(
                topic_id="t1",
                title="Present Value",
                status_label="Current",
            ),
            needs_attention=(
                JourneyTopicViewModel(
                    topic_id="t2",
                    title="Annuities",
                    status_label="Strengthen",
                ),
            ),
            progress_label="On track",
        )
        page = _page(home, history=history, journey=journey)
        with app.test_request_context("/student/"):
            built = StudentHomeService().build_home(page)
            html = render_template(
                "student/home.html",
                page=page,
                home=built,
                form=None,
            )
        assert "Present Value" in html
        assert "Annuities" in html
        # KWP-013 — Home is Adaptive Study Workspace; briefing data still
        # projects into Current Focus / Morning Brief rather than a separate
        # "This Week" card.
        assert 'data-kwp="013"' in html
        assert 'data-workspace="adaptive-study"' in html
        assert 'data-workspace-section="morning-brief"' in html
        assert 'data-workspace-section="current-focus"' in html
        assert "digital twin" not in html.lower()
        assert "evidence authority" not in html.lower()
        assert "progress engine" not in html.lower()
        assert built.briefing is not None
        assert built.briefing.has_briefing is True
        assert "Annuities" in (built.briefing.needs_reinforcement or ())


# --- Product language --------------------------------------------------------


def test_exam_week_briefing_approved_term():
    assert "Exam Week Briefing" in APPROVED_TERMS


def test_study_health_uses_stage_not_percent(app, ctx):
    home = _start_home(exam_readiness=0.72)
    with app.test_request_context("/student/"):
        page = StudentHomeService().build_home(_page(home))
    assert page.study_health is not None
    assert "%" not in page.study_health.status_label
    assert page.study_health.status_label == "Ready for Revision"
