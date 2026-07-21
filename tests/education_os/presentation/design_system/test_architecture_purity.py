"""Architecture purity for the V3 design system (V3-002)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4] / "src" / "presentation" / "design_system"
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
        "bootstrap",
    }
)

FORBIDDEN_PREFIXES = (
    "flask.",
    "sqlalchemy.",
    "infrastructure.",
    "web.",
    "app.",
    "domain.",
    "application.",
    "openai.",
    "anthropic.",
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
    }
)

EXPECTED_TOKEN_FILES = {
    PACKAGE_ROOT / "design_tokens.py",
    PACKAGE_ROOT / "typography.py",
    PACKAGE_ROOT / "spacing.py",
    PACKAGE_ROOT / "colours.py",
    PACKAGE_ROOT / "elevation.py",
    PACKAGE_ROOT / "radius.py",
    PACKAGE_ROOT / "icons.py",
    PACKAGE_ROOT / "motion.py",
    PACKAGE_ROOT / "layout.py",
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
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
    }


def test_package_layout() -> None:
    assert PACKAGE_ROOT.is_dir()
    for path in EXPECTED_TOKEN_FILES:
        assert path.is_file(), f"missing {path.name}"
    assert (PACKAGE_ROOT / "components").is_dir()


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
def test_no_persistence_or_ai_or_flask_styling(path: Path) -> None:
    source = path.read_text(encoding="utf-8").lower()
    for fragment in (
        "create_engine",
        "sessionmaker",
        "sqlite3.connect",
        "psycopg",
        "import openai",
        "import anthropic",
        "import flask",
        "from flask",
        "import jinja2",
        "from jinja2",
        "bootstrap",
        "render_template",
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


def test_public_exports() -> None:
    from presentation.design_system import (
        DESKTOP_GRID,
        MOBILE_GRID,
        TABLET_GRID,
        TOKENS,
        Button,
        MissionCard,
        get_tokens,
        primary_button,
    )

    assert get_tokens() is TOKENS
    assert primary_button("Go").label == "Go"
    assert isinstance(Button, type)
    assert MissionCard is not None
    assert MOBILE_GRID.columns == 4
    assert TABLET_GRID.columns == 8
    assert DESKTOP_GRID.columns == 12


def test_imports_stay_within_presentation_design_system() -> None:
    for path in _iter_python_files():
        for name in _imported_modules(path):
            if name.startswith("presentation."):
                assert name.startswith(
                    "presentation.design_system"
                ), f"{path.name} imports {name}"
