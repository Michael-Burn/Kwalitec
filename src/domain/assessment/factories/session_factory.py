"""Factories for Assessment Engine domain objects.

Architecture Source
    knowledge/product/AP-002/ASSESSMENT_LIFECYCLE.md
    knowledge/product/AP-002/QUESTION_MODEL.md
"""

from __future__ import annotations

from collections.abc import Sequence

from domain.assessment.entities.assessment_instrument import AssessmentInstrument
from domain.assessment.entities.assessment_observation import AssessmentObservation
from domain.assessment.entities.assessment_result import AssessmentResult
from domain.assessment.entities.assessment_session import AssessmentSession
from domain.assessment.enums import (
    AssessmentPurpose,
    AssessmentType,
    AttemptOutcome,
    EvidenceSource,
    ObservationKind,
)
from domain.assessment.value_objects.configuration import (
    AssessmentConfiguration,
    AssessmentMetadata,
)
from domain.assessment.value_objects.evidence_dimensions import EvidenceDimensions
from domain.assessment.value_objects.ids import (
    InstrumentId,
    ObservationId,
    ResultId,
    SessionId,
)
from domain.assessment.value_objects.levels import EvidenceStrength
from domain.assessment.value_objects.references import (
    LearningObjectiveReference,
    QuestionReference,
)


class AssessmentInstrumentFactory:
    """Construct validated AssessmentInstrument instances."""

    @staticmethod
    def create(
        instrument_id: InstrumentId,
        assessment_type: AssessmentType,
        purpose: AssessmentPurpose,
        questions: Sequence[QuestionReference],
        learning_objectives: Sequence[LearningObjectiveReference],
        metadata: AssessmentMetadata,
        *,
        configuration: AssessmentConfiguration | None = None,
    ) -> AssessmentInstrument:
        return AssessmentInstrument(
            instrument_id=instrument_id,
            assessment_type=assessment_type,
            purpose=purpose,
            questions=questions,
            learning_objectives=learning_objectives,
            metadata=metadata,
            configuration=configuration,
        )


class AssessmentSessionFactory:
    """Construct AssessmentSession aggregates from an instrument."""

    @staticmethod
    def create_from_instrument(
        session_id: SessionId,
        student_id: str,
        instrument: AssessmentInstrument,
        *,
        twin_id: str | None = None,
        mission_id: str | None = None,
        configuration: AssessmentConfiguration | None = None,
    ) -> AssessmentSession:
        return AssessmentSession.create(
            session_id=session_id,
            student_id=student_id,
            instrument_id=instrument.instrument_id,
            purpose=instrument.purpose,
            assessment_type=instrument.assessment_type,
            questions=instrument.question_references,
            configuration=configuration or instrument.configuration,
            metadata=instrument.metadata,
            twin_id=twin_id,
            mission_id=mission_id,
        )


class AssessmentObservationFactory:
    """Construct immutable AssessmentObservation facts."""

    @staticmethod
    def create(
        observation_id: ObservationId,
        session_id: SessionId,
        kind: ObservationKind,
        *,
        evidence_source: EvidenceSource = EvidenceSource.ASSESSMENT_ENGINE,
        dimensions: EvidenceDimensions | None = None,
        question_id=None,
        provenance=None,
    ) -> AssessmentObservation:
        return AssessmentObservation(
            observation_id=observation_id,
            session_id=session_id,
            kind=kind,
            evidence_source=evidence_source,
            dimensions=dimensions,
            question_id=question_id,
            provenance=provenance,
        )


class AssessmentResultFactory:
    """Construct evidence-only AssessmentResult packaging."""

    @staticmethod
    def create(
        result_id: ResultId,
        session_id: SessionId,
        *,
        observation_ids: Sequence[ObservationId] = (),
        correctness_counts: dict[AttemptOutcome, int] | None = None,
        evidence_strength: EvidenceStrength | None = None,
        evidence_bundle=None,
    ) -> AssessmentResult:
        counts = tuple((k, v) for k, v in (correctness_counts or {}).items())
        return AssessmentResult(
            result_id=result_id,
            session_id=session_id,
            observation_ids=tuple(observation_ids),
            correctness_counts=counts,
            evidence_strength=evidence_strength,
            evidence_bundle=evidence_bundle,
        )
