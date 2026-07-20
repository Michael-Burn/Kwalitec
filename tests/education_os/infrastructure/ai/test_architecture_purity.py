"""Architecture purity tests for AI-001 Educational Enrichment Layer."""

from __future__ import annotations

import ast
from pathlib import Path

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4] / "src" / "infrastructure" / "ai"
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
        "openai",
        "anthropic",
        "google",
        "google.generativeai",
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
    "openai.",
    "anthropic.",
    "google.",
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
        "generate_mission",
        "generate_recommendations",
        "rewrite_mission",
        "change_recommendation",
        "mutate_recommendation",
    }
)

EXPECTED_LAYOUT = {
    PACKAGE_ROOT / "__init__.py",
    PACKAGE_ROOT / "providers" / "__init__.py",
    PACKAGE_ROOT / "providers" / "ai_provider.py",
    PACKAGE_ROOT / "providers" / "openai_provider.py",
    PACKAGE_ROOT / "providers" / "anthropic_provider.py",
    PACKAGE_ROOT / "providers" / "gemini_provider.py",
    PACKAGE_ROOT / "prompting" / "__init__.py",
    PACKAGE_ROOT / "prompting" / "prompt_builder.py",
    PACKAGE_ROOT / "prompting" / "mission_prompt_builder.py",
    PACKAGE_ROOT / "prompting" / "recommendation_prompt_builder.py",
    PACKAGE_ROOT / "enrichment" / "__init__.py",
    PACKAGE_ROOT / "enrichment" / "mission_enricher.py",
    PACKAGE_ROOT / "enrichment" / "recommendation_enricher.py",
    PACKAGE_ROOT / "models" / "__init__.py",
    PACKAGE_ROOT / "models" / "enhanced_mission.py",
    PACKAGE_ROOT / "models" / "enhanced_recommendation.py",
}

ALLOWED_DOMAIN_PREFIXES = (
    "domain.mission_generation",
    "domain.recommendation",
    "domain.student_experience",
    "domain.education.foundation",
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


def test_expected_package_layout() -> None:
    assert PACKAGE_ROOT.is_dir()
    for path in EXPECTED_LAYOUT:
        assert path.is_file(), f"missing {path.relative_to(PACKAGE_ROOT)}"


def test_architecture_purity() -> None:
    for path in _iter_python_files():
        imported = _imported_modules(path)
        for name in imported:
            assert name not in FORBIDDEN_MODULES, f"{path.name} imports {name}"
            assert not any(
                name == prefix.rstrip(".") or name.startswith(prefix)
                for prefix in FORBIDDEN_PREFIXES
            ), f"{path.name} imports forbidden module {name}"
            if name.startswith("domain."):
                assert any(
                    name == allowed or name.startswith(allowed + ".")
                    for allowed in ALLOWED_DOMAIN_PREFIXES
                ), f"{path.name} imports disallowed domain module {name}"

        methods = _defined_methods(path)
        for forbidden in FORBIDDEN_METHOD_NAMES:
            assert forbidden not in methods, f"{path.name} defines {forbidden}"

        content = path.read_text(encoding="utf-8")
        if content.strip():
            assert "from __future__ import annotations" in content


def test_ai_layer_does_not_import_educational_decision_engines() -> None:
    forbidden_tokens = (
        "MissionGenerator",
        "RecommendationGenerator",
        "ExperienceGenerator",
        "StudyPlanner",
        "ProgressEvaluator",
        "DigitalTwin",
        "DiagnosisEngine",
    )
    for path in _iter_python_files():
        text = path.read_text(encoding="utf-8")
        for token in forbidden_tokens:
            assert token not in text, f"{path.name} references {token}"


def test_enrichers_depend_on_provider_abstraction() -> None:
    mission_src = (
        PACKAGE_ROOT / "enrichment" / "mission_enricher.py"
    ).read_text(encoding="utf-8")
    recommendation_src = (
        PACKAGE_ROOT / "enrichment" / "recommendation_enricher.py"
    ).read_text(encoding="utf-8")
    assert "AIProvider" in mission_src
    assert "AIProvider" in recommendation_src
    assert "OpenAIProvider" not in mission_src
    assert "AnthropicProvider" not in mission_src
    assert "GeminiProvider" not in mission_src
    assert "OpenAIProvider" not in recommendation_src
