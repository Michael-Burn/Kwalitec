"""Additional coverage: exceptions, edge cases, and workflow matrix."""

from __future__ import annotations

import pytest

from app.application.education_platform.composition_root import CompositionRoot
from app.application.education_platform.dependency_registry import DependencyRegistry
from app.application.education_platform.dto.education_request import EducationRequest
from app.application.education_platform.dto.education_response import EducationResponse
from app.application.education_platform.dto.generated_mission import GeneratedMission
from app.application.education_platform.dto.generated_session import GeneratedSession
from app.application.education_platform.dto.subject_plan import SubjectPlan
from app.application.education_platform.dto.workflow_result import WorkflowResult
from app.application.education_platform.exceptions import (
    CompositionError,
    DependencyError,
    EducationPlatformError,
    OrchestrationError,
    PortUnavailable,
    ValidationError,
    WorkflowError,
)
from app.application.education_platform.orchestration_service import (
    OrchestrationService,
)
from app.application.education_platform.platform import EducationPlatform
from app.application.education_platform.policies.orchestration_policy import (
    ALL_WORKFLOWS,
    DEPENDENCY_CHAIN,
    OrchestrationPolicy,
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
    make_platform,
    make_request,
)


@pytest.mark.parametrize(
    "exc",
    [
        EducationPlatformError,
        DependencyError,
        ValidationError,
        WorkflowError,
        OrchestrationError,
        CompositionError,
        PortUnavailable,
    ],
)
def test_exception_can_be_raised_and_caught(exc):
    with pytest.raises(EducationPlatformError):
        raise exc("boom")


@pytest.mark.parametrize("workflow", sorted(ALL_WORKFLOWS))
def test_policy_steps_are_tuples(workflow):
    steps = OrchestrationPolicy.steps_for(workflow)
    assert isinstance(steps, tuple)
    for step in steps:
        assert step in DEPENDENCY_CHAIN


@pytest.mark.parametrize("workflow", sorted(ALL_WORKFLOWS))
def test_workflow_ready_with_full_registration(workflow):
    assert OrchestrationPolicy.workflow_ready(
        workflow, registered=set(DEPENDENCY_CHAIN)
    )


@pytest.mark.parametrize("name", list(DEPENDENCY_CHAIN))
def test_registry_roundtrip_each_port(name):
    reg = DependencyRegistry()
    ports = make_full_ports()
    reg.register(name, ports[name])
    assert reg.get(name) is ports[name]
    reg.unregister(name)
    assert not reg.has(name)


def test_executor_unknown_step_fails():
    reg = CompositionRoot.build_registry(curriculum=FakeCurriculum())
    resp = WorkflowExecutor().run(
        request=make_request(workflow="generate_subject"),
        steps=("ghost",),  # type: ignore[arg-type]
        registry=reg,
    )
    assert resp.success is False


def test_request_with_empty_learner_still_structures():
    platform = make_platform()
    resp = platform.generate_subject(
        EducationRequest(workflow="generate_subject", learner_id="")
    )
    assert resp.success
    assert resp.subject_plan is not None


def test_mission_id_override():
    platform = make_platform()
    resp = platform.generate_daily_missions(
        make_request(mission_id="custom-mission")
    )
    assert resp.missions[0].mission_id == "custom-mission"


def test_session_id_override_for_activities():
    platform = make_platform()
    resp = platform.generate_learning_activities(
        make_request(session_id="session-override")
    )
    assert resp.success
    assert all(a.startswith("session-override:") for a in resp.activity_ids)


def test_subject_plan_title_present():
    platform = make_platform()
    resp = platform.generate_subject(make_request())
    assert resp.subject_plan.title


def test_workflow_result_on_success():
    platform = make_platform()
    resp = platform.generate_subject(make_request())
    assert isinstance(resp.workflow_result, WorkflowResult)
    assert resp.workflow_result.success is True
    assert resp.workflow_result.error is None


def test_response_error_none_on_success():
    platform = make_platform()
    resp = platform.generate_journey(make_request())
    assert resp.error is None


def test_build_registry_kwargs_none_skipped():
    reg = CompositionRoot.build_registry(
        curriculum=FakeCurriculum(),
        blueprint=None,
        journey=None,
    )
    assert reg.registered_names() == ("curriculum",)


def test_platform_create_empty_is_valid_object():
    platform = EducationPlatform.create()
    assert isinstance(platform, EducationPlatform)
    assert platform.validate_platform().validation_passed is False


def test_diagnostics_after_failed_workflow():
    platform = EducationPlatform.create(curriculum=FakeCurriculum())
    platform.generate_daily_missions(make_request())
    report = platform.diagnostics()
    assert "generate_daily_missions" in report.workflow_timings


def test_health_registered_components_tuple():
    health = make_platform().health_status()
    assert isinstance(health["registered_components"], tuple)


def test_orchestration_service_uses_injected_executor():
    class CountingExecutor(WorkflowExecutor):
        def __init__(self) -> None:
            super().__init__()
            self.runs = 0

        def run(self, **kwargs):
            self.runs += 1
            return super().run(**kwargs)

    reg = CompositionRoot.build_registry(curriculum=FakeCurriculum())
    executor = CountingExecutor()
    orch = OrchestrationService(registry=reg, executor=executor)
    orch.execute(make_request(workflow="generate_subject"))
    assert executor.runs == 1


