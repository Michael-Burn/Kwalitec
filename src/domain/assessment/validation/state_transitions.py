"""Assessment session lifecycle transition rules.

Architecture Source
    knowledge/product/AP-002/ASSESSMENT_LIFECYCLE.md §3
"""

from __future__ import annotations

from domain.assessment.enums import AssessmentStatus
from domain.assessment.exceptions import InvalidAssessmentStateTransition

# Lawful directed transitions for AssessmentSession status.
ALLOWED_TRANSITIONS: dict[AssessmentStatus, frozenset[AssessmentStatus]] = {
    AssessmentStatus.DRAFT: frozenset(
        {AssessmentStatus.READY, AssessmentStatus.INVALIDATED}
    ),
    AssessmentStatus.READY: frozenset(
        {
            AssessmentStatus.IN_PROGRESS,
            AssessmentStatus.ABANDONED,
            AssessmentStatus.INVALIDATED,
        }
    ),
    AssessmentStatus.IN_PROGRESS: frozenset(
        {
            AssessmentStatus.PAUSED,
            AssessmentStatus.SUBMITTED,
            AssessmentStatus.ABANDONED,
            AssessmentStatus.INVALIDATED,
        }
    ),
    AssessmentStatus.PAUSED: frozenset(
        {
            AssessmentStatus.IN_PROGRESS,
            AssessmentStatus.ABANDONED,
            AssessmentStatus.INVALIDATED,
        }
    ),
    AssessmentStatus.SUBMITTED: frozenset(
        {AssessmentStatus.OBSERVED, AssessmentStatus.INVALIDATED}
    ),
    AssessmentStatus.OBSERVED: frozenset(
        {AssessmentStatus.REASONED, AssessmentStatus.INVALIDATED}
    ),
    AssessmentStatus.REASONED: frozenset(
        {AssessmentStatus.CLOSED, AssessmentStatus.INVALIDATED}
    ),
    AssessmentStatus.CLOSED: frozenset(),
    AssessmentStatus.ABANDONED: frozenset(),
    AssessmentStatus.INVALIDATED: frozenset(),
}


def can_transition(current: AssessmentStatus, target: AssessmentStatus) -> bool:
    """Return True when ``current → target`` is a lawful lifecycle step."""
    if not isinstance(current, AssessmentStatus) or not isinstance(
        target, AssessmentStatus
    ):
        return False
    return target in ALLOWED_TRANSITIONS.get(current, frozenset())


def assert_can_transition(current: AssessmentStatus, target: AssessmentStatus) -> None:
    """Raise when the requested lifecycle transition is unlawful."""
    if can_transition(current, target):
        return
    raise InvalidAssessmentStateTransition(
        f"cannot transition assessment session from {current.value} to {target.value}",
        from_status=current.value,
        to_status=target.value,
    )
