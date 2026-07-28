"""Telemetry aggregation and purity guards (RI-001)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.runtime_integration.dto import (
    FallbackReason,
    IntegrationSurface,
)
from app.application.runtime_integration.telemetry import RuntimeIntegrationTelemetry


def test_telemetry_aggregates_fallback_and_adoption() -> None:
    telemetry = RuntimeIntegrationTelemetry()
    telemetry.record_fallback(
        student_id=1,
        subject="CS1",
        reason=FallbackReason.NO_ACTIVE_SCI,
        surface=IntegrationSurface.DASHBOARD,
        missing_prerequisite="active_student_curriculum_instance",
    )
    telemetry.record_educational_intelligence(
        student_id=2,
        subject="CS1",
        surface=IntegrationSurface.RECOMMENDATION,
        instance_id="sci-2",
        decision_id="ere-1",
    )
    telemetry.record_educational_intelligence(
        student_id=2,
        subject="CS1",
        surface=IntegrationSurface.COACH,
        instance_id="sci-2",
        decision_id="ere-1",
    )
    snap = telemetry.snapshot()
    assert snap.total_requests == 3
    assert snap.fallback_count == 1
    assert snap.educational_intelligence_count == 2
    assert snap.fallback_rate == pytest.approx(1 / 3)
    assert snap.educational_intelligence_adoption_pct == pytest.approx(200 / 3)
    assert telemetry.migrated_user_count() == 1
    assert snap.fallback_by_reason[FallbackReason.NO_ACTIVE_SCI.value] == 1


def test_runtime_integration_flag_defaults_on() -> None:
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_RUNTIME_INTEGRATION is True


def test_runtime_integration_flag_can_disable() -> None:
    flags = resolve_v2_feature_flags(environ={"KWALITEC_RUNTIME_INTEGRATION": "0"})
    assert flags.ENABLE_RUNTIME_INTEGRATION is False


def test_runtime_integration_service_avoids_flask_request() -> None:
    path = Path("app/application/runtime_integration/service.py")
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    forbidden = {"flask", "flask.request", "flask.session"}
    assert not forbidden.intersection(imports)


def test_runtime_integration_does_not_import_reasoning_engine() -> None:
    """Controllers/adapters must not embed EI-007 reasoning — query only."""
    root = Path("app/application/runtime_integration")
    forbidden_modules = {
        "app.domain.educational_reasoning_engine.engine",
        "app.domain.educational_reasoning_engine.rules",
        "app.application.educational_reasoning_engine.reasoning_service",
    }
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)
        assert not forbidden_modules.intersection(imports), path


def test_dashboard_routes_do_not_import_reasoning_engine() -> None:
    path = Path("app/dashboard/routes.py")
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    forbidden = {
        "app.domain.educational_reasoning_engine.engine",
        "app.domain.educational_reasoning_engine.rules",
        "app.application.educational_reasoning_engine.reasoning_service",
    }
    assert not forbidden.intersection(imports)
