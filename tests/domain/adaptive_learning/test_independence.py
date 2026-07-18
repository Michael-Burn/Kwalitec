"""Framework independence for adaptive learning domain."""

from __future__ import annotations

import ast
from pathlib import Path

FORBIDDEN = (
    "flask",
    "sqlalchemy",
    "app.extensions",
    "app.models",
    "app.services",
    "app.application",
)


def test_domain_modules_have_no_forbidden_imports():
    root = Path("app/domain/adaptive_learning")
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


def test_domain_does_not_import_flask_or_sqlalchemy():
    root = Path("app/domain/adaptive_learning")
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "flask" not in text.lower() or "flask" not in [
            n.split()[1] if len(n.split()) > 1 else ""
            for n in text.splitlines()
            if n.strip().startswith("import ") or n.strip().startswith("from ")
        ]
        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith("flask")
                    assert not alias.name.startswith("sqlalchemy")
            elif isinstance(node, ast.ImportFrom) and node.module:
                assert not node.module.startswith("flask")
                assert not node.module.startswith("sqlalchemy")


def test_expected_domain_modules_exist():
    root = Path("app/domain/adaptive_learning")
    expected = {
        "adaptive_decision.py",
        "decision_explanation.py",
        "decision_snapshot.py",
        "educational_roi.py",
        "intervention.py",
        "intervention_priority.py",
        "intervention_type.py",
        "revision_candidate.py",
        "revision_plan.py",
        "revision_window.py",
        "__init__.py",
    }
    present = {p.name for p in root.glob("*.py")}
    assert expected <= present
