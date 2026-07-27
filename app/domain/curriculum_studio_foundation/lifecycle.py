"""Founder Curriculum Studio foundation lifecycle stages (PI-001A).

Maps the product onboarding path to observable, auditable stages.
Does not teach, plan, or recommend.
"""

from __future__ import annotations

from enum import StrEnum


class FoundationStage(StrEnum):
    """Canonical Founder Curriculum Studio foundation stages."""

    CREATE_SUBJECT = "create_subject"
    UPLOAD_CMP = "upload_cmp"
    UPLOAD_SYLLABUS = "upload_syllabus"
    EXTRACT = "extract"
    PARSE = "parse"
    VALIDATE = "validate"
    FOUNDER_REVIEW = "founder_review"
    PUBLISH = "publish"


class FoundationPublicationState(StrEnum):
    """Publication posture for a curriculum version."""

    DRAFT = "draft"
    PROCESSING = "processing"
    READY_FOR_REVIEW = "ready_for_review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    FAILED = "failed"


# Authoritative forward order for the foundation lifecycle.
CANONICAL_FOUNDATION_STAGES: tuple[FoundationStage, ...] = (
    FoundationStage.CREATE_SUBJECT,
    FoundationStage.UPLOAD_CMP,
    FoundationStage.UPLOAD_SYLLABUS,
    FoundationStage.EXTRACT,
    FoundationStage.PARSE,
    FoundationStage.VALIDATE,
    FoundationStage.FOUNDER_REVIEW,
    FoundationStage.PUBLISH,
)

STAGE_LABELS: dict[FoundationStage, str] = {
    FoundationStage.CREATE_SUBJECT: "Create Subject",
    FoundationStage.UPLOAD_CMP: "Upload CMP",
    FoundationStage.UPLOAD_SYLLABUS: "Upload Syllabus",
    FoundationStage.EXTRACT: "Extract",
    FoundationStage.PARSE: "Parse",
    FoundationStage.VALIDATE: "Validate",
    FoundationStage.FOUNDER_REVIEW: "Founder Review",
    FoundationStage.PUBLISH: "Publish Curriculum Version",
}


def resolve_foundation_stage(value: FoundationStage | str) -> FoundationStage:
    """Resolve a FoundationStage from enum or string token."""
    if isinstance(value, FoundationStage):
        return value
    token = (value or "").strip().lower().replace("-", "_").replace(" ", "_")
    try:
        return FoundationStage(token)
    except ValueError as exc:
        raise ValueError(f"Unknown foundation stage: {value!r}") from exc


def stage_index(stage: FoundationStage | str) -> int:
    """Zero-based index in the canonical foundation lifecycle."""
    return CANONICAL_FOUNDATION_STAGES.index(resolve_foundation_stage(stage))


def has_reached(
    current: FoundationStage | str,
    milestone: FoundationStage | str,
) -> bool:
    """True when ``current`` is at or beyond ``milestone``."""
    return stage_index(current) >= stage_index(milestone)


def next_stage(current: FoundationStage | str) -> FoundationStage | None:
    """Return the next forward stage, or None at PUBLISH."""
    idx = stage_index(current)
    if idx >= len(CANONICAL_FOUNDATION_STAGES) - 1:
        return None
    return CANONICAL_FOUNDATION_STAGES[idx + 1]


def stage_label(stage: FoundationStage | str) -> str:
    """Human-readable stage label."""
    return STAGE_LABELS[resolve_foundation_stage(stage)]


def is_student_consumable(state: FoundationPublicationState | str) -> bool:
    """True only for PUBLISHED — drafts must never reach students."""
    if isinstance(state, FoundationPublicationState):
        return state is FoundationPublicationState.PUBLISHED
    token = (state or "").strip().lower()
    return token == FoundationPublicationState.PUBLISHED.value
