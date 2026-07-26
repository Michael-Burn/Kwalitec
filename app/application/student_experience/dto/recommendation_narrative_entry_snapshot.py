"""Immutable recommendation-history narrative entry (EP-008.3)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RecommendationNarrativeEntrySnapshot:
    """One educational history entry — not an audit log row."""

    kind: str = ""  # completed | deferred | committed_incomplete
    title: str = ""
    occurred_at: str = ""
    summary_line: str = ""
    reason_label: str = ""
