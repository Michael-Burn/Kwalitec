"""Tests for observation aggregation."""

from __future__ import annotations

import pytest

from domain.assessment import (
    AssessmentInvariantViolation,
    AssessmentObservationFactory,
    EvidenceSource,
    ObservationAggregator,
    ObservationCollection,
    ObservationId,
    ObservationKind,
    QuestionId,
    SessionId,
)


def _obs(oid: str, *, session: str = "sess-1", question: str | None = "q-1"):
    return AssessmentObservationFactory.create(
        observation_id=ObservationId(oid),
        session_id=SessionId(session),
        kind=ObservationKind.QUESTION_ANSWERED,
        evidence_source=EvidenceSource.STUDENT_RESPONSE,
        question_id=QuestionId(question) if question else None,
        provenance={"response_payload": {"selected": "a"}},
    )


def test_observation_collection_rejects_duplicates() -> None:
    with pytest.raises(AssessmentInvariantViolation):
        ObservationCollection(observations=(_obs("obs-1"), _obs("obs-1")))


def test_observation_collection_rejects_mixed_sessions() -> None:
    with pytest.raises(AssessmentInvariantViolation):
        ObservationCollection(
            observations=(_obs("obs-1", session="s1"), _obs("obs-2", session="s2"))
        )


def test_aggregator_preserves_order_and_traceability() -> None:
    collection = ObservationAggregator.aggregate(
        [_obs("obs-1", question="q-1"), _obs("obs-2", question="q-2")]
    )
    assert len(collection) == 2
    assert collection.observation_ids() == (
        ObservationId("obs-1"),
        ObservationId("obs-2"),
    )
    assert collection.distinct_question_ids() == (
        QuestionId("q-1"),
        QuestionId("q-2"),
    )
    assert collection.get(ObservationId("obs-2")) is not None
