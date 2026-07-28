"""Editorial operations recognised by the Founder publishing workflow."""

from __future__ import annotations

from enum import StrEnum


class EditorialAction(StrEnum):
    """Auditable Founder editorial operations on a draft edition."""

    APPROVE_NODE = "approve_node"
    REJECT_NODE = "reject_node"
    EDIT_METADATA = "edit_metadata"
    RESOLVE_VALIDATION_ISSUE = "resolve_validation_issue"
    REVALIDATE = "revalidate"
    APPROVE_EDITION = "approve_edition"
    REJECT_EDITION = "reject_edition"
    START_REVIEW = "start_review"
