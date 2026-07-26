"""Unit tests — Twin Input Adapter (MS-004 T4)."""

from __future__ import annotations

from types import MappingProxyType

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.adaptive_engine import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    FIELD_TWIN,
    AdaptiveEngineExecutor,
    AdaptiveInputBundle,
    TwinAdaptiveInputAttachment,
    TwinInputAdapter,
    build_twin_input_adapter,
    serialize_canonical,
    twin_attachment_is_available,
)
from app.infrastructure.adapters.adaptive_engine.twin_input import (
    REASON_TWIN_UNAVAILABLE,
)
from app.infrastructure.adapters.digital_twin import (
    AVAILABILITY_UNAVAILABLE as TWIN_FACET_UNAVAILABLE,
)
from app.infrastructure.adapters.digital_twin import (
    CompletenessEvaluator,
    ConsistencyFacet,
    FacetExplanation,
    LearningRhythmFacet,
    SnapshotExplanation,
    TwinCompleteness,
    TwinProfile,
    TwinProvenance,
    TwinSnapshot,
    UnavailableSummary,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)


def _sample_snapshot(*, student_id: str = "42") -> TwinSnapshot:
    return TwinSnapshot(
        profile=TwinProfile(
            student_id=student_id,
            learning_rhythm=LearningRhythmFacet(
                label="steady",
                typical_session_minutes=25.0,
                availability="available",
                unavailable_reason="",
                evidence_refs=("attempt:1",),
            ),
            consistency=ConsistencyFacet(
                label="regular",
                availability="available",
                unavailable_reason="",
                evidence_refs=("mission:9",),
            ),
            limitations_codes=("sparse_predictions",),
        ),
        profile_version="t1.0",
        source_evidence_version="ev-1",
        generated_at="2026-07-25T10:00:00",
        provenance=TwinProvenance(
            source_service="twin_snapshot_builder",
            source_entity="TwinSnapshot",
            collected_at="2026-07-25T10:00:00",
            availability="available",
            kind="twin_derived",
        ),
        completeness=TwinCompleteness(
            score=None,
            facets_present=("consistency", "learning_rhythm"),
            facets_unavailable=("cognitive_load_indicators",),
            status="partial",
            summary="partial structural coverage",
        ),
        twin_id=f"twin-{student_id}",
        snapshot_version="t2.0",
        schema_version="twin_snapshot.v2",
        unavailable_summary=UnavailableSummary(
            facets=("cognitive_load_indicators",),
            reasons={"cognitive_load_indicators": "estimate_deferred"},
        ),
    )


def _sample_explanation(snapshot: TwinSnapshot) -> SnapshotExplanation:
    return SnapshotExplanation(
        twin_id=snapshot.twin_id,
        student_id=snapshot.profile.student_id,
        generated_at=snapshot.generated_at,
        explainability_version="t3.0",
        overall_completeness_explanation="partial",
        unavailable_summary_explanation="some facets unavailable",
        evidence_coverage_summary="runtime_a refs present",
        facet_explanations=(
            FacetExplanation(
                facet_name="learning_rhythm",
                availability="available",
                contributing_runtime_a_evidence=("attempt:1",),
                derivation_summary="from study attempts",
                completeness_reasoning="present",
                provenance_refs=("study_attempts",),
                rule_or_model_id="twin.structure.learning_rhythm",
                rule_version="t3.0",
            ),
        ),
        provenance_refs=("study_attempts",),
    )


def test_project_reads_snapshot_explanation_and_provenance():
    adapter = TwinInputAdapter()
    snapshot = _sample_snapshot()
    explanation = _sample_explanation(snapshot)
    attachment = adapter.project(snapshot, explanation=explanation)

    assert isinstance(attachment, TwinAdaptiveInputAttachment)
    assert attachment.availability == AVAILABILITY_AVAILABLE
    assert attachment.twin_id == "twin-42"
    assert attachment.twin_snapshot_ref.startswith("twin-")
    assert attachment.behaviour["learning_rhythm"]["label"] == "steady"
    assert attachment.memory["confidence_trend"]["availability"] == (
        TWIN_FACET_UNAVAILABLE
    )
    assert "cognitive_load_indicators" in attachment.predictions
    assert "sparse_predictions" in attachment.limitations
    assert attachment.provenance["source_evidence_version"] == "ev-1"
    assert attachment.explanation["explainability_version"] == "t3.0"
    assert attachment.completeness["status"] == "partial"


def test_project_is_deterministic():
    adapter = TwinInputAdapter()
    snapshot = _sample_snapshot()
    explanation = _sample_explanation(snapshot)
    left = adapter.project(snapshot, explanation=explanation).serialize()
    right = adapter.project(snapshot, explanation=explanation).serialize()
    assert left == right
    assert serialize_canonical(adapter.project(snapshot).to_canonical_dict()) == (
        adapter.project(snapshot).serialize()
    )


def test_enrich_bundle_fail_open_without_snapshot():
    adapter = TwinInputAdapter()
    base = AdaptiveInputBundle(
        student_id="42",
        as_of="2026-07-25",
        evidence={"attempt_count": 1},
        authority_tags=("runtime_a",),
    )
    enriched = adapter.enrich_bundle(base, snapshot=None, collected_at="2026-07-25")
    assert enriched.evidence == base.evidence
    assert enriched.twin["availability"] == AVAILABILITY_UNAVAILABLE
    assert enriched.twin["unavailable_reason"] == REASON_TWIN_UNAVAILABLE
    assert FIELD_TWIN in enriched.field_provenance
    assert not twin_attachment_is_available(enriched.twin)


