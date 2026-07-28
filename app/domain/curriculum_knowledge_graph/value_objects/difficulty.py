"""Relative educational difficulty band for CKG nodes."""

from __future__ import annotations

from enum import StrEnum


class DifficultyBand(StrEnum):
    """Relative difficulty posture within a curriculum graph."""

    FOUNDATIONAL = "foundational"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    CAPSTONE = "capstone"
