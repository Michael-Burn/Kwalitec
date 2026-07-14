"""Test helpers for Knowledge Engine integration tests (FSI-001)."""

from __future__ import annotations

from pathlib import Path


def write_markdown(
    path: Path,
    *,
    title: str,
    document_id: str = "",
    body: str = "Content.",
) -> None:
    """Write a deterministic markdown artefact for fixture repos."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {title}", ""]
    if document_id:
        lines.extend([f"**Document ID:** {document_id}", ""])
    lines.extend(["---", "", body, ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def build_knowledge_fixture(root: Path) -> Path:
    """Create a minimal repository layout for Knowledge Engine tests.

    Returns:
        The fixture repository root.
    """
    write_markdown(
        root / "knowledge" / "engineering" / "standards" / "ENG-001.md",
        title="Engineering Handbook",
        document_id="ENG-001",
    )
    write_markdown(
        root / "knowledge" / "architecture" / "ADR-001-service-layer.md",
        title="ADR-001 Service Layer",
        document_id="ADR-001",
    )
    write_markdown(
        root / "knowledge" / "founder" / "FOS-003_INTERNAL_ALPHA_PIPELINE.md",
        title="FOS-003 Internal Alpha",
        document_id="FOS-003",
    )
    write_markdown(
        root / "research" / "notes" / "alpha-findings.md",
        title="Alpha Findings",
        document_id="RES-001",
    )
    write_markdown(
        root / "docs" / "architecture" / "ADR-002-example.md",
        title="ADR-002 Example",
        document_id="ADR-002",
    )
    write_markdown(
        root / "docs" / "reviews" / "EPIC_1_COMPLETION_REVIEW.md",
        title="Epic 1 Completion Review",
    )
    # Marker files so discover_repo_root works when pointing at the fixture.
    (root / "pyproject.toml").write_text(
        '[project]\nname = "fixture"\n', encoding="utf-8"
    )
    (root / "app").mkdir(exist_ok=True)
    (root / "app" / "__init__.py").write_text("", encoding="utf-8")
    return root
