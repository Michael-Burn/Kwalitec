"""Internal Alpha subsystem DTO for operational-state aggregation."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class InternalAlphaSubsystemDTO:
    """Summary read-model from Internal Alpha pipeline outputs (FOS-003).

    Week-level counts only — never raw feedback text.
    """

    source_version: str
    current_week: str
    feedback_count: int
    duplicate_count: int
    category_counts: Mapping[str, int]
    recent_week_labels: tuple[str, ...] = ()
