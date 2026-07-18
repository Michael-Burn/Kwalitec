"""Immutable ordered activity sequence for a Learning Session."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.learning_activity.entities.learning_activity import LearningActivity


@dataclass(frozen=True)
class ActivitySequence:
    """Ordered Learning Activities produced by the Sequence Builder.

    Attributes:
        session_id: Parent Learning Session identity.
        sequence_id: Stable identity for this sequence instance.
        activities: Ordered LearningActivity entities (0-based indices).
        plan_rationale_tags: Planning rationale carried from the plan.
    """

    session_id: str
    sequence_id: str
    activities: tuple[LearningActivity, ...]
    plan_rationale_tags: tuple[str, ...] = ()

    @property
    def length(self) -> int:
        """Number of activities in the sequence."""
        return len(self.activities)

    def activity_by_id(self, activity_id: str) -> LearningActivity | None:
        """Return the activity with the given id, or None."""
        for activity in self.activities:
            if activity.activity_id == activity_id:
                return activity
        return None

    def activity_at(self, index: int) -> LearningActivity | None:
        """Return the activity at index, or None if out of range."""
        if index < 0 or index >= len(self.activities):
            return None
        return self.activities[index]

    def with_activity(self, updated: LearningActivity) -> ActivitySequence:
        """Return a new sequence replacing the matching activity by id.

        Raises:
            ValueError: When the activity id is not in the sequence.
        """
        found = False
        rebuilt: list[LearningActivity] = []
        for activity in self.activities:
            if activity.activity_id == updated.activity_id:
                rebuilt.append(updated)
                found = True
            else:
                rebuilt.append(activity)
        if not found:
            raise ValueError(
                f"activity {updated.activity_id!r} is not in sequence "
                f"{self.sequence_id!r}"
            )
        return ActivitySequence(
            session_id=self.session_id,
            sequence_id=self.sequence_id,
            activities=tuple(rebuilt),
            plan_rationale_tags=self.plan_rationale_tags,
        )
