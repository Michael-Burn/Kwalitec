"""Additional volume matrix — learner × subject × event × availability."""

from __future__ import annotations

import pytest

from app.application.learning_orchestrator.policies.pipeline_policy import (
    PipelinePolicy,
)
from tests.application.learning_orchestrator.helpers import (
    EVENT_TYPES,
    FakeEvidence,
    FakeTwin,
    make_orchestrator,
    make_request,
    outcomes,
)

LEARNERS = ("L1", "L2", "L3")
SUBJECTS = ("S1", "S2", "S3")
AVAIL = (True, False)


@pytest.mark.parametrize("learner_id", LEARNERS)
@pytest.mark.parametrize("subject_id", SUBJECTS)
@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_orchestrate_identity_grid(learner_id, subject_id, event_type):
    orch = make_orchestrator()
    response = orch.orchestrate(
        make_request(
            event_type=event_type,
            learner_id=learner_id,
            subject_id=subject_id,
            event_id=f"{learner_id}-{subject_id}-{event_type}",
            orchestration_id=f"orch-{learner_id}-{subject_id}",
        )
    )
    assert response.learner_id == learner_id
    assert response.success is True
    assert response.execution_summary is not None
    assert response.execution_summary.learner_id == learner_id


@pytest.mark.parametrize("event_type", EVENT_TYPES)
@pytest.mark.parametrize("evidence_ok", AVAIL)
@pytest.mark.parametrize("twin_ok", AVAIL)
def test_availability_combination_grid(event_type, evidence_ok, twin_ok):
    orch = make_orchestrator(
        evidence=FakeEvidence(available=evidence_ok),
        twin=FakeTwin(available=twin_ok),
        pipeline_policy=PipelinePolicy.isolated(),
    )
    response = orch.orchestrate(make_request(event_type=event_type))
    o = outcomes(response)
    if not evidence_ok:
        assert o["evidence"] == "failure"
        assert response.success is False
    elif not twin_ok:
        assert o["evidence"] in {"success", "warning"}
        assert o["twin"] == "failure"
        assert response.success is False
    else:
        assert response.success is True
