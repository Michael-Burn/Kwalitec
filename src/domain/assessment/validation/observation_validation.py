"""Observation payload validation.

Architecture Source
    knowledge/product/AP-002/EVIDENCE_MODEL.md
    knowledge/product/AP-002/SCORING_MODEL.md
"""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Any

from domain.assessment.enums import EvidenceSource, ObservationKind
from domain.assessment.exceptions import (
    AssessmentInvariantViolation,
    InvalidObservationPayloadError,
)
from domain.assessment.value_objects.evidence_dimensions import EvidenceDimensions
from domain.assessment.value_objects.ids import ObservationId, QuestionId, SessionId


def assert_observation_identity(observation_id: ObservationId) -> ObservationId:
    if not isinstance(observation_id, ObservationId):
        raise AssessmentInvariantViolation(
            "observation_id must be an ObservationId",
            invariant="AssessmentObservation.observation_id.type",
        )
    return observation_id


def assert_observation_payload(
    *,
    session_id: SessionId,
    kind: ObservationKind,
    evidence_source: EvidenceSource,
    dimensions: EvidenceDimensions | None,
    question_id: QuestionId | None,
    provenance: Mapping[str, Any] | None,
) -> tuple[
    SessionId,
    ObservationKind,
    EvidenceSource,
    EvidenceDimensions | None,
    QuestionId | None,
    Mapping[str, Any],
]:
    """Validate observation construction inputs; return normalised values."""
    if not isinstance(session_id, SessionId):
        raise InvalidObservationPayloadError("session_id must be a SessionId")
    if not isinstance(kind, ObservationKind):
        raise InvalidObservationPayloadError("kind must be an ObservationKind")
    if not isinstance(evidence_source, EvidenceSource):
        raise InvalidObservationPayloadError(
            "evidence_source must be an EvidenceSource"
        )
    if dimensions is not None and not isinstance(dimensions, EvidenceDimensions):
        raise InvalidObservationPayloadError(
            "dimensions must be EvidenceDimensions when provided"
        )
    if question_id is not None and not isinstance(question_id, QuestionId):
        raise InvalidObservationPayloadError(
            "question_id must be a QuestionId when provided"
        )
    if kind is ObservationKind.QUESTION_ANSWERED and question_id is None:
        raise InvalidObservationPayloadError(
            "question_answered observations require a question_id"
        )
    frozen_provenance = MappingProxyType(dict(provenance or {}))
    if "assessment_session_id" in frozen_provenance:
        if frozen_provenance["assessment_session_id"] != session_id.value:
            raise InvalidObservationPayloadError(
                "provenance.assessment_session_id must match session_id"
            )
    return (
        session_id,
        kind,
        evidence_source,
        dimensions,
        question_id,
        frozen_provenance,
    )
