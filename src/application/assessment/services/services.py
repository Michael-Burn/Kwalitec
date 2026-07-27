"""Assessment application service skeletons (AP-002A).

Methods that belong to later milestones raise ``NotImplementedError``.
No Twin updates, Reasoning, Mission, Tutor, or delivery logic.
"""

from __future__ import annotations

from application.assessment.commands.commands import (
    CommitAssessmentResponseCommand,
    CreateAssessmentSessionCommand,
    RecordAssessmentObservationCommand,
    StartAssessmentSessionCommand,
    SubmitAssessmentSessionCommand,
)
from application.assessment.dto.models import (
    AssessmentAttemptDTO,
    AssessmentInstrumentDTO,
    AssessmentObservationDTO,
    AssessmentSessionDTO,
)
from application.assessment.ports.repositories import (
    AssessmentInstrumentRepository,
    AssessmentObservationRepository,
    AssessmentSessionRepository,
)
from application.assessment.queries.queries import (
    GetAssessmentInstrumentQuery,
    GetAssessmentSessionQuery,
    ListObservationsForSessionQuery,
    ListStudentAssessmentSessionsQuery,
)


class AssessmentService:
    """Facade coordinating assessment application use cases (skeleton)."""

    def __init__(
        self,
        sessions: AssessmentSessionRepository,
        instruments: AssessmentInstrumentRepository,
        observations: AssessmentObservationRepository,
    ) -> None:
        self._sessions = sessions
        self._instruments = instruments
        self._observations = observations

    def create_session(
        self, command: CreateAssessmentSessionCommand
    ) -> AssessmentSessionDTO:
        raise NotImplementedError("AP-002B: session creation / delivery")

    def get_session(self, query: GetAssessmentSessionQuery) -> AssessmentSessionDTO:
        raise NotImplementedError("AP-002B: session read model")


class AssessmentSessionService:
    """Session lifecycle application service (skeleton)."""

    def __init__(self, sessions: AssessmentSessionRepository) -> None:
        self._sessions = sessions

    def create(
        self, command: CreateAssessmentSessionCommand
    ) -> AssessmentSessionDTO:
        raise NotImplementedError("AP-002B: construct session from instrument")

    def start(self, command: StartAssessmentSessionCommand) -> AssessmentSessionDTO:
        raise NotImplementedError("AP-002B: start session delivery")

    def commit_response(
        self, command: CommitAssessmentResponseCommand
    ) -> AssessmentAttemptDTO:
        raise NotImplementedError("AP-002B: commit response capture")

    def submit(
        self, command: SubmitAssessmentSessionCommand
    ) -> AssessmentSessionDTO:
        raise NotImplementedError("AP-002B: submit session for observation emission")

    def get(self, query: GetAssessmentSessionQuery) -> AssessmentSessionDTO | None:
        raise NotImplementedError("AP-002B: load session DTO")

    def list_for_student(
        self, query: ListStudentAssessmentSessionsQuery
    ) -> list[AssessmentSessionDTO]:
        raise NotImplementedError("AP-002B: list student sessions")


class AssessmentObservationService:
    """Observation recording application service (skeleton).

    Does not update the Student Digital Twin or invoke Educational Reasoning.
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
        raise NotImplementedError("AP-002C: observation packaging / AP-001 emission")

    def list_for_session(
        self, query: ListObservationsForSessionQuery
    ) -> list[AssessmentObservationDTO]:
        raise NotImplementedError("AP-002C: list session observations")


class AssessmentInstrumentService:
    """Instrument catalogue application service (skeleton)."""

    def __init__(self, instruments: AssessmentInstrumentRepository) -> None:
        self._instruments = instruments

    def get(
        self, query: GetAssessmentInstrumentQuery
    ) -> AssessmentInstrumentDTO | None:
        raise NotImplementedError("AP-002B: instrument catalogue reads")
