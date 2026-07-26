"""Immutable ExplanationSnapshot DTO for Student Experience.

EP-006.2 widens the DTO so authored MES fields (next action, review point,
confidence basis) reach Home/Coach without presentation re-narration.

EP-008.1 adds trust presentation fields (coherence, refusal, timeliness,
completion loop) — still pass-through / composition of authored fragments.
"""

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
    suggested_next_action: str = ""
    review_point: str = ""
    confidence_basis: str = ""
    is_complete: bool = False
    # EP-008.1 — Recommendation Trust (defaults preserve back-compat).
    plan_coherence: str = ""
    plan_coherence_label: str = ""
    honest_refusal: bool = False
    timeliness_line: str = ""
    completion_loop_line: str = ""
