"""Assessment application services (AP-002B delivery + AP-002C evidence packaging).

Evidence packaging is handled by ``EvidencePackagingService``.
No Twin updates, Reasoning, Mission, or Tutor behaviour.
"""

from __future__ import annotations

from application.assessment.commands.commands import (
    CommitAssessmentResponseCommand,
    CreateAssessmentSessionCommand,
    RecordAssessmentObservationCommand,
    StartAssessmentSessionCommand,
    SubmitAssessmentSessionCommand,
)
from application.assessment.delivery.exceptions import SessionNotFoundError
from application.assessment.dto.models import (
    AssessmentAttemptDTO,
    AssessmentInstrumentDTO,
    AssessmentObservationDTO,
    AssessmentSessionDTO,
)
from application.assessment.mappers.mappers import (
    to_attempt_dto,
    to_instrument_dto,
    to_observation_dto,
    to_session_dto,
)
from application.assessment.ports.repositories import (
    AssessmentInstrumentRepository,
    AssessmentObservationRepository,
    AssessmentSessionBuilder,
    AssessmentSessionRepository,
)
from application.assessment.queries.queries import (
    GetAssessmentInstrumentQuery,
    GetAssessmentSessionQuery,
    ListObservationsForSessionQuery,
    ListStudentAssessmentSessionsQuery,
)
from domain.assessment.enums import EvidenceSource, ObservationKind
from domain.assessment.factories import AssessmentObservationFactory
from domain.assessment.value_objects.ids import (
    InstrumentId,
    ObservationId,
    QuestionId,
    SessionId,
)
from domain.assessment.value_objects.levels import ConfidenceLevel


class AssessmentService:
    """Facade coordinating assessment application use cases."""

    def __init__(
        self,
        sessions: AssessmentSessionRepository,
        instruments: AssessmentInstrumentRepository,
        observations: AssessmentObservationRepository,
        *,
        session_builder: AssessmentSessionBuilder | None = None,
    ) -> None:
        self._sessions = sessions
        self._instruments = instruments
        self._observations = observations
        self._session_service = AssessmentSessionService(
            sessions, instruments=instruments, session_builder=session_builder
        )
        self._instrument_service = AssessmentInstrumentService(instruments)

    def create_session(
        self, command: CreateAssessmentSessionCommand
    ) -> AssessmentSessionDTO:
        return self._session_service.create(command)

    def get_session(self, query: GetAssessmentSessionQuery) -> AssessmentSessionDTO:
        dto = self._session_service.get(query)
        if dto is None:
            raise SessionNotFoundError(f"session not found: {query.session_id}")
        return dto


class AssessmentSessionService:
    """Session lifecycle application service."""

    def __init__(
        self,
        sessions: AssessmentSessionRepository,
        *,
        instruments: AssessmentInstrumentRepository | None = None,
        session_builder: AssessmentSessionBuilder | None = None,
    ) -> None:
        self._sessions = sessions
        self._instruments = instruments
        self._session_builder = session_builder

    def create(
        self, command: CreateAssessmentSessionCommand
    ) -> AssessmentSessionDTO:
        if self._instruments is None or self._session_builder is None:
            raise RuntimeError(
                "AssessmentSessionService.create requires "
                "instruments and session_builder"
            )
        instrument = self._instruments.get(InstrumentId(command.instrument_id))
        if instrument is None:
            raise SessionNotFoundError(
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
        session.pull_events()
        return to_session_dto(session)

    def start(self, command: StartAssessmentSessionCommand) -> AssessmentSessionDTO:
        session = self._require(command.session_id)
        from domain.assessment.enums import AssessmentStatus

        if session.status.value == AssessmentStatus.READY.value:
            session.start()
        elif session.status.value == AssessmentStatus.PAUSED.value:
            session.resume()
        self._sessions.save(session)
        session.pull_events()
        return to_session_dto(session)

    def commit_response(
        self, command: CommitAssessmentResponseCommand
    ) -> AssessmentAttemptDTO:
        session = self._require(command.session_id)
        confidence = (
            ConfidenceLevel(command.confidence)
            if command.confidence is not None
            else None
        )
        attempt = session.commit_response(
            QuestionId(command.question_id),
            response_payload=command.response_payload,
            confidence=confidence,
            response_time_ms=command.response_time_ms,
            hints_used=command.hints_used,
            retries=command.retries,
            abandoned=command.abandoned,
            skipped=command.skipped,
        )
        self._sessions.save(session)
        session.pull_events()
        return to_attempt_dto(attempt)

    def submit(
        self, command: SubmitAssessmentSessionCommand
    ) -> AssessmentSessionDTO:
        session = self._require(command.session_id)
        session.submit()
        self._sessions.save(session)
        session.pull_events()
        return to_session_dto(session)

    def get(self, query: GetAssessmentSessionQuery) -> AssessmentSessionDTO | None:
        session = self._sessions.get(SessionId(query.session_id))
        return to_session_dto(session) if session is not None else None

    def list_for_student(
        self, query: ListStudentAssessmentSessionsQuery
    ) -> list[AssessmentSessionDTO]:
        return [
            to_session_dto(session)
            for session in self._sessions.list_by_student(query.student_id)
        ]

    def _require(self, session_id: str):
        session = self._sessions.get(SessionId(session_id))
        if session is None:
            raise SessionNotFoundError(f"session not found: {session_id}")
        return session


class AssessmentObservationService:
    """Observation recording application service.

    Records local AssessmentObservation facts only. Does not update the
    Student Digital Twin or invoke Educational Reasoning. Rich packaging is
    performed by EvidencePackagingService (AP-002C); AP-001 emission remains
    deferred to AP-002D.
    """

    def __init__(
        self,
        observations: AssessmentObservationRepository,
        sessions: AssessmentSessionRepository,
    ) -> None:
        self._observations = observations
        self._sessions = sessions

    def record(
        self, command: RecordAssessmentObservationCommand
    ) -> AssessmentObservationDTO:
        session = self._sessions.get(SessionId(command.session_id))
        if session is None:
            raise SessionNotFoundError(f"session not found: {command.session_id}")
        observation = AssessmentObservationFactory.create(
            observation_id=ObservationId(command.observation_id),
            session_id=SessionId(command.session_id),
            kind=ObservationKind(command.kind),
            evidence_source=EvidenceSource.ASSESSMENT_ENGINE,
            question_id=(
                QuestionId(command.question_id) if command.question_id else None
            ),
            provenance=command.provenance,
        )
        self._observations.save(observation)
        session.record_observation(observation)
        self._sessions.save(session)
        session.pull_events()
        return to_observation_dto(observation)

    def list_for_session(
        self, query: ListObservationsForSessionQuery
    ) -> list[AssessmentObservationDTO]:
        return [
            to_observation_dto(observation)
            for observation in self._observations.list_by_session(
                SessionId(query.session_id)
            )
        ]


class AssessmentInstrumentService:
    """Instrument catalogue application service."""

    def __init__(self, instruments: AssessmentInstrumentRepository) -> None:
        self._instruments = instruments

    def get(
        self, query: GetAssessmentInstrumentQuery
    ) -> AssessmentInstrumentDTO | None:
        instrument = self._instruments.get(InstrumentId(query.instrument_id))
        return to_instrument_dto(instrument) if instrument is not None else None
