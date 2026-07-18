"""Framework independence for Student Experience application."""

from __future__ import annotations

import ast
from pathlib import Path

APP_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "application"
    / "student_experience"
)
DOMAIN_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "domain"
    / "student_experience"
)

FORBIDDEN_MODULES = (
    "flask",
    "sqlalchemy",
    "app.extensions",
    "app.models",
    "app.services",
    "app.curriculum",
    "app.infrastructure",
    "app.application.student_twin",
    "app.application.adaptive_learning",
    "app.application.learning_orchestrator",
    "app.application.learning_journey",
    "app.application.mission_engine",
    "app.application.mission_engine_v2",
    "app.application.mission_adapter",
    "app.application.education_platform",
    "app.domain.student_twin",
    "app.domain.adaptive_learning",
    "app.domain.learning_orchestrator",
    "app.domain.learning_journey",
    "app.domain.mission",
)


def _offenders(root: Path) -> list[str]:
    found: list[str] = []
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if any(
                        alias.name == f or alias.name.startswith(f + ".")
                        for f in FORBIDDEN_MODULES
                    ):
                        found.append(f"{path}: import {alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                if any(
                    node.module == f or node.module.startswith(f + ".")
                    for f in FORBIDDEN_MODULES
                ):
                    found.append(f"{path}: from {node.module}")
    return found


def test_application_no_forbidden_imports():
    assert _offenders(APP_ROOT) == []


def test_domain_no_forbidden_imports():
    # Domain must not import application either
    forbidden = FORBIDDEN_MODULES + ("app.application",)
    found: list[str] = []
    for path in DOMAIN_ROOT.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                if any(
                    node.module == f or node.module.startswith(f + ".")
                    for f in forbidden
                ):
                    found.append(f"{path}: from {node.module}")
    assert found == []


def test_ports_are_protocols_only():
    ports = APP_ROOT / "ports"
    for path in ports.glob("*_port.py"):
        text = path.read_text(encoding="utf-8")
        assert "Protocol" in text
        assert "import app.application.student_twin" not in text


def test_no_flask_sqlalchemy_literals():
    for path in APP_ROOT.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith("flask")
                    assert not alias.name.startswith("sqlalchemy")
