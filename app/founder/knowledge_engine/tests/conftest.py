"""Shared fixtures for Knowledge Engine tests (FSI-001)."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.founder.knowledge_engine.tests.helpers import build_knowledge_fixture


@pytest.fixture
def knowledge_repo(tmp_path: Path) -> Path:
    """Temporary repository with a deterministic Knowledge Engine fixture."""
    return build_knowledge_fixture(tmp_path / "repo")
