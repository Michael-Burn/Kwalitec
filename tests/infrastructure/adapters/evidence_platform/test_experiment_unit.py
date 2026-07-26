"""Unit tests — Learning Evidence Platform E2 Experiment Framework."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.evidence_platform import (
    ASSIGNMENT_MECHANISM_HASH,
    ASSIGNMENT_MECHANISM_MANUAL_ALLOWLIST,
    AUTHORITY_EVIDENCE_PLATFORM,
    QUALITY_PASS,
    EvidenceFactory,
    EvidencePlatformAdapter,
    EvidenceQuality,
    EvidenceRecord,
    ExperimentArm,
    ExperimentAssigner,
    ExperimentDefinition,
    ExperimentDefinitionRegistry,
    ExperimentFramework,
    ExperimentObservation,
    ExperimentValidationError,
    ExperimentValidator,
    ObservedEvent,
    build_evidence_platform_adapter,
    build_experiment_assigner,
    build_experiment_definition_registry,
    build_experiment_framework,
    build_experiment_validator,
    serialize_canonical,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    EXPERIMENT_ASSIGNMENT_COMPLETED,
    EXPERIMENT_ASSIGNMENT_REQUESTED,
)


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
        "payload_summary": {"mission_status": "completed"},
    }
    base.update(overrides)
    return ObservedEvent(**base)


def _validated_evidence(**overrides) -> EvidenceRecord:
    record = EvidenceFactory().create(_mission_event(**overrides))
    assert record.quality.result == QUALITY_PASS
    return record


def _definition(**overrides) -> ExperimentDefinition:
    base = {
        "experiment_id": "exp-shadow-parity",
        "definition_version": "e2.0",
        "title": "Shadow parity",
        "hypothesis": "Observational metrics remain stable",
        "arms": (
            ExperimentArm(
                arm_id="control",
                label="control",
                exposure="shadow_only",
            ),
            ExperimentArm(
                arm_id="treatment",
                label="treatment",
                exposure="shadow_only",
                upstream_flag_snapshot={"ENABLE_STRATEGY_SHADOW": True},
            ),
        ),
        "assignment_mechanism": ASSIGNMENT_MECHANISM_HASH,
        "primary_outcomes": ("completion_rate",),
        "pre_registration": "pre-reg-exp-shadow-parity-v1",
        "status": "registered",
    }
    base.update(overrides)
    return ExperimentDefinition(**base)


def test_build_helpers_respect_feature_flag():
    assert build_experiment_framework(enabled=False) is None
    assert build_experiment_assigner(enabled=False) is None
    assert build_experiment_definition_registry(enabled=False) is None
    assert isinstance(build_experiment_validator(), ExperimentValidator)
    assert isinstance(build_experiment_framework(enabled=True), ExperimentFramework)


def test_adapter_wires_framework_when_enabled():
    adapter = build_evidence_platform_adapter(enabled=True)
    assert adapter is not None
    assert isinstance(adapter.experiment_framework, ExperimentFramework)


def test_composition_wires_framework_only_when_flag_on():
    flags_off = resolve_v2_feature_flags(environ={})
    composition_off, _ = build_production_experience(flags=flags_off)
    assert composition_off.evidence_platform is None

    flags_on = resolve_v2_feature_flags(
        environ={"KWALITEC_EVIDENCE_PLATFORM": "1"}
    )
    composition_on, _ = build_production_experience(flags=flags_on)
    assert isinstance(composition_on.evidence_platform, EvidencePlatformAdapter)
    assert isinstance(
        composition_on.evidence_platform.experiment_framework,
        ExperimentFramework,
    )


def test_registry_registers_and_looks_up():
    registry = ExperimentDefinitionRegistry()
    definition = _definition()
    registry.register(definition)
    assert registry.contains("exp-shadow-parity")
    assert registry.require("exp-shadow-parity").experiment_id == "exp-shadow-parity"
    assert registry.list_ids() == ("exp-shadow-parity",)
    with pytest.raises(ExperimentValidationError, match="already registered"):
        registry.register(definition)


def test_validator_rejects_draft_for_assignment():
    validator = ExperimentValidator()
    draft = _definition(status="draft")
    with pytest.raises(ExperimentValidationError, match="status must be"):
        validator.validate_definition(draft, require_assignable=True)


def test_validator_rejects_duplicate_arms():
    with pytest.raises(ExperimentValidationError, match="duplicate arm_id"):
        ExperimentValidator().validate_definition(
            _definition(
                arms=(
                    ExperimentArm(arm_id="control", label="a", exposure="shadow_only"),
                    ExperimentArm(arm_id="control", label="b", exposure="shadow_only"),
                )
            )
        )


def test_assigner_determinism():
    record = _validated_evidence()
    definition = _definition()
    assigner = ExperimentAssigner()
    first = assigner.assign(record, definition)
    second = assigner.assign(record, definition)
    assert isinstance(first, ExperimentObservation)
    assert first.serialize() == second.serialize()
    assert first.observation_id == second.observation_id
    assert first.observation_id.startswith("obs-")
    assert first.experiment_id == "exp-shadow-parity"
    assert first.experiment_version == "e2.0"
    assert first.evidence_id == record.evidence_id
    assert first.assignment_mechanism == ASSIGNMENT_MECHANISM_HASH
    assert first.authority == AUTHORITY_EVIDENCE_PLATFORM


def test_assigner_does_not_mutate_evidence():
    record = _validated_evidence()
    original = record.serialize()
    observation = ExperimentAssigner().assign(record, _definition())
    assert record.serialize() == original
    assert observation.evidence_ref["evidence_id"] == record.evidence_id
    with pytest.raises(FrozenInstanceError):
        observation.arm_id = "mutated"  # type: ignore[misc]
    with pytest.raises(TypeError):
        observation.metadata["x"] = 1  # type: ignore[index]


def test_different_students_may_differ_same_definition():
    definition = _definition()
    assigner = ExperimentAssigner()
    a = assigner.assign(_validated_evidence(student_id="1"), definition)
    b = assigner.assign(_validated_evidence(student_id="2"), definition)
    # Same definition; subject key participates in hash — observations differ.
    assert a.student_id != b.student_id
    assert a.serialize() != b.serialize()


def test_manual_allowlist_assignment():
    definition = _definition(
        assignment_mechanism=ASSIGNMENT_MECHANISM_MANUAL_ALLOWLIST,
        eligibility={"arm_allowlist": {"42": "treatment"}},
    )
    observation = ExperimentAssigner().assign(_validated_evidence(), definition)
    assert observation.arm_id == "treatment"
    assert observation.cohort == "treatment"
    assert "allowlist_matched" in observation.assignment_rationale


def test_eligibility_failure():
    definition = _definition(eligibility={"student_ids": ["99"]})
    with pytest.raises(ExperimentValidationError, match="not eligible"):
        ExperimentAssigner().assign(_validated_evidence(), definition)


def test_framework_registry_path_and_telemetry():
    events = EventRegistry()
    framework = ExperimentFramework(events=events)
    framework.register_definition(_definition())
    record = _validated_evidence()
    observation = framework.assign_registered(record, "exp-shadow-parity")
    assert observation.evidence_id == record.evidence_id
    types = [e.event_type for e in events.published()]
    assert EXPERIMENT_ASSIGNMENT_REQUESTED in types
    assert EXPERIMENT_ASSIGNMENT_COMPLETED in types


def test_observation_serialization_stable():
    observation = ExperimentAssigner().assign(_validated_evidence(), _definition())
    payload = observation.to_canonical_dict()
    assert serialize_canonical(payload) == observation.serialize()
    required = {
        "observation_id",
        "experiment_id",
        "experiment_version",
        "arm_id",
        "cohort",
        "evidence_id",
        "evidence_ref",
        "assignment_rationale",
        "metadata",
    }
    assert required.issubset(payload.keys())


def test_quality_gate_eligibility():
    definition = _definition(eligibility={"require_quality_pass": True})
    bad = EvidenceRecord(
        evidence_id="ev-bad",
        student_id="42",
        quality=EvidenceQuality(result="fail", codes=("incomplete",)),
        availability="unavailable",
        unavailable_reason="incomplete",
    )
    with pytest.raises(ExperimentValidationError, match="not eligible"):
        ExperimentAssigner().assign(bad, definition)
