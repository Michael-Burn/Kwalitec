"""Shared fixtures for Internal Alpha Live Workflow tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.founder.internal_alpha_workflow.tests.helpers import (
    build_internal_alpha_root,
    build_week,
)


@pytest.fixture
def alpha_root(tmp_path: Path) -> Path:
    return build_internal_alpha_root(tmp_path)


@pytest.fixture
def week_001(alpha_root: Path) -> Path:
    return build_week(alpha_root, "week_001")
