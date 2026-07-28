"""Architecture purity checks for Curriculum Knowledge Graph domain package."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "domain"
    / "curriculum_knowledge_graph"
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
        "networkx",
    }
)

FORBIDDEN_PREFIXES = (
    "flask.",
    "sqlalchemy.",
    "alembic.",
    "app.models",
    "app.services",
    "app.extensions",
)


def _iter_python_files() -> list[Path]:
    return sorted(PACKAGE_ROOT.rglob("*.py"))


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                found.add(node.module)
    return found


def test_package_exists() -> None:
    assert PACKAGE_ROOT.is_dir()
    assert (PACKAGE_ROOT / "__init__.py").is_file()


@pytest.mark.parametrize("path", _iter_python_files(), ids=lambda p: str(p.name))
def test_no_forbidden_imports(path: Path) -> None:
    imports = _imported_modules(path)
    for name in imports:
        root = name.split(".", 1)[0]
        if root in FORBIDDEN_MODULES or name in FORBIDDEN_MODULES:
            pytest.fail(f"{path.name} imports forbidden module {name!r}")
        for prefix in FORBIDDEN_PREFIXES:
            if name == prefix.rstrip(".") or name.startswith(prefix):
                pytest.fail(f"{path.name} imports forbidden prefix {name!r}")
