"""Architecture purity for Student Onboarding presentation (BR-002)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4] / "src" / "presentation" / "onboarding"
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
    "adapters.",
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
        "save",
        "commit",
    }
)

EXPECTED_FILES = {
    PACKAGE_ROOT / "__init__.py",
    PACKAGE_ROOT / "onboarding_view_model.py",
    PACKAGE_ROOT / "onboarding_presenter.py",
    PACKAGE_ROOT / "onboarding_mapper.py",
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


@pytest.mark.parametrize("path", _iter_python_files(), ids=lambda p: p.name)
def test_no_educational_methods(path: Path) -> None:
    banned = _defined_methods(path) & FORBIDDEN_METHOD_NAMES
    assert not banned


@pytest.mark.parametrize("path", _iter_python_files(), ids=lambda p: p.name)
def test_future_annotations(path: Path) -> None:
    assert "from __future__ import annotations" in path.read_text(encoding="utf-8")


def test_view_models_are_frozen() -> None:
    from presentation.onboarding import OnboardingViewModel

    assert OnboardingViewModel.__dataclass_params__.frozen  # type: ignore[attr-defined]
