"""Architecture purity for Adaptive Mission Generator (PRD-001)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4]
    / "src"
    / "application"
    / "education"
    / "mission_generation"
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
        "openai",
        "anthropic",
        "pydantic",
        "marshmallow",
        "numpy",
        "scipy",
        "sklearn",
        "random",
        "uuid",
        "logging",
    }
)

FORBIDDEN_PREFIXES = (
    "flask.",
    "sqlalchemy.",
    "infrastructure.",
    "web.",
    "app.",
    "presentation.",
    "openai.",
    "anthropic.",
)

# Must not re-enter educational reasoning engines or mutate twin/state.
FORBIDDEN_METHOD_NAMES = frozenset(
    {
        "estimate_mastery",
        "estimate_mastery_score",
        "calculate_mastery",
        "compute_mastery",
        "recommend",
        "rank_recommendations",
        "prioritise_recommendations",
        "generate_recommendation",
        "update_student_state",
        "mutate_student_state",
        "update_digital_twin",
        "diagnose",
        "invoke_ai",
        "call_llm",
        "persist",
        "save",
        "to_dict",
        "to_json",
    }
)

ALLOWED_DOMAIN_PREFIXES = (
    "domain.education.recommendation_engine",
)

EXPECTED_LAYOUT = {
    PACKAGE_ROOT / "__init__.py",
    PACKAGE_ROOT / "adaptive_mission_generator.py",
    PACKAGE_ROOT / "enums.py",
    PACKAGE_ROOT / "ids.py",
    PACKAGE_ROOT / "errors.py",
    PACKAGE_ROOT / "planning_constraints.py",
    PACKAGE_ROOT / "models" / "__init__.py",
    PACKAGE_ROOT / "models" / "mission.py",
    PACKAGE_ROOT / "models" / "mission_plan.py",
    PACKAGE_ROOT / "models" / "mission_step.py",
    PACKAGE_ROOT / "models" / "mission_objective.py",
    PACKAGE_ROOT / "models" / "mission_constraint.py",
    PACKAGE_ROOT / "models" / "mission_estimate.py",
    PACKAGE_ROOT / "models" / "mission_ordering.py",
    PACKAGE_ROOT / "models" / "mission_snapshot.py",
    PACKAGE_ROOT / "models" / "mission_summary.py",
    PACKAGE_ROOT / "rules" / "__init__.py",
    PACKAGE_ROOT / "ports" / "__init__.py",
    PACKAGE_ROOT / "ports" / "mission_publisher.py",
    PACKAGE_ROOT / "ports" / "mission_template_provider.py",
    PACKAGE_ROOT / "ports" / "study_constraint_provider.py",
}


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
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
    }


def test_package_layout() -> None:
    assert PACKAGE_ROOT.is_dir()
    for path in EXPECTED_LAYOUT:
        assert path.is_file(), f"missing {path.relative_to(PACKAGE_ROOT.parent)}"


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_forbidden_imports(path: Path) -> None:
    for module in _imported_modules(path):
        root = module.split(".", 1)[0]
        assert root not in FORBIDDEN_MODULES and module not in FORBIDDEN_MODULES, (
            f"{path.name} imports forbidden module {module}"
        )
        for prefix in FORBIDDEN_PREFIXES:
            assert not module.startswith(prefix), (
                f"{path.name} imports forbidden prefix {module}"
            )


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_domain_imports_are_recommendation_engine_only(path: Path) -> None:
    for module in _imported_modules(path):
        if not module.startswith("domain."):
            continue
        if module.startswith("domain.education.recommendation_engine"):
            continue
        pytest.fail(
            f"{path.name} imports disallowed domain module {module} "
            "(mission generation may only consume RecommendationSet)"
        )


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_forbidden_reasoning_methods(path: Path) -> None:
    methods = _defined_methods(path)
    forbidden = methods & FORBIDDEN_METHOD_NAMES
    assert forbidden == set(), f"{path.name} defines forbidden methods {forbidden}"


def test_ports_are_abstract_only() -> None:
    ports_root = PACKAGE_ROOT / "ports"
    for path in ports_root.glob("*.py"):
        if path.name == "__init__.py":
            continue
        source = path.read_text(encoding="utf-8")
        assert "ABC" in source
        assert "abstractmethod" in source
        assert "from sqlalchemy" not in source
        assert "import sqlalchemy" not in source
        assert "Session(" not in source


def test_no_datetime_now_or_uuid4_or_random() -> None:
    for path in _iter_python_files():
        source = path.read_text(encoding="utf-8")
        assert "datetime.now" not in source
        assert "uuid4" not in source
        assert "time.time" not in source
        assert "random." not in source


def test_package_exports() -> None:
    from application.education.mission_generation import (
        AdaptiveMissionGenerator,
        Mission,
        MissionPlan,
        MissionPublisher,
        MissionSnapshot,
        MissionTemplateProvider,
        PlanningConstraints,
        StudyConstraintProvider,
    )

    assert AdaptiveMissionGenerator is not None
    assert MissionPlan is not None
    assert Mission is not None
    assert MissionSnapshot is not None
    assert PlanningConstraints is not None
    assert MissionPublisher is not None
    assert MissionTemplateProvider is not None
    assert StudyConstraintProvider is not None
