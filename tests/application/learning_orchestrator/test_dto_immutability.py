"""DTO immutability tests for Learning Orchestrator."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime
from types import MappingProxyType

import pytest

from app.application.learning_orchestrator.dto.execution_summary import (
    ExecutionSummary,
)
from app.application.learning_orchestrator.dto.orchestration_request import (
    OrchestrationRequest,
)
from app.application.learning_orchestrator.dto.orchestration_response import (
    OrchestrationResponse,
)
from app.application.learning_orchestrator.dto.pipeline_snapshot import (
    PipelineSnapshot,
)
from tests.application.learning_orchestrator.helpers import (
    EVENT_TYPES,
    make_orchestrator,
    make_request,
)

NOW = datetime(2026, 7, 18, 18, 0, tzinfo=UTC)


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_request_frozen(event_type):
    req = make_request(event_type=event_type)
    with pytest.raises(FrozenInstanceError):
        req.learner_id = "other"  # type: ignore[misc]


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_response_frozen(event_type):
    orch = make_orchestrator()
    response = orch.orchestrate(make_request(event_type=event_type))
    with pytest.raises(FrozenInstanceError):
        response.success = False  # type: ignore[misc]


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_pipeline_snapshot_frozen(event_type):
    orch = make_orchestrator()
    response = orch.orchestrate(make_request(event_type=event_type))
    snap = response.pipeline_snapshots[0]
    with pytest.raises(FrozenInstanceError):
        snap.outcome = "failure"  # type: ignore[misc]


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_execution_summary_frozen(event_type):
    orch = make_orchestrator()
    response = orch.orchestrate(make_request(event_type=event_type))
    summary = response.execution_summary
    assert summary is not None
    with pytest.raises(FrozenInstanceError):
        summary.success = False  # type: ignore[misc]


def test_request_coerces_payload_to_mapping_proxy():
    req = OrchestrationRequest(
        event_type="learning_activity_completed",
        learner_id="l1",
        event_id="e1",
        occurred_at=NOW,
        payload={"a": 1},
    )
    assert isinstance(req.payload, MappingProxyType)
    with pytest.raises(TypeError):
        req.payload["a"] = 2  # type: ignore[index]


def test_request_requires_learner_id():
    with pytest.raises(ValueError):
        OrchestrationRequest(
            event_type="learning_activity_completed",
            learner_id="",
            event_id="e1",
            occurred_at=NOW,
        )


def test_pipeline_snapshot_from_result_keys():
    from app.domain.learning_orchestrator.pipeline_result import PipelineResult
    from app.domain.learning_orchestrator.pipeline_stage import (
        PipelineStageName,
    )

    result = PipelineResult.success(
        PipelineStageName.EVIDENCE,
        payload={"z": 1, "a": 2},
    )
    snap = PipelineSnapshot.from_result(result)
    assert snap.payload_keys == ("a", "z")
    assert snap.succeeded is True


def test_execution_summary_stage_timings_immutable():
    summary = ExecutionSummary(
        orchestration_id="o1",
        event_id="e1",
        learner_id="l1",
        event_type="learning_activity_completed",
        state="completed",
        success=True,
        executed_stages=("evidence",),
        duration_ms=1.0,
        stage_timings_ms={"evidence": 1.0},
        pipeline_diagnostics=(),
        dependency_status={},
        warnings=(),
    )
    assert isinstance(summary.stage_timings_ms, MappingProxyType)
    with pytest.raises(TypeError):
        summary.stage_timings_ms["evidence"] = 99  # type: ignore[index]


def test_response_failed_stages_property():
    response = OrchestrationResponse(
        orchestration_id="o1",
        event_id="e1",
        learner_id="l1",
        event_type="learning_activity_completed",
        success=False,
        state="partial",
        pipeline_snapshots=(
            PipelineSnapshot(stage="evidence", outcome="success"),
            PipelineSnapshot(stage="twin", outcome="failure", error="x"),
        ),
    )
    assert response.failed_stages == ("twin",)
    assert response.executed_stages == ("evidence", "twin")
