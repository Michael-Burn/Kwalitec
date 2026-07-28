"""Ingress mapping + traceability tests (AP-002D1)."""

from __future__ import annotations

from app.application.assessment_pipeline.evidence_ingress import (
    INGRESS_CONTRACT_VERSION,
    INGRESS_TRIGGERED_BY,
    EvidenceIngressRequest,
    map_evidence_bundle,
)
from tests.application.assessment_pipeline.evidence_ingress.conftest import make_bundle


def test_mapping_preserves_traceability_identifiers() -> None:
    bundle = make_bundle(
        bundle_id="bundle-trace",
        session_id="sess-trace",
        learning_objective_ids=("lo-alpha", "lo-beta"),
    )
    request = EvidenceIngressRequest(
        twin_id="twin-1",
        bundle=bundle,
        correlation_id="corr-abc",
        reasoning_request_id="rrq-fixed",
    )
    mapping = map_evidence_bundle(request)

    assert mapping.triggered_by == INGRESS_TRIGGERED_BY
    assert mapping.reasoning_request_id == "rrq-fixed"
    trace = mapping.traceability
    assert trace.assessment_session_id == "sess-trace"
    assert trace.evidence_bundle_id == "bundle-trace"
    assert trace.observation_ids == ("obs-1", "obs-2")
    assert "q-1" in trace.question_references
    assert "q-2" in trace.question_references
    assert trace.learning_objective_references == ("lo-alpha", "lo-beta")
    assert trace.correlation_id == "corr-abc"
    assert trace.reasoning_request_id == "rrq-fixed"
    assert trace.ingress_contract_version == INGRESS_CONTRACT_VERSION
    assert trace.packaging_version == "AP-002C.1"


def test_mapping_embeds_traceability_in_observation_metadata() -> None:
    request = EvidenceIngressRequest(
        twin_id="twin-1",
        bundle=make_bundle(),
        correlation_id="corr-meta",
        reasoning_request_id="rrq-meta",
    )
    mapping = map_evidence_bundle(request)
    assert len(mapping.observations) == 2
    for obs in mapping.observations:
        assert obs.metadata["correlation_id"] == "corr-meta"
        assert obs.metadata["reasoning_request_id"] == "rrq-meta"
        assert obs.metadata["evidence_bundle_id"] == "bundle-1"
        assert obs.metadata["assessment_session_id"] == "sess-1"
        assert obs.metadata["packaging_version"] == "AP-002C.1"
        assert obs.provenance.startswith("assessment_pipeline:evidence_bundle:")
        assert obs.evidence_reference.startswith("evidence_bundle:bundle-1:")


def test_mapping_sets_correct_flag_from_correctness() -> None:
    mapping = map_evidence_bundle(
        EvidenceIngressRequest(
            twin_id="twin-1",
            bundle=make_bundle(),
            correlation_id="corr-1",
        )
    )
    by_obs = {o.source_observation_id: o for o in mapping.observations}
    assert by_obs["obs-1"].correct is True
    assert by_obs["obs-2"].correct is False
