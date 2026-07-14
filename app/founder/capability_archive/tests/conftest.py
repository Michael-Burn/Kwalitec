"""Shared fixtures for Capability Archive tests (FSI-001)."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.founder.capability_archive.tests.helpers import build_archive_fixture


@pytest.fixture
def archive_repo(tmp_path: Path) -> Path:
    """Temporary repository with a deterministic Capability Archive fixture."""
    return build_archive_fixture(tmp_path / "repo")
