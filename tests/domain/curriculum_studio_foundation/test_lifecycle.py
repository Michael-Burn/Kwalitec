"""Unit tests for Curriculum Studio foundation lifecycle domain."""

from __future__ import annotations

import pytest

from app.domain.curriculum_studio_foundation.lifecycle import (
    CANONICAL_FOUNDATION_STAGES,
    FoundationPublicationState,
    FoundationStage,
    has_reached,
    is_student_consumable,
    next_stage,
    stage_label,
)


def test_canonical_lifecycle_order():
    assert CANONICAL_FOUNDATION_STAGES[0] is FoundationStage.CREATE_SUBJECT
    assert CANONICAL_FOUNDATION_STAGES[-1] is FoundationStage.PUBLISH
    assert len(CANONICAL_FOUNDATION_STAGES) == 8


def test_has_reached_and_next_stage():
    assert has_reached(FoundationStage.VALIDATE, FoundationStage.EXTRACT)
    assert not has_reached(FoundationStage.EXTRACT, FoundationStage.VALIDATE)
    assert next_stage(FoundationStage.VALIDATE) is FoundationStage.FOUNDER_REVIEW
    assert next_stage(FoundationStage.PUBLISH) is None


def test_stage_labels():
    assert "Subject" in stage_label(FoundationStage.CREATE_SUBJECT)
    assert "Publish" in stage_label(FoundationStage.PUBLISH)


@pytest.mark.parametrize(
    ("state", "expected"),
    [
        (FoundationPublicationState.DRAFT, False),
        (FoundationPublicationState.PROCESSING, False),
        (FoundationPublicationState.READY_FOR_REVIEW, False),
        (FoundationPublicationState.APPROVED, False),
        (FoundationPublicationState.PUBLISHED, True),
        (FoundationPublicationState.ARCHIVED, False),
        ("published", True),
        ("draft", False),
    ],
)
def test_students_only_consume_published(state, expected):
    assert is_student_consumable(state) is expected
