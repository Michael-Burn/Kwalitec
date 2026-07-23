"""Architecture purity for AI Learning Coach (XP-005)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4]
    / "src"
    / "application"
    / "student_experience"
    / "coach"
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
        "google.generativeai",
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
    "google.generativeai.",
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
        "call_gpt",
        "call_claude",
        "call_gemini",
        "forecast",
        "predict_mastery",
        "predict_exam",
        "generate_recommendation",
        "generate_recommendations",
    }
)

EXPECTED_LAYOUT = {
    PACKAGE_ROOT / "__init__.py",
    PACKAGE_ROOT / "learning_coach_service.py",
    PACKAGE_ROOT / "coach_composer.py",
    PACKAGE_ROOT / "coach_inputs.py",
    PACKAGE_ROOT / "presentation.py",
    PACKAGE_ROOT / "enums.py",
    PACKAGE_ROOT / "errors.py",
    PACKAGE_ROOT / "ids.py",
    PACKAGE_ROOT / "models" / "__init__.py",
    PACKAGE_ROOT / "models" / "coach_context.py",
    PACKAGE_ROOT / "models" / "conversation_context.py",
    PACKAGE_ROOT / "models" / "suggested_questions.py",
    PACKAGE_ROOT / "models" / "explanation_cards.py",
    PACKAGE_ROOT / "models" / "reflection_prompts.py",
    PACKAGE_ROOT / "models" / "celebration_moments.py",
    PACKAGE_ROOT / "models" / "coach_snapshot.py",
    PACKAGE_ROOT / "ports" / "__init__.py",
    PACKAGE_ROOT / "ports" / "coach_publisher.py",
    PACKAGE_ROOT / "ports" / "coach_context_publisher.py",
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
def test_no_domain_imports(path: Path) -> None:
    for module in _imported_modules(path):
        if module.startswith("domain."):
            pytest.fail(f"{path.name} imports domain module {module}")


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
        assert "openai" not in source.lower()
        assert "anthropic" not in source.lower()
        assert "gemini" not in source.lower()


def test_package_exports() -> None:
    from application.student_experience.coach import (
        CoachContext,
        CoachContextPublisher,
        CoachPublisher,
        ConversationContext,
        ExplanationCards,
        LearningCoachService,
        ReflectionPrompts,
        SuggestedQuestions,
    )

    assert LearningCoachService is not None
    assert CoachContext is not None
    assert ConversationContext is not None
    assert SuggestedQuestions is not None
    assert ExplanationCards is not None
    assert ReflectionPrompts is not None
    assert CoachPublisher is not None
    assert CoachContextPublisher is not None


def test_no_datetime_now_or_uuid4() -> None:
    for path in _iter_python_files():
        source = path.read_text(encoding="utf-8")
        assert "datetime.now" not in source
        assert "uuid4" not in source
        assert "time.time" not in source


def test_no_persistence_or_llm_implementation() -> None:
    for path in _iter_python_files():
        source = path.read_text(encoding="utf-8")
        lowered = source.lower()
        assert "db.session" not in source
        assert "openai" not in lowered
        assert "anthropic" not in lowered
        assert "ChatCompletion" not in source
        assert "generativeai" not in lowered
        assert "gpt-4" not in lowered
        assert "claude-" not in lowered
