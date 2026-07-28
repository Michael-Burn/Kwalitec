"""Domain tests for Student Curriculum Binding (EI-004)."""

from __future__ import annotations

import pytest

from app.domain.student_curriculum_binding.aggregation import (
    aggregate_progress,
    is_descendant_or_self,
)
from app.domain.student_curriculum_binding.invariants import (
    BindingInvariant,
    BindingInvariantError,
    assert_can_bind,
    assert_published_edition,
)
from app.domain.student_curriculum_binding.node_state import (
    CompletionStatus,
    NodeStateSnapshot,
    RevisionStatus,
    derive_completion_status,
    initial_node_state,
    worst_revision_status,
)


def test_published_edition_only() -> None:
    assert_published_edition("published")
    with pytest.raises(BindingInvariantError) as exc:
        assert_published_edition("draft")
    assert exc.value.invariant is BindingInvariant.PUBLISHED_EDITION_ONLY


def test_assert_can_bind_rejects_draft_and_subject_mismatch() -> None:
    with pytest.raises(BindingInvariantError) as exc:
        assert_can_bind(
            student_id=1,
            edition_id="ed-1",
            publication_state="draft",
            edition_subject_code="CS1",
            requested_subject_code="CS1",
            existing_active_instance_id=None,
            existing_active_edition_id=None,
        )
    assert exc.value.invariant is BindingInvariant.PUBLISHED_EDITION_ONLY

    with pytest.raises(BindingInvariantError) as exc2:
        assert_can_bind(
            student_id=1,
            edition_id="ed-1",
            publication_state="published",
            edition_subject_code="CS1",
            requested_subject_code="CM1",
            existing_active_instance_id=None,
            existing_active_edition_id=None,
        )
    assert exc2.value.invariant is BindingInvariant.SUBJECT_MATCHES_EDITION


def test_one_active_binding_per_subject() -> None:
    with pytest.raises(BindingInvariantError) as exc:
        assert_can_bind(
            student_id=1,
            edition_id="ed-2",
            publication_state="published",
            edition_subject_code="CS1",
            requested_subject_code="CS1",
            existing_active_instance_id="sci-old",
            existing_active_edition_id="ed-1",
        )
    assert exc.value.invariant is BindingInvariant.ONE_ACTIVE_PER_SUBJECT

    # Same edition is allowed (idempotent re-bind path).
    assert_can_bind(
        student_id=1,
        edition_id="ed-1",
        publication_state="published",
        edition_subject_code="CS1",
        requested_subject_code="CS1",
        existing_active_instance_id="sci-old",
        existing_active_edition_id="ed-1",
    )


def test_initial_node_state_defaults() -> None:
    snap = initial_node_state("CS1.T01", "topic")
    assert snap.mastery == 0.0
    assert snap.confidence == 0.0
    assert snap.attempts == 0
    assert snap.evidence_count == 0
    assert snap.completion_status == CompletionStatus.NOT_STARTED.value
    assert snap.revision_status == RevisionStatus.NOT_DUE.value
    assert snap.last_interaction_at is None


def test_aggregate_progress_deterministic() -> None:
    states = [
        NodeStateSnapshot(
            node_stable_id="CS1.T01.S01.01.SS01.LO01",
            node_kind="learning_objective",
            mastery=0.5,
            confidence=0.4,
            revision_status=RevisionStatus.DUE.value,
            attempts=2,
            total_study_time_minutes=30,
            completion_status=CompletionStatus.COMPLETED.value,
            evidence_count=1,
        ),
        NodeStateSnapshot(
            node_stable_id="CS1.T01.S01.01.SS01.LO02",
            node_kind="learning_objective",
            mastery=0.3,
            confidence=0.2,
            revision_status=RevisionStatus.NOT_DUE.value,
            attempts=1,
            total_study_time_minutes=10,
            completion_status=CompletionStatus.IN_PROGRESS.value,
            evidence_count=0,
        ),
        NodeStateSnapshot(
            node_stable_id="CS1.T01.S01.01.SS01",
            node_kind="subsection",
            mastery=0.0,
            confidence=0.0,
            attempts=0,
            total_study_time_minutes=0,
            completion_status=CompletionStatus.NOT_STARTED.value,
            evidence_count=0,
        ),
        NodeStateSnapshot(
            node_stable_id="CS1.T02.S01.01.SS01.LO01",
            node_kind="learning_objective",
            mastery=1.0,
            confidence=1.0,
            attempts=5,
            total_study_time_minutes=100,
            completion_status=CompletionStatus.COMPLETED.value,
            evidence_count=3,
        ),
    ]

    first = aggregate_progress("CS1.T01.S01.01.SS01", "subsection", states)
    second = aggregate_progress("CS1.T01.S01.01.SS01", "subsection", reversed(states))
    assert first == second
    assert first.node_count == 3  # subsection + 2 LOs under T01
    assert first.completed_count == 1
    assert first.in_progress_count == 1
    assert first.mean_mastery == round((0.5 + 0.3 + 0.0) / 3, 6)
    assert first.total_attempts == 3
    assert first.total_study_time_minutes == 40
    assert first.revision_status == RevisionStatus.DUE.value
    assert first.completion_status == CompletionStatus.IN_PROGRESS.value

    topic = aggregate_progress("CS1.T01", "topic", states)
    assert topic.node_count == 3
    assert "CS1.T02" not in topic.stable_id or topic.completed_count == 1


def test_descendant_helper_and_completion_derive() -> None:
    assert is_descendant_or_self("CS1.T01.S01.01", "CS1.T01")
    assert is_descendant_or_self("CS1.T01", "CS1.T01")
    assert not is_descendant_or_self("CS1.T02", "CS1.T01")
    assert (
        derive_completion_status(
            completed_count=2, in_progress_count=0, total_count=2
        )
        == CompletionStatus.COMPLETED.value
    )
    assert worst_revision_status(
        [RevisionStatus.NOT_DUE.value, RevisionStatus.OVERDUE.value]
    ) == RevisionStatus.OVERDUE.value
