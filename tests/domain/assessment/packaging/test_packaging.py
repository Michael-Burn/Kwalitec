"""Tests for evidence packaging builder, validation, events, and immutability."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from domain.assessment import (
    AssessmentEvidenceCreated,
    AssessmentInvariantViolation,
    AssessmentObservationFactory,
    AssessmentResultFactory,
    EvidenceBundleBuilder,
    EvidencePackaged,
    EvidencePackager,
    EvidenceSource,
    EvidenceValidated,
    ObservationId,
    ObservationKind,
    QuestionId,
    ResultId,
    SessionId,
)
from domain.assessment.packaging.ids import sequential_id_factory


def _obs(oid: str, qid: str) -> object:
    return AssessmentObservationFactory.create(
        observation_id=ObservationId(oid),
        session_id=SessionId("sess-pack"),
        kind=ObservationKind.QUESTION_ANSWERED,
        evidence_source=EvidenceSource.STUDENT_RESPONSE,
        question_id=QuestionId(qid),
        provenance={
            "response_payload": {"selected_option": "a"},
            "confidence": 4,
            "response_time_ms": 900,
            "hints_used": 0,
            "retries": 0,
        },
    )


def test_builder_packages_with_full_traceability() -> None:
    builder = (
        EvidenceBundleBuilder(
            collected_at=datetime(2026, 7, 28, tzinfo=UTC),
            id_factory=sequential_id_factory(),
        )
        .with_bundle_id("bundle-pack-1")
        .with_context(
            session_id="sess-pack",
            instrument_id="inst-1",
            purpose="diagnostic",
            student_id="student-1",
        )
        .with_expected_question_count(2)
        .add_observations([_obs("obs-a", "q-a"), _obs("obs-b", "q-b")])  # type: ignore[list-item]
    )
    bundle = builder.build()
    assert len(bundle.items) == 2
    assert bundle.metadata.packaging_version.startswith("AP-002C")
    assert {i.reference.observation_id.value for i in bundle.items} == {
        "obs-a",
        "obs-b",
    }
    assert all(item.dimensions is not None for item in bundle.items)


def test_packager_emits_factual_events_only() -> None:
    packager = EvidencePackager(id_factory=sequential_id_factory())
    result = packager.package(
        [_obs("obs-a", "q-a"), _obs("obs-b", "q-b")],  # type: ignore[list-item]
        session_id="sess-pack",
        result_id="result-pack-1",
        instrument_id="inst-1",
        expected_question_count=2,
    )
    assert result.validated is True
    assert len(result.events) == 3
    assert isinstance(result.events[0], EvidencePackaged)
    assert isinstance(result.events[1], EvidenceValidated)
    assert isinstance(result.events[2], AssessmentEvidenceCreated)
    assert result.events[2].result_id == ResultId("result-pack-1")


def test_assessment_result_exposes_packaged_evidence() -> None:
    packager = EvidencePackager(id_factory=sequential_id_factory())
    packaging = packager.package(
        [_obs("obs-a", "q-a"), _obs("obs-b", "q-b")],  # type: ignore[list-item]
        session_id="sess-pack",
        result_id="result-pack-2",
        expected_question_count=2,
    )
    result = AssessmentResultFactory.create(
        result_id=ResultId("result-pack-2"),
        session_id=SessionId("sess-pack"),
        observation_ids=packaging.bundle.observation_ids(),
        evidence_bundle=packaging.bundle,
    )
    assert result.packaged_evidence() is packaging.bundle
    assert result.evidence_strength == packaging.bundle.strength


def test_validation_rejects_information_loss() -> None:
    from domain.assessment.evidence.models import (
        EvidenceItem,
        EvidenceItemId,
        EvidenceReference,
    )
    from domain.assessment.packaging.validation import assert_observation_traceability

    observations = [_obs("obs-a", "q-a"), _obs("obs-b", "q-b")]
    items = (
        EvidenceItem(
            item_id=EvidenceItemId("item-1"),
            reference=EvidenceReference(observation_id=ObservationId("obs-a")),
            kind=ObservationKind.QUESTION_ANSWERED,
            evidence_source=EvidenceSource.STUDENT_RESPONSE,
        ),
    )
    with pytest.raises(AssessmentInvariantViolation):
        assert_observation_traceability(observations, items)  # type: ignore[arg-type]
