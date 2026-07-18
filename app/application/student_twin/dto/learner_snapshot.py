"""Immutable learner snapshot DTO."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.student_twin.learner import Learner


@dataclass(frozen=True)
class LearnerSnapshot:
    """Read-only learner identity projection."""

    learner_id: str
    display_name: str | None = None
    subject_codes: tuple[str, ...] = field(default_factory=tuple)
    subject_count: int = 0

    @classmethod
    def from_domain(cls, learner: Learner) -> LearnerSnapshot:
        """Project a domain Learner to a DTO."""
        return cls(
            learner_id=learner.learner_id,
            display_name=learner.display_name,
            subject_codes=learner.subject_codes,
            subject_count=learner.subject_count,
        )
