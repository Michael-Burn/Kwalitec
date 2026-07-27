"""Assessment application layer — ports, DTOs, and service skeletons (AP-002A)."""

from __future__ import annotations

from application.assessment.commands import (
    CommitAssessmentResponseCommand,
    CreateAssessmentSessionCommand,
    RecordAssessmentObservationCommand,
    StartAssessmentSessionCommand,
    SubmitAssessmentSessionCommand,
)
from application.assessment.dto import (
    AssessmentAttemptDTO,
    AssessmentInstrumentDTO,
    AssessmentObservationDTO,
    AssessmentResultDTO,
    AssessmentSessionDTO,
    QuestionReferenceDTO,
)
from application.assessment.mappers import (
    to_attempt_dto,
    to_instrument_dto,
    to_observation_dto,
    to_question_reference_dto,
    to_result_dto,
    to_session_dto,
)
from application.assessment.ports import (
    AssessmentInstrumentBuilder,
    AssessmentInstrumentRepository,
    AssessmentObservationRepository,
    AssessmentRepository,
    AssessmentResultRepository,
    AssessmentSessionBuilder,
    AssessmentSessionRepository,
)
from application.assessment.queries import (
    GetAssessmentInstrumentQuery,
    GetAssessmentSessionQuery,
    ListObservationsForSessionQuery,
    ListStudentAssessmentSessionsQuery,
)
from application.assessment.services import (
    AssessmentInstrumentService,
    AssessmentObservationService,
    AssessmentService,
    AssessmentSessionService,
)

__all__ = [
    "AssessmentAttemptDTO",
    "AssessmentInstrumentBuilder",
    "AssessmentInstrumentDTO",
    "AssessmentInstrumentRepository",
    "AssessmentInstrumentService",
    "AssessmentObservationDTO",
    "AssessmentObservationRepository",
    "AssessmentObservationService",
    "AssessmentRepository",
    "AssessmentResultDTO",
    "AssessmentResultRepository",
    "AssessmentService",
    "AssessmentSessionBuilder",
    "AssessmentSessionDTO",
    "AssessmentSessionRepository",
    "AssessmentSessionService",
    "CommitAssessmentResponseCommand",
    "CreateAssessmentSessionCommand",
    "GetAssessmentInstrumentQuery",
    "GetAssessmentSessionQuery",
    "ListObservationsForSessionQuery",
    "ListStudentAssessmentSessionsQuery",
    "QuestionReferenceDTO",
    "RecordAssessmentObservationCommand",
    "StartAssessmentSessionCommand",
    "SubmitAssessmentSessionCommand",
    "to_attempt_dto",
    "to_instrument_dto",
    "to_observation_dto",
    "to_question_reference_dto",
    "to_result_dto",
    "to_session_dto",
]
