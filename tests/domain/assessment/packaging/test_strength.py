"""Tests for evidence strength calculation (observation quality only)."""

from __future__ import annotations

from domain.assessment import (
    AssessmentObservationFactory,
    EvidenceSource,
    EvidenceStrength,
    ObservationAggregator,
    ObservationId,
    ObservationKind,
    QuestionId,
    SessionId,
    calculate_evidence_strength,
    derive_strength_factors,
)
from domain.assessment.value_objects.evidence_dimensions import EvidenceDimensions
from domain.assessment.value_objects.levels import ConfidenceLevel


def _question_obs(
    oid: str,
    qid: str,
    *,
    hints: int = 0,
    retries: int = 0,
    confidence: int | None = 3,
    timing: int | None = 1200,
    payload: bool = True,
):
    dims = EvidenceDimensions(
        confidence=ConfidenceLevel(confidence) if confidence else None,
        response_time_ms=timing,
        hints_used=hints,
        retries=retries,
    )
    return AssessmentObservationFactory.create(
        observation_id=ObservationId(oid),
        session_id=SessionId("sess-1"),
        kind=ObservationKind.QUESTION_ANSWERED,
        evidence_source=EvidenceSource.STUDENT_RESPONSE,
        question_id=QuestionId(qid),
        dimensions=dims,
        provenance={
            "response_payload": {"selected": "a"} if payload else {},
            "hints_used": hints,
            "retries": retries,
            "confidence": confidence,
            "response_time_ms": timing,
        },
    )


def test_empty_collection_is_thin() -> None:
    collection = ObservationAggregator.aggregate([])
    assert calculate_evidence_strength(collection) == EvidenceStrength.thin()


def test_single_item_with_heavy_hints_is_thin() -> None:
    collection = ObservationAggregator.aggregate(
        [_question_obs("obs-1", "q-1", hints=3, retries=3)]
    )
    factors = derive_strength_factors(collection)
    assert factors.heavy_scaffolding is True
    assert factors.to_strength() == EvidenceStrength.thin()


def test_multiple_quality_items_can_be_strong() -> None:
    collection = ObservationAggregator.aggregate(
        [
            _question_obs("obs-1", "q-1"),
            _question_obs("obs-2", "q-2"),
            _question_obs("obs-3", "q-3"),
        ]
    )
    strength = calculate_evidence_strength(
        collection, expected_question_count=3
    )
    assert strength in {EvidenceStrength.moderate(), EvidenceStrength.strong()}
    factors = derive_strength_factors(collection, expected_question_count=3)
    assert factors.question_coverage is True
    assert factors.quality_points() >= 3


def test_strength_is_deterministic() -> None:
    observations = [
        _question_obs("obs-1", "q-1"),
        _question_obs("obs-2", "q-2"),
    ]
    a = calculate_evidence_strength(ObservationAggregator.aggregate(observations))
    b = calculate_evidence_strength(ObservationAggregator.aggregate(observations))
    assert a == b
