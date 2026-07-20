"""Architecture purity and package export checks for Evidence domain."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4]
    / "src"
    / "domain"
    / "education"
    / "evidence"
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
        PACKAGE_ROOT / "aggregates" / "evidence_record.py",
        PACKAGE_ROOT / "entities" / "evidence_item.py",
        PACKAGE_ROOT / "entities" / "evidence_source.py",
        PACKAGE_ROOT / "entities" / "evidence_context.py",
        PACKAGE_ROOT / "value_objects" / "evidence_strength.py",
        PACKAGE_ROOT / "value_objects" / "evidence_timestamp.py",
        PACKAGE_ROOT / "value_objects" / "confidence_measure.py",
        PACKAGE_ROOT / "policies" / "evidence_validation_policy.py",
        PACKAGE_ROOT / "policies" / "evidence_consistency_policy.py",
        PACKAGE_ROOT / "specifications" / "evidence_is_sufficient.py",
        PACKAGE_ROOT / "specifications" / "evidence_is_consistent.py",
        PACKAGE_ROOT / "events" / "evidence_recorded.py",
        PACKAGE_ROOT / "events" / "evidence_updated.py",
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
        "datetime",
    }
    for path in _iter_python_files():
        for name in _imported_modules(path):
            if name.startswith("domain.education.foundation"):
                continue
            if name.startswith("domain.education.evidence"):
                continue
            assert name in allowed_stdlib, (
                f"{path.relative_to(PACKAGE_ROOT)} imports unexpected {name}"
            )


def test_public_exports() -> None:
    from domain.education import evidence as package

    required = [
        "EvidenceRecord",
        "EvidenceItem",
        "EvidenceItemId",
        "EvidenceSource",
        "EvidenceSourceId",
        "EvidenceContext",
        "EvidenceContextId",
        "EvidenceStrength",
        "EvidenceTimestamp",
        "ConfidenceMeasure",
        "EvidenceItemKind",
        "EvidenceSourceKind",
        "EvidenceRecordStatus",
        "EvidenceStrengthLevel",
        "EvidenceValidationPolicy",
        "EvidenceConsistencyPolicy",
        "EvidenceIsSufficientSpecification",
        "EvidenceIsConsistentSpecification",
        "EvidenceRecorded",
        "EvidenceUpdated",
    ]
    for name in required:
        assert hasattr(package, name), f"missing export: {name}"
        assert name in package.__all__


@pytest.mark.parametrize(
    "module_path",
    [
        "domain.education.evidence.aggregates.evidence_record",
        "domain.education.evidence.entities.evidence_item",
        "domain.education.evidence.entities.evidence_source",
        "domain.education.evidence.entities.evidence_context",
        "domain.education.evidence.value_objects.evidence_strength",
        "domain.education.evidence.value_objects.evidence_timestamp",
        "domain.education.evidence.value_objects.confidence_measure",
        "domain.education.evidence.policies.evidence_validation_policy",
        "domain.education.evidence.policies.evidence_consistency_policy",
        "domain.education.evidence.events.evidence_recorded",
        "domain.education.evidence.events.evidence_updated",
        "domain.education.evidence.specifications.evidence_is_sufficient",
        "domain.education.evidence.specifications.evidence_is_consistent",
    ],
)
def test_architecture_source_traceability(module_path: str) -> None:
    module = __import__(module_path, fromlist=["*"])
    doc = module.__doc__ or ""
    assert "Architecture Source" in doc
    assert any(
        token in doc
        for token in (
            "EDUCATIONAL_EVIDENCE_MODEL.md",
            "CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md",
            "PRODUCTION_INTEGRATION.md",
        )
    )
    assert "Concept" in doc


def test_no_setter_methods_on_aggregate() -> None:
    from domain.education.evidence import EvidenceRecord

    forbidden = {
        name
        for name in dir(EvidenceRecord)
        if name.startswith("set_") or name.startswith("update_")
    }
    assert forbidden == set()


def test_no_infrastructure_import_statements() -> None:
    for path in _iter_python_files():
        imported = _imported_modules(path)
        for name in imported:
            lowered = name.casefold()
            assert "flask" not in lowered
            assert "sqlalchemy" not in lowered
            assert "repository" not in lowered
            assert not lowered.endswith(".dto")


def test_package_docstring_forbids_diagnosis() -> None:
    from domain.education import evidence as package

    doc = package.__doc__ or ""
    assert "does not diagnose" in doc.casefold()
    assert "recommend" in doc.casefold()
    assert "prioritise" in doc.casefold() or "prioritize" in doc.casefold()