def test_generated_session_equality():
    a = GeneratedSession(session_id="s", journey_id="j", topic_id="t")
    b = GeneratedSession(session_id="s", journey_id="j", topic_id="t")
    assert a == b


def test_generated_mission_equality():
    kwargs = dict(
        mission_id="m",
        learner_id="l",
        journey_id="j",
        topic_id="t",
        session_id="s",
    )
    assert GeneratedMission(**kwargs) == GeneratedMission(**kwargs)


def test_subject_plan_equality():
    a = SubjectPlan(subject_id="s", curriculum_id="c", topic_ids=("t",))
    b = SubjectPlan(subject_id="s", curriculum_id="c", topic_ids=("t",))
    assert a == b


def test_education_response_equality():
    a = EducationResponse(workflow="generate_subject", success=True)
    b = EducationResponse(workflow="generate_subject", success=True)
    assert a == b


@pytest.mark.parametrize("count", [1, 2, 3, 5])
def test_session_count_matrix(count):
    platform = EducationPlatform.create(
        curriculum=FakeCurriculum(),
        blueprint=FakeBlueprint(session_count=count),
        journey=FakeJourney(),
        session=FakeSession(),
        activity=FakeActivity(),
        mission=FakeMission(),
    )
    resp = platform.generate_learning_sessions(make_request())
    assert len(resp.sessions) == count


def test_zero_blueprint_session_count_becomes_one():
    platform = EducationPlatform.create(
        curriculum=FakeCurriculum(),
        blueprint=FakeBlueprint(session_count=0),
        journey=FakeJourney(),
        session=FakeSession(),
    )
    resp = platform.generate_learning_sessions(make_request())
    assert len(resp.sessions) == 1


def test_topic_from_subject_when_request_topic_absent():
    platform = EducationPlatform.create(
        curriculum=FakeCurriculum(topic_ids=("first-topic", "second")),
        blueprint=FakeBlueprint(session_count=1),
        journey=FakeJourney(),
        session=FakeSession(),
        activity=FakeActivity(),
        mission=FakeMission(),
    )
    resp = platform.generate_daily_missions(make_request(topic_id=None))
    assert resp.success
    assert resp.missions[0].topic_id in {"first-topic", "topic-a"}


def test_package_getattr_unknown():
    import app.application.education_platform as pkg

    with pytest.raises(AttributeError):
        _ = pkg.DoesNotExist  # type: ignore[attr-defined]


@pytest.mark.parametrize(
    "learner_id",
    ["l1", "learner-abc", "user_001", "x"],
)
def test_learner_id_propagates_to_mission(learner_id):
    platform = make_platform()
    resp = platform.generate_daily_missions(
        make_request(learner_id=learner_id)
    )
    assert resp.missions[0].learner_id == learner_id


@pytest.mark.parametrize(
    "subject_id,curriculum_id",
    [
        ("s1", "c1"),
        ("cs1", "ifoa-cs1-2026"),
        ("law", "bar-2025"),
    ],
)
def test_subject_and_curriculum_ids(subject_id, curriculum_id):
    platform = make_platform()
    resp = platform.generate_subject(
        make_request(subject_id=subject_id, curriculum_id=curriculum_id)
    )
    assert resp.subject_plan.subject_id == subject_id
    assert resp.subject_plan.curriculum_id == curriculum_id


@pytest.mark.parametrize("effort", ["low", "medium", "high"])
def test_session_effort_passthrough(effort):
    class EffortSession(FakeSession):
        def plan_sessions(self, request, *, journey_id, count=1):
            sessions = super().plan_sessions(
                request, journey_id=journey_id, count=count
            )
            return tuple(
                GeneratedSession(
                    session_id=s.session_id,
                    journey_id=s.journey_id,
                    topic_id=s.topic_id,
                    sequence_index=s.sequence_index,
                    effort=effort,
                )
                for s in sessions
            )

    platform = EducationPlatform.create(
        curriculum=FakeCurriculum(),
        blueprint=FakeBlueprint(session_count=1),
        journey=FakeJourney(),
        session=EffortSession(),
    )
    resp = platform.generate_learning_sessions(make_request())
    assert resp.sessions[0].effort == effort


def test_validate_platform_steps_in_result():
    platform = make_platform()
    resp = platform.validate_platform()
    assert resp.workflow_result.steps == ("validate",)


def test_snapshot_workflow_readiness_complete():
    platform = make_platform()
    snap = platform.build_platform_snapshot(make_request()).snapshot
    assert all(snap.workflow_readiness.values())


def test_multiple_platforms_isolated():
    a = make_platform()
    b = EducationPlatform.create(curriculum=FakeCurriculum(subject_id="only-b"))
    a_plan = a.generate_subject(make_request()).subject_plan
    b_plan = b.generate_subject(make_request(subject_id=None)).subject_plan
    assert a_plan.subject_id == "subject-1"
    assert b_plan.subject_id == "only-b"
