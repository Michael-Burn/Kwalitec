"""Matrix tests for Learning Orchestrator readiness and isolation."""

from __future__ import annotations

import pytest

from app.application.learning_orchestrator.policies.orchestration_policy import (
    PORT_NAMES,
    OrchestrationPolicy,
)
from app.application.learning_orchestrator.policies.pipeline_policy import (
    PipelinePolicy,
)
from tests.application.learning_orchestrator.helpers import (
    EVENT_TYPES,
    FakeAdaptive,
    FakeAnalytics,
    FakeEvidence,
    FakeMission,
    FakeTwin,
    make_orchestrator,
    make_request,
    outcomes,
)

FAIL_PORTS = {
    "evidence": ("evidence", FakeEvidence),
    "twin": ("twin", FakeTwin),
    "adaptive_learning": ("adaptive_learning", FakeAdaptive),
    "mission": ("mission", FakeMission),
    "analytics": ("analytics", FakeAnalytics),
}

STAGE_FOR_PORT = {
    "evidence": "evidence",
    "twin": "twin",
    "adaptive_learning": "decision",
    "mission": "mission",
    "analytics": "analytics",
}


@pytest.mark.parametrize("event_type", EVENT_TYPES)
@pytest.mark.parametrize("port_name", list(PORT_NAMES))
def test_event_readiness_requires_each_port(event_type, port_name):
    required = OrchestrationPolicy.required_ports(event_type)
    registered = set(PORT_NAMES) - {port_name}
    ready = OrchestrationPolicy.event_ready(
        event_type, registered=registered
    )
    if port_name in required:
        assert ready is False
    else:
        assert ready is True


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_event_ready_with_full_registration(event_type):
    assert OrchestrationPolicy.event_ready(
        event_type, registered=set(PORT_NAMES)
    )


@pytest.mark.parametrize("event_type", EVENT_TYPES)
@pytest.mark.parametrize("fail_port", list(FAIL_PORTS))
def test_isolated_failure_per_port(event_type, fail_port):
    if fail_port == "mission" and event_type == "manual_confidence_update":
        pytest.skip("manual confidence does not run mission stage")
    kw_name, cls = FAIL_PORTS[fail_port]
    kwargs = {
        kw_name: cls(raise_error=RuntimeError(f"{fail_port} down")),
        "pipeline_policy": PipelinePolicy.isolated(),
    }
    orch = make_orchestrator(**kwargs)
    response = orch.orchestrate(make_request(event_type=event_type))
    stage = STAGE_FOR_PORT[fail_port]
    assert outcomes(response)[stage] == "failure"
    assert response.state in {"partial", "failed"}


@pytest.mark.parametrize("event_type", EVENT_TYPES)
@pytest.mark.parametrize("fail_port", list(FAIL_PORTS))
def test_fail_fast_per_port(event_type, fail_port):
    if fail_port == "mission" and event_type == "manual_confidence_update":
        pytest.skip("manual confidence does not run mission stage")
    kw_name, cls = FAIL_PORTS[fail_port]
    kwargs = {
        kw_name: cls(raise_error=RuntimeError(f"{fail_port} down")),
        "pipeline_policy": PipelinePolicy.fail_fast(),
    }
    orch = make_orchestrator(**kwargs)
    response = orch.orchestrate(make_request(event_type=event_type))
    stage = STAGE_FOR_PORT[fail_port]
    o = outcomes(response)
    assert o[stage] == "failure"
    # Later stages in the response should be skipped when fail-fast
    stage_order = [s.stage for s in response.pipeline_snapshots]
    idx = stage_order.index(stage)
    for later in stage_order[idx + 1 :]:
        assert o[later] == "skipped"


@pytest.mark.parametrize("event_type", EVENT_TYPES)
@pytest.mark.parametrize("unavailable_port", list(FAIL_PORTS))
def test_unavailable_port_isolated(event_type, unavailable_port):
    if (
        unavailable_port == "mission"
        and event_type == "manual_confidence_update"
    ):
        pytest.skip("manual confidence does not run mission stage")
    kw_name, cls = FAIL_PORTS[unavailable_port]
    kwargs = {
        kw_name: cls(available=False),
        "pipeline_policy": PipelinePolicy.isolated(),
    }
    orch = make_orchestrator(**kwargs)
    response = orch.orchestrate(make_request(event_type=event_type))
    stage = STAGE_FOR_PORT[unavailable_port]
    assert outcomes(response)[stage] == "failure"


@pytest.mark.parametrize("event_type", EVENT_TYPES)
@pytest.mark.parametrize(
    "policy_factory",
    [PipelinePolicy.isolated, PipelinePolicy.fail_fast, PipelinePolicy.sequential],
)
def test_policy_variants_complete(event_type, policy_factory):
    orch = make_orchestrator(pipeline_policy=policy_factory())
    response = orch.orchestrate(make_request(event_type=event_type))
    assert response.state == "completed"
    assert response.success is True


@pytest.mark.parametrize("event_type", sorted(EVENT_TYPES))
@pytest.mark.parametrize("n", range(5))
def test_idempotent_repeated_orchestration(event_type, n):
    orch = make_orchestrator()
    response = orch.orchestrate(
        make_request(event_type=event_type, event_id=f"evt-{n}")
    )
    assert response.success is True
    assert response.event_id == f"evt-{n}"
