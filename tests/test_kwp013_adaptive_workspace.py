"""KWP-013 — Adaptive Study Workspace tests.

Presentation-only composition of Mission, Focus, Progress, Forecast,
Journey, and Quick Actions. No Educational Intelligence redesign.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from app.application.educational_memory.dto import (
    MILESTONE_TITLES,
    PATTERN_TITLES,
    LearningJourneyNarrative,
    LearningMilestone,
    LongitudinalPattern,
    MilestoneKind,
    PatternKind,
    TimelineEntry,
    TimelineEventKind,
)
from app.application.readiness_forecast.dto import (
    ForecastConfidence,
    ForecastLabel,
    ReadinessForecast,
    StudyTrajectory,
    TrendDirection,
)
from app.application.student_experience.dto.home_snapshot import (
    HomeSnapshot,
    StartSessionActionSnapshot,
)
from app.presentation.product_language import APPROVED_TERMS
from app.presentation.student.adaptive_workspace import compose_adaptive_workspace
from app.presentation.student.dto.adaptive_workspace import AdaptiveStudyWorkspace
from app.presentation.student.dto.student_home import (
    HomeMission,
    HomeStudyHealth,
    StudentHomePage,
)
from app.presentation.student.services.student_home_service import (
    StudentHomeService,
)
from app.presentation.student.view_models import (
    HistoryPageViewModel,
    HistorySessionViewModel,
    RevisionOptionViewModel,
    RevisionPageViewModel,
    StudentPageViewModel,
    StudentShellViewModel,
    home_vm,
)
from app.services.study_workspace_metrics import StudyWorkspaceMetrics

FOUNDER_ALPHA = Path(
    "app/founder/dashboard/templates/founder_dashboard/alpha_observability.html"
)
HOME_TMPL = Path("app/templates/student/home.html")

_FORBIDDEN = (
    "digital twin",
    "evidence authority",
    "pass probability",
    "guaranteed",
    "will definitely",
    "cognitive load",
    "overloaded",
    "badge",
    "leaderboard",
)


def _page(home_vm_obj, *, history=None, revision=None):
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


def _start_home(**kwargs):
    defaults = dict(
        student_id="1",
        examination_label="CS1 FR",
        has_recommendation=True,
        recommendation_title="Annuities",
        can_start_session=True,
        exam_readiness=0.45,
        exam_countdown_days=42,
        start_session=StartSessionActionSnapshot(
            label="Start Session",
            enabled=True,
            can_start=True,
            mission_id="m1",
            session_id="",
            estimated_minutes=70,
            topic_title="Annuities",
        ),
    )
    defaults.update(kwargs)
    return home_vm(HomeSnapshot(**defaults), unified_journey=False)


def _home_page(*, mission=True) -> StudentHomePage:
    m = None
    if mission:
        m = HomeMission(
            subject_name="CS1 FR",
            objective="Annuities",
            status_label="Ready · 70 minutes",
            why_now="Continue momentum from discount factors",
            after_completion="Return tomorrow to consolidate",
            primary_label="Start Today's Session",
            primary_kind="start_form",
            duration_label="70 minutes",
            mission_id="m1",
            title="Annuities",
            learning_objective="Strengthen annuities after discount factors",
        )
    return StudentHomePage(
        mission=m,
        learning_queue=(),
        recent_progress=(),
        examination=None,
        study_health=HomeStudyHealth(
            status_label="Strengthening",
            detail="Steady gains this week",
            tone="positive",
        ),
        quick_actions=(),
        deadlines=(),
        state="mission" if mission else "quiet",
        empty_reason="",
        empty_action_label="",
        empty_action_href="",
        page_question="Where you stand — and what to do today.",
        mission_section_title="Today's Mission",
        briefing=None,
        insights=(),
    )


def test_workspace_disabled_for_empty_home(app):
    with app.test_request_context("/"):
        page = StudentPageViewModel(
            shell=StudentShellViewModel(
                active_surface="home",
                active_label="Home",
                navigation=(),
                page_title="Home",
            ),
            home=None,
        )
        empty = StudentHomeService().build_home(None)
        ws = compose_adaptive_workspace(page, empty)
        assert ws.enabled is False


def test_morning_brief_greeting_and_duration(app):
    with app.test_request_context("/"):
        home_vm_obj = _start_home()
        page = _page(home_vm_obj)
        home = _home_page()
        evening = datetime(2026, 7, 30, 20, 0, tzinfo=UTC)
        ws = compose_adaptive_workspace(page, home, now=evening)
        assert ws.enabled is True
        assert ws.morning_brief is not None
        assert ws.morning_brief.greeting == "Good evening."
        assert "steady" in ws.morning_brief.momentum_line.lower()
        assert "70" in ws.morning_brief.estimated_study_label
        assert "Annuities" in ws.morning_brief.today_line


def test_current_focus_combines_topic_guidance(app):
    with app.test_request_context("/"):
        home_vm_obj = _start_home()
        revision = RevisionPageViewModel(
            primary=RevisionOptionViewModel(
                topic_title="Discount Factors",
                expected_benefit="Strengthen foundations",
                is_primary=True,
            ),
            has_revision=True,
            option_count=1,
        )
        # Mission focus stays Annuities; revision is complementary.
        page = _page(home_vm_obj, revision=revision)
        home = _home_page()
        ws = compose_adaptive_workspace(page, home)
        assert ws.current_focus is not None
        assert ws.current_focus.topic_title == "Annuities"
        assert ws.current_focus.has_focus is True
        assert ws.current_focus.guidance
        lowered = (
            ws.current_focus.guidance + " " + ws.current_focus.detail
        ).lower()
        for fragment in _FORBIDDEN:
            assert fragment not in lowered


def test_progress_narrative_prefers_memory_recovery(app, monkeypatch):
    narrative = LearningJourneyNarrative(
        headline="My Learning Journey",
        story_paragraphs=("You recovered well.",),
        patterns=(
            LongitudinalPattern(
                kind=PatternKind.REPEATED_SUCCESSFUL_RECOVERIES,
                title=PATTERN_TITLES[
                    PatternKind.REPEATED_SUCCESSFUL_RECOVERIES
                ],
                narrative=(
                    "You have recovered from your previous difficulties "
                    "with probability distributions."
                ),
                topics=("Probability Distributions",),
                occurrence_count=2,
            ),
        ),
        milestones=(),
        sitting_archives=(),
        sitting_count=3,
        topic_count=2,
        has_memory=True,
    )

    monkeypatch.setattr(
        "app.presentation.student.adaptive_workspace._journey_narrative",
        lambda **_kwargs: narrative,
    )
    monkeypatch.setattr(
        "app.presentation.student.adaptive_workspace._readiness_forecast",
        lambda **_kwargs: None,
    )
    monkeypatch.setattr(
        "app.presentation.student.adaptive_workspace._store_and_student",
        lambda: (None, "1"),
    )

    with app.test_request_context("/"):
        page = _page(_start_home())
        home = _home_page()
        ws = compose_adaptive_workspace(page, home)
        assert ws.progress_narrative is not None
        assert "recovered" in ws.progress_narrative.body.lower()
        assert "probability distributions" in ws.progress_narrative.body.lower()
        assert ws.progress_narrative.home_worthy is True


def test_progress_narrative_study_health_fallback_not_home_worthy(app, monkeypatch):
    """Study-health-only progress stays computable but must not surface on Home."""
    monkeypatch.setattr(
        "app.presentation.student.adaptive_workspace._journey_narrative",
        lambda **_kwargs: None,
    )
    monkeypatch.setattr(
        "app.presentation.student.adaptive_workspace._readiness_forecast",
        lambda **_kwargs: None,
    )
    monkeypatch.setattr(
        "app.presentation.student.adaptive_workspace._store_and_student",
        lambda: (None, "1"),
    )
    with app.test_request_context("/"):
        page = _page(_start_home())
        home = _home_page()
        ws = compose_adaptive_workspace(page, home)
        assert ws.progress_narrative is not None
        assert ws.progress_narrative.has_narrative is True
        assert "steady gains" in ws.progress_narrative.body.lower()
        assert ws.progress_narrative.home_worthy is False


def test_home_continuity_prefers_yesterday_over_momentum():
    from app.presentation.student.adaptive_workspace import home_continuity_line
    from app.presentation.student.dto.adaptive_workspace import (
        WorkspaceMorningBrief,
    )

    brief = WorkspaceMorningBrief(
        greeting="Good morning.",
        momentum_line="You are recovering well from earlier difficulties.",
        yesterday_line="Yesterday's session strengthened Discount Factors.",
        today_line="Today's session continues that momentum with Annuities.",
        has_brief=True,
    )
    assert home_continuity_line(brief) == (
        "Yesterday's session strengthened Discount Factors."
    )
    # Never invent filler when brief has only generic momentum.
    generic = WorkspaceMorningBrief(
        greeting="Good morning.",
        momentum_line="You are building exam readiness step by step.",
        has_brief=True,
    )
    assert home_continuity_line(generic, fallback="") == ""
    assert home_continuity_line(generic, fallback="You left off on Annuities.") == (
        "You left off on Annuities."
    )
    # Memory-backed momentum is allowed when yesterday is empty.
    memory = WorkspaceMorningBrief(
        greeting="Good morning.",
        momentum_line="Your recent sittings show meaningful educational growth.",
        has_brief=True,
    )
    assert "educational growth" in home_continuity_line(memory).lower()


def test_forecast_reuses_kwp012_guidance(app, monkeypatch):
    forecast = ReadinessForecast(
        label=ForecastLabel.ON_TRACK,
        title="On Track",
        guidance=(
            "If your recent study pattern continues, you are likely to "
            "reach Ready for Revision before your scheduled sitting."
        ),
        explanation="Deterministic projection from recent sittings.",
        trajectory=StudyTrajectory(
            current_trend=TrendDirection.IMPROVING,
            current_trend_title="Improving",
            projected_readiness_stage="Ready for Revision",
            projected_readiness_ratio=0.82,
            key_assumptions=("Recent pattern continues",),
            influential_factors=("Consistency",),
            confidence=ForecastConfidence.ESTABLISHED,
            confidence_title="Established",
        ),
        has_forecast=True,
    )
    monkeypatch.setattr(
        "app.presentation.student.adaptive_workspace._readiness_forecast",
        lambda **_kwargs: forecast,
    )
    monkeypatch.setattr(
        "app.presentation.student.adaptive_workspace._journey_narrative",
        lambda **_kwargs: None,
    )
    monkeypatch.setattr(
        "app.presentation.student.adaptive_workspace._store_and_student",
        lambda: (None, "1"),
    )

    with app.test_request_context("/"):
        page = _page(_start_home())
        home = _home_page()
        ws = compose_adaptive_workspace(page, home)
        assert ws.forecast is not None
        assert ws.forecast.has_forecast is True
        assert ws.forecast.title == "On Track"
        assert "Ready for Revision" in ws.forecast.guidance
        assert "pass probability" not in ws.forecast.guidance.lower()


def test_journey_highlights_one_of_each(app, monkeypatch):
    narrative = LearningJourneyNarrative(
        headline="My Learning Journey",
        story_paragraphs=("Growth continues.",),
        patterns=(
            LongitudinalPattern(
                kind=PatternKind.IMPROVING_CONSISTENCY,
                title=PATTERN_TITLES[PatternKind.IMPROVING_CONSISTENCY],
                narrative="Recent sessions suggest stronger consistency.",
                topics=(),
                occurrence_count=2,
            ),
        ),
        milestones=(
            LearningMilestone(
                kind=MilestoneKind.FIRST_SUCCESSFUL_RECOVERY,
                title=MILESTONE_TITLES[
                    MilestoneKind.FIRST_SUCCESSFUL_RECOVERY
                ],
                narrative="First successful recovery on Discount Factors.",
                topic_title="Discount Factors",
                session_id="s1",
                recorded_at="2026-01-02T10:00:00+00:00",
            ),
        ),
        timeline=(
            TimelineEntry(
                kind=TimelineEventKind.UNDERSTANDING_IMPROVED,
                title="Understanding improved",
                body="Understanding of Annuities improved.",
                topic_title="Annuities",
                session_id="s2",
                recorded_at="2026-01-03T10:00:00+00:00",
            ),
        ),
        sitting_archives=(),
        sitting_count=3,
        topic_count=2,
        has_memory=True,
    )
    monkeypatch.setattr(
        "app.presentation.student.adaptive_workspace._journey_narrative",
        lambda **_kwargs: narrative,
    )
    monkeypatch.setattr(
        "app.presentation.student.adaptive_workspace._readiness_forecast",
        lambda **_kwargs: None,
    )
    monkeypatch.setattr(
        "app.presentation.student.adaptive_workspace._store_and_student",
        lambda: (None, "1"),
    )

    with app.test_request_context("/"):
        page = _page(_start_home())
        home = _home_page()
        ws = compose_adaptive_workspace(page, home)
        assert ws.journey_highlights is not None
        assert "recovery" in ws.journey_highlights.milestone.lower()
        assert "consistency" in ws.journey_highlights.pattern.lower()
        assert "annuities" in ws.journey_highlights.improvement.lower()


def test_quick_actions_include_mandated_set(app, monkeypatch):
    monkeypatch.setattr(
        "app.presentation.student.adaptive_workspace._journey_narrative",
        lambda **_kwargs: None,
    )
    monkeypatch.setattr(
        "app.presentation.student.adaptive_workspace._readiness_forecast",
        lambda **_kwargs: None,
    )
    monkeypatch.setattr(
        "app.presentation.student.adaptive_workspace._store_and_student",
        lambda: (None, "1"),
    )
    history = HistoryPageViewModel(
        sessions=(
            HistorySessionViewModel(
                session_id="sess-y",
                topic_title="Discount Factors",
                sitting_report_href="/session/sess-y/complete",
            ),
        ),
        session_count=1,
    )
    revision = RevisionPageViewModel(
        primary=RevisionOptionViewModel(
            topic_title="Discount Factors",
            is_primary=True,
        ),
        has_revision=True,
        option_count=1,
    )

    with app.test_request_context("/"):
        page = _page(_start_home(), history=history, revision=revision)
        home = _home_page()
        ws = compose_adaptive_workspace(page, home)
        labels = [a.label for a in ws.quick_actions]
        # UX-001: Start/Continue lives on the mission hero, not Quick Actions.
        assert not any("Begin" in label or "Start" in label for label in labels)
        assert "Review Yesterday" in labels
        assert "Resume Revision" in labels
        assert "View My Learning Journey" in labels
        # Forecast Quick Action only when a forecast projection exists (V1S-005).
        assert "Curriculum Map" in labels


def test_home_service_attaches_workspace(app):
    with app.test_request_context("/"):
        page = _page(_start_home())
        built = StudentHomeService().build_home(page)
        assert built.workspace is not None
        assert isinstance(built.workspace, AdaptiveStudyWorkspace)
        assert built.workspace.enabled is True
        assert built.mission_section_title == "Today's Mission"
        assert "what should i do now" in built.page_question.lower()
        assert built.greeting


def test_home_template_has_workspace_layout_markers():
    text = HOME_TMPL.read_text(encoding="utf-8")
    for marker in (
        'data-kwp="013"',
        'data-workspace-section="greeting"',
        'data-workspace-section="todays-mission"',
        'data-workspace-section="why-this-matters"',
        'data-workspace-section="recent-progress"',
        'data-workspace-section="study-signals"',
        'data-workspace-section="quick-actions"',
        'data-px004="continuity"',
        "Why this topic matters",
        "Recent progress",
    ):
        assert marker in text
    # UX-001: Session/Journey-exclusive overload stays off Home default view.
    for removed in (
        'data-workspace-section="morning-brief"',
        'data-workspace-section="session-plan"',
        'data-workspace-section="current-focus"',
        'data-workspace-section="forecast"',
        'data-workspace-section="learning-journey"',
        'data-workspace-section="tomorrow-preview"',
        "015-learning-episode",
        "checkpoint_prompt",
        "reflection_prompt",
    ):
        assert removed not in text


def test_home_html_shows_continuity_and_disclosures_when_supported(app, monkeypatch):
    """Returning student with history: continuity + two disclosures appear."""
    from dataclasses import replace

    from flask import render_template

    from app.presentation.student.dto.adaptive_workspace import (
        AdaptiveStudyWorkspace,
        WorkspaceCurrentFocus,
        WorkspaceMorningBrief,
        WorkspaceProgressNarrative,
    )

    narrative = LearningJourneyNarrative(
        headline="My Learning Journey",
        story_paragraphs=("You recovered well.",),
        patterns=(
            LongitudinalPattern(
                kind=PatternKind.REPEATED_SUCCESSFUL_RECOVERIES,
                title=PATTERN_TITLES[
                    PatternKind.REPEATED_SUCCESSFUL_RECOVERIES
                ],
                narrative=(
                    "You have recovered from your previous difficulties "
                    "with probability distributions."
                ),
                topics=("Probability Distributions",),
                occurrence_count=2,
            ),
        ),
        milestones=(),
        sitting_archives=(),
        sitting_count=3,
        topic_count=2,
        has_memory=True,
    )
    monkeypatch.setattr(
        "app.presentation.student.adaptive_workspace._journey_narrative",
        lambda **_kwargs: narrative,
    )
    monkeypatch.setattr(
        "app.presentation.student.adaptive_workspace._readiness_forecast",
        lambda **_kwargs: None,
    )
    monkeypatch.setattr(
        "app.presentation.student.adaptive_workspace._store_and_student",
        lambda: (None, "1"),
    )
    history = HistoryPageViewModel(
        sessions=(
            HistorySessionViewModel(
                session_id="sess-y",
                topic_title="Discount Factors",
            ),
        ),
        session_count=1,
    )
    with app.test_request_context("/student/"):
        page = _page(_start_home(), history=history)
        built = StudentHomeService().build_home(page)
        # Inject curriculum_why (engine-dependent) while keeping real continuity
        # and memory-backed progress from composition.
        assert built.workspace is not None
        focus = built.workspace.current_focus or WorkspaceCurrentFocus(
            topic_title="Annuities",
            has_focus=True,
        )
        focus = replace(
            focus,
            curriculum_why=(
                "Annuities relies heavily on Discount Factors. "
                "Strengthening Discount Factors is expected to improve "
                "your understanding of Annuities."
            ),
        )
        ws = replace(
            built.workspace,
            current_focus=focus,
            morning_brief=WorkspaceMorningBrief(
                greeting="Good morning.",
                yesterday_line="Yesterday's session strengthened Discount Factors.",
                momentum_line="You are recovering well from earlier difficulties.",
                today_line="Today's session continues that momentum with Annuities.",
                has_brief=True,
            ),
            progress_narrative=WorkspaceProgressNarrative(
                headline="Recovery in progress",
                body=(
                    "You have recovered from your previous difficulties "
                    "with probability distributions."
                ),
                has_narrative=True,
                home_worthy=True,
            ),
        )
        home = replace(
            built,
            workspace=ws,
            continuity_line="Yesterday's session strengthened Discount Factors.",
        )
        html = render_template("student/home.html", page=page, home=home, form=None)

    assert 'data-px004="continuity"' in html
    assert "Yesterday" in html and "Discount Factors" in html
    assert "Yesterday&#39;s session strengthened Discount Factors." in html
    assert 'data-workspace-section="why-this-matters"' in html
    assert "Why this topic matters" in html
    assert "Annuities relies heavily on Discount Factors" in html
    assert 'data-workspace-section="recent-progress"' in html
    assert "probability distributions" in html.lower()
    # Session-exclusive fields remain absent from Home HTML.
    assert 'data-workspace-section="session-plan"' not in html
    assert 'data-workspace-section="forecast"' not in html
    assert 'data-workspace-section="learning-journey"' not in html
    assert "015-learning-episode" not in html
    assert "checkpoint_prompt" not in html
    assert "reflection_prompt" not in html
    assert 'data-workspace-section="morning-brief"' not in html
    assert 'data-workspace-section="current-focus"' not in html


def test_home_html_omits_empty_disclosures_and_generic_continuity(app, monkeypatch):
    """Fresh / day-zero student: no empty disclosure chrome, no filler continuity."""
    from dataclasses import replace

    from flask import render_template

    from app.presentation.student.dto.adaptive_workspace import (
        AdaptiveStudyWorkspace,
        WorkspaceCurrentFocus,
        WorkspaceMorningBrief,
        WorkspaceProgressNarrative,
    )

    monkeypatch.setattr(
        "app.presentation.student.adaptive_workspace._journey_narrative",
        lambda **_kwargs: None,
    )
    monkeypatch.setattr(
        "app.presentation.student.adaptive_workspace._readiness_forecast",
        lambda **_kwargs: None,
    )
    monkeypatch.setattr(
        "app.presentation.student.adaptive_workspace._store_and_student",
        lambda: (None, "1"),
    )
    with app.test_request_context("/student/"):
        page = _page(_start_home())
        built = StudentHomeService().build_home(page)
        assert built.workspace is not None
        # Explicit empty curriculum_why + non-home-worthy progress + generic momentum.
        focus = WorkspaceCurrentFocus(
            topic_title="Annuities",
            guidance="Practice steadily.",
            curriculum_why="",
            has_focus=True,
        )
        ws = replace(
            built.workspace or AdaptiveStudyWorkspace(enabled=True),
            current_focus=focus,
            morning_brief=WorkspaceMorningBrief(
                greeting="Good morning.",
                momentum_line="You are building exam readiness step by step.",
                yesterday_line="",
                has_brief=True,
            ),
            progress_narrative=WorkspaceProgressNarrative(
                headline="Strengthening",
                body="Steady gains this week",
                has_narrative=True,
                home_worthy=False,
            ),
            mission_composition=None,
        )
        home = replace(
            built,
            workspace=ws,
            continuity_line="",
            density_mode="day_zero",
            show_progress_strip=False,
        )
        html = render_template("student/home.html", page=page, home=home, form=None)

    assert 'data-workspace-section="why-this-matters"' not in html
    assert "Why this topic matters" not in html
    assert 'data-workspace-section="recent-progress"' not in html
    # No continuity paragraph when line is empty (greeting support fallback may
    # still show mission-ready copy — that is not the educational continuity line).
    assert 'data-px004="continuity"' not in html
    assert "You are building exam readiness step by step." not in html
    assert "Steady gains this week" not in html


def test_founder_workspace_metrics_and_template():
    snap = StudyWorkspaceMetrics.from_event_counts(
        {
            "dashboard_opened": 10,
            "workspace_opened": 8,
            "mission_started": 5,
            "mission_completed": 4,
            "learning_journey_opened": 3,
            "forecast_viewed": 2,
            "provenance_expanded": 1,
            "workspace_interaction": 6,
        },
        unique_learners=5,
    )
    opaque = snap.to_opaque()
    assert opaque["workspace_opens"] == 18
    assert opaque["mission_completions"] == 4
    assert opaque["journey_opens"] == 3
    assert opaque["forecast_views"] == 2
    assert opaque["insight_usefulness_signals"] >= 1
    assert 0.0 <= opaque["mission_completion_rate"] <= 1.0

    text = FOUNDER_ALPHA.read_text(encoding="utf-8")
    assert "Adaptive Study Workspace" in text
    assert "study_workspace" in text
    assert "Workspace opens" in text


def test_approved_product_terms_include_workspace():
    for term in (
        "Adaptive Study Workspace",
        "Morning Brief",
        "Current Focus",
        "Session Plan",
    ):
        assert term in APPROVED_TERMS


def test_workspace_scrub_forbids_internal_vocabulary():
    from app.presentation.student.adaptive_workspace import _scrub

    cleaned = _scrub(
        "Digital Twin suggests pass probability is guaranteed."
    )
    lowered = cleaned.lower()
    assert "digital twin" not in lowered
    assert "pass probability" not in lowered
    assert "guaranteed" not in lowered
