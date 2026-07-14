"""Pytest fixtures for FSI-005 Operational Certification."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.certification.helpers import (
    CERT_NOW,
    build_combined_fixture,
    build_full_cert_fixture,
)


@pytest.fixture
def cert_repo(tmp_path: Path) -> Path:
    """Temporary repo with Knowledge Engine + Capability Archive fixtures."""

    return build_combined_fixture(tmp_path)


@pytest.fixture
def cert_full(tmp_path: Path) -> tuple[Path, Path]:
    """Temporary repo plus Internal Alpha week layout."""

    return build_full_cert_fixture(tmp_path)


@pytest.fixture
def cert_now():
    """Fixed clock for deterministic certification runs."""

    return CERT_NOW
