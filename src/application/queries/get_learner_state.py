"""GetLearnerState query."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetLearnerState:
    """Load learner state projection from the Digital Twin."""

    twin_id: str | None = None
    student_id: str | None = None
