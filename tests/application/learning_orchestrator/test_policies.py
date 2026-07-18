"""Policy unit tests for Learning Orchestrator."""

from __future__ import annotations

import pytest

from app.application.learning_orchestrator.exceptions import OrchestrationError
from app.application.learning_orchestrator.policies.orchestration_policy import (
    DEPENDENCY_CHAIN,
    OrchestrationPolicy,
)
from app.application.learning_orchestrator.policies.pipeline_policy import (
    PipelinePolicy,
)
from app.application.learning_orchestrator.policies.retry_policy import (
    RetryPolicy,
)
from app.domain.learning_orchestrator.pipeline_result import PipelineResult
from app.domain.learning_orchestrator.pipeline_stage import PipelineStageName
from tests.application.learning_orchestrator.helpers import EVENT_TYPES


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_stages_for_known_events(event_type):
    stages = OrchestrationPolicy.stages_for(event_type)
    assert stages
    assert all(isinstance(s, PipelineStageName) for s in stages)


def test_unknown_event_raises():
    with pytest.raises(OrchestrationError):
        OrchestrationPolicy.stages_for("totally_unknown")


def test_dependency_chain_order():
    assert DEPENDENCY_CHAIN == (
        "evidence",
        "twin",
        "decision",
        "mission",
        "analytics",
    )


def test_manual_confidence_omits_mission():
    stages = OrchestrationPolicy.stages_for("manual_confidence_update")
    assert PipelineStageName.MISSION not in stages
    assert PipelineStageName.EVIDENCE in stages
    assert PipelineStageName.ANALYTICS in stages


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_required_ports_subset_of_port_names(event_type):
    required = OrchestrationPolicy.required_ports(event_type)
    assert required.issubset(set(OrchestrationPolicy.port_names()))


def test_retry_policy_none():
    policy = RetryPolicy.none()
    assert policy.max_attempts == 1
    assert policy.should_retry(attempt=1, error_kind="port_error") is False


def test_retry_policy_technical():
    policy = RetryPolicy.technical(max_attempts=3)
    assert policy.should_retry(attempt=1, error_kind="unavailable") is True
    assert policy.should_retry(attempt=2, error_kind="port_error") is True
    assert policy.should_retry(attempt=3, error_kind="port_error") is False


def test_retry_policy_rejects_zero_attempts():
    with pytest.raises(ValueError):
        RetryPolicy(max_attempts=0)


def test_pipeline_isolated_continues():
    policy = PipelinePolicy.isolated()
    failure = PipelineResult.failure(
        PipelineStageName.TWIN, error="boom"
    )
    assert policy.should_continue_after(failure) is True


def test_pipeline_fail_fast_stops():
    policy = PipelinePolicy.fail_fast()
    failure = PipelineResult.failure(
        PipelineStageName.TWIN, error="boom"
    )
    assert policy.should_continue_after(failure) is False


def test_pipeline_may_run_after_isolated_failure():
    policy = PipelinePolicy.isolated()
    prior = (
        PipelineResult.failure(PipelineStageName.EVIDENCE, error="x"),
    )
    allowed, reason = policy.may_run_stage(
        PipelineStageName.TWIN, prior_results=prior
    )
    assert allowed is True
    assert reason is None


def test_pipeline_may_not_run_after_fail_fast():
    policy = PipelinePolicy.fail_fast()
    prior = (
        PipelineResult.failure(PipelineStageName.EVIDENCE, error="x"),
    )
    allowed, reason = policy.may_run_stage(
        PipelineStageName.TWIN, prior_results=prior
    )
    assert allowed is False
    assert reason is not None


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_is_known_event(event_type):
    assert OrchestrationPolicy.is_known_event(event_type)


def test_register_event_stages_extension():
    from app.domain.learning_orchestrator.pipeline_stage import (
        PipelineStageName as S,
    )

    OrchestrationPolicy.register_event_stages(
        "future_custom_event",
        (S.EVIDENCE, S.ANALYTICS),
    )
    assert OrchestrationPolicy.is_known_event("future_custom_event")
    assert OrchestrationPolicy.stages_for("future_custom_event") == (
        S.EVIDENCE,
        S.ANALYTICS,
    )
