"""Learning trajectory — append-only educational memory spine.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
    EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md
Concept
    Learning Trajectory
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.digital_twin.enums import TrajectoryPointKind
from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class TrajectoryPoint(EducationalValueObject):
    """Single immutable point on a LearningTrajectory."""

    sequence: int
    kind: TrajectoryPointKind
    label: str

    def _validate(self) -> None:
        if not isinstance(self.sequence, int) or isinstance(self.sequence, bool):
            raise EducationalInvariantViolation(
                "sequence must be an integer",
                invariant="TrajectoryPoint.sequence.type",
            )
        if self.sequence < 1:
            raise EducationalInvariantViolation(
                "sequence must be a positive integer",
                invariant="TrajectoryPoint.sequence.positive",
            )
        if not isinstance(self.kind, TrajectoryPointKind):
            raise EducationalInvariantViolation(
                "kind must be a TrajectoryPointKind",
                invariant="TrajectoryPoint.kind.type",
            )
        object.__setattr__(
            self,
            "label",
            require_non_empty_text(self.label, "label"),
        )


@dataclass(frozen=True, slots=True)
class LearningTrajectory(EducationalValueObject):
    """Immutable ordered educational trajectory.

    Trajectory points are append-only through ``with_appended``. History cannot
    be rewritten or deleted via this value object.
    """

    points: tuple[TrajectoryPoint, ...] = ()

    def _validate(self) -> None:
        if not isinstance(self.points, tuple):
            raise EducationalInvariantViolation(
                "points must be a tuple of TrajectoryPoint",
                invariant="LearningTrajectory.points.type",
            )
        previous = 0
        for point in self.points:
            if not isinstance(point, TrajectoryPoint):
                raise EducationalInvariantViolation(
                    "each trajectory point must be a TrajectoryPoint",
                    invariant="LearningTrajectory.points.item_type",
                )
            if point.sequence <= previous:
                raise EducationalInvariantViolation(
                    "trajectory sequences must be strictly increasing",
                    invariant="LearningTrajectory.points.sequence_order",
                )
            previous = point.sequence

    @classmethod
    def empty(cls) -> LearningTrajectory:
        return cls(points=())

    @classmethod
    def of(cls, *points: TrajectoryPoint) -> LearningTrajectory:
        return cls(points=tuple(points))

    def with_appended(self, point: TrajectoryPoint) -> LearningTrajectory:
        """Return a new trajectory with ``point`` appended (never mutates)."""
        if not isinstance(point, TrajectoryPoint):
            raise EducationalInvariantViolation(
                "appended point must be a TrajectoryPoint",
                invariant="LearningTrajectory.with_appended.type",
            )
        if self.points and point.sequence <= self.points[-1].sequence:
            raise EducationalInvariantViolation(
                "appended trajectory sequence must exceed prior sequence",
                invariant="LearningTrajectory.with_appended.sequence",
            )
        return LearningTrajectory(points=(*self.points, point))

    def length(self) -> int:
        return len(self.points)

    def last(self) -> TrajectoryPoint | None:
        if not self.points:
            return None
        return self.points[-1]

    def next_sequence(self) -> int:
        if not self.points:
            return 1
        return self.points[-1].sequence + 1
