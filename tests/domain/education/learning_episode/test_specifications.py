"""Specification tests for Learning Episode."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import EvidenceId
from domain.education.learning_episode import (
    EpisodeCanCompleteSpecification,
    EpisodeCanTransitionSpecification,
    EpisodeIsAtomicSpecification,
    EpisodeIsCompleteSpecification,
    EpisodeOutcomeKind,
    EpisodeSupportsReflectionSpecification,
)
from tests.domain.education.learning_episode.conftest import (
    make_episode,
    make_goal,
    make_outcome,
    make_reflection,
    start_and_finish_required_steps,
)


class TestEpisodeIsAtomicSpecification:
    def test_satisfied(self) -> None:
        episode = make_episode()
        assert EpisodeIsAtomicSpecification().is_satisfied_by(episode)

    def test_goal_helper(self) -> None:
        assert EpisodeIsAtomicSpecification().is_satisfied_by_goal(make_goal())

    def test_assert_passes(self) -> None:
        EpisodeIsAtomicSpecification().assert_satisfied_by(make_episode())


class TestEpisodeCanCompleteSpecification:
    def test_unsatisfied_when_planned(self) -> None:
        assert not EpisodeCanCompleteSpecification().is_satisfied_by(make_episode())

    def test_satisfied_after_work(self) -> None:
        episode = make_episode()
        start_and_finish_required_steps(episode)
        # Drain remaining steps
        for _ in range(10):
            try:
                episode.advance_step()
            except EducationalInvariantViolation:
                break
        episode.attach_evidence(EvidenceId("ev-1"))
        episode.record_reflection(make_reflection())
        assert EpisodeCanCompleteSpecification().is_satisfied_by(episode)
        EpisodeCanCompleteSpecification().assert_satisfied_by(episode)

    def test_assert_fails_without_reflection(self) -> None:
        episode = make_episode()
        start_and_finish_required_steps(episode)
        episode.attach_evidence(EvidenceId("ev-1"))
        with pytest.raises(EducationalInvariantViolation):
            EpisodeCanCompleteSpecification().assert_satisfied_by(episode)


class TestEpisodeIsCompleteSpecification:
    def test_false_initially(self) -> None:
        assert not EpisodeIsCompleteSpecification().is_satisfied_by(make_episode())

    def test_true_after_complete(self) -> None:
        episode = make_episode()
        start_and_finish_required_steps(episode)
        for _ in range(10):
            try:
                episode.advance_step()
            except EducationalInvariantViolation:
                break
        episode.attach_evidence(EvidenceId("ev-1"))
        episode.record_reflection(make_reflection())
        episode.complete(make_outcome())
        assert EpisodeIsCompleteSpecification().is_satisfied_by(episode)


class TestEpisodeSupportsReflectionSpecification:
    def test_after_start(self) -> None:
        episode = make_episode()
        episode.start()
        assert EpisodeSupportsReflectionSpecification().is_satisfied_by(episode)

    def test_false_after_recorded(self) -> None:
        episode = make_episode()
        episode.start()
        episode.record_reflection(make_reflection())
        assert not EpisodeSupportsReflectionSpecification().is_satisfied_by(episode)


class TestEpisodeCanTransitionSpecification:
    def test_planned_transitions(self) -> None:
        spec = EpisodeCanTransitionSpecification()
        episode = make_episode()
        assert spec.can_start(episode)
        assert not spec.can_advance_step(episode)
        assert spec.can_interrupt(episode)
        assert not spec.can_complete(episode)

    def test_in_progress_transitions(self) -> None:
        spec = EpisodeCanTransitionSpecification()
        episode = make_episode()
        episode.start()
        assert not spec.can_start(episode)
        assert spec.can_advance_step(episode)
        assert spec.can_attach_evidence(episode)
        assert spec.can_record_reflection(episode)
        assert spec.can_interrupt(episode)

    def test_is_satisfied_by_named(self) -> None:
        spec = EpisodeCanTransitionSpecification()
        episode = make_episode()
        assert spec.is_satisfied_by(episode, "start")
        assert not spec.is_satisfied_by(episode, "complete")

    def test_unknown_transition(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeCanTransitionSpecification().is_satisfied_by(
                make_episode(), "teleport"
            )

    def test_assert_satisfied_by(self) -> None:
        EpisodeCanTransitionSpecification().assert_satisfied_by(
            make_episode(), "start"
        )
        with pytest.raises(EducationalInvariantViolation):
            EpisodeCanTransitionSpecification().assert_satisfied_by(
                make_episode(), "complete"
            )

    def test_terminal_cannot_interrupt(self) -> None:
        episode = make_episode()
        episode.interrupt(
            make_outcome(
                kind=EpisodeOutcomeKind.INTERRUPTED,
                summary="Fatigue abort with attempt recorded",
            )
        )
        spec = EpisodeCanTransitionSpecification()
        assert not spec.can_interrupt(episode)
        assert not spec.can_start(episode)
