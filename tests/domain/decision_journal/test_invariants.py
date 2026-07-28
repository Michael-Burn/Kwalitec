"""Unit tests for Decision Journal domain invariants (ILE-002)."""

from __future__ import annotations

import pytest

from app.domain.decision_journal import (
    JournalLifecycleStatus,
    assert_student_safe_text,
    can_transition,
)


class TestLifecycleTransitions:
    def test_recommended_to_accepted(self):
        assert can_transition(
            JournalLifecycleStatus.RECOMMENDED,
            JournalLifecycleStatus.ACCEPTED,
        )

    def test_recommended_to_deferred(self):
        assert can_transition(
            JournalLifecycleStatus.RECOMMENDED,
            JournalLifecycleStatus.DEFERRED,
        )

    def test_cannot_skip_to_archived_from_recommended_via_outcome(self):
        assert not can_transition(
            JournalLifecycleStatus.RECOMMENDED,
            JournalLifecycleStatus.OUTCOME_RECORDED,
        )

    def test_archived_is_terminal(self):
        assert not can_transition(
            JournalLifecycleStatus.ARCHIVED,
            JournalLifecycleStatus.ACCEPTED,
        )

    def test_same_status_allowed(self):
        assert can_transition(
            JournalLifecycleStatus.REFLECTED,
            JournalLifecycleStatus.REFLECTED,
        )


class TestStudentSafeText:
    def test_plain_language_ok(self):
        assert_student_safe_text(
            "Recent practice on Discounting looks fragile."
        )

    def test_rejects_twin_leak(self):
        with pytest.raises(ValueError, match="digital twin"):
            assert_student_safe_text("Updated the digital twin state.")

    def test_rejects_mastery_score(self):
        with pytest.raises(ValueError, match="mastery score"):
            assert_student_safe_text("Your mastery score rose.")
