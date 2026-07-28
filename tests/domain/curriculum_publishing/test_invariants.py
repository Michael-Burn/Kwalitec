"""Domain tests for Founder curriculum publishing invariants (EI-003)."""

from __future__ import annotations

import pytest

from app.domain.curriculum_publishing.invariants import (
    PublicationInvariant,
    PublicationInvariantError,
    assert_can_approve_edition,
    assert_can_publish,
    assert_draft_only_editorial,
)
from app.domain.curriculum_publishing.review_state import ReviewStatus


def test_validation_alone_never_publishes() -> None:
    with pytest.raises(PublicationInvariantError) as exc:
        assert_can_publish(
            publication_state="draft",
            validation_status="passed",
            review_status=ReviewStatus.PENDING.value,
            publisher="founder@kwalitec.test",
            rationale="Ready",
        )
    assert exc.value.invariant is PublicationInvariant.REVIEW_APPROVAL_REQUIRED


def test_publish_requires_rationale_and_publisher() -> None:
    with pytest.raises(PublicationInvariantError) as exc:
        assert_can_publish(
            publication_state="draft",
            validation_status="passed",
            review_status=ReviewStatus.APPROVED.value,
            publisher="",
            rationale="Ready",
        )
    assert exc.value.invariant is PublicationInvariant.PUBLISHER_REQUIRED

    with pytest.raises(PublicationInvariantError) as exc2:
        assert_can_publish(
            publication_state="draft",
            validation_status="passed",
            review_status=ReviewStatus.APPROVED.value,
            publisher="founder@kwalitec.test",
            rationale="  ",
        )
    assert exc2.value.invariant is PublicationInvariant.RATIONALE_REQUIRED


def test_editorial_only_on_draft() -> None:
    with pytest.raises(PublicationInvariantError) as exc:
        assert_draft_only_editorial("published", operation="edit metadata")
    assert exc.value.invariant is PublicationInvariant.DRAFT_ONLY_EDITORIAL


def test_approve_edition_requires_validation_and_no_rejects() -> None:
    with pytest.raises(PublicationInvariantError):
        assert_can_approve_edition(
            publication_state="draft",
            validation_status="failed",
            rejected_node_count=0,
        )
    with pytest.raises(PublicationInvariantError):
        assert_can_approve_edition(
            publication_state="draft",
            validation_status="passed",
            rejected_node_count=2,
        )
    assert_can_approve_edition(
        publication_state="draft",
        validation_status="passed",
        rejected_node_count=0,
    )


def test_happy_path_publish_gates() -> None:
    assert_can_publish(
        publication_state="draft",
        validation_status="passed",
        review_status=ReviewStatus.APPROVED.value,
        publisher="founder@kwalitec.test",
        rationale="Validated educational structure for CS1 2026",
    )
