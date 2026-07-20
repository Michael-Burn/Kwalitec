"""Architecture purity and package export checks for Educational Orchestrator."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4]
    / "src"
    / "domain"
    / "education"
    / "orchestrator"
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
    "domain.education.evidence.",
    "domain.education.evidence_interpretation.",
    "domain.education.learning_episode.",
    "domain.education.subject_knowledge.",
    "domain.education.diagnosis.",
    "domain.education.hypothesis.",
    "domain.education.priority.",
    "domain.education.teaching_intention.",
    "domain.education.teaching_strategy.",
    "domain.education.decision.",
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


def test_package_directory_layout() -> None:
    assert PACKAGE_ROOT.is_dir()
    expected_files = {
        PACKAGE_ROOT / "__init__.py",
        PACKAGE_ROOT / "aggregates" / "educational_orchestrator.py",
        PACKAGE_ROOT / "entities" / "orchestration_plan.py",
        PACKAGE_ROOT / "entities" / "orchestration_stage.py",
        PACKAGE_ROOT / "entities" / "orchestration_reference.py",
        PACKAGE_ROOT / "value_objects" / "orchestration_state.py",
        PACKAGE_ROOT / "value_objects" / "orchestration_progress.py",
        PACKAGE_ROOT / "policies" / "orchestration_policy.py",
        PACKAGE_ROOT / "policies" / "sequencing_policy.py",
        PACKAGE_ROOT / "specifications" / "orchestration_is_valid.py",
        PACKAGE_ROOT / "specifications" / "stage_is_executable.py",
        PACKAGE_ROOT / "events" / "orchestration_started.py",
        PACKAGE_ROOT / "events" / "orchestration_completed.py",
        PACKAGE_ROOT / "events" / "orchestration_paused.py",
        PACKAGE_ROOT / "enums.py",
    }
    for path in expected_files:
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
def test_no_persistence_or_serialization_imports(path: Path) -> None:
    imported = _imported_modules(path)
    forbidden_substrings = (
        "pickle",
        "sqlite",
        "psycopg",
        "pymongo",
        "dto",
        "repository",
        "serializer",
    )
    for name in imported:
        lowered = name.lower()
        for fragment in forbidden_substrings:
            assert fragment not in lowered.split("."), (
                f"{path.name} imports infrastructure-like module {name}"
            )


def test_imports_only_stdlib_foundation_or_self() -> None:
    allowed_stdlib = {
        "dataclasses",
        "typing",
        "collections.abc",
        "abc",
        "__future__",
        "enum",
    }
    for path in _iter_python_files():
        for name in _imported_modules(path):
            if name.startswith("domain.education.foundation"):
                continue
            if name.startswith("domain.education.orchestrator"):
                continue
            assert name in allowed_stdlib, (
                f"{path.relative_to(PACKAGE_ROOT)} imports unexpected {name}"
            )


def test_public_exports() -> None:
    from domain.education import orchestrator as package

    required = [
        "EducationalOrchestrator",
        "OrchestrationPlan",
        "OrchestrationPlanId",
        "OrchestrationStage",
        "OrchestrationStageId",
        "ApprovedDecisionReference",
        "StrategyReference",
        "EpisodeReference",
        "OrchestrationState",
        "OrchestrationProgress",
        "OrchestratorId",
        "OrchestrationStatus",
        "StageStatus",
        "OrchestrationStageKind",
        "EvidenceCollectionPointKind",
        "OrchestrationPolicy",
        "SequencingPolicy",
        "OrchestrationIsValidSpecification",
        "StageIsExecutableSpecification",
        "OrchestrationStarted",
        "OrchestrationCompleted",
        "OrchestrationPaused",
    ]
    for name in required:
        assert hasattr(package, name), f"missing export: {name}"
        assert name in package.__all__


def test_package_docstring_declares_coordination_only() -> None:
    text = (PACKAGE_ROOT / "__init__.py").read_text(encoding="utf-8").lower()
    assert "coordinate" in text
    assert "does not reason" in text or "does not diagnose" in text
    assert "flask" in text
    assert "sqlalchemy" in text or "orm" in text


FORBIDDEN_REASONING_TERMS = (
    "diagnose",
    "hypothesis",
    "repriorit",
    "select_strateg",
    "interpret_evidence",
)


@pytest.mark.parametrize(
    "path",
    [
        PACKAGE_ROOT / "aggregates" / "educational_orchestrator.py",
        PACKAGE_ROOT / "policies" / "orchestration_policy.py",
    ],
    ids=lambda p: p.name,
)
def test_aggregate_docstrings_forbid_reasoning(path: Path) -> None:
    text = path.read_text(encoding="utf-8").lower()
    assert "does not" in text
    assert any(
        phrase in text
        for phrase in (
            "does not reason",
            "does not diagnose",
            "does not",
        )
    )


def test_no_flask_or_sqlalchemy_in_source_text() -> None:
    for path in _iter_python_files():
        text = path.read_text(encoding="utf-8")
        assert "from flask" not in text
        assert "import flask" not in text
        assert "sqlalchemy" not in text.lower() or "no" in text.lower()
