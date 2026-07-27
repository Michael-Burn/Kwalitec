"""Assessment delivery orchestration service (AP-002B).

Creates sessions, sequences questions, captures responses as observations,
and packages an AssessmentResult. Stops before Educational Reasoning / Twin.
"""

from __future__ import annotations

import uuid
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from typing import Any

from application.assessment.commands.commands import (
    CancelAssessmentSessionCommand,
    CommitAssessmentResponseCommand,
    CreateAssessmentSessionCommand,
    NavigateAssessmentSessionCommand,
    PauseAssessmentSessionCommand,
    RequestAssessmentHintCommand,
    ResumeAssessmentSessionCommand,
    StartAssessmentSessionCommand,
    SubmitAssessmentSessionCommand,
)
from application.assessment.delivery.exceptions import (
    DuplicateSubmissionError,
    ExpiredSessionError,
    QuestionUnavailableError,
    SessionNotFoundError,
    SessionOwnershipError,
    SessionStateError,
)
from application.assessment.delivery.question_content import QuestionContent
from application.assessment.delivery.sequencing import (
    SessionDeliveryState,
    compute_progress,
)
from application.assessment.delivery.strategies import get_strategy
from application.assessment.dto.models import (
    AssessmentAttemptDTO,
    AssessmentDeliveryDTO,
    DeliveryProgressDTO,
    QuestionDeliveryDTO,
)
from application.assessment.mappers.mappers import (
    to_attempt_dto,
    to_result_dto,
    to_session_dto,
)
from application.assessment.ports.repositories import (
    AssessmentInstrumentRepository,
    AssessmentObservationRepository,
    AssessmentResultRepository,
    AssessmentSessionBuilder,
    AssessmentSessionRepository,
    QuestionContentRepository,
    SessionDeliveryStateRepository,
)
from domain.assessment.enums import (
    AssessmentStatus,
    EvidenceSource,
    HintPolicy,
    ObservationKind,
    RetryPolicy,
)
from domain.assessment.exceptions import (
    AssessmentInvariantViolation,
    InvalidAssessmentStateTransition,
)
from domain.assessment.factories import (
    AssessmentObservationFactory,
    AssessmentResultFactory,
)
from domain.assessment.value_objects.ids import (
    InstrumentId,
    ObservationId,
    QuestionId,
    ResultId,
    SessionId,
)
from domain.assessment.value_objects.levels import ConfidenceLevel

PURPOSE_COPY: dict[str, tuple[str, str]] = {
    "diagnostic": (
        "Learning Check",
        "This activity helps Kwalitec understand how to support you.",
    ),
    "formative_checkpoint": (
        "Knowledge Check",
        "A short checkpoint so today's plan stays accurate. No grades.",
    ),
    "adaptive_probe": (
        "Concept Check",
        "A quick probe to clarify what still feels solid.",
    ),
    "recovery_check": (
        "Checkpoint",
        "A gentle check after practice — useful signals, not a verdict.",
    ),
    "mastery_verification": (
        "Concept Check",
        "Helps confirm what is ready to reinforce next.",
    ),
    "revision_stability": (
        "Knowledge Check",
        "Checks whether ideas still feel stable after revision.",
    ),
    "reflection": (
        "Reflection",
        "A moment to notice how learning feels — not a test.",
    ),
}


