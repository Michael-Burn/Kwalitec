"""Architecture purity tests for the web layer (WEB-001)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = Path(__file__).resolve().parents[3] / "src" / "web"

FORBIDDEN_MODULES = frozenset(
    {
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
    "sqlalchemy.",
    "app.",
    "app.models",
    "app.services",
    "app.domain",
)

# Blueprint packages must not import domain or persistence layers.
BLUEPRINT_FORBIDDEN_MODULES = frozenset({"domain", "sqlalchemy"})
BLUEPRINT_FORBIDDEN_PREFIXES = (
    "domain.",
    "sqlalchemy.",
    "infrastructure.persistence",
    "infrastructure.repositories",
    "application.ports.repositories",
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
    PACKAGE_ROOT / "app.py",
    PACKAGE_ROOT / "lifecycle.py",
    PACKAGE_ROOT / "errors.py",
    PACKAGE_ROOT / "middleware.py",
    PACKAGE_ROOT / "blueprints" / "__init__.py",
    PACKAGE_ROOT / "blueprints" / "learning" / "__init__.py",
    PACKAGE_ROOT / "blueprints" / "learning" / "routes.py",
    PACKAGE_ROOT / "blueprints" / "learning" / "schemas.py",
    PACKAGE_ROOT / "blueprints" / "dashboard" / "__init__.py",
    PACKAGE_ROOT / "blueprints" / "dashboard" / "routes.py",
    PACKAGE_ROOT / "blueprints" / "dashboard" / "schemas.py",
}

BLUEPRINTS_ROOT = PACKAGE_ROOT / "blueprints"


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
    for path in EXPECTED_LAYOUT:
        assert path.is_file(), f"missing {path.relative_to(PACKAGE_ROOT.parent)}"


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_forbidden_infrastructure_imports(path: Path) -> None:
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


def _iter_blueprint_files() -> list[Path]:
    if not BLUEPRINTS_ROOT.is_dir():
        return []
    return sorted(BLUEPRINTS_ROOT.rglob("*.py"))


@pytest.mark.parametrize(
    "path",
    _iter_blueprint_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_blueprints_forbid_domain_and_persistence_imports(path: Path) -> None:
    imported = _imported_modules(path)
    for name in imported:
        assert name not in BLUEPRINT_FORBIDDEN_MODULES, f"{path.name} imports {name}"
        assert not any(
            name == prefix.rstrip(".") or name.startswith(prefix)
            for prefix in BLUEPRINT_FORBIDDEN_PREFIXES
        ), f"{path.name} imports forbidden module {name}"


@pytest.mark.parametrize(
    "relative_path",
    (
        "blueprints/learning/routes.py",
        "blueprints/dashboard/routes.py",
    ),
)
def test_route_handlers_stay_thin(relative_path: str) -> None:
    routes = PACKAGE_ROOT / relative_path
    tree = ast.parse(routes.read_text(encoding="utf-8"), filename=str(routes))
    for node in tree.body:
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            line_count = node.end_lineno - node.lineno + 1  # type: ignore[operator]
            assert line_count <= 30, f"{node.name} is {line_count} lines (max 30)"
