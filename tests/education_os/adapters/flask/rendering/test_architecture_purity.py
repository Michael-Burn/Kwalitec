"""Architecture purity for the Design System renderer (V4-003)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[5] / "src" / "adapters" / "flask" / "rendering"
)

FORBIDDEN_MODULES = frozenset(
    {
        "flask",
        "sqlalchemy",
        "alembic",
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
    "alembic.",
    "openai.",
    "anthropic.",
    "app.models",
    "app.services",
    "domain.",
    "infrastructure.persistence",
    "infrastructure.ai",
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
        "orchestrate",
        "persist",
        "commit",
    }
)

EXPECTED_MODULES = {
    PACKAGE_ROOT / "__init__.py",
    PACKAGE_ROOT / "html_helpers.py",
    PACKAGE_ROOT / "token_renderer.py",
    PACKAGE_ROOT / "style_renderer.py",
    PACKAGE_ROOT / "accessibility_renderer.py",
    PACKAGE_ROOT / "component_renderer.py",
}

EXPECTED_TEMPLATES = {
    PACKAGE_ROOT / "templates" / "components" / "page_header.html",
    PACKAGE_ROOT / "templates" / "components" / "mission_card.html",
    PACKAGE_ROOT / "templates" / "components" / "section.html",
    PACKAGE_ROOT / "templates" / "components" / "progress_bar.html",
    PACKAGE_ROOT / "templates" / "components" / "badge.html",
    PACKAGE_ROOT / "templates" / "components" / "timeline.html",
    PACKAGE_ROOT / "templates" / "components" / "primary_button.html",
    PACKAGE_ROOT / "templates" / "components" / "secondary_button.html",
    PACKAGE_ROOT / "templates" / "components" / "achievement_card.html",
    PACKAGE_ROOT / "templates" / "components" / "statistic_card.html",
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
    for path in EXPECTED_MODULES:
        assert path.is_file(), f"missing {path.name}"
    for path in EXPECTED_TEMPLATES:
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
def test_no_educational_intelligence_methods(path: Path) -> None:
    methods = _defined_methods(path)
    for forbidden in FORBIDDEN_METHOD_NAMES:
        assert forbidden not in methods, f"{path.name} defines {forbidden}"


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
        "session.add",
        "uow.commit",
        "from flask",
        "import flask",
    ):
        assert fragment not in source, f"{path.name} contains {fragment}"


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
    from adapters.flask.rendering import (
        AccessibilityRenderer,
        ComponentRenderer,
        StyleRenderer,
        TokenRenderer,
    )

    assert ComponentRenderer is not None
    assert StyleRenderer is not None
    assert TokenRenderer is not None
    assert AccessibilityRenderer is not None


def test_templates_contain_no_educational_logic() -> None:
    forbidden = (
        "mastery",
        "diagnose",
        "recommendation_engine",
        "digital_twin",
        "openai",
        "sqlalchemy",
    )
    for path in EXPECTED_TEMPLATES:
        source = path.read_text(encoding="utf-8").lower()
        for fragment in forbidden:
            assert fragment not in source, f"{path.name} contains {fragment}"
