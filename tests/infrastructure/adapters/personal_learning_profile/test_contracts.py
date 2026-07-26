"""Contract tests for Personal Learning Profile (EP-004.1)."""

from __future__ import annotations

import pytest

from app.infrastructure.adapters.personal_learning_profile import (
    ATTR_PREFERRED_STUDY_WINDOWS,
    KIND_UNSUPPORTED,
    PROFILE_ATTRIBUTE_KEYS,
    STATUS_UNSUPPORTED,
    PersonalLearningProfile,
    ProfileAttribute,
    ProfileEvidenceRef,
    confidence_from_sample_size,
    deterministic_profile_id,
)


def _base_attrs(**overrides: ProfileAttribute) -> dict[str, ProfileAttribute]:
    attrs: dict[str, ProfileAttribute] = {}
    for key in PROFILE_ATTRIBUTE_KEYS:
        attrs[key] = ProfileAttribute(
            key=key,
            kind=KIND_UNSUPPORTED,
            status=STATUS_UNSUPPORTED,
            claim_boundary="unsupported_assumption",
            explanation="placeholder",
        )
    attrs.update(overrides)
    return attrs


def test_confidence_from_sample_size_is_deterministic():
    assert confidence_from_sample_size(0) == 0.0
    assert confidence_from_sample_size(1) == 0.1
    assert confidence_from_sample_size(10) == 1.0
    assert confidence_from_sample_size(25) == 1.0


def test_profile_requires_all_attribute_keys():
    with pytest.raises(ValueError, match="missing required attributes"):
        PersonalLearningProfile(
            profile_id="plp-x",
            student_id="1",
            as_of="2026-07-26T10:00:00Z",
            attributes={},
            evidence_fingerprint="abc",
        )


def test_forbidden_inference_rejected_in_provenance():
    with pytest.raises(ValueError, match="forbidden inference"):
        PersonalLearningProfile(
            profile_id="plp-x",
            student_id="1",
            as_of="2026-07-26T10:00:00Z",
            attributes=_base_attrs(),
            evidence_fingerprint="abc",
            provenance={"mastery": 0.9},
        )


def test_unsupported_kind_requires_unsupported_status():
    with pytest.raises(ValueError, match="kind=unsupported"):
        ProfileAttribute(
            key=ATTR_PREFERRED_STUDY_WINDOWS,
            kind=KIND_UNSUPPORTED,
            status="available",
            claim_boundary="unsupported_assumption",
        )


def test_evidence_ref_requires_feedback_id():
    with pytest.raises(ValueError, match="feedback_id"):
        ProfileEvidenceRef(
            feedback_id="",
            event_type="plan_completed",
            source_authority="planning_service",
        )


def test_deterministic_profile_id_stable():
    a = deterministic_profile_id(
        student_id="7",
        as_of="2026-07-26T10:00:00Z",
        evidence_fingerprint="fp1",
    )
    b = deterministic_profile_id(
        student_id="7",
        as_of="2026-07-26T10:00:00Z",
        evidence_fingerprint="fp1",
    )
    assert a == b
    assert a.startswith("plp-")


def test_consumer_view_hides_implementation_fingerprint():
    profile = PersonalLearningProfile(
        profile_id="plp-demo",
        student_id="9",
        as_of="2026-07-26T10:00:00Z",
        attributes=_base_attrs(),
        evidence_fingerprint="secret-fingerprint",
        evidence_event_count=0,
    )
    view = profile.consumer_view()
    assert "evidence_fingerprint" not in view
    assert view["student_id"] == "9"
    assert set(view["attributes"]) == set(PROFILE_ATTRIBUTE_KEYS)
