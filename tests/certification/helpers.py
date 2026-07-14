"""Shared helpers for FSI-005 Operational Certification."""

from __future__ import annotations

import ast
import time
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.founder.capability_archive.tests.helpers import (
    build_archive_fixture,
    sample_entry,
    write_entry,
)
from app.founder.internal_alpha_workflow.tests.helpers import (
    build_week,
    make_workflow_service,
)
from app.founder.knowledge_engine.tests.helpers import (
    build_knowledge_fixture,
    write_markdown,
)
from app.founder.operational_state.providers import (
    CapabilityArchiveProvider,
    CapabilityProvider,
    InternalAlphaProvider,
    KnowledgeProvider,
    KnowledgeQueryProvider,
    StaticCapabilitySource,
    StaticInternalAlphaSource,
    StaticKnowledgeSource,
)
from app.founder.operational_state.tests.helpers import (
    make_alpha_dto,
    make_capability_dto,
    make_knowledge_dto,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
FOUNDER_ROOT = REPO_ROOT / "app" / "founder"
AUTOMATION_ROOT = REPO_ROOT / "app" / "automation"
KNOWLEDGE_ROOT = REPO_ROOT / "knowledge"

CERT_NOW = datetime(2026, 7, 14, 19, 0, 0, tzinfo=UTC)

# Soft upper bounds — fail if exceeded; tune only with Architecture Office.
PERF_BUDGETS_MS: dict[str, float] = {
    "knowledge_indexing": 5_000.0,
    "operational_state": 2_000.0,
    "recommendations": 1_000.0,
    "weekly_briefing": 1_000.0,
    "dashboard_service": 1_000.0,
    "automation_execution": 15_000.0,
}


@dataclass(frozen=True)
class TimedResult:
    """Outcome of a timed certification measurement."""

    name: str
    duration_ms: float
    budget_ms: float
    detail: dict[str, Any]

    @property
    def within_budget(self) -> bool:
        return self.duration_ms <= self.budget_ms


def time_call(
    name: str,
    fn: Callable[[], Any],
    *,
    budget_ms: float | None = None,
) -> tuple[Any, TimedResult]:
    """Execute ``fn`` and return ``(result, timing)``."""

    budget = budget_ms if budget_ms is not None else PERF_BUDGETS_MS[name]
    started = time.perf_counter()
    value = fn()
    elapsed_ms = (time.perf_counter() - started) * 1000.0
    return value, TimedResult(
        name=name,
        duration_ms=elapsed_ms,
        budget_ms=budget,
        detail={},
    )


def build_combined_fixture(tmp_path: Path) -> Path:
    """Knowledge + Capability Archive fixtures under one repo root."""

    root = tmp_path / "cert_repo"
    build_knowledge_fixture(root)
    build_archive_fixture(root)
    return root


def build_full_cert_fixture(tmp_path: Path) -> tuple[Path, Path]:
    """Combined knowledge/archive fixture plus Internal Alpha week root.

    Returns:
        ``(repo_root, internal_alpha_root)``
    """

    repo = build_combined_fixture(tmp_path)
    alpha_root = repo / "research" / "internal_alpha"
    alpha_root.mkdir(parents=True, exist_ok=True)
    build_week(alpha_root, "week_001", with_feedback=True, with_output_dirs=True)
    return repo, alpha_root


def iter_python_files(root: Path) -> Iterator[Path]:
    """Yield ``.py`` files under ``root``, skipping ``tests`` and caches."""

    for path in sorted(root.rglob("*.py")):
        parts = set(path.parts)
        if "__pycache__" in parts or "tests" in parts:
            continue
        yield path


def module_imports(path: Path) -> set[str]:
    """Return top-level import module names referenced by ``path``."""

    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError:
        return set()

    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
            names.add(node.module)
    return names


def package_imports(package_dir: Path) -> set[str]:
    """Union of imports across non-test modules in a package directory."""

    collected: set[str] = set()
    for path in iter_python_files(package_dir):
        collected |= module_imports(path)
    return collected


def imports_matching(imports: set[str], prefix: str) -> set[str]:
    """Filter imports that equal or start with ``prefix``."""

    return {
        name
        for name in imports
        if name == prefix or name.startswith(prefix + ".")
    }


def live_state_providers(repo_root: Path):
    """Build live Knowledge + Archive providers against a fixture repo."""

    return {
        "knowledge": KnowledgeQueryProvider(repo_root=repo_root),
        "capability": CapabilityArchiveProvider(repo_root=repo_root),
        "internal_alpha": InternalAlphaProvider(
            StaticInternalAlphaSource(make_alpha_dto())
        ),
    }


def static_state_providers():
    """Static providers for fast deterministic certification paths."""

    return {
        "knowledge": KnowledgeProvider(
            StaticKnowledgeSource(make_knowledge_dto())
        ),
        "capability": CapabilityProvider(
            StaticCapabilitySource(make_capability_dto())
        ),
        "internal_alpha": InternalAlphaProvider(
            StaticInternalAlphaSource(make_alpha_dto())
        ),
    }


def write_corrupt_archive_entry(entries_dir: Path) -> Path:
    """Write an unreadable JSON archive entry; return its path."""

    path = entries_dir / "CORRUPT.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{not-valid-json", encoding="utf-8")
    return path


def write_duplicate_archive_entries(entries_dir: Path) -> None:
    """Write two entries that share the same capability_id."""

    write_entry(
        entries_dir / "DUP-A.json",
        sample_entry(capability_id="DUP-001", title="Duplicate A"),
    )
    write_entry(
        entries_dir / "DUP-B.json",
        sample_entry(capability_id="DUP-001", title="Duplicate B"),
    )


def enrich_knowledge_fixture(root: Path) -> None:
    """Add extra markdown so indexing has a realistic small corpus."""

    write_markdown(
        root / "knowledge" / "engineering" / "handbook" / "ENG-001.md",
        title="Engineering Handbook",
        document_id="ENG-001",
    )
    write_markdown(
        root / "knowledge" / "founder" / "FSI-005_OPERATIONAL_CERTIFICATION.md",
        title="FSI-005 Certification",
        document_id="FSI-005",
    )


__all__ = [
    "AUTOMATION_ROOT",
    "CERT_NOW",
    "FOUNDER_ROOT",
    "KNOWLEDGE_ROOT",
    "PERF_BUDGETS_MS",
    "REPO_ROOT",
    "TimedResult",
    "build_combined_fixture",
    "build_full_cert_fixture",
    "enrich_knowledge_fixture",
    "imports_matching",
    "iter_python_files",
    "live_state_providers",
    "make_workflow_service",
    "module_imports",
    "package_imports",
    "static_state_providers",
    "time_call",
    "write_corrupt_archive_entry",
    "write_duplicate_archive_entries",
]
