"""Structural validation for Learning Activity sequences and transitions.

Ensures single active activity, no duplicate identifiers, sequence integrity,
and valid transitions.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.learning_activity.dto.activity_sequence import ActivitySequence
from app.application.learning_activity.exceptions import ValidationError
from app.application.learning_activity.policies.transition_policy import (
    TransitionPolicy,
)
from app.domain.learning_activity.value_objects.activity_state import (
    ActivityState,
    ActivityTransitionEvent,
)


@dataclass(frozen=True)
class ValidationIssue:
    """One structural validation finding."""

    code: str
    message: str


@dataclass(frozen=True)
class ValidationResult:
    """Outcome of validating an activity sequence."""

    is_valid: bool
    issues: tuple[ValidationIssue, ...]

    @property
    def codes(self) -> tuple[str, ...]:
        """Stable issue codes."""
        return tuple(issue.code for issue in self.issues)


class ActivityValidator:
    """Validate Learning Activity sequence integrity invariants."""

    def validate(
        self,
        sequence: ActivitySequence,
        *,
        allow_multiple_active: bool = False,
    ) -> ValidationResult:
        """Validate sequence integrity without mutating state."""
        issues: list[ValidationIssue] = []

        if not sequence.session_id or not sequence.session_id.strip():
            issues.append(
                ValidationIssue("empty_session_id", "session_id must be non-empty")
            )
        if not sequence.sequence_id or not sequence.sequence_id.strip():
            issues.append(
                ValidationIssue(
                    "empty_sequence_id", "sequence_id must be non-empty"
                )
            )

        ids: list[str] = []
        indices: list[int] = []
        active_count = 0
        for activity in sequence.activities:
            if activity.session_id != sequence.session_id:
                issues.append(
                    ValidationIssue(
                        "session_mismatch",
                        f"activity {activity.activity_id!r} session_id mismatch",
                    )
                )
            if activity.activity_id in ids:
                issues.append(
                    ValidationIssue(
                        "duplicate_id",
                        f"duplicate activity identity: {activity.activity_id!r}",
                    )
                )
            ids.append(activity.activity_id)
            if activity.sequence_index in indices:
                issues.append(
                    ValidationIssue(
                        "duplicate_index",
                        f"duplicate sequence_index: {activity.sequence_index}",
                    )
                )
            indices.append(activity.sequence_index)
            if activity.state == ActivityState.ACTIVE:
                active_count += 1

        if indices and sorted(indices) != list(range(len(indices))):
            # Contiguous 0..n-1 expected for sequence integrity.
            expected = list(range(len(sequence.activities)))
            if sorted(indices) != expected:
                issues.append(
                    ValidationIssue(
                        "index_gap",
                        "sequence_index values must be contiguous from 0",
                    )
                )

        ordered = [a.sequence_index for a in sequence.activities]
        if ordered != sorted(ordered):
            issues.append(
                ValidationIssue(
                    "order_mismatch",
                    "activities must be ordered by ascending sequence_index",
                )
            )

        if not allow_multiple_active and active_count > 1:
            issues.append(
                ValidationIssue(
                    "multiple_active",
                    f"expected at most one ACTIVE activity; found {active_count}",
                )
            )

        return ValidationResult(is_valid=not issues, issues=tuple(issues))

    def assert_valid(
        self,
        sequence: ActivitySequence,
        *,
        allow_multiple_active: bool = False,
    ) -> None:
        """Raise ValidationError when the sequence is invalid."""
        result = self.validate(
            sequence, allow_multiple_active=allow_multiple_active
        )
        if not result.is_valid:
            codes = ", ".join(result.codes)
            raise ValidationError(f"Activity sequence validation failed: {codes}")

    def assert_transition_lawful(
        self,
        state: ActivityState,
        event: ActivityTransitionEvent,
    ) -> None:
        """Raise ValidationError when a transition is unlawful."""
        if not TransitionPolicy.is_lawful(state, event):
            raise ValidationError(
                f"Invalid transition: {state.value} + {event.value}"
            )
