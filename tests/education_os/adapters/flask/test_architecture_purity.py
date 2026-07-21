"""Architecture purity for the Flask adapter layer (V4-002 / V4-004)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = Path(__file__).resolve().parents[4] / "src" / "adapters" / "flask"

FORBIDDEN_MODULES = frozenset(
    {
        "sqlalchemy",
        "alembic",
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
    }
)

FORBIDDEN_PREFIXES = (
    "sqlalchemy.",
    "alembic.",
    "openai.",
    "anthropic.",
    "app.models",
    "app.services",
    "infrastructure.persistence",
    "web.",
)

# Controllers, mappers, and renderers stay Flask-free for unit testing.
FLASK_FREE_RELATIVE = frozenset(
    {
        "template_mapper.py",
        "navigation.py",
        "page_renderer.py",
        "checkpoint_store.py",
        "dashboard/controller.py",
        "session/controller.py",
        "reflection/controller.py",
        "mission/controller.py",
        "auth/controller.py",
        "auth/secure_cookies.py",
        "rendering/__init__.py",
        "rendering/html_helpers.py",
        "rendering/token_renderer.py",
        "rendering/style_renderer.py",
        "rendering/accessibility_renderer.py",
        "rendering/component_renderer.py",
    }
)

CONTROLLER_FORBIDDEN = frozenset({"flask", "jinja2", "sqlalchemy", "domain"})
CONTROLLER_FORBIDDEN_PREFIXES = (
    "flask.",
    "jinja2.",
    "sqlalchemy.",
    "domain.",
    "infrastructure.persistence",
    "infrastructure.ai",
    "web.",
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
        "orchestrate",
        "persist",
        "commit",
    }
)

EXPECTED_FILES = {
    PACKAGE_ROOT / "__init__.py",
    PACKAGE_ROOT / "template_mapper.py",
    PACKAGE_ROOT / "navigation.py",
    PACKAGE_ROOT / "page_renderer.py",
    PACKAGE_ROOT / "wiring.py",
    PACKAGE_ROOT / "checkpoint_store.py",
    PACKAGE_ROOT / "dashboard" / "__init__.py",
    PACKAGE_ROOT / "dashboard" / "routes.py",
    PACKAGE_ROOT / "dashboard" / "controller.py",
    PACKAGE_ROOT / "dashboard" / "dependency_provider.py",
    PACKAGE_ROOT / "session" / "__init__.py",
    PACKAGE_ROOT / "session" / "routes.py",
    PACKAGE_ROOT / "session" / "controller.py",
    PACKAGE_ROOT / "reflection" / "__init__.py",
    PACKAGE_ROOT / "reflection" / "routes.py",
    PACKAGE_ROOT / "reflection" / "controller.py",
    PACKAGE_ROOT / "mission" / "__init__.py",
    PACKAGE_ROOT / "mission" / "routes.py",
    PACKAGE_ROOT / "mission" / "controller.py",
    PACKAGE_ROOT / "login" / "__init__.py",
    PACKAGE_ROOT / "login" / "routes.py",
    PACKAGE_ROOT / "auth" / "__init__.py",
    PACKAGE_ROOT / "auth" / "routes.py",
    PACKAGE_ROOT / "auth" / "controller.py",
    PACKAGE_ROOT / "auth" / "dependency_provider.py",
    PACKAGE_ROOT / "auth" / "factory.py",
    PACKAGE_ROOT / "auth" / "secure_cookies.py",
    PACKAGE_ROOT / "auth" / "csrf.py",
    PACKAGE_ROOT / "rendering" / "__init__.py",
    PACKAGE_ROOT / "rendering" / "html_helpers.py",
    PACKAGE_ROOT / "rendering" / "token_renderer.py",
    PACKAGE_ROOT / "rendering" / "style_renderer.py",
    PACKAGE_ROOT / "rendering" / "accessibility_renderer.py",
    PACKAGE_ROOT / "rendering" / "component_renderer.py",
}

EXPECTED_COMPONENT_TEMPLATES = {
    PACKAGE_ROOT / "rendering" / "templates" / "components" / "page_header.html",
    PACKAGE_ROOT / "rendering" / "templates" / "components" / "mission_card.html",
    PACKAGE_ROOT / "rendering" / "templates" / "components" / "section.html",
    PACKAGE_ROOT / "rendering" / "templates" / "components" / "progress_bar.html",
    PACKAGE_ROOT / "rendering" / "templates" / "components" / "badge.html",
    PACKAGE_ROOT / "rendering" / "templates" / "components" / "timeline.html",
    PACKAGE_ROOT / "rendering" / "templates" / "components" / "primary_button.html",
    PACKAGE_ROOT / "rendering" / "templates" / "components" / "secondary_button.html",
    PACKAGE_ROOT / "rendering" / "templates" / "components" / "achievement_card.html",
    PACKAGE_ROOT / "rendering" / "templates" / "components" / "statistic_card.html",
}

EXPECTED_PAGE_TEMPLATES = {
    PACKAGE_ROOT / "rendering" / "templates" / "eos" / "base.html",
    PACKAGE_ROOT / "rendering" / "templates" / "eos" / "login.html",
    PACKAGE_ROOT / "rendering" / "templates" / "eos" / "dashboard.html",
    PACKAGE_ROOT / "rendering" / "templates" / "eos" / "mission.html",
    PACKAGE_ROOT / "rendering" / "templates" / "eos" / "session.html",
    PACKAGE_ROOT / "rendering" / "templates" / "eos" / "reflection.html",
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
    for path in EXPECTED_FILES:
        assert path.is_file(), f"missing {path.relative_to(PACKAGE_ROOT.parent)}"
    for path in EXPECTED_COMPONENT_TEMPLATES:
        assert path.is_file(), f"missing {path.relative_to(PACKAGE_ROOT.parent)}"
    for path in EXPECTED_PAGE_TEMPLATES:
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
    "relative",
    sorted(FLASK_FREE_RELATIVE),
)
def test_controllers_and_mapper_forbid_flask(relative: str) -> None:
    path = PACKAGE_ROOT / relative
    imported = _imported_modules(path)
    # Jinja2 is permitted inside the Design System renderer (markup only).
    forbidden = set(CONTROLLER_FORBIDDEN)
    forbidden_prefixes = list(CONTROLLER_FORBIDDEN_PREFIXES)
    if relative.startswith("rendering/"):
        forbidden.discard("jinja2")
        forbidden_prefixes = [
            prefix for prefix in forbidden_prefixes if not prefix.startswith("jinja2")
        ]
    for name in imported:
        assert name not in forbidden, f"{relative} imports {name}"
        assert not any(
            name == prefix.rstrip(".") or name.startswith(prefix)
            for prefix in forbidden_prefixes
        ), f"{relative} imports forbidden module {name}"


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
def test_no_persistence_or_ai_code(path: Path) -> None:
    source = path.read_text(encoding="utf-8").lower()
    for fragment in (
        "create_engine",
        "sessionmaker",
        "sqlite3.connect",
        "psycopg",
        "openai",
        "anthropic",
        "session.add",
        "uow.commit",
    ):
        assert fragment not in source, f"{path.name} contains {fragment}"


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
    "relative_path",
    (
        "dashboard/routes.py",
        "session/routes.py",
        "reflection/routes.py",
        "mission/routes.py",
        "login/routes.py",
    ),
)
def test_route_handlers_stay_thin(relative_path: str) -> None:
    routes = PACKAGE_ROOT / relative_path
    tree = ast.parse(routes.read_text(encoding="utf-8"), filename=str(routes))
    for node in tree.body:
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            if node.name.startswith("register_"):
                continue
            line_count = node.end_lineno - node.lineno + 1  # type: ignore[operator]
            assert line_count <= 45, f"{node.name} is {line_count} lines (max 45)"


def test_public_exports() -> None:
    from adapters.flask import (
        AccessibilityRenderer,
        AdapterDependencies,
        ComponentRenderer,
        DashboardController,
        FlaskDependencyProvider,
        MissionController,
        PageRenderer,
        ReflectionController,
        SessionController,
        StyleRenderer,
        TemplateMapper,
        TokenRenderer,
        dashboard_bp,
        login_bp,
        mission_bp,
        reflection_bp,
        register_adapter_blueprints,
        session_bp,
        wire_adapter_layer,
    )

    assert DashboardController is not None
    assert SessionController is not None
    assert ReflectionController is not None
    assert MissionController is not None
    assert TemplateMapper is not None
    assert PageRenderer is not None
    assert ComponentRenderer is not None
    assert StyleRenderer is not None
    assert TokenRenderer is not None
    assert AccessibilityRenderer is not None
    assert AdapterDependencies is not None
    assert FlaskDependencyProvider is not None
    assert dashboard_bp is not None
    assert session_bp is not None
    assert reflection_bp is not None
    assert mission_bp is not None
    assert login_bp is not None
    assert callable(register_adapter_blueprints)
    assert callable(wire_adapter_layer)
