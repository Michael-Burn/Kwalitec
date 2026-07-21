"""Architecture purity for Student Twin Initialization (BR-003)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4]
    / "src"
    / "application"
    / "student_initialization"
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
    "presentation.",
    "adapters.",
)

FORBIDDEN_METHOD_NAMES = frozenset(
    {
        "recommend",
        "generate_recommendations",
        "rewrite_mission",
        "change_recommendation",
        "mutate_recommendation",
        "plan_study",
    }
)

EXPECTED_FILES = {
    PACKAGE_ROOT / "__init__.py",
    PACKAGE_ROOT / "errors.py",
    PACKAGE_ROOT / "ports.py",
    PACKAGE_ROOT / "results.py",
    PACKAGE_ROOT / "twin_builder.py",
    PACKAGE_ROOT / "evidence_seeder.py",
    PACKAGE_ROOT / "availability_mapper.py",
    PACKAGE_ROOT / "session_context_factory.py",
    PACKAGE_ROOT / "student_initialization_service.py",
    PACKAGE_ROOT / "onboarding_adapter.py",
}

ALLOWED_APPLICATION_PREFIXES = (
    "application.student_initialization",
    "application.onboarding",
    "application.pipeline",
    "application.errors",
    "application.events",
    "application.ports",
)

ALLOWED_DOMAIN_PREFIXES = (
    "domain.education",
    "domain.study_planning",
    "domain.onboarding",
    "domain.mission_generation",
    "domain.progress_evaluation",
    "domain.recommendation",
    "domain.student_experience",
    "domain.explainability",
)


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
def test_imports_stay_within_allowed_boundaries(path: Path) -> None:
    for name in _imported_modules(path):
        if name.startswith("application."):
            assert any(
                name == prefix or name.startswith(prefix + ".")
                for prefix in ALLOWED_APPLICATION_PREFIXES
            ), f"{path.name} imports unexpected application module {name}"
        if name.startswith("domain."):
            assert any(
                name == prefix or name.startswith(prefix + ".")
                for prefix in ALLOWED_DOMAIN_PREFIXES
            ), f"{path.name} imports unexpected domain module {name}"


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_ai_or_framework_code(path: Path) -> None:
    source = path.read_text(encoding="utf-8").lower()
    for fragment in (
        "create_engine",
        "sessionmaker",
        "sqlite3.connect",
        "psycopg",
        "openai",
        "anthropic",
        "datetime.now",
        "time.time",
        "<html",
        "jinja",
    ):
        assert fragment not in source, f"{path.name} contains {fragment}"


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_recommendation_methods_outside_pipeline(path: Path) -> None:
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


def test_recommendations_only_via_pipeline_result() -> None:
    service_source = (
        PACKAGE_ROOT / "student_initialization_service.py"
    ).read_text(encoding="utf-8")
    assert "RecommendationGenerator" not in service_source
    assert "MissionGenerator" not in service_source
    assert "EducationalPipeline" in service_source or "pipeline" in service_source


def test_public_exports() -> None:
    from application.student_initialization import (
        InitialEvidence,
        InitializationResult,
        StudentInitializationService,
        StudentTwin,
        StudentTwinInitializerAdapter,
    )

    assert StudentInitializationService is not None
    assert InitializationResult is not None
    assert InitialEvidence is not None
    assert StudentTwin is not None
    assert StudentTwinInitializerAdapter is not None
