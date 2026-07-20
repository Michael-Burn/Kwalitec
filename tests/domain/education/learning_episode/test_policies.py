"""Policy tests for Learning Episode."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import LearningDimension
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import (
    EvidenceId,
    LearningEpisodeId,
    LearningObjectiveId,
    TeachingStrategyId,
)
from domain.education.foundation.references import LearningObjectiveReference
from domain.education.learning_episode import (
    AtomicityPolicy,
    EpisodeStatus,
    EpisodeStep,
    EpisodeStepId,
    EpisodeStepKind,
    EpisodeValidationPolicy,
    SequencingPolicy,
)
from tests.domain.education.learning_episode.conftest import (
    make_goal,
    make_outcome,
    make_step,
    make_steps,
)


class TestEpisodeValidationPolicy:
    def test_assert_identity(self) -> None:
        eid = LearningEpisodeId("ep-1")
        assert EpisodeValidationPolicy.assert_identity(eid) is eid

    def test_identity_type_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeValidationPolicy.assert_identity("ep-1")  # type: ignore[arg-type]

    def test_student_id(self) -> None:
        assert EpisodeValidationPolicy.assert_student_id("student-1") == "student-1"

    def test_student_id_whitespace_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeValidationPolicy.assert_student_id("student 1")

    def test_learning_objectives_required(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeValidationPolicy.assert_learning_objectives([])

    def test_duplicate_objectives_rejected(self) -> None:
        ref = LearningObjectiveReference(
            objective_id=LearningObjectiveId("lo-1"),
        )
        with pytest.raises(EducationalInvariantViolation):
            EpisodeValidationPolicy.assert_learning_objectives([ref, ref])

    def test_steps_require_contiguous_indexes(self) -> None:
        steps = [
            make_step(step_id="a", index=0),
            make_step(step_id="b", index=2),
        ]
        with pytest.raises(EducationalInvariantViolation):
            EpisodeValidationPolicy.assert_steps(steps)

    def test_steps_require_one_required(self) -> None:
        steps = [
            make_step(step_id="a", index=0, required=False),
            make_step(step_id="b", index=1, required=False),
        ]
        with pytest.raises(EducationalInvariantViolation):
            EpisodeValidationPolicy.assert_steps(steps)

    def test_duplicate_step_ids_rejected(self) -> None:
        steps = [
            make_step(step_id="same", index=0),
            make_step(step_id="same", index=1),
        ]
        with pytest.raises(EducationalInvariantViolation):
            EpisodeValidationPolicy.assert_steps(steps)

    def test_assert_can_start_only_planned(self) -> None:
        EpisodeValidationPolicy.assert_can_start(EpisodeStatus.PLANNED)
        with pytest.raises(EducationalInvariantViolation):
            EpisodeValidationPolicy.assert_can_start(EpisodeStatus.IN_PROGRESS)

    def test_assert_can_complete_requires_reflection(self) -> None:
        with pytest.raises(EducationalInvariantViolation) as exc:
            EpisodeValidationPolicy.assert_can_complete(
                EpisodeStatus.IN_PROGRESS,
                required_steps_complete=True,
                has_reflection=False,
                has_evidence=True,
            )
        assert exc.value.invariant == "LearningEpisode.complete.reflection_required"

    def test_assert_can_complete_requires_evidence(self) -> None:
        with pytest.raises(EducationalInvariantViolation) as exc:
            EpisodeValidationPolicy.assert_can_complete(
                EpisodeStatus.IN_PROGRESS,
                required_steps_complete=True,
                has_reflection=True,
                has_evidence=False,
            )
        assert exc.value.invariant == "LearningEpisode.complete.evidence_required"

    def test_assert_can_complete_requires_steps(self) -> None:
        with pytest.raises(EducationalInvariantViolation) as exc:
            EpisodeValidationPolicy.assert_can_complete(
                EpisodeStatus.IN_PROGRESS,
                required_steps_complete=False,
                has_reflection=True,
                has_evidence=True,
            )
        assert exc.value.invariant == "LearningEpisode.complete.required_steps"

    def test_completion_outcome_rejects_interrupted(self) -> None:
        from domain.education.learning_episode import EpisodeOutcomeKind

        outcome = make_outcome(kind=EpisodeOutcomeKind.INTERRUPTED)
        with pytest.raises(EducationalInvariantViolation):
            EpisodeValidationPolicy.assert_completion_outcome(outcome)

    def test_interrupt_outcome_rejects_achieved(self) -> None:
        from domain.education.learning_episode import EpisodeOutcomeKind

        outcome = make_outcome(kind=EpisodeOutcomeKind.GOAL_ACHIEVED)
        with pytest.raises(EducationalInvariantViolation):
            EpisodeValidationPolicy.assert_interrupt_outcome(outcome)

    def test_evidence_duplicate(self) -> None:
        eid = EvidenceId("ev-1")
        with pytest.raises(EducationalInvariantViolation):
            EpisodeValidationPolicy.assert_evidence_not_duplicate([eid], eid)

    def test_reflection_consequence(self) -> None:
        from domain.education.foundation.enums import ReflectionType
        from domain.education.foundation.ids import ReflectionId
        from domain.education.learning_episode import EpisodeReflection

        weak = EpisodeReflection(
            reflection_id=ReflectionId("r1"),
            reflection_type=ReflectionType.POST_EPISODE,
            content="no",
        )
        with pytest.raises(EducationalInvariantViolation):
            EpisodeValidationPolicy.assert_reflection(weak)

    def test_strategy_required(self) -> None:
        sid = TeachingStrategyId("s1")
        assert EpisodeValidationPolicy.assert_teaching_strategy(sid) is sid

    def test_dimension_required(self) -> None:
        dim = LearningDimension.TRANSFER
        assert EpisodeValidationPolicy.assert_primary_dimension(dim) is dim

    def test_goal_change_only_planned(self) -> None:
        EpisodeValidationPolicy.assert_not_started_for_goal_change(
            EpisodeStatus.PLANNED
        )
        with pytest.raises(EducationalInvariantViolation):
            EpisodeValidationPolicy.assert_not_started_for_goal_change(
                EpisodeStatus.IN_PROGRESS
            )


class TestAtomicityPolicy:
    @pytest.mark.parametrize(
        "statement",
        [
            "Repair select vs ultimate confusion",
            "Teach exponential-family intuition",
            "Guided practice on term-assurance EPV",
            "Retrieve commutation-function selection rules",
        ],
    )
    def test_atomic_statements(self, statement: str) -> None:
        assert AtomicityPolicy.is_atomic_statement(statement)

    @pytest.mark.parametrize(
        "statement",
        [
            "Revise the entire chapter",
            "Teach all GLMs",
            "Do Chapter 4",
            "Finish the chapter today",
            "Practice everything weak this month",
            "Master the topic completely",
            "Revise the whole subject",
            "Cover all topics in one sitting",
            "Introduce X and also revise Y",
        ],
    )
    def test_non_atomic_statements(self, statement: str) -> None:
        assert not AtomicityPolicy.is_atomic_statement(statement)
        with pytest.raises(EducationalInvariantViolation):
            AtomicityPolicy.assert_atomic_statement(statement)

    def test_assert_atomic_goal(self) -> None:
        goal = make_goal()
        assert AtomicityPolicy.assert_atomic_goal(goal) is goal

    def test_non_atomic_goal_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            AtomicityPolicy.assert_atomic_goal(
                make_goal(statement="Revise the entire chapter on mortality")
            )


class TestSequencingPolicy:
    def test_build_sequence(self) -> None:
        steps = make_steps()
        seq = SequencingPolicy.build_sequence(steps)
        assert seq.length == 3
        assert len(seq.required_step_ids) == 3

    def test_progress(self) -> None:
        steps = make_steps()
        progress = SequencingPolicy.progress_of(steps)
        assert progress.completed_steps == 0
        assert progress.total_steps == 3

    def test_assert_can_advance_first_pending(self) -> None:
        steps = make_steps()
        current = SequencingPolicy.assert_can_advance(steps)
        assert current.sequence_index == 0

    def test_activate_first_pending(self) -> None:
        steps = make_steps()
        updated = SequencingPolicy.activate_first_pending(list(steps))
        assert updated[0].is_active()

    def test_replace_step(self) -> None:
        steps = list(make_steps())
        activated = steps[0].activate()
        updated = SequencingPolicy.replace_step(steps, activated)
        assert updated[0].is_active()

    def test_replace_unknown_rejected(self) -> None:
        steps = list(make_steps())
        foreign = EpisodeStep(
            step_id=EpisodeStepId("foreign"),
            kind=EpisodeStepKind.explanation(),
            sequence_index=0,
            label="x",
        )
        with pytest.raises(EducationalInvariantViolation):
            SequencingPolicy.replace_step(steps, foreign)

    def test_exhausted(self) -> None:
        steps = [
            make_step(step_id="a", index=0).activate().complete(),
        ]
        with pytest.raises(EducationalInvariantViolation) as exc:
            SequencingPolicy.assert_can_advance(steps)
        assert exc.value.invariant == "SequencingPolicy.exhausted"

    def test_step_belongs(self) -> None:
        steps = make_steps()
        found = SequencingPolicy.assert_step_belongs(steps, steps[1].step_id)
        assert found == steps[1]

    def test_step_not_found(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            SequencingPolicy.assert_step_belongs(
                make_steps(), EpisodeStepId("missing")
            )
