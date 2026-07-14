"""Test helpers for Capability Archive integration tests (FSI-001)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_entry(path: Path, payload: dict[str, Any]) -> None:
    """Write one Capability Archive JSON entry."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def sample_entry(**overrides: Any) -> dict[str, Any]:
    """Return a complete archive entry payload."""
    base: dict[str, Any] = {
        "capability_id": "CAP-001",
        "title": "Sample Capability",
        "status": "completed",
        "version": "1.0",
        "completion_date": "2026-07-01",
        "programme": "Founder Operating System",
        "subsystem": "sample",
        "related_documents": ["FOS-003"],
    }
    base.update(overrides)
    return base


def build_archive_fixture(root: Path) -> Path:
    """Create a minimal repository with Capability Archive entries.

    Returns:
        The fixture repository root.
    """
    entries = root / "research" / "capability_archive" / "entries"
    write_entry(
        entries / "CAP-001.json",
        sample_entry(
            capability_id="CAP-001",
            status="completed",
            version="1.0",
            completion_date="2026-07-10",
        ),
    )
    write_entry(
        entries / "CAP-002.json",
        sample_entry(
            capability_id="CAP-002",
            title="Active Capability",
            status="active",
            version="0.9",
            completion_date="2026-07-12",
            subsystem="active_sub",
        ),
    )
    (root / "pyproject.toml").write_text(
        '[project]\nname = "fixture"\n', encoding="utf-8"
    )
    (root / "app").mkdir(exist_ok=True)
    (root / "app" / "__init__.py").write_text("", encoding="utf-8")
    return root
