"""Architecture purity checks for the educational foundation package."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

FOUNDATION_ROOT = (
    Path(__file__).resolve().parents[4]
    / "src"
    / "domain"
    / "education"
    / "foundation"
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
    }
)

FORBIDDEN_PREFIXES = (
    "flask.",
    "sqlalchemy.",
    "app.",
    "app.models",
    "app.services",
)


def _iter_python_files() -> list[Path]:
    return sorted(FOUNDATION_ROOT.glob("*.py"))


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


def test_foundation_package_exists() -> None:
    assert FOUNDATION_ROOT.is_dir()
    expected = {
        "__init__.py",
        "base.py",
        "errors.py",
        "result.py",
        "ids.py",
        "enums.py",
        "references.py",
    }
    present = {path.name for path in _iter_python_files()}
    assert expected <= present


@pytest.mark.parametrize("path", _iter_python_files(), ids=lambda p: p.name)
def test_no_forbidden_infrastructure_imports(path: Path) -> None:
    imported = _imported_modules(path)
    for name in imported:
        assert name not in FORBIDDEN_MODULES, f"{path.name} imports {name}"
        assert not any(
            name == prefix.rstrip(".") or name.startswith(prefix)
            for prefix in FORBIDDEN_PREFIXES
        ), f"{path.name} imports forbidden module {name}"


def test_public_exports_cover_milestone_types() -> None:
    from domain.education import foundation as package

    required = [
        "LearningObjectiveId",
        "ConceptId",
        "LearningEpisodeId",
        "TeachingStrategyId",
        "TeachingIntentionId",
        "DiagnosisId",
        "HypothesisId",
        "PriorityId",
        "DecisionId",
        "OrchestratorId",
        "EvidenceId",
        "ReflectionId",
        "StudentKnowledgeId",
        "MisconceptionId",
        "UnderstandingLevel",
        "LearningDimension",
        "TeachingIntentionType",
        "TeachingStrategyType",
        "DiagnosisType",
        "EvidenceType",
        "ReflectionType",
        "ConfidenceLevel",
        "TransferLevel",
        "LearningObjectiveReference",
        "ConceptReference",
        "MisconceptionReference",
        "RepresentationReference",
        "DependencyReference",
        "TransferContextReference",
        "ApplicationContextReference",
        "EducationalValueObject",
        "EducationalEntity",
        "EducationalInvariantViolation",
        "EducationalDomainError",
        "EducationalResult",
    ]
    for name in required:
        assert hasattr(package, name), f"missing export: {name}"
        assert name in package.__all__
