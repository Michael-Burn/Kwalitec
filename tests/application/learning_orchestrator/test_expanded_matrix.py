"""Expanded combinatorial matrices for Learning Orchestrator."""

from __future__ import annotations

import pytest

from app.application.learning_orchestrator.policies.pipeline_policy import (
    PipelinePolicy,
)
from app.application.learning_orchestrator.policies.retry_policy import (
    RetryPolicy,
)
from tests.application.learning_orchestrator.helpers import (
    EVENT_TYPES,
    STAGES,
    FakeAdaptive,
    FakeAnalytics,
    FakeEvidence,
    FakeMission,
    FakeTwin,
    make_orchestrator,
    make_request,
    outcomes,
)

LEARNERS = ("learner-a", "learner-b", "learner-c", "learner-d")
TOPICS = ("topic-x", "topic-y")
SUBJECTS = ("math", "physics")

PORT_FAIL = {
    "evidence": ("evidence", FakeEvidence),
    "twin": ("twin", FakeTwin),
    "decision": ("adaptive_learning", FakeAdaptive),
    "mission": ("mission", FakeMission),
    "analytics": ("analytics", FakeAnalytics),
}


@pytest.mark.parametrize("learner_id", LEARNERS)
@pytest.mark.parametrize("event_type", EVENT_TYPES)
@pytest.mark.parametrize("topic_id", TOPICS)
def test_success_grid_learner_event_topic(learner_id, event_type, topic_id):
    orch = make_orchestrator()
    response = orch.orchestrate(
        make_request(
            event_type=event_type,
            learner_id=learner_id,
            topic_id=topic_id,
            event_id=f"{learner_id}-{event_type}-{topic_id}",
        )
    )
    assert response.success is True
    assert response.learner_id == learner_id
    assert response.event_type == event_type


@pytest.mark.parametrize("subject_id", SUBJECTS)
@pytest.mark.parametrize("event_type", EVENT_TYPES)
@pytest.mark.parametrize("stage", STAGES)
def test_fail_stage_isolated_grid(subject_id, event_type, stage):
    if stage == "mission" and event_type == "manual_confidence_update":
        pytest.skip("manual confidence does not run mission")
    kw_name, cls = PORT_FAIL[stage]
    orch = make_orchestrator(
        **{
            kw_name: cls(raise_error=RuntimeError("boom")),
            "pipeline_policy": PipelinePolicy.isolated(),
        }
    )
    response = orch.orchestrate(
        make_request(event_type=event_type, subject_id=subject_id)
    )
    assert outcomes(response)[stage] == "failure"
    assert response.success is False


@pytest.mark.parametrize("event_type", EVENT_TYPES)
@pytest.mark.parametrize("max_attempts", [1, 2, 3])
def test_retry_recovers_transient_failure(event_type, max_attempts):
    evidence = FakeEvidence(fail_times=1)
    orch = make_orchestrator(
        evidence=evidence,
        retry_policy=RetryPolicy.technical(max_attempts=max_attempts),
    )
    response = orch.orchestrate(make_request(event_type=event_type))
    if max_attempts >= 2:
        assert outcomes(response)["evidence"] in {"success", "warning"}
        assert evidence.calls.count("process_evidence") == 2
    else:
        assert outcomes(response)["evidence"] == "failure"


@pytest.mark.parametrize("event_type", EVENT_TYPES)
@pytest.mark.parametrize("available", [True, False])
def test_health_reflects_availability(event_type, available):
    del event_type  # matrix lever for volume / readiness coupling
    orch = make_orchestrator(twin=FakeTwin(available=available))
    health = orch.health_status()
    if available:
        assert health["orchestrator_status"] in {"healthy", "degraded"}
        assert not health["unavailable_dependencies"]
    else:
        assert health["orchestrator_status"] == "unhealthy"
        assert "twin" in health["unavailable_dependencies"]


@pytest.mark.parametrize("event_type", EVENT_TYPES)
@pytest.mark.parametrize("n", range(4))
def test_deterministic_stage_outcomes(event_type, n):
    orch = make_orchestrator()
    response = orch.orchestrate(
        make_request(
            event_type=event_type,
            event_id=f"det-{event_type}-{n}",
            orchestration_id=f"orch-det-{event_type}",
        )
    )
    expected = {
        "evidence": "success",
        "twin": "success",
        "decision": "success",
        "analytics": "success",
    }
    if event_type != "manual_confidence_update":
        expected["mission"] = "success"
    assert outcomes(response) == expected


@pytest.mark.parametrize("learner_id", LEARNERS)
@pytest.mark.parametrize("subject_id", SUBJECTS)
def test_diagnostics_accumulate_timings(learner_id, subject_id):
    orch = make_orchestrator()
    for event_type in EVENT_TYPES[:3]:
        orch.orchestrate(
            make_request(
                event_type=event_type,
                learner_id=learner_id,
                subject_id=subject_id,
                event_id=f"{learner_id}-{subject_id}-{event_type}",
            )
        )
    report = orch.diagnostics()
    assert len(report.execution_timings) >= 1
    assert report.registered_ports
