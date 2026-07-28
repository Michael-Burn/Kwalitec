"""Application-layer assessment foundation and delivery tests."""

from __future__ import annotations

import inspect
from abc import ABC

import pytest

from application.assessment import (
    AssessmentInstrumentBuilder,
    AssessmentInstrumentRepository,
    AssessmentObservationRepository,
    AssessmentRepository,
    AssessmentResultRepository,
    AssessmentSessionBuilder,
    AssessmentSessionRepository,
    CreateAssessmentSessionCommand,
    GetAssessmentSessionQuery,
    StartAssessmentSessionCommand,
    to_instrument_dto,
    to_session_dto,
)
from application.assessment.ports import EvidenceBundleRepository
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
from infrastructure.assessment.composition import build_assessment_delivery

REPOSITORY_PORTS = [
    AssessmentRepository,
    AssessmentSessionRepository,
    AssessmentInstrumentRepository,
    AssessmentObservationRepository,
    AssessmentResultRepository,
    EvidenceBundleRepository,
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
    composition = build_assessment_delivery(seed=True)
    service = composition.assessment_service
    session_service = composition.session_service
    observation_service = composition.observation_service
    instrument_service = composition.instrument_service

    assert service is not None
    assert session_service is not None
    assert observation_service is not None
    assert instrument_service is not None
    assert session_service.get(GetAssessmentSessionQuery(session_id="missing")) is None


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


def test_session_service_create_start_commit_submit() -> None:
    composition = build_assessment_delivery(seed=True)
    session_service = composition.session_service
    created = session_service.create(
        CreateAssessmentSessionCommand(
            session_id="sess-app-1",
            student_id="student-1",
            instrument_id=composition.default_instrument_id,
        )
    )
    assert created.status == "ready"
    started = session_service.start(
        StartAssessmentSessionCommand(session_id="sess-app-1")
    )
    assert started.status == "in_progress"
