"""Immutable alternative-recommendation DTO for trust presentation (EP-008.1)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RecommendationAlternativeSnapshot:
    """One Runtime A alternative tip — informational agency only (no re-rank)."""

    title: str = ""
    why_recommended: str = ""
    expected_benefit: str = ""
    suggested_next_action: str = ""
