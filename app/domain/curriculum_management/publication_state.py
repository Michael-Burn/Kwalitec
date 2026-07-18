"""Publication lifecycle states for curriculum subject versions.

Lifecycle only — no educational behaviour, no content parsing.
"""

from __future__ import annotations

from enum import StrEnum


class PublicationState(StrEnum):
    """Lifecycle posture of a subject version through Curriculum Studio.

    Terminal retention state: ARCHIVED.
    Forward publication pipeline ends at PUBLISHED.
    """

    DRAFT = "draft"
    UPLOADED = "uploaded"
    VALIDATED = "validated"
    BLUEPRINT_ASSIGNED = "blueprint_assigned"
    PREVIEW_READY = "preview_ready"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class PublicationTransitionEvent(StrEnum):
    """Named events for PublicationState transitions."""

    MARK_UPLOADED = "mark_uploaded"
    MARK_VALIDATED = "mark_validated"
    MARK_BLUEPRINT_ASSIGNED = "mark_blueprint_assigned"
    MARK_PREVIEW_READY = "mark_preview_ready"
    MARK_APPROVED = "mark_approved"
    MARK_PUBLISHED = "mark_published"
    MARK_ARCHIVED = "mark_archived"
    REVERT_TO_DRAFT = "revert_to_draft"
    REVERT_TO_UPLOADED = "revert_to_uploaded"
    REVERT_TO_VALIDATED = "revert_to_validated"
    REVERT_TO_BLUEPRINT_ASSIGNED = "revert_to_blueprint_assigned"
    REVERT_TO_PREVIEW_READY = "revert_to_preview_ready"


# (from_state, event) → to_state — authoritative lawful map.
LAWFUL_PUBLICATION_TRANSITIONS: dict[
    tuple[PublicationState, PublicationTransitionEvent], PublicationState
] = {
    (
        PublicationState.DRAFT,
        PublicationTransitionEvent.MARK_UPLOADED,
    ): PublicationState.UPLOADED,
    (
        PublicationState.UPLOADED,
        PublicationTransitionEvent.MARK_VALIDATED,
    ): PublicationState.VALIDATED,
    (
        PublicationState.UPLOADED,
        PublicationTransitionEvent.REVERT_TO_DRAFT,
    ): PublicationState.DRAFT,
    (
        PublicationState.VALIDATED,
        PublicationTransitionEvent.MARK_BLUEPRINT_ASSIGNED,
    ): PublicationState.BLUEPRINT_ASSIGNED,
    (
        PublicationState.VALIDATED,
        PublicationTransitionEvent.REVERT_TO_UPLOADED,
    ): PublicationState.UPLOADED,
    (
        PublicationState.BLUEPRINT_ASSIGNED,
        PublicationTransitionEvent.MARK_PREVIEW_READY,
    ): PublicationState.PREVIEW_READY,
    (
        PublicationState.BLUEPRINT_ASSIGNED,
        PublicationTransitionEvent.REVERT_TO_VALIDATED,
    ): PublicationState.VALIDATED,
    (
        PublicationState.PREVIEW_READY,
        PublicationTransitionEvent.MARK_APPROVED,
    ): PublicationState.APPROVED,
    (
        PublicationState.PREVIEW_READY,
        PublicationTransitionEvent.REVERT_TO_BLUEPRINT_ASSIGNED,
    ): PublicationState.BLUEPRINT_ASSIGNED,
    (
        PublicationState.APPROVED,
        PublicationTransitionEvent.MARK_PUBLISHED,
    ): PublicationState.PUBLISHED,
    (
        PublicationState.APPROVED,
        PublicationTransitionEvent.REVERT_TO_PREVIEW_READY,
    ): PublicationState.PREVIEW_READY,
    (
        PublicationState.PUBLISHED,
        PublicationTransitionEvent.MARK_ARCHIVED,
    ): PublicationState.ARCHIVED,
}


# Ordered forward pipeline (excludes ARCHIVED).
PUBLICATION_PIPELINE: tuple[PublicationState, ...] = (
    PublicationState.DRAFT,
    PublicationState.UPLOADED,
    PublicationState.VALIDATED,
    PublicationState.BLUEPRINT_ASSIGNED,
    PublicationState.PREVIEW_READY,
    PublicationState.APPROVED,
    PublicationState.PUBLISHED,
)


def resolve_publication_state(value: PublicationState | str) -> PublicationState:
    """Resolve a PublicationState from enum or string token."""
    if isinstance(value, PublicationState):
        return value
    token = (value or "").strip().lower().replace("-", "_").replace(" ", "_")
    try:
        return PublicationState(token)
    except ValueError as exc:
        raise ValueError(f"Unknown publication state: {value!r}") from exc


def next_publication_state(
    current: PublicationState,
    event: PublicationTransitionEvent,
) -> PublicationState | None:
    """Return the lawful next state, or None if the transition is invalid."""
    return LAWFUL_PUBLICATION_TRANSITIONS.get((current, event))


def is_terminal_publication_state(state: PublicationState) -> bool:
    """True when the version may not advance the publication pipeline."""
    return state is PublicationState.ARCHIVED


def is_editable_publication_state(state: PublicationState) -> bool:
    """True when assets / assignments may still be mutated."""
    return state in {
        PublicationState.DRAFT,
        PublicationState.UPLOADED,
        PublicationState.VALIDATED,
        PublicationState.BLUEPRINT_ASSIGNED,
        PublicationState.PREVIEW_READY,
    }


def pipeline_index(state: PublicationState) -> int:
    """Return the forward-pipeline index, or -1 for ARCHIVED."""
    try:
        return PUBLICATION_PIPELINE.index(state)
    except ValueError:
        return -1


def has_reached(state: PublicationState, milestone: PublicationState) -> bool:
    """True when ``state`` is at or beyond ``milestone`` in the forward pipeline."""
    if state is PublicationState.ARCHIVED:
        return milestone is PublicationState.ARCHIVED or milestone in {
            PublicationState.PUBLISHED,
            *PUBLICATION_PIPELINE,
        }
    current_idx = pipeline_index(state)
    milestone_idx = pipeline_index(milestone)
    if current_idx < 0 or milestone_idx < 0:
        return False
    return current_idx >= milestone_idx
