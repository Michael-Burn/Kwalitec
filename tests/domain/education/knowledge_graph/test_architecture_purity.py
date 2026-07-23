"""Architecture purity and package export checks for Knowledge Dependency Graph."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from domain.education.knowledge_graph import (
    AcyclicPrerequisiteSpecification,
    GraphValidationPolicy,
    KnowledgeGraph,
    KnowledgeGraphConsistencySpecification,
    RelationshipValiditySpecification,
)

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4]
    / "src"
    / "domain"
    / "education"
    / "knowledge_graph"
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
        "networkx",
        "igraph",
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
    "domain.education.digital_twin.",
    "domain.education.student_state.",
    "domain.education.educational_evidence.",
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
        "update_student_state",
        "update_digital_twin",
        "render",
        "to_dict",
        "to_json",
        "save",
        "persist",
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
        PACKAGE_ROOT / "aggregates" / "knowledge_graph.py",
        PACKAGE_ROOT / "value_objects" / "knowledge_node.py",
        PACKAGE_ROOT / "value_objects" / "knowledge_relationship.py",
        PACKAGE_ROOT / "value_objects" / "knowledge_edge.py",
        PACKAGE_ROOT / "value_objects" / "dependency_strength.py",
        PACKAGE_ROOT / "value_objects" / "relationship_metadata.py",
        PACKAGE_ROOT / "value_objects" / "learning_depth.py",
        PACKAGE_ROOT / "value_objects" / "knowledge_path.py",
        PACKAGE_ROOT / "value_objects" / "concept_cluster.py",
        PACKAGE_ROOT / "value_objects" / "knowledge_snapshot.py",
        PACKAGE_ROOT / "policies" / "graph_validation_policy.py",
        PACKAGE_ROOT / "policies" / "relationship_policy.py",
        PACKAGE_ROOT / "policies" / "cycle_detection_policy.py",
        PACKAGE_ROOT / "policies" / "learning_path_policy.py",
        PACKAGE_ROOT
        / "specifications"
        / "knowledge_graph_consistency_specification.py",
        PACKAGE_ROOT / "specifications" / "acyclic_prerequisite_specification.py",
        PACKAGE_ROOT / "specifications" / "relationship_validity_specification.py",
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
            assert fragment not in lowered.split(
                "."
            ), f"{path.name} imports infrastructure-like module {name}"


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
            if name.startswith("domain.education.knowledge_graph"):
                continue
            assert (
                name in allowed_stdlib
            ), f"{path.relative_to(PACKAGE_ROOT)} imports unexpected {name}"


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
    from domain.education import knowledge_graph as pkg

    assert pkg.KnowledgeGraph is KnowledgeGraph
    for expected in (
        "KnowledgeNode",
        "KnowledgeRelationship",
        "KnowledgeEdge",
        "DependencyStrength",
        "RelationshipMetadata",
        "LearningDepth",
        "KnowledgePath",
        "ConceptCluster",
        "KnowledgeSnapshot",
        "KnowledgeGraphId",
        "KnowledgeNodeId",
        "KnowledgeRelationshipId",
        "RelationshipType",
        "KnowledgeNodeKind",
        "DependencyStrengthBand",
    ):
        assert expected in pkg.__all__


def test_aggregate_has_expected_behaviour_surface() -> None:
    behaviour = {
        name
        for name in dir(KnowledgeGraph)
        if callable(getattr(KnowledgeGraph, name)) and not name.startswith("_")
    }
    for expected in (
        "create",
        "add_node",
        "remove_node",
        "connect",
        "disconnect",
        "find_prerequisites",
        "find_dependents",
        "find_learning_path",
        "find_foundations",
        "find_concept_clusters",
        "detect_cycles",
        "produce_snapshot",
    ):
        assert expected in behaviour
    for forbidden in FORBIDDEN_METHOD_NAMES:
        assert forbidden not in behaviour


def test_policy_has_no_reasoning_surface() -> None:
    assert hasattr(GraphValidationPolicy, "assert_identity")
    assert hasattr(GraphValidationPolicy, "assert_nodes")
    for forbidden in FORBIDDEN_METHOD_NAMES:
        assert not hasattr(GraphValidationPolicy, forbidden)


def test_specifications_exist() -> None:
    assert KnowledgeGraphConsistencySpecification is not None
    assert AcyclicPrerequisiteSpecification is not None
    assert RelationshipValiditySpecification is not None


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
    """Determinism guard: the graph never reads the wall clock itself.

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
def test_no_random_or_uuid_identity_generation(path: Path) -> None:
    """Determinism guard: identities are derived, never randomly generated."""
    source = path.read_text(encoding="utf-8")
    assert "import uuid" not in source
    assert "import random" not in source
