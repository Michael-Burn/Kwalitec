"""Core Learning Orchestrator facade and pipeline execution tests."""

from __future__ import annotations

import pytest

from app.application.learning_orchestrator.exceptions import EventDispatchError
from app.application.learning_orchestrator.policies.pipeline_policy import (
    PipelinePolicy,
)
from app.domain.learning_orchestrator.orchestration_event import (
    OrchestrationEventType,
)
from tests.application.learning_orchestrator.helpers import (
    EVENT_TYPES,
    FakeEvidence,
    FakeTwin,
    make_event,
    make_orchestrator,
    make_request,
    outcomes,
)


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_full_pipeline_succeeds_for_each_event(event_type):
    orch = make_orchestrator()
    response = orch.orchestrate(make_request(event_type=event_type))
    assert response.success is True or response.state == "completed"
    assert response.learner_id == "learner-1"
    assert response.event_type == event_type
    assert response.execution_summary is not None
    assert response.execution_summary.duration_ms >= 0


def test_learning_activity_completed_handler():
    orch = make_orchestrator()
    response = orch.handle_learning_activity_completed(make_request())
    assert response.event_type == (
        OrchestrationEventType.LEARNING_ACTIVITY_COMPLETED.value
    )
    assert "evidence" in response.executed_stages


def test_knowledge_check_handler():
    orch = make_orchestrator()
    response = orch.handle_knowledge_check_completed(make_request())
    assert response.event_type == (
        OrchestrationEventType.KNOWLEDGE_CHECK_COMPLETED.value
    )


def test_reflection_handler():
    orch = make_orchestrator()
    response = orch.handle_reflection_submitted(make_request())
    assert response.event_type == (
        OrchestrationEventType.REFLECTION_SUBMITTED.value
    )


def test_session_completed_handler():
    orch = make_orchestrator()
    response = orch.handle_session_completed(make_request())
    assert response.event_type == (
        OrchestrationEventType.SESSION_COMPLETED.value
    )


def test_mission_completed_handler():
    orch = make_orchestrator()
    response = orch.handle_mission_completed(make_request())
    assert response.event_type == (
        OrchestrationEventType.MISSION_COMPLETED.value
    )


def test_manual_confidence_skips_mission_stage():
    orch = make_orchestrator()
    response = orch.handle_manual_confidence_update(make_request())
    stages = [s.stage for s in response.pipeline_snapshots]
    assert "mission" not in stages
    assert stages == ["evidence", "twin", "decision", "analytics"]


def test_handle_domain_event():
    orch = make_orchestrator()
    response = orch.handle_event(make_event())
    assert response.success is True
    assert response.event_id == "evt-1"


def test_unknown_event_raises():
    orch = make_orchestrator()
    with pytest.raises(EventDispatchError):
        orch.orchestrate(make_request(event_type="not_a_real_event"))


def test_canonical_stage_order():
    log: list[str] = []
    orch = make_orchestrator(call_log=log)
    orch.orchestrate(make_request())
    # First call of each port in order
    firsts = []
    for name in log:
        if name not in firsts:
            firsts.append(name)
    assert firsts == [
        "process_evidence",
        "update_from_evidence",
        "decide",
        "apply_decision",
        "record_execution",
    ]


def test_isolated_failure_continues_pipeline():
    orch = make_orchestrator(
        twin=FakeTwin(raise_error=RuntimeError("twin boom")),
        pipeline_policy=PipelinePolicy.isolated(),
    )
    response = orch.orchestrate(make_request())
    o = outcomes(response)
    assert o["twin"] == "failure"
    assert o["decision"] in {"success", "warning"}
    assert o["mission"] in {"success", "warning"}
    assert o["analytics"] in {"success", "warning"}
    assert response.state == "partial"
    assert response.success is False


def test_fail_fast_stops_pipeline():
    orch = make_orchestrator(
        evidence=FakeEvidence(raise_error=RuntimeError("ev boom")),
        pipeline_policy=PipelinePolicy.fail_fast(),
    )
    response = orch.orchestrate(make_request())
    o = outcomes(response)
    assert o["evidence"] == "failure"
    assert o["twin"] == "skipped"
    assert o["decision"] == "skipped"
    assert o["mission"] == "skipped"
    assert o["analytics"] == "skipped"
    assert response.state == "failed"


def test_port_substitution():
    orch = make_orchestrator()
    replacement = FakeEvidence(payload={"component": "evidence", "alt": True})
    orch.replace_port("evidence", replacement)
    response = orch.orchestrate(make_request())
    assert response.success is True
    assert "process_evidence" in replacement.calls


def test_unbound_ports_report_failures():
    orch = make_orchestrator(include_all=False)
    response = orch.orchestrate(make_request())
    assert response.success is False
    assert response.failed_stages
    assert all(
        s.outcome == "failure" for s in response.pipeline_snapshots
        if s.outcome != "skipped"
    )


def test_health_healthy_when_all_bound():
    orch = make_orchestrator()
    health = orch.health_status()
    assert health["orchestrator_status"] == "healthy"
    assert health["all_events_ready"] is True


def test_health_degraded_when_missing():
    orch = make_orchestrator(include_all=False)
    health = orch.health_status()
    assert health["orchestrator_status"] == "degraded"
    assert health["missing_dependencies"]


def test_diagnostics_report_immutable():
    orch = make_orchestrator()
    orch.orchestrate(make_request())
    report = orch.diagnostics()
    assert report.orchestrator_version == "learning-orchestrator-1"
    assert report.canonical_pipeline == (
        "evidence",
        "twin",
        "decision",
        "mission",
        "analytics",
    )
    with pytest.raises(Exception):
        report.registered_ports = ()  # type: ignore[misc]


def test_execution_summary_observability():
    orch = make_orchestrator()
    response = orch.orchestrate(make_request())
    summary = response.execution_summary
    assert summary is not None
    assert summary.executed_stages
    assert "evidence" in summary.stage_timings_ms
    assert summary.dependency_status
    assert isinstance(summary.pipeline_diagnostics, tuple)


def test_deterministic_same_inputs():
    orch1 = make_orchestrator()
    orch2 = make_orchestrator()
    r1 = orch1.orchestrate(make_request(orchestration_id="same"))
    r2 = orch2.orchestrate(make_request(orchestration_id="same"))
    assert r1.event_type == r2.event_type
    assert r1.state == r2.state
    assert outcomes(r1) == outcomes(r2)
    assert r1.executed_stages == r2.executed_stages