class AssessmentDeliveryService:
    """Orchestrates student-facing assessment delivery without educational inference."""

    def __init__(
        self,
        *,
        sessions: AssessmentSessionRepository,
        instruments: AssessmentInstrumentRepository,
        observations: AssessmentObservationRepository,
        results: AssessmentResultRepository,
        question_content: QuestionContentRepository,
        delivery_state: SessionDeliveryStateRepository,
        session_builder: AssessmentSessionBuilder,
        default_instrument_id: str | None = None,
        clock: Callable[[], datetime] | None = None,
        id_factory: Callable[[str], str] | None = None,
    ) -> None:
        self._sessions = sessions
        self._instruments = instruments
        self._observations = observations
        self._results = results
        self._question_content = question_content
        self._delivery_state = delivery_state
        self._session_builder = session_builder
        self._default_instrument_id = default_instrument_id
        self._clock = clock or (lambda: datetime.now(UTC))
        self._id_factory = id_factory or (
            lambda prefix: f"{prefix}-{uuid.uuid4().hex[:12]}"
        )

    @property
    def default_instrument_id(self) -> str | None:
        return self._default_instrument_id

    def create_session(
        self, command: CreateAssessmentSessionCommand
    ) -> AssessmentDeliveryDTO:
        instrument = self._instruments.get(InstrumentId(command.instrument_id))
        if instrument is None:
            raise QuestionUnavailableError(
                f"instrument not found: {command.instrument_id}"
            )
        session = self._session_builder.build_from_instrument(
            session_id=SessionId(command.session_id),
            student_id=command.student_id,
            instrument=instrument,
            twin_id=command.twin_id,
            mission_id=command.mission_id,
        )
        session.mark_ready()
        self._sessions.save(session)
        now = self._clock()
        expires_at = None
        budget = session.configuration.time_budget_seconds
        if budget is not None:
            expires_at = now + timedelta(seconds=budget)
        state = SessionDeliveryState(
            session_id=session.session_id.value,
            current_index=0,
            started_at=None,
            expires_at=expires_at,
            allow_previous=True,
        )
        self._delivery_state.save(state)
        session.pull_events()
        return self.get_delivery(
            session.session_id.value, student_id=command.student_id
        )

    def start(
        self, command: StartAssessmentSessionCommand, *, student_id: str
    ) -> AssessmentDeliveryDTO:
        session = self._require_owned(command.session_id, student_id)
        self._assert_not_expired(session.session_id.value)
        try:
            if session.status is AssessmentStatus.READY:
                session.start()
            elif session.status is AssessmentStatus.PAUSED:
                session.resume()
            elif session.status is AssessmentStatus.IN_PROGRESS:
                pass
            else:
                raise SessionStateError(
                    f"cannot start session in status {session.status.value}"
                )
        except InvalidAssessmentStateTransition as exc:
            raise SessionStateError(str(exc)) from exc
        state = self._require_state(session.session_id.value)
        if state.started_at is None:
            state.started_at = self._clock()
        self._mark_question_visited(state, session)
        self._sessions.save(session)
        self._delivery_state.save(state)
        session.pull_events()
        return self.get_delivery(session.session_id.value, student_id=student_id)

    def pause(
        self, command: PauseAssessmentSessionCommand, *, student_id: str
    ) -> AssessmentDeliveryDTO:
        session = self._require_owned(command.session_id, student_id)
        self._assert_not_expired(session.session_id.value)
        try:
            session.pause()
        except (AssessmentInvariantViolation, InvalidAssessmentStateTransition) as exc:
            raise SessionStateError(str(exc)) from exc
        self._sessions.save(session)
        session.pull_events()
        return self.get_delivery(session.session_id.value, student_id=student_id)

    def resume(
        self, command: ResumeAssessmentSessionCommand, *, student_id: str
    ) -> AssessmentDeliveryDTO:
        session = self._require_owned(command.session_id, student_id)
        self._assert_not_expired(session.session_id.value)
        try:
            session.resume()
        except InvalidAssessmentStateTransition as exc:
            raise SessionStateError(str(exc)) from exc
        self._sessions.save(session)
        session.pull_events()
        return self.get_delivery(session.session_id.value, student_id=student_id)

    def cancel(
        self, command: CancelAssessmentSessionCommand, *, student_id: str
    ) -> AssessmentDeliveryDTO:
        session = self._require_owned(command.session_id, student_id)
        try:
            session.abandon()
        except InvalidAssessmentStateTransition as exc:
            raise SessionStateError(str(exc)) from exc
        self._sessions.save(session)
        session.pull_events()
        return self.get_delivery(session.session_id.value, student_id=student_id)

    def navigate(
        self, command: NavigateAssessmentSessionCommand, *, student_id: str
    ) -> AssessmentDeliveryDTO:
        session = self._require_owned(command.session_id, student_id)
        self._assert_active_delivery(session)
        state = self._require_state(session.session_id.value)
        total = len(session.questions)
        direction = command.direction.strip().lower()
        if direction == "next":
            if state.current_index >= total - 1:
                raise SessionStateError("already on the last question")
            state.current_index += 1
        elif direction == "previous":
            if not state.allow_previous or state.current_index <= 0:
                raise SessionStateError("cannot go to the previous question")
            state.current_index -= 1
        else:
            raise SessionStateError("direction must be 'next' or 'previous'")
        self._mark_question_visited(state, session)
        self._delivery_state.save(state)
        return self.get_delivery(session.session_id.value, student_id=student_id)

    def request_hint(
        self, command: RequestAssessmentHintCommand, *, student_id: str
    ) -> AssessmentDeliveryDTO:
        session = self._require_owned(command.session_id, student_id)
        self._assert_active_delivery(session)
        if session.configuration.hint_policy is HintPolicy.NONE:
            raise SessionStateError("hints are not available for this check")
        state = self._require_state(session.session_id.value)
        qid = command.question_id.strip()
        state.hints_requested[qid] = state.hints_requested.get(qid, 0) + 1
        self._delivery_state.save(state)
        return self.get_delivery(session.session_id.value, student_id=student_id)

    def commit_response(
        self, command: CommitAssessmentResponseCommand, *, student_id: str
    ) -> AssessmentAttemptDTO:
        session = self._require_owned(command.session_id, student_id)
        self._assert_active_delivery(session)
        question_id = QuestionId(command.question_id)
        content = self._require_content(command.question_id)
        strategy = get_strategy(content.item_type)

        if command.abandoned or command.skipped:
            payload: dict[str, Any] = {
                "item_type": content.item_type.value,
                "abandoned": command.abandoned,
                "skipped": command.skipped,
            }
        else:
            payload = strategy.map_response(command.response_payload, content)

        state = self._require_state(session.session_id.value)
        hints_used = max(
            command.hints_used,
            state.hints_requested.get(command.question_id, 0),
        )
        response_time_ms = command.response_time_ms
        started = state.question_started_at.get(command.question_id)
        if response_time_ms is None and started is not None:
            delta = self._clock() - started
            response_time_ms = max(0, int(delta.total_seconds() * 1000))

        confidence = None
        if command.confidence is not None:
            confidence = ConfidenceLevel(command.confidence)
        elif (
            content.item_type.value == "confidence_rating"
            and "confidence" in payload
            and session.configuration.invite_confidence
        ):
            confidence = ConfidenceLevel(int(payload["confidence"]))

        answered = {
            attempt.question_id.value
            for attempt in session.attempts
            if attempt.committed and not attempt.abandoned
        }
        if (
            command.question_id in answered
            and session.configuration.retry_policy is RetryPolicy.NONE
            and not (command.abandoned or command.skipped)
        ):
            raise DuplicateSubmissionError(
                "this question already has a committed response"
            )

        try:
            attempt = session.commit_response(
                question_id,
                response_payload=payload,
                confidence=confidence,
                response_time_ms=response_time_ms,
                hints_used=hints_used,
                retries=command.retries,
                abandoned=command.abandoned,
                skipped=command.skipped,
            )
        except AssessmentInvariantViolation as exc:
            if "retry" in (exc.invariant or ""):
                raise DuplicateSubmissionError(str(exc)) from exc
            raise SessionStateError(str(exc)) from exc

        # Advance cursor when one-item-at-a-time and not on last unanswered
        question_ids = [q.question_id.value for q in session.questions]
        if (
            session.configuration.one_item_at_a_time
            and state.current_index < len(question_ids) - 1
            and command.question_id == question_ids[state.current_index]
            and not command.abandoned
        ):
            state.current_index += 1
            self._mark_question_visited(state, session)

        self._sessions.save(session)
        self._delivery_state.save(state)
        session.pull_events()
        return to_attempt_dto(attempt)

    def complete(
        self, command: SubmitAssessmentSessionCommand, *, student_id: str
    ) -> AssessmentDeliveryDTO:
        """Submit session, record local observations, package AssessmentResult."""
        session = self._require_owned(command.session_id, student_id)
        self._assert_not_expired(session.session_id.value)
        if session.status is AssessmentStatus.SUBMITTED:
            return self.get_delivery(session.session_id.value, student_id=student_id)
        if session.status is not AssessmentStatus.IN_PROGRESS:
            raise SessionStateError(
                f"cannot complete session in status {session.status.value}"
            )
        try:
            session.submit()
        except AssessmentInvariantViolation as exc:
            raise SessionStateError(str(exc)) from exc

        observation_ids: list[ObservationId] = []
        for attempt in session.attempts:
            if not attempt.committed:
                continue
            observation = AssessmentObservationFactory.create(
                observation_id=ObservationId(self._id_factory("obs")),
                session_id=session.session_id,
                kind=ObservationKind.QUESTION_ANSWERED,
                evidence_source=EvidenceSource.STUDENT_RESPONSE,
                question_id=attempt.question_id,
                provenance={
                    "response_payload": dict(attempt.response_payload),
                    "confidence": (
                        attempt.confidence.value if attempt.confidence else None
                    ),
                    "response_time_ms": attempt.response_time_ms,
                    "hints_used": attempt.hints_used,
                    "retries": attempt.retries,
                    "attempt_number": attempt.attempt_number.value,
                    "abandoned": attempt.abandoned,
                    "skipped": attempt.skipped,
                    "engine": "assessment_delivery",
                    "milestone": "AP-002B",
                },
            )
            self._observations.save(observation)
            session.record_observation(observation)
            observation_ids.append(observation.observation_id)

        quiz_observation = AssessmentObservationFactory.create(
            observation_id=ObservationId(self._id_factory("obs")),
            session_id=session.session_id,
            kind=ObservationKind.QUIZ_COMPLETED,
            evidence_source=EvidenceSource.SESSION_SUMMARY,
            provenance={
                "attempt_count": len(session.attempts),
                "observation_count": len(observation_ids),
                "engine": "assessment_delivery",
                "milestone": "AP-002B",
            },
        )
        self._observations.save(quiz_observation)
        session.record_observation(quiz_observation)
        observation_ids.append(quiz_observation.observation_id)

        result = AssessmentResultFactory.create(
            result_id=ResultId(self._id_factory("result")),
            session_id=session.session_id,
            observation_ids=observation_ids,
        )
        self._results.save(result)
        self._sessions.save(session)
        session.pull_events()
        return self.get_delivery(session.session_id.value, student_id=student_id)

    def get_delivery(
        self, session_id: str, *, student_id: str
    ) -> AssessmentDeliveryDTO:
        session = self._require_owned(session_id, student_id)
        instrument = self._instruments.get(session.instrument_id)
        title = (
            instrument.metadata.title
            if instrument is not None
            else "Learning Check"
        )
        purpose = session.purpose.value
        purpose_label, purpose_explanation = PURPOSE_COPY.get(
            purpose,
            (
                "Learning Check",
                "This activity helps Kwalitec understand how to support you.",
            ),
        )
        state = self._delivery_state.get(session_id) or SessionDeliveryState(
            session_id=session_id
        )
        question_ids = tuple(q.question_id.value for q in session.questions)
        answered = {
            attempt.question_id.value
            for attempt in session.attempts
            if attempt.committed and not attempt.abandoned
        }
        submitted = session.status in {
            AssessmentStatus.SUBMITTED,
            AssessmentStatus.OBSERVED,
            AssessmentStatus.REASONED,
            AssessmentStatus.CLOSED,
        }
        progress = compute_progress(
            question_ids=question_ids,
            answered_question_ids=answered,
            current_index=state.current_index,
            allow_previous=state.allow_previous,
            session_submitted=submitted,
        )
        question_dto = None
        if progress.current_question_id and not submitted:
            question_dto = self._build_question_dto(
                session=session,
                state=state,
                question_id=progress.current_question_id,
                answered=answered,
            )
        result = self._results.get_by_session(session.session_id)
        result_dto = to_result_dto(result) if result is not None else None
        return AssessmentDeliveryDTO(
            session=to_session_dto(session),
            progress=DeliveryProgressDTO(
                current_index=progress.current_index,
                total_questions=progress.total_questions,
                answered_count=progress.answered_count,
                remaining_count=progress.remaining_count,
                percent_complete=progress.percent_complete,
                current_question_id=progress.current_question_id,
                can_go_previous=progress.can_go_previous,
                can_go_next=progress.can_go_next,
                can_complete=progress.can_complete,
                is_complete=progress.is_complete,
            ),
            instrument_title=title,
            purpose_label=purpose_label,
            purpose_explanation=purpose_explanation,
            allow_pause=session.configuration.allow_pause,
            status=session.status.value,
            question=question_dto,
            result=result_dto,
            observation_count=len(session.observation_ids),
        )

    def list_instruments(self) -> list[str]:
        """Return seeded instrument ids (delivery catalogue)."""
        # Port has list_by_purpose only; seed stores under known purposes.
        from domain.assessment.enums import AssessmentPurpose

        seen: list[str] = []
        for purpose in AssessmentPurpose:
            for instrument in self._instruments.list_by_purpose(purpose):
                iid = instrument.instrument_id.value
                if iid not in seen:
                    seen.append(iid)
        return seen

    def _build_question_dto(
        self,
        *,
        session,
        state: SessionDeliveryState,
        question_id: str,
        answered: set[str],
    ) -> QuestionDeliveryDTO:
        content = self._require_content(question_id)
        strategy = get_strategy(content.item_type)
        model = strategy.presentation_model(content)
        index = next(
            (
                item.sequence_index
                for item in session.questions
                if item.question_id.value == question_id
            ),
            0,
        )
        hints_available = (
            session.configuration.hint_policy is not HintPolicy.NONE
            and bool(content.hints)
        )
        return QuestionDeliveryDTO(
            question_id=model.question_id,
            item_type=model.item_type,
            stem=model.stem,
            version=model.version,
            sequence_index=index,
            options=model.options,
            hints=content.hints if state.hints_requested.get(question_id, 0) else (),
            placeholder=model.placeholder,
            unit_label=model.unit_label,
            accessibility_note=model.accessibility_note,
            input_name=model.input_name,
            allows_multiple=model.allows_multiple,
            is_numeric=model.is_numeric,
            is_text=model.is_text,
            is_confidence_only=model.is_confidence_only,
            invite_confidence=session.configuration.invite_confidence,
            require_confidence=session.configuration.require_confidence,
            hints_available=hints_available,
            hints_requested=state.hints_requested.get(question_id, 0),
            already_answered=question_id in answered,
            visited=question_id in state.visited_question_ids,
        )

    def _require_owned(self, session_id: str, student_id: str):
        session = self._sessions.get(SessionId(session_id))
        if session is None:
            raise SessionNotFoundError(f"session not found: {session_id}")
        if session.student_id != student_id:
            raise SessionOwnershipError(
                f"session {session_id} is not owned by student {student_id}"
            )
        return session

    def _require_state(self, session_id: str) -> SessionDeliveryState:
        state = self._delivery_state.get(session_id)
        if state is None:
            state = SessionDeliveryState(session_id=session_id)
            self._delivery_state.save(state)
        return state

    def _require_content(self, question_id: str) -> QuestionContent:
        content = self._question_content.get(question_id)
        if content is None:
            raise QuestionUnavailableError(f"question content not found: {question_id}")
        if not isinstance(content, QuestionContent):
            raise QuestionUnavailableError(
                f"invalid question content for: {question_id}"
            )
        return content

    def _assert_not_expired(self, session_id: str) -> None:
        state = self._delivery_state.get(session_id)
        if state is None or state.expires_at is None:
            return
        if self._clock() > state.expires_at:
            raise ExpiredSessionError("this learning check has expired")

    def _assert_active_delivery(self, session) -> None:
        self._assert_not_expired(session.session_id.value)
        if session.status is not AssessmentStatus.IN_PROGRESS:
            raise SessionStateError(
                f"session must be in_progress (was {session.status.value})"
            )

    def _mark_question_visited(self, state: SessionDeliveryState, session) -> None:
        if not session.questions:
            return
        index = max(0, min(state.current_index, len(session.questions) - 1))
        qid = session.questions[index].question_id.value
        if qid not in state.visited_question_ids:
            state.visited_question_ids.append(qid)
        state.question_started_at.setdefault(qid, self._clock())
