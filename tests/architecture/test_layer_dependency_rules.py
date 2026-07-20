"""Layer dependency purity gates (APP-003).

- Domain imports no Flask / SQLAlchemy / AI
- Application (non-composition) imports no ORM / infrastructure
- Infrastructure owns integration packages
"""

from __future__ import annotations

import pytest

from tests.architecture import (
    AI_MODULES,
    APPLICATION_ROOT,
    DOMAIN_ROOT,
    FRAMEWORK_MODULES,
    INFRASTRUCTURE_ROOT,
    imported_modules,
    is_under_composition,
    iter_python_files,
    module_matches,
    top_level_name,
)

DOMAIN_FORBIDDEN_PREFIXES = (
    "flask",
    "sqlalchemy",
    "alembic",
    "jinja2",
    "wtforms",
    "application",
    "infrastructure",
    "web",
    "app",
    *AI_MODULES,
)

APPLICATION_FORBIDDEN_PREFIXES = (
    "flask",
    "sqlalchemy",
    "alembic",
    "infrastructure",
    "web",
    "app",
    *AI_MODULES,
)


@pytest.mark.parametrize(
    "path",
    iter_python_files(DOMAIN_ROOT),
    ids=lambda p: str(p.relative_to(DOMAIN_ROOT)),
)
def test_domain_imports_no_flask(path) -> None:
    for name in imported_modules(path):
        assert top_level_name(name) != "flask", f"{path} imports {name}"
        assert not name.startswith("flask."), f"{path} imports {name}"


@pytest.mark.parametrize(
    "path",
    iter_python_files(DOMAIN_ROOT),
    ids=lambda p: str(p.relative_to(DOMAIN_ROOT)),
)
def test_domain_imports_no_sqlalchemy(path) -> None:
    for name in imported_modules(path):
        assert top_level_name(name) != "sqlalchemy", f"{path} imports {name}"
        assert not name.startswith("sqlalchemy."), f"{path} imports {name}"
        assert top_level_name(name) != "alembic", f"{path} imports {name}"


@pytest.mark.parametrize(
    "path",
    iter_python_files(DOMAIN_ROOT),
    ids=lambda p: str(p.relative_to(DOMAIN_ROOT)),
)
def test_domain_imports_no_ai(path) -> None:
    for name in imported_modules(path):
        assert not module_matches(name, AI_MODULES), f"{path} imports AI ({name})"
        assert top_level_name(name) != "infrastructure", (
            f"{path} imports infrastructure ({name})"
        )
        assert not name.startswith("infrastructure.ai"), f"{path} imports {name}"


@pytest.mark.parametrize(
    "path",
    iter_python_files(DOMAIN_ROOT),
    ids=lambda p: str(p.relative_to(DOMAIN_ROOT)),
)
def test_domain_imports_no_outer_layers(path) -> None:
    for name in imported_modules(path):
        for prefix in DOMAIN_FORBIDDEN_PREFIXES:
            assert not (
                name == prefix or name.startswith(prefix + ".")
            ), f"{path} imports forbidden module {name}"


def test_application_imports_no_orm_outside_composition() -> None:
    for path in iter_python_files(APPLICATION_ROOT):
        if is_under_composition(path, APPLICATION_ROOT):
            continue
        for name in imported_modules(path):
            assert top_level_name(name) not in FRAMEWORK_MODULES, (
                f"{path} imports framework/ORM ({name})"
            )
            assert not name.startswith("sqlalchemy."), f"{path} imports {name}"
            assert top_level_name(name) != "infrastructure", (
                f"application business module {path} imports infrastructure ({name})"
            )
            for prefix in APPLICATION_FORBIDDEN_PREFIXES:
                assert not (
                    name == prefix or name.startswith(prefix + ".")
                ), f"{path} imports forbidden module {name}"


def test_infrastructure_owns_integrations() -> None:
    """Integration packages must live under infrastructure, not domain/application."""
    ai_root = INFRASTRUCTURE_ROOT / "ai"
    persistence_root = INFRASTRUCTURE_ROOT / "persistence"
    assert ai_root.is_dir(), "infrastructure.ai must own AI integrations"
    assert persistence_root.is_dir(), (
        "infrastructure.persistence must own persistence integrations"
    )
    assert not (DOMAIN_ROOT / "ai").exists()
    assert not (APPLICATION_ROOT / "ai").exists()
    assert not (DOMAIN_ROOT / "persistence").exists()

    assert any(ai_root.rglob("*.py")), "AI integration package is empty"
