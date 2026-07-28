"""Architecture purity for assessment evidence packaging."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

DOMAIN_ROOT = Path(__file__).resolve().parents[4] / "src" / "domain" / "assessment"

FORBIDDEN_MODULES = frozenset(
    {
        "flask",
        "sqlalchemy",
        "alembic",
        "jinja2",
        "wtforms",
        "requests",
        "httpx",
    }
)
FORBIDDEN_PREFIXES = (
    "flask.",
    "sqlalchemy.",
    "app.",
    "infrastructure.",
    "application.",
)
FORBIDDEN_SUBSTRINGS = (
    "student_reasoning",
    "StudentReasoningService",
    "digital_twin",
    "mission_engine",
    "tutor",
)


def _iter_python_files() -> list[Path]:
    paths: list[Path] = []
    for sub in ("evidence", "packaging", "aggregation"):
        root = DOMAIN_ROOT / sub
        paths.extend(sorted(root.rglob("*.py")))
    return paths


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


def test_evidence_packaging_packages_exist() -> None:
    for expected in ("evidence", "packaging", "aggregation"):
        assert (DOMAIN_ROOT / expected).is_dir()


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(DOMAIN_ROOT)),
)
def test_evidence_packages_have_no_forbidden_imports(path: Path) -> None:
    imported = _imported_modules(path)
    text = path.read_text(encoding="utf-8")
    for name in imported:
        assert name not in FORBIDDEN_MODULES, f"{path} imports {name}"
        assert not any(
            name == prefix.rstrip(".") or name.startswith(prefix)
            for prefix in FORBIDDEN_PREFIXES
        ), f"{path} imports {name}"
    for needle in FORBIDDEN_SUBSTRINGS:
        assert needle not in text or needle in (
            # allow documentary mentions in module docstrings only via negative check
            ""
        )
    # Hard ban on Reasoning / Twin / Mission / Tutor invocation patterns
    assert "StudentReasoningService" not in text
    assert "update_mastery" not in text
    assert "EstimatedMastery" not in text
