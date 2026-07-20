"""Architecture purity tests for the application layer (APP-001/APP-002)."""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

import pytest

PACKAGE_ROOT = Path(__file__).resolve().parents[3] / "src" / "application"

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

FORBIDDEN_METHOD_NAMES = frozenset(
    {
        "diagnose",
        "calculate_mastery",
        "prioritise",
        "prioritize",
        "choose_strategy",
        "select_strategy",
        "interpret_evidence",
        "create_hypothesis",
    }
)

EXPECTED_LAYOUT = {
    PACKAGE_ROOT / "__init__.py",
    PACKAGE_ROOT / "errors.py",
    PACKAGE_ROOT / "dto" / "__init__.py",
    PACKAGE_ROOT / "commands" / "__init__.py",
    PACKAGE_ROOT / "queries" / "__init__.py",
    PACKAGE_ROOT / "services" / "__init__.py",
    PACKAGE_ROOT / "handlers" / "__init__.py",
    PACKAGE_ROOT / "events" / "__init__.py",
    PACKAGE_ROOT / "ports" / "__init__.py",
    PACKAGE_ROOT / "services" / "learning_application_service.py",
    PACKAGE_ROOT / "services" / "twin_application_service.py",
    PACKAGE_ROOT / "services" / "assessment_application_service.py",
    PACKAGE_ROOT / "services" / "planning_application_service.py",
    PACKAGE_ROOT / "services" / "dashboard_application_service.py",
    PACKAGE_ROOT / "ports" / "repositories.py",
    PACKAGE_ROOT / "ports" / "unit_of_work.py",
    PACKAGE_ROOT / "ports" / "clock.py",
    PACKAGE_ROOT / "ports" / "uuid_generator.py",
    PACKAGE_ROOT / "ports" / "transaction_manager.py",
    PACKAGE_ROOT / "ports" / "event_publisher.py",
    PACKAGE_ROOT / "composition" / "__init__.py",
    PACKAGE_ROOT / "composition" / "container.py",
    PACKAGE_ROOT / "composition" / "service_registry.py",
    PACKAGE_ROOT / "composition" / "application_factory.py",
    PACKAGE_ROOT / "commands" / "start_learning_session.py",
    PACKAGE_ROOT / "commands" / "complete_learning_episode.py",
    PACKAGE_ROOT / "commands" / "record_evidence.py",
    PACKAGE_ROOT / "commands" / "update_digital_twin.py",
    PACKAGE_ROOT / "commands" / "generate_teaching_plan.py",
    PACKAGE_ROOT / "queries" / "get_learner_state.py",
    PACKAGE_ROOT / "queries" / "get_teaching_plan.py",
    PACKAGE_ROOT / "queries" / "get_evidence_history.py",
    PACKAGE_ROOT / "queries" / "get_learning_trajectory.py",
    PACKAGE_ROOT / "queries" / "get_dashboard.py",
    PACKAGE_ROOT / "queries" / "get_todays_mission.py",
    PACKAGE_ROOT / "queries" / "get_progress_summary.py",
    PACKAGE_ROOT / "queries" / "get_recommendations.py",
    PACKAGE_ROOT / "queries" / "get_timeline.py",
    PACKAGE_ROOT / "read_models" / "__init__.py",
    PACKAGE_ROOT / "read_models" / "serialization.py",
    PACKAGE_ROOT / "read_models" / "dashboard" / "dashboard_read_model.py",
    PACKAGE_ROOT / "read_models" / "today" / "todays_mission_read_model.py",
    PACKAGE_ROOT / "read_models" / "missions" / "mission_task_read_model.py",
    PACKAGE_ROOT / "read_models" / "recommendations" / "recommendation_read_model.py",
    PACKAGE_ROOT / "read_models" / "progress" / "progress_summary_read_model.py",
    PACKAGE_ROOT / "read_models" / "timeline" / "timeline_read_model.py",
    PACKAGE_ROOT / "pipeline" / "__init__.py",
    PACKAGE_ROOT / "pipeline" / "educational_pipeline.py",
    PACKAGE_ROOT / "pipeline" / "pipeline_request.py",
    PACKAGE_ROOT / "pipeline" / "pipeline_result.py",
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
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            names.add(node.name)
    return names


def test_package_directory_layout() -> None:
    assert PACKAGE_ROOT.is_dir()
    for path in EXPECTED_LAYOUT:
        assert path.is_file(), f"missing {path.relative_to(PACKAGE_ROOT.parent)}"


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
def test_no_persistence_implementations(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    lowered = source.lower()
    for fragment in ("create_engine", "sessionmaker", "sqlite3.connect", "psycopg"):
        assert fragment not in lowered, f"{path.name} contains persistence code"


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_educational_intelligence_methods(path: Path) -> None:
    methods = _defined_methods(path)
    for forbidden in FORBIDDEN_METHOD_NAMES:
        assert forbidden not in methods, f"{path.name} defines {forbidden}"


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
def test_no_flask_http_surface(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    assert "flask.request" not in source
    assert "from flask" not in source
    assert "@app.route" not in source
    assert "Blueprint(" not in source


def test_required_services_exist() -> None:
    from application.services import (
        AssessmentApplicationService,
        DashboardApplicationService,
        LearningApplicationService,
        PlanningApplicationService,
        TwinApplicationService,
    )

    assert LearningApplicationService is not None
    assert TwinApplicationService is not None
    assert AssessmentApplicationService is not None
    assert PlanningApplicationService is not None
    assert DashboardApplicationService is not None


def test_services_depend_on_unit_of_work() -> None:
    from application.services.assessment_application_service import (
        AssessmentApplicationService,
    )
    from application.services.learning_application_service import (
        LearningApplicationService,
    )
    from application.services.planning_application_service import (
        PlanningApplicationService,
    )
    from application.services.twin_application_service import TwinApplicationService

    for service in (
        LearningApplicationService,
        TwinApplicationService,
        AssessmentApplicationService,
        PlanningApplicationService,
    ):
        params = inspect.signature(service.__init__).parameters
        assert "uow" in params
        assert "clock" in params


def test_application_services_do_not_call_uuid4_directly() -> None:
    for path in (PACKAGE_ROOT / "services").rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert "uuid4" not in source
        assert "uuid.uuid4" not in source
        assert "datetime.now" not in source
