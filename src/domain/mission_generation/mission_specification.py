"""MissionSpecification — deterministic educational mission projection.

Architecture Source
    EDUCATIONAL_ORCHESTRATION_MODEL.md
    SESSION_ASSEMBLY_MODEL.md
Concept
    Mission Specification
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import (
    DiagnosisId,
    DigitalTwinId,
    PriorityId,
    TeachingStrategyId,
)
from domain.mission_generation.enums import CompletionConditionCode
from domain.mission_generation.ids import MissionSpecificationId
from domain.mission_generation.mission_duration import MissionDuration
from domain.mission_generation.mission_objective import MissionObjective
from domain.mission_generation.mission_priority import MissionPriority
from domain.mission_generation.mission_sequence import MissionSequence


@dataclass(frozen=True, slots=True)
class SuccessCriterion(EducationalValueObject):
    """Observable educational success signal for a mission."""

    statement: str
    code: str | None = None

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "statement",
            require_non_empty_text(self.statement, "statement"),
        )
        if self.code is not None:
            object.__setattr__(
                self,
                "code",
                require_non_empty_text(self.code, "code"),
            )


@dataclass(frozen=True, slots=True)
class CompletionCondition(EducationalValueObject):
    """Deterministic condition that must hold for mission completion."""

    statement: str
    code: CompletionConditionCode

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "statement",
            require_non_empty_text(self.statement, "statement"),
        )
        if not isinstance(self.code, CompletionConditionCode):
            raise EducationalInvariantViolation(
                "code must be a CompletionConditionCode",
                invariant="CompletionCondition.code.type",
            )


@dataclass(frozen=True, slots=True)
class MissionSpecification(EducationalValueObject):
    """Fully explainable mission projection from Educational OS state.

    A MissionSpecification is a pure educational plan: objective, duration,
    priority, ordered tasks, success criteria, completion conditions, and
    educational rationale. It does not schedule calendar slots, mutate the
    Twin, or invoke AI.
    """

    mission_id: MissionSpecificationId
    student_id: str
    objective: MissionObjective
    duration: MissionDuration
    priority: MissionPriority
    sequence: MissionSequence
    success_criteria: tuple[SuccessCriterion, ...]
    completion_conditions: tuple[CompletionCondition, ...]
    educational_rationale: str
    twin_id: DigitalTwinId
    diagnosis_id: DiagnosisId
    priority_id: PriorityId
    strategy_id: TeachingStrategyId

    def _validate(self) -> None:
        if not isinstance(self.mission_id, MissionSpecificationId):
            raise EducationalInvariantViolation(
                "mission_id must be a MissionSpecificationId",
                invariant="MissionSpecification.mission_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_non_empty_text(self.student_id, "student_id"),
        )
        if not isinstance(self.objective, MissionObjective):
            raise EducationalInvariantViolation(
                "objective must be a MissionObjective",
                invariant="MissionSpecification.objective.type",
            )
        if not isinstance(self.duration, MissionDuration):
            raise EducationalInvariantViolation(
                "duration must be a MissionDuration",
                invariant="MissionSpecification.duration.type",
            )
        if not isinstance(self.priority, MissionPriority):
            raise EducationalInvariantViolation(
                "priority must be a MissionPriority",
                invariant="MissionSpecification.priority.type",
            )
        if not isinstance(self.sequence, MissionSequence):
            raise EducationalInvariantViolation(
                "sequence must be a MissionSequence",
                invariant="MissionSpecification.sequence.type",
            )
        if not isinstance(self.success_criteria, tuple) or not self.success_criteria:
            raise EducationalInvariantViolation(
                "success_criteria must be a non-empty tuple",
                invariant="MissionSpecification.success_criteria.min_one",
            )
        for criterion in self.success_criteria:
            if not isinstance(criterion, SuccessCriterion):
                raise EducationalInvariantViolation(
                    "success_criteria must contain SuccessCriterion values",
                    invariant="MissionSpecification.success_criteria.item_type",
                )
        if (
            not isinstance(self.completion_conditions, tuple)
            or not self.completion_conditions
        ):
            raise EducationalInvariantViolation(
                "completion_conditions must be a non-empty tuple",
                invariant="MissionSpecification.completion_conditions.min_one",
            )
        for condition in self.completion_conditions:
            if not isinstance(condition, CompletionCondition):
                raise EducationalInvariantViolation(
                    "completion_conditions must contain CompletionCondition values",
                    invariant="MissionSpecification.completion_conditions.item_type",
                )
        object.__setattr__(
            self,
            "educational_rationale",
            require_non_empty_text(
                self.educational_rationale, "educational_rationale"
            ),
        )
        if len(self.educational_rationale) < 24:
            raise EducationalInvariantViolation(
                "educational rationale must be educationally substantive",
                invariant="MissionSpecification.educational_rationale.substantive",
            )
        if not isinstance(self.twin_id, DigitalTwinId):
            raise EducationalInvariantViolation(
                "twin_id must be a DigitalTwinId",
                invariant="MissionSpecification.twin_id.type",
            )
        if not isinstance(self.diagnosis_id, DiagnosisId):
            raise EducationalInvariantViolation(
                "diagnosis_id must be a DiagnosisId",
                invariant="MissionSpecification.diagnosis_id.type",
            )
        if not isinstance(self.priority_id, PriorityId):
            raise EducationalInvariantViolation(
                "priority_id must be a PriorityId",
                invariant="MissionSpecification.priority_id.type",
            )
        if not isinstance(self.strategy_id, TeachingStrategyId):
            raise EducationalInvariantViolation(
                "strategy_id must be a TeachingStrategyId",
                invariant="MissionSpecification.strategy_id.type",
            )
        # Duration must equal sequence total (honest capacity).
        if self.duration.planned_minutes != self.sequence.total_estimated_minutes():
            raise EducationalInvariantViolation(
                "mission duration must equal the sum of task estimated minutes",
                invariant="MissionSpecification.duration.matches_sequence",
            )

    @property
    def ordered_tasks(self) -> tuple:
        return self.sequence.tasks

    def task_count(self) -> int:
        return self.sequence.length
