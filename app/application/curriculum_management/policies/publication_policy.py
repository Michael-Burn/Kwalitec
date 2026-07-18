"""Stateless publication lifecycle policy."""

from __future__ import annotations

from app.application.curriculum_management.exceptions import PolicyViolation
from app.domain.curriculum_management.publication_state import (
    PublicationState,
    PublicationTransitionEvent,
    has_reached,
    next_publication_state,
)
from app.domain.curriculum_management.subject_version import SubjectVersion


class PublicationPolicy:
    """Deterministic publication transition rules (stateless)."""

    FORWARD_EVENTS: tuple[PublicationTransitionEvent, ...] = (
        PublicationTransitionEvent.MARK_UPLOADED,
        PublicationTransitionEvent.MARK_VALIDATED,
        PublicationTransitionEvent.MARK_BLUEPRINT_ASSIGNED,
        PublicationTransitionEvent.MARK_PREVIEW_READY,
        PublicationTransitionEvent.MARK_APPROVED,
        PublicationTransitionEvent.MARK_PUBLISHED,
        PublicationTransitionEvent.MARK_ARCHIVED,
    )

    @staticmethod
    def assert_transition_allowed(
        current: PublicationState,
        event: PublicationTransitionEvent,
    ) -> PublicationState:
        """Return next state or raise PolicyViolation."""
        nxt = next_publication_state(current, event)
        if nxt is None:
            raise PolicyViolation(
                f"Illegal publication transition: {current.value} "
                f"+ {event.value}"
            )
        return nxt

    @staticmethod
    def assert_not_archived(version: SubjectVersion) -> None:
        """Raise when the version is archived."""
        if version.state is PublicationState.ARCHIVED:
            raise PolicyViolation("Archived versions cannot be mutated")

    @staticmethod
    def assert_can_publish(version: SubjectVersion) -> None:
        """Raise when a version is not ready to publish."""
        if version.state is not PublicationState.APPROVED:
            raise PolicyViolation(
                f"Publish requires APPROVED state; got {version.state.value}"
            )
        latest = version.latest_validation
        if latest is None or not latest.passed:
            raise PolicyViolation("Publish requires a passing validation report")
        approval = version.latest_approval
        if approval is None or not approval.is_approved:
            raise PolicyViolation("Publish requires an APPROVED approval record")

    @staticmethod
    def assert_at_least(
        version: SubjectVersion,
        milestone: PublicationState,
    ) -> None:
        """Raise when version has not reached ``milestone``."""
        if not has_reached(version.state, milestone):
            raise PolicyViolation(
                f"Requires state at least {milestone.value}; "
                f"got {version.state.value}"
            )

    @staticmethod
    def next_forward_event(
        state: PublicationState,
    ) -> PublicationTransitionEvent | None:
        """Return the next forward pipeline event, or None at end/archive."""
        mapping = {
            PublicationState.DRAFT: PublicationTransitionEvent.MARK_UPLOADED,
            PublicationState.UPLOADED: PublicationTransitionEvent.MARK_VALIDATED,
            PublicationState.VALIDATED: (
                PublicationTransitionEvent.MARK_BLUEPRINT_ASSIGNED
            ),
            PublicationState.BLUEPRINT_ASSIGNED: (
                PublicationTransitionEvent.MARK_PREVIEW_READY
            ),
            PublicationState.PREVIEW_READY: (
                PublicationTransitionEvent.MARK_APPROVED
            ),
            PublicationState.APPROVED: PublicationTransitionEvent.MARK_PUBLISHED,
            PublicationState.PUBLISHED: PublicationTransitionEvent.MARK_ARCHIVED,
        }
        return mapping.get(state)
