"""Policy governing Learning Episode construction and identity integrity.

Architecture Source
    LEARNING_EPISODE_ARCHITECTURE.md / LEARNING_EPISODE_INVARIANTS.md
Concept
    Episode Validation Policy
"""

from __future__ import annotations

from domain.education.foundation.base import (
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.enums import LearningDimension
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import (
    EvidenceId,
    LearningEpisodeId,
    TeachingStrategyId,
)
from domain.education.foundation.references import (
    ConceptReference,
    LearningObjectiveReference,
)
from domain.education.learning_episode.entities.episode_goal import EpisodeGoal
from domain.education.learning_episode.entities.episode_outcome import EpisodeOutcome
from domain.education.learning_episode.entities.episode_reflection import (
    EpisodeReflection,
)
from domain.education.learning_episode.entities.episode_step import EpisodeStep
from domain.education.learning_episode.enums import (
    EpisodeOutcomeKind,
    EpisodeStatus,
)


class EpisodeValidationPolicy:
    """Enforces Learning Episode identity, ownership, and closure invariants."""

    @staticmethod
    def assert_identity(episode_id: LearningEpisodeId) -> LearningEpisodeId:
        if not isinstance(episode_id, LearningEpisodeId):
            raise EducationalInvariantViolation(
                "episode must possess a LearningEpisodeId identity",
                invariant="LearningEpisode.identity.required",
            )
        return episode_id

    @staticmethod
    def assert_student_id(student_id: str) -> str:
        return require_identity_value(student_id, "student_id")

    @staticmethod
    def assert_teaching_goal(goal: EpisodeGoal) -> EpisodeGoal:
        if not isinstance(goal, EpisodeGoal):
            raise EducationalInvariantViolation(
                "episode must own exactly one EpisodeGoal",
                invariant="LearningEpisode.teaching_goal.required",
            )
        return goal

    @staticmethod
    def assert_teaching_strategy(
        strategy_id: TeachingStrategyId,
    ) -> TeachingStrategyId:
        if not isinstance(strategy_id, TeachingStrategyId):
            raise EducationalInvariantViolation(
                "episode must reference a TeachingStrategyId",
                invariant="LearningEpisode.teaching_strategy.required",
            )
        return strategy_id

    @staticmethod
    def assert_learning_objectives(
        objectives: tuple[LearningObjectiveReference, ...]
        | list[LearningObjectiveReference],
    ) -> tuple[LearningObjectiveReference, ...]:
        """Invariant E2 — learning objective required."""
        items = tuple(objectives)
        if not items:
            raise EducationalInvariantViolation(
                "learning episode requires at least one learning objective",
                invariant="LearningEpisode.learning_objectives.min_one",
            )
        seen: set[str] = set()
        for objective in items:
            if not isinstance(objective, LearningObjectiveReference):
                raise EducationalInvariantViolation(
                    "learning objectives must be LearningObjectiveReference values",
                    invariant="LearningEpisode.learning_objectives.type",
                )
            key = objective.objective_id.value
            if key in seen:
                raise EducationalInvariantViolation(
                    "duplicate learning objective reference is not allowed",
                    invariant="LearningEpisode.learning_objectives.no_duplicate",
                )
            seen.add(key)
        return items

    @staticmethod
    def assert_concept_references(
        concepts: tuple[ConceptReference, ...] | list[ConceptReference],
    ) -> tuple[ConceptReference, ...]:
        items = tuple(concepts)
        seen: set[str] = set()
        for concept in items:
            if not isinstance(concept, ConceptReference):
                raise EducationalInvariantViolation(
                    "concept references must be ConceptReference values",
                    invariant="LearningEpisode.concept_references.type",
                )
            key = concept.concept_id.value
            if key in seen:
                raise EducationalInvariantViolation(
                    "duplicate concept reference is not allowed",
                    invariant="LearningEpisode.concept_references.no_duplicate",
                )
            seen.add(key)
        return items

    @staticmethod
    def assert_steps(
        steps: tuple[EpisodeStep, ...] | list[EpisodeStep],
    ) -> tuple[EpisodeStep, ...]:
        items = tuple(steps)
        if not items:
            raise EducationalInvariantViolation(
                "learning episode requires at least one episode step",
                invariant="LearningEpisode.steps.min_one",
            )
        seen_ids: set[str] = set()
        seen_indexes: set[int] = set()
        required_count = 0
        for step in items:
            if not isinstance(step, EpisodeStep):
                raise EducationalInvariantViolation(
                    "steps must be EpisodeStep entities",
                    invariant="LearningEpisode.steps.type",
                )
            if step.step_id.value in seen_ids:
                raise EducationalInvariantViolation(
                    "duplicate episode step identity is not allowed",
                    invariant="LearningEpisode.steps.no_duplicate_id",
                )
            seen_ids.add(step.step_id.value)
            if step.sequence_index in seen_indexes:
                raise EducationalInvariantViolation(
                    "duplicate episode step sequence_index is not allowed",
                    invariant="LearningEpisode.steps.no_duplicate_index",
                )
            seen_indexes.add(step.sequence_index)
            if step.required:
                required_count += 1
        if required_count < 1:
            raise EducationalInvariantViolation(
                "learning episode requires at least one required step",
                invariant="LearningEpisode.steps.min_one_required",
            )
        ordered = tuple(sorted(items, key=lambda s: s.sequence_index))
        expected = list(range(len(ordered)))
        actual = [step.sequence_index for step in ordered]
        if actual != expected:
            raise EducationalInvariantViolation(
                "episode step sequence_index values must be contiguous from 0",
                invariant="LearningEpisode.steps.contiguous_indexes",
            )
        return ordered

    @staticmethod
    def assert_primary_dimension(dimension: LearningDimension) -> LearningDimension:
        """Invariant E12 — dimensional aim required."""
        if not isinstance(dimension, LearningDimension):
            raise EducationalInvariantViolation(
                "episode must name a primary LearningDimension",
                invariant="LearningEpisode.primary_dimension.required",
            )
        return dimension

    @staticmethod
    def assert_can_start(status: EpisodeStatus) -> None:
        if status is not EpisodeStatus.PLANNED:
            raise EducationalInvariantViolation(
                "cannot start an episode that is not in PLANNED status",
                invariant="LearningEpisode.start.not_planned",
            )

    @staticmethod
    def assert_not_started_for_goal_change(status: EpisodeStatus) -> None:
        if status is not EpisodeStatus.PLANNED:
            raise EducationalInvariantViolation(
                "cannot change teaching goal after the episode has started",
                invariant="LearningEpisode.teaching_goal.immutable_after_start",
            )

    @staticmethod
    def assert_in_progress(status: EpisodeStatus, *, action: str) -> None:
        if status is not EpisodeStatus.IN_PROGRESS:
            raise EducationalInvariantViolation(
                f"cannot {action} unless the episode is in progress",
                invariant=f"LearningEpisode.{action}.not_in_progress",
            )

    @staticmethod
    def assert_not_terminal(status: EpisodeStatus, *, action: str) -> None:
        if status in {EpisodeStatus.COMPLETED, EpisodeStatus.INTERRUPTED}:
            raise EducationalInvariantViolation(
                f"cannot {action} a terminal episode",
                invariant=f"LearningEpisode.{action}.terminal",
            )

    @staticmethod
    def assert_can_complete(
        status: EpisodeStatus,
        *,
        required_steps_complete: bool,
        has_reflection: bool,
        has_evidence: bool,
    ) -> None:
        EpisodeValidationPolicy.assert_in_progress(status, action="complete")
        if not required_steps_complete:
            raise EducationalInvariantViolation(
                "cannot complete before all required steps are finished",
                invariant="LearningEpisode.complete.required_steps",
            )
        if not has_reflection:
            raise EducationalInvariantViolation(
                "reflection is required before episode completion",
                invariant="LearningEpisode.complete.reflection_required",
            )
        if not has_evidence:
            raise EducationalInvariantViolation(
                "at least one evidence item is required before completion",
                invariant="LearningEpisode.complete.evidence_required",
            )

    @staticmethod
    def assert_completion_outcome(outcome: EpisodeOutcome) -> EpisodeOutcome:
        if not isinstance(outcome, EpisodeOutcome):
            raise EducationalInvariantViolation(
                "completion requires an EpisodeOutcome",
                invariant="LearningEpisode.complete.outcome.required",
            )
        if outcome.kind is EpisodeOutcomeKind.INTERRUPTED:
            raise EducationalInvariantViolation(
                "INTERRUPTED outcome is reserved for interrupt(), not complete()",
                invariant="LearningEpisode.complete.outcome.not_interrupted",
            )
        return outcome

    @staticmethod
    def assert_interrupt_outcome(outcome: EpisodeOutcome) -> EpisodeOutcome:
        if not isinstance(outcome, EpisodeOutcome):
            raise EducationalInvariantViolation(
                "interrupt requires an EpisodeOutcome",
                invariant="LearningEpisode.interrupt.outcome.required",
            )
        if outcome.kind not in {
            EpisodeOutcomeKind.INTERRUPTED,
            EpisodeOutcomeKind.REQUIRES_REMEDIATION,
            EpisodeOutcomeKind.REQUIRES_FOLLOW_UP,
        }:
            raise EducationalInvariantViolation(
                "interrupt outcome must be interrupted, remediation, or follow-up",
                invariant="LearningEpisode.interrupt.outcome.kind",
            )
        return outcome

    @staticmethod
    def assert_reflection(reflection: EpisodeReflection) -> EpisodeReflection:
        if not isinstance(reflection, EpisodeReflection):
            raise EducationalInvariantViolation(
                "reflection must be an EpisodeReflection",
                invariant="LearningEpisode.reflection.type",
            )
        if not reflection.can_influence_next_decision():
            raise EducationalInvariantViolation(
                "reflection must be capable of influencing the next decision",
                invariant="LearningEpisode.reflection.consequence",
            )
        return reflection

    @staticmethod
    def assert_evidence_not_duplicate(
        existing: tuple[EvidenceId, ...] | list[EvidenceId],
        evidence_id: EvidenceId,
    ) -> EvidenceId:
        if not isinstance(evidence_id, EvidenceId):
            raise EducationalInvariantViolation(
                "evidence_id must be an EvidenceId",
                invariant="LearningEpisode.evidence.type",
            )
        for item in existing:
            if item == evidence_id:
                raise EducationalInvariantViolation(
                    "cannot attach duplicate evidence to an episode",
                    invariant="LearningEpisode.evidence.no_duplicate",
                )
        return evidence_id

    @staticmethod
    def assert_selection_rationale(rationale: str | None) -> str | None:
        """Invariant E19 — explainable selection when provided."""
        if rationale is None:
            return None
        return require_non_empty_text(rationale, "selection_rationale")
