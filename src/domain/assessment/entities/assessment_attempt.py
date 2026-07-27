"""Assessment question reference and attempt entities.

Architecture Source
    knowledge/product/AP-002/QUESTION_MODEL.md
    knowledge/product/AP-002/ASSESSMENT_LIFECYCLE.md §2.6
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from domain.assessment.enums import AttemptOutcome
from domain.assessment.exceptions import AssessmentInvariantViolation
from domain.assessment.value_objects.ids import AttemptNumber, QuestionId, SessionId
from domain.assessment.value_objects.levels import ConfidenceLevel
from domain.assessment.value_objects.references import QuestionReference
from domain.education.foundation.base import EducationalEntity


@dataclass(frozen=True, slots=True, eq=False)
class AssessmentQuestionReference(EducationalEntity):
    """Ordered question reference within an instrument or session."""

    reference: QuestionReference
    sequence_index: int

    @property
    def entity_id(self) -> QuestionId:
        return self.reference.question_id

    @property
    def question_id(self) -> QuestionId:
        return self.reference.question_id

    def _validate(self) -> None:
        if not isinstance(self.reference, QuestionReference):
            raise AssessmentInvariantViolation(
                "reference must be a QuestionReference",
                invariant="AssessmentQuestionReference.reference.type",
            )
        if (
            not isinstance(self.sequence_index, int)
            or isinstance(self.sequence_index, bool)
            or self.sequence_index < 0
        ):
            raise AssessmentInvariantViolation(
                "sequence_index must be a non-negative integer",
                invariant="AssessmentQuestionReference.sequence_index.range",
            )


@dataclass(frozen=True, slots=True, eq=False)
class AssessmentAttempt(EducationalEntity):
    """Response attempt for one question in a session.

    Once ``committed`` is True, a new instance must be created to change
    evaluation outcome; raw payload remains fixed.
    """

    session_id: SessionId
    question_id: QuestionId
    attempt_number: AttemptNumber
    response_payload: Mapping[str, Any] = MappingProxyType({})
    confidence: ConfidenceLevel | None = None
    response_time_ms: int | None = None
    hints_used: int = 0
    retries: int = 0
    outcome: AttemptOutcome | None = None
    abandoned: bool = False
    skipped: bool = False
    committed: bool = False

    @property
    def entity_id(self) -> AttemptNumber:
        return self.attempt_number

    def _validate(self) -> None:
        if not isinstance(self.session_id, SessionId):
            raise AssessmentInvariantViolation(
                "session_id must be a SessionId",
                invariant="AssessmentAttempt.session_id.type",
            )
        if not isinstance(self.question_id, QuestionId):
            raise AssessmentInvariantViolation(
                "question_id must be a QuestionId",
                invariant="AssessmentAttempt.question_id.type",
            )
        if not isinstance(self.attempt_number, AttemptNumber):
            raise AssessmentInvariantViolation(
                "attempt_number must be an AttemptNumber",
                invariant="AssessmentAttempt.attempt_number.type",
            )
        object.__setattr__(
            self,
            "response_payload",
            MappingProxyType(dict(self.response_payload or {})),
        )
        if self.confidence is not None and not isinstance(
            self.confidence, ConfidenceLevel
        ):
            raise AssessmentInvariantViolation(
                "confidence must be a ConfidenceLevel when provided",
                invariant="AssessmentAttempt.confidence.type",
            )
        if self.response_time_ms is not None and (
            not isinstance(self.response_time_ms, int)
            or isinstance(self.response_time_ms, bool)
            or self.response_time_ms < 0
        ):
            raise AssessmentInvariantViolation(
                "response_time_ms must be a non-negative integer",
                invariant="AssessmentAttempt.response_time_ms.range",
            )
        if (
            not isinstance(self.hints_used, int)
            or isinstance(self.hints_used, bool)
            or self.hints_used < 0
        ):
            raise AssessmentInvariantViolation(
                "hints_used must be a non-negative integer",
                invariant="AssessmentAttempt.hints_used.range",
            )
        if (
            not isinstance(self.retries, int)
            or isinstance(self.retries, bool)
            or self.retries < 0
        ):
            raise AssessmentInvariantViolation(
                "retries must be a non-negative integer",
                invariant="AssessmentAttempt.retries.range",
            )
        if self.outcome is not None and not isinstance(self.outcome, AttemptOutcome):
            raise AssessmentInvariantViolation(
                "outcome must be an AttemptOutcome when provided",
                invariant="AssessmentAttempt.outcome.type",
            )
        if self.abandoned and self.skipped:
            raise AssessmentInvariantViolation(
                "attempt cannot be both abandoned and skipped",
                invariant="AssessmentAttempt.flags.exclusive",
            )

    def commit(self) -> AssessmentAttempt:
        """Return this attempt frozen as committed."""
        if self.committed:
            raise AssessmentInvariantViolation(
                "attempt is already committed",
                invariant="AssessmentAttempt.commit.already",
            )
        return AssessmentAttempt(
            session_id=self.session_id,
            question_id=self.question_id,
            attempt_number=self.attempt_number,
            response_payload=self.response_payload,
            confidence=self.confidence,
            response_time_ms=self.response_time_ms,
            hints_used=self.hints_used,
            retries=self.retries,
            outcome=self.outcome,
            abandoned=self.abandoned,
            skipped=self.skipped,
            committed=True,
        )

    def with_outcome(self, outcome: AttemptOutcome) -> AssessmentAttempt:
        """Return a committed attempt with an evaluation label (evidence only)."""
        if not self.committed:
            raise AssessmentInvariantViolation(
                "cannot assign outcome before commit",
                invariant="AssessmentAttempt.outcome.requires_commit",
            )
        if self.outcome is not None:
            raise AssessmentInvariantViolation(
                "outcome is already assigned",
                invariant="AssessmentAttempt.outcome.immutable",
            )
        if not isinstance(outcome, AttemptOutcome):
            raise AssessmentInvariantViolation(
                "outcome must be an AttemptOutcome",
                invariant="AssessmentAttempt.outcome.type",
            )
        return AssessmentAttempt(
            session_id=self.session_id,
            question_id=self.question_id,
            attempt_number=self.attempt_number,
            response_payload=self.response_payload,
            confidence=self.confidence,
            response_time_ms=self.response_time_ms,
            hints_used=self.hints_used,
            retries=self.retries,
            outcome=outcome,
            abandoned=self.abandoned,
            skipped=self.skipped,
            committed=True,
        )
