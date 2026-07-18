"""Framework independence tests for curriculum management domain."""

from __future__ import annotations

import ast
from pathlib import Path

FORBIDDEN = (
    "flask",
    "sqlalchemy",
    "app.extensions",
    "app.models",
    "app.application.education_platform",
    "app.application.instructional_blueprint",
    "app.application.learning_journey",
    "app.application.learning_activity",
    "app.application.learning_session",
    "app.application.mission_engine",
    "app.application.mission_engine_v2",
    "app.application.mission_adapter",
)


def test_domain_modules_have_no_forbidden_imports():
    root = Path("app/domain/curriculum_management")
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


def test_domain_package_imports_without_flask():
    from app.domain import curriculum_management as cm

    assert cm.PublicationState.DRAFT.value == "draft"
    assert cm.SubjectIdentifier.create("CS1").code == "CS1"


def test_lazy_exports_dir():
    from app.domain import curriculum_management as cm

    names = dir(cm)
    assert "Subject" in names
    assert "PublicationState" in names
