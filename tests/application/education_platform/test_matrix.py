"""Expanded matrix tests to harden composition behaviour."""

from __future__ import annotations

import pytest

from app.application.education_platform.composition_root import CompositionRoot
from app.application.education_platform.dependency_registry import DependencyRegistry
from app.application.education_platform.platform import EducationPlatform
from app.application.education_platform.policies.orchestration_policy import (
    ALL_WORKFLOWS,
    DEPENDENCY_CHAIN,
    OrchestrationPolicy,
)
from app.application.education_platform.policies.validation_policy import (
    ValidationPolicy,
)
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


@pytest.mark.parametrize("workflow", sorted(ALL_WORKFLOWS))
@pytest.mark.parametrize("name", list(DEPENDENCY_CHAIN))
def test_readiness_without_each_port(workflow, name):
    registered = set(DEPENDENCY_CHAIN) - {name}
    required = OrchestrationPolicy.required_ports(workflow)
    expected = required.issubset(registered)
    assert (
        OrchestrationPolicy.workflow_ready(workflow, registered=registered)
        is expected
    )


@pytest.mark.parametrize("name", list(DEPENDENCY_CHAIN))
def test_health_lists_each_component(name):
    health = make_platform().health_status()
    assert name in health["components"]
    assert health["components"][name]["available"] is True


@pytest.mark.parametrize("name", list(DEPENDENCY_CHAIN))
def test_diagnostics_lists_each_engine(name):
    report = make_platform().diagnostics()
    assert name in report.registered_engines
    assert name in report.component_versions


@pytest.mark.parametrize(
    "method",
    [
        "generate_subject",
        "generate_journey",
        "generate_learning_sessions",
        "generate_learning_activities",
        "generate_daily_missions",
        "build_platform_snapshot",
        "validate_platform",
    ],
)
def test_facade_methods_exist(method):
    assert callable(getattr(EducationPlatform, method))


@pytest.mark.parametrize("name", list(DEPENDENCY_CHAIN))
def test_missing_ports_order_stable(name):
    registered = set(DEPENDENCY_CHAIN) - {name}
    missing = ValidationPolicy.missing_ports(registered)
    assert missing == (name,)


@pytest.mark.parametrize(
    "a,b",
    list(zip(DEPENDENCY_CHAIN[:-1], DEPENDENCY_CHAIN[1:], strict=True)),
)
def test_dependency_graph_edges(a, b):
    health = make_platform().health_status()
    assert (a, b) in health["dependency_graph"]


@pytest.mark.parametrize("workflow", sorted(ALL_WORKFLOWS))
def test_failed_then_fixed_composition(workflow):
    platform = EducationPlatform.create()
    if workflow == "validate_platform":
        # Always runnable
        assert platform.validate_platform().success
        return
    method = {
        "generate_subject": "generate_subject",
        "generate_journey": "generate_journey",
        "generate_learning_sessions": "generate_learning_sessions",
        "generate_learning_activities": "generate_learning_activities",
        "generate_daily_missions": "generate_daily_missions",
        "build_platform_snapshot": "build_platform_snapshot",
    }[workflow]
    assert not getattr(platform, method)(make_request()).success
    # Repair by assembling full platform
    full = make_platform()
    assert getattr(full, method)(make_request()).success


@pytest.mark.parametrize(
    "port_name,factory",
    [
        ("curriculum", FakeCurriculum),
        ("blueprint", FakeBlueprint),
        ("journey", FakeJourney),
        ("session", FakeSession),
        ("activity", FakeActivity),
        ("mission", FakeMission),
    ],
)
def test_register_via_composition_root_single(port_name, factory):
    kwargs = {port_name: factory()}
    reg = CompositionRoot.build_registry(**kwargs)
    assert reg.registered_names() == (port_name,)


@pytest.mark.parametrize("n", range(10))
def test_repeated_validate_stable(n):
    platform = make_platform()
    resp = platform.validate_platform()
    assert resp.validation_passed is True
    assert resp.validation_issues == ()


@pytest.mark.parametrize("n", range(8))
def test_repeated_subject_generation_stable(n):
    platform = make_platform()
    resp = platform.generate_subject(make_request())
    assert resp.subject_plan.topic_ids == ("topic-a", "topic-b")


@pytest.mark.parametrize(
    "available_map",
    [
        {"curriculum": False},
        {"blueprint": False},
        {"journey": False},
        {"session": False},
        {"activity": False},
        {"mission": False},
    ],
)
def test_unavailable_port_marks_unhealthy(available_map):
    ports = make_full_ports()
    name, _ = next(iter(available_map.items()))
    port = ports[name]
    port.set_available(False)
    platform = EducationPlatform.create(**ports)
    health = platform.health_status()
    assert health["platform_status"] == "unhealthy"
    assert health["components"][name]["available"] is False


@pytest.mark.parametrize("name", list(DEPENDENCY_CHAIN))
def test_unregister_then_missing(name):
    reg = DependencyRegistry()
    for n, p in make_full_ports().items():
        reg.register(n, p)
    reg.unregister(name)
    assert name in reg.missing_names()
    assert name not in reg.registered_names()
