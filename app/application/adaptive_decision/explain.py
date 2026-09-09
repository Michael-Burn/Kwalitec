"""Plain-language explanations for Policy V1 decisions (including SAFE_FALLBACK).

Every Policy V1 outcome must explain itself in operator-auditable prose.
Student Home surfaces ``selection_explanation`` for spaced_review and
adaptive_review; sequential SAFE_FALLBACK may keep the study-plan why-now line
while still recording ``decision_explanation`` on DECISION_RECORDED.
"""

from __future__ import annotations

from app.application.adaptive_decision.types import POLICY_V1_MIN_EVIDENCE


def explain_not_review_day(
    *,
    topics_since_last_review: int,
    days_remaining: int | None,
    cadence_threshold: float | None,
) -> str:
    """Explain deferral because exam-proximity review cadence is not met."""
    if days_remaining is None:
        return (
            "Fell back to sequential progression because no exam date is "
            "available, so Policy V1 cannot evaluate review cadence."
        )
    threshold = (
        f"{cadence_threshold:g}"
        if cadence_threshold is not None
        else "the cadence threshold"
    )
    return (
        "Fell back to sequential progression because review cadence is not "
        f"due yet ({topics_since_last_review} topic"
        f"{'' if topics_since_last_review == 1 else 's'} since last review; "
        f"threshold {threshold} with {days_remaining} day"
        f"{'' if days_remaining == 1 else 's'} remaining to exam)."
    )


def explain_insufficient_evidence(
    *,
    min_evidence: int = POLICY_V1_MIN_EVIDENCE,
    max_evidence_observed: int | None = None,
    eligible_package_count: int = 0,
) -> str:
    """Explain SAFE_FALLBACK when no revision package meets the evidence bar."""
    if eligible_package_count > 0:
        return (
            "Fell back to sequential progression because no revision package "
            "met Policy V1's evidence bar for adaptive review."
        )
    if max_evidence_observed is None:
        return (
            "Fell back to sequential progression because no covered revision "
            f"topic yet has the {min_evidence} Twin evidence observations "
            "required for a reliable adaptive review decision."
        )
    return (
        "Fell back to sequential progression because only "
        f"{max_evidence_observed} of {min_evidence} required Twin evidence "
        "observations exist for the strongest covered revision topic "
        "(none yet meet the reliability floor for adaptive review)."
    )


def explain_deferred_to_spaced_due(*, due_package_id: str) -> str:
    """Explain preserving Spacing Scheduler due over adaptive weakness pick."""
    return explain_protected_spaced_review(
        package_id=due_package_id,
        lifecycle="due",
    )


def explain_protected_spaced_review(
    *,
    package_id: str,
    lifecycle: str,
) -> str:
    """Explain preserving a protected spaced review over adaptive selection."""
    pid = (package_id or "").strip() or "a package"
    life = (lifecycle or "due").strip().lower()
    if life == "overdue":
        return (
            "Kept calendar spaced review because the Spacing Scheduler marks "
            f"{pid} overdue; overdue review is protected and is not treated "
            "as weak, so spaced_review remains the selection reason."
        )
    return (
        "Kept calendar spaced review because the Spacing Scheduler marks "
        f"{pid} due; due review is protected and is not treated as weak, "
        "so spaced_review remains the selection reason."
    )


def explain_adaptive_block_weakness(
    *,
    package_id: str,
    weakness_score: float,
    eligible_count: int,
    min_evidence: int = POLICY_V1_MIN_EVIDENCE,
) -> str:
    """Explain a genuine ADAPTIVE revision-block selection."""
    pid = (package_id or "").strip() or "the selected revision package"
    n = max(0, int(eligible_count))
    return (
        f"Selected {pid} for adaptive review because reliable Twin evidence "
        f"({n} covered topic{'' if n == 1 else 's'} with at least "
        f"{min_evidence} observations each; mean estimated knowledge "
        f"{weakness_score:.3f}) indicates it is the weakest eligible "
        "revision cluster."
    )


def explain_blocked_carrier(*, package_id: str | None = None) -> str:
    """Explain when an adaptive candidate existed but V0 could not materialise."""
    if package_id:
        return (
            "Fell back because Policy V1 identified "
            f"{package_id} as the adaptive review target, but no valid "
            "sitting could be materialised from the sequential carrier."
        )
    return (
        "Fell back because Policy V1 could not materialise a valid sitting "
        "for the adaptive review candidate."
    )
