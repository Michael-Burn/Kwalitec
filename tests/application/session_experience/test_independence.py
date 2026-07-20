"""Framework independence for Learning Session Experience application."""

from __future__ import annotations

import ast
from pathlib import Path

APP_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "application"
    / "session_experience"
)

FORBIDDEN = (
    "flask",
    "sqlalchemy",
    "app.extensions",
    "app.models",
    "app.presentation",
)


def _offenders() -> list[str]:
    found: list[str] = []
    for path in APP_ROOT.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if any(
                        alias.name == f or alias.name.startswith(f + ".")
                        for f in FORBIDDEN
                    ):
                        found.append(f"{path}: import {alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                if any(
                    node.module == f or node.module.startswith(f + ".")
                    for f in FORBIDDEN
                ):
                    found.append(f"{path}: from {node.module}")
    return found


def test_application_no_flask_sqlalchemy_presentation():
    assert _offenders() == []


def test_expected_modules_present():
    names = {p.name for p in APP_ROOT.glob("*.py")}
    for required in (
        "facade.py",
        "session_service.py",
        "activity_service.py",
        "progress_service.py",
        "reflection_service.py",
        "completion_service.py",
        "diagnostics.py",
    ):
        assert required in names


def test_dto_and_ports_packages_exist():
    assert (APP_ROOT / "dto").is_dir()
    assert (APP_ROOT / "ports").is_dir()
