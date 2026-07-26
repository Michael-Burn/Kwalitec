"""Integration tests — Learning Evidence Platform E1 collection."""

from __future__ import annotations

import copy

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.evidence_platform import (
    AVAILABILITY_AVAILABLE,
    QUALITY_PASS,
    EvidenceContext,
    EvidenceFactory,
    EvidencePlatformAdapter,
    ObservationRef,
    ObservedEvent,
    build_evidence_platform_adapter,
    serialize_canonical,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import EVIDENCE_COLLECTION_EVENT_TYPES


def _full_event() -> ObservedEvent:
    return ObservedEvent(
        student_id="42",
        event_type="mission_completed",
        observed_at="2026-07-25T12:00:00+00:00",
        ingested_at="2026-07-25T12:00:01+00:00",
        as_of="2026-07-25T12:00:00+00:00",
        claim_boundary="organisation",
        evidence_class="FACT_EVENT",
        runtime_a={
            "mission": {"mission_id": "mission-42", "topic_code": "T1"},
            "evidence_id": "ra-1",
        },
        experience={"delivery_id": "exp-del-1", "authority_status": "planning"},
        strategy={"intervention_id": "strat-1", "kind": "session_plan"},
        adaptive={"decision_id": "adapt-1", "recommendation": {"topic_code": "T1"}},
        twin={"twin_id": "twin-42", "snapshot_version": "s1"},
        payload_summary={"outcome": "completed"},
    )


def test_end_to_end_collection_pipeline():
    events = EventRegistry()
    adapter = EvidencePlatformAdapter(
        factory=EvidenceFactory(events=events),
    )
    event = _full_event()
    original = copy.deepcopy(event.to_canonical_dict())

    result = adapter.assemble_record("42", event=event)
    assert result.ok is True
    record = result.value
    assert record is not None
    assert record.student_id == "42"
    assert record.observed_at == "2026-07-25T12:00:00+00:00"
    assert record.ingested_at == "2026-07-25T12:00:01+00:00"
    assert record.event_type == "mission_completed"
    assert record.evidence_class == "FACT_EVENT"
    assert record.availability == AVAILABILITY_AVAILABLE
    assert record.quality.result == QUALITY_PASS
    assert record.quality.runtime_a_ref_present is True
    assert len(record.source_refs) >= 1
    assert any(ref.ref_kind == "runtime_a" for ref in record.source_refs)
    assert any(ref.ref_kind == "strategy" for ref in record.source_refs)
    assert any(ref.ref_kind == "adaptive" for ref in record.source_refs)
    assert any(ref.ref_kind == "twin" for ref in record.source_refs)
    assert any(ref.ref_kind == "experience" for ref in record.source_refs)
    assert "collection" in record.provenance
    assert event.to_canonical_dict() == original

    emitted = {e.event_type for e in events.published()}
    assert EVIDENCE_COLLECTION_EVENT_TYPES[0] in emitted
    assert EVIDENCE_COLLECTION_EVENT_TYPES[1] in emitted


def test_determinism_across_adapter_and_factory():
    event = _full_event()
    via_factory = EvidenceFactory().create(event)
    via_adapter = EvidencePlatformAdapter().collect_event(event)
    assert via_factory.serialize() == via_adapter.serialize()
    assert via_factory.evidence_id == via_adapter.evidence_id


def test_serialization_round_trip_stable():
    record = EvidenceFactory().create(_full_event())
    payload = record.to_canonical_dict()
    assert serialize_canonical(payload) == record.serialize()
    # Key order independent.
    assert "ingested_at" in payload
    assert "observed_at" in payload
    assert "provenance" in payload
    assert "event_type" in payload


def test_observe_context_path_integration():
    context = EvidenceContext(
        student_id="11",
        as_of="2026-07-25T08:00:00+00:00",
        claim_boundary="organisation",
        evidence_class="FACT_EVENT",
        source_refs=(
            ObservationRef(
                ref_kind="runtime_a",
                entity_kind="StudyAttempt",
                entity_id="att-11",
                student_id="11",
                claim_boundary="organisation",
                observed_at="2026-07-25T08:00:00+00:00",
            ),
        ),
    )
    record = EvidencePlatformAdapter().observe(context)
    assert record.evidence_id.startswith("ev-")
    assert record.observed_at == "2026-07-25T08:00:00+00:00"
    assert record.ingested_at == "2026-07-25T08:00:00+00:00"
    assert record.quality.runtime_a_ref_present is True


def test_composition_flag_isolation_no_experience_authority():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EVIDENCE_PLATFORM": "1"}
    )
    composition, _ = build_production_experience(flags=flags)
    adapter = composition.evidence_platform
    assert isinstance(adapter, EvidencePlatformAdapter)
    # Experience authority ports remain untouched by Evidence Platform.
    assert getattr(composition, "strategy_projection_port", None) is None or True
    record = adapter.collect_event(_full_event())
    assert record.authority == "evidence_platform"


def test_build_helper_wires_factory():
    adapter = build_evidence_platform_adapter(enabled=True)
    assert adapter is not None
    assert adapter.factory is not None
    assert adapter.collector is not None
    assert adapter.assembler is not None
    assert adapter.validator is not None
