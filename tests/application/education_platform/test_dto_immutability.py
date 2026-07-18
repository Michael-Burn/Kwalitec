"""DTO immutability and structural tests."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from types import MappingProxyType

import pytest

from app.application.education_platform.dto.education_request import EducationRequest
from app.application.education_platform.dto.education_response import EducationResponse
from app.application.education_platform.dto.generated_mission import GeneratedMission
from app.application.education_platform.dto.generated_session import GeneratedSession
from app.application.education_platform.dto.platform_snapshot import PlatformSnapshot
from app.application.education_platform.dto.subject_plan import SubjectPlan
from app.application.education_platform.dto.workflow_result import WorkflowResult


def test_education_request_frozen():
    req = EducationRequest(workflow="generate_subject", learner_id="l1")
    with pytest.raises(FrozenInstanceError):
        req.learner_id = "x"  # type: ignore[misc]


def test_education_request_context_proxy():
    req = EducationRequest(
        workflow="generate_subject",
        learner_id="l1",
        context={"a": "1"},
    )
    assert isinstance(req.context, MappingProxyType)
    with pytest.raises(TypeError):
        req.context["a"] = "2"  # type: ignore[index]


def test_education_request_default_context():
    req = EducationRequest(workflow="generate_subject", learner_id="l1")
    assert dict(req.context) == {}


def test_education_request_preserves_proxy():
    proxy = MappingProxyType({"k": "v"})
    req = EducationRequest(
        workflow="generate_subject", learner_id="l1", context=proxy
    )
    assert req.context is proxy or dict(req.context) == {"k": "v"}


@pytest.mark.parametrize(
    "field,value",
    [
        ("curriculum_id", "c1"),
        ("subject_id", "s1"),
        ("topic_id", "t1"),
        ("journey_id", "j1"),
        ("session_id", "sess1"),
        ("mission_id", "m1"),
        ("organisation_id", "org1"),
        ("correlation_id", "corr1"),
    ],
)
def test_education_request_optional_fields(field, value):
    req = EducationRequest(
        workflow="generate_subject", learner_id="l1", **{field: value}
    )
    assert getattr(req, field) == value


def test_subject_plan_frozen():
    plan = SubjectPlan(subject_id="s", curriculum_id="c")
    with pytest.raises(FrozenInstanceError):
        plan.subject_id = "x"  # type: ignore[misc]


def test_subject_plan_topic_ids_tuple():
    plan = SubjectPlan(
        subject_id="s", curriculum_id="c", topic_ids=["a", "b"]  # type: ignore[arg-type]
    )
    assert plan.topic_ids == ("a", "b")
    assert isinstance(plan.topic_ids, tuple)


def test_subject_plan_module_ids_tuple():
    plan = SubjectPlan(
        subject_id="s", curriculum_id="c", module_ids=["m1"]  # type: ignore[arg-type]
    )
    assert plan.module_ids == ("m1",)


def test_subject_plan_metadata_proxy():
    plan = SubjectPlan(
        subject_id="s", curriculum_id="c", metadata={"x": "1"}
    )
    assert isinstance(plan.metadata, MappingProxyType)
    with pytest.raises(TypeError):
        plan.metadata["x"] = "2"  # type: ignore[index]


def test_subject_plan_default_metadata():
    plan = SubjectPlan(subject_id="s", curriculum_id="c")
    assert dict(plan.metadata) == {}


def test_generated_session_frozen():
    s = GeneratedSession(session_id="s1", journey_id="j1", topic_id="t1")
    with pytest.raises(FrozenInstanceError):
        s.session_id = "x"  # type: ignore[misc]


def test_generated_session_activity_ids_tuple():
    s = GeneratedSession(
        session_id="s1",
        journey_id="j1",
        topic_id="t1",
        activity_ids=["a1"],  # type: ignore[arg-type]
    )
    assert s.activity_ids == ("a1",)


def test_generated_session_metadata_proxy():
    s = GeneratedSession(
        session_id="s1",
        journey_id="j1",
        topic_id="t1",
        metadata={"k": "v"},
    )
    assert isinstance(s.metadata, MappingProxyType)


def test_generated_session_defaults():
    s = GeneratedSession(session_id="s1", journey_id="j1", topic_id="t1")
    assert s.sequence_index == 0
    assert s.effort is None
    assert s.activity_ids == ()


def test_generated_mission_frozen():
    m = GeneratedMission(
        mission_id="m1",
        learner_id="l1",
        journey_id="j1",
        topic_id="t1",
        session_id="s1",
    )
    with pytest.raises(FrozenInstanceError):
        m.mission_id = "x"  # type: ignore[misc]


def test_generated_mission_metadata_proxy():
    m = GeneratedMission(
        mission_id="m1",
        learner_id="l1",
        journey_id="j1",
        topic_id="t1",
        session_id="s1",
        metadata={"a": "b"},
    )
    assert isinstance(m.metadata, MappingProxyType)


def test_generated_mission_defaults():
    m = GeneratedMission(
        mission_id="m1",
        learner_id="l1",
        journey_id="j1",
        topic_id="t1",
        session_id="s1",
    )
    assert m.mission_type == "today"
    assert m.is_revision is False
    assert m.sequence_index == 0


def test_workflow_result_frozen():
    wr = WorkflowResult(workflow="generate_subject", success=True)
    with pytest.raises(FrozenInstanceError):
        wr.success = False  # type: ignore[misc]


def test_workflow_result_steps_tuple():
    wr = WorkflowResult(
        workflow="generate_subject",
        success=True,
        steps=["curriculum"],  # type: ignore[arg-type]
    )
    assert wr.steps == ("curriculum",)


def test_workflow_result_timings_proxy():
    wr = WorkflowResult(
        workflow="generate_subject",
        success=True,
        step_timings_ms={"curriculum": 1.5},
    )
    assert isinstance(wr.step_timings_ms, MappingProxyType)


def test_workflow_result_metadata_proxy():
    wr = WorkflowResult(
        workflow="generate_subject", success=True, metadata={"k": "v"}
    )
    assert isinstance(wr.metadata, MappingProxyType)


def test_platform_snapshot_frozen():
    snap = PlatformSnapshot(platform_version="v1", learner_id="l1")
    with pytest.raises(FrozenInstanceError):
        snap.learner_id = "x"  # type: ignore[misc]


def test_platform_snapshot_sessions_tuple():
    s = GeneratedSession(session_id="s1", journey_id="j1", topic_id="t1")
    snap = PlatformSnapshot(
        platform_version="v1",
        learner_id="l1",
        sessions=[s],  # type: ignore[arg-type]
    )
    assert snap.sessions == (s,)


def test_platform_snapshot_missions_tuple():
    m = GeneratedMission(
        mission_id="m1",
        learner_id="l1",
        journey_id="j1",
        topic_id="t1",
        session_id="s1",
    )
    snap = PlatformSnapshot(
        platform_version="v1",
        learner_id="l1",
        missions=[m],  # type: ignore[arg-type]
    )
    assert snap.missions == (m,)


def test_platform_snapshot_readiness_proxy():
    snap = PlatformSnapshot(
        platform_version="v1",
        learner_id="l1",
        workflow_readiness={"generate_subject": True},
    )
    assert isinstance(snap.workflow_readiness, MappingProxyType)


def test_platform_snapshot_metadata_proxy():
    snap = PlatformSnapshot(
        platform_version="v1", learner_id="l1", metadata={"a": "1"}
    )
    assert isinstance(snap.metadata, MappingProxyType)


def test_platform_snapshot_defaults():
    snap = PlatformSnapshot(platform_version="v1", learner_id="l1")
    assert snap.sessions == ()
    assert snap.missions == ()
    assert snap.registered_ports == ()
    assert snap.missing_ports == ()


def test_education_response_frozen():
    resp = EducationResponse(workflow="generate_subject", success=True)
    with pytest.raises(FrozenInstanceError):
        resp.success = False  # type: ignore[misc]


def test_education_response_collections_tuple():
    resp = EducationResponse(
        workflow="generate_subject",
        success=True,
        activity_ids=["a1"],  # type: ignore[arg-type]
        validation_issues=["x"],  # type: ignore[arg-type]
    )
    assert resp.activity_ids == ("a1",)
    assert resp.validation_issues == ("x",)


def test_education_response_metadata_proxy():
    resp = EducationResponse(
        workflow="generate_subject", success=True, metadata={"z": "1"}
    )
    assert isinstance(resp.metadata, MappingProxyType)


def test_education_response_defaults():
    resp = EducationResponse(workflow="generate_subject", success=True)
    assert resp.sessions == ()
    assert resp.missions == ()
    assert resp.subject_plan is None
    assert resp.error is None


@pytest.mark.parametrize(
    "cls,kwargs,field",
    [
        (
            EducationRequest,
            {"workflow": "generate_subject", "learner_id": "l"},
            "workflow",
        ),
        (
            SubjectPlan,
            {"subject_id": "s", "curriculum_id": "c"},
            "subject_id",
        ),
        (
            GeneratedSession,
            {"session_id": "s", "journey_id": "j", "topic_id": "t"},
            "session_id",
        ),
        (
            GeneratedMission,
            {
                "mission_id": "m",
                "learner_id": "l",
                "journey_id": "j",
                "topic_id": "t",
                "session_id": "s",
            },
            "mission_id",
        ),
        (
            WorkflowResult,
            {"workflow": "generate_subject", "success": True},
            "workflow",
        ),
        (
            PlatformSnapshot,
            {"platform_version": "v", "learner_id": "l"},
            "platform_version",
        ),
        (
            EducationResponse,
            {"workflow": "generate_subject", "success": True},
            "workflow",
        ),
    ],
)
def test_all_dtos_reject_mutation(cls, kwargs, field):
    obj = cls(**kwargs)
    with pytest.raises(FrozenInstanceError):
        setattr(obj, field, "mutated")


def test_dto_package_exports():
    from app.application.education_platform import dto as dto_pkg

    for name in (
        "EducationRequest",
        "EducationResponse",
        "GeneratedMission",
        "GeneratedSession",
        "PlatformSnapshot",
        "SubjectPlan",
        "WorkflowResult",
    ):
        assert hasattr(dto_pkg, name)
