"""HealthService and Diagnostics tests."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from types import MappingProxyType

import pytest

from app.application.education_platform.composition_root import CompositionRoot
from app.application.education_platform.diagnostics import (
    DiagnosticReport,
    Diagnostics,
)
from app.application.education_platform.dto.workflow_result import WorkflowResult
from app.application.education_platform.health_service import HealthService
from app.application.education_platform.platform import EducationPlatform
from app.application.education_platform.platform_context import PlatformContext
from tests.application.education_platform.helpers import (
    NOW,
    FakeCurriculum,
    FakeSession,
    make_full_ports,
    make_platform,
)


def test_health_healthy_when_complete():
    reg = CompositionRoot.build_registry(**make_full_ports())
    health = HealthService(
        registry=reg,
        platform_version=EducationPlatform.PLATFORM_VERSION,
        clock=lambda: NOW,
    ).status()
    assert health["platform_status"] == "healthy"
    assert health["all_workflows_ready"] is True
    assert health["missing_dependencies"] == ()


def test_health_degraded_when_missing():
    reg = CompositionRoot.build_registry(curriculum=FakeCurriculum())
    health = HealthService(
        registry=reg,
        platform_version="v",
        clock=lambda: NOW,
    ).status()
    assert health["platform_status"] == "degraded"
    assert health["missing_dependencies"]
    assert health["all_workflows_ready"] is False


def test_health_unhealthy_when_port_down():
    ports = make_full_ports()
    ports["session"] = FakeSession(available=False)
    reg = CompositionRoot.build_registry(**ports)
    health = HealthService(
        registry=reg, platform_version="v", clock=lambda: NOW
    ).status()
    assert health["platform_status"] == "unhealthy"


def test_health_no_mutation():
    reg = CompositionRoot.build_registry(**make_full_ports())
    svc = HealthService(registry=reg, platform_version="v", clock=lambda: NOW)
    before = reg.registered_names()
    svc.status()
    svc.status()
    assert reg.registered_names() == before


def test_health_components_versions():
    reg = CompositionRoot.build_registry(
        curriculum=FakeCurriculum(component_version="2.3.4")
    )
    health = HealthService(
        registry=reg, platform_version="v", clock=lambda: NOW
    ).status()
    comps = health["components"]
    assert comps["curriculum"]["component_version"] == "2.3.4"
    assert comps["curriculum"]["available"] is True


def test_health_observed_at():
    reg = CompositionRoot.build_registry()
    health = HealthService(
        registry=reg, platform_version="v", clock=lambda: NOW
    ).status()
    assert health["observed_at"] == NOW.isoformat()


def test_health_dependency_graph():
    reg = CompositionRoot.build_registry(**make_full_ports())
    health = HealthService(
        registry=reg, platform_version="v", clock=lambda: NOW
    ).status()
    graph = health["dependency_graph"]
    assert ("curriculum", "blueprint") in graph
    assert ("activity", "mission") in graph


def test_health_workflow_readiness_proxy():
    reg = CompositionRoot.build_registry(**make_full_ports())
    health = HealthService(
        registry=reg, platform_version="v", clock=lambda: NOW
    ).status()
    assert isinstance(health["workflow_readiness"], MappingProxyType)


def test_platform_context_from_registry():
    reg = CompositionRoot.build_registry(**make_full_ports())
    ctx = PlatformContext.from_registry(reg, platform_version="p1")
    assert ctx.platform_version == "p1"
    assert len(ctx.registered_ports) == 6
    assert ctx.missing_ports == ()
    assert len(ctx.dependency_graph) == 5


def test_platform_context_frozen():
    reg = CompositionRoot.build_registry(curriculum=FakeCurriculum())
    ctx = PlatformContext.from_registry(reg, platform_version="p1")
    with pytest.raises(FrozenInstanceError):
        ctx.platform_version = "x"  # type: ignore[misc]


def test_diagnostics_report_immutable():
    platform = make_platform()
    report = platform.diagnostics()
    with pytest.raises(FrozenInstanceError):
        report.validation_passed = False  # type: ignore[misc]


def test_diagnostics_records_timings():
    reg = CompositionRoot.build_registry(**make_full_ports())
    diag = Diagnostics(
        registry=reg,
        platform_version="v",
        clock=lambda: NOW,
    )
    diag.record_workflow_timing(
        WorkflowResult(
            workflow="generate_subject", success=True, duration_ms=12.5
        )
    )
    report = diag.report()
    assert report.workflow_timings["generate_subject"] == 12.5
    assert report.generated_at == NOW.isoformat()


def test_diagnostics_canonical_chain():
    report = make_platform().diagnostics()
    assert report.canonical_chain[0] == "curriculum"
    assert report.canonical_chain[-1] == "mission"


def test_diagnostics_registered_engines():
    report = make_platform().diagnostics()
    assert "journey" in report.registered_engines


def test_diagnostics_metadata_proxy():
    report = DiagnosticReport(
        platform_version="v",
        generated_at="t",
        registered_engines=(),
        missing_ports=(),
        dependency_graph=(),
        component_versions=MappingProxyType({}),
        validation_passed=True,
        validation_issues=(),
        workflow_readiness=MappingProxyType({}),
        workflow_timings=MappingProxyType({}),
        canonical_chain=(),
        metadata={"a": "1"},
    )
    assert isinstance(report.metadata, MappingProxyType)


def test_diagnostics_does_not_mutate_registry():
    reg = CompositionRoot.build_registry(**make_full_ports())
    diag = Diagnostics(registry=reg, platform_version="v", clock=lambda: NOW)
    names = reg.registered_names()
    diag.report()
    assert reg.registered_names() == names


@pytest.mark.parametrize(
    "key",
    [
        "platform_version",
        "platform_status",
        "observed_at",
        "registered_components",
        "missing_dependencies",
        "components",
        "workflow_readiness",
        "all_workflows_ready",
        "dependency_graph",
        "component_versions",
    ],
)
def test_health_payload_keys(key):
    health = make_platform().health_status()
    assert key in health
