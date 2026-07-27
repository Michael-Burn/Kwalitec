"""Founder review and verification contracts (CIP-002).

Review decisions are durable and append-only. Approving/rejecting/remapping
never overwrites provenance or original confidence records.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ReviewStatus(StrEnum):
    """Lifecycle status for Founder review of a mapping."""

    PENDING = "pending"
    NEEDS_REVIEW = "needs_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    REMAPPED = "remapped"


class VerificationStatus(StrEnum):
    """Whether a Founder has verified the educational fact."""

    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    DISPUTED = "disputed"


class ReviewDecision(StrEnum):
    """Founder action recorded on a review."""

    APPROVE = "approve"
    REJECT = "reject"
    REMAP = "remap"
    FLAG = "flag"


@dataclass(frozen=True)
class ReviewRecord:
    """Durable Founder review decision for one subject."""

    review_id: str
    subject_kind: str
    subject_id: str
    document_id: int
    workspace_id: str
    decision: ReviewDecision
    review_status: ReviewStatus
    verification_status: VerificationStatus
    actor_id: str
    reason: str
    suggested_learning_objective: str
    remap_target_id: str
    confidence_at_review: float
    pipeline_job_id: str
    provenance_id: str | None
    created_at_iso: str
