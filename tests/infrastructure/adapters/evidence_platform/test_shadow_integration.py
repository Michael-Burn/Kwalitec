"""Integration tests — Evidence Shadow Validation (MS-006 E5).

Verifies deterministic readiness reports, subsystem coverage, health
monitoring, rollback isolation, feature-flag isolation, and no Runtime A /
Twin / Adaptive / Strategy / Experience behavioural change.
"""

from __future__ import annotations

import ast
from pathlib import Path

import app.infrastructure.adapters.evidence_platform as evidence_pkg
from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.evidence_platform import (
    QUALITY_PASS,
    AnalyticsEngine,
    EvidenceFactory,
    EvidencePlatformState,
    EvidenceProjector,
    EvidenceShadowValidator,
    ExperimentArm,
    ExperimentDefinition,
    ExperimentFramework,
    ObservedEvent,
    PolicyDefinition,
    PolicyEvaluationFactory,
    build_evidence_platform_adapter,
    build_evidence_shadow_ops_dashboard,
    build_evidence_shadow_validator,
    verify_evidence_shadow_rollback,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    EVIDENCE_SHADOW_COMPLETED,
    EVIDENCE_SHADOW_HEALTH,
    EVIDENCE_SHADOW_LATENCY,
    EVIDENCE_SHADOW_READINESS,
    EVIDENCE_SHADOW_REQUESTED,
    EVIDENCE_SHADOW_ROLLBACK_VERIFIED,
    EVIDENCE_SHADOW_STABILITY,
)

ADAPTER_ROOT = Path(evidence_pkg.__file__).resolve().parent
AS_OF = "2026-07-25T12:00:00+00:00"
SHADOW_MODULES = (
    "shadow.py",
    "shadow_determinism.py",
    "shadow_health.py",
    "shadow_readiness.py",
    "shadow_rollback.py",
    "shadow_telemetry.py",
)


def _mission_event(*, student_id: str = "42", **overrides) -> ObservedEvent:
    base = {
        "student_id": student_id,
        "event_type": "mission_completed",
        "observed_at": "2026-07-25T10:00:00+00:00",
        "ingested_at": "2026-07-25T10:00:05+00:00",
        "as_of": AS_OF,
        "claim_boundary": "organisation",
        "evidence_class": "FACT_EVENT",
        "runtime_a": {
            "mission": {"mission_id": f"m-{student_id}", "status": "completed"},
            "evidence_id": f"ra-ev-{student_id}",
        },
        "payload_summary": {"mission_status": "completed"},
    }
    base.update(overrides)
    return ObservedEvent(**base)


def _definition_exp() -> ExperimentDefinition:
    return ExperimentDefinition(
        experiment_id="exp-e5-int",
        definition_version="e2.0",
        title="E5 integration",
        arms=(
            ExperimentArm(
                arm_id="control",
                label="control",
                exposure="shadow_only",
            ),
            ExperimentArm(
                arm_id="treatment",
                label="treatment",
                exposure="shadow_only",
            ),
        ),
        assignment_mechanism="hash",
        pre_registration="pre-reg-e5-int",
        status="running",
        primary_outcomes=("organisation_completion",),
        policy_id="pol-e5-int",
    )


def _policy() -> PolicyDefinition:
    return PolicyDefinition(
        policy_id="pol-e5-int",
        policy_version="1.0.0",
        definition_version="e3.0",
        title="E5 integration policy",
        intent="Observe shadow stability",
        owner_layer="adaptive",
        claim_boundary_intent="organisation",
        principles=("ep.inspectability.why_tonight",),
        sp_mapping=("SP8",),
        upstream_controls={"ENABLE_ADAPTIVE_SHADOW": True},
        experiment_ids=("exp-e5-int",),
        evaluation_kind="shadow_descriptive",
        evaluation_eligibility={"min_observations": 3, "min_students": 2},
        educational_rationale={
            "organisation_vs_learning_note": (
                "Organisation outcomes remain separate from learning depth."
            ),
        },
        statistical_plan={"design": "descriptive_soak"},
        status="active",
        spec_ref="adr-ms006-pol-e5-int",
        limitations=("shadow_only",),
    )


def _platform_state() -> EvidencePlatformState:
    framework = ExperimentFramework()
    framework.register_definition(_definition_exp())
    factory = EvidenceFactory()
    evidence_records = []
    observations = []
    for index in range(4):
        student_id = str(60 + index)
        record = factory.create(_mission_event(student_id=student_id))
        assert record.quality.result == QUALITY_PASS
        evidence_records.append(record)
        observations.append(framework.assign(record, experiment_id="exp-e5-int"))
    eval_factory = PolicyEvaluationFactory()
    eval_factory.register_definition(_policy())
    evaluation = eval_factory.evaluate(
        observations, policy_id="pol-e5-int", created_at=AS_OF
    )
    analytics = AnalyticsEngine().aggregate(
        evaluations=(evaluation,),
        observations=tuple(observations),
        evidence_records=tuple(evidence_records),
        as_of=AS_OF,
    )
    projection = EvidenceProjector().project(analytics, as_of=AS_OF)
    return EvidencePlatformState(
        evidence_records=tuple(evidence_records),
        observations=tuple(observations),
        evaluations=(evaluation,),
        analytics_summaries=(analytics,),
        projections=(projection,),
    )


