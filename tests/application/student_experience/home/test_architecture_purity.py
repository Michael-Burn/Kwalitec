"""Architecture purity for Student Home Experience (XP-001)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4]
    / "src"
    / "application"
    / "student_experience"
    / "home"
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
        "estimate_mastery_score",
        "calculate_mastery",
        "compute_mastery",
        "score_mastery",
        "rank_recommendations",
        "prioritise_recommendations",
        "prioritize_recommendations",
        "select_recommendation",
        "diagnose",
        "choose_strategy",
        "generate_mission",
        "generate_missions",
        "generate_schedule",
        "plan_schedule",
        "invoke_ai",
        "call_llm",
    }
)

ALLOWED_DOMAIN_PREFIXES = (
    "domain.education.mastery_estimation",
    "domain.education.recommendation_engine",
    "domain.education.foundation",
)

EXPECTED_LAYOUT = {
    PACKAGE_ROOT / "__init__.py",
    PACKAGE_ROOT / "student_home_service.py",
    PACKAGE_ROOT / "home_composer.py",
    PACKAGE_ROOT / "home_inputs.py",
    PACKAGE_ROOT / "presentation.py",
    PACKAGE_ROOT / "enums.py",
    PACKAGE_ROOT / "errors.py",
    PACKAGE_ROOT / "ids.py",
    PACKAGE_ROOT / "models" / "__init__.py",
    PACKAGE_ROOT / "models" / "home_view_model.py",
    PACKAGE_ROOT / "models" / "home_snapshot.py",
    PACKAGE_ROOT / "models" / "todays_focus_card.py",
    PACKAGE_ROOT / "models" / "todays_study_session_card.py",
    PACKAGE_ROOT / "models" / "progress_card.py",
    PACKAGE_ROOT / "models" / "progress_summary.py",
    PACKAGE_ROOT / "models" / "momentum_card.py",
    PACKAGE_ROOT / "models" / "upcoming_milestone_card.py",
    PACKAGE_ROOT / "models" / "exam_readiness_card.py",
    PACKAGE_ROOT / "models" / "achievement_card.py",
    PACKAGE_ROOT / "models" / "learning_insight_card.py",
    PACKAGE_ROOT / "models" / "quick_actions_card.py",
    PACKAGE_ROOT / "models" / "primary_focus.py",
    PACKAGE_ROOT / "ports" / "__init__.py",
    PACKAGE_ROOT / "ports" / "notification_provider.py",
    PACKAGE_ROOT / "ports" / "achievement_provider.py",
    PACKAGE_ROOT / "ports" / "home_publisher.py",
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
def test_domain_imports_are_allowed_only(path: Path) -> None:
    for module in _imported_modules(path):
        if not module.startswith("domain."):
            continue
        if module.startswith("domain.education."):
            allowed = any(
                module == prefix or module.startswith(prefix + ".")
                for prefix in ALLOWED_DOMAIN_PREFIXES
            )
            assert allowed, (
                f"{path.name} imports disallowed domain module {module}"
            )
            continue
        pytest.fail(f"{path.name} imports non-education domain module {module}")


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


def test_package_exports() -> None:
    from application.student_experience.home import (
        AchievementProvider,
        HomePublisher,
        HomeSnapshot,
        HomeViewModel,
        NotificationProvider,
        StudentHomeService,
        TodaysFocusCard,
    )

    assert StudentHomeService is not None
    assert HomeViewModel is not None
    assert HomeSnapshot is not None
    assert TodaysFocusCard is not None
    assert NotificationProvider is not None
    assert AchievementProvider is not None
    assert HomePublisher is not None


def test_no_datetime_now_or_uuid4() -> None:
    for path in _iter_python_files():
        source = path.read_text(encoding="utf-8")
        assert "datetime.now" not in source
        assert "uuid4" not in source
        assert "time.time" not in source


def test_no_persistence_or_ai_calls() -> None:
    for path in _iter_python_files():
        source = path.read_text(encoding="utf-8")
        assert "db.session" not in source
        assert "openai" not in source.lower()
        assert "anthropic" not in source.lower()
        assert "ChatCompletion" not in source
