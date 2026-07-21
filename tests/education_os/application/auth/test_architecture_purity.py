"""Architecture purity for Production Authentication application layer (BR-001)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = Path(__file__).resolve().parents[4] / "src" / "application" / "auth"

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
        "argon2",
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
    "presentation.",
    "argon2.",
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
        "create_twin",
        "create_student_twin",
        "onboard",
        "orchestrate",
    }
)

EXPECTED_FILES = {
    PACKAGE_ROOT / "__init__.py",
    PACKAGE_ROOT / "auth_service.py",
    PACKAGE_ROOT / "errors.py",
    PACKAGE_ROOT / "ports.py",
    PACKAGE_ROOT / "requests.py",
    PACKAGE_ROOT / "results.py",
    PACKAGE_ROOT / "security.py",
    PACKAGE_ROOT / "memory.py",
}

ALLOWED_APPLICATION_PREFIXES = (
    "application.auth",
    "application.errors",
)

ALLOWED_DOMAIN_PREFIXES = ("domain.auth",)


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


@pytest.mark.parametrize("path", _iter_python_files(), ids=lambda p: p.name)
def test_future_annotations(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    assert "from __future__ import annotations" in source


@pytest.mark.parametrize("path", _iter_python_files(), ids=lambda p: p.name)
def test_no_forbidden_imports(path: Path) -> None:
    imports = _imported_modules(path)
    for name in imports:
        root = name.split(".", 1)[0]
        assert root not in FORBIDDEN_MODULES and name not in FORBIDDEN_MODULES, name
        assert not any(name == p or name.startswith(p) for p in FORBIDDEN_PREFIXES), name


@pytest.mark.parametrize("path", _iter_python_files(), ids=lambda p: p.name)
def test_import_allowlist(path: Path) -> None:
    for name in _imported_modules(path):
        if name.startswith("application."):
            assert any(
                name == p or name.startswith(p + ".")
                for p in ALLOWED_APPLICATION_PREFIXES
            ), name
        if name.startswith("domain."):
            assert any(
                name == p or name.startswith(p + ".") for p in ALLOWED_DOMAIN_PREFIXES
            ), name


@pytest.mark.parametrize("path", _iter_python_files(), ids=lambda p: p.name)
def test_no_educational_methods(path: Path) -> None:
    methods = _defined_methods(path)
    banned = methods & FORBIDDEN_METHOD_NAMES
    assert not banned
