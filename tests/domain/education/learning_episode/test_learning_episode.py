"""Learning Episode aggregate behaviour and lifecycle tests."""

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
    EpisodeCompleted,
    EpisodeOutcomeKind,
    EpisodeStarted,
    EpisodeStatus,
    EpisodeStepKind,
    LearningEpisode,
    ReflectionRecorded,
)
from tests.domain.education.learning_episode.conftest import (
    make_episode,
    make_goal,
    make_objective_ref,
    make_outcome,
    make_reflection,
    make_step,
    make_steps,
    start_and_finish_required_steps,
)


class TestLearningEpisodeCreate:
    def test_create_planned(self) -> None:
        episode = make_episode()
        assert episode.is_planned()
        assert episode.status is EpisodeStatus.PLANNED
        assert episode.reflection is None
        assert episode.outcome is None
        assert episode.evidence_ids == ()

    def test_owns_exactly_one_goal(self) -> None:
        episode = make_episode()
        assert episode.teaching_goal.statement
        assert (
            episode.educational_purpose()
            == episode.teaching_goal.educational_purpose
        )

    def test_primary_dimension_aligned(self) -> None:
        goal = make_goal(dimension=LearningDimension.TRANSFER)
        episode = make_episode(goal=goal)
        assert episode.primary_dimension is LearningDimension.TRANSFER

    def test_requires_learning_objective(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            LearningEpisode.create(
                episode_id=LearningEpisodeId("ep-x"),
                student_id="student-1",
                teaching_goal=make_goal(),
                teaching_strategy_id=TeachingStrategyId("s1"),
                learning_objectives=[],
                steps=make_steps(),
            )

    def test_requires_steps(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            LearningEpisode.create(
                episode_id=LearningEpisodeId("ep-x"),
                student_id="student-1",
                teaching_goal=make_goal(),
                teaching_strategy_id=TeachingStrategyId("s1"),
                learning_objectives=[make_objective_ref()],
                steps=[],
            )

    def test_identity_equality(self) -> None:
        a = make_episode(episode_id="same")
        b = make_episode(episode_id="same")
        assert a == b
        assert hash(a) == hash(b)

    def test_repr(self) -> None:
        text = repr(make_episode())
        assert "LearningEpisode" in text
        assert "episode-001" in text

    def test_queries(self) -> None:
        episode = make_episode()
        assert episode.has_learning_objective("lo-select-ultimate")
        assert episode.has_concept("concept-select-mortality")
        assert not episode.has_evidence(EvidenceId("missing"))

    def test_sequence_and_progress(self) -> None:
        episode = make_episode()
        assert episode.sequence.length == 3
        assert episode.progress.completed_steps == 0


class TestStart:
    def test_start_transitions(self) -> None:
        episode = make_episode()
        episode.start()
        assert episode.is_in_progress()
        assert episode.steps[0].is_active()

    def test_start_emits_event(self) -> None:
        episode = make_episode()
        episode.start()
        events = episode.pull_events()
        assert len(events) == 1
        assert isinstance(events[0], EpisodeStarted)
        assert events[0].first_step_id == episode.steps[0].step_id

    def test_cannot_start_twice(self) -> None:
        episode = make_episode()
        episode.start()
        with pytest.raises(EducationalInvariantViolation):
            episode.start()

    def test_pull_events_clears(self) -> None:
        episode = make_episode()
        episode.start()
        assert episode.pull_events()
        assert episode.pull_events() == []


class TestAdvanceStep:
    def test_advance_completes_active_and_activates_next(self) -> None:
        episode = make_episode()
        episode.start()
        completed = episode.advance_step()
        assert completed.is_completed()
        assert episode.steps[0].is_completed()
        assert episode.steps[1].is_active()

    def test_advance_through_all(self) -> None:
        episode = make_episode()
        episode.start()
        episode.advance_step()
        episode.advance_step()
        episode.advance_step()
        assert episode.progress.all_steps_complete
        with pytest.raises(EducationalInvariantViolation):
            episode.advance_step()

    def test_cannot_advance_when_planned(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            make_episode().advance_step()


class TestEvidence:
    def test_attach_evidence(self) -> None:
        episode = make_episode()
        episode.start()
        eid = EvidenceId("ev-1")
        episode.attach_evidence(eid)
        assert episode.has_evidence(eid)

    def test_duplicate_evidence_rejected(self) -> None:
        episode = make_episode()
        episode.start()
        eid = EvidenceId("ev-1")
        episode.attach_evidence(eid)
        with pytest.raises(EducationalInvariantViolation) as exc:
            episode.attach_evidence(eid)
        assert exc.value.invariant == "LearningEpisode.evidence.no_duplicate"

    def test_multiple_distinct_evidence(self) -> None:
        episode = make_episode()
        episode.start()
        episode.attach_evidence(EvidenceId("ev-1"))
        episode.attach_evidence(EvidenceId("ev-2"))
        assert len(episode.evidence_ids) == 2


class TestReflection:
    def test_record_reflection(self) -> None:
        episode = make_episode()
        episode.start()
        episode.record_reflection(make_reflection())
        assert episode.reflection is not None
        events = episode.pull_events()
        assert any(isinstance(e, ReflectionRecorded) for e in events)

    def test_cannot_record_twice(self) -> None:
        episode = make_episode()
        episode.start()
        episode.record_reflection(make_reflection())
        with pytest.raises(EducationalInvariantViolation):
            episode.record_reflection(make_reflection(reflection_id="refl-002"))


class TestComplete:
    def _ready(self) -> LearningEpisode:
        episode = make_episode()
        start_and_finish_required_steps(episode)
        for _ in range(10):
            try:
                episode.advance_step()
            except EducationalInvariantViolation:
                break
        episode.attach_evidence(EvidenceId("ev-1"))
        episode.record_reflection(make_reflection())
        return episode

    def test_complete_happy_path(self) -> None:
        episode = self._ready()
        episode.complete(make_outcome())
        assert episode.is_completed()
        assert episode.outcome is not None
        events = [e for e in episode.pull_events() if isinstance(e, EpisodeCompleted)]
        assert len(events) == 1

    def test_cannot_complete_twice(self) -> None:
        episode = self._ready()
        episode.complete(make_outcome())
        with pytest.raises(EducationalInvariantViolation):
            episode.complete(make_outcome(outcome_id="out-2"))

    def test_cannot_complete_without_reflection(self) -> None:
        episode = make_episode()
        start_and_finish_required_steps(episode)
        episode.attach_evidence(EvidenceId("ev-1"))
        with pytest.raises(EducationalInvariantViolation):
            episode.complete(make_outcome())

    def test_cannot_complete_without_evidence(self) -> None:
        episode = make_episode()
        start_and_finish_required_steps(episode)
        episode.record_reflection(make_reflection())
        with pytest.raises(EducationalInvariantViolation):
            episode.complete(make_outcome())

    def test_cannot_complete_before_required_steps(self) -> None:
        episode = make_episode()
        episode.start()
        episode.attach_evidence(EvidenceId("ev-1"))
        episode.record_reflection(make_reflection())
        with pytest.raises(EducationalInvariantViolation):
            episode.complete(make_outcome())

    @pytest.mark.parametrize(
        "kind",
        [
            EpisodeOutcomeKind.GOAL_ACHIEVED,
            EpisodeOutcomeKind.GOAL_PARTIALLY_ACHIEVED,
            EpisodeOutcomeKind.REQUIRES_REMEDIATION,
            EpisodeOutcomeKind.REQUIRES_FOLLOW_UP,
        ],
    )
    def test_completion_outcomes(self, kind: EpisodeOutcomeKind) -> None:
        episode = self._ready()
        episode.complete(make_outcome(kind=kind, summary="Judgement recorded"))
        assert episode.outcome is not None
        assert episode.outcome.kind is kind


class TestInterrupt:
    def test_interrupt_from_planned(self) -> None:
        episode = make_episode()
        episode.interrupt(
            make_outcome(
                kind=EpisodeOutcomeKind.INTERRUPTED,
                summary="Session ended before start",
            )
        )
        assert episode.is_interrupted()
        assert episode.is_terminal()

    def test_interrupt_from_in_progress(self) -> None:
        episode = make_episode()
        episode.start()
        episode.attach_evidence(EvidenceId("ev-attempt"))
        episode.interrupt(
            make_outcome(
                kind=EpisodeOutcomeKind.REQUIRES_REMEDIATION,
                summary="Prerequisite collapse mid-episode",
            )
        )
        assert episode.is_interrupted()
        assert episode.has_evidence(EvidenceId("ev-attempt"))

    def test_cannot_interrupt_completed(self) -> None:
        episode = TestComplete()._ready()
        episode.complete(make_outcome())
        with pytest.raises(EducationalInvariantViolation):
            episode.interrupt(
                make_outcome(
                    kind=EpisodeOutcomeKind.INTERRUPTED,
                    summary="late abort",
                )
            )

    def test_cannot_interrupt_twice(self) -> None:
        episode = make_episode()
        episode.interrupt(
            make_outcome(
                kind=EpisodeOutcomeKind.INTERRUPTED,
                summary="first abort",
            )
        )
        with pytest.raises(EducationalInvariantViolation):
            episode.interrupt(
                make_outcome(
                    kind=EpisodeOutcomeKind.INTERRUPTED,
                    summary="second abort",
                )
            )


class TestTeachingGoalImmutability:
    def test_can_replace_while_planned(self) -> None:
        episode = make_episode()
        new_goal = make_goal(
            goal_id="goal-002",
            statement="Strengthen retrieval of select table lookup",
            purpose="Strengthen retrieval of select table lookup",
            dimension=LearningDimension.RETENTION,
        )
        episode.replace_teaching_goal(new_goal)
        assert episode.teaching_goal.goal_id.value == "goal-002"
        assert episode.primary_dimension is LearningDimension.RETENTION

    def test_cannot_replace_after_start(self) -> None:
        episode = make_episode()
        episode.start()
        with pytest.raises(EducationalInvariantViolation) as exc:
            episode.replace_teaching_goal(
                make_goal(goal_id="goal-002", statement="Another aim")
            )
        assert (
            exc.value.invariant
            == "LearningEpisode.teaching_goal.immutable_after_start"
        )


class TestExtensibleSteps:
    def test_custom_pedagogy_steps(self) -> None:
        steps = [
            make_step(
                step_id="s1",
                kind=EpisodeStepKind.custom("contrastive_examples"),
                index=0,
                label="Contrast",
            ),
            make_step(
                step_id="s2",
                kind=EpisodeStepKind.custom("discrimination_probe"),
                index=1,
                label="Probe",
            ),
        ]
        episode = make_episode(steps=steps)
        episode.start()
        episode.advance_step()
        assert episode.steps[0].is_completed()
        assert episode.steps[1].is_active()

    def test_optional_trailing_step(self) -> None:
        steps = [
            make_step(step_id="s1", index=0, required=True),
            make_step(step_id="s2", index=1, required=False, label="Optional stretch"),
        ]
        episode = make_episode(steps=steps)
        episode.start()
        episode.advance_step()
        assert episode.progress.required_sequence_complete
        episode.attach_evidence(EvidenceId("ev-1"))
        episode.record_reflection(make_reflection())
        episode.complete(make_outcome())
        assert episode.is_completed()
