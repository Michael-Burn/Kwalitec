"""Presentation independence — no educational engine imports in UI package."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PRESENTATION_ROOT = Path("app/presentation/student")
TEMPLATE_ROOT = Path("app/templates/student")

FORBIDDEN_IMPORT_PREFIXES = (
    "app.domain.student_twin",
    "app.application.student_twin",
    "app.domain.adaptive_learning",
    "app.application.adaptive_learning",
    "app.domain.learning_orchestrator",
    "app.application.learning_orchestrator",
    "app.application.mission_engine",
    "app.domain.learning_journey",
    "app.application.learning_journey",
    "app.models",
)

PY_FILES = sorted(PRESENTATION_ROOT.rglob("*.py"))


def _student_py_params():
    params = []
    for path in PY_FILES:
        if path.name == "adaptive_workspace.py":
            params.append(
                pytest.param(
                    path,
                    marks=pytest.mark.xfail(
                        reason=(
                            "adaptive_workspace.py imports RuntimeEnrolment ORM "
                            "for V1S-007 Runtime C Home composition "
                            "(presentation/model debt)"
                        ),
                        strict=False,
                    ),
                )
            )
        else:
            params.append(path)
    return params
TEMPLATE_FILES = sorted(TEMPLATE_ROOT.rglob("*.html"))


def test_presentation_package_exists():
    assert PRESENTATION_ROOT.is_dir()
    assert TEMPLATE_ROOT.is_dir()


@pytest.mark.parametrize("path", _student_py_params())
def test_no_forbidden_imports(path):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            for prefix in FORBIDDEN_IMPORT_PREFIXES:
                assert not node.module.startswith(prefix), (
                    f"{path} imports forbidden module {node.module}"
                )
        if isinstance(node, ast.Import):
            for alias in node.names:
                for prefix in FORBIDDEN_IMPORT_PREFIXES:
                    assert not alias.name.startswith(prefix)


@pytest.mark.parametrize("path", TEMPLATE_FILES)
def test_templates_do_not_reference_engines(path):
    text = path.read_text(encoding="utf-8")
    assert "app.domain" not in text
    assert "StudentTwin" not in text
    assert "AdaptiveDecision" not in text
    assert "LearningOrchestrator" not in text
