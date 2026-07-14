"""Configuration for the Knowledge Engine (FOS-001) / FSI-001 integration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

SOURCE_VERSION = "knowledge-engine-1.0"

# Logical collection names — never filesystem paths.
COLLECTION_ENGINEERING_STANDARDS = "engineering_standards"
COLLECTION_ARCHITECTURE = "architecture"
COLLECTION_RESEARCH = "research"
COLLECTION_FOUNDER_CAPABILITY = "founder_capability"
COLLECTION_ADR = "adr"
COLLECTION_COMPLETION_REPORT = "completion_report"
COLLECTION_ENGINEERING = "engineering"
COLLECTION_OTHER = "other"

INDEXABLE_SUFFIXES = frozenset({".md", ".markdown"})

# Roots relative to repository root (scanned only; never exposed in DTOs).
DEFAULT_SCAN_ROOTS: tuple[str, ...] = (
    "knowledge",
    "research",
    "docs/architecture",
    "docs/reviews",
)

SKIP_DIR_NAMES = frozenset(
    {
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
    }
)


@dataclass(frozen=True)
class KnowledgeEngineConfig:
    """Immutable Knowledge Engine scan configuration."""

    source_version: str = SOURCE_VERSION
    scan_roots: tuple[str, ...] = DEFAULT_SCAN_ROOTS
    indexable_suffixes: frozenset[str] = INDEXABLE_SUFFIXES
    skip_dir_names: frozenset[str] = SKIP_DIR_NAMES


def default_config() -> KnowledgeEngineConfig:
    """Return the Version 1 default Knowledge Engine configuration."""
    return KnowledgeEngineConfig()


def discover_repo_root(start: Path | None = None) -> Path:
    """Locate the repository root by walking upward from ``start``.

    Looks for ``pyproject.toml`` alongside an ``app/`` directory.

    Args:
        start: Path to begin the search (defaults to this module).

    Returns:
        Absolute path to the repository root.

    Raises:
        FileNotFoundError: When no repository root can be located.
    """
    cursor = (start or Path(__file__)).resolve()
    if cursor.is_file():
        cursor = cursor.parent
    for candidate in (cursor, *cursor.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / "app").is_dir():
            return candidate
    raise FileNotFoundError(
        "Unable to locate repository root (pyproject.toml + app/)."
    )