def test_enrich_bundle_attaches_available_twin():
    adapter = TwinInputAdapter()
    base = AdaptiveInputBundle(student_id="42", as_of="2026-07-25")
    snapshot = _sample_snapshot()
    enriched = adapter.enrich_bundle(
        base,
        snapshot=snapshot,
        explanation=_sample_explanation(snapshot),
        collected_at="2026-07-25",
    )
    assert twin_attachment_is_available(enriched.twin)
    assert enriched.twin["twin_snapshot_ref"] == adapter.twin_snapshot_ref(snapshot)
    assert "digital_twin_synthesis" in enriched.authority_tags
    assert dict(enriched.field_provenance[FIELD_TWIN])["availability"] == (
        AVAILABILITY_AVAILABLE
    )


def test_enrich_rejects_student_id_mismatch():
    adapter = TwinInputAdapter()
    base = AdaptiveInputBundle(student_id="42", as_of="2026-07-25")
    snapshot = _sample_snapshot(student_id="99")
    enriched = adapter.enrich_bundle(base, snapshot=snapshot)
    assert enriched.twin["availability"] == AVAILABILITY_UNAVAILABLE
    assert enriched.twin["unavailable_reason"] == "twin_invalid_snapshot"


def test_twin_snapshot_immutable_after_project():
    adapter = TwinInputAdapter()
    snapshot = _sample_snapshot()
    before = snapshot.serialize()
    adapter.project(snapshot)
    after = snapshot.serialize()
    assert before == after
    with pytest.raises(Exception):
        snapshot.twin_id = "mutated"  # type: ignore[misc]


def test_attachment_frozen_mappings():
    attachment = TwinAdaptiveInputAttachment(
        twin_snapshot_ref="twin-abc",
        behaviour={"consistency": {"label": "x"}},
        availability="available",
    )
    assert isinstance(attachment.behaviour, MappingProxyType)
    with pytest.raises(TypeError):
        attachment.behaviour["consistency"] = {}  # type: ignore[index]


def test_executor_lists_twin_in_inputs_used_without_changing_runtime_a_selection():
    adapter = TwinInputAdapter()
    base = AdaptiveInputBundle(
        student_id="42",
        as_of="2026-07-25",
        curriculum={
            "leaves": [{"topic_id": "T1", "topic_name": "Intro"}],
            "leaf_count": 1,
        },
        field_provenance={
            "evidence": {
                "source_service": "s",
                "source_entity": "e",
                "collected_at": "2026-07-25",
                "availability": "unavailable",
                "unavailable_reason": "UNAVAILABLE",
            },
            "topic_progress": {
                "source_service": "s",
                "source_entity": "e",
                "collected_at": "2026-07-25",
                "availability": "unavailable",
                "unavailable_reason": "UNAVAILABLE",
            },
            "study_attempts": {
                "source_service": "s",
                "source_entity": "e",
                "collected_at": "2026-07-25",
                "availability": "unavailable",
                "unavailable_reason": "UNAVAILABLE",
            },
            "mission": {
                "source_service": "s",
                "source_entity": "e",
                "collected_at": "2026-07-25",
                "availability": "unavailable",
                "unavailable_reason": "UNAVAILABLE",
            },
            "readiness": {
                "source_service": "s",
                "source_entity": "e",
                "collected_at": "2026-07-25",
                "availability": "unavailable",
                "unavailable_reason": "UNAVAILABLE",
            },
            "curriculum": {
                "source_service": "s",
                "source_entity": "e",
                "collected_at": "2026-07-25",
                "availability": "available",
                "unavailable_reason": "",
            },
            "student_goals": {
                "source_service": "s",
                "source_entity": "e",
                "collected_at": "2026-07-25",
                "availability": "unavailable",
                "unavailable_reason": "UNAVAILABLE",
            },
            "lifecycle_stage": {
                "source_service": "s",
                "source_entity": "e",
                "collected_at": "2026-07-25",
                "availability": "unavailable",
                "unavailable_reason": "UNAVAILABLE",
            },
        },
    )
    with_twin = adapter.enrich_bundle(base, snapshot=_sample_snapshot())
    executor = AdaptiveEngineExecutor()
    without = executor.evaluate(base)
    with_out = executor.evaluate(with_twin)
    assert without.recommendation.topic_code == with_out.recommendation.topic_code
    assert FIELD_TWIN in with_out.explanation.inputs_used
    assert any(
        ref.kind == "twin_snapshot" for ref in with_out.explanation.evidence_refs
    )


def test_build_twin_input_adapter_flag_gate():
    assert build_twin_input_adapter(enabled=False) is None
    wired = build_twin_input_adapter(enabled=True)
    assert isinstance(wired, TwinInputAdapter)


def test_feature_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_DIGITAL_TWIN is False


def test_composition_wires_twin_input_when_digital_twin_on(monkeypatch):
    monkeypatch.setenv("KWALITEC_DIGITAL_TWIN", "1")
    monkeypatch.setenv("KWALITEC_ADAPTIVE_ENGINE", "1")
    composition, _service = build_production_experience()
    assert composition.twin_input_adapter is not None
    assert composition.adaptive_input_assembler is not None
    assert composition.adaptive_input_assembler.twin_input is (
        composition.twin_input_adapter
    )


def test_composition_omits_twin_input_when_flag_off(monkeypatch):
    monkeypatch.delenv("KWALITEC_DIGITAL_TWIN", raising=False)
    monkeypatch.setenv("KWALITEC_ADAPTIVE_ENGINE", "1")
    composition, _service = build_production_experience()
    assert composition.twin_input_adapter is None
    assert composition.adaptive_input_assembler is not None
    assert composition.adaptive_input_assembler.twin_input is None


def test_completeness_evaluator_still_independent():
    # Sanity: Twin completeness helpers remain usable for fixture assembly.
    evaluator = CompletenessEvaluator()
    assert evaluator is not None
