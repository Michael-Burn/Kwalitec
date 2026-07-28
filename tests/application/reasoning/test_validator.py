"""Validation tests for educational evidence interpretation (AP-002D2)."""

from __future__ import annotations

import pytest

from app.application.reasoning.interpretation.errors import (
    BrokenEvidenceReference,
    InvalidConceptMapping,
    MissingLearningObjective,
    UnsupportedEvidenceSchema,
)
from app.application.reasoning.interpretation.validator import (
    validate_evidence_for_interpretation,
)
from tests.application.reasoning.conftest import make_bundle, make_item


def test_valid_bundle_passes() -> None:
    bundle = validate_evidence_for_interpretation(make_bundle())
    assert bundle.bundle_id == "bundle-1"


def test_unsupported_packaging_version() -> None:
    with pytest.raises(UnsupportedEvidenceSchema):
        validate_evidence_for_interpretation(
            make_bundle(packaging_version="AP-999.0")
        )


def test_missing_learning_objectives() -> None:
    with pytest.raises(MissingLearningObjective):
        validate_evidence_for_interpretation(
            make_bundle(learning_objective_ids=())
        )


def test_blank_learning_objective_rejected() -> None:
    with pytest.raises(MissingLearningObjective):
        validate_evidence_for_interpretation(
            make_bundle(learning_objective_ids=("",))
        )


def test_blank_concept_mapping_rejected() -> None:
    with pytest.raises(InvalidConceptMapping):
        validate_evidence_for_interpretation(make_bundle(concept_ids=("",)))


def test_broken_observation_reference() -> None:
    item = make_item(observation_id="obs-1")
    with pytest.raises(BrokenEvidenceReference):
        validate_evidence_for_interpretation(
            make_bundle(items=(item,), observation_ids=("obs-missing",))
        )


def test_null_bundle_rejected() -> None:
    with pytest.raises(UnsupportedEvidenceSchema):
        validate_evidence_for_interpretation(None)


def test_summary_count_mismatch() -> None:
    with pytest.raises(UnsupportedEvidenceSchema):
        validate_evidence_for_interpretation(make_bundle(summary_count=99))


def test_empty_concept_ids_allowed() -> None:
    bundle = validate_evidence_for_interpretation(make_bundle(concept_ids=()))
    assert bundle.metadata.concept_ids == ()
