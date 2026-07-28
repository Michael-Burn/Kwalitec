"""Architecture purity for AP-002D4 Learning Graph projection."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

DOMAIN_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "domain"
    / "learning_graph"
    / "projections"
)
APPLICATION_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "application"
    / "learning_graph"
    / "projections"
)

FORBIDDEN_MODULES = frozenset(
    {
        "flask",
        "jinja2",
        "wtforms",
        "requests",
        "httpx",
    }
)
FORBIDDEN_PREFIXES = (
    "app.presentation.",
    "app.templates",
    "app.mission.",
    "app.application.adaptive_mission",
    "app.application.intelligent_tutor",
    "app.application.mission_engine",
    "app.application.assessment",
    "domain.assessment.packaging",
    "domain.assessment.aggregation",
)
FORBIDDEN_SUBSTRINGS = (
    "AdaptiveMissionService",
    "IntelligentTutor",
    "StudentReasoningService",
    "RecommendationService",
    "KnowledgeGapService",
)


def _iter_python_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.py"))


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


def test_required_projection_structure_exists() -> None:
    assert DOMAIN_ROOT.is_dir()
    assert APPLICATION_ROOT.is_dir()
    for name in (
        "relationship_type.py",
        "relationship.py",
        "projection.py",
        "batch.py",
        "context.py",
        "reference.py",
        "result.py",
        "events.py",
        "version.py",
        "errors.py",
    ):
        assert (DOMAIN_ROOT / name).is_file(), name
    for name in (
        "twin_projection_service.py",
        "relationship_builder.py",
        "validator.py",
        "persistence.py",
        "versions.py",
    ):
        assert (APPLICATION_ROOT / name).is_file(), name
    assert (
        Path(__file__).resolve().parents[3]
        / "app"
        / "application"
        / "learning_graph"
        / "dto"
        / "projection_dto.py"
    ).is_file()
    assert (
        Path(__file__).resolve().parents[3]
        / "app"
        / "application"
        / "learning_graph"
        / "mappers"
        / "projection_mapper.py"
    ).is_file()


@pytest.mark.parametrize(
    "path",
    _iter_python_files(DOMAIN_ROOT) + _iter_python_files(APPLICATION_ROOT),
    ids=lambda p: str(p.relative_to(p.parents[4])),
)
def test_projection_packages_have_no_forbidden_authority_imports(path: Path) -> None:
    imported = _imported_modules(path)
    text = path.read_text(encoding="utf-8")
    for name in imported:
        assert name not in FORBIDDEN_MODULES, f"{path} imports {name}"
        assert not any(
            name == prefix.rstrip(".") or name.startswith(prefix)
            for prefix in FORBIDDEN_PREFIXES
        ), f"{path} imports {name}"
    for needle in FORBIDDEN_SUBSTRINGS:
        assert needle not in text, f"{path} contains forbidden {needle}"


def test_domain_projections_do_not_import_application() -> None:
    for path in _iter_python_files(DOMAIN_ROOT):
        for name in _imported_modules(path):
            assert not name.startswith("app.application."), path
            assert not name.startswith("application."), path


def test_projection_does_not_write_twin_belief() -> None:
    service = APPLICATION_ROOT / "twin_projection_service.py"
    text = service.read_text(encoding="utf-8")
    assert "with_inferences" not in text
    assert "TwinUpdater" not in text
    assert "MasteryService" not in text
