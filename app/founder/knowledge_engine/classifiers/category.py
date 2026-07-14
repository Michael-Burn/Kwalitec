"""Classify indexed artefacts into logical Knowledge Engine collections."""

from __future__ import annotations

from pathlib import Path

from app.founder.knowledge_engine.config import (
    COLLECTION_ADR,
    COLLECTION_ARCHITECTURE,
    COLLECTION_COMPLETION_REPORT,
    COLLECTION_ENGINEERING,
    COLLECTION_ENGINEERING_STANDARDS,
    COLLECTION_FOUNDER_CAPABILITY,
    COLLECTION_OTHER,
    COLLECTION_RESEARCH,
)


def classify_relative_path(relative: Path) -> str:
    """Map a repo-relative path to a logical collection name.

    Args:
        relative: Path relative to the repository root (internal only).

    Returns:
        Logical collection identifier (never a filesystem path).
    """
    parts = relative.as_posix().lower().split("/")
    name = relative.name.lower()
    stem = relative.stem.lower()

    if "research" in parts[:1] or parts[:1] == ["research"]:
        return COLLECTION_RESEARCH

    if name.startswith("adr-") or "/adr-" in relative.as_posix().lower():
        return COLLECTION_ADR

    if "completion" in stem and "review" in stem:
        return COLLECTION_COMPLETION_REPORT
    if parts[:2] == ["docs", "reviews"] and "completion" in stem:
        return COLLECTION_COMPLETION_REPORT

    if parts[:2] == ["knowledge", "engineering"] and "standards" in parts:
        if name.startswith("readme"):
            return COLLECTION_ENGINEERING
        return COLLECTION_ENGINEERING_STANDARDS

    if parts[:2] == ["knowledge", "engineering"]:
        return COLLECTION_ENGINEERING

    if parts[:2] == ["knowledge", "architecture"] or parts[:2] == [
        "docs",
        "architecture",
    ]:
        return COLLECTION_ARCHITECTURE

    if parts[:2] == ["knowledge", "founder"] or stem.startswith(
        ("fos-", "fsi-", "capability_")
    ):
        return COLLECTION_FOUNDER_CAPABILITY

    if parts[:1] == ["docs"] and "architecture" in parts:
        return COLLECTION_ARCHITECTURE

    if parts[:1] == ["knowledge"]:
        return COLLECTION_OTHER

    return COLLECTION_OTHER
