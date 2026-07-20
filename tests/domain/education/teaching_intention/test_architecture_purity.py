"""Architecture purity and package export checks for Teaching Intention."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4]
    / "src"
    / "domain"
    / "education"
    / "teaching_intention"
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
        PACKAGE_ROOT / "aggregates" / "teaching_intention.py",
        PACKAGE_ROOT / "entities" / "intention_goal.py",
        PACKAGE_ROOT / "entities" / "intention_scope.py",
        PACKAGE_ROOT / "entities" / "intention_constraint.py",
        PACKAGE_ROOT / "entities" / "intention_reference.py",
        PACKAGE_ROOT / "value_objects" / "intention_strength.py",
        PACKAGE_ROOT / "value_objects" / "expected_outcome.py",
        PACKAGE_ROOT / "policies" / "intention_validation_policy.py",
        PACKAGE_ROOT / "policies" / "intention_alignment_policy.py",
        PACKAGE_ROOT / "specifications" / "intention_is_actionable.py",
        PACKAGE_ROOT / "specifications" / "intention_is_aligned.py",
        PACKAGE_ROOT / "events" / "intention_created.py",
        PACKAGE_ROOT / "events" / "intention_revised.py",
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
            if name.startswith("domain.education.teaching_intention"):
                continue
            assert name in allowed_stdlib, (
                f"{path.relative_to(PACKAGE_ROOT)} imports unexpected {name}"
            )


def test_public_exports() -> None:
    from domain.education import teaching_intention as package

    required = [
        "TeachingIntention",
        "IntentionGoal",
        "IntentionGoalId",
        "IntentionScope",
        "IntentionScopeId",
        "IntentionConstraint",
        "IntentionConstraintId",
        "PriorityReference",
        "DiagnosisReference",
        "HypothesisReference",
        "IntentionStrength",
        "ExpectedOutcome",
        "TeachingIntentionId",
        "TeachingIntentionType",
        "IntentionStatus",
        "IntentionStrengthLevel",
        "IntentionScopeKind",
        "IntentionConstraintKind",
        "IntentionRevisionKind",
        "IntentionValidationPolicy",
        "IntentionAlignmentPolicy",
        "IntentionIsActionableSpecification",
        "IntentionIsAlignedSpecification",
        "TeachingIntentionCreated",
        "TeachingIntentionRevised",
    ]
    for name in required:
        assert hasattr(package, name), f"missing export: {name}"
        assert name in package.__all__


@pytest.mark.parametrize(
    "module_path",
    [
        "domain.education.teaching_intention.aggregates.teaching_intention",
        "domain.education.teaching_intention.entities.intention_goal",
        "domain.education.teaching_intention.entities.intention_scope",
        "domain.education.teaching_intention.entities.intention_constraint",
        "domain.education.teaching_intention.entities.intention_reference",
        "domain.education.teaching_intention.value_objects.intention_strength",
        "domain.education.teaching_intention.value_objects.expected_outcome",
        "domain.education.teaching_intention.policies.intention_validation_policy",
        "domain.education.teaching_intention.policies.intention_alignment_policy",
        "domain.education.teaching_intention.events.intention_created",
        "domain.education.teaching_intention.events.intention_revised",
        "domain.education.teaching_intention.specifications.intention_is_actionable",
        "domain.education.teaching_intention.specifications.intention_is_aligned",
    ],
)
def test_architecture_source_traceability(module_path: str) -> None:
    module = __import__(module_path, fromlist=["*"])
    doc = module.__doc__ or ""
    assert "Architecture Source" in doc
    assert "TEACHING_INTENTION_MODEL.md" in doc
    assert "Concept" in doc


def test_no_setter_methods_on_aggregate() -> None:
    from domain.education.teaching_intention import TeachingIntention

    forbidden = {
        name
        for name in dir(TeachingIntention)
        if name.startswith("set_") or name.startswith("update_")
    }
    assert forbidden == set()


def test_package_docstring_forbids_downstream_acts() -> None:
    from domain.education import teaching_intention as package

    doc = (package.__doc__ or "").casefold()
    assert "does not" in doc
    assert "teaching strateg" in doc
    assert "learning episode" in doc
    assert "orchestrat" in doc
    assert "what educational change" in doc or "educational change" in doc


def test_does_not_import_sibling_education_packages() -> None:
    for path in _iter_python_files():
        for name in _imported_modules(path):
            for sibling in (
                "domain.education.evidence.",
                "domain.education.evidence_interpretation.",
                "domain.education.diagnosis.",
                "domain.education.hypothesis.",
                "domain.education.priority.",
                "domain.education.learning_episode.",
                "domain.education.subject_knowledge.",
            ):
                assert not name.startswith(sibling), (
                    f"{path.name} couples to sibling via {name}"
                )


def test_catalogue_matches_teaching_intention_model() -> None:
    from domain.education.foundation.enums import TeachingIntentionType

    catalogue = {member.value for member in TeachingIntentionType}
    expected = {
        "repair_misconception",
        "build_intuition",
        "strengthen_prerequisite",
        "improve_transfer",
        "increase_procedural_fluency",
        "consolidate_understanding",
        "recover_confidence",
        "prepare_for_examination",
        "improve_retention",
        "calibrate_confidence_downward",
        "connect_fragmented_knowledge",
        "strengthen_application",
        "complete_missing_facets",
    }
    assert catalogue == expected
    assert len(TeachingIntentionType) == 13


def test_no_strategy_or_episode_types_exported() -> None:
    from domain.education import teaching_intention as package

    assert not hasattr(package, "TeachingStrategyType")
    assert not hasattr(package, "EpisodeType")
    assert "TeachingStrategy" not in package.__all__


def test_source_files_have_no_http_route_decorators() -> None:
    for path in _iter_python_files():
        text = path.read_text(encoding="utf-8")
        assert "@app.route" not in text
        assert "db.session" not in text


def test_no_infrastructure_import_statements() -> None:
    for path in _iter_python_files():
        imported = _imported_modules(path)
        for name in imported:
            lowered = name.casefold()
            assert "flask" not in lowered
            assert "sqlalchemy" not in lowered
            assert "repository" not in lowered
            assert not lowered.endswith(".dto")
