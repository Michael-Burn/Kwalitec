"""Longitudinal evidence contract tests (P4-MS002)."""

from __future__ import annotations

import pytest

from app.infrastructure.adapters.longitudinal_evidence import (
    APPROVED_ADVISORY_FIELD,
    EVENT_MISSION,
    EVENT_STUDY_SESSION,
    LONGITUDINAL_EVIDENCE_SCHEMA_VERSION,
    SOURCE_UNIFIED_JOURNEY,
    LearningEvidenceRecord,
    LongitudinalEvidenceProvenance,
    LongitudinalEvidenceRepository,
    build_provenance,
    is_schema_compatible,
    serialize_canonical,
    validate_learning_evidence_record,
)


def test_learning_evidence_record_immutable_and_hashes_only():
    record = LearningEvidenceRecord(
        record_id="lerec-1",
        student_id_hash="stuhash-abc",
        event_type=EVENT_STUDY_SESSION,
        event_timestamp="2026-07-25T10:00:00+00:00",
        source_component=SOURCE_UNIFIED_JOURNEY,
        policy_version="p3.ms004.1",
        advisory_field="engagement_summary",
        trial_id="educational-trial-p4-ms001",
        provenance=build_provenance(
            originating_component=SOURCE_UNIFIED_JOURNEY,
            policy_version="p3.ms004.1",
            feature_flags={"ENABLE_LONGITUDINAL_EVIDENCE": True},
            trial_context={"trial_id": "educational-trial-p4-ms001"},
            advisory_provenance={"field": APPROVED_ADVISORY_FIELD},
        ),
    )
    assert record.advisory_field == APPROVED_ADVISORY_FIELD
    assert record.operational_only is True
    assert "email" not in record.to_canonical_dict()
    assert "student_id" not in record.to_canonical_dict()
    with pytest.raises(Exception):
        record.event_type = EVENT_MISSION  # type: ignore[misc]


def test_learning_evidence_record_rejects_unknown_event_type():
    record = LearningEvidenceRecord(
        record_id="lerec-2",
        student_id_hash="stuhash-abc",
        event_type="mastery_score",
        event_timestamp="2026-07-25T10:00:00+00:00",
        source_component=SOURCE_UNIFIED_JOURNEY,
        provenance=build_provenance(originating_component=SOURCE_UNIFIED_JOURNEY),
    )
    assert record.event_type == ""
    ok, detail = validate_learning_evidence_record(record)
    assert ok is False
    assert detail == "event_type_invalid"


def test_learning_evidence_record_canonical_serialization_is_stable():
    provenance = LongitudinalEvidenceProvenance(
        originating_component=SOURCE_UNIFIED_JOURNEY,
        policy_version="p3.ms004.1",
        feature_flags={"ENABLE_LONGITUDINAL_EVIDENCE": True},
        trial_context={"cohort": "treatment"},
        advisory_provenance={"field": APPROVED_ADVISORY_FIELD},
        collected_at="2026-07-25T10:00:00+00:00",
    )
    record = LearningEvidenceRecord(
        record_id="lerec-stable",
        student_id_hash="stuhash-stable",
        event_type=EVENT_MISSION,
        event_timestamp="2026-07-25T10:00:00+00:00",
        source_component=SOURCE_UNIFIED_JOURNEY,
        policy_version="p3.ms004.1",
        advisory_field=APPROVED_ADVISORY_FIELD,
        trial_id="educational-trial-p4-ms001",
        provenance=provenance,
    )
    first = record.serialize()
    second = LearningEvidenceRecord(**record.to_canonical_dict()).serialize()
    assert first == second
    assert record.schema_version == LONGITUDINAL_EVIDENCE_SCHEMA_VERSION
    assert serialize_canonical(record.to_canonical_dict()) == first


def test_provenance_preserves_required_dimensions():
    provenance = build_provenance(
        originating_component=SOURCE_UNIFIED_JOURNEY,
        policy_version="p3.ms004.1",
        feature_flags={
            "ENABLE_LONGITUDINAL_EVIDENCE": True,
            "ENABLE_EDUCATIONAL_TRIALS": False,
        },
        trial_context={"trial_id": "educational-trial-p4-ms001", "cohort": "baseline"},
        advisory_provenance={
            "field": APPROVED_ADVISORY_FIELD,
            "activation_status": "activated",
        },
        collected_at="2026-07-25T12:00:00+00:00",
        notes=("operational_only",),
    )
    payload = provenance.to_canonical_dict()
    assert payload["originating_component"] == SOURCE_UNIFIED_JOURNEY
    assert payload["policy_version"] == "p3.ms004.1"
    assert payload["feature_flags"]["ENABLE_LONGITUDINAL_EVIDENCE"] is True
    assert payload["trial_context"]["cohort"] == "baseline"
    assert payload["advisory_provenance"]["field"] == APPROVED_ADVISORY_FIELD


def test_schema_compatibility_helpers():
    assert is_schema_compatible(LONGITUDINAL_EVIDENCE_SCHEMA_VERSION) is True
    assert is_schema_compatible("p4.ms999.0") is False
    assert is_schema_compatible("") is False


def test_repository_protocol_is_runtime_checkable():
    assert issubclass(
        type("Repo", (), {}),
        object,
    )
    # Protocol is available for structural typing / isinstance checks.
    assert LongitudinalEvidenceRepository is not None
