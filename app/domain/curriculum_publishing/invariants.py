"""Publication and editorial invariants for Founder curriculum governance.

Principle 1 — Only Published editions may be consumed by student-facing systems.
Principle 2 — Publishing is an explicit Founder action; validation never publishes.
Principle 3 — Every publication decision is explainable and auditable.
"""

from __future__ import annotations

from enum import StrEnum

from app.domain.curriculum_extraction.publication_state import (
    PublicationState,
    ValidationStatus,
)
from app.domain.curriculum_publishing.review_state import (
    NodeReviewStatus,
    ReviewStatus,
)


class PublicationInvariant(StrEnum):
    """Named governance invariants enforced at the domain boundary."""

    DRAFT_ONLY_EDITORIAL = "draft_only_editorial"
    VALIDATION_REQUIRED = "validation_required"
    REVIEW_APPROVAL_REQUIRED = "review_approval_required"
    NO_REJECTED_NODES = "no_rejected_nodes"
    EXPLICIT_PUBLISH = "explicit_publish"
    SINGLE_PUBLISHED_PER_SUBJECT = "single_published_per_subject"
    RATIONALE_REQUIRED = "rationale_required"
    PUBLISHER_REQUIRED = "publisher_required"


class PublicationInvariantError(ValueError):
    """Raised when a publication or editorial invariant is violated."""

    def __init__(self, invariant: PublicationInvariant, message: str) -> None:
        self.invariant = invariant
        super().__init__(f"[{invariant.value}] {message}")


def assert_draft_only_editorial(
    publication_state: str,
    *,
    operation: str,
) -> None:
    """Editorial mutations are allowed only on draft editions."""
    if publication_state != PublicationState.DRAFT.value:
        raise PublicationInvariantError(
            PublicationInvariant.DRAFT_ONLY_EDITORIAL,
            f"Cannot {operation}: edition is {publication_state}, not draft",
        )


def assert_can_approve_edition(
    *,
    publication_state: str,
    validation_status: str,
    rejected_node_count: int,
) -> None:
    """Edition approval requires a validated draft with no rejected nodes."""
    assert_draft_only_editorial(publication_state, operation="approve edition")
    if validation_status != ValidationStatus.PASSED.value:
        raise PublicationInvariantError(
            PublicationInvariant.VALIDATION_REQUIRED,
            "Cannot approve edition until validation_status is passed",
        )
    if rejected_node_count > 0:
        raise PublicationInvariantError(
            PublicationInvariant.NO_REJECTED_NODES,
            f"Cannot approve edition while {rejected_node_count} node(s) are rejected",
        )


def assert_can_publish(
    *,
    publication_state: str,
    validation_status: str,
    review_status: str,
    publisher: str,
    rationale: str,
    rejected_node_count: int = 0,
) -> None:
    """Publication gates — validation alone is never sufficient."""
    if publication_state != PublicationState.DRAFT.value:
        raise PublicationInvariantError(
            PublicationInvariant.EXPLICIT_PUBLISH,
            f"Only draft editions may be published (state={publication_state})",
        )
    if validation_status != ValidationStatus.PASSED.value:
        raise PublicationInvariantError(
            PublicationInvariant.VALIDATION_REQUIRED,
            "Cannot publish until validation_status is passed",
        )
    if review_status != ReviewStatus.APPROVED.value:
        raise PublicationInvariantError(
            PublicationInvariant.REVIEW_APPROVAL_REQUIRED,
            "Cannot publish until Founder review_status is approved",
        )
    if rejected_node_count > 0:
        raise PublicationInvariantError(
            PublicationInvariant.NO_REJECTED_NODES,
            f"Cannot publish while {rejected_node_count} node(s) are rejected",
        )
    if not (publisher or "").strip():
        raise PublicationInvariantError(
            PublicationInvariant.PUBLISHER_REQUIRED,
            "Publisher identity is required for an auditable publication",
        )
    if not (rationale or "").strip():
        raise PublicationInvariantError(
            PublicationInvariant.RATIONALE_REQUIRED,
            "Publication rationale is required for an auditable publication",
        )


def is_node_blocking_approval(status: str) -> bool:
    """Rejected nodes block edition approval and publication."""
    return status == NodeReviewStatus.REJECTED.value
