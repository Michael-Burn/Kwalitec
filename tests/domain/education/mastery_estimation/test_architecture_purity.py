"""Architecture purity and package export checks for Mastery Estimation.

Unlike its sibling bounded contexts (``student_state``,
``educational_evidence``, ``knowledge_graph``), which must never import one
another, Mastery Estimation legitimately imports all three — its entire
purpose is to reason across them. This test therefore forbids
infrastructure, HTTP, persistence, and unrelated/future reasoning-engine
bounded contexts, but explicitly permits those three.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from domain.education.mastery_estimation import (
    AssessmentConfidenceSpecification,
    KnowledgeGapSpecification,
    MasteryAssessment,
    MasteryAssessmentConsistencySpecification,
    MasteryEstimator,
)
from domain.education.mastery_estimation.policies.assessment_validation_policy import (  # noqa: E501
    AssessmentValidationPolicy,
)

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4]
    / "src"
    / "domain"
    / "education"
    / "mastery_estimation"
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

# Mastery Estimation legitimately depends on foundation, student_state,
# educational_evidence, and knowledge_graph — its entire purpose is to
# reason across those bounded contexts. Everything else stays forbidden:
# infrastructure, HTTP, and unrelated/future reasoning-engine contexts.
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
    "domain.education.recommendation_engine.",
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
        "recommend",
        "predict",
        "update_student_state",
        "update_digital_twin",
        "update_knowledge_graph",
        "render",
        "to_dict",
        "to_json",
        "save",
        "persist",
        "generate_mission",
        "generate_recommendation",
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
        PACKAGE_ROOT / "aggregates" / "mastery_assessment.py",
        PACKAGE_ROOT / "engines" / "mastery_estimator.py",
        PACKAGE_ROOT / "value_objects" / "mastery_score.py",
        PACKAGE_ROOT / "value_objects" / "confidence_score.py",
        PACKAGE_ROOT / "value_objects" / "learning_stability.py",
        PACKAGE_ROOT / "value_objects" / "evidence_contribution.py",
        PACKAGE_ROOT / "value_objects" / "knowledge_gap.py",
        PACKAGE_ROOT / "value_objects" / "assessment_reason.py",
        PACKAGE_ROOT / "value_objects" / "mastery_confidence.py",
        PACKAGE_ROOT / "value_objects" / "competency_assessment.py",
        PACKAGE_ROOT / "value_objects" / "subject_assessment.py",
        PACKAGE_ROOT / "value_objects" / "assessment_snapshot.py",
        PACKAGE_ROOT / "policies" / "evidence_weight_policy.py",
        PACKAGE_ROOT / "policies" / "mastery_policy.py",
        PACKAGE_ROOT / "policies" / "prerequisite_influence_policy.py",
        PACKAGE_ROOT / "policies" / "confidence_policy.py",
        PACKAGE_ROOT / "policies" / "stability_policy.py",
        PACKAGE_ROOT / "policies" / "assessment_validation_policy.py",
        PACKAGE_ROOT
        / "specifications"
        / "mastery_assessment_consistency_specification.py",
        PACKAGE_ROOT / "specifications" / "assessment_confidence_specification.py",
        PACKAGE_ROOT / "specifications" / "knowledge_gap_specification.py",
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
        "domain.education.mastery_estimation",
        "domain.education.student_state",
        "domain.education.educational_evidence",
        "domain.education.knowledge_graph",
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
def test_no_reasoning_method_names(path: Path) -> None:
    methods = _defined_methods(path)
    for forbidden in FORBIDDEN_METHOD_NAMES:
        assert forbidden not in methods, f"{path.name} defines {forbidden}"


def test_public_exports_include_engine_aggregate_and_value_types() -> None:
    from domain.education import mastery_estimation as pkg

    assert pkg.MasteryEstimator is MasteryEstimator
    assert pkg.MasteryAssessment is MasteryAssessment
    for expected in (
        "MasteryScore",
        "ConfidenceScore",
        "MasteryConfidence",
        "LearningStability",
        "EvidenceContribution",
        "KnowledgeGap",
        "AssessmentReason",
        "CompetencyAssessment",
        "SubjectAssessment",
        "AssessmentSnapshot",
        "AssessmentId",
        "SubjectId",
        "CompetencyId",
        "MasteryBand",
        "LearningStabilityBand",
        "KnowledgeGapKind",
        "KnowledgeGapSeverity",
        "AssessmentReasonCode",
        "EvidenceWeightPolicy",
        "MasteryPolicy",
        "PrerequisiteInfluencePolicy",
        "ConfidencePolicy",
        "StabilityPolicy",
    ):
        assert expected in pkg.__all__


def test_engine_has_expected_behaviour_surface() -> None:
    behaviour = {
        name
        for name in dir(MasteryEstimator)
        if callable(getattr(MasteryEstimator, name)) and not name.startswith("_")
    }
    for expected in (
        "estimate",
        "estimate_subject",
        "estimate_competency",
        "identify_knowledge_gaps",
        "identify_prerequisite_weaknesses",
        "calculate_confidence",
        "calculate_learning_stability",
        "produce_snapshot",
    ):
        assert expected in behaviour
    for forbidden in FORBIDDEN_METHOD_NAMES:
        assert forbidden not in behaviour


def test_aggregate_has_expected_behaviour_surface() -> None:
    behaviour = {
        name
        for name in dir(MasteryAssessment)
        if callable(getattr(MasteryAssessment, name)) and not name.startswith("_")
    }
    for expected in (
        "subject_assessment_for",
        "competency_assessment_for",
        "weak_prerequisites",
        "direct_gaps",
        "has_knowledge_gaps",
        "produce_snapshot",
    ):
        assert expected in behaviour
    for forbidden in FORBIDDEN_METHOD_NAMES:
        assert forbidden not in behaviour


def test_policy_has_no_reasoning_surface() -> None:
    assert hasattr(AssessmentValidationPolicy, "assert_identity")
    assert hasattr(AssessmentValidationPolicy, "assert_subject_assessments")
    for forbidden in FORBIDDEN_METHOD_NAMES:
        assert not hasattr(AssessmentValidationPolicy, forbidden)


def test_specifications_exist() -> None:
    assert MasteryAssessmentConsistencySpecification is not None
    assert AssessmentConfidenceSpecification is not None
    assert KnowledgeGapSpecification is not None


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
    """Determinism guard: the engine never reads the wall clock itself.

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
    """Determinism guard: identities and estimates never use randomness."""
    source = path.read_text(encoding="utf-8")
    assert "import uuid" not in source
    assert "import random" not in source


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_machine_learning_imports(path: Path) -> None:
    """The estimator must remain deterministic and rule-based, never ML."""
    source = path.read_text(encoding="utf-8").lower()
    for fragment in ("sklearn", "torch", "tensorflow", "keras", "xgboost"):
        assert fragment not in source, f"{path.name} references {fragment}"
