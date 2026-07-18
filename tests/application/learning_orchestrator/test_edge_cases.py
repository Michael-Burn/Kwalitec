"""Edge-case and failure-handling tests."""

from __future__ import annotations

import pytest

from app.application.learning_orchestrator.exceptions import (
    EventDispatchError,
)
from app.application.learning_orchestrator.policies.pipeline_policy import (
    PipelinePolicy,
)
from app.application.learning_orchestrator.policies.retry_policy import (
    RetryPolicy,
)
from app.domain.learning_orchestrator.pipeline_stage import PipelineStageName
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
def test_empty_optional_ids_ok(event_type):
    orch = make_orchestrator()
    response = orch.orchestrate(
        make_request(
            event_type=event_type,
            session_id=None,
            activity_id=None,
            mission_id=None,
            evidence_id=None,
        )
    )
    assert response.success is True


def test_all_ports_unavailable():
    orch = make_orchestrator(
        evidence=FakeEvidence(available=False),
        twin=FakeTwin(available=False),
        pipeline_policy=PipelinePolicy.isolated(),
    )
    response = orch.orchestrate(make_request())
    assert response.success is False
    assert outcomes(response)["evidence"] == "failure"


def test_retry_exhausted_still_fails():
    evidence = FakeEvidence(fail_times=5)
    orch = make_orchestrator(
        evidence=evidence,
        retry_policy=RetryPolicy.technical(max_attempts=3),
        pipeline_policy=PipelinePolicy.fail_fast(),
    )
    response = orch.orchestrate(make_request())
    assert outcomes(response)["evidence"] == "failure"
    assert evidence.calls.count("process_evidence") == 3
    assert outcomes(response)["twin"] == "skipped"


def test_sequential_policy_requires_prior_success():
    orch = make_orchestrator(
        evidence=FakeEvidence(raise_error=RuntimeError("nope")),
        pipeline_policy=PipelinePolicy.sequential(),
    )
    response = orch.orchestrate(make_request())
    o = outcomes(response)
    assert o["evidence"] == "failure"
    assert o["twin"] == "skipped"


def test_dispatcher_supported_events():
    orch = make_orchestrator()
    supported = orch.dispatcher.supported_events()
    for event_type in EVENT_TYPES:
        assert event_type in supported


def test_dispatch_type_convenience():
    orch = make_orchestrator()
    response = orch.dispatcher.dispatch_type(
        "session_completed",
        learner_id="learner-9",
        event_id="evt-9",
    )
    assert response.event_type == "session_completed"
    assert response.learner_id == "learner-9"


def test_dispatch_type_unknown_raises():
    orch = make_orchestrator()
    with pytest.raises(EventDispatchError):
        orch.dispatcher.dispatch_type(
            "not_real",
            learner_id="learner-9",
        )


def test_request_from_event_roundtrip():
    from app.application.learning_orchestrator.event_dispatcher import (
        EventDispatcher,
    )

    event = make_event()
    request = EventDispatcher.request_from_event(event)
    assert request.event_type == event.event_type.value
    assert request.learner_id == event.learner_id
    assert request.event_id == event.event_id


@pytest.mark.parametrize("stage", list(PipelineStageName))
def test_pipeline_result_factories(stage):
    from app.domain.learning_orchestrator.pipeline_result import PipelineResult

    ok = PipelineResult.success(stage, payload={"a": 1}, warnings=("w",))
    assert ok.succeeded is True
    assert ok.outcome.value == "warning"
    fail = PipelineResult.failure(stage, error="e")
    assert fail.failed is True
    skip = PipelineResult.skip(stage, reason="later")
    assert skip.skipped is True


def test_fail_fast_on_specific_stage():
    policy = PipelinePolicy(
        continue_on_failure=True,
        fail_fast_stages=frozenset({PipelineStageName.EVIDENCE}),
    )
    orch = make_orchestrator(
        evidence=FakeEvidence(raise_error=RuntimeError("critical")),
        pipeline_policy=policy,
    )
    response = orch.orchestrate(make_request())
    o = outcomes(response)
    assert o["evidence"] == "failure"
    assert o["twin"] == "skipped"


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_warnings_propagate_to_response(event_type):
    # Success with empty warnings is the baseline; ensure tuple typing.
    orch = make_orchestrator()
    response = orch.orchestrate(make_request(event_type=event_type))
    assert isinstance(response.warnings, tuple)
