"""GetLearningTrajectory query."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetLearningTrajectory:
    """Load learning trajectory projection from the Digital Twin."""

    twin_id: str | None = None
    student_id: str | None = None
