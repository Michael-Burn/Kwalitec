"""Architecture purity for AP-002D educational reasoning (D2/D3)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

DOMAIN_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "domain"
    / "reasoning"
)
APPLICATION_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "application"
    / "reasoning"
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
    "app.application.learning_graph",
    "domain.assessment.packaging",
    "domain.assessment.aggregation",
)
FORBIDDEN_SUBSTRINGS = (
    "update_mastery",
    "EstimatedMastery",
    "AdaptiveMissionService",
    "IntelligentTutor",
    "MasteryService",
    "KnowledgeGapService",
    "RecommendationService",
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


def test_required_structure_exists() -> None:
    assert DOMAIN_ROOT.is_dir()
    assert (DOMAIN_ROOT / "observations").is_dir()
    assert (DOMAIN_ROOT / "interpretation").is_dir()
    assert (DOMAIN_ROOT / "decisions").is_dir()
    assert APPLICATION_ROOT.is_dir()
    for name in ("interpretation", "builders", "dto", "mappers", "decisions"):
        assert (APPLICATION_ROOT / name).is_dir()
    assert (
        APPLICATION_ROOT / "interpretation" / "evidence_interpreter.py"
    ).is_file()
    assert (
        APPLICATION_ROOT / "interpretation" / "observation_interpreter.py"
    ).is_file()
    assert (APPLICATION_ROOT / "builders" / "observation_builder.py").is_file()
    assert (APPLICATION_ROOT / "builders" / "decision_builder.py").is_file()
    assert (APPLICATION_ROOT / "decisions" / "decision_generator.py").is_file()
    assert (APPLICATION_ROOT / "decisions" / "twin_updater.py").is_file()
    assert (APPLICATION_ROOT / "decisions" / "validator.py").is_file()


@pytest.mark.parametrize(
    "path",
    _iter_python_files(DOMAIN_ROOT) + _iter_python_files(APPLICATION_ROOT),
    ids=lambda p: str(
        p.relative_to(DOMAIN_ROOT.parent.parent)
        if DOMAIN_ROOT.parent.parent in p.parents
        else p
    ),
)
def test_reasoning_packages_have_no_forbidden_authority_imports(path: Path) -> None:
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


def test_interpretation_does_not_import_twin_persistence() -> None:
    for path in _iter_python_files(APPLICATION_ROOT):
        imported = _imported_modules(path)
        for name in imported:
            assert "twin.persistence" not in name
            assert not name.endswith("TwinPersistenceService")
            assert "observation_service" not in name


def test_domain_does_not_import_application() -> None:
    for path in _iter_python_files(DOMAIN_ROOT):
        for name in _imported_modules(path):
            assert not name.startswith("app.application."), path
            assert not name.startswith("application."), path


def test_decision_pipeline_does_not_touch_learning_graph_or_mission() -> None:
    twin_updater = APPLICATION_ROOT / "decisions" / "twin_updater.py"
    generator = APPLICATION_ROOT / "decisions" / "decision_generator.py"
    for path in (twin_updater, generator):
        text = path.read_text(encoding="utf-8")
        imported = _imported_modules(path)
        assert not any("learning_graph" in name for name in imported)
        assert not any("mission" in name.lower() for name in imported)
        assert "RecommendationService" not in text
        assert "AdaptiveMissionService" not in text
        assert "IntelligentTutor" not in text
