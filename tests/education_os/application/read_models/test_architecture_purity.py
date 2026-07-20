"""Architecture purity tests for application read models (WEB-003)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4] / "src" / "application" / "read_models"
)

FORBIDDEN_MODULES = frozenset(
    {
        "flask",
        "sqlalchemy",
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
    "sqlalchemy.",
    "infrastructure.",
    "app.",
    "domain.",
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

EXPECTED_LAYOUT = {
    PACKAGE_ROOT / "__init__.py",
    PACKAGE_ROOT / "serialization.py",
    PACKAGE_ROOT / "dashboard" / "__init__.py",
    PACKAGE_ROOT / "dashboard" / "dashboard_read_model.py",
    PACKAGE_ROOT / "dashboard" / "projection_builder.py",
    PACKAGE_ROOT / "today" / "__init__.py",
    PACKAGE_ROOT / "today" / "todays_mission_read_model.py",
    PACKAGE_ROOT / "today" / "projection_builder.py",
    PACKAGE_ROOT / "missions" / "__init__.py",
    PACKAGE_ROOT / "missions" / "mission_task_read_model.py",
    PACKAGE_ROOT / "missions" / "projection_builder.py",
    PACKAGE_ROOT / "recommendations" / "__init__.py",
    PACKAGE_ROOT / "recommendations" / "recommendation_read_model.py",
    PACKAGE_ROOT / "recommendations" / "projection_builder.py",
    PACKAGE_ROOT / "progress" / "__init__.py",
    PACKAGE_ROOT / "progress" / "progress_summary_read_model.py",
    PACKAGE_ROOT / "progress" / "projection_builder.py",
    PACKAGE_ROOT / "timeline" / "__init__.py",
    PACKAGE_ROOT / "timeline" / "timeline_read_model.py",
    PACKAGE_ROOT / "timeline" / "projection_builder.py",
}

EXPECTED_DIRECTORIES = (
    "dashboard",
    "today",
    "missions",
    "recommendations",
    "progress",
    "timeline",
)


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
    for name in EXPECTED_DIRECTORIES:
        assert (PACKAGE_ROOT / name).is_dir(), f"missing directory {name}"
    for path in EXPECTED_LAYOUT:
        assert path.is_file(), f"missing {path.relative_to(PACKAGE_ROOT.parent)}"


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
def test_no_persistence_implementations(path: Path) -> None:
    source = path.read_text(encoding="utf-8").lower()
    for fragment in ("create_engine", "sessionmaker", "sqlite3.connect", "psycopg"):
        assert fragment not in source, f"{path.name} contains persistence code"


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


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_aggregate_mutation_apis(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    for fragment in (".save(", ".commit(", ".delete(", "session.add"):
        assert fragment not in source, f"{path.name} mutates persistence ({fragment})"


def test_required_read_models_exported() -> None:
    from application.read_models import (
        DashboardReadModel,
        ProgressSummaryReadModel,
        RecommendationReadModel,
        TimelineReadModel,
        TodaysMissionReadModel,
    )

    assert DashboardReadModel is not None
    assert TodaysMissionReadModel is not None
    assert ProgressSummaryReadModel is not None
    assert RecommendationReadModel is not None
    assert TimelineReadModel is not None
