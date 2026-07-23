"""Null-safety coverage for Student Dashboard 2.0 mappers (V4-001)."""

from __future__ import annotations

from types import SimpleNamespace

from presentation.dashboard import (
    DashboardMapper,
    DashboardPresenter,
    MissionCardMapper,
    ProgressMapper,
    StatisticsMapper,
)


def test_mission_mapper_null_safe() -> None:
    card = MissionCardMapper.map_mission_card(None)
    reason = MissionCardMapper.map_mission_reason(None)

    assert card.title == "Today's Mission"
    assert card.body
    assert card.duration_label == "Duration not available"
    assert reason.body
    assert reason.title


def test_progress_mapper_null_safe() -> None:
    card = ProgressMapper.map_progress_card(None)
    bar = ProgressMapper.map_progress_bar(None)

    assert card.title == "Progress"
    assert card.body
    assert bar.percent == 0.0
    assert bar.label


def test_statistics_mapper_ignores_invalid_numbers() -> None:
    statistics = SimpleNamespace(
        sessions_completed="not-a-number",
        total_minutes=None,
        progress_percent=True,
        current_streak_days=-3,
    )
    tiles = StatisticsMapper.map_learning_statistics(statistics=statistics)
    streak = StatisticsMapper.map_streak(statistics=statistics)

    assert tiles
    assert streak.current_days == 0


def test_dashboard_mapper_null_safe() -> None:
    greeting_text, greeting = DashboardMapper.map_greeting(None)
    primary = DashboardMapper.map_primary_action(None)
    quick = DashboardMapper.map_quick_actions(None)
    upcoming = DashboardMapper.map_upcoming_sessions()
    header = DashboardMapper.map_header(greeting=greeting_text, mission_title="")

    assert greeting_text
    assert greeting.description == greeting_text
    assert primary.label == "Begin Session"
    assert quick
    assert upcoming[0].label == "No upcoming sessions"
    assert header.title == "Learning Dashboard"


def test_presenter_handles_partial_optional_inputs() -> None:
    twin = SimpleNamespace(display_name="Alex", concept_states=())
    evidence = SimpleNamespace(records=(), count=0)
    statistics = SimpleNamespace()
    view = DashboardPresenter.present(
        None,
        twin=twin,
        evidence_history=evidence,
        statistics=statistics,
        achievements=(),
    )

    assert "Alex" in view.greeting_text
    # Decision screen suppresses metric grids; mapper cargo stays available.
    assert view.learning_statistics == ()
    assert view.hero.greeting
    assert view.readiness.category_label
    assert view.achievements[0].title == "No achievements yet"
    assert view.upcoming_sessions
    assert view.upcoming_milestones
