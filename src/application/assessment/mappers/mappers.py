"""Mappers between assessment domain objects and application DTOs."""

from __future__ import annotations

from application.assessment.dto.models import (
    AssessmentAttemptDTO,
    AssessmentInstrumentDTO,
    AssessmentObservationDTO,
    AssessmentResultDTO,
    AssessmentSessionDTO,
    QuestionReferenceDTO,
)
from domain.assessment.entities.assessment_attempt import AssessmentAttempt
from domain.assessment.entities.assessment_instrument import AssessmentInstrument
from domain.assessment.entities.assessment_observation import AssessmentObservation
from domain.assessment.entities.assessment_result import AssessmentResult
from domain.assessment.entities.assessment_session import AssessmentSession
from domain.assessment.value_objects.references import QuestionReference


def to_question_reference_dto(reference: QuestionReference) -> QuestionReferenceDTO:
    return QuestionReferenceDTO(
        question_id=reference.question_id.value,
        item_type=reference.item_type.value,
        version=reference.version,
        learning_objective_id=reference.learning_objective.objective_id.value,
        learning_objective_label=reference.learning_objective.label,
        curriculum_entity_id=reference.curriculum_entity_id,
        knowledge_level=(
            reference.knowledge_level.value if reference.knowledge_level else None
        ),
        difficulty=reference.difficulty.band.value if reference.difficulty else None,
        estimated_time_seconds=reference.estimated_time_seconds,
    )


def to_instrument_dto(instrument: AssessmentInstrument) -> AssessmentInstrumentDTO:
    return AssessmentInstrumentDTO(
        instrument_id=instrument.instrument_id.value,
        assessment_type=instrument.assessment_type.value,
        purpose=instrument.purpose.value,
        title=instrument.metadata.title,
        version=instrument.metadata.version,
        question_count=instrument.question_count(),
        learning_objective_ids=tuple(
            obj.objective_id.value for obj in instrument.learning_objectives
        ),
        questions=tuple(
            to_question_reference_dto(item.reference) for item in instrument.questions
        ),
    )


def to_attempt_dto(attempt: AssessmentAttempt) -> AssessmentAttemptDTO:
    return AssessmentAttemptDTO(
        session_id=attempt.session_id.value,
        question_id=attempt.question_id.value,
        attempt_number=attempt.attempt_number.value,
        committed=attempt.committed,
        response_payload=dict(attempt.response_payload),
        confidence=attempt.confidence.value if attempt.confidence else None,
        response_time_ms=attempt.response_time_ms,
        hints_used=attempt.hints_used,
        retries=attempt.retries,
        outcome=attempt.outcome.value if attempt.outcome else None,
        abandoned=attempt.abandoned,
        skipped=attempt.skipped,
    )


def to_session_dto(session: AssessmentSession) -> AssessmentSessionDTO:
    return AssessmentSessionDTO(
        session_id=session.session_id.value,
        student_id=session.student_id,
        instrument_id=session.instrument_id.value,
        purpose=session.purpose.value,
        assessment_type=session.assessment_type.value,
        status=session.status.value,
        question_ids=tuple(q.question_id.value for q in session.questions),
        twin_id=session.twin_id,
        mission_id=session.mission_id,
        attempt_count=len(session.attempts),
        observation_ids=session.observation_ids,
    )


def to_observation_dto(
    observation: AssessmentObservation,
) -> AssessmentObservationDTO:
    return AssessmentObservationDTO(
        observation_id=observation.observation_id.value,
        session_id=observation.session_id.value,
        kind=observation.kind.value,
        evidence_source=observation.evidence_source.value,
        question_id=observation.question_id.value if observation.question_id else None,
        provenance=dict(observation.provenance),
    )


def to_result_dto(result: AssessmentResult) -> AssessmentResultDTO:
    from application.assessment.evidence.mapper import to_evidence_bundle_dto

    evidence_bundle = None
    if result.evidence_bundle is not None:
        evidence_bundle = to_evidence_bundle_dto(result.evidence_bundle)
    return AssessmentResultDTO(
        result_id=result.result_id.value,
        session_id=result.session_id.value,
        observation_ids=tuple(oid.value for oid in result.observation_ids),
        evidence_strength=(
            result.evidence_strength.band.value if result.evidence_strength else None
        ),
        evidence_bundle=evidence_bundle,
        correctness_counts={
            key.value: value for key, value in result.correctness_counts
        },
    )
