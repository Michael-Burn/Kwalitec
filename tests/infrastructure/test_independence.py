"""Framework isolation — application/domain must not import infrastructure."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
APP_ROOT = ROOT / "app" / "application"
DOMAIN_ROOT = ROOT / "app" / "domain"
INFRA_ROOT = ROOT / "app" / "infrastructure"

FORBIDDEN_IN_APP_DOMAIN = ("app.infrastructure",)


def _offenders(root: Path, forbidden: tuple[str, ...]) -> list[str]:
    found: list[str] = []
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if any(
                        alias.name == f or alias.name.startswith(f + ".")
                        for f in forbidden
                    ):
                        found.append(f"{path}: import {alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                if any(
                    node.module == f or node.module.startswith(f + ".")
                    for f in forbidden
                ):
                    found.append(f"{path}: from {node.module}")
    return found


def test_application_does_not_import_infrastructure():
    assert _offenders(APP_ROOT, FORBIDDEN_IN_APP_DOMAIN) == []


def test_domain_does_not_import_infrastructure():
    assert _offenders(DOMAIN_ROOT, FORBIDDEN_IN_APP_DOMAIN) == []


def test_infrastructure_package_exists():
    assert (INFRA_ROOT / "__init__.py").is_file()
    for name in (
        "adapters",
        "persistence",
        "events",
        "repositories",
        "diagnostics",
    ):
        assert (INFRA_ROOT / name).is_dir()


@pytest.mark.parametrize(
    "adapter_pkg",
    [
        "curriculum_management",
        "curriculum_ingestion",
        "education_platform",
        "student_twin",
        "adaptive_learning",
        "mission",
        "learning_orchestrator",
    ],
)
def test_adapter_packages_present(adapter_pkg):
    path = INFRA_ROOT / "adapters" / adapter_pkg / "adapter.py"
    assert path.is_file()


FORBIDDEN_DOMAIN_MATH_IN_INFRA_REPOS = (
    "MasteryCalculator",
    "RetentionEstimator",
    "ReadinessEstimator",
    "InterventionSelector",
    "RevisionPlanner",
)


@pytest.mark.parametrize(
    "token",
    FORBIDDEN_DOMAIN_MATH_IN_INFRA_REPOS,
)
def test_infra_repos_do_not_call_domain_math_classes(token):
    offenders = []
    for path in (INFRA_ROOT / "repositories").rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if token in text:
            offenders.append(str(path))
    for path in (INFRA_ROOT / "persistence").rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if token in text:
            offenders.append(str(path))
    assert offenders == []
