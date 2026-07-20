"""Shared helpers for APP-003 architecture governance gates."""

from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
DOMAIN_ROOT = SRC_ROOT / "domain"
APPLICATION_ROOT = SRC_ROOT / "application"
INFRASTRUCTURE_ROOT = SRC_ROOT / "infrastructure"
WEB_ROOT = SRC_ROOT / "web"
DOCS_ROOT = REPO_ROOT / "docs"
ADR_ROOT = DOCS_ROOT / "adr"

COMPOSITION_PARTS = frozenset({"composition"})

FRAMEWORK_MODULES = frozenset(
    {
        "flask",
        "sqlalchemy",
        "alembic",
        "jinja2",
        "wtforms",
    }
)

AI_MODULES = frozenset(
    {
        "openai",
        "anthropic",
        "google",
        "google.generativeai",
    }
)

EDUCATIONAL_DECISION_METHODS = frozenset(
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

PIPELINE_ORCHESTRATION_FORBIDDEN_METHODS = frozenset(
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


def iter_python_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.py") if path.is_file())


def imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def top_level_name(module: str) -> str:
    return module.split(".", 1)[0]


def defined_function_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
    }


def call_names(path: Path) -> set[str]:
    """Return simple Name/Attribute call targets (e.g. EducationalPipeline)."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name):
            names.add(func.id)
        elif isinstance(func, ast.Attribute):
            names.add(func.attr)
    return names


def is_under_composition(path: Path, layer_root: Path) -> bool:
    try:
        parts = path.relative_to(layer_root).parts
    except ValueError:
        return False
    return bool(COMPOSITION_PARTS.intersection(parts))


def module_matches(name: str, forbidden: frozenset[str]) -> bool:
    if name in forbidden:
        return True
    return any(
        name == item or name.startswith(item + ".") for item in forbidden
    )
