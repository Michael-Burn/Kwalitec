"""Learning Journey composition tests (XP-002)."""

from __future__ import annotations

from datetime import UTC, datetime

from application.student_experience.progress import (
    JourneyId,
    JourneyMilestoneKind,
    LearningJourneyService,
    ProvidedMilestone,
    TrajectoryLabel,
    TrendDirection,
)
from tests.application.student_experience.progress.conftest import (
    AS_OF,
    STUDENT_ID,
    FakeMilestoneProvider,
    RecordingJourneyPublisher,
    make_rich_inputs,
)


def test_build_journey_composes_all_sections(
    service: LearningJourneyService,
) -> None:
    journey = service.build_journey(
        make_rich_inputs(), journey_id=JourneyId("journey-001")
    )

    assert journey.student_id == STUDENT_ID
    assert journey.journey_id.value == "journey-001"
    assert journey.timeline.has_events is True
    assert journey.progress_overview.has_overview_data is True
    assert journey.growth.has_growth_data is True
    assert journey.consistency.has_consistency_data is True
    assert journey.study_habits.has_habits_data is True
    assert journey.milestones.has_milestones is True
    assert journey.learning_trends.has_trend_data is True
    assert journey.weekly_summary.week_end == AS_OF.date()
    assert journey.monthly_summary.month_end == AS_OF.date()


def test_journey_never_exposes_domain_type_names(
    service: LearningJourneyService,
) -> None:
    journey = service.build_journey(make_rich_inputs())
    blob = " ".join(
        [
            journey.progress_overview.trajectory_message,
            journey.progress_overview.weekly_growth_message,
            journey.progress_overview.learning_momentum_message,
            journey.consistency.consistency_message,
            journey.study_habits.preferred_study_time_message,
            journey.study_habits.mission_completion_quality_message,
            *(event.message for event in journey.timeline.events),
            *(milestone.message for milestone in journey.milestones.milestones),
            journey.learning_trends.mastery_trend_message,
            journey.weekly_summary.summary_message,
            journey.monthly_summary.summary_message,
        ]
    )
    for forbidden in (
        "MasteryAssessment",
        "RecommendationSet",
        "MissionPlan",
        "EducationalEvaluation",
        "StudySchedule",
        "MissionExecution",
        "ExecutionHistory",
        "HomeSnapshot",
    ):
        assert forbidden not in blob


def test_growth_uses_student_facing_language(
    service: LearningJourneyService,
) -> None:
    growth = service.summarise_growth(make_rich_inputs())
    assert growth.weekly_missions_completed >= 1
    assert "You've completed" in growth.weekly_growth_message
    assert "MissionExecution" not in growth.weekly_growth_message
    assert growth.mastery_trend is TrendDirection.IMPROVING


def test_refresh_journey_publishes() -> None:
    publisher = RecordingJourneyPublisher()
    service = LearningJourneyService(journey_publisher=publisher)
    journey = service.refresh_journey(
        make_rich_inputs(), journey_id="journey-refresh"
    )
    assert len(publisher.journeys) == 1
    assert len(publisher.snapshots) == 1
    assert publisher.journeys[0].journey_id.value == "journey-refresh"
    assert publisher.snapshots[0].student_id == journey.student_id


def test_milestones_from_provider() -> None:
    provider = FakeMilestoneProvider(
        (
            ProvidedMilestone(
                milestone_id="m1",
                kind=JourneyMilestoneKind.CUSTOM,
                title="Custom milestone",
                description="You unlocked a custom milestone.",
                reached_at=AS_OF,
            ),
        )
    )
    service = LearningJourneyService(milestone_provider=provider)
    journey = service.build_journey(make_rich_inputs())
    titles = {item.title for item in journey.milestones.milestones}
    assert "Custom milestone" in titles


def test_deterministic_journey_id_from_as_of(
    service: LearningJourneyService,
) -> None:
    inputs = make_rich_inputs(as_of=datetime(2026, 7, 23, 8, 0, tzinfo=UTC))
    journey = service.build_journey(inputs)
    assert journey.journey_id.value == "journey:student-001:20260723T080000"


def test_progress_overview_trajectory(
    service: LearningJourneyService,
) -> None:
    journey = service.build_journey(make_rich_inputs())
    assert journey.progress_overview.trajectory in {
        TrajectoryLabel.BUILDING,
        TrajectoryLabel.STEADY,
        TrajectoryLabel.ACCELERATING,
        TrajectoryLabel.JUST_STARTING,
    }
    assert journey.progress_overview.strongest_subject is not None
    assert journey.progress_overview.most_improved_competency is not None
