"""Architecture purity for AP-002D1 evidence ingress."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

INGRESS_ROOT = (
    Path(__file__).resolve().parents[4]
    / "app"
    / "application"
    / "assessment_pipeline"
    / "evidence_ingress"
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
    "domain.assessment.packaging",
    "domain.assessment.aggregation",
)
FORBIDDEN_SUBSTRINGS = (
    "update_mastery",
    "EstimatedMastery",
    "AdaptiveMissionService",
    "IntelligentTutor",
)


def _iter_python_files() -> list[Path]:
    return sorted(INGRESS_ROOT.rglob("*.py"))


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


def test_ingress_package_exists() -> None:
    assert INGRESS_ROOT.is_dir()
    for name in (
        "errors.py",
        "dto.py",
        "validator.py",
        "mapper.py",
        "repository.py",
        "service.py",
        "versions.py",
    ):
        assert (INGRESS_ROOT / name).is_file()


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(INGRESS_ROOT)),
)
def test_ingress_has_no_forbidden_authority_imports(path: Path) -> None:
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


def test_ingress_does_not_modify_assessment_packaging() -> None:
    """Guard: ingress must consume DTO export, not packaging internals."""
    service = (INGRESS_ROOT / "service.py").read_text(encoding="utf-8")
    assert "EvidencePackager" not in service
    assert "EvidencePackagingService" not in service
    assert "package_session" not in service
