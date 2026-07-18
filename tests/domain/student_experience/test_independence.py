"""Framework independence for Student Experience domain."""

from __future__ import annotations

import ast
from pathlib import Path

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
    "app.application",
    "app.infrastructure",
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


def test_domain_no_forbidden_imports():
    assert _offenders(DOMAIN_ROOT) == []


def test_no_flask_sqlalchemy():
    for path in DOMAIN_ROOT.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "flask" not in text.lower() or "flask" not in [
            n.name for n in ast.walk(ast.parse(text)) if isinstance(n, ast.Import)
        ]


def test_package_has_expected_modules():
    names = {p.name for p in DOMAIN_ROOT.glob("*.py")}
    for required in (
        "experience_workspace.py",
        "experience_session.py",
        "experience_snapshot.py",
        "student_home.py",
        "journey_projection.py",
        "revision_projection.py",
        "history_projection.py",
        "profile_projection.py",
        "recommendation_explanation.py",
    ):
        assert required in names
