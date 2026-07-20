"""Framework independence for Learning Session Experience domain."""

from __future__ import annotations

import ast
from pathlib import Path

DOMAIN_ROOT = (
    Path(__file__).resolve().parents[3] / "app" / "domain" / "session_experience"
)

FORBIDDEN_MODULES = (
    "flask",
    "sqlalchemy",
    "app.extensions",
    "app.models",
    "app.services",
    "app.curriculum",
    "app.application",
    "app.infrastructure",
    "app.domain.student_twin",
    "app.domain.adaptive_learning",
    "app.domain.learning_orchestrator",
    "app.domain.learning_journey",
    "app.domain.mission",
    "app.application.learning_session",
    "app.application.learning_activity",
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


def test_domain_no_forbidden_imports():
    assert _offenders(DOMAIN_ROOT) == []


def test_package_has_expected_modules():
    names = {p.name for p in DOMAIN_ROOT.glob("*.py")}
    for required in (
        "learning_session.py",
        "session_workspace.py",
        "session_progress.py",
        "activity_projection.py",
        "reflection_projection.py",
        "completion_projection.py",
        "session_navigation.py",
    ):
        assert required in names


def test_no_flask_sqlalchemy_strings_as_imports():
    offenders = _offenders(DOMAIN_ROOT)
    assert not any("flask" in o.lower() for o in offenders)
    assert not any("sqlalchemy" in o.lower() for o in offenders)
