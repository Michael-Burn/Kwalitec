"""Architecture purity tests for SQLAlchemy persistence models (INF-002)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[5]
    / "src"
    / "infrastructure"
    / "persistence"
    / "sqlalchemy"
)

FORBIDDEN_MODULES = frozenset(
    {
        "flask",
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
    "app.",
    "app.models",
    "app.services",
    "app.domain",
    "domain.",
    "domain",
    "application.",
    "application",
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
    PACKAGE_ROOT / "base.py",
    PACKAGE_ROOT / "session.py",
    PACKAGE_ROOT / "metadata.py",
    PACKAGE_ROOT / "models" / "__init__.py",
    PACKAGE_ROOT / "models" / "digital_twin.py",
    PACKAGE_ROOT / "models" / "learning_episode.py",
    PACKAGE_ROOT / "models" / "evidence.py",
    PACKAGE_ROOT / "models" / "subject_knowledge.py",
    PACKAGE_ROOT / "models" / "teaching_plan.py",
    PACKAGE_ROOT / "models" / "diagnosis.py",
    PACKAGE_ROOT / "models" / "hypothesis.py",
    PACKAGE_ROOT / "models" / "priority.py",
    PACKAGE_ROOT / "models" / "teaching_intention.py",
    PACKAGE_ROOT / "models" / "teaching_strategy.py",
    PACKAGE_ROOT / "models" / "decision.py",
    PACKAGE_ROOT / "models" / "orchestrator.py",
    PACKAGE_ROOT / "models" / "user_account.py",
    PACKAGE_ROOT / "models" / "auth_token.py",
    PACKAGE_ROOT / "models" / "onboarding_session.py",
    PACKAGE_ROOT / "models" / "session_checkpoint.py",
}

MODEL_FILES = sorted((PACKAGE_ROOT / "models").glob("*.py"))
MODEL_FILES = [path for path in MODEL_FILES if path.name != "__init__.py"]

# INF-002 purity covers models/session/base only — repositories are INF-003.
_INF002_ROOTS = (
    PACKAGE_ROOT / "__init__.py",
    PACKAGE_ROOT / "base.py",
    PACKAGE_ROOT / "session.py",
    PACKAGE_ROOT / "metadata.py",
)


def _iter_python_files() -> list[Path]:
    files = [path for path in _INF002_ROOTS if path.is_file()]
    models_root = PACKAGE_ROOT / "models"
    if models_root.is_dir():
        files.extend(sorted(models_root.rglob("*.py")))
    return files


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


def _class_defined_methods(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef):
                    names.add(child.name)
    return names


def _module_defined_functions(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {
        node.name
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
    }


def test_package_directory_layout() -> None:
    assert PACKAGE_ROOT.is_dir()
    for path in EXPECTED_LAYOUT:
        assert path.is_file(), f"missing {path.relative_to(PACKAGE_ROOT)}"


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
def test_no_repository_implementations(path: Path) -> None:
    source = path.read_text(encoding="utf-8").lower()
    assert "class repository" not in source
    assert "repositoryport" not in source.replace("_", "")


@pytest.mark.parametrize(
    "path",
    MODEL_FILES,
    ids=lambda p: p.name,
)
def test_models_define_no_methods(path: Path) -> None:
    methods = _class_defined_methods(path)
    assert methods == set(), f"{path.name} defines methods: {sorted(methods)}"


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_educational_intelligence_methods(path: Path) -> None:
    methods = _class_defined_methods(path) | _module_defined_functions(path)
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


def test_session_module_exposes_factory_only() -> None:
    from infrastructure.persistence.sqlalchemy import session as session_module

    assert hasattr(session_module, "create_session_factory")
    assert "Repository" not in dir(session_module)
