"""Architecture purity and package export checks for Educational Priority."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4]
    / "src"
    / "domain"
    / "education"
    / "priority"
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
        PACKAGE_ROOT / "aggregates" / "educational_priority.py",
        PACKAGE_ROOT / "entities" / "priority_factor.py",
        PACKAGE_ROOT / "entities" / "priority_scope.py",
        PACKAGE_ROOT / "entities" / "priority_constraint.py",
        PACKAGE_ROOT / "entities" / "priority_references.py",
        PACKAGE_ROOT / "value_objects" / "priority_score.py",
        PACKAGE_ROOT / "value_objects" / "urgency.py",
        PACKAGE_ROOT / "value_objects" / "instructional_impact.py",
        PACKAGE_ROOT / "policies" / "priority_calculation_policy.py",
        PACKAGE_ROOT / "policies" / "priority_validation_policy.py",
        PACKAGE_ROOT / "specifications" / "priority_is_actionable.py",
        PACKAGE_ROOT / "specifications" / "priority_is_stable.py",
        PACKAGE_ROOT / "events" / "priority_assigned.py",
        PACKAGE_ROOT / "events" / "priority_revised.py",
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
            if name.startswith("domain.education.priority"):
                continue
            assert name in allowed_stdlib, (
                f"{path.relative_to(PACKAGE_ROOT)} imports unexpected {name}"
            )


def test_public_exports() -> None:
    from domain.education import priority as package

    required = [
        "EducationalPriority",
        "PriorityFactor",
        "PriorityFactorId",
        "PriorityScope",
        "PriorityScopeId",
        "PriorityConstraint",
        "PriorityConstraintId",
        "DiagnosisReference",
        "HypothesisReference",
        "PriorityScore",
        "Urgency",
        "InstructionalImpact",
        "PriorityId",
        "PriorityStatus",
        "PriorityFactorKind",
        "PriorityScoreBand",
        "UrgencyLevel",
        "InstructionalImpactLevel",
        "PriorityScopeKind",
        "PriorityConstraintKind",
        "PriorityRevisionKind",
        "PriorityValidationPolicy",
        "PriorityCalculationPolicy",
        "PriorityIsActionableSpecification",
        "PriorityIsStableSpecification",
        "PriorityAssigned",
        "PriorityRevised",
    ]
    for name in required:
        assert hasattr(package, name), f"missing export: {name}"
        assert name in package.__all__


@pytest.mark.parametrize(
    "module_path",
    [
        "domain.education.priority.aggregates.educational_priority",
        "domain.education.priority.entities.priority_factor",
        "domain.education.priority.entities.priority_scope",
        "domain.education.priority.entities.priority_constraint",
        "domain.education.priority.entities.priority_references",
        "domain.education.priority.value_objects.priority_score",
        "domain.education.priority.value_objects.urgency",
        "domain.education.priority.value_objects.instructional_impact",
        "domain.education.priority.policies.priority_calculation_policy",
        "domain.education.priority.policies.priority_validation_policy",
        "domain.education.priority.events.priority_assigned",
        "domain.education.priority.events.priority_revised",
        "domain.education.priority.specifications.priority_is_actionable",
        "domain.education.priority.specifications.priority_is_stable",
    ],
)
def test_architecture_source_traceability(module_path: str) -> None:
    module = __import__(module_path, fromlist=["*"])
    doc = module.__doc__ or ""
    assert "Architecture Source" in doc
    assert "EDUCATIONAL_PRIORITY_MODEL.md" in doc
    assert "Concept" in doc


def test_no_setter_methods_on_aggregate() -> None:
    from domain.education.priority import EducationalPriority

    forbidden = {
        name
        for name in dir(EducationalPriority)
        if name.startswith("set_") or name.startswith("update_")
    }
    assert forbidden == set()


def test_package_docstring_forbids_downstream_and_upstream_acts() -> None:
    from domain.education import priority as package

    doc = (package.__doc__ or "").casefold()
    assert "does not diagnose" in doc
    assert "explain" in doc
    assert "teaching strateg" in doc
    assert "severity" in doc
    assert "instructional ordering" in doc or "address first" in doc


def test_does_not_import_sibling_education_packages() -> None:
    for path in _iter_python_files():
        for name in _imported_modules(path):
            for sibling in (
                "domain.education.evidence.",
                "domain.education.evidence_interpretation.",
                "domain.education.diagnosis.",
                "domain.education.hypothesis.",
                "domain.education.learning_episode.",
                "domain.education.subject_knowledge.",
            ):
                assert not name.startswith(sibling), (
                    f"{path.name} couples to sibling via {name}"
                )


def test_eight_priority_factor_kinds() -> None:
    from domain.education.priority import PriorityFactorKind

    assert len(PriorityFactorKind) == 8
    catalogue = {member.value for member in PriorityFactorKind}
    expected = {
        "prerequisite_importance",
        "transfer_blocking",
        "exam_relevance",
        "concept_centrality",
        "learning_dependency_depth",
        "misconception_persistence",
        "educational_leverage",
        "confidence_in_diagnosis",
    }
    assert catalogue == expected


def test_severity_not_exported_as_priority_concept() -> None:
    from domain.education import priority as package

    assert not hasattr(package, "DiagnosisSeverity")
    assert not hasattr(package, "DiagnosisSeverityLevel")
    assert "Severity" not in package.__all__


def test_no_infrastructure_import_statements() -> None:
    for path in _iter_python_files():
        imported = _imported_modules(path)
        for name in imported:
            lowered = name.casefold()
            assert "flask" not in lowered
            assert "sqlalchemy" not in lowered
            assert "repository" not in lowered
            assert not lowered.endswith(".dto")


def test_source_files_have_no_http_route_decorators() -> None:
    for path in _iter_python_files():
        text = path.read_text(encoding="utf-8")
        assert "@app.route" not in text
        assert "db.session" not in text
