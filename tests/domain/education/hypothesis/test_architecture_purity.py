"""Architecture purity and package export checks for Educational Hypothesis."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4]
    / "src"
    / "domain"
    / "education"
    / "hypothesis"
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
        PACKAGE_ROOT / "aggregates" / "educational_hypothesis.py",
        PACKAGE_ROOT / "entities" / "hypothesis_reason.py",
        PACKAGE_ROOT / "entities" / "hypothesis_scope.py",
        PACKAGE_ROOT / "entities" / "competing_hypothesis.py",
        PACKAGE_ROOT / "value_objects" / "plausibility.py",
        PACKAGE_ROOT / "value_objects" / "explanatory_strength.py",
        PACKAGE_ROOT / "policies" / "hypothesis_validation_policy.py",
        PACKAGE_ROOT / "policies" / "hypothesis_revision_policy.py",
        PACKAGE_ROOT / "specifications" / "hypothesis_is_supported.py",
        PACKAGE_ROOT / "specifications" / "hypothesis_is_revisable.py",
        PACKAGE_ROOT / "events" / "hypothesis_created.py",
        PACKAGE_ROOT / "events" / "hypothesis_revised.py",
        PACKAGE_ROOT / "events" / "hypothesis_discarded.py",
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
            if name.startswith("domain.education.hypothesis"):
                continue
            assert name in allowed_stdlib, (
                f"{path.relative_to(PACKAGE_ROOT)} imports unexpected {name}"
            )


def test_public_exports() -> None:
    from domain.education import hypothesis as package

    required = [
        "EducationalHypothesis",
        "HypothesisReason",
        "HypothesisReasonId",
        "HypothesisScope",
        "HypothesisScopeId",
        "CompetingHypothesis",
        "CompetingHypothesisId",
        "DiagnosisReference",
        "InterpretationReference",
        "Plausibility",
        "ExplanatoryStrength",
        "HypothesisId",
        "HypothesisKind",
        "HypothesisStatus",
        "PlausibilityLevel",
        "ExplanatoryStrengthLevel",
        "HypothesisScopeKind",
        "RevisionForm",
        "HypothesisValidationPolicy",
        "HypothesisRevisionPolicy",
        "HypothesisIsSupportedSpecification",
        "HypothesisIsRevisableSpecification",
        "HypothesisCreated",
        "HypothesisRevised",
        "HypothesisDiscarded",
    ]
    for name in required:
        assert hasattr(package, name), f"missing export: {name}"
        assert name in package.__all__


@pytest.mark.parametrize(
    "module_path",
    [
        "domain.education.hypothesis.aggregates.educational_hypothesis",
        "domain.education.hypothesis.entities.hypothesis_reason",
        "domain.education.hypothesis.entities.hypothesis_scope",
        "domain.education.hypothesis.entities.competing_hypothesis",
        "domain.education.hypothesis.value_objects.plausibility",
        "domain.education.hypothesis.value_objects.explanatory_strength",
        "domain.education.hypothesis.policies.hypothesis_validation_policy",
        "domain.education.hypothesis.policies.hypothesis_revision_policy",
        "domain.education.hypothesis.events.hypothesis_created",
        "domain.education.hypothesis.events.hypothesis_revised",
        "domain.education.hypothesis.events.hypothesis_discarded",
        "domain.education.hypothesis.specifications.hypothesis_is_supported",
        "domain.education.hypothesis.specifications.hypothesis_is_revisable",
    ],
)
def test_architecture_source_traceability(module_path: str) -> None:
    module = __import__(module_path, fromlist=["*"])
    doc = module.__doc__ or ""
    assert "Architecture Source" in doc
    assert "EDUCATIONAL_HYPOTHESIS_MODEL.md" in doc
    assert "Concept" in doc


def test_no_setter_methods_on_aggregate() -> None:
    from domain.education.hypothesis import EducationalHypothesis

    forbidden = {
        name
        for name in dir(EducationalHypothesis)
        if name.startswith("set_") or name.startswith("update_")
    }
    assert forbidden == set()


def test_package_docstring_forbids_downstream_acts() -> None:
    from domain.education import hypothesis as package

    doc = (package.__doc__ or "").casefold()
    assert "revisable" in doc
    assert "not facts" in doc or "are not facts" in doc
    assert "does not diagnos" in doc
    assert "teaching strateg" in doc
    assert "priorit" in doc


def test_does_not_import_sibling_education_packages() -> None:
    for path in _iter_python_files():
        for name in _imported_modules(path):
            assert not name.startswith("domain.education.diagnosis."), (
                f"{path.name} couples to diagnosis package via {name}"
            )
            assert not name.startswith("domain.education.evidence."), (
                f"{path.name} couples to evidence via {name}"
            )
            assert not name.startswith(
                "domain.education.evidence_interpretation."
            ), f"{path.name} couples to evidence_interpretation via {name}"


def test_seven_hypothesis_kinds_only() -> None:
    from domain.education.hypothesis import HypothesisKind

    assert len(HypothesisKind) == 7
    catalogue = {member.value for member in HypothesisKind}
    expected = {
        "prerequisite_deficiency",
        "representation_mismatch",
        "weak_abstraction",
        "surface_memorisation",
        "procedural_fixation",
        "transfer_limitation",
        "confidence_calibration_issue",
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
