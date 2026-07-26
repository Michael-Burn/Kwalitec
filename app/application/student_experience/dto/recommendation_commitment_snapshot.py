"""Immutable recommendation-commitment DTO (EP-008.3)."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.student_experience.dto.commitment_reflection_snapshot import (
    CommitmentReflectionSnapshot,
)


@dataclass(frozen=True)
class RecommendationCommitmentSnapshot:
    """Student-visible commitment / defer state for one tip (preference only)."""

    state: str = "offered"
    recommendation_key: str = ""
    title: str = ""
    committed_at: str = ""
    deferred_reason_code: str = ""
    deferred_reason_label: str = ""
    continuity_line: str = ""
    reflection: CommitmentReflectionSnapshot | None = None
    show_commit_affordance: bool = False
    show_defer_affordance: bool = False
