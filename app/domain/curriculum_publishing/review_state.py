"""Founder review lifecycle for CKG editions and nodes (EI-003)."""

from __future__ import annotations

from enum import StrEnum


class ReviewStatus(StrEnum):
    """Edition-level Founder review status.

    Validation alone never advances this to ``approved``.
    """

    PENDING = "pending"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"


class NodeReviewStatus(StrEnum):
    """Per-node editorial review disposition."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
