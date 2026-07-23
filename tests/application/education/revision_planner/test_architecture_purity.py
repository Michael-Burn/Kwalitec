"""Architecture purity for Adaptive Revision Planner (PRD-002)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4]
    / "src"
    / "application"
    / "education"
    / "revision_planner"
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
        "generate_mission",
        "generate_missions",
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

ALLOWED_APPLICATION_PREFIXES = (
    "application.education.revision_planner",
    "application.education.mission_generation",
    "application.education.mission_execution",
    "application.errors",
)

EXPECTED_LAYOUT = {
    PACKAGE_ROOT / "__init__.py",
    PACKAGE_ROOT / "adaptive_revision_planner.py",
    PACKAGE_ROOT / "enums.py",
    PACKAGE_ROOT / "ids.py",
    PACKAGE_ROOT / "errors.py",
    PACKAGE_ROOT / "planning_constraints.py",
    PACKAGE_ROOT / "student_availability.py",
    PACKAGE_ROOT / "exam_target.py",
    PACKAGE_ROOT / "execution_history.py",
    PACKAGE_ROOT / "models" / "__init__.py",
    PACKAGE_ROOT / "models" / "study_schedule.py",
    PACKAGE_ROOT / "models" / "study_day.py",
    PACKAGE_ROOT / "models" / "study_session.py",
    PACKAGE_ROOT / "models" / "scheduled_mission.py",
    PACKAGE_ROOT / "models" / "schedule_summary.py",
    PACKAGE_ROOT / "models" / "schedule_snapshot.py",
    PACKAGE_ROOT / "models" / "study_calendar_projection.py",
    PACKAGE_ROOT / "models" / "schedule_metrics.py",
    PACKAGE_ROOT / "models" / "completion_metrics.py",
    PACKAGE_ROOT / "services" / "__init__.py",
    PACKAGE_ROOT / "services" / "dependency_resolver.py",
    PACKAGE_ROOT / "services" / "session_allocator.py",
    PACKAGE_ROOT / "services" / "workload_balancer.py",
    PACKAGE_ROOT / "services" / "spacing_strategy.py",
    PACKAGE_ROOT / "services" / "schedule_validator.py",
    PACKAGE_ROOT / "services" / "schedule_rebalancer.py",
    PACKAGE_ROOT / "ports" / "__init__.py",
    PACKAGE_ROOT / "ports" / "calendar_provider.py",
    PACKAGE_ROOT / "ports" / "availability_provider.py",
    PACKAGE_ROOT / "ports" / "schedule_publisher.py",
    PACKAGE_ROOT / "ports" / "holiday_provider.py",
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
def test_application_imports_are_scoped(path: Path) -> None:
    for module in _imported_modules(path):
        if not module.startswith("application."):
            continue
        if any(module.startswith(prefix) for prefix in ALLOWED_APPLICATION_PREFIXES):
            continue
        pytest.fail(
            f"{path.name} imports disallowed application module {module}"
        )


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_domain_imports_are_disallowed(path: Path) -> None:
    for module in _imported_modules(path):
        if module.startswith("domain."):
            pytest.fail(
                f"{path.name} imports domain module {module} "
                "(revision planner must not re-enter domain engines)"
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
    from application.education.revision_planner import (
        AdaptiveRevisionPlanner,
        AvailabilityProvider,
        CalendarProvider,
        DependencyResolver,
        HolidayProvider,
        PlanningConstraints,
        SchedulePublisher,
        ScheduleRebalancer,
        ScheduleValidator,
        SessionAllocator,
        SpacingStrategy,
        StudySchedule,
        WorkloadBalancer,
    )

    assert AdaptiveRevisionPlanner is not None
    assert StudySchedule is not None
    assert PlanningConstraints is not None
    assert DependencyResolver is not None
    assert SessionAllocator is not None
    assert WorkloadBalancer is not None
    assert SpacingStrategy is not None
    assert ScheduleValidator is not None
    assert ScheduleRebalancer is not None
    assert CalendarProvider is not None
    assert AvailabilityProvider is not None
    assert SchedulePublisher is not None
    assert HolidayProvider is not None
