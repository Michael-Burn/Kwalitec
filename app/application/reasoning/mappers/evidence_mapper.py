"""Map domain InterpretationResult → application DTOs."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.application.reasoning.dto.interpretation_dto import (
    InterpretationResultDTO,
    InterpretedObservationDTO,
)
from app.domain.reasoning.interpretation.result import InterpretationResult
from app.domain.reasoning.observations.observation import EducationalObservation


def map_interpretation_result(result: InterpretationResult) -> InterpretationResultDTO:
    """Project an immutable domain result into an application DTO."""
    context = result.context
    observations = tuple(
        _map_observation(observation)
        for observation in result.observation_set.observations
    )
    return InterpretationResultDTO(
        reasoning_request_id=context.reasoning_request_id,
        evidence_bundle_id=context.evidence_bundle_id,
        session_id=context.session_id,
        packaging_version=context.packaging_version,
        interpreter_version=context.interpreter_version,
        correlation_id=context.correlation_id,
        set_id=result.observation_set.set_id,
        interpreted_at=result.interpreted_at,
        observations=observations,
        observation_ids=result.observation_ids,
    )


def _map_observation(observation: EducationalObservation) -> InterpretedObservationDTO:
    value: Any = observation.value
    if isinstance(value, Mapping):
        value = dict(value)

    return InterpretedObservationDTO(
        observation_id=observation.observation_id,
        evidence_reference=observation.evidence_reference,
        learning_objective_reference=observation.learning_objective_reference,
        concept_reference=observation.concept_reference,
        category=observation.category.value,
        value=value,
        provenance=observation.provenance,
        interpretation_version=observation.interpretation_version,
        recorded_at=observation.recorded_at,
        reasoning_request_id=observation.reasoning_request_id,
        evidence_bundle_id=observation.evidence_bundle_id,
        session_id=observation.session_id,
        correlation_id=observation.correlation_id,
        source_observation_id=observation.source_observation_id,
        question_reference=observation.question_reference,
        traceability=dict(observation.traceability),
    )
