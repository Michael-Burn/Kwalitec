"""Application-layer assessment foundation tests."""

from __future__ import annotations

import inspect
from abc import ABC

import pytest

from application.assessment import (
    AssessmentInstrumentBuilder,
    AssessmentInstrumentRepository,
    AssessmentInstrumentService,
    AssessmentObservationRepository,
    AssessmentObservationService,
    AssessmentRepository,
    AssessmentResultRepository,
    AssessmentService,
    AssessmentSessionBuilder,
    AssessmentSessionRepository,
    AssessmentSessionService,
    CreateAssessmentSessionCommand,
    GetAssessmentSessionQuery,
    to_instrument_dto,
    to_session_dto,
)
from domain.assessment import (
    AssessmentMetadata,
    AssessmentPurpose,
    AssessmentType,
    InstrumentId,
    ItemType,
    LearningObjectiveId,
    LearningObjectiveReference,
    QuestionId,
    QuestionReference,
    SessionId,
)
from domain.assessment.factories import (
    AssessmentInstrumentFactory,
    AssessmentSessionFactory,
)

REPOSITORY_PORTS = [
    AssessmentRepository,
    AssessmentSessionRepository,
    AssessmentInstrumentRepository,
    AssessmentObservationRepository,
    AssessmentResultRepository,
]

BUILDER_PORTS = [
    AssessmentInstrumentBuilder,
    AssessmentSessionBuilder,
]


@pytest.mark.parametrize("port", REPOSITORY_PORTS + BUILDER_PORTS)
def test_ports_are_abstract(port: type) -> None:
    assert issubclass(port, ABC)
    assert inspect.isabstract(port)


@pytest.mark.parametrize("port", REPOSITORY_PORTS + BUILDER_PORTS)
def test_ports_cannot_be_instantiated(port: type) -> None:
    with pytest.raises(TypeError):
        port()  # type: ignore[misc]


def test_services_construct_with_ports() -> None:
    class FakeSessionRepo(AssessmentSessionRepository):
        def get(self, session_id):  # type: ignore[no-untyped-def]
            return None

        def list_by_student(self, student_id):  # type: ignore[no-untyped-def]
            return []

        def save(self, session):  # type: ignore[no-untyped-def]
            return None

    class FakeInstrumentRepo(AssessmentInstrumentRepository):
        def get(self, instrument_id):  # type: ignore[no-untyped-def]
            return None

        def list_by_purpose(self, purpose):  # type: ignore[no-untyped-def]
            return []

        def save(self, instrument):  # type: ignore[no-untyped-def]
            return None

    class FakeObservationRepo(AssessmentObservationRepository):
        def get(self, observation_id):  # type: ignore[no-untyped-def]
            return None

        def list_by_session(self, session_id):  # type: ignore[no-untyped-def]
            return []

        def save(self, observation):  # type: ignore[no-untyped-def]
            return None

    sessions = FakeSessionRepo()
    instruments = FakeInstrumentRepo()
    observations = FakeObservationRepo()

    service = AssessmentService(sessions, instruments, observations)
    session_service = AssessmentSessionService(sessions)
    observation_service = AssessmentObservationService(observations, sessions)
    instrument_service = AssessmentInstrumentService(instruments)

    assert service is not None
    assert session_service is not None
    assert observation_service is not None
    assert instrument_service is not None

    with pytest.raises(NotImplementedError):
        service.create_session(
            CreateAssessmentSessionCommand(
                session_id="s",
                student_id="u",
                instrument_id="i",
            )
        )
    with pytest.raises(NotImplementedError):
        session_service.get(GetAssessmentSessionQuery(session_id="s"))


def test_mappers_do_not_expose_domain_entities() -> None:
    objective = LearningObjectiveReference(
        objective_id=LearningObjectiveId("lo-1"),
        label="LO",
    )
    question = QuestionReference(
        question_id=QuestionId("q-1"),
        item_type=ItemType.MULTIPLE_CHOICE,
        version="1",
        learning_objective=objective,
    )
    instrument = AssessmentInstrumentFactory.create(
        instrument_id=InstrumentId("inst-1"),
        assessment_type=AssessmentType.SINGLE_ITEM,
        purpose=AssessmentPurpose.DIAGNOSTIC,
        questions=[question],
        learning_objectives=[objective],
        metadata=AssessmentMetadata(version="1", title="Check"),
    )
    session = AssessmentSessionFactory.create_from_instrument(
        session_id=SessionId("sess-1"),
        student_id="student-1",
        instrument=instrument,
    )
    instrument_dto = to_instrument_dto(instrument)
    session_dto = to_session_dto(session)
    assert instrument_dto.instrument_id == "inst-1"
    assert session_dto.status == "draft"
    assert instrument_dto.questions[0].question_id == "q-1"
