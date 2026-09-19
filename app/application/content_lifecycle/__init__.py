"""Founder Console content lifecycle foundation.

Draft persistence and Structural/Mechanical/Deterministic validation only.
No UI, AI integration, or student publish path.
"""

from __future__ import annotations

from app.application.content_lifecycle.draft_service import (
    ApprovedContentImmutableError,
    ContentDraftService,
    ContentLifecycleError,
    IllegalLifecycleTransitionError,
)
from app.application.content_lifecycle.statuses import (
    ALL_STATUSES,
    EDITABLE_STATUSES,
    STATUS_APPROVED,
    STATUS_DRAFT,
    STATUS_READY_FOR_REVIEW,
    STATUS_REJECTED,
)
from app.application.content_lifecycle.structural_mechanical_validator import (
    StructuralMechanicalFinding,
    validate_mcq_check_structure,
    validate_structural_and_mechanical,
)

__all__ = [
    "ALL_STATUSES",
    "ApprovedContentImmutableError",
    "ContentDraftService",
    "ContentLifecycleError",
    "EDITABLE_STATUSES",
    "IllegalLifecycleTransitionError",
    "STATUS_APPROVED",
    "STATUS_DRAFT",
    "STATUS_READY_FOR_REVIEW",
    "STATUS_REJECTED",
    "StructuralMechanicalFinding",
    "validate_mcq_check_structure",
    "validate_structural_and_mechanical",
]
