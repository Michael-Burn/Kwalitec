"""Architecture purity and package export checks for Educational Digital Twin."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from domain.education.digital_twin import (
    EducationalDigitalTwin,
    MasteryChanged,
    TwinCreated,
    TwinIsConsistentSpecification,
    TwinUpdated,
    TwinUpdatePolicy,
)

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4]
    / "src"
    / "domain"
    / "education"
    / "digital_twin"
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
    "domain.education.orchestrator.",
)

FORBIDDEN_METHOD_NAMES = frozenset(
    {
        "diagnose",
        "interpret_evidence",
        "create_hypothesis",
        "choose_priority",
        "choose_strategy",
        "select_strategy",
        "approve_intervention",
        "orchestrate",
    }
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
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            names.add(node.name)
    return names


def test_package_directory_layout() -> None:
    assert PACKAGE_ROOT.is_dir()
    expected_files = {
        PACKAGE_ROOT / "__init__.py",
        PACKAGE_ROOT / "aggregates" / "educational_digital_twin.py",
        PACKAGE_ROOT / "entities" / "learner_state.py",
        PACKAGE_ROOT / "entities" / "concept_state.py",
        PACKAGE_ROOT / "entities" / "misconception_state.py",
        PACKAGE_ROOT / "entities" / "intervention_history.py",
        PACKAGE_ROOT / "entities" / "evidence_history.py",
        PACKAGE_ROOT / "value_objects" / "mastery_state.py",
        PACKAGE_ROOT / "value_objects" / "retention_state.py",
        PACKAGE_ROOT / "value_objects" / "confidence_profile.py",
        PACKAGE_ROOT / "value_objects" / "learning_trajectory.py",
        PACKAGE_ROOT / "policies" / "twin_update_policy.py",
        PACKAGE_ROOT / "policies" / "state_validation_policy.py",
        PACKAGE_ROOT / "specifications" / "twin_is_consistent.py",
        PACKAGE_ROOT / "specifications" / "state_transition_is_valid.py",
        PACKAGE_ROOT / "events" / "twin_created.py",
        PACKAGE_ROOT / "events" / "twin_updated.py",
        PACKAGE_ROOT / "events" / "mastery_changed.py",
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
            if name.startswith("domain.education.digital_twin"):
                continue
            assert name in allowed_stdlib, (
                f"{path.relative_to(PACKAGE_ROOT)} imports unexpected {name}"
            )


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_reasoning_method_names(path: Path) -> None:
    methods = _defined_methods(path)
    for forbidden in FORBIDDEN_METHOD_NAMES:
        assert forbidden not in methods, f"{path.name} defines {forbidden}"


def test_public_exports_include_aggregate_and_memory_types() -> None:
    from domain.education import digital_twin as pkg

    assert pkg.EducationalDigitalTwin is EducationalDigitalTwin
    assert "LearnerState" in pkg.__all__
    assert "EvidenceHistoryEntry" in pkg.__all__
    assert "InterventionHistoryEntry" in pkg.__all__
    assert "MasteryState" in pkg.__all__
    assert "RetentionState" in pkg.__all__
    assert "ConfidenceProfile" in pkg.__all__
    assert "LearningTrajectory" in pkg.__all__
    assert "TwinCreated" in pkg.__all__
    assert "TwinUpdated" in pkg.__all__
    assert "MasteryChanged" in pkg.__all__


def test_twin_remembers_without_reasoning_surface() -> None:
    behaviour = {
        name
        for name in dir(EducationalDigitalTwin)
        if callable(getattr(EducationalDigitalTwin, name)) and not name.startswith("_")
    }
    assert "create" in behaviour
    assert "record_evidence" in behaviour
    assert "record_intervention" in behaviour
    assert "update_mastery" in behaviour
    assert "update_retention" in behaviour
    assert "archive" in behaviour
    for forbidden in FORBIDDEN_METHOD_NAMES:
        assert forbidden not in behaviour


def test_policy_is_memory_law_not_reasoning() -> None:
    assert hasattr(TwinUpdatePolicy, "assert_mutable")
    assert hasattr(TwinUpdatePolicy, "assert_evidence_appendable")
    assert hasattr(TwinUpdatePolicy, "assert_intervention_appendable")
    assert not hasattr(TwinUpdatePolicy, "diagnose")
    assert not hasattr(TwinUpdatePolicy, "choose_strategy")


def test_consistency_spec_exists() -> None:
    assert TwinIsConsistentSpecification is not None
    assert TwinCreated is not None
    assert TwinUpdated is not None
    assert MasteryChanged is not None


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_modules_use_future_annotations(path: Path) -> None:
    if path.name == "__init__.py" and path.read_text(encoding="utf-8").strip() == "":
        return
    source = path.read_text(encoding="utf-8")
    if not source.strip():
        return
    assert "from __future__ import annotations" in source


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_flask_request_or_session(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    assert "flask.request" not in source
    assert "from flask" not in source
