"""Architecture purity and package export checks for Teaching Strategy."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4]
    / "src"
    / "domain"
    / "education"
    / "teaching_strategy"
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
    "domain.education.teaching_intention.",
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
        PACKAGE_ROOT / "aggregates" / "teaching_strategy.py",
        PACKAGE_ROOT / "entities" / "strategy_goal.py",
        PACKAGE_ROOT / "entities" / "strategy_constraint.py",
        PACKAGE_ROOT / "entities" / "strategy_reference.py",
        PACKAGE_ROOT / "entities" / "strategy_rationale.py",
        PACKAGE_ROOT / "value_objects" / "strategy_effectiveness.py",
        PACKAGE_ROOT / "value_objects" / "instructional_complexity.py",
        PACKAGE_ROOT / "policies" / "strategy_selection_policy.py",
        PACKAGE_ROOT / "policies" / "strategy_validation_policy.py",
        PACKAGE_ROOT / "policies" / "strategy_composition_policy.py",
        PACKAGE_ROOT / "specifications" / "strategy_is_applicable.py",
        PACKAGE_ROOT / "specifications" / "strategy_is_composable.py",
        PACKAGE_ROOT / "events" / "strategy_selected.py",
        PACKAGE_ROOT / "events" / "strategy_revised.py",
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
            name == prefix or name.startswith(prefix)
            for prefix in FORBIDDEN_PREFIXES
        ), f"{path.name} imports forbidden {name}"


def test_package_exports_aggregate_and_policies() -> None:
    from domain.education import teaching_strategy as pkg

    assert pkg.TeachingStrategy is not None
    assert pkg.StrategySelectionPolicy is not None
    assert pkg.StrategyCompositionPolicy is not None
    assert pkg.StrategyValidationPolicy is not None
    assert pkg.StrategyIsApplicableSpecification is not None
    assert pkg.StrategyIsComposableSpecification is not None
    assert pkg.TeachingStrategySelected is not None
    assert pkg.TeachingStrategyRevised is not None


def test_catalogue_size_matches_foundation_enum() -> None:
    from domain.education.foundation.enums import TeachingStrategyType
    from domain.education.teaching_strategy import StrategySelectionPolicy

    assert len(StrategySelectionPolicy.catalogue()) == len(TeachingStrategyType)
    assert StrategySelectionPolicy.catalogue() == frozenset(TeachingStrategyType)


def test_no_sqlalchemy_or_flask_in_source_text() -> None:
    for path in _iter_python_files():
        text = path.read_text(encoding="utf-8").casefold()
        assert "sqlalchemy" not in text
        assert "from flask" not in text
        assert "import flask" not in text


@pytest.mark.parametrize(
    "export_name",
    [
        "TeachingStrategy",
        "StrategyGoal",
        "StrategyRationale",
        "StrategyConstraint",
        "IntentionReference",
        "DiagnosisReference",
        "HypothesisReference",
        "SecondaryStrategyReference",
        "StrategyEffectiveness",
        "InstructionalComplexity",
        "StrategyStatus",
        "EffectivenessLevel",
        "ComplexityLevel",
        "CompositionPattern",
        "StrategySelectionPolicy",
        "StrategyCompositionPolicy",
        "StrategyValidationPolicy",
        "StrategyIsApplicableSpecification",
        "StrategyIsComposableSpecification",
        "TeachingStrategySelected",
        "TeachingStrategyRevised",
    ],
)
def test_public_exports_present(export_name: str) -> None:
    from domain.education import teaching_strategy as pkg

    assert hasattr(pkg, export_name)
    assert export_name in pkg.__all__
