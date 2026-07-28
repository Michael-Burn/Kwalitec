"""Binding invariants for Student Curriculum Binding (EI-004).

Principle 1 — Every student is bound to exactly one Published edition per subject.
Principle 2 — Student Curriculum Binding is the SoT for individual educational state.
Principle 3 — Curriculum knowledge is immutable; learner state is mutable.
"""

from __future__ import annotations

from enum import StrEnum

from app.domain.curriculum_extraction.publication_state import PublicationState


class BindingInvariant(StrEnum):
    """Named binding invariants enforced at the domain boundary."""

    PUBLISHED_EDITION_ONLY = "published_edition_only"
    ONE_ACTIVE_PER_SUBJECT = "one_active_per_subject"
    SUBJECT_MATCHES_EDITION = "subject_matches_edition"
    STUDENT_REQUIRED = "student_required"
    EDITION_REQUIRED = "edition_required"


class BindingInvariantError(ValueError):
    """Raised when a student curriculum binding invariant is violated."""

    def __init__(self, invariant: BindingInvariant, message: str) -> None:
        self.invariant = invariant
        super().__init__(f"[{invariant.value}] {message}")


def assert_published_edition(publication_state: str) -> None:
    """Students may bind only to Published Curriculum Editions."""
    if publication_state != PublicationState.PUBLISHED.value:
        raise BindingInvariantError(
            BindingInvariant.PUBLISHED_EDITION_ONLY,
            f"Cannot bind to edition with publication_state={publication_state!r}; "
            "only published editions are allowed",
        )


def assert_can_bind(
    *,
    student_id: int | None,
    edition_id: str | None,
    publication_state: str,
    edition_subject_code: str,
    requested_subject_code: str,
    existing_active_instance_id: str | None,
    existing_active_edition_id: str | None,
) -> None:
    """Validate creation of a Student Curriculum Instance."""
    if student_id is None or student_id < 1:
        raise BindingInvariantError(
            BindingInvariant.STUDENT_REQUIRED,
            "A positive student_id is required to create a curriculum binding",
        )
    if not (edition_id or "").strip():
        raise BindingInvariantError(
            BindingInvariant.EDITION_REQUIRED,
            "A published curriculum edition_id is required",
        )
    assert_published_edition(publication_state)

    subject = (requested_subject_code or "").strip().upper()
    edition_subject = (edition_subject_code or "").strip().upper()
    if not subject or subject != edition_subject:
        raise BindingInvariantError(
            BindingInvariant.SUBJECT_MATCHES_EDITION,
            f"Subject {subject!r} does not match edition subject {edition_subject!r}",
        )

    if existing_active_instance_id and existing_active_edition_id:
        if existing_active_edition_id == edition_id:
            return
        raise BindingInvariantError(
            BindingInvariant.ONE_ACTIVE_PER_SUBJECT,
            f"Student already has active binding {existing_active_instance_id} "
            f"to edition {existing_active_edition_id}; cannot bind to {edition_id}",
        )
