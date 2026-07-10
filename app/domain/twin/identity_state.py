"""Identity domain state for the Student Digital Twin.

Anchors the Twin to a learner and their exam/curriculum context.
Structural state only — no authentication or preference algorithms.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class IdentityState:
    """Who the learner is relative to a syllabus and sitting.

    Attributes:
        student_id: Stable learner identity used to scope Twin operations.
        curriculum_id: Canonical curriculum identity when a syllabus is attached.
        current_exam: Active exam / paper label when known.
        target_sitting: Target sitting date when known.
    """

    student_id: str
    curriculum_id: str | None = None
    current_exam: str | None = None
    target_sitting: date | None = None

    @classmethod
    def create(
        cls,
        student_id: str,
        *,
        curriculum_id: str | None = None,
        current_exam: str | None = None,
        target_sitting: date | None = None,
    ) -> IdentityState:
        """Construct an IdentityState.

        Args:
            student_id: Non-empty learner identity.
            curriculum_id: Optional canonical curriculum reference.
            current_exam: Optional exam / paper identifier.
            target_sitting: Optional target sitting date.

        Returns:
            A frozen IdentityState instance.

        Raises:
            ValueError: If ``student_id`` is empty or blank.
        """
        normalized = student_id.strip() if isinstance(student_id, str) else ""
        if not normalized:
            raise ValueError("student_id must be a non-empty string")
        return cls(
            student_id=normalized,
            curriculum_id=curriculum_id,
            current_exam=current_exam,
            target_sitting=target_sitting,
        )
