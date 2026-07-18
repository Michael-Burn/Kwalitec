"""OrchestrationService and WorkflowExecutor tests."""

from __future__ import annotations

import pytest

from app.application.education_platform.composition_root import CompositionRoot
from app.application.education_platform.dto.education_request import EducationRequest
from app.application.education_platform.exceptions import (
    OrchestrationError,
    ValidationError,
)
from app.application.education_platform.orchestration_service import (
    OrchestrationService,
)
from app.application.education_platform.policies.orchestration_policy import (
    WORKFLOW_GENERATE_DAILY_MISSIONS,
    WORKFLOW_GENERATE_JOURNEY,
    WORKFLOW_GENERATE_LEARNING_ACTIVITIES,
    WORKFLOW_GENERATE_LEARNING_SESSIONS,
    WORKFLOW_GENERATE_SUBJECT,
    WORKFLOW_VALIDATE_PLATFORM,
)
from app.application.education_platform.workflow_executor import WorkflowExecutor
from tests.application.education_platform.helpers import (
    FakeActivity,
    FakeBlueprint,
    FakeCurriculum,
    FakeJourney,
    FakeMission,
    FakeSession,
    make_full_ports,
    make_request,
)


def test_orchestration_unknown_workflow_raises():
    reg = CompositionRoot.build_registry(curriculum=FakeCurriculum())
    orch = OrchestrationService(registry=reg)
    with pytest.raises(OrchestrationError):
        orch.execute(
            EducationRequest(workflow="hallucinate", learner_id="l1")
        )


def test_orchestration_not_ready_raises():
    reg = CompositionRoot.build_registry()
    orch = OrchestrationService(registry=reg)
    with pytest.raises(ValidationError):
        orch.execute(make_request(workflow=WORKFLOW_GENERATE_SUBJECT))


def test_executor_generate_subject():
    reg = CompositionRoot.build_registry(curriculum=FakeCurriculum())
    executor = WorkflowExecutor()
    resp = executor.run(
        request=make_request(workflow=WORKFLOW_GENERATE_SUBJECT),
        steps=("curriculum",),
        registry=reg,
    )
    assert resp.success
    assert resp.subject_plan is not None
    assert resp.subject_plan.subject_id == "subject-1"
    assert resp.workflow_result.steps == ("curriculum",)


def test_executor_generate_journey():
    call_log: list[str] = []
    reg = CompositionRoot.build_registry(
        curriculum=FakeCurriculum(call_log=call_log),
        blueprint=FakeBlueprint(call_log=call_log),
        journey=FakeJourney(call_log=call_log),
    )
    executor = WorkflowExecutor()
    resp = executor.run(
        request=make_request(workflow=WORKFLOW_GENERATE_JOURNEY),
        steps=("curriculum", "blueprint", "journey"),
        registry=reg,
    )
    assert resp.success
    assert resp.journey_id == "journey-1"
    assert resp.blueprint_id == "bp-standard"
    assert call_log == [
        "resolve_subject",
        "select_blueprint_id",
        "create_journey",
    ]


def test_executor_sessions_uses_blueprint_count():
    reg = CompositionRoot.build_registry(
        curriculum=FakeCurriculum(),
        blueprint=FakeBlueprint(session_count=3),
        journey=FakeJourney(),
        session=FakeSession(),
    )
    resp = WorkflowExecutor().run(
        request=make_request(workflow=WORKFLOW_GENERATE_LEARNING_SESSIONS),
        steps=("curriculum", "blueprint", "journey", "session"),
        registry=reg,
    )
    assert resp.success
    assert len(resp.sessions) == 3


def test_executor_activities():
    reg = CompositionRoot.build_registry(
        curriculum=FakeCurriculum(),
        blueprint=FakeBlueprint(session_count=1),
        journey=FakeJourney(),
        session=FakeSession(),
        activity=FakeActivity(),
    )
    resp = WorkflowExecutor().run(
        request=make_request(workflow=WORKFLOW_GENERATE_LEARNING_ACTIVITIES),
        steps=("curriculum", "blueprint", "journey", "session", "activity"),
        registry=reg,
    )
    assert resp.success
    assert len(resp.activity_ids) == 3
    assert resp.sessions[0].activity_ids


def test_executor_missions():
    ports = make_full_ports()
    reg = CompositionRoot.build_registry(**ports)
    resp = WorkflowExecutor().run(
        request=make_request(workflow=WORKFLOW_GENERATE_DAILY_MISSIONS),
        steps=(
            "curriculum",
            "blueprint",
            "journey",
            "session",
            "activity",
            "mission",
        ),
        registry=reg,
    )
    assert resp.success
    assert len(resp.missions) == 1
    assert resp.missions[0].mission_id == "mission-1"


