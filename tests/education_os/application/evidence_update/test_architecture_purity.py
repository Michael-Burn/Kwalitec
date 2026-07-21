"""Architecture purity for Educational Evidence Update (V3-007)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4] / "src" / "application" / "evidence_update"
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
        "orchestrate",
        "plan_study",
        "recommend",
    }
)

EXPECTED_FILES = {
    PACKAGE_ROOT / "__init__.py",
    PACKAGE_ROOT / "evidence_update_service.py",
    PACKAGE_ROOT / "evidence_update_request.py",
    PACKAGE_ROOT / "evidence_update_result.py",
    PACKAGE_ROOT / "evidence_transformer.py",
}

ALLOWED_APPLICATION_PREFIXES = (
    "application.evidence_capture",
    "application.evidence_update",
    "application.errors",
    "application.events",
    "application.ports",
)

ALLOWED_DOMAIN_PREFIXES = (
    "domain.education.evidence",
    "domain.education.foundation",
    "domain.education.digital_twin",
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
            ) or name.startswith("application.evidence_update"), (
                f"{path.name} imports unexpected application module {name}"
            )
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


def test_no_engine_or_pipeline_authority() -> None:
    sources = [path.read_text(encoding="utf-8") for path in _iter_python_files()]
    for source in sources:
        assert "MissionGenerator" not in source
        assert "StudyPlanner" not in source
        assert "ProgressEvaluator" not in source
        assert "RecommendationGenerator" not in source
        assert "EducationalPipeline" not in source
        assert "ExperienceGenerator" not in source
        assert "EducationalDiagnosis" not in source


def test_public_exports() -> None:
    from application.evidence_update import (
        EvidenceTransformer,
        EvidenceUpdateRequest,
        EvidenceUpdateResult,
        EvidenceUpdateService,
    )

    assert EvidenceUpdateService is not None
    assert EvidenceUpdateRequest is not None
    assert EvidenceUpdateResult is not None
    assert EvidenceTransformer is not None
