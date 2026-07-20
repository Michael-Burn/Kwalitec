"""Architecture purity and package export checks for Subject Knowledge."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4]
    / "src"
    / "domain"
    / "education"
    / "subject_knowledge"
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
        PACKAGE_ROOT / "aggregates" / "concept.py",
        PACKAGE_ROOT / "aggregates" / "concept_network.py",
        PACKAGE_ROOT / "entities" / "learning_objective.py",
        PACKAGE_ROOT / "entities" / "misconception.py",
        PACKAGE_ROOT / "entities" / "representation.py",
        PACKAGE_ROOT / "entities" / "application_context.py",
        PACKAGE_ROOT / "entities" / "transfer_context.py",
        PACKAGE_ROOT / "value_objects" / "dependency.py",
        PACKAGE_ROOT / "value_objects" / "concept_boundary.py",
        PACKAGE_ROOT / "value_objects" / "mastery_indicator.py",
        PACKAGE_ROOT / "policies" / "dependency_policy.py",
        PACKAGE_ROOT / "policies" / "concept_validation_policy.py",
        PACKAGE_ROOT / "policies" / "representation_policy.py",
        PACKAGE_ROOT / "events" / "concept_created.py",
        PACKAGE_ROOT / "events" / "misconception_registered.py",
        PACKAGE_ROOT / "events" / "dependency_added.py",
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
        "json",
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


def test_imports_only_stdlib_typing_and_foundation_or_self() -> None:
    """Subject Knowledge may depend on foundation and itself only."""
    allowed_prefixes = (
        "domain.education.foundation",
        "domain.education.subject_knowledge",
        "dataclasses",
        "enum",
        "typing",
        "collections",
        "abc",
        "__future__",
    )
    for path in _iter_python_files():
        for name in _imported_modules(path):
            if name.startswith("domain.education.foundation"):
                continue
            if name.startswith("domain.education.subject_knowledge"):
                continue
            assert any(
                name == prefix or name.startswith(prefix + ".")
                for prefix in allowed_prefixes
                if not prefix.startswith("domain.")
            ) or name in {
                "dataclasses",
                "typing",
                "collections.abc",
                "abc",
                "__future__",
            }, f"{path.relative_to(PACKAGE_ROOT)} imports unexpected {name}"


def test_public_exports() -> None:
    from domain.education import subject_knowledge as package

    required = [
        "Concept",
        "ConceptNetwork",
        "NetworkDependency",
        "LearningObjective",
        "Misconception",
        "Representation",
        "RepresentationId",
        "ApplicationContext",
        "ApplicationContextId",
        "TransferContext",
        "TransferContextId",
        "Dependency",
        "ConceptBoundary",
        "MasteryIndicator",
        "DependencyPolicy",
        "ConceptValidationPolicy",
        "RepresentationPolicy",
        "ConceptCreated",
        "MisconceptionRegistered",
        "DependencyAdded",
    ]
    for name in required:
        assert hasattr(package, name), f"missing export: {name}"
        assert name in package.__all__


@pytest.mark.parametrize(
    "module_path",
    [
        "domain.education.subject_knowledge.aggregates.concept",
        "domain.education.subject_knowledge.aggregates.concept_network",
        "domain.education.subject_knowledge.entities.learning_objective",
        "domain.education.subject_knowledge.entities.misconception",
        "domain.education.subject_knowledge.entities.representation",
        "domain.education.subject_knowledge.entities.application_context",
        "domain.education.subject_knowledge.entities.transfer_context",
        "domain.education.subject_knowledge.value_objects.dependency",
        "domain.education.subject_knowledge.value_objects.concept_boundary",
        "domain.education.subject_knowledge.value_objects.mastery_indicator",
    ],
)
def test_architecture_source_traceability(module_path: str) -> None:
    """Every aggregate/entity/value object module documents architecture source."""
    module = __import__(module_path, fromlist=["*"])
    doc = module.__doc__ or ""
    assert "Architecture Source" in doc
    assert any(
        token in doc
        for token in (
            "SUBJECT_KNOWLEDGE_MODEL.md",
            "CONCEPT_ARCHITECTURE.md",
            "KNOWLEDGE_DEPENDENCY_MODEL.md",
            "CONCEPT_NETWORK_MODEL.md",
            "REPRESENTATION_MODEL.md",
            "APPLICATION_AND_TRANSFER_MODEL.md",
            "MISCONCEPTION_AUTHORING_MODEL.md",
        )
    )
    assert "Concept" in doc


def test_no_setter_methods_on_concept() -> None:
    from domain.education.subject_knowledge import Concept

    forbidden = {
        name
        for name in dir(Concept)
        if name.startswith("set_") or name.startswith("update_")
    }
    assert forbidden == set()
