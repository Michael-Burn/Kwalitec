"""Architecture purity tests for SQLAlchemy repository adapters (INF-003)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[6]
    / "src"
    / "infrastructure"
    / "persistence"
    / "sqlalchemy"
    / "repositories"
)

FORBIDDEN_MODULES = frozenset(
    {
        "flask",
        "alembic",
        "jinja2",
        "wtforms",
        "requests",
        "httpx",
        "celery",
        "redis",
        "boto3",
        "pydantic",
        "marshmallow",
    }
)

FORBIDDEN_PREFIXES = (
    "flask.",
    "app.",
    "app.models",
    "app.services",
    "app.domain",
)

FORBIDDEN_METHOD_NAMES = frozenset(
    {
        "diagnose",
        "calculate_mastery",
        "prioritise",
        "prioritize",
        "choose_strategy",
        "select_strategy",
        "interpret_evidence",
        "create_hypothesis",
    }
)

EXPECTED_REPOSITORIES = {
    PACKAGE_ROOT / "digital_twin_repository.py",
    PACKAGE_ROOT / "learning_episode_repository.py",
    PACKAGE_ROOT / "evidence_repository.py",
    PACKAGE_ROOT / "subject_knowledge_repository.py",
    PACKAGE_ROOT / "diagnosis_repository.py",
    PACKAGE_ROOT / "hypothesis_repository.py",
    PACKAGE_ROOT / "priority_repository.py",
    PACKAGE_ROOT / "teaching_intention_repository.py",
    PACKAGE_ROOT / "teaching_strategy_repository.py",
    PACKAGE_ROOT / "decision_repository.py",
    PACKAGE_ROOT / "orchestrator_repository.py",
    PACKAGE_ROOT / "teaching_plan_repository.py",
}


def _iter_python_files() -> list[Path]:
    return sorted(PACKAGE_ROOT.rglob("*.py"))


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def _defined_methods(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            names.add(node.name)
    return names


def test_package_directory_layout() -> None:
    assert PACKAGE_ROOT.is_dir()
    for path in EXPECTED_REPOSITORIES:
        assert path.is_file(), f"missing {path.relative_to(PACKAGE_ROOT)}"


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_forbidden_imports(path: Path) -> None:
    imported = _imported_modules(path)
    for name in imported:
        assert name not in FORBIDDEN_MODULES, f"{path.name} imports {name}"
        assert not any(
            name == prefix.rstrip(".") or name.startswith(prefix)
            for prefix in FORBIDDEN_PREFIXES
        ), f"{path.name} imports forbidden module {name}"


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_educational_intelligence_methods(path: Path) -> None:
    methods = _defined_methods(path)
    for forbidden in FORBIDDEN_METHOD_NAMES:
        assert forbidden not in methods, f"{path.name} defines {forbidden}"


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_modules_use_future_annotations(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    if not source.strip():
        return
    assert "from __future__ import annotations" in source


def test_repositories_remain_thin() -> None:
    """Repository modules should not grow educational policy helpers."""
    for path in EXPECTED_REPOSITORIES:
        source = path.read_text(encoding="utf-8").lower()
        for fragment in (
            "masteryband",
            "calculate_mastery",
            "diagnose(",
            "prioritise(",
            "prioritize(",
            "select_strategy(",
            "choose_strategy(",
        ):
            assert fragment not in source, f"{path.name} contains {fragment}"