def test_executor_validate_platform():
    reg = CompositionRoot.build_registry(**make_full_ports())
    resp = WorkflowExecutor().run(
        request=make_request(workflow=WORKFLOW_VALIDATE_PLATFORM),
        steps=(),
        registry=reg,
    )
    assert resp.success
    assert resp.validation_passed is True


def test_executor_validate_incomplete():
    reg = CompositionRoot.build_registry(curriculum=FakeCurriculum())
    resp = WorkflowExecutor().run(
        request=make_request(workflow=WORKFLOW_VALIDATE_PLATFORM),
        steps=(),
        registry=reg,
    )
    assert resp.success  # validation ran
    assert resp.validation_passed is False
    assert resp.validation_issues


def test_executor_snapshot():
    reg = CompositionRoot.build_registry(**make_full_ports())
    resp = WorkflowExecutor().run(
        request=make_request(workflow="build_platform_snapshot"),
        steps=(
            "curriculum",
            "blueprint",
            "journey",
            "session",
            "activity",
            "mission",
        ),
        registry=reg,
    )
    assert resp.success
    assert resp.snapshot is not None
    assert resp.snapshot.learner_id == "learner-1"
    assert resp.snapshot.missions


def test_executor_unavailable_port_fails_response():
    curr = FakeCurriculum(available=False)
    reg = CompositionRoot.build_registry(curriculum=curr)
    resp = WorkflowExecutor().run(
        request=make_request(workflow=WORKFLOW_GENERATE_SUBJECT),
        steps=("curriculum",),
        registry=reg,
    )
    assert resp.success is False
    assert "PortUnavailable" in (resp.error or "")


def test_executor_records_timings():
    reg = CompositionRoot.build_registry(curriculum=FakeCurriculum())
    resp = WorkflowExecutor().run(
        request=make_request(workflow=WORKFLOW_GENERATE_SUBJECT),
        steps=("curriculum",),
        registry=reg,
    )
    assert "curriculum" in resp.workflow_result.step_timings_ms
    assert resp.workflow_result.duration_ms >= 0


def test_executor_reuses_existing_journey_id():
    reg = CompositionRoot.build_registry(
        curriculum=FakeCurriculum(),
        blueprint=FakeBlueprint(),
        journey=FakeJourney(),
    )
    resp = WorkflowExecutor().run(
        request=make_request(
            workflow=WORKFLOW_GENERATE_JOURNEY, journey_id="existing-j"
        ),
        steps=("curriculum", "blueprint", "journey"),
        registry=reg,
    )
    assert resp.journey_id == "existing-j"


def test_orchestration_execute_subject():
    reg = CompositionRoot.build_registry(curriculum=FakeCurriculum())
    orch = OrchestrationService(registry=reg)
    resp = orch.execute(make_request(workflow=WORKFLOW_GENERATE_SUBJECT))
    assert resp.success
    assert resp.subject_plan is not None


def test_step_order_deterministic():
    log: list[str] = []
    ports = {
        "curriculum": FakeCurriculum(call_log=log),
        "blueprint": FakeBlueprint(call_log=log),
        "journey": FakeJourney(call_log=log),
        "session": FakeSession(call_log=log),
        "activity": FakeActivity(call_log=log),
        "mission": FakeMission(call_log=log),
    }
    reg = CompositionRoot.build_registry(**ports)
    WorkflowExecutor().run(
        request=make_request(workflow=WORKFLOW_GENERATE_DAILY_MISSIONS),
        steps=(
            "curriculum",
            "blueprint",
            "journey",
            "session",
            "activity",
            "mission",
        ),
        registry=reg,
    )
    # blueprint estimate_session_count is also called during session step
    assert log[0] == "resolve_subject"
    assert log[1] == "select_blueprint_id"
    assert log[2] == "create_journey"
    assert "plan_sessions" in log
    assert "plan_activity_ids" in log
    assert log[-1] == "generate_missions"


@pytest.mark.parametrize(
    "workflow,expected_prefix",
    [
        (WORKFLOW_GENERATE_SUBJECT, ("curriculum",)),
        (WORKFLOW_GENERATE_JOURNEY, ("curriculum", "blueprint", "journey")),
        (
            WORKFLOW_GENERATE_LEARNING_SESSIONS,
            ("curriculum", "blueprint", "journey", "session"),
        ),
    ],
)
def test_orchestration_step_prefixes(workflow, expected_prefix):
    ports = make_full_ports()
    reg = CompositionRoot.build_registry(**ports)
    resp = OrchestrationService(registry=reg).execute(
        make_request(workflow=workflow)
    )
    assert resp.success
    assert resp.workflow_result.steps[: len(expected_prefix)] == expected_prefix
