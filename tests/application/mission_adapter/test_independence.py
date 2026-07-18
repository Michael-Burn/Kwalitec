"""Framework independence and dependency isolation tests."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

FORBIDDEN_MODULES = (
    "flask",
    "sqlalchemy",
    "app.extensions",
    "app.models",
    "app.services.mission_service",
    "app.application.mission_engine.engine",
)


def test_mission_adapter_modules_have_no_forbidden_imports():
    root = Path("app/application/mission_adapter")
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if any(
                        alias.name == f or alias.name.startswith(f + ".")
                        for f in FORBIDDEN_MODULES
                    ):
                        offenders.append(f"{path}: import {alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                if any(
                    node.module == f or node.module.startswith(f + ".")
                    for f in FORBIDDEN_MODULES
                ):
                    offenders.append(f"{path}: from {node.module}")
    assert offenders == []


def test_import_adapter_without_app_context():
    from app.application.mission_adapter.adapter import MissionAdapter

    adapter = MissionAdapter.create()
    assert adapter.health_status()["invocations"] == 0


def test_no_mission_engine_instantiation_in_adapter_source():
    text = Path("app/application/mission_adapter/adapter.py").read_text(
        encoding="utf-8"
    )
    assert "MissionEngine(" not in text
    assert "MissionService(" not in text


def test_no_flask_sqlalchemy_imports_in_package_source():
    root = Path("app/application/mission_adapter")
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith("flask")
                    assert not alias.name.startswith("sqlalchemy")
            elif isinstance(node, ast.ImportFrom) and node.module:
                assert not node.module.startswith("flask")
                assert not node.module.startswith("sqlalchemy")


def test_contracts_are_protocol_only():
    from app.application.mission_adapter.contracts import MissionEnginePort

    assert hasattr(MissionEnginePort, "generate_mission")
    assert hasattr(MissionEnginePort, "is_available")


def test_adapter_does_not_import_v1_mission_adapter():
    """Mission Adapter layer is separate from Mission Engine's V1MissionAdapter."""
    root = Path("app/application/mission_adapter")
    for path in root.rglob("*.py"):
        content = path.read_text(encoding="utf-8")
        assert "V1MissionAdapter" not in content
        assert "mission_engine.adapters" not in content


def test_exceptions_hierarchy():
    from app.application.mission_adapter.exceptions import (
        AuditFailure,
        ComparisonFailure,
        EngineUnavailable,
        MigrationStateError,
        MissionAdapterError,
        RoutingError,
    )

    for cls in (
        RoutingError,
        ComparisonFailure,
        MigrationStateError,
        EngineUnavailable,
        AuditFailure,
    ):
        assert issubclass(cls, MissionAdapterError)


@pytest.mark.parametrize(
    "name",
    [
        "MissionAdapterError",
        "RoutingError",
        "ComparisonFailure",
        "MigrationStateError",
        "EngineUnavailable",
        "AuditFailure",
    ],
)
def test_exception_exports(name):
    import app.application.mission_adapter as pkg

    assert hasattr(pkg, name)


def test_regression_mission_engine_untouched():
    """Existing Mission Engine 2.0 package still imports cleanly."""
    from app.application.mission_engine.engine import MissionEngine

    engine = MissionEngine()
    assert engine.all_missions() == ()
