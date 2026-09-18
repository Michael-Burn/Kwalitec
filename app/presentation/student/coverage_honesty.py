"""Student-facing Study Progress coverage presentation (read-only).

Primary coverage numbers for active CS1 use the dual-source reconciliation
layer (CONFIRMED_COVERED + HISTORICALLY_COMPLETED). Other subjects keep the
verified-only Study Progress path until identity reconciliation exists for
them. Prior-knowledge claims appear as a separate quiet line when present,
never folded into coverage.
"""

from __future__ import annotations

from typing import Any, NamedTuple

from app.application.coverage_reconciliation import (
    CoverageDisplay,
    CoverageReconciliationService,
)
from app.application.curriculum_identity.constants import (
    ACTIVE_CS1_CURRICULUM_VERSION,
)


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


def uses_reconciled_coverage(
    *,
    subject_code: str = "",
    curriculum_identity: str = "",
) -> bool:
    """True when dual-source reconciliation is the live coverage authority.

    Reconciliation today is seeded for active CS1 only. Non-CS1 subjects keep
    their prior verified / Stage A engines until a matching identity map exists.
    """
    code = (subject_code or "").strip().upper()
    identity = (curriculum_identity or "").strip()
    if code == "CS1":
        return True
    if identity == ACTIVE_CS1_CURRICULUM_VERSION or identity.startswith("CS1:"):
        return True
    return False


def reconciled_coverage_for_learner(user_id: int) -> CoverageDisplay:
    """Live student coverage numbers from dual-source reconciliation."""
    return CoverageReconciliationService.coverage_for_learner(user_id)


def verified_coverage_from_progress(snap: Any) -> VerifiedCoveragePresentation:
    """Project Study Progress into verified-only coverage numbers.

    Used for non-CS1 subjects and for prior-knowledge claim counts. Live CS1
    syllabus coverage displays use ``reconciled_coverage_for_learner`` instead.
    """
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
