"""Shared fixtures for Internal Alpha pipeline unit tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.founder.internal_alpha.config import (
    InternalAlphaPipelineConfig,
    default_config,
)


@pytest.fixture
def config() -> InternalAlphaPipelineConfig:
    return default_config()


@pytest.fixture
def week_dir(tmp_path: Path) -> Path:
    """Minimal valid week folder with two feedback files."""

    week = tmp_path / "2026-W28"
    raw = week / "raw_feedback"
    raw.mkdir(parents=True)
    (raw / "alice.txt").write_text(
        "The architecture layering feels unclear around services.\n",
        encoding="utf-8",
    )
    (raw / "bob.txt").write_text(
        "There is a bug causing a crash on the mission page.\n",
        encoding="utf-8",
    )
    return week
