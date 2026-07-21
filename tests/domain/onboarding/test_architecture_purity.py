"""Architecture purity for onboarding domain (BR-002)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = Path(__file__).resolve().parents[3] / "src" / "domain" / "onboarding"

FORBIDDEN_MODULES = frozenset(
    {
        "flask",
        "sqlalchemy",
        "alembic",
        "jinja2",
        "wtforms",
        "requests",
        "httpx",
        "openai",
        "anthropic",
    }
)

FORBIDDEN_PREFIXES = (
    "flask.",
    "sqlalchemy.",
    "infrastructure.",
    "application.",
    "web.",
    "app.",
    "presentation.",
    "adapters.",
    "domain.education.",
    "domain.auth.",
)

EXPECTED_FILES = {
    PACKAGE_ROOT / "__init__.py",
    PACKAGE_ROOT / "errors.py",
    PACKAGE_ROOT / "enums.py",
    PACKAGE_ROOT / "ids.py",
    PACKAGE_ROOT / "step_payloads.py",
    PACKAGE_ROOT / "step_policy.py",
    PACKAGE_ROOT / "onboarding_session.py",
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


def test_package_layout() -> None:
    assert PACKAGE_ROOT.is_dir()
    for path in EXPECTED_FILES:
        assert path.is_file(), f"missing {path.name}"


@pytest.mark.parametrize("path", _iter_python_files(), ids=lambda p: p.name)
def test_no_forbidden_imports(path: Path) -> None:
    for name in _imported_modules(path):
        root = name.split(".", 1)[0]
        assert root not in FORBIDDEN_MODULES, name
        assert not any(
            name == p or name.startswith(p) for p in FORBIDDEN_PREFIXES
        ), name
        if name.startswith("domain."):
            assert name == "domain.onboarding" or name.startswith(
                "domain.onboarding."
            ), name
