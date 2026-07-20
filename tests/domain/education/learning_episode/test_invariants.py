"""Invariant coverage mapped to LEARNING_EPISODE_INVARIANTS.md E1–E20."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import LearningDimension
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import (
    EvidenceId,
    LearningEpisodeId,
    TeachingStrategyId,
)
from domain.education.learning_episode import (
    EpisodeOutcomeKind,
    LearningEpisode,
)
from tests.domain.education.learning_episode.conftest import (
    make_episode,
    make_goal,
    make_objective_ref,
    make_outcome,
    make_reflection,
    make_steps,
    start_and_finish_required_steps,
)


class TestE1ExactlyOnePurpose:
    def test_single_goal_owned(self) -> None:
        episode = make_episode()
        assert episode.teaching_goal is not None
        assert episode.educational_purpose()

    def test_bundled_purpose_rejected_at_construction(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            make_episode(
                goal=make_goal(
                    statement="Introduce X and also revise Y",
                    purpose="Introduce X and also revise Y",
                )
            )


class TestE2LearningObjectiveRequired:
    def test_missing_objective_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            LearningEpisode.create(
                episode_id=LearningEpisodeId("ep"),
                student_id="student-1",
                teaching_goal=make_goal(),
                teaching_strategy_id=TeachingStrategyId("s"),
                learning_objectives=[],
                steps=make_steps(),
            )

    def test_objective_present(self) -> None:
        episode = make_episode(objectives=[make_objective_ref()])
        assert len(episode.learning_objectives) == 1


class TestE3EvidenceRequired:
    def test_complete_without_evidence_forbidden(self) -> None:
        episode = make_episode()
        start_and_finish_required_steps(episode)
        episode.record_reflection(make_reflection())
        with pytest.raises(EducationalInvariantViolation) as exc:
            episode.complete(make_outcome())
        assert exc.value.invariant == "LearningEpisode.complete.evidence_required"


class TestE5NeverDeclareMastery:
    def test_goal_rejects_mastery(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            make_goal(statement="Master force of mortality")

    def test_outcome_rejects_mastery(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            make_outcome(summary="Topic mastered after this episode")

    def test_no_mastery_outcome_kind(self) -> None:
        assert all("master" not in kind.value for kind in EpisodeOutcomeKind)


class TestE6ReflectionBelongs:
    def test_reflection_required_for_complete(self) -> None:
        episode = make_episode()
        start_and_finish_required_steps(episode)
        episode.attach_evidence(EvidenceId("ev"))
        with pytest.raises(EducationalInvariantViolation) as exc:
            episode.complete(make_outcome())
        assert exc.value.invariant == "LearningEpisode.complete.reflection_required"

    def test_reflection_attaches_to_episode(self) -> None:
        episode = make_episode()
        episode.start()
        episode.record_reflection(make_reflection())
        assert episode.reflection is not None


class TestE11Atomicity:
    @pytest.mark.parametrize(
        "statement",
        [
            "Teach all GLMs this sitting",
            "Revise the entire chapter",
            "Do Chapter 4",
        ],
    )
    def test_non_atomic_rejected(self, statement: str) -> None:
        with pytest.raises(EducationalInvariantViolation):
            make_episode(goal=make_goal(statement=statement, purpose=statement))


class TestE12DimensionalAim:
    @pytest.mark.parametrize("dimension", list(LearningDimension))
    def test_dimension_required(self, dimension: LearningDimension) -> None:
        episode = make_episode(goal=make_goal(dimension=dimension))
        assert episode.primary_dimension is dimension


class TestE13CompletionIsNotLearning:
    def test_completed_has_modest_outcome_not_mastery(self) -> None:
        episode = make_episode()
        start_and_finish_required_steps(episode)
        for _ in range(10):
            try:
                episode.advance_step()
            except EducationalInvariantViolation:
                break
        episode.attach_evidence(EvidenceId("ev"))
        episode.record_reflection(make_reflection())
        episode.complete(
            make_outcome(
                kind=EpisodeOutcomeKind.GOAL_PARTIALLY_ACHIEVED,
                summary="Partial advance on discrimination probes",
            )
        )
        assert episode.is_completed()
        assert episode.outcome is not None
        assert "master" not in episode.outcome.summary.casefold()


class TestE15NoSecondPurposeMidFlight:
    def test_goal_immutable_after_start(self) -> None:
        episode = make_episode()
        episode.start()
        with pytest.raises(EducationalInvariantViolation):
            episode.replace_teaching_goal(
                make_goal(
                    goal_id="other",
                    statement="Suddenly also fix retention",
                    purpose="Suddenly also fix retention",
                )
            )


class TestE16AbortPreservesTruth:
    def test_interrupt_keeps_evidence(self) -> None:
        episode = make_episode()
        episode.start()
        episode.attach_evidence(EvidenceId("attempt-1"))
        episode.interrupt(
            make_outcome(
                kind=EpisodeOutcomeKind.INTERRUPTED,
                summary="Fatigue; attempt evidence retained",
            )
        )
        assert episode.has_evidence(EvidenceId("attempt-1"))
        assert episode.outcome is not None


class TestSequenceAndDuplicates:
    def test_cannot_skip_required_by_completing_early(self) -> None:
        episode = make_episode()
        episode.start()
        episode.attach_evidence(EvidenceId("ev"))
        episode.record_reflection(make_reflection())
        with pytest.raises(EducationalInvariantViolation):
            episode.complete(make_outcome())

    def test_duplicate_evidence_forbidden(self) -> None:
        episode = make_episode()
        episode.start()
        episode.attach_evidence(EvidenceId("ev"))
        with pytest.raises(EducationalInvariantViolation):
            episode.attach_evidence(EvidenceId("ev"))

    def test_cannot_complete_twice(self) -> None:
        episode = make_episode()
        start_and_finish_required_steps(episode)
        for _ in range(10):
            try:
                episode.advance_step()
            except EducationalInvariantViolation:
                break
        episode.attach_evidence(EvidenceId("ev"))
        episode.record_reflection(make_reflection())
        episode.complete(make_outcome())
        with pytest.raises(EducationalInvariantViolation):
            episode.complete(make_outcome(outcome_id="out-2"))

    def test_cannot_start_twice(self) -> None:
        episode = make_episode()
        episode.start()
        with pytest.raises(EducationalInvariantViolation):
            episode.start()
