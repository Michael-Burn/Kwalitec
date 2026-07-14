"""Configuration for the Capability Archive (FOS-002) / FSI-001 integration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

SOURCE_VERSION = "capability-archive-1.0"

# Archive entries live under this root relative to the repository.
DEFAULT_ARCHIVE_ROOT = "research/capability_archive"
DEFAULT_ENTRIES_DIR = "entries"

ENTRY_SUFFIXES = frozenset({".json"})

REQUIRED_FIELDS: tuple[str, ...] = (
    "capability_id",
    "status",
    "version",
    "completion_date",
    "programme",
    "subsystem",
    "related_documents",
)

COMPLETED_STATUSES = frozenset(
    {
        "completed",
        "implemented",
        "released",
        "closed",
        "version 1.0 implemented",
    }
)

ACTIVE_STATUSES = frozenset(
    {
        "active",
        "in_progress",
        "approved",
        "approved for implementation",
    }
)

RECENT_CAPABILITY_LIMIT = 10


@dataclass(frozen=True)
class CapabilityArchiveConfig:
    """Immutable Capability Archive scan configuration."""

    source_version: str = SOURCE_VERSION
    archive_root: str = DEFAULT_ARCHIVE_ROOT
    entries_dir: str = DEFAULT_ENTRIES_DIR
    entry_suffixes: frozenset[str] = ENTRY_SUFFIXES
    required_fields: tuple[str, ...] = REQUIRED_FIELDS
    completed_statuses: frozenset[str] = COMPLETED_STATUSES
    active_statuses: frozenset[str] = ACTIVE_STATUSES
    recent_limit: int = RECENT_CAPABILITY_LIMIT
    default_release: str = "1.0.0"


def default_config() -> CapabilityArchiveConfig:
    """Return the Version 1 default Capability Archive configuration."""
    return CapabilityArchiveConfig()


def discover_repo_root(start: Path | None = None) -> Path:
    """Locate the repository root by walking upward from ``start``.

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
