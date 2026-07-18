"""Immutable ExplanationSnapshot DTO for Student Experience."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ExplanationSnapshot:
    """Student-safe recommendation explanation DTO."""

    summary: str = ""
    why_recommended: str = ""
    evidence_points: tuple[str, ...] = field(default_factory=tuple)
    expected_benefit: str = ""
    confidence_label: str = ""
    is_complete: bool = False
