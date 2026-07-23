"""Architecture purity and package export checks for Recommendation Engine.

Recommendation Engine legitimately imports foundation, student_state,
mastery_estimation, educational_evidence, and knowledge_graph — its entire
purpose is to reason across them. This test forbids infrastructure, HTTP,
persistence, AI, and unrelated/future reasoning-engine bounded contexts.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from domain.education.recommendation_engine import (
    ConstraintSpecification,
    PrioritySpecification,
    RecommendationConsistencySpecification,
    RecommendationEngine,
    RecommendationSet,
)
from domain.education.recommendation_engine.policies.recommendation_validation_policy import (  # noqa: E501
    RecommendationValidationPolicy,
)

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4]
    / "src"
    / "domain"
    / "education"
    / "recommendation_engine"
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
        "numpy",
        "scipy",
        "sklearn",
        "random",
        "uuid",
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
)

# Methods that must never appear on this pure decision engine.
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
        "predict",
        "update_student_state",
        "update_digital_twin",
        "update_knowledge_graph",
        "mutate_student_state",
        "render",
        "to_dict",
        "to_json",
        "save",
        "persist",
        "generate_mission",
        "estimate_mastery",
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
        PACKAGE_ROOT / "aggregates" / "recommendation_set.py",
        PACKAGE_ROOT / "engines" / "recommendation_engine.py",
        PACKAGE_ROOT / "value_objects" / "recommendation.py",
        PACKAGE_ROOT / "value_objects" / "recommendation_priority.py",
        PACKAGE_ROOT / "value_objects" / "recommendation_impact.py",
        PACKAGE_ROOT / "value_objects" / "recommendation_confidence.py",
        PACKAGE_ROOT / "value_objects" / "recommendation_reason.py",
        PACKAGE_ROOT / "value_objects" / "recommendation_constraint.py",
        PACKAGE_ROOT / "value_objects" / "recommendation_target.py",
        PACKAGE_ROOT / "value_objects" / "recommendation_ordering.py",
        PACKAGE_ROOT / "value_objects" / "recommendation_explanation.py",
        PACKAGE_ROOT / "value_objects" / "recommendation_snapshot.py",
        PACKAGE_ROOT / "policies" / "recommendation_policy.py",
        PACKAGE_ROOT / "policies" / "priority_policy.py",
        PACKAGE_ROOT / "policies" / "impact_policy.py",
        PACKAGE_ROOT / "policies" / "constraint_policy.py",
        PACKAGE_ROOT / "policies" / "ordering_policy.py",
        PACKAGE_ROOT / "policies" / "recommendation_validation_policy.py",
        PACKAGE_ROOT
        / "specifications"
        / "recommendation_consistency_specification.py",
        PACKAGE_ROOT / "specifications" / "priority_specification.py",
        PACKAGE_ROOT / "specifications" / "constraint_specification.py",
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


def test_imports_only_stdlib_foundation_permitted_contexts_or_self() -> None:
    allowed_stdlib = {
        "dataclasses",
        "typing",
        "collections.abc",
        "abc",
        "__future__",
        "enum",
        "datetime",
    }
    allowed_context_prefixes = (
        "domain.education.foundation",
        "domain.education.recommendation_engine",
        "domain.education.student_state",
        "domain.education.educational_evidence",
        "domain.education.knowledge_graph",
        "domain.education.mastery_estimation",
    )
    for path in _iter_python_files():
        for name in _imported_modules(path):
            if any(name.startswith(prefix) for prefix in allowed_context_prefixes):
                continue
            assert (
                name in allowed_stdlib
            ), f"{path.relative_to(PACKAGE_ROOT)} imports unexpected {name}"


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_forbidden_method_names(path: Path) -> None:
    methods = _defined_methods(path)
    for forbidden in FORBIDDEN_METHOD_NAMES:
        assert forbidden not in methods, f"{path.name} defines {forbidden}"


def test_public_exports_include_engine_aggregate_and_value_types() -> None:
    from domain.education import recommendation_engine as pkg

    assert pkg.RecommendationEngine is RecommendationEngine
    assert pkg.RecommendationSet is RecommendationSet
    for expected in (
        "Recommendation",
        "RecommendationPriority",
        "RecommendationImpact",
        "RecommendationConfidence",
        "RecommendationReason",
        "RecommendationConstraint",
        "RecommendationTarget",
        "RecommendationOrdering",
        "RecommendationExplanation",
        "RecommendationSnapshot",
        "RecommendationSetId",
        "RecommendationId",
        "SubjectId",
        "CompetencyId",
        "RecommendationCategory",
        "RecommendationPriorityBand",
        "RecommendationImpactBand",
        "RecommendationReasonCode",
        "RecommendationConstraintKind",
        "RecommendationPolicy",
        "PriorityPolicy",
        "ImpactPolicy",
        "ConstraintPolicy",
        "OrderingPolicy",
        "RecommendationValidationPolicy",
        "RecommendationConsistencySpecification",
        "PrioritySpecification",
        "ConstraintSpecification",
    ):
        assert expected in pkg.__all__


def test_engine_has_expected_behaviour_surface() -> None:
    behaviour = {
        name
        for name in dir(RecommendationEngine)
        if callable(getattr(RecommendationEngine, name)) and not name.startswith("_")
    }
    for expected in (
        "recommend",
        "recommend_for_subject",
        "recommend_for_competency",
        "prioritise",
        "rank",
        "identify_highest_impact_actions",
        "produce_snapshot",
        "generate_reasoning",
    ):
        assert expected in behaviour
    for forbidden in FORBIDDEN_METHOD_NAMES:
        assert forbidden not in behaviour


def test_aggregate_has_expected_behaviour_surface() -> None:
    behaviour = {
        name
        for name in dir(RecommendationSet)
        if callable(getattr(RecommendationSet, name)) and not name.startswith("_")
    }
    for expected in (
        "recommendations_for_subject",
        "recommendations_for_competency",
        "recommendations_of_category",
        "highest_impact_actions",
        "highest_priority",
        "has_blocking_constraints",
        "produce_snapshot",
    ):
        assert expected in behaviour
    for forbidden in FORBIDDEN_METHOD_NAMES:
        assert forbidden not in behaviour


def test_policy_has_no_forbidden_surface() -> None:
    assert hasattr(RecommendationValidationPolicy, "assert_identity")
    assert hasattr(RecommendationValidationPolicy, "assert_recommendations")
    for forbidden in FORBIDDEN_METHOD_NAMES:
        assert not hasattr(RecommendationValidationPolicy, forbidden)


def test_specifications_exist() -> None:
    assert RecommendationConsistencySpecification is not None
    assert PrioritySpecification is not None
    assert ConstraintSpecification is not None


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
    source = path.read_text(encoding="utf-8")
    assert "datetime.now(" not in source
    assert "utcnow(" not in source


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_random_or_uuid_identity_generation(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    assert "import uuid" not in source
    assert "import random" not in source


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_machine_learning_or_ai_imports(path: Path) -> None:
    source = path.read_text(encoding="utf-8").lower()
    for fragment in (
        "sklearn",
        "torch",
        "tensorflow",
        "keras",
        "xgboost",
        "openai",
        "anthropic",
        "langchain",
    ):
        assert fragment not in source, f"{path.name} references {fragment}"
