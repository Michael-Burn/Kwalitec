"""Instrument and session structural validation.

Architecture Source
    knowledge/product/AP-002/QUESTION_MODEL.md
    knowledge/product/AP-002/ASSESSMENT_LIFECYCLE.md
"""

from __future__ import annotations

from collections.abc import Sequence

from domain.assessment.exceptions import (
    AssessmentInvariantViolation,
    DuplicateQuestionReferenceError,
    MissingLearningObjectiveError,
)
from domain.assessment.value_objects.ids import QuestionId
from domain.assessment.value_objects.references import (
    LearningObjectiveReference,
    QuestionReference,
)
from domain.education.foundation.base import require_non_empty_text


def assert_student_id(student_id: str) -> str:
    return require_non_empty_text(student_id, "student_id")


def assert_question_references(
    references: Sequence[QuestionReference],
) -> tuple[QuestionReference, ...]:
    """Validate ordered question refs: non-empty, typed, no duplicate question ids."""
    if not references:
        raise AssessmentInvariantViolation(
            "at least one question reference is required",
            invariant="question_references.non_empty",
        )
    seen: set[str] = set()
    ordered: list[QuestionReference] = []
    for ref in references:
        if not isinstance(ref, QuestionReference):
            raise AssessmentInvariantViolation(
                "each item must be a QuestionReference",
                invariant="question_references.type",
            )
        key = ref.question_id.value
        if key in seen:
            raise DuplicateQuestionReferenceError(
                f"duplicate question reference: {key}"
            )
        seen.add(key)
        ordered.append(ref)
    return tuple(ordered)


def assert_learning_objectives(
    objectives: Sequence[LearningObjectiveReference],
) -> tuple[LearningObjectiveReference, ...]:
    """Require at least one learning objective reference."""
    if not objectives:
        raise MissingLearningObjectiveError(
            "at least one learning objective reference is required"
        )
    ordered: list[LearningObjectiveReference] = []
    seen: set[str] = set()
    for objective in objectives:
        if not isinstance(objective, LearningObjectiveReference):
            raise AssessmentInvariantViolation(
                "each objective must be a LearningObjectiveReference",
                invariant="learning_objectives.type",
            )
        key = objective.objective_id.value
        if key in seen:
            continue
        seen.add(key)
        ordered.append(objective)
    return tuple(ordered)


def assert_question_in_set(
    question_id: QuestionId,
    references: Sequence[QuestionReference],
) -> None:
    known = {ref.question_id.value for ref in references}
    if question_id.value not in known:
        raise AssessmentInvariantViolation(
            f"question_id {question_id.value} is not part of this session",
            invariant="session.question_membership",
        )
