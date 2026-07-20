"""Educational Pipeline performs orchestration only (APP-003)."""

from __future__ import annotations

import pytest

from tests.architecture import (
    APPLICATION_ROOT,
    FRAMEWORK_MODULES,
    PIPELINE_ORCHESTRATION_FORBIDDEN_METHODS,
    defined_function_names,
    imported_modules,
    iter_python_files,
    top_level_name,
)

PIPELINE_ROOT = APPLICATION_ROOT / "pipeline"


@pytest.mark.parametrize(
    "path",
    iter_python_files(PIPELINE_ROOT),
    ids=lambda p: str(p.relative_to(PIPELINE_ROOT)),
)
def test_pipeline_defines_no_educational_intelligence_methods(path) -> None:
    defined = defined_function_names(path)
    for name in PIPELINE_ORCHESTRATION_FORBIDDEN_METHODS:
        assert name not in defined, f"{path.name} defines educational method {name}"


@pytest.mark.parametrize(
    "path",
    iter_python_files(PIPELINE_ROOT),
    ids=lambda p: str(p.relative_to(PIPELINE_ROOT)),
)
def test_pipeline_imports_no_flask_or_orm(path) -> None:
    for name in imported_modules(path):
        assert top_level_name(name) not in FRAMEWORK_MODULES, (
            f"{path.name} imports {name}"
        )
        assert not name.startswith("sqlalchemy."), f"{path.name} imports {name}"
        assert top_level_name(name) != "infrastructure", (
            f"{path.name} imports infrastructure ({name})"
        )


@pytest.mark.parametrize(
    "path",
    iter_python_files(PIPELINE_ROOT),
    ids=lambda p: str(p.relative_to(PIPELINE_ROOT)),
)
def test_pipeline_has_no_persistence_construction(path) -> None:
    source = path.read_text(encoding="utf-8").lower()
    for fragment in ("create_engine", "sessionmaker", "flask.request", "blueprint("):
        assert fragment not in source, f"{path.name} contains {fragment}"
