"""Architecture purity and package export checks for Educational Diagnosis."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4]
    / "src"
    / "domain"
    / "education"
    / "diagnosis"
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
        PACKAGE_ROOT / "aggregates" / "educational_diagnosis.py",
        PACKAGE_ROOT / "entities" / "diagnosis_indicator.py",
        PACKAGE_ROOT / "entities" / "diagnosis_reason.py",
        PACKAGE_ROOT / "entities" / "diagnosis_scope.py",
        PACKAGE_ROOT / "value_objects" / "diagnosis_confidence.py",
        PACKAGE_ROOT / "value_objects" / "diagnosis_severity.py",
        PACKAGE_ROOT / "policies" / "diagnosis_validation_policy.py",
        PACKAGE_ROOT / "policies" / "diagnosis_consistency_policy.py",
        PACKAGE_ROOT / "specifications" / "diagnosis_is_supported.py",
        PACKAGE_ROOT / "specifications" / "diagnosis_is_actionable.py",
        PACKAGE_ROOT / "events" / "diagnosis_created.py",
        PACKAGE_ROOT / "events" / "diagnosis_invalidated.py",
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
            if name.startswith("domain.education.diagnosis"):
                continue
            assert name in allowed_stdlib, (
                f"{path.relative_to(PACKAGE_ROOT)} imports unexpected {name}"
            )


def test_public_exports() -> None:
    from domain.education import diagnosis as package

    required = [
        "EducationalDiagnosis",
        "DiagnosisIndicator",
        "DiagnosisIndicatorId",
        "InterpretationReference",
        "DiagnosisReason",
        "DiagnosisReasonId",
        "DiagnosisScope",
        "DiagnosisScopeId",
        "DiagnosisConfidence",
        "DiagnosisSeverity",
        "DiagnosisId",
        "DiagnosisType",
        "DiagnosisStatus",
        "DiagnosisSeverityLevel",
        "EducationalScopeKind",
        "IndicatorKind",
        "DiagnosisValidationPolicy",
        "DiagnosisConsistencyPolicy",
        "DiagnosisIsSupportedSpecification",
        "DiagnosisIsActionableSpecification",
        "DiagnosisCreated",
        "DiagnosisInvalidated",
    ]
    for name in required:
        assert hasattr(package, name), f"missing export: {name}"
        assert name in package.__all__


@pytest.mark.parametrize(
    "module_path",
    [
        "domain.education.diagnosis.aggregates.educational_diagnosis",
        "domain.education.diagnosis.entities.diagnosis_indicator",
        "domain.education.diagnosis.entities.diagnosis_reason",
        "domain.education.diagnosis.entities.diagnosis_scope",
        "domain.education.diagnosis.value_objects.diagnosis_confidence",
        "domain.education.diagnosis.value_objects.diagnosis_severity",
        "domain.education.diagnosis.policies.diagnosis_validation_policy",
        "domain.education.diagnosis.policies.diagnosis_consistency_policy",
        "domain.education.diagnosis.events.diagnosis_created",
        "domain.education.diagnosis.events.diagnosis_invalidated",
        "domain.education.diagnosis.specifications.diagnosis_is_supported",
        "domain.education.diagnosis.specifications.diagnosis_is_actionable",
    ],
)
def test_architecture_source_traceability(module_path: str) -> None:
    module = __import__(module_path, fromlist=["*"])
    doc = module.__doc__ or ""
    assert "Architecture Source" in doc
    assert "EDUCATIONAL_DIAGNOSIS_MODEL.md" in doc
    assert "Concept" in doc


def test_no_setter_methods_on_aggregate() -> None:
    from domain.education.diagnosis import EducationalDiagnosis

    forbidden = {
        name
        for name in dir(EducationalDiagnosis)
        if name.startswith("set_") or name.startswith("update_")
    }
    assert forbidden == set()


def test_package_docstring_forbids_downstream_acts() -> None:
    from domain.education import diagnosis as package

    doc = (package.__doc__ or "").casefold()
    assert "does not priorit" in doc or "does not prioritize" in doc
    assert "recommend" in doc
    assert "teaching strateg" in doc
    assert "hypothes" in doc


def test_does_not_import_sibling_education_packages() -> None:
    for path in _iter_python_files():
        for name in _imported_modules(path):
            assert not name.startswith("domain.education.evidence."), (
                f"{path.name} couples to evidence via {name}"
            )
            assert not name.startswith(
                "domain.education.evidence_interpretation."
            ), f"{path.name} couples to evidence_interpretation via {name}"


def test_twelve_diagnosis_types_only() -> None:
    from domain.education.foundation.enums import DiagnosisType

    assert len(DiagnosisType) == 12
    catalogue = {member.value for member in DiagnosisType}
    expected = {
        "conceptual_misunderstanding",
        "procedural_weakness",
        "weak_retention",
        "knowledge_fragmentation",
        "prerequisite_gap",
        "misconception",
        "low_confidence",
        "false_confidence",
        "exam_technique_weakness",
        "application_weakness",
        "transfer_weakness",
        "incomplete_understanding",
    }
    assert catalogue == expected


def test_no_infrastructure_import_statements() -> None:
    for path in _iter_python_files():
        imported = _imported_modules(path)
        for name in imported:
            lowered = name.casefold()
            assert "flask" not in lowered
            assert "sqlalchemy" not in lowered
            assert "repository" not in lowered
            assert not lowered.endswith(".dto")
