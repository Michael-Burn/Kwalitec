"""Integration tests — Adaptive Observational Traceability (MS-003 A5).

Verifies DecisionTrace creation on shadow / cutover paths, lineage
reconstruction, correlation consistency, Runtime A read-only behaviour,
and unchanged recommendation behaviour when Authority is OFF.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

import app.infrastructure.adapters.adaptive_engine as adaptive_engine_pkg
from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.adaptive_engine import (
    AUTHORITY_ADAPTIVE_DELIVERED,
    AUTHORITY_ADAPTIVE_ENGINE,
    AUTHORITY_SHADOW_ONLY,
    AdaptiveEngineExecutor,
    AdaptiveInputAssembler,
    ExplainabilityGate,
    TraceabilityService,
    build_traceability_service,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.events.types import (
    ADAPTIVE_TRACE_CREATED,
    ADAPTIVE_TRACE_RECONSTRUCTED,
)
from app.services.recommendation_service import RecommendationService
from tests.conftest import (
    _make_curriculum,
    _make_mission,
    _make_study_attempt,
    _make_study_plan,
    _make_subject,
    _make_topic_progress,
    _make_user,
)

ADAPTER_ROOT = Path(adaptive_engine_pkg.__file__).resolve().parent
TRACE_MODULES = (
    ADAPTER_ROOT / "traceability.py",
    ADAPTER_ROOT / "trace_telemetry.py",
    ADAPTER_ROOT / "shadow.py",
    ADAPTER_ROOT / "port_cutover.py",
)


@pytest.fixture
def learner(app, ctx):
    user = _make_user()
    subject = _make_subject(user.id)
    curriculum, topics = _make_curriculum()
    plan = _make_study_plan(user.id)
    plan.curriculum_id = curriculum.id
    from app.extensions import db

    db.session.commit()
    mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)
    attempt = _make_study_attempt(user.id, topics[0].id, mission.id)
    progress = _make_topic_progress(user.id, topics[0].id)
    return {
        "user": user,
        "subject": subject,
        "curriculum": curriculum,
        "topics": topics,
        "plan": plan,
        "mission": mission,
        "attempt": attempt,
        "progress": progress,
    }


def _shadow_flags(**extra: str) -> dict[str, str]:
    env = {
        "KWALITEC_ADAPTIVE_ENGINE": "1",
        "KWALITEC_ADAPTIVE_SHADOW": "1",
        "KWALITEC_RECOMMENDATION_BRIDGE": "1",
    }
    env.update(extra)
    return env


def _cutover_flags(**extra: str) -> dict[str, str]:
    return _shadow_flags(KWALITEC_ADAPTIVE_AUTHORITY="1", **extra)


def test_shadow_execution_produces_complete_decision_trace(learner):
    flags = resolve_v2_feature_flags(environ=_shadow_flags())
    composition, _ = build_production_experience(flags=flags)
    assert composition.adaptive_shadow is not None
    assert composition.adaptive_traceability is not None

    sid = str(learner["user"].id)
    result = composition.adaptive_shadow.execute_shadow(sid)
    assert result.ok is True
    assert result.value is not None

    trace = composition.adaptive_shadow.last_trace
    assert trace is not None
    assert trace.decision_id == result.value.decision_id
    assert trace.correlation_id
    assert trace.engine_version
    assert trace.runtime_a_snapshot_id.startswith("snap-")
    assert trace.input_bundle_ref.startswith("input-")
    assert trace.output_bundle_ref.startswith("output-")
    assert trace.authority_status == AUTHORITY_SHADOW_ONLY
    assert trace.executed_at
    assert composition.adaptive_traceability.get_trace(trace.decision_id) is trace

    types = [e.event_type for e in composition.events.published()]
    assert ADAPTIVE_TRACE_CREATED in types


def test_lineage_reconstruction_after_shadow(learner):
    flags = resolve_v2_feature_flags(environ=_shadow_flags())
    composition, _ = build_production_experience(flags=flags)
    sid = str(learner["user"].id)
    result = composition.adaptive_shadow.execute_shadow(sid)
    decision_id = result.value.decision_id

    lineage_a = composition.adaptive_traceability.reconstruct_lineage(decision_id)
    lineage_b = composition.adaptive_traceability.reconstruct_lineage(decision_id)
    assert lineage_a is not None
    assert lineage_a.serialize() == lineage_b.serialize()
    assert lineage_a.routing_decision == "shadow_only"
    assert lineage_a.delivery_status == "shadow_only"

    types = [e.event_type for e in composition.events.published()]
    assert ADAPTIVE_TRACE_RECONSTRUCTED in types


def test_correlation_consistency_on_shadow_lifecycle(learner):
    flags = resolve_v2_feature_flags(environ=_shadow_flags())
    composition, _ = build_production_experience(flags=flags)
    sid = str(learner["user"].id)
    composition.adaptive_shadow.execute_shadow(sid)
    trace = composition.adaptive_shadow.last_trace
    assert trace is not None

    related = [
        e
        for e in composition.events.published()
        if e.correlation_id == trace.correlation_id
    ]
    assert related
    assert all(e.correlation_id == trace.correlation_id for e in related)
    assert composition.adaptive_traceability.traces_for_correlation(
        trace.correlation_id
    )[0].decision_id == trace.decision_id


def test_cutover_success_records_delivered_trace(learner):
    flags = resolve_v2_feature_flags(environ=_cutover_flags())
    composition, _ = build_production_experience(flags=flags)
    assert composition.adaptive_port_router is not None

    sid = str(learner["user"].id)
    projected = composition.adaptive.get_todays_recommendation(sid)
    assert projected is not None
    assert projected["authority"] == AUTHORITY_ADAPTIVE_ENGINE

    trace = composition.adaptive_port_router.last_trace
    assert trace is not None
    assert trace.decision_id == projected.get("decision_id")
    assert trace.authority_status == AUTHORITY_ADAPTIVE_DELIVERED
    assert trace.lineage.delivery_status == "delivered"
    assert trace.lineage.routing_decision == "authoritative"


def test_authority_off_recommendation_behaviour_unchanged(learner):
    """Traceability must not change Experience recommendation when Authority OFF."""
    flags = resolve_v2_feature_flags(environ=_shadow_flags())
    composition, _ = build_production_experience(flags=flags)
    assert composition.adaptive_port_router is None
    assert composition.adaptive_traceability is not None

    sid = str(learner["user"].id)
    # Shadow still produces traces observationally.
    shadow = composition.adaptive_shadow.execute_shadow(sid)
    assert shadow.ok is True
    assert composition.adaptive_shadow.last_trace is not None

    # Experience still uses RecommendationService / bridge path (not adaptive).
    result = composition.adaptive.get_todays_recommendation(sid)
    assert result is not None
    assert result.get("authority") != AUTHORITY_ADAPTIVE_ENGINE


def test_recommendation_service_stable_with_traceability(learner):
    flags = resolve_v2_feature_flags(environ=_shadow_flags())
    composition, _ = build_production_experience(flags=flags)
    sid = int(learner["user"].id)

    baseline = RecommendationService.generate_today_recommendation(sid)
    composition.adaptive_shadow.execute_shadow(str(sid))
    after = RecommendationService.generate_today_recommendation(sid)

    assert baseline is not None and after is not None
    assert baseline.get("title") == after.get("title")
    assert baseline.get("category") == after.get("category")
    assert baseline.get("priority") == after.get("priority")


def test_runtime_a_read_only_in_trace_modules():
    forbidden = {
        "db.session.add",
        "db.session.commit",
        "db.session.delete",
        "db.session.flush",
        "session.add",
        "session.commit",
        "session.delete",
    }
    for path in TRACE_MODULES:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        src = path.read_text(encoding="utf-8")
        for name in forbidden:
            assert name not in src, f"{path.name} must not call {name}"
        # Also reject common write service imports used for educational mutation.
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                assert "planning_service" not in (node.module or "")
                assert "adaptive_learning_service" not in (node.module or "")


def test_assembler_and_executor_pipeline_still_deterministic(learner):
    assembler = AdaptiveInputAssembler()
    executor = AdaptiveEngineExecutor()
    gate = ExplainabilityGate(enabled=True)
    svc = build_traceability_service(enabled=True)
    assert isinstance(svc, TraceabilityService)

    sid = str(learner["user"].id)
    bundle_a = assembler.assemble(sid, as_of="2026-07-25")
    bundle_b = assembler.assemble(sid, as_of="2026-07-25")
    assert bundle_a.serialize() == bundle_b.serialize()

    out_a = executor.evaluate(bundle_a)
    out_b = executor.evaluate(bundle_b)
    assert out_a.serialize() == out_b.serialize()

    gate_a = gate.validate(out_a, student_id=sid)
    gate_b = gate.validate(out_b, student_id=sid)
    assert gate_a.passed == gate_b.passed

    t1 = svc.record_decision(
        student_id=sid,
        inputs=bundle_a,
        output=out_a,
        gate_result=gate_a,
        correlation_id="det-1",
        executed_at="2026-07-25T00:00:00+00:00",
    )
    t2 = svc.record_decision(
        student_id=sid,
        inputs=bundle_b,
        output=out_b,
        gate_result=gate_b,
        correlation_id="det-2",
        executed_at="2026-07-25T00:00:01+00:00",
    )
    assert t1 is not None and t2 is not None
    assert t1.decision_id == t2.decision_id
    assert t1.runtime_a_snapshot_id == t2.runtime_a_snapshot_id
    assert t1.lineage.serialize() == t2.lineage.serialize()
