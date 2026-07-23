"""Architecture purity for Mission Execution Engine (PRD-001.5)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4]
    / "src"
    / "application"
    / "education"
    / "mission_execution"
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
        "numpy",
        "scipy",
        "sklearn",
        "random",
        "uuid",
        "logging",
    }
)

FORBIDDEN_PREFIXES = (
    "flask.",
    "sqlalchemy.",
    "infrastructure.",
    "web.",
    "app.",
    "presentation.",
    "openai.",
    "anthropic.",
)

FORBIDDEN_METHOD_NAMES = frozenset(
    {
        "estimate_mastery",
        "estimate_mastery_score",
        "calculate_mastery",
        "compute_mastery",
        "recommend",
        "rank_recommendations",
        "prioritise_recommendations",
        "generate_recommendation",
        "generate_mission",
        "generate_missions",
        "update_student_state",
        "mutate_student_state",
        "update_digital_twin",
        "diagnose",
        "invoke_ai",
        "call_llm",
        "persist",
        "save",
        "to_dict",
        "to_json",
    }
)

ALLOWED_DOMAIN_PREFIXES = (
    "domain.education.educational_evidence",
    "domain.education.foundation",
)

ALLOWED_APPLICATION_PREFIXES = (
    "application.education.mission_execution",
    "application.education.mission_generation",
    "application.errors",
)

EXPECTED_LAYOUT = {
    PACKAGE_ROOT / "__init__.py",
    PACKAGE_ROOT / "mission_execution_engine.py",
    PACKAGE_ROOT / "execution_command_result.py",
    PACKAGE_ROOT / "enums.py",
    PACKAGE_ROOT / "ids.py",
    PACKAGE_ROOT / "errors.py",
    PACKAGE_ROOT / "models" / "__init__.py",
    PACKAGE_ROOT / "models" / "mission_execution.py",
    PACKAGE_ROOT / "models" / "execution_progress.py",
    PACKAGE_ROOT / "models" / "execution_metrics.py",
    PACKAGE_ROOT / "models" / "execution_summary.py",
    PACKAGE_ROOT / "models" / "execution_snapshot.py",
    PACKAGE_ROOT / "models" / "confidence_record.py",
    PACKAGE_ROOT / "models" / "reflection_record.py",
    PACKAGE_ROOT / "events" / "__init__.py",
    PACKAGE_ROOT / "rules" / "__init__.py",
    PACKAGE_ROOT / "rules" / "lifecycle_rules.py",
    PACKAGE_ROOT / "rules" / "progress_rules.py",
    PACKAGE_ROOT / "rules" / "metrics_rules.py",
    PACKAGE_ROOT / "rules" / "evidence_mapping_rules.py",
    PACKAGE_ROOT / "ports" / "__init__.py",
    PACKAGE_ROOT / "ports" / "clock.py",
    PACKAGE_ROOT / "ports" / "mission_execution_publisher.py",
    PACKAGE_ROOT / "ports" / "educational_evidence_publisher.py",
    PACKAGE_ROOT / "ports" / "mission_execution_store.py",
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
    for path in EXPECTED_LAYOUT:
        assert path.is_file(), f"missing {path.relative_to(PACKAGE_ROOT.parent)}"


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_forbidden_imports(path: Path) -> None:
    for module in _imported_modules(path):
        root = module.split(".", 1)[0]
        assert root not in FORBIDDEN_MODULES and module not in FORBIDDEN_MODULES, (
            f"{path.name} imports forbidden module {module}"
        )
        for prefix in FORBIDDEN_PREFIXES:
            assert not module.startswith(prefix), (
                f"{path.name} imports forbidden prefix {module}"
            )


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_domain_imports_are_allowed_only(path: Path) -> None:
    for module in _imported_modules(path):
        if not module.startswith("domain."):
            continue
        if any(module.startswith(prefix) for prefix in ALLOWED_DOMAIN_PREFIXES):
            continue
        pytest.fail(
            f"{path.name} imports disallowed domain module {module} "
            "(mission execution may only consume educational_evidence + foundation)"
        )


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_application_imports_are_scoped(path: Path) -> None:
    for module in _imported_modules(path):
        if not module.startswith("application."):
            continue
        if any(module.startswith(prefix) for prefix in ALLOWED_APPLICATION_PREFIXES):
            continue
        pytest.fail(
            f"{path.name} imports disallowed application module {module}"
        )


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_forbidden_reasoning_methods(path: Path) -> None:
    methods = _defined_methods(path)
    # MissionExecutionStore.save is an abstract port method name — allow on ports.
    if path.parent.name == "ports" and path.name == "mission_execution_store.py":
        methods = methods - {"save"}
    forbidden = methods & FORBIDDEN_METHOD_NAMES
    assert forbidden == set(), f"{path.name} defines forbidden methods {forbidden}"


def test_ports_are_abstract_only() -> None:
    ports_root = PACKAGE_ROOT / "ports"
    for path in ports_root.glob("*.py"):
        if path.name == "__init__.py":
            continue
        source = path.read_text(encoding="utf-8")
        assert "ABC" in source
        assert "abstractmethod" in source
        assert "from sqlalchemy" not in source
        assert "import sqlalchemy" not in source
        assert "Session(" not in source


def test_no_datetime_now_or_uuid4_or_random() -> None:
    for path in _iter_python_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        source = path.read_text(encoding="utf-8")
        # Reject wall-clock / non-deterministic calls in executable code,
        # ignoring docstring prose that may mention them as forbidden.
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                call_src = ast.get_source_segment(source, node) or ""
                assert "datetime.now" not in call_src
                assert "uuid4" not in call_src
                assert "time.time" not in call_src
                assert "random." not in call_src
        assert "import random" not in source
        assert "from random" not in source
        assert "import uuid" not in source
        assert "from uuid" not in source


def test_engine_has_required_api() -> None:
    required = {
        "start_execution",
        "pause_execution",
        "resume_execution",
        "complete_step",
        "skip_step",
        "record_confidence",
        "record_reflection",
        "complete_execution",
        "abandon_execution",
        "expire_execution",
        "produce_snapshot",
    }
    from application.education.mission_execution import MissionExecutionEngine

    for name in required:
        assert hasattr(MissionExecutionEngine, name)


def test_package_exports() -> None:
    from application.education.mission_execution import (
        Clock,
        EducationalEvidencePublisher,
        ExecutionSnapshot,
        MissionExecution,
        MissionExecutionEngine,
        MissionExecutionPublisher,
        MissionExecutionStore,
    )

    assert MissionExecutionEngine is not None
    assert MissionExecution is not None
    assert ExecutionSnapshot is not None
    assert Clock is not None
    assert MissionExecutionPublisher is not None
    assert EducationalEvidencePublisher is not None
    assert MissionExecutionStore is not None


def test_no_mastery_or_recommendation_imports() -> None:
    for path in _iter_python_files():
        for module in _imported_modules(path):
            assert "mastery" not in module
            assert "recommendation_engine" not in module
            assert "student_state" not in module
            assert "digital_twin" not in module
