"""Goals domain state for the Student Digital Twin.

Represents what the learner is trying to achieve. Structural state only —
no planning or capacity algorithms.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


def _validate_probability(name: str, value: float | None) -> None:
    if value is not None and not (0.0 <= value <= 1.0):
        raise ValueError(f"{name} must be between 0.0 and 1.0 inclusive, got {value}")


@dataclass(frozen=True)
class GoalState:
    """Learner goals and capacity commitments.

    Attributes:
        target_pass_probability: Ambition for pass likelihood (0–1) when set.
        target_completion_date: Date by which the learner aims to be ready.
        planned_study_hours_per_week: Committed weekly study hours when set.
    """

    target_pass_probability: float | None = None
    target_completion_date: date | None = None
    planned_study_hours_per_week: float | None = None

    @classmethod
    def create(
        cls,
        *,
        target_pass_probability: float | None = None,
        target_completion_date: date | None = None,
        planned_study_hours_per_week: float | None = None,
    ) -> GoalState:
        """Construct a GoalState.

        Args:
            target_pass_probability: Optional pass ambition in ``[0.0, 1.0]``.
            target_completion_date: Optional readiness / completion target date.
            planned_study_hours_per_week: Optional non-negative weekly hours.

        Returns:
            A frozen GoalState instance.

        Raises:
            ValueError: If probability or hours are out of range.
        """
        _validate_probability("target_pass_probability", target_pass_probability)
        if (
            planned_study_hours_per_week is not None
            and planned_study_hours_per_week < 0.0
        ):
            raise ValueError(
                "planned_study_hours_per_week must be non-negative, "
                f"got {planned_study_hours_per_week}"
            )
        return cls(
            target_pass_probability=target_pass_probability,
            target_completion_date=target_completion_date,
            planned_study_hours_per_week=planned_study_hours_per_week,
        )
