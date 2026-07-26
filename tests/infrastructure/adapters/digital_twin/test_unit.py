"""Unit / serialization / immutability tests — Digital Twin Contracts (T0)."""

from __future__ import annotations

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.digital_twin import (
    CognitiveLoadIndicatorsFacet,
    ConsistencyFacet,
    DigitalTwinAdapter,
    LearningRhythmFacet,
    TwinCompleteness,
    TwinProfile,
    TwinProvenance,
    TwinSnapshot,
    empty_twin_snapshot,
    serialize_canonical,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)


def test_snapshot_is_immutable():
    snapshot = empty_twin_snapshot(profile=TwinProfile(student_id="7"))
    with pytest.raises(Exception):
        snapshot.profile_version = "mutated"  # type: ignore[misc]
    with pytest.raises(Exception):
        snapshot.provenance.source_service = "x"  # type: ignore[misc]
    with pytest.raises(TypeError):
        snapshot.field_provenance["k"] = "v"  # type: ignore[index]


def test_profile_and_facets_are_immutable():
    profile = TwinProfile(
        student_id="7",
        learning_rhythm=LearningRhythmFacet(
            label="sparse",
            evidence_refs=("a1",),
        ),
        consistency=ConsistencyFacet(label="sparse"),
        limitations_codes=("estimate_deferred",),
    )
    with pytest.raises(Exception):
        profile.student_id = "8"  # type: ignore[misc]
    with pytest.raises(Exception):
        profile.learning_rhythm.label = "mutated"  # type: ignore[misc]
    with pytest.raises(AttributeError):
        profile.limitations_codes.append("x")  # type: ignore[attr-defined]
    with pytest.raises(AttributeError):
        profile.learning_rhythm.evidence_refs.append("a2")  # type: ignore[attr-defined]


def test_completeness_and_provenance_immutable():
    completeness = TwinCompleteness(
        facets_unavailable=("learning_rhythm",),
        summary="empty",
    )
    provenance = TwinProvenance(
        source_service="digital_twin",
        availability="unavailable",
        kind="twin_derived",
    )
    with pytest.raises(Exception):
        completeness.summary = "x"  # type: ignore[misc]
    with pytest.raises(Exception):
        provenance.kind = "fact"  # type: ignore[misc]


def test_identical_snapshots_serialize_identically():
    left = TwinSnapshot(
        profile=TwinProfile(
            student_id="1",
            learning_rhythm=LearningRhythmFacet(
                label="a",
                typical_session_minutes=30.0,
                evidence_refs=("e2", "e1"),
            ),
            consistency=ConsistencyFacet(label="b", adherence_note="ok"),
            cognitive_load_indicators=CognitiveLoadIndicatorsFacet(
                label="c",
                load_note="deferred",
            ),
            limitations_codes=("estimate_deferred", "sparse_evidence"),
            limitations_summary="T0 placeholder",
        ),
        profile_version="t0.1",
        source_evidence_version="ev-1",
        generated_at="2026-07-25T10:00:00+00:00",
        provenance=TwinProvenance(
            source_service="digital_twin",
            source_entity="TwinSnapshot",
            collected_at="2026-07-25T10:00:00+00:00",
            availability="unavailable",
            unavailable_reason="contracts_only_no_synthesis",
            kind="twin_derived",
        ),
        completeness=TwinCompleteness(
            score=None,
            facets_present=(),
            facets_unavailable=(
                "cognitive_load_indicators",
                "confidence_trend",
                "consistency",
                "learning_rhythm",
                "persistence",
                "revision_behaviour",
                "session_habits",
            ),
            summary="T0 contracts only — Twin synthesis not implemented.",
        ),
        twin_id="twin-1",
        field_provenance={"learning_rhythm": {"availability": "unavailable"}},
    )
    right = TwinSnapshot(
        profile=TwinProfile(
            student_id="1",
            learning_rhythm=LearningRhythmFacet(
                label="a",
                typical_session_minutes=30.0,
                evidence_refs=("e2", "e1"),
            ),
            consistency=ConsistencyFacet(adherence_note="ok", label="b"),
            cognitive_load_indicators=CognitiveLoadIndicatorsFacet(
                load_note="deferred",
                label="c",
            ),
            limitations_codes=("estimate_deferred", "sparse_evidence"),
            limitations_summary="T0 placeholder",
        ),
        profile_version="t0.1",
        source_evidence_version="ev-1",
        generated_at="2026-07-25T10:00:00+00:00",
        provenance=TwinProvenance(
            source_entity="TwinSnapshot",
            source_service="digital_twin",
            collected_at="2026-07-25T10:00:00+00:00",
            availability="unavailable",
            unavailable_reason="contracts_only_no_synthesis",
            kind="twin_derived",
        ),
        completeness=TwinCompleteness(
            score=None,
            facets_present=(),
            facets_unavailable=(
                "cognitive_load_indicators",
                "confidence_trend",
                "consistency",
                "learning_rhythm",
                "persistence",
                "revision_behaviour",
                "session_habits",
            ),
            summary="T0 contracts only — Twin synthesis not implemented.",
        ),
        twin_id="twin-1",
        field_provenance={"learning_rhythm": {"availability": "unavailable"}},
    )
    assert left.serialize() == right.serialize()
    assert serialize_canonical(left.to_canonical_dict()) == left.serialize()


def test_snapshot_method_is_deterministic():
    adapter = DigitalTwinAdapter()
    profile = TwinProfile(student_id="99")
    first = adapter.snapshot(profile)
    second = adapter.snapshot(profile)
    assert first.serialize() == second.serialize()


def test_assemble_rejects_empty_student_id():
    result = DigitalTwinAdapter().assemble_snapshot(" ")
    assert result.ok is False
    assert result.error_code == "INVALID_STATE"


def test_assemble_rejects_mismatched_profile_student_id():
    result = DigitalTwinAdapter().assemble_snapshot(
        "1",
        profile=TwinProfile(student_id="2"),
    )
    assert result.ok is False
    assert result.error_code == "INVALID_STATE"


def test_flag_default_off_and_di_wiring():
    flags_off = resolve_v2_feature_flags(environ={})
    assert flags_off.ENABLE_DIGITAL_TWIN is False
    composition_off, _ = build_production_experience(flags=flags_off)
    assert composition_off.digital_twin is None
    # Experience TwinPort remains the prior path — unchanged by T0.
    assert composition_off.twin is not None

    flags_on = resolve_v2_feature_flags(environ={"KWALITEC_DIGITAL_TWIN": "1"})
    assert flags_on.ENABLE_DIGITAL_TWIN is True
    composition_on, _ = build_production_experience(flags=flags_on)
    assert isinstance(composition_on.digital_twin, DigitalTwinAdapter)
    assert composition_on.digital_twin.adapter_id == "digital_twin"
    # T0 must not cut over Experience StudentTwinPort to Digital Twin.
    assert composition_on.digital_twin is not composition_on.twin


def test_empty_snapshot_exposes_required_metadata():
    snapshot = empty_twin_snapshot(
        profile=TwinProfile(student_id="5"),
        generated_at="2026-07-25",
    )
    assert snapshot.profile_version == "t0.1"
    assert snapshot.source_evidence_version == ""
    assert snapshot.generated_at == "2026-07-25"
    assert snapshot.provenance.availability == "unavailable"
    assert snapshot.completeness.facets_present == ()
    assert "learning_rhythm" in snapshot.completeness.facets_unavailable
