"""Statistics and achievement rendering for Student Dashboard 2.0 (V4-001)."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from application.pipeline import EducationalPipeline, PipelineResult
from presentation.dashboard import (
    AchievementMapper,
    DashboardPresenter,
    StatisticsMapper,
)
from presentation.design_system import StatisticTile
from tests.education_os.application.pipeline.test_educational_pipeline import (
    make_pipeline_request,
)


@pytest.fixture(scope="module")
def pipeline_result() -> PipelineResult:
    return EducationalPipeline().run(make_pipeline_request())


def test_statistics_mapper_forwards_study_statistics() -> None:
    statistics = SimpleNamespace(
        sessions_completed=4,
        total_minutes=120,
        concepts_practiced=6,
        evidence_count=9,
        mastery_label="developing",
        confidence_label="moderate",
        progress_percent=40,
        current_streak_days=3,
        longest_streak_days=5,
    )
    tiles = StatisticsMapper.map_learning_statistics(statistics=statistics)
    streak = StatisticsMapper.map_streak(statistics=statistics)

    labels = {tile.label for tile in tiles}
    assert "Sessions completed" in labels
    assert "Study minutes" in labels
    assert "Concepts tracked" in labels
    assert "Evidence records" in labels
    assert "Mastery posture" in labels
    assert "Confidence posture" in labels
    assert all(isinstance(tile, StatisticTile) for tile in tiles)
    assert streak.current_days == 3
    assert streak.longest_days == 5
    assert streak.tile is not None
    assert streak.tile.value == "3 days"


def test_statistics_mapper_reads_twin_and_evidence() -> None:
    twin = SimpleNamespace(
        concept_states=(object(), object(), object()),
        confidence=SimpleNamespace(overall=SimpleNamespace(value="high")),
        mastery=SimpleNamespace(band=SimpleNamespace(value="stable")),
        evidence_history=(object(), object()),
    )
    evidence = SimpleNamespace(
        student_id="s1",
        records=(object(), object(), object()),
        count=3,
    )
    tiles = StatisticsMapper.map_learning_statistics(
        twin=twin,
        evidence_history=evidence,
    )
    by_label = {tile.label: tile.value for tile in tiles}
    assert by_label["Concepts tracked"] == "3"
    assert by_label["Evidence records"] == "3"
    assert by_label["Mastery posture"] == "Stable"
    assert by_label["Confidence posture"] == "High"


def test_streak_forwards_student_experience(
    pipeline_result: PipelineResult,
) -> None:
    streak = StatisticsMapper.map_streak(result=pipeline_result)
    experience_streak = pipeline_result.student_experience.streak

    assert streak.current_days == experience_streak.current_days
    assert streak.longest_days == experience_streak.longest_days
    assert streak.detail == experience_streak.explanation
    assert streak.band_label


def test_achievement_mapper_renders_achievements() -> None:
    achievements = (
        SimpleNamespace(
            title="First mission",
            message="You completed your first mission.",
            kind=SimpleNamespace(value="first_mission"),
            sequence=1,
        ),
        SimpleNamespace(
            title="Three-day streak",
            message="You kept a three-day streak.",
            kind="streak_three",
            sequence=2,
        ),
    )
    views = AchievementMapper.map_achievements(achievements)

    assert len(views) == 2
    assert views[0].title == "First mission"
    assert views[0].kind_label == "First mission"
    assert views[0].card is not None
    assert views[0].badge is not None
    assert views[1].title == "Three-day streak"


def test_achievement_mapper_falls_back_to_pipeline(
    pipeline_result: PipelineResult,
) -> None:
    views = AchievementMapper.map_achievements(result=pipeline_result)
    source = pipeline_result.student_experience.achievements
    if source:
        assert len(views) == len(source)
        assert views[0].title == source[0].title
    else:
        assert views[0].title == "No achievements yet"


def test_presenter_composes_statistics_and_achievements(
    pipeline_result: PipelineResult,
) -> None:
    statistics = SimpleNamespace(
        sessions_completed=2,
        total_minutes=45,
        evidence_count=1,
        progress_percent=25,
        current_streak_days=1,
        longest_streak_days=1,
    )
    achievements = (
        SimpleNamespace(
            title="Plan progress",
            message="You made plan progress.",
            kind="plan_progress",
            sequence=1,
        ),
    )
    view = DashboardPresenter.present(
        pipeline_result,
        statistics=statistics,
        achievements=achievements,
    )

    assert view.learning_statistics == ()
    assert view.progress_bar.percent == 25.0
    assert view.current_streak.current_days == 1
    assert view.achievements[0].title == "Plan progress"
    assert view.hero.mission_title
    assert view.readiness.category_label


def test_empty_statistics_remain_null_safe() -> None:
    tiles = StatisticsMapper.map_learning_statistics()
    streak = StatisticsMapper.map_streak()
    achievements = AchievementMapper.map_achievements()

    assert tiles
    assert tiles[0].value == "Not available"
    assert streak.current_days == 0
    assert streak.detail
    assert achievements[0].title == "No achievements yet"
