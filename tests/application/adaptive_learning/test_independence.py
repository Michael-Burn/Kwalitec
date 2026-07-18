"""Framework independence for adaptive learning application."""

from __future__ import annotations

import ast
from pathlib import Path

FORBIDDEN = (
    "flask",
    "sqlalchemy",
    "app.extensions",
    "app.models",
    "app.services",
)


def test_application_modules_have_no_forbidden_imports():
    root = Path("app/application/adaptive_learning")
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if any(
                        alias.name == f or alias.name.startswith(f + ".")
                        for f in FORBIDDEN
                    ):
                        offenders.append(f"{path}: import {alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                if any(
                    node.module == f or node.module.startswith(f + ".")
                    for f in FORBIDDEN
                ):
                    offenders.append(f"{path}: from {node.module}")
    assert offenders == []


def test_no_flask_sqlalchemy():
    root = Path("app/application/adaptive_learning")
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


def test_expected_application_modules_exist():
    root = Path("app/application/adaptive_learning")
    expected = {
        "decision_engine.py",
        "revision_planner.py",
        "priority_calculator.py",
        "roi_estimator.py",
        "revision_scheduler.py",
        "intervention_selector.py",
        "explanation_service.py",
        "diagnostics.py",
        "exceptions.py",
        "__init__.py",
    }
    present = {p.name for p in root.glob("*.py")}
    assert expected <= present
    assert (root / "dto").is_dir()
    assert (root / "policies").is_dir()


def test_does_not_import_education_platform_or_mission():
    root = Path("app/application/adaptive_learning")
    blocked = (
        "app.application.education_platform",
        "app.application.mission_engine",
        "app.application.mission_engine_v2",
        "app.application.curriculum_management",
        "app.application.curriculum_ingestion",
    )
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                assert not any(
                    node.module == b or node.module.startswith(b + ".")
                    for b in blocked
                )
