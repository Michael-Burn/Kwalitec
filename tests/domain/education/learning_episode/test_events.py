"""Domain event tests for Learning Episode."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import ReflectionType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import LearningEpisodeId, ReflectionId
from domain.education.learning_episode import (
    EpisodeCompleted,
    EpisodeGoalId,
    EpisodeOutcomeId,
    EpisodeOutcomeKind,
    EpisodeStarted,
    EpisodeStepId,
    ReflectionRecorded,
)


class TestEpisodeStarted:
    def test_valid(self) -> None:
        event = EpisodeStarted(
            episode_id=LearningEpisodeId("ep-1"),
            teaching_goal_id=EpisodeGoalId("goal-1"),
            first_step_id=EpisodeStepId("step-1"),
        )
        assert event.episode_id.value == "ep-1"

    def test_frozen(self) -> None:
        event = EpisodeStarted(
            episode_id=LearningEpisodeId("ep-1"),
            teaching_goal_id=EpisodeGoalId("goal-1"),
            first_step_id=EpisodeStepId("step-1"),
        )
        with pytest.raises(Exception):
            event.episode_id = LearningEpisodeId("other")  # type: ignore[misc]

    def test_equality(self) -> None:
        a = EpisodeStarted(
            episode_id=LearningEpisodeId("ep-1"),
            teaching_goal_id=EpisodeGoalId("goal-1"),
            first_step_id=EpisodeStepId("step-1"),
        )
        b = EpisodeStarted(
            episode_id=LearningEpisodeId("ep-1"),
            teaching_goal_id=EpisodeGoalId("goal-1"),
            first_step_id=EpisodeStepId("step-1"),
        )
        assert a == b


class TestEpisodeCompleted:
    @pytest.mark.parametrize(
        "kind",
        [
            EpisodeOutcomeKind.GOAL_ACHIEVED,
            EpisodeOutcomeKind.GOAL_PARTIALLY_ACHIEVED,
            EpisodeOutcomeKind.REQUIRES_REMEDIATION,
            EpisodeOutcomeKind.REQUIRES_FOLLOW_UP,
        ],
    )
    def test_lawful_kinds(self, kind: EpisodeOutcomeKind) -> None:
        event = EpisodeCompleted(
            episode_id=LearningEpisodeId("ep-1"),
            outcome_id=EpisodeOutcomeId("out-1"),
            outcome_kind=kind,
        )
        assert event.outcome_kind is kind

    def test_interrupted_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeCompleted(
                episode_id=LearningEpisodeId("ep-1"),
                outcome_id=EpisodeOutcomeId("out-1"),
                outcome_kind=EpisodeOutcomeKind.INTERRUPTED,
            )

    def test_frozen(self) -> None:
        event = EpisodeCompleted(
            episode_id=LearningEpisodeId("ep-1"),
            outcome_id=EpisodeOutcomeId("out-1"),
            outcome_kind=EpisodeOutcomeKind.GOAL_ACHIEVED,
        )
        with pytest.raises(Exception):
            event.outcome_kind = EpisodeOutcomeKind.REQUIRES_FOLLOW_UP  # type: ignore[misc]


class TestReflectionRecorded:
    @pytest.mark.parametrize("rtype", list(ReflectionType))
    def test_all_types(self, rtype: ReflectionType) -> None:
        event = ReflectionRecorded(
            episode_id=LearningEpisodeId("ep-1"),
            reflection_id=ReflectionId("r-1"),
            reflection_type=rtype,
        )
        assert event.reflection_type is rtype

    def test_frozen(self) -> None:
        event = ReflectionRecorded(
            episode_id=LearningEpisodeId("ep-1"),
            reflection_id=ReflectionId("r-1"),
            reflection_type=ReflectionType.POST_EPISODE,
        )
        with pytest.raises(Exception):
            event.reflection_id = ReflectionId("other")  # type: ignore[misc]
