"""Celebration moment tests for AI Learning Coach (XP-005)."""

from __future__ import annotations

from application.student_experience.coach import CelebrationKind, LearningCoachService
from tests.application.student_experience.coach.conftest import (
    make_empty_inputs,
    make_full_inputs,
    make_journey_snapshot,
)


def test_seven_day_streak_celebration(
    service: LearningCoachService,
) -> None:
    context = service.build_context(
        make_full_inputs(journey_snapshot=make_journey_snapshot(streak=7))
    )
    kinds = {moment.kind for moment in context.celebration_moments.moments}
    assert CelebrationKind.STUDY_STREAK in kinds
    streak = next(
        moment
        for moment in context.celebration_moments.moments
        if moment.kind is CelebrationKind.STUDY_STREAK
    )
    assert "seven" in streak.title.lower() or "7" in streak.title


def test_mastery_improved_celebration(
    service: LearningCoachService,
) -> None:
    context = service.build_context(make_full_inputs())
    kinds = {moment.kind for moment in context.celebration_moments.moments}
    assert CelebrationKind.MASTERY_IMPROVED in kinds


def test_first_revision_cycle_celebration(
    service: LearningCoachService,
) -> None:
    context = service.build_context(make_full_inputs())
    kinds = {moment.kind for moment in context.celebration_moments.moments}
    assert CelebrationKind.FIRST_REVISION_CYCLE in kinds


def test_empty_inputs_have_no_celebrations(
    service: LearningCoachService,
) -> None:
    context = service.build_context(make_empty_inputs())
    assert context.celebration_moments.moments == ()
