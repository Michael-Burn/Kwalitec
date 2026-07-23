"""Snapshot composition tests."""

from __future__ import annotations

from application.student_experience.home import (
    HomeId,
    SnapshotId,
    StudentHomeService,
)
from tests.application.student_experience.home.conftest import make_full_inputs


def test_build_snapshot_from_home(service: StudentHomeService) -> None:
    home = service.build_home(make_full_inputs(), home_id=HomeId("home-snap"))
    snapshot = service.build_snapshot(home, snapshot_id=SnapshotId("snap-001"))

    assert snapshot.snapshot_id.value == "snap-001"
    assert snapshot.student_id == home.student_id
    assert snapshot.focus_headline == home.todays_focus.headline
    assert snapshot.focus_mission_title == home.todays_focus.mission_title
    assert snapshot.completed_missions == home.progress.completed_missions
    assert snapshot.current_streak_days == home.momentum.current_streak_days
    assert snapshot.hours_studied == home.progress.hours_studied
    assert snapshot.exam_available is home.exam_readiness.available
    assert snapshot.exam_days_remaining == home.exam_readiness.days_remaining
    assert snapshot.insight_count == len(home.learning_insights.insights)
    assert snapshot.quick_action_count == len(home.quick_actions.actions)


def test_snapshot_id_defaults_deterministically(service: StudentHomeService) -> None:
    home = service.build_home(make_full_inputs(), home_id="home-abc")
    snapshot = service.build_snapshot(home)
    assert snapshot.snapshot_id.value == "snap:home-abc:20260723T120000"
