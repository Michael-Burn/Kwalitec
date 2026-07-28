"""Contract validation tests for AP-002D1 evidence ingress."""

from __future__ import annotations

from dataclasses import replace

import pytest

from app.application.assessment_pipeline.evidence_ingress import (
    IncompleteEvidenceBundle,
    InvalidEvidenceBundle,
    MissingObservationReference,
    UnsupportedEvidenceVersion,
    validate_evidence_bundle,
)
from application.assessment.evidence.dto import EvidenceContextDTO, EvidenceItemDTO
from tests.application.assessment_pipeline.evidence_ingress.conftest import (
    make_bundle,
    make_item,
)


def test_valid_bundle_passes() -> None:
    bundle = make_bundle()
    assert validate_evidence_bundle(bundle) is bundle


def test_rejects_null_bundle() -> None:
    with pytest.raises(InvalidEvidenceBundle, match="null"):
        validate_evidence_bundle(None)


def test_rejects_wrong_type() -> None:
    with pytest.raises(InvalidEvidenceBundle, match="EvidenceBundleDTO"):
        validate_evidence_bundle({"bundle_id": "x"})  # type: ignore[arg-type]


def test_rejects_missing_metadata_version() -> None:
    bundle = make_bundle(packaging_version="")
    with pytest.raises(IncompleteEvidenceBundle, match="packaging_version"):
        validate_evidence_bundle(bundle)


def test_rejects_unknown_packaging_version() -> None:
    bundle = make_bundle(packaging_version="AP-999Z.0")
    with pytest.raises(UnsupportedEvidenceVersion, match="AP-999Z.0"):
        validate_evidence_bundle(bundle)


def test_rejects_empty_items() -> None:
    bundle = make_bundle(items=(), observation_ids=(), summary_count=0)
    with pytest.raises(IncompleteEvidenceBundle, match="no items"):
        validate_evidence_bundle(bundle)


def test_rejects_missing_observation_id_on_item() -> None:
    bad = make_item(observation_id="")
    bundle = make_bundle(items=(bad,), observation_ids=("obs-1",), summary_count=1)
    with pytest.raises(MissingObservationReference, match="observation_id"):
        validate_evidence_bundle(bundle)


def test_rejects_observation_id_mismatch() -> None:
    bundle = make_bundle(observation_ids=("obs-unknown", "obs-2"))
    with pytest.raises(MissingObservationReference):
        validate_evidence_bundle(bundle)


def test_rejects_blank_declared_observation_ids() -> None:
    items = (make_item(),)
    bundle = make_bundle(items=items, observation_ids=("obs-1", ""), summary_count=1)
    with pytest.raises(MissingObservationReference, match="blank"):
        validate_evidence_bundle(bundle)


def test_rejects_duplicate_item_observation_ids() -> None:
    items = (
        make_item(item_id="i1", observation_id="obs-dup"),
        make_item(item_id="i2", observation_id="obs-dup", question_id="q-2"),
    )
    bundle = make_bundle(items=items, observation_ids=("obs-dup",), summary_count=2)
    with pytest.raises(InvalidEvidenceBundle, match="duplicate observation_id"):
        validate_evidence_bundle(bundle)


def test_rejects_summary_count_mismatch() -> None:
    bundle = make_bundle(summary_count=99)
    with pytest.raises(InvalidEvidenceBundle, match="observation_count"):
        validate_evidence_bundle(bundle)


def test_rejects_session_id_mismatch() -> None:
    bundle = make_bundle(session_id="sess-a")
    mismatched = replace(
        bundle,
        context=EvidenceContextDTO(
            session_id="sess-other",
            instrument_id=bundle.context.instrument_id,
            assessment_id=bundle.context.assessment_id,
            purpose=bundle.context.purpose,
            assessment_type=bundle.context.assessment_type,
            student_id=bundle.context.student_id,
        ),
    )
    with pytest.raises(InvalidEvidenceBundle, match="session_id"):
        validate_evidence_bundle(mismatched)


def test_rejects_corrupted_item_payload() -> None:
    bundle = make_bundle()
    corrupted = replace(bundle, items=(None,))  # type: ignore[arg-type]
    with pytest.raises(InvalidEvidenceBundle, match="corrupted"):
        validate_evidence_bundle(corrupted)


def test_rejects_missing_bundle_id() -> None:
    bundle = replace(make_bundle(), bundle_id="")
    with pytest.raises(IncompleteEvidenceBundle, match="bundle_id"):
        validate_evidence_bundle(bundle)


def test_item_must_be_evidence_item_dto() -> None:
    assert isinstance(make_item(), EvidenceItemDTO)
