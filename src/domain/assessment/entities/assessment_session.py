"""AssessmentSession aggregate — lifecycle for evidence collection.

Architecture Source
    knowledge/product/AP-002/ASSESSMENT_LIFECYCLE.md
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from domain.assessment.entities.assessment_attempt import (
    AssessmentAttempt,
    AssessmentQuestionReference,
)
from domain.assessment.entities.assessment_observation import AssessmentObservation
from domain.assessment.enums import AssessmentPurpose, AssessmentStatus, AssessmentType
from domain.assessment.events.session_events import (
    AssessmentObservationRecorded,
    AssessmentResponseCommitted,
    AssessmentSessionClosed,
    AssessmentSessionConstructed,
    AssessmentSessionStarted,
    AssessmentSessionSubmitted,
)
from domain.assessment.exceptions import AssessmentInvariantViolation
from domain.assessment.validation.instrument_validation import (
    assert_question_in_set,
    assert_question_references,
    assert_student_id,
)
from domain.assessment.validation.state_transitions import assert_can_transition
from domain.assessment.value_objects.configuration import (
    AssessmentConfiguration,
    AssessmentMetadata,
)
from domain.assessment.value_objects.ids import (
    AttemptNumber,
    InstrumentId,
    QuestionId,
    SessionId,
)
from domain.assessment.value_objects.levels import ConfidenceLevel
from domain.assessment.value_objects.references import QuestionReference

DomainEvent = (
    AssessmentSessionConstructed
    | AssessmentSessionStarted
    | AssessmentResponseCommitted
    | AssessmentSessionSubmitted
    | AssessmentObservationRecorded
    | AssessmentSessionClosed
)


class AssessmentSession:
    """Aggregate root for one assessment evidence-collection run.

    Owns ordered items, committed attempts, and lifecycle status. Does not
    call Educational Reasoning, update the Twin, or emit AP-001 events.
    """

    def __init__(
        self,
        session_id: SessionId,
        student_id: str,
        instrument_id: InstrumentId,
        purpose: AssessmentPurpose,
        assessment_type: AssessmentType,
        questions: Sequence[QuestionReference],
        *,
        configuration: AssessmentConfiguration | None = None,
        metadata: AssessmentMetadata | None = None,
        twin_id: str | None = None,
        mission_id: str | None = None,
        status: AssessmentStatus = AssessmentStatus.DRAFT,
        attempts: Sequence[AssessmentAttempt] | None = None,
        observation_ids: Sequence[str] | None = None,
        _record_constructed: bool = False,
    ) -> None:
        if not isinstance(session_id, SessionId):
            raise AssessmentInvariantViolation(
                "session_id must be a SessionId",
                invariant="AssessmentSession.session_id.type",
            )
        if not isinstance(instrument_id, InstrumentId):
            raise AssessmentInvariantViolation(
                "instrument_id must be an InstrumentId",
                invariant="AssessmentSession.instrument_id.type",
            )
        if not isinstance(purpose, AssessmentPurpose):
            raise AssessmentInvariantViolation(
                "purpose must be an AssessmentPurpose",
                invariant="AssessmentSession.purpose.type",
            )
        if not isinstance(assessment_type, AssessmentType):
            raise AssessmentInvariantViolation(
                "assessment_type must be an AssessmentType",
                invariant="AssessmentSession.assessment_type.type",
            )
        if not isinstance(status, AssessmentStatus):
            raise AssessmentInvariantViolation(
                "status must be an AssessmentStatus",
                invariant="AssessmentSession.status.type",
            )
        self._session_id = session_id
        self._student_id = assert_student_id(student_id)
        self._instrument_id = instrument_id
        self._purpose = purpose
        self._assessment_type = assessment_type
        refs = assert_question_references(questions)
        self._questions = tuple(
            AssessmentQuestionReference(reference=ref, sequence_index=index)
            for index, ref in enumerate(refs)
        )
        self._configuration = configuration or AssessmentConfiguration()
        if not isinstance(self._configuration, AssessmentConfiguration):
            raise AssessmentInvariantViolation(
                "configuration must be an AssessmentConfiguration",
                invariant="AssessmentSession.configuration.type",
            )
        self._metadata = metadata
        if metadata is not None and not isinstance(metadata, AssessmentMetadata):
            raise AssessmentInvariantViolation(
                "metadata must be an AssessmentMetadata when provided",
                invariant="AssessmentSession.metadata.type",
            )
        self._twin_id = twin_id.strip() if twin_id else None
        self._mission_id = mission_id.strip() if mission_id else None
        self._status = status
        self._attempts: list[AssessmentAttempt] = list(attempts or ())
        self._observation_ids: list[str] = list(observation_ids or ())
        self._pending_events: list[DomainEvent] = []
        if _record_constructed:
            self._pending_events.append(
                AssessmentSessionConstructed(
                    session_id=self._session_id,
                    instrument_id=self._instrument_id,
                    purpose=self._purpose,
                    status=self._status,
                )
            )

    @classmethod
    def create(
        cls,
        session_id: SessionId,
        student_id: str,
        instrument_id: InstrumentId,
        purpose: AssessmentPurpose,
        assessment_type: AssessmentType,
        questions: Sequence[QuestionReference],
        *,
        configuration: AssessmentConfiguration | None = None,
        metadata: AssessmentMetadata | None = None,
        twin_id: str | None = None,
        mission_id: str | None = None,
    ) -> AssessmentSession:
        """Factory: construct a DRAFT session ready for eligibility checks."""
        return cls(
            session_id=session_id,
            student_id=student_id,
            instrument_id=instrument_id,
            purpose=purpose,
            assessment_type=assessment_type,
            questions=questions,
            configuration=configuration,
            metadata=metadata,
            twin_id=twin_id,
            mission_id=mission_id,
            status=AssessmentStatus.DRAFT,
            _record_constructed=True,
        )

    # --- reads ---

    @property
    def session_id(self) -> SessionId:
        return self._session_id

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def instrument_id(self) -> InstrumentId:
        return self._instrument_id

    @property
    def purpose(self) -> AssessmentPurpose:
        return self._purpose

    @property
    def assessment_type(self) -> AssessmentType:
        return self._assessment_type

    @property
    def questions(self) -> tuple[AssessmentQuestionReference, ...]:
        return self._questions

    @property
    def question_references(self) -> tuple[QuestionReference, ...]:
        return tuple(item.reference for item in self._questions)

    @property
    def configuration(self) -> AssessmentConfiguration:
        return self._configuration

    @property
    def metadata(self) -> AssessmentMetadata | None:
        return self._metadata

    @property
    def twin_id(self) -> str | None:
        return self._twin_id

    @property
    def mission_id(self) -> str | None:
        return self._mission_id

    @property
    def status(self) -> AssessmentStatus:
        return self._status

    @property
    def attempts(self) -> tuple[AssessmentAttempt, ...]:
        return tuple(self._attempts)

    @property
    def observation_ids(self) -> tuple[str, ...]:
        return tuple(self._observation_ids)

    def pull_events(self) -> list[DomainEvent]:
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    # --- lifecycle ---

    def mark_ready(self) -> None:
        self._transition_to(AssessmentStatus.READY)

    def start(self) -> None:
        self._transition_to(AssessmentStatus.IN_PROGRESS)
        self._pending_events.append(
            AssessmentSessionStarted(session_id=self._session_id)
        )

    def pause(self) -> None:
        if not self._configuration.allow_pause:
            raise AssessmentInvariantViolation(
                "pause is not allowed by session configuration",
                invariant="AssessmentSession.pause.forbidden",
            )
        self._transition_to(AssessmentStatus.PAUSED)

    def resume(self) -> None:
        self._transition_to(AssessmentStatus.IN_PROGRESS)

    def submit(self) -> None:
        if not any(attempt.committed for attempt in self._attempts):
            raise AssessmentInvariantViolation(
                "cannot submit a session with no committed attempts",
                invariant="AssessmentSession.submit.no_attempts",
            )
        self._transition_to(AssessmentStatus.SUBMITTED)
        self._pending_events.append(
            AssessmentSessionSubmitted(session_id=self._session_id)
        )

    def mark_observed(self) -> None:
        """Advance after observations are recorded (AP-001 emission deferred)."""
        self._transition_to(AssessmentStatus.OBSERVED)

    def mark_reasoned(self) -> None:
        """Advance after Reasoning consumed observations (ownership outside Engine)."""
        self._transition_to(AssessmentStatus.REASONED)

    def close(self) -> None:
        self._transition_to(AssessmentStatus.CLOSED)
        self._pending_events.append(
            AssessmentSessionClosed(
                session_id=self._session_id, status=AssessmentStatus.CLOSED
            )
        )

    def abandon(self) -> None:
        self._transition_to(AssessmentStatus.ABANDONED)
        self._pending_events.append(
            AssessmentSessionClosed(
                session_id=self._session_id, status=AssessmentStatus.ABANDONED
            )
        )

    def invalidate(self) -> None:
        self._transition_to(AssessmentStatus.INVALIDATED)
        self._pending_events.append(
            AssessmentSessionClosed(
                session_id=self._session_id, status=AssessmentStatus.INVALIDATED
            )
        )

    def commit_response(
        self,
        question_id: QuestionId,
        *,
        response_payload: Mapping[str, Any] | None = None,
        confidence: ConfidenceLevel | None = None,
        response_time_ms: int | None = None,
        hints_used: int = 0,
        retries: int = 0,
        abandoned: bool = False,
        skipped: bool = False,
    ) -> AssessmentAttempt:
        """Commit an immutable response for a session question."""
        if self._status is not AssessmentStatus.IN_PROGRESS:
            raise AssessmentInvariantViolation(
                "responses may only be committed while in_progress",
                invariant="AssessmentSession.commit_response.status",
            )
        assert_question_in_set(question_id, self.question_references)
        if self._configuration.require_confidence and confidence is None and not (
            abandoned or skipped
        ):
            raise AssessmentInvariantViolation(
                "confidence is required by session configuration",
                invariant="AssessmentSession.commit_response.confidence_required",
            )
        if (
            not self._configuration.invite_confidence
            and confidence is not None
        ):
            raise AssessmentInvariantViolation(
                "confidence is not invited by session configuration",
                invariant="AssessmentSession.commit_response.confidence_forbidden",
            )
        attempt_number = self._next_attempt_number(question_id)
        if (
            self._configuration.retry_policy.value == "none"
            and attempt_number.value > 1
        ):
            raise AssessmentInvariantViolation(
                "retries are not permitted by configuration",
                invariant="AssessmentSession.commit_response.retry_forbidden",
            )
        if (
            self._configuration.retry_policy.value == "limited"
            and self._configuration.max_retries is not None
            and attempt_number.value > self._configuration.max_retries + 1
        ):
            raise AssessmentInvariantViolation(
                "retry limit exceeded",
                invariant="AssessmentSession.commit_response.retry_limit",
            )
        draft = AssessmentAttempt(
            session_id=self._session_id,
            question_id=question_id,
            attempt_number=attempt_number,
            response_payload=response_payload or {},
            confidence=confidence,
            response_time_ms=response_time_ms,
            hints_used=hints_used,
            retries=retries,
            abandoned=abandoned,
            skipped=skipped,
            committed=False,
        )
        committed = draft.commit()
        self._attempts.append(committed)
        self._pending_events.append(
            AssessmentResponseCommitted(
                session_id=self._session_id,
                question_id=question_id,
                attempt_number=committed.attempt_number.value,
            )
        )
        return committed

    def record_observation(self, observation: AssessmentObservation) -> None:
        """Attach a recorded observation id for audit (does not emit AP-001)."""
        if self._status not in {
            AssessmentStatus.SUBMITTED,
            AssessmentStatus.OBSERVED,
        }:
            raise AssessmentInvariantViolation(
                "observations may only be recorded after submit",
                invariant="AssessmentSession.record_observation.status",
            )
        if not isinstance(observation, AssessmentObservation):
            raise AssessmentInvariantViolation(
                "observation must be an AssessmentObservation",
                invariant="AssessmentSession.record_observation.type",
            )
        if observation.session_id != self._session_id:
            raise AssessmentInvariantViolation(
                "observation session_id must match this session",
                invariant="AssessmentSession.record_observation.session",
            )
        oid = observation.observation_id.value
        if oid in self._observation_ids:
            raise AssessmentInvariantViolation(
                "observation already recorded on session",
                invariant="AssessmentSession.record_observation.duplicate",
            )
        self._observation_ids.append(oid)
        self._pending_events.append(
            AssessmentObservationRecorded(
                session_id=self._session_id,
                observation_id=observation.observation_id,
                kind=observation.kind,
            )
        )

    def _next_attempt_number(self, question_id: QuestionId) -> AttemptNumber:
        count = sum(
            1 for attempt in self._attempts if attempt.question_id == question_id
        )
        return AttemptNumber(count + 1)

    def _transition_to(self, target: AssessmentStatus) -> None:
        assert_can_transition(self._status, target)
        self._status = target
