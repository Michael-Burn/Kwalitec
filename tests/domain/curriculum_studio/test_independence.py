"""Framework independence tests for Curriculum Studio domain."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

DOMAIN_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "domain"
    / "curriculum_studio"
)

FORBIDDEN_MODULES = (
    "flask",
    "sqlalchemy",
    "app.extensions",
    "app.models",
    "app.services",
    "app.curriculum",
    "app.application",
    "app.domain.curriculum_management",
    "app.domain.curriculum_ingestion",
    "app.domain.student_twin",
    "app.domain.adaptive_learning",
    "app.domain.learning_orchestrator",
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


@pytest.mark.parametrize(
    "module_path",
    [
        "app.domain.curriculum_studio.workflow_stage",
        "app.domain.curriculum_studio.studio_workflow",
        "app.domain.curriculum_studio.curriculum_workspace",
        "app.domain.curriculum_studio.publication_checklist",
        "app.domain.curriculum_studio.validation_summary",
        "app.domain.curriculum_studio.preview_summary",
        "app.domain.curriculum_studio.publication_summary",
        "app.domain.curriculum_studio.version_history",
        "app.domain.curriculum_studio.curriculum_diff",
    ],
)
def test_domain_modules_import_cleanly(module_path):
    import importlib

    module = importlib.import_module(module_path)
    assert module is not None


def test_package_exports():
    from app.domain import curriculum_studio as pkg

    assert pkg.WorkflowStage.SUBJECT.value == "subject"
    assert pkg.ChecklistItemCode.READY_TO_PUBLISH.value == "ready_to_publish"
