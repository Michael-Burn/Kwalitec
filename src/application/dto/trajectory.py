"""Learning trajectory application DTOs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TrajectoryPointDTO:
    """One point on a learning trajectory projection."""

    sequence: int
    kind: str
    label: str


@dataclass(frozen=True, slots=True)
class LearningTrajectoryDTO:
    """Projection of Digital Twin learning trajectory memory."""

    twin_id: str
    student_id: str
    points: tuple[TrajectoryPointDTO, ...]

    @property
    def length(self) -> int:
        return len(self.points)
