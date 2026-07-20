"""Architecture purity tests for the persistence mapping layer (INF-001)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4] / "src" / "infrastructure" / "persistence"
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
        "pydantic",
        "marshmallow",
    }
)

FORBIDDEN_PREFIXES = (
    "flask.",
    "sqlalchemy.",
    "app.",
    "app.models",
    "app.services",
    "app.domain",
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

EXPECTED_MAPPERS = {
    PACKAGE_ROOT / "mappers" / "digital_twin_mapper.py",
    PACKAGE_ROOT / "mappers" / "learning_episode_mapper.py",
    PACKAGE_ROOT / "mappers" / "evidence_mapper.py",
    PACKAGE_ROOT / "mappers" / "subject_knowledge_mapper.py",
    PACKAGE_ROOT / "mappers" / "diagnosis_mapper.py",
    PACKAGE_ROOT / "mappers" / "hypothesis_mapper.py",
    PACKAGE_ROOT / "mappers" / "priority_mapper.py",
    PACKAGE_ROOT / "mappers" / "teaching_intention_mapper.py",
    PACKAGE_ROOT / "mappers" / "teaching_strategy_mapper.py",
    PACKAGE_ROOT / "mappers" / "decision_mapper.py",
    PACKAGE_ROOT / "mappers" / "orchestrator_mapper.py",
}


def _iter_python_files() -> list[Path]:
    """INF-001 mapping layer only — exclude ``sqlalchemy/`` (INF-002)."""
    files: list[Path] = []
    for name in ("__init__.py",):
        path = PACKAGE_ROOT / name
        if path.is_file():
            files.append(path)
    for subpackage in ("dto", "mappers"):
        root = PACKAGE_ROOT / subpackage
        if root.is_dir():
            files.extend(sorted(root.rglob("*.py")))
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


def _defined_methods(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            names.add(node.name)
    return names


def test_package_directory_layout() -> None:
    assert PACKAGE_ROOT.is_dir()
    for path in EXPECTED_MAPPERS:
        assert path.is_file(), f"missing {path.relative_to(PACKAGE_ROOT)}"


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
def test_no_persistence_session_or_repositories(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    lowered = source.lower()
    for fragment in (
        "create_engine",
        "sessionmaker",
        "sqlalchemy.orm.session",
        "class repository",
        "sqlite3.connect",
        "psycopg",
    ):
        assert fragment not in lowered, f"{path.name} contains {fragment}"


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


def test_mappers_expose_conversion_api() -> None:
    from infrastructure.persistence.mappers import (
        DecisionMapper,
        DiagnosisMapper,
        DigitalTwinMapper,
        EvidenceMapper,
        HypothesisMapper,
        LearningEpisodeMapper,
        OrchestratorMapper,
        PriorityMapper,
        SubjectKnowledgeMapper,
        TeachingIntentionMapper,
        TeachingStrategyMapper,
    )

    for mapper in (
        DigitalTwinMapper,
        LearningEpisodeMapper,
        EvidenceMapper,
        SubjectKnowledgeMapper,
        DiagnosisMapper,
        HypothesisMapper,
        PriorityMapper,
        TeachingIntentionMapper,
        TeachingStrategyMapper,
        DecisionMapper,
        OrchestratorMapper,
    ):
        assert hasattr(mapper, "to_persistence")
        assert hasattr(mapper, "to_domain")
