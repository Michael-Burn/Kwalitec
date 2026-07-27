"""Composition root for Assessment Delivery (AP-002B)."""

from __future__ import annotations

from dataclasses import dataclass

from application.assessment.delivery.delivery_service import AssessmentDeliveryService
from application.assessment.services.services import (
    AssessmentInstrumentService,
    AssessmentObservationService,
    AssessmentService,
    AssessmentSessionService,
)
from infrastructure.assessment.catalogue_seed import (
    DEFAULT_INSTRUMENT_ID,
    seed_delivery_catalogue,
)
from infrastructure.assessment.in_memory import (
    DomainAssessmentInstrumentBuilder,
    DomainAssessmentSessionBuilder,
    InMemoryAssessmentInstrumentRepository,
    InMemoryAssessmentObservationRepository,
    InMemoryAssessmentResultRepository,
    InMemoryAssessmentSessionRepository,
    InMemoryQuestionContentRepository,
    InMemorySessionDeliveryStateRepository,
)


@dataclass
class AssessmentDeliveryComposition:
    """Wires in-memory adapters and delivery services."""

    sessions: InMemoryAssessmentSessionRepository
    instruments: InMemoryAssessmentInstrumentRepository
    observations: InMemoryAssessmentObservationRepository
    results: InMemoryAssessmentResultRepository
    question_content: InMemoryQuestionContentRepository
    delivery_state: InMemorySessionDeliveryStateRepository
    session_builder: DomainAssessmentSessionBuilder
    instrument_builder: DomainAssessmentInstrumentBuilder
    default_instrument_id: str
    delivery_service: AssessmentDeliveryService
    session_service: AssessmentSessionService
    instrument_service: AssessmentInstrumentService
    observation_service: AssessmentObservationService
    assessment_service: AssessmentService


def build_assessment_delivery(
    *, seed: bool = True
) -> AssessmentDeliveryComposition:
    """Construct a delivery-ready composition (no Twin / Reasoning wiring)."""
    sessions = InMemoryAssessmentSessionRepository()
    instruments = InMemoryAssessmentInstrumentRepository()
    observations = InMemoryAssessmentObservationRepository()
    results = InMemoryAssessmentResultRepository()
    question_content = InMemoryQuestionContentRepository()
    delivery_state = InMemorySessionDeliveryStateRepository()
    session_builder = DomainAssessmentSessionBuilder()
    instrument_builder = DomainAssessmentInstrumentBuilder()

    default_id = DEFAULT_INSTRUMENT_ID
    if seed:
        default_id = seed_delivery_catalogue(instruments, question_content)

    delivery_service = AssessmentDeliveryService(
        sessions=sessions,
        instruments=instruments,
        observations=observations,
        results=results,
        question_content=question_content,
        delivery_state=delivery_state,
        session_builder=session_builder,
        default_instrument_id=default_id,
    )
    session_service = AssessmentSessionService(
        sessions, instruments=instruments, session_builder=session_builder
    )
    instrument_service = AssessmentInstrumentService(instruments)
    observation_service = AssessmentObservationService(observations, sessions)
    assessment_service = AssessmentService(
        sessions,
        instruments,
        observations,
        session_builder=session_builder,
    )
    return AssessmentDeliveryComposition(
        sessions=sessions,
        instruments=instruments,
        observations=observations,
        results=results,
        question_content=question_content,
        delivery_state=delivery_state,
        session_builder=session_builder,
        instrument_builder=instrument_builder,
        default_instrument_id=default_id,
        delivery_service=delivery_service,
        session_service=session_service,
        instrument_service=instrument_service,
        observation_service=observation_service,
        assessment_service=assessment_service,
    )
