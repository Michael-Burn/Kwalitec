"""Unit tests — Learning Evidence Platform E1 collection."""

from __future__ import annotations

import copy
from dataclasses import FrozenInstanceError

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.evidence_platform import (
    AUTHORITY_EVIDENCE_PLATFORM,
    QUALITY_INELIGIBLE,
    QUALITY_PASS,
    CollectedObservation,
    EvidenceAssembler,
    EvidenceCollector,
    EvidenceContext,
    EvidenceFactory,
    EvidencePlatformAdapter,
    EvidenceRecord,
    EvidenceValidationError,
    EvidenceValidator,
    ObservationRef,
    ObservedEvent,
    build_evidence_assembler,
    build_evidence_collector,
    build_evidence_factory,
    build_evidence_platform_adapter,
    build_evidence_validator,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.diagnostics.dual_run import build_dual_run_status
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    EVIDENCE_COLLECTION_COMPLETED,
    EVIDENCE_COLLECTION_REQUESTED,
)


def test_evidence_platform_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_EVIDENCE_PLATFORM is False
    dual = build_dual_run_status(flags=flags)
    assert dual.evidence_platform is False


def test_evidence_platform_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EVIDENCE_PLATFORM": "1"}
    )
    assert flags.ENABLE_EVIDENCE_PLATFORM is True
    dual = build_dual_run_status(flags=flags)
    assert dual.evidence_platform is True


def test_composition_wires_adapter_only_when_flag_on():
    flags_off = resolve_v2_feature_flags(environ={})
    assert flags_off.ENABLE_EVIDENCE_PLATFORM is False
    composition_off, _ = build_production_experience(flags=flags_off)
    assert composition_off.evidence_platform is None

    flags_on = resolve_v2_feature_flags(
        environ={"KWALITEC_EVIDENCE_PLATFORM": "1"}
    )
    assert flags_on.ENABLE_EVIDENCE_PLATFORM is True
    composition_on, _ = build_production_experience(flags=flags_on)
    assert isinstance(composition_on.evidence_platform, EvidencePlatformAdapter)
    assert isinstance(composition_on.evidence_platform.factory, EvidenceFactory)


def test_build_helpers_off_by_default():
    assert build_evidence_platform_adapter(enabled=False) is None
    assert build_evidence_collector(enabled=False) is None
    assert build_evidence_assembler(enabled=False) is None
    assert build_evidence_factory(enabled=False) is None
    assert isinstance(build_evidence_validator(), EvidenceValidator)


def _mission_event(**overrides) -> ObservedEvent:
    base = {
        "student_id": "42",
        "event_type": "mission_completed",
        "observed_at": "2026-07-25T10:00:00+00:00",
        "ingested_at": "2026-07-25T10:00:05+00:00",
        "as_of": "2026-07-25T10:00:00+00:00",
        "claim_boundary": "organisation",
        "evidence_class": "FACT_EVENT",
        "runtime_a": {
            "mission": {"mission_id": "m-9", "status": "completed"},
            "evidence_id": "ra-ev-1",
        },
        "strategy": {"intervention_id": "int-1"},
        "adaptive": {"decision_id": "adaptive-7"},
        "twin": {"twin_id": "twin-3", "snapshot_version": "snap-1"},
        "experience": {"delivery_id": "del-1"},
        "payload_summary": {"mission_status": "completed"},
    }
    base.update(overrides)
    return ObservedEvent(**base)


def test_collector_freezes_without_mutating_inputs():
    runtime_a = {"mission": {"mission_id": "m-1", "status": "completed"}}
    event = ObservedEvent(
        student_id="7",
        event_type="mission_completed",
        observed_at="2026-07-25T00:00:00+00:00",
        ingested_at="2026-07-25T00:00:00+00:00",
        runtime_a=runtime_a,
    )
    original = copy.deepcopy(dict(runtime_a))
    observation = EvidenceCollector().collect(event)
    assert isinstance(observation, CollectedObservation)
    assert runtime_a == original
    runtime_a["mission"]["status"] = "mutated"
    assert observation.source_refs[0].entity_id == "m-1"
    assert observation.observed_at == "2026-07-25T00:00:00+00:00"
    assert observation.ingested_at == "2026-07-25T00:00:00+00:00"


def test_collector_preserves_distinct_observation_and_ingestion_clocks():
    event = _mission_event()
    observation = EvidenceCollector().collect(event)
    assert observation.observed_at == "2026-07-25T10:00:00+00:00"
    assert observation.ingested_at == "2026-07-25T10:00:05+00:00"
    assert observation.observed_at != observation.ingested_at


def test_assembler_builds_immutable_record():
    observation = EvidenceCollector().collect(_mission_event())
    record = EvidenceAssembler().assemble(observation, evidence_id="ev-test")
    assert isinstance(record, EvidenceRecord)
    assert record.evidence_id == "ev-test"
    assert record.authority == AUTHORITY_EVIDENCE_PLATFORM
    assert record.quality.result == QUALITY_PASS
    assert record.quality.runtime_a_ref_present is True
    with pytest.raises(FrozenInstanceError):
        record.evidence_id = "mutated"  # type: ignore[misc]
    with pytest.raises(TypeError):
        record.payload_summary["x"] = 1  # type: ignore[index]


def test_factory_determinism():
    event = _mission_event()
    factory = EvidenceFactory()
    first = factory.create(event)
    second = factory.create(event)
    assert first.serialize() == second.serialize()
    assert first.evidence_id == second.evidence_id
    assert first.evidence_id.startswith("ev-")


def test_factory_preserves_timestamps():
    event = _mission_event()
    record = EvidenceFactory().create(event)
    assert record.observed_at == "2026-07-25T10:00:00+00:00"
    assert record.ingested_at == "2026-07-25T10:00:05+00:00"
    assert record.event_type == "mission_completed"
    assert record.evidence_class == "FACT_EVENT"
    assert "runtime_a" in record.provenance
    assert record.engine_version == "e1.0"


def test_validator_rejects_cross_student_refs():
    event = ObservedEvent(
        student_id="1",
        observed_at="2026-07-25T00:00:00+00:00",
        source_refs=(
            ObservationRef(
                ref_kind="runtime_a",
                entity_kind="Mission",
                entity_id="m-1",
                student_id="2",
            ),
        ),
    )
    with pytest.raises(EvidenceValidationError, match="CROSS_STUDENT"):
        EvidenceCollector().collect(event)


def test_validator_rejects_secret_payload_keys():
    event = ObservedEvent(
        student_id="1",
        payload_summary={"password": "secret"},
    )
    with pytest.raises(EvidenceValidationError, match="forbidden payload"):
        EvidenceValidator().validate_observed_event(event)


def test_empty_observation_is_unavailable_honest():
    context = EvidenceContext(student_id="9", as_of="2026-07-25T00:00:00+00:00")
    record = EvidenceFactory().create_from_context(context)
    assert record.availability == "unavailable"
    assert record.quality.result == QUALITY_INELIGIBLE
    assert "empty_observation" in record.limitations


def test_collection_telemetry_emitted():
    events = EventRegistry()
    factory = EvidenceFactory(events=events)
    record = factory.create(_mission_event())
    types = [e.event_type for e in events.published()]
    assert EVIDENCE_COLLECTION_REQUESTED in types
    assert EVIDENCE_COLLECTION_COMPLETED in types
    assert record.evidence_id


def test_flag_off_leaves_experience_unchanged():
    flags = resolve_v2_feature_flags(environ={})
    composition, _ = build_production_experience(flags=flags)
    assert composition.evidence_platform is None
