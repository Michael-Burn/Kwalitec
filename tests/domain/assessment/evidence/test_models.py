"""Tests for assessment evidence models."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from domain.assessment import (
    AssessmentInvariantViolation,
    EvidenceBundle,
    EvidenceBundleId,
    EvidenceContext,
    EvidenceItem,
    EvidenceItemId,
    EvidenceMetadata,
    EvidencePackagingResult,
    EvidenceReference,
    EvidenceSource,
    EvidenceStrength,
    EvidenceSummary,
    ObservationId,
    ObservationKind,
    QuestionId,
    ResultId,
    SessionId,
)


def test_evidence_bundle_immutable_and_traceable() -> None:
    item = EvidenceItem(
        item_id=EvidenceItemId("item-1"),
        reference=EvidenceReference(
            observation_id=ObservationId("obs-1"),
            question_id=QuestionId("q-1"),
            kind=ObservationKind.QUESTION_ANSWERED,
        ),
        kind=ObservationKind.QUESTION_ANSWERED,
        evidence_source=EvidenceSource.STUDENT_RESPONSE,
    )
    bundle = EvidenceBundle(
        bundle_id=EvidenceBundleId("bundle-1"),
        context=EvidenceContext(session_id=SessionId("sess-1")),
        metadata=EvidenceMetadata(
            evidence_source=EvidenceSource.ASSESSMENT_ENGINE,
            collected_at=datetime(2026, 7, 28, tzinfo=UTC),
            question_ids=(QuestionId("q-1"),),
        ),
        summary=EvidenceSummary(
            observation_count=1,
            question_observation_count=1,
            distinct_question_count=1,
        ),
        strength=EvidenceStrength.thin(),
        items=(item,),
    )
    assert bundle.observation_ids() == (ObservationId("obs-1"),)
    assert bundle.item_for_observation(ObservationId("obs-1")) is item
    with pytest.raises(Exception):
        bundle.strength = EvidenceStrength.strong()  # type: ignore[misc]


def test_evidence_bundle_rejects_duplicate_observation_refs() -> None:
    ref = EvidenceReference(observation_id=ObservationId("obs-1"))
    items = (
        EvidenceItem(
            item_id=EvidenceItemId("item-1"),
            reference=ref,
            kind=ObservationKind.QUESTION_ANSWERED,
            evidence_source=EvidenceSource.STUDENT_RESPONSE,
        ),
        EvidenceItem(
            item_id=EvidenceItemId("item-2"),
            reference=ref,
            kind=ObservationKind.QUESTION_ANSWERED,
            evidence_source=EvidenceSource.STUDENT_RESPONSE,
        ),
    )
    with pytest.raises(AssessmentInvariantViolation):
        EvidenceBundle(
            bundle_id=EvidenceBundleId("bundle-1"),
            context=EvidenceContext(session_id=SessionId("sess-1")),
            metadata=EvidenceMetadata(
                evidence_source=EvidenceSource.ASSESSMENT_ENGINE
            ),
            summary=EvidenceSummary(
                observation_count=2,
                question_observation_count=2,
                distinct_question_count=1,
            ),
            strength=EvidenceStrength.thin(),
            items=items,
        )


def test_packaging_result_exposes_strength() -> None:
    bundle = EvidenceBundle(
        bundle_id=EvidenceBundleId("bundle-1"),
        context=EvidenceContext(session_id=SessionId("sess-1")),
        metadata=EvidenceMetadata(evidence_source=EvidenceSource.ASSESSMENT_ENGINE),
        summary=EvidenceSummary(
            observation_count=0,
            question_observation_count=0,
            distinct_question_count=0,
        ),
        strength=EvidenceStrength.moderate(),
        items=(),
    )
    result = EvidencePackagingResult(
        bundle=bundle, result_id=ResultId("result-1"), validated=True
    )
    assert result.strength == EvidenceStrength.moderate()
    assert result.observation_ids == ()
