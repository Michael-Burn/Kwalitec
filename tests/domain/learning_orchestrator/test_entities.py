"""Domain vocabulary tests for Learning Orchestrator."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime
from types import MappingProxyType

import pytest

from app.domain.learning_orchestrator.orchestration_context import (
    OrchestrationContext,
)
from app.domain.learning_orchestrator.orchestration_event import (
    OrchestrationEvent,
    OrchestrationEventType,
)
from app.domain.learning_orchestrator.orchestration_result import (
    OrchestrationResult,
)
from app.domain.learning_orchestrator.orchestration_snapshot import (
    OrchestrationSnapshot,
)
from app.domain.learning_orchestrator.orchestration_state import (
    OrchestrationState,
)
from app.domain.learning_orchestrator.pipeline_result import PipelineResult
from app.domain.learning_orchestrator.pipeline_stage import (
    CANONICAL_PIPELINE,
    STAGE_PORT_NAMES,
    PipelineStageName,
    StageOutcome,
)

NOW = datetime(2026, 7, 18, 18, 0, tzinfo=UTC)
EVENT_TYPES = tuple(OrchestrationEventType)


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_event_create_and_freeze(event_type):
    event = OrchestrationEvent.create(
        event_type=event_type,
        learner_id="l1",
        event_id="e1",
        occurred_at=NOW,
        payload={"k": "v"},
    )
    assert event.event_type == event_type
    assert isinstance(event.payload, MappingProxyType)
    with pytest.raises(FrozenInstanceError):
        event.learner_id = "x"  # type: ignore[misc]


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_event_resolve_token(event_type):
    assert OrchestrationEventType.resolve(event_type.value) == event_type


def test_unknown_event_resolve_raises():
    with pytest.raises(ValueError):
        OrchestrationEventType.resolve("nope")


def test_event_requires_ids():
    with pytest.raises(ValueError):
        OrchestrationEvent.create(
            event_type=OrchestrationEventType.SESSION_COMPLETED,
            learner_id="",
            event_id="e1",
            occurred_at=NOW,
        )


@pytest.mark.parametrize("state", list(OrchestrationState))
def test_state_terminal_flag(state):
    expected = state in {
        OrchestrationState.COMPLETED,
        OrchestrationState.PARTIAL,
        OrchestrationState.FAILED,
        OrchestrationState.CANCELLED,
    }
    assert state.is_terminal() is expected


@pytest.mark.parametrize("stage", list(PipelineStageName))
def test_stage_port_mapping(stage):
    assert stage.value in STAGE_PORT_NAMES[stage] or STAGE_PORT_NAMES[stage]


def test_canonical_pipeline_length():
    assert len(CANONICAL_PIPELINE) == 5
    assert CANONICAL_PIPELINE[0] == PipelineStageName.EVIDENCE
    assert CANONICAL_PIPELINE[-1] == PipelineStageName.ANALYTICS


@pytest.mark.parametrize("stage", list(PipelineStageName))
@pytest.mark.parametrize("outcome", list(StageOutcome))
def test_pipeline_result_outcome_matrix(stage, outcome):
    result = PipelineResult(
        stage=stage,
        outcome=outcome,
        error="e" if outcome == StageOutcome.FAILURE else None,
    )
    assert result.stage == stage
    assert result.outcome == outcome
    assert isinstance(result.diagnostics, MappingProxyType)


@pytest.mark.parametrize("stage", list(PipelineStageName))
def test_context_accumulates_results(stage):
    event = OrchestrationEvent.create(
        event_type=OrchestrationEventType.SESSION_COMPLETED,
        learner_id="l1",
        event_id="e1",
        occurred_at=NOW,
    )
    ctx = OrchestrationContext(
        event=event,
        orchestration_id="o1",
        state=OrchestrationState.RUNNING,
        started_at=NOW,
    )
    result = PipelineResult.success(stage, payload={"x": 1})
    updated = ctx.with_result(result)
    assert len(updated.stage_results) == 1
    assert updated.payload_for(stage)["x"] == 1
    assert updated.state == OrchestrationState.RUNNING


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_result_and_snapshot_projection(event_type):
    results = tuple(
        PipelineResult.success(s, payload={"ok": True})
        for s in CANONICAL_PIPELINE
    )
    domain_result = OrchestrationResult.from_context(
        orchestration_id="o1",
        event_id="e1",
        learner_id="l1",
        event_type=event_type.value,
        state=OrchestrationState.COMPLETED,
        stage_results=results,
        duration_ms=12.5,
    )
    assert domain_result.success is True
    snap = OrchestrationSnapshot.from_result(domain_result)
    assert snap.success is True
    assert snap.stage_outcome(PipelineStageName.EVIDENCE) == "success"
    with pytest.raises(FrozenInstanceError):
        snap.success = False  # type: ignore[misc]


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_partial_result_not_success(event_type):
    results = (
        PipelineResult.success(PipelineStageName.EVIDENCE),
        PipelineResult.failure(PipelineStageName.TWIN, error="boom"),
        PipelineResult.success(PipelineStageName.DECISION),
    )
    domain_result = OrchestrationResult.from_context(
        orchestration_id="o1",
        event_id="e1",
        learner_id="l1",
        event_type=event_type.value,
        state=OrchestrationState.PARTIAL,
        stage_results=results,
        duration_ms=3.0,
    )
    assert domain_result.success is False
    assert domain_result.failed_stages == (PipelineStageName.TWIN,)