def _build_validator(*, events: EventRegistry | None = None) -> EvidenceShadowValidator:
    adapter = build_evidence_platform_adapter(enabled=True)
    validator = build_evidence_shadow_validator(
        enabled=True,
        adapter=adapter,
        events=events or EventRegistry(),
    )
    assert validator is not None
    return validator


def test_end_to_end_shadow_validation_produces_readiness_report():
    events = EventRegistry()
    validator = _build_validator(events=events)
    observation = validator.validate_shadow(state=_platform_state(), as_of=AS_OF)
    assert observation.ok is True
    assert observation.determinism_ok is True
    assert observation.report is not None
    assert observation.report.deploys_policy is False
    assert observation.report.influences_student is False
    assert len(observation.report.coverage.subsystems_covered) == 5
    types = {event.event_type for event in events.published()}
    assert {
        EVIDENCE_SHADOW_REQUESTED,
        EVIDENCE_SHADOW_STABILITY,
        EVIDENCE_SHADOW_COMPLETED,
        EVIDENCE_SHADOW_LATENCY,
        EVIDENCE_SHADOW_HEALTH,
        EVIDENCE_SHADOW_READINESS,
    }.issubset(types)


def test_batch_replay_is_deterministic():
    validator = _build_validator()
    state = _platform_state()
    results = validator.validate_shadow_batch(
        (state, state), as_of=AS_OF, iterations=3
    )
    assert len(results) == 6
    serializations = {item.report.serialize() for item in results if item.report}
    assert len(serializations) == 1
    assert all(item.ok for item in results)


def test_flag_off_leaves_experience_and_upstream_unchanged():
    flags = resolve_v2_feature_flags(environ={})
    composition, service = build_production_experience(flags=flags)
    assert composition.evidence_platform is None
    assert composition.evidence_shadow is None
    assert composition.twin is not None
    assert service is not None
    assert flags.ENABLE_EVIDENCE_PLATFORM is False
    assert flags.ENABLE_DIGITAL_TWIN is False
    assert flags.ENABLE_ADAPTIVE_ENGINE is False
    assert flags.ENABLE_STRATEGY_ENGINE is False


def test_flag_on_wires_shadow_without_authority_cutover():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EVIDENCE_PLATFORM": "1"}
    )
    composition, service = build_production_experience(flags=flags)
    assert composition.evidence_platform is not None
    assert composition.evidence_shadow is not None
    assert composition.evidence_shadow.is_enabled() is True
    assert service is not None
    dashboard = build_evidence_shadow_ops_dashboard(composition.evidence_shadow)
    assert dashboard["evidence_shadow_validation"]["deploys_policy"] is False


def test_rollback_drill_emits_verified_event():
    events = EventRegistry()
    result = verify_evidence_shadow_rollback(events=events)
    assert result.ok is True
    assert any(
        event.event_type == EVIDENCE_SHADOW_ROLLBACK_VERIFIED
        for event in events.published()
    )


def test_shadow_modules_have_no_educational_write_calls():
    forbidden_snippets = (
        "db.session.commit",
        "db.session.add",
        "persist(",
        "promote_policy",
        "deploy_policy",
        "cutover",
        "ENABLE_ADAPTIVE_AUTHORITY=True",
    )
    for module_name in SHADOW_MODULES:
        source = (ADAPTER_ROOT / module_name).read_text(encoding="utf-8")
        tree = ast.parse(source)
        text = ast.unparse(tree)
        for snippet in forbidden_snippets:
            assert snippet not in text, f"{module_name} contains {snippet}"


def test_shadow_package_does_not_import_flask_or_experience_routes():
    for module_name in SHADOW_MODULES:
        source = (ADAPTER_ROOT / module_name).read_text(encoding="utf-8")
        assert "from flask" not in source
        assert "import flask" not in source
        assert "app.auth" not in source
        assert "app.mission" not in source
        assert "app.dashboard" not in source


def test_health_accumulates_across_shadow_window():
    validator = _build_validator()
    state = _platform_state()
    validator.validate_shadow_batch((state,), as_of=AS_OF, iterations=4)
    snapshot = validator.health_snapshot()
    assert snapshot.executions == 4
    assert snapshot.validation_success_rate == 1.0
    assert snapshot.determinism_success_rate == 1.0
    assert snapshot.evidence_coverage_count == 4
    assert snapshot.projection_coverage_count == 4
