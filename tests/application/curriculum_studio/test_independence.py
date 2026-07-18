"""Framework independence and package isolation for Curriculum Studio."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

APP_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "application"
    / "curriculum_studio"
)
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
    "app.application.education_platform",
    "app.application.curriculum_management",
    "app.application.curriculum_ingestion",
    "app.application.student_twin",
    "app.application.adaptive_learning",
    "app.application.learning_orchestrator",
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


def test_application_no_forbidden_imports():
    assert _offenders(APP_ROOT) == []


def test_domain_no_forbidden_imports():
    assert _offenders(DOMAIN_ROOT) == []


def test_no_flask_sqlalchemy_in_application():
    for path in APP_ROOT.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith("flask")
                    assert not alias.name.startswith("sqlalchemy")
            elif isinstance(node, ast.ImportFrom) and node.module:
                assert not node.module.startswith("flask")
                assert not node.module.startswith("sqlalchemy")


def test_import_studio_without_app_context():
    from app.application.curriculum_studio.curriculum_studio_service import (
        CurriculumStudioService,
    )

    studio = CurriculumStudioService.create()
    assert studio.health()["studio_status"] == "degraded"


def test_no_concrete_engine_instantiation():
    forbidden_snippets = (
        "CurriculumManagementFacade(",
        "CurriculumIngestionEngine(",
        "EducationPlatform(",
        "LearningOrchestrator(",
        "AdaptiveDecisionEngine(",
        "TwinEngine(",
    )
    for path in APP_ROOT.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for snippet in forbidden_snippets:
            assert snippet not in text, f"{path} contains {snippet}"


@pytest.mark.parametrize(
    "module_path",
    [
        "app.application.curriculum_studio.curriculum_studio_service",
        "app.application.curriculum_studio.workflow_service",
        "app.application.curriculum_studio.publication_service",
        "app.application.curriculum_studio.preview_service",
        "app.application.curriculum_studio.validation_service",
        "app.application.curriculum_studio.version_service",
        "app.application.curriculum_studio.diff_service",
        "app.application.curriculum_studio.diagnostics",
        "app.application.curriculum_studio.ports",
    ],
)
def test_modules_import_cleanly(module_path):
    import importlib

    module = importlib.import_module(module_path)
    assert module is not None


def test_package_lazy_exports():
    from app.application import curriculum_studio as pkg

    assert pkg.CurriculumStudioService is not None
    assert pkg.PORT_NAMES == (
        "curriculum_management",
        "curriculum_ingestion",
        "education_platform",
    )
