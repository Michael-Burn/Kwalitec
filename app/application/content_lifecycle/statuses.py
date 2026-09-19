"""Lifecycle status constants for educational content drafts."""

from __future__ import annotations

from app.models.content_draft import (
    CONTENT_DRAFT_STATUS_APPROVED,
    CONTENT_DRAFT_STATUS_DRAFT,
    CONTENT_DRAFT_STATUS_READY_FOR_REVIEW,
    CONTENT_DRAFT_STATUS_REJECTED,
    CONTENT_DRAFT_STATUSES,
)

# Re-export with domain-facing names used by the draft service.
STATUS_DRAFT = CONTENT_DRAFT_STATUS_DRAFT
STATUS_READY_FOR_REVIEW = CONTENT_DRAFT_STATUS_READY_FOR_REVIEW
STATUS_APPROVED = CONTENT_DRAFT_STATUS_APPROVED
STATUS_REJECTED = CONTENT_DRAFT_STATUS_REJECTED

ALL_STATUSES: frozenset[str] = frozenset(CONTENT_DRAFT_STATUSES)

# Statuses whose payload may be mutated in place.
EDITABLE_STATUSES: frozenset[str] = frozenset(
    {
        STATUS_DRAFT,
        STATUS_READY_FOR_REVIEW,
        STATUS_REJECTED,
    }
)

# Lawful forward transitions: from_status -> allowed next statuses.
LAWFUL_TRANSITIONS: dict[str, frozenset[str]] = {
    STATUS_DRAFT: frozenset({STATUS_READY_FOR_REVIEW}),
    STATUS_READY_FOR_REVIEW: frozenset(
        {STATUS_APPROVED, STATUS_REJECTED}
    ),
    STATUS_REJECTED: frozenset({STATUS_DRAFT, STATUS_READY_FOR_REVIEW}),
    STATUS_APPROVED: frozenset(),  # payload edits create a new revision
}
