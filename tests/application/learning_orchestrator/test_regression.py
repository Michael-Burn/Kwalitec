"""Regression and e2e orchestration tests."""

from __future__ import annotations

import pytest

from app.application.learning_orchestrator.policies.orchestration_policy import (
    DEPENDENCY_CHAIN,
)
from tests.application.learning_orchestrator.helpers import (
    EVENT_TYPES,
    FakeAdaptive,
    FakeEvidence,
    make_orchestrator,
    make_request,
    outcomes,
)


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_full_chain_order_regression(event_type):
    orch = make_orchestrator()
    response = orch.orchestrate(make_request(event_type=event_type))
    stage_names = [s.stage for s in response.pipeline_snapshots]
    # Stage order must be a subsequence of the canonical chain
    chain_index = {name: i for i, name in enumerate(DEPENDENCY_CHAIN)}
    indices = [chain_index[s] for s in stage_names]
    assert indices == sorted(indices)


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_does_not_own_educational_payload_semantics(event_type):
    """Orchestrator passes opaque payloads through without interpreting them."""
    orch = make_orchestrator(
        evidence=FakeEvidence(
            payload={"score": 0.42, "opaque": {"nested": True}}
        ),
        adaptive_learning=FakeAdaptive(
            payload={"intervention": "revision", "priority": 0.9}
        ),
    )
    response = orch.orchestrate(make_request(event_type=event_type))
    assert response.success is True
    # Snapshots expose keys only — not educational conclusions
    evidence_snap = next(
        s for s in response.pipeline_snapshots if s.stage == "evidence"
    )
    assert "opaque" in evidence_snap.payload_keys or "score" in (
        evidence_snap.payload_keys
    )


@pytest.mark.parametrize("event_type", EVENT_TYPES)
@pytest.mark.parametrize("run", range(4))
def test_e2e_repeated_runs_stable(event_type, run):
    orch = make_orchestrator()
    response = orch.orchestrate(
        make_request(event_type=event_type, event_id=f"e2e-{run}")
    )
    assert response.state == "completed"
    assert set(outcomes(response).values()) <= {"success", "warning"}


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_execution_summary_matches_response(event_type):
    orch = make_orchestrator()
    response = orch.orchestrate(make_request(event_type=event_type))
    summary = response.execution_summary
    assert summary is not None
    assert summary.orchestration_id == response.orchestration_id
    assert summary.event_id == response.event_id
    assert summary.success == response.success
    assert summary.state == response.state
    assert summary.executed_stages == response.executed_stages


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_health_unchanged_by_orchestration(event_type):
    orch = make_orchestrator()
    before = orch.health_status()
    orch.orchestrate(make_request(event_type=event_type))
    after = orch.health_status()
    assert before["orchestrator_status"] == after["orchestrator_status"]
    assert before["registered_components"] == after["registered_components"]


def test_package_exports_lazy():
    import app.application.learning_orchestrator as pkg

    assert pkg.LearningOrchestrator is not None
    assert pkg.OrchestrationPolicy is not None
    assert pkg.PipelineEngine is not None


def test_domain_package_exports_lazy():
    import app.domain.learning_orchestrator as pkg

    assert pkg.OrchestrationEvent is not None
    assert pkg.CANONICAL_PIPELINE is not None
    assert pkg.OrchestrationState.COMPLETED.value == "completed"
