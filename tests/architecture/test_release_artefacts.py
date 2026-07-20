"""Release artefacts required to close Version 2 (APP-004)."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_ARTEFACTS = (
    REPO_ROOT / "VERSION",
    REPO_ROOT / "CHANGELOG.md",
    REPO_ROOT / "RELEASE_NOTES_V2.md",
    REPO_ROOT / "ROADMAP_V3.md",
    REPO_ROOT / "docs" / "release" / "V2_RELEASE_CHECKLIST.md",
    REPO_ROOT / "docs" / "release" / "DEPENDENCY_AUDIT_V2.md",
)


@pytest.mark.parametrize("path", REQUIRED_ARTEFACTS, ids=lambda p: p.name)
def test_v2_release_artefacts_exist(path: Path) -> None:
    assert path.is_file(), f"missing release artefact {path}"
    assert path.stat().st_size > 0, f"{path.name} appears empty"


def test_version_file_is_v2() -> None:
    text = (REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    assert text == "2.0.0"


def test_release_notes_reference_v2() -> None:
    text = (REPO_ROOT / "RELEASE_NOTES_V2.md").read_text(encoding="utf-8")
    assert "2.0.0" in text
    assert "Educational Operating System" in text


def test_roadmap_v3_is_forward_looking() -> None:
    text = (REPO_ROOT / "ROADMAP_V3.md").read_text(encoding="utf-8")
    assert "Version 3" in text
    assert "Version 2" in text


def test_release_checklist_covers_gates() -> None:
    text = (REPO_ROOT / "docs" / "release" / "V2_RELEASE_CHECKLIST.md").read_text(
        encoding="utf-8"
    )
    for gate in (
        "Architecture Governance",
        "Unit tests",
        "Integration tests",
        "Lint",
        "Release build",
        "Dependency audit",
        "Health endpoints",
    ):
        assert gate in text, f"checklist missing gate: {gate}"
