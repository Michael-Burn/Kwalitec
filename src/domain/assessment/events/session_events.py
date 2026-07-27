"""Lightweight assessment domain events.

Architecture Source
    knowledge/product/AP-002/ASSESSMENT_LIFECYCLE.md
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.assessment.enums import AssessmentPurpose, AssessmentStatus, ObservationKind
from domain.assessment.exceptions import AssessmentInvariantViolation
from domain.assessment.value_objects.ids import (
    InstrumentId,
    ObservationId,
    QuestionId,
    SessionId,
)
from domain.education.foundation.base import EducationalValueObject


@dataclass(frozen=True, slots=True)
class AssessmentSessionConstructed(EducationalValueObject):
    """Session constructed after instrument selection."""

    session_id: SessionId
    instrument_id: InstrumentId
    purpose: AssessmentPurpose
    status: AssessmentStatus

    def _validate(self) -> None:
        if not isinstance(self.session_id, SessionId):
            raise AssessmentInvariantViolation(
                "session_id must be a SessionId",
                invariant="AssessmentSessionConstructed.session_id.type",
            )
        if not isinstance(self.instrument_id, InstrumentId):
            raise AssessmentInvariantViolation(
                "instrument_id must be an InstrumentId",
                invariant="AssessmentSessionConstructed.instrument_id.type",
            )
        if not isinstance(self.purpose, AssessmentPurpose):
            raise AssessmentInvariantViolation(
                "purpose must be an AssessmentPurpose",
                invariant="AssessmentSessionConstructed.purpose.type",
            )
        if not isinstance(self.status, AssessmentStatus):
            raise AssessmentInvariantViolation(
                "status must be an AssessmentStatus",
                invariant="AssessmentSessionConstructed.status.type",
            )


@dataclass(frozen=True, slots=True)
class AssessmentSessionStarted(EducationalValueObject):
    """Session entered in_progress (delivery begun)."""

    session_id: SessionId

    def _validate(self) -> None:
        if not isinstance(self.session_id, SessionId):
            raise AssessmentInvariantViolation(
                "session_id must be a SessionId",
                invariant="AssessmentSessionStarted.session_id.type",
            )


@dataclass(frozen=True, slots=True)
class AssessmentResponseCommitted(EducationalValueObject):
    """Raw response committed for an item (immutable thereafter)."""

    session_id: SessionId
    question_id: QuestionId
    attempt_number: int

    def _validate(self) -> None:
        if not isinstance(self.session_id, SessionId):
            raise AssessmentInvariantViolation(
                "session_id must be a SessionId",
                invariant="AssessmentResponseCommitted.session_id.type",
            )
        if not isinstance(self.question_id, QuestionId):
            raise AssessmentInvariantViolation(
                "question_id must be a QuestionId",
                invariant="AssessmentResponseCommitted.question_id.type",
            )
        if (
            not isinstance(self.attempt_number, int)
            or isinstance(self.attempt_number, bool)
            or self.attempt_number < 1
        ):
            raise AssessmentInvariantViolation(
                "attempt_number must be >= 1",
                invariant="AssessmentResponseCommitted.attempt_number.range",
            )


@dataclass(frozen=True, slots=True)
class AssessmentSessionSubmitted(EducationalValueObject):
    """Session responses submitted for observation emission."""

    session_id: SessionId

    def _validate(self) -> None:
        if not isinstance(self.session_id, SessionId):
            raise AssessmentInvariantViolation(
                "session_id must be a SessionId",
                invariant="AssessmentSessionSubmitted.session_id.type",
            )


@dataclass(frozen=True, slots=True)
class AssessmentObservationRecorded(EducationalValueObject):
    """Observation fact recorded for a session (AP-001 emission deferred)."""

    session_id: SessionId
    observation_id: ObservationId
    kind: ObservationKind

    def _validate(self) -> None:
        if not isinstance(self.session_id, SessionId):
            raise AssessmentInvariantViolation(
                "session_id must be a SessionId",
                invariant="AssessmentObservationRecorded.session_id.type",
            )
        if not isinstance(self.observation_id, ObservationId):
            raise AssessmentInvariantViolation(
                "observation_id must be an ObservationId",
                invariant="AssessmentObservationRecorded.observation_id.type",
            )
        if not isinstance(self.kind, ObservationKind):
            raise AssessmentInvariantViolation(
                "kind must be an ObservationKind",
                invariant="AssessmentObservationRecorded.kind.type",
            )


@dataclass(frozen=True, slots=True)
class AssessmentSessionClosed(EducationalValueObject):
    """Session reached a terminal closed status."""

    session_id: SessionId
    status: AssessmentStatus

    def _validate(self) -> None:
        if not isinstance(self.session_id, SessionId):
            raise AssessmentInvariantViolation(
                "session_id must be a SessionId",
                invariant="AssessmentSessionClosed.session_id.type",
            )
        if not isinstance(self.status, AssessmentStatus):
            raise AssessmentInvariantViolation(
                "status must be an AssessmentStatus",
                invariant="AssessmentSessionClosed.status.type",
            )
        if self.status not in {
            AssessmentStatus.CLOSED,
            AssessmentStatus.ABANDONED,
            AssessmentStatus.INVALIDATED,
        }:
            raise AssessmentInvariantViolation(
                "closed event status must be a terminal status",
                invariant="AssessmentSessionClosed.status.terminal",
            )
