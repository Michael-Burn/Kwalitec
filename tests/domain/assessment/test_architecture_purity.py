"""Architecture purity for assessment domain package."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

DOMAIN_ROOT = (
    Path(__file__).resolve().parents[3] / "src" / "domain" / "assessment"
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
    }
)
FORBIDDEN_PREFIXES = (
    "flask.",
    "sqlalchemy.",
    "app.",
    "infrastructure.",
    "application.",
)


def _iter_python_files() -> list[Path]:
    return sorted(DOMAIN_ROOT.rglob("*.py"))


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


def test_assessment_domain_package_exists() -> None:
    assert DOMAIN_ROOT.is_dir()
    for expected in (
        "entities",
        "value_objects",
        "enums",
        "factories",
        "validation",
        "exceptions",
        "events",
    ):
        assert (DOMAIN_ROOT / expected).is_dir()


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(DOMAIN_ROOT)),
)
def test_no_forbidden_imports(path: Path) -> None:
    imported = _imported_modules(path)
    for name in imported:
        assert name not in FORBIDDEN_MODULES, f"{path} imports {name}"
        assert not any(
            name == prefix.rstrip(".") or name.startswith(prefix)
            for prefix in FORBIDDEN_PREFIXES
        ), f"{path} imports {name}"
