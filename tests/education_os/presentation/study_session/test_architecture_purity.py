"""Architecture purity for Study Session Runner presentation (V3-003)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4] / "src" / "presentation" / "study_session"
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
        "openai",
        "anthropic",
        "pydantic",
        "marshmallow",
    }
)

FORBIDDEN_PREFIXES = (
    "flask.",
    "sqlalchemy.",
    "infrastructure.",
    "web.",
    "app.",
    "openai.",
    "anthropic.",
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
        "generate_mission",
        "generate_recommendations",
        "rewrite_mission",
        "change_recommendation",
        "mutate_recommendation",
        "orchestrate",
        "persist",
        "save",
        "commit",
    }
)

EXPECTED_FILES = {
    PACKAGE_ROOT / "__init__.py",
    PACKAGE_ROOT / "session_view_model.py",
    PACKAGE_ROOT / "session_presenter.py",
    PACKAGE_ROOT / "session_timeline.py",
    PACKAGE_ROOT / "resource_mapper.py",
    PACKAGE_ROOT / "completion_mapper.py",
}

DESIGN_SYSTEM_IMPORT_PREFIX = "presentation.design_system"


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
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
    }


def test_package_layout() -> None:
    assert PACKAGE_ROOT.is_dir()
    for path in EXPECTED_FILES:
        assert path.is_file(), f"missing {path.name}"


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
def test_no_persistence_or_ai_code(path: Path) -> None:
    source = path.read_text(encoding="utf-8").lower()
    for fragment in (
        "create_engine",
        "sessionmaker",
        "sqlite3.connect",
        "psycopg",
        "openai",
        "anthropic",
        ".commit(",
        "session.add",
    ):
        assert fragment not in source, f"{path.name} contains {fragment}"


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


def test_presenter_consumes_pipeline_and_workspace_only() -> None:
    """Public present() accepts pipeline/workspace; package must not import engines."""
    sources = [
        (PACKAGE_ROOT / name).read_text(encoding="utf-8")
        for name in (
            "session_presenter.py",
            "session_timeline.py",
            "resource_mapper.py",
            "completion_mapper.py",
        )
    ]
    for source in sources:
        assert "MissionGenerator" not in source
        assert "StudyPlanner" not in source
        assert "ProgressEvaluator" not in source
        assert "RecommendationGenerator" not in source
        assert "EducationalPipeline" not in source
        assert "ExperienceGenerator" not in source


def test_package_uses_design_system() -> None:
    """Runner chrome must compose Design System contracts."""
    found = False
    for path in _iter_python_files():
        imported = _imported_modules(path)
        if any(
            name == DESIGN_SYSTEM_IMPORT_PREFIX
            or name.startswith(f"{DESIGN_SYSTEM_IMPORT_PREFIX}.")
            for name in imported
        ):
            found = True
            break
    assert found, "study_session must import presentation.design_system"


def test_public_exports() -> None:
    from presentation.study_session import (
        CompletionMapper,
        ResourceMapper,
        SessionPresenter,
        SessionTimeline,
        StudySessionViewModel,
    )

    assert SessionPresenter is not None
    assert SessionTimeline is not None
    assert ResourceMapper is not None
    assert CompletionMapper is not None
    assert StudySessionViewModel is not None
