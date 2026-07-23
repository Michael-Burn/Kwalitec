"""Architecture purity and package export checks for Educational Evidence."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from domain.education.educational_evidence import (
    EducationalEvidence,
    EvidenceBelongsToStudentSpecification,
    EvidenceIsConsistentSpecification,
    EvidenceNormalisationPolicy,
    EvidenceValidationPolicy,
    NormalisedEvidenceSpecification,
)

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4]
    / "src"
    / "domain"
    / "education"
    / "educational_evidence"
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
    # Every other education bounded context — this engine is intentionally
    # isolated, including from the unrelated IMP-004 evidence package and
    # from the EDU-003.1 student_state context.
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
    "domain.education.digital_twin.",
    "domain.education.student_state.",
)

FORBIDDEN_METHOD_NAMES = frozenset(
    {
        "estimate_mastery",
        "diagnose",
        "interpret_evidence",
        "create_hypothesis",
        "choose_priority",
        "choose_strategy",
        "select_strategy",
        "approve_intervention",
        "orchestrate",
        "recommend",
        "predict",
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
        PACKAGE_ROOT / "enums.py",
        PACKAGE_ROOT / "ids.py",
        PACKAGE_ROOT / "aggregates" / "educational_evidence.py",
        PACKAGE_ROOT / "value_objects" / "evidence_source.py",
        PACKAGE_ROOT / "value_objects" / "evidence_weight.py",
        PACKAGE_ROOT / "value_objects" / "learning_environment.py",
        PACKAGE_ROOT / "value_objects" / "learning_context.py",
        PACKAGE_ROOT / "value_objects" / "evidence_context.py",
        PACKAGE_ROOT / "value_objects" / "evidence_metadata.py",
        PACKAGE_ROOT / "value_objects" / "evidence_timestamp.py",
        PACKAGE_ROOT / "value_objects" / "evidence_snapshot.py",
        PACKAGE_ROOT / "policies" / "evidence_validation_policy.py",
        PACKAGE_ROOT / "policies" / "evidence_normalisation_policy.py",
        PACKAGE_ROOT / "specifications" / "evidence_is_consistent.py",
        PACKAGE_ROOT / "specifications" / "evidence_belongs_to_student.py",
        PACKAGE_ROOT / "specifications" / "normalised_evidence.py",
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
        "datetime",
    }
    for path in _iter_python_files():
        for name in _imported_modules(path):
            if name.startswith("domain.education.foundation"):
                continue
            if name.startswith("domain.education.educational_evidence"):
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


def test_public_exports_include_aggregate_and_value_types() -> None:
    from domain.education import educational_evidence as pkg

    assert pkg.EducationalEvidence is EducationalEvidence
    for expected in (
        "EvidenceSource",
        "EvidenceWeight",
        "EvidenceContext",
        "EvidenceMetadata",
        "LearningContext",
        "LearningEnvironment",
        "EvidenceTimestamp",
        "EvidenceSnapshot",
        "EvidenceId",
        "SubjectId",
        "CompetencyId",
        "MissionId",
        "CheckpointId",
        "EvidenceType",
        "EvidenceSourceKind",
        "LearningEnvironmentKind",
        "EvidenceWeightBand",
    ):
        assert expected in pkg.__all__


def test_aggregate_has_expected_behaviour_surface() -> None:
    behaviour = {
        name
        for name in dir(EducationalEvidence)
        if callable(getattr(EducationalEvidence, name))
        and not name.startswith("_")
    }
    for expected in (
        "record_question_answer",
        "record_reflection",
        "record_session_start",
        "record_session_completion",
        "record_mission_completion",
        "record_hint_request",
        "record_checkpoint",
        "record_confidence",
        "record_time_invested",
        "record_review_completion",
        "record_goal_achievement",
        "record_subject_visit",
        "record_competency_practice",
        "normalise",
        "produce_snapshot",
    ):
        assert expected in behaviour
    for forbidden in FORBIDDEN_METHOD_NAMES:
        assert forbidden not in behaviour


def test_aggregate_has_no_public_setters() -> None:
    behaviour = {
        name
        for name in dir(EducationalEvidence)
        if callable(getattr(EducationalEvidence, name))
        and not name.startswith("_")
    }
    for name in behaviour:
        assert not name.startswith("set_"), f"unexpected setter: {name}"
        assert not name.startswith("update_"), f"unexpected setter: {name}"


def test_policy_has_no_reasoning_surface() -> None:
    assert hasattr(EvidenceValidationPolicy, "assert_identity")
    assert hasattr(EvidenceValidationPolicy, "assert_context_matches_type")
    assert hasattr(EvidenceNormalisationPolicy, "normalise_metadata")
    for forbidden in FORBIDDEN_METHOD_NAMES:
        assert not hasattr(EvidenceValidationPolicy, forbidden)
        assert not hasattr(EvidenceNormalisationPolicy, forbidden)


def test_specifications_exist() -> None:
    assert EvidenceIsConsistentSpecification is not None
    assert EvidenceBelongsToStudentSpecification is not None
    assert NormalisedEvidenceSpecification is not None


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


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_flask_request_or_session(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    assert "flask.request" not in source
    assert "from flask" not in source


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_wall_clock_reads(path: Path) -> None:
    """Determinism guard: nothing in this package reads the wall clock.

    Timestamps must always be supplied explicitly by the caller.
    """
    source = path.read_text(encoding="utf-8")
    assert "datetime.now(" not in source
    assert "utcnow(" not in source


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_random_usage(path: Path) -> None:
    """Determinism guard: nothing in this package uses randomness."""
    source = path.read_text(encoding="utf-8")
    assert "import random" not in source
    assert "secrets." not in source
    assert "uuid.uuid4" not in source
