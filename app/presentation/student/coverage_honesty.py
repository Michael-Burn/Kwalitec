"""Student-facing Study Progress coverage presentation (read-only).

Verified completion and prior-knowledge claims are different facts. Primary
coverage numbers use Kwalitec-verified completion only. Claims appear as a
separate quiet line when present, never folded into the verified ratio.
"""

from __future__ import annotations

from typing import Any, NamedTuple


class VerifiedCoveragePresentation(NamedTuple):
    verified_count: int
    topic_count: int
    verified_ratio: float
    verified_percent: int
    coverage_label: str
    claimed_count: int
    claim_label: str


def prior_knowledge_claim_label(claimed_count: int) -> str:
    """Plain label for self-declared prior knowledge, or empty when none."""
    n = max(0, int(claimed_count or 0))
    if n <= 0:
        return ""
    if n == 1:
        return "1 already knew coming in"
    return f"{n} already knew coming in"


def verified_coverage_from_progress(snap: Any) -> VerifiedCoveragePresentation:
    """Project Study Progress into honest student coverage numbers."""
    topic_ids = tuple(getattr(snap, "topic_ids", ()) or ())
    total = len(topic_ids)
    verified = tuple(getattr(snap, "verified_completed_topic_ids", ()) or ())
    claimed = tuple(getattr(snap, "prior_knowledge_claimed_topic_ids", ()) or ())

    # Legacy / incomplete fixtures may only populate progressed completed_ids.
    if not verified and not claimed:
        verified = tuple(getattr(snap, "completed_topic_ids", ()) or ())
        claimed = ()
        ratio = float(getattr(snap, "coverage_ratio", 0.0) or 0.0)
    else:
        ratio = float(getattr(snap, "verified_coverage_ratio", 0.0) or 0.0)
        if total and verified and ratio <= 0.0:
            ratio = len(verified) / total

    ratio = max(0.0, min(1.0, ratio))
    percent = int(round(ratio * 100)) if total else 0
    covered = len(verified)
    coverage_label = (
        f"{covered} of {total} topics completed" if total else ""
    )
    claimed_count = len(claimed)
    return VerifiedCoveragePresentation(
        verified_count=covered,
        topic_count=total,
        verified_ratio=ratio,
        verified_percent=percent,
        coverage_label=coverage_label,
        claimed_count=claimed_count,
        claim_label=prior_knowledge_claim_label(claimed_count),
    )
