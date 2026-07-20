"""Entity tests for Learning Episode."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import (
    ConfidenceLevel,
    LearningDimension,
    ReflectionType,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ReflectionId
from domain.education.learning_episode import (
    EpisodeGoal,
    EpisodeGoalId,
    EpisodeOutcome,
    EpisodeOutcomeId,
    EpisodeOutcomeKind,
    EpisodeReflection,
    EpisodeStep,
    EpisodeStepId,
    EpisodeStepKind,
    EpisodeStepStatus,
)
from tests.domain.education.learning_episode.conftest import (
    make_goal,
    make_outcome,
    make_reflection,
    make_step,
)


class TestEpisodeGoal:
    def test_valid(self) -> None:
        goal = make_goal()
        assert goal.entity_id == goal.goal_id
        assert goal.primary_dimension is LearningDimension.UNDERSTANDING

    def test_blank_statement_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeGoal(
                goal_id=EpisodeGoalId("g1"),
                statement=" ",
                educational_purpose="valid purpose",
                primary_dimension=LearningDimension.APPLICATION,
            )

    def test_blank_purpose_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeGoal(
                goal_id=EpisodeGoalId("g1"),
                statement="valid statement",
                educational_purpose="",
                primary_dimension=LearningDimension.APPLICATION,
            )

    def test_mastery_language_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation) as exc:
            EpisodeGoal(
                goal_id=EpisodeGoalId("g1"),
                statement="Master the mortality tables",
                educational_purpose="Master the mortality tables",
                primary_dimension=LearningDimension.UNDERSTANDING,
            )
        assert exc.value.invariant == "EpisodeGoal.no_mastery"

    @pytest.mark.parametrize("dimension", list(LearningDimension))
    def test_all_dimensions(self, dimension: LearningDimension) -> None:
        goal = make_goal(dimension=dimension)
        assert goal.primary_dimension is dimension

    def test_identity_equality(self) -> None:
        a = make_goal(goal_id="same")
        b = EpisodeGoal(
            goal_id=EpisodeGoalId("same"),
            statement="Different statement wording",
            educational_purpose="Different purpose wording",
            primary_dimension=LearningDimension.APPLICATION,
        )
        assert a == b
        assert hash(a) == hash(b)

    def test_different_identity(self) -> None:
        assert make_goal(goal_id="a") != make_goal(goal_id="b")


class TestEpisodeStep:
    def test_lifecycle_activate_complete(self) -> None:
        step = make_step()
        assert step.is_pending()
        active = step.activate()
        assert active.is_active()
        done = active.complete()
        assert done.is_completed()

    def test_activate_idempotent_when_active(self) -> None:
        step = make_step().activate()
        assert step.activate() is step or step.activate() == step

    def test_cannot_complete_when_pending(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            make_step().complete()

    def test_cannot_activate_completed(self) -> None:
        done = make_step().activate().complete()
        with pytest.raises(EducationalInvariantViolation):
            done.activate()

    def test_cannot_complete_twice(self) -> None:
        done = make_step().activate().complete()
        with pytest.raises(EducationalInvariantViolation):
            done.complete()

    def test_blank_label_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeStep(
                step_id=EpisodeStepId("s1"),
                kind=EpisodeStepKind.explanation(),
                sequence_index=0,
                label=" ",
            )

    def test_negative_index_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeStep(
                step_id=EpisodeStepId("s1"),
                kind=EpisodeStepKind.explanation(),
                sequence_index=-1,
                label="x",
            )

    def test_optional_step(self) -> None:
        step = make_step(required=False)
        assert step.required is False

    def test_identity_equality(self) -> None:
        a = make_step(step_id="s1", label="A")
        b = EpisodeStep(
            step_id=EpisodeStepId("s1"),
            kind=EpisodeStepKind.worked_example(),
            sequence_index=2,
            label="B",
            status=EpisodeStepStatus.ACTIVE,
        )
        assert a == b

    @pytest.mark.parametrize(
        "kind",
        [
            EpisodeStepKind.explanation(),
            EpisodeStepKind.worked_example(),
            EpisodeStepKind.guided_practice(),
            EpisodeStepKind.independent_practice(),
            EpisodeStepKind.reflection(),
            EpisodeStepKind.custom("error_analysis"),
            EpisodeStepKind.custom("retrieval_probe"),
        ],
    )
    def test_extensible_kinds(self, kind: EpisodeStepKind) -> None:
        step = EpisodeStep(
            step_id=EpisodeStepId(f"s-{kind.value}"),
            kind=kind,
            sequence_index=0,
            label=kind.value,
        )
        assert step.kind == kind


class TestEpisodeReflection:
    def test_valid(self) -> None:
        reflection = make_reflection()
        assert reflection.can_influence_next_decision()

    def test_blank_content_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeReflection(
                reflection_id=ReflectionId("r1"),
                reflection_type=ReflectionType.DIFFICULTY,
                content="  ",
            )

    def test_short_content_not_consequential(self) -> None:
        reflection = EpisodeReflection(
            reflection_id=ReflectionId("r1"),
            reflection_type=ReflectionType.CONFIDENCE,
            content="ok",
        )
        assert not reflection.can_influence_next_decision()

    @pytest.mark.parametrize("rtype", list(ReflectionType))
    def test_all_reflection_types(self, rtype: ReflectionType) -> None:
        reflection = EpisodeReflection(
            reflection_id=ReflectionId(f"r-{rtype.value}"),
            reflection_type=rtype,
            content="I need more practice on discrimination tasks",
        )
        assert reflection.reflection_type is rtype

    def test_identity_equality(self) -> None:
        a = make_reflection(reflection_id="same")
        b = EpisodeReflection(
            reflection_id=ReflectionId("same"),
            reflection_type=ReflectionType.UNCERTAINTY,
            content="Different content but same identity",
            perceived_difficulty=ConfidenceLevel.LOW,
        )
        assert a == b


class TestEpisodeOutcome:
    @pytest.mark.parametrize("kind", list(EpisodeOutcomeKind))
    def test_all_outcome_kinds(self, kind: EpisodeOutcomeKind) -> None:
        outcome = make_outcome(kind=kind, summary="Provisional educational judgement")
        assert outcome.kind is kind

    def test_mastery_language_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeOutcome(
                outcome_id=EpisodeOutcomeId("o1"),
                kind=EpisodeOutcomeKind.GOAL_ACHIEVED,
                summary="Student has mastered the topic",
            )

    def test_blank_summary_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EpisodeOutcome(
                outcome_id=EpisodeOutcomeId("o1"),
                kind=EpisodeOutcomeKind.GOAL_ACHIEVED,
                summary="",
            )

    def test_terminal_success(self) -> None:
        assert make_outcome(kind=EpisodeOutcomeKind.GOAL_ACHIEVED).is_terminal_success()
        assert make_outcome(
            kind=EpisodeOutcomeKind.GOAL_PARTIALLY_ACHIEVED
        ).is_terminal_success()
        assert not make_outcome(
            kind=EpisodeOutcomeKind.REQUIRES_REMEDIATION
        ).is_terminal_success()

    def test_interrupt_kind(self) -> None:
        assert make_outcome(kind=EpisodeOutcomeKind.INTERRUPTED).is_interrupt_kind()

    def test_requires_further_action(self) -> None:
        assert make_outcome(
            kind=EpisodeOutcomeKind.REQUIRES_FOLLOW_UP
        ).requires_further_action()
        assert not make_outcome(
            kind=EpisodeOutcomeKind.GOAL_ACHIEVED
        ).requires_further_action()

    def test_no_mastery_kind_exists(self) -> None:
        values = {kind.value for kind in EpisodeOutcomeKind}
        assert "mastered" not in values
        assert "mastery" not in values
