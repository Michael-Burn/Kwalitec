"""Integration tests — Learning Evidence Platform E2 Experiment Framework."""

from __future__ import annotations

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.evidence_platform import (
    AVAILABILITY_AVAILABLE,
    QUALITY_PASS,
    EvidenceFactory,
    EvidencePlatformAdapter,
    ExperimentArm,
    ExperimentDefinition,
    ExperimentFramework,
    ExperimentObservation,
    ObservedEvent,
    build_evidence_platform_adapter,
    build_experiment_framework,
    serialize_canonical,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import EXPERIMENT_ASSIGNMENT_EVENT_TYPES


def _full_event(**overrides) -> ObservedEvent:
    base = {
        "student_id": "42",
        "event_type": "mission_completed",
        "observed_at": "2026-07-25T12:00:00+00:00",
        "ingested_at": "2026-07-25T12:00:01+00:00",
        "as_of": "2026-07-25T12:00:00+00:00",
        "claim_boundary": "organisation",
        "evidence_class": "FACT_EVENT",
        "runtime_a": {
            "mission": {"mission_id": "mission-42", "topic_code": "T1"},
            "evidence_id": "ra-1",
        },
        "experience": {"delivery_id": "exp-del-1"},
        "strategy": {"intervention_id": "strat-1"},
        "adaptive": {"decision_id": "adapt-1"},
        "twin": {"twin_id": "twin-42"},
        "payload_summary": {"outcome": "completed"},
    }
    base.update(overrides)
    return ObservedEvent(**base)


def _definition() -> ExperimentDefinition:
    return ExperimentDefinition(
        experiment_id="exp-e2-integration",
        definition_version="e2.0",
        title="E2 integration",
        arms=(
            ExperimentArm(
                arm_id="control",
                label="control",
                exposure="shadow_only",
            ),
            ExperimentArm(
                arm_id="treatment_a",
                label="treatment_a",
                exposure="shadow_only",
            ),
        ),
        assignment_mechanism="hash",
        pre_registration="pre-reg-e2-integration",
        status="running",
        primary_outcomes=("organisation_completion",),
    )


def test_collect_then_assign_pipeline():
    events = EventRegistry()
    framework = ExperimentFramework(events=events)
    framework.register_definition(_definition())
    adapter = EvidencePlatformAdapter(
        factory=EvidenceFactory(events=events),
        experiment_framework=framework,
    )
    event = _full_event()
    original_event = event.serialize()

    collected = adapter.assemble_record("42", event=event)
    assert collected.ok is True
    record = collected.value
    assert record is not None
    original_record = record.serialize()

    assigned = adapter.assign_to_experiment(record, experiment_id="exp-e2-integration")
    assert assigned.ok is True
    observation = assigned.value
    assert isinstance(observation, ExperimentObservation)
    assert observation.experiment_id == "exp-e2-integration"
    assert observation.evidence_id == record.evidence_id
    assert observation.student_id == "42"
    assert observation.arm_id in {"control", "treatment_a"}
    assert observation.assignment_rationale
    assert record.availability == AVAILABILITY_AVAILABLE
    assert record.quality.result == QUALITY_PASS

    # Evidence immutability + input freeze.
    assert event.serialize() == original_event
    assert record.serialize() == original_record

    emitted = {e.event_type for e in events.published()}
    assert EXPERIMENT_ASSIGNMENT_EVENT_TYPES[0] in emitted
    assert EXPERIMENT_ASSIGNMENT_EVENT_TYPES[1] in emitted


def test_determinism_across_framework_and_adapter():
    definition = _definition()
    record = EvidenceFactory().create(_full_event())
    via_framework = ExperimentFramework().assign(record, definition)
    adapter = EvidencePlatformAdapter(
        experiment_framework=ExperimentFramework(),
    )
    via_adapter = adapter.assign_to_experiment(record, definition)
    assert via_adapter.ok is True
    assert via_adapter.value is not None
    assert via_framework.serialize() == via_adapter.value.serialize()
    assert via_framework.observation_id == via_adapter.value.observation_id


def test_identical_inputs_identical_observation_every_execution():
    definition = _definition()
    record = EvidenceFactory().create(_full_event())
    framework = ExperimentFramework()
    observations = [framework.assign(record, definition) for _ in range(5)]
    serialised = {obs.serialize() for obs in observations}
    assert len(serialised) == 1
    assert observations[0].observation_id.startswith("obs-")


def test_serialization_round_trip_stable():
    observation = ExperimentFramework().assign(
        EvidenceFactory().create(_full_event()),
        _definition(),
    )
    payload = observation.to_canonical_dict()
    assert serialize_canonical(payload) == observation.serialize()
    assert payload["evidence_ref"]["evidence_id"] == observation.evidence_id


def test_flag_off_no_framework_no_experience_change():
    flags = resolve_v2_feature_flags(environ={})
    composition, _ = build_production_experience(flags=flags)
    assert composition.evidence_platform is None
    assert build_experiment_framework(enabled=False) is None
    assert build_evidence_platform_adapter(enabled=False) is None


def test_flag_on_composition_assignment_isolated():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EVIDENCE_PLATFORM": "1"}
    )
    composition, _ = build_production_experience(flags=flags)
    adapter = composition.evidence_platform
    assert isinstance(adapter, EvidencePlatformAdapter)
    assert adapter.experiment_framework is not None
    adapter.experiment_framework.register_definition(_definition())
    record = adapter.collect_event(_full_event())
    result = adapter.assign_to_experiment(
        record, experiment_id="exp-e2-integration"
    )
    assert result.ok is True
    assert isinstance(result.value, ExperimentObservation)
    assert result.value.authority == "evidence_platform"
