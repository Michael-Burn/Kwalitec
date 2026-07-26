"""Immutable readiness explanation DTO for Student Experience Home.

EP-006.4: carries authored ReadinessService MES fields to Home without
presentation re-narration or score recalculation.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ReadinessExplanationSnapshot:
    """Student-safe readiness explanation projection for Home."""

    why_this_estimate: str = ""
    confidence_label: str = ""
    confidence_basis: str = ""
    suggested_next_action: str = ""
    review_point: str = ""
    readiness_drivers: tuple[str, ...] = field(default_factory=tuple)
    supporting_evidence: tuple[str, ...] = field(default_factory=tuple)
    expected_benefit: str = ""
    can_estimate: bool = True
    is_complete: bool = False
