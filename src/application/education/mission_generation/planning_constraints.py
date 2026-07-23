"""Planning constraints — optional application inputs to mission generation.

These are caller-supplied preferences and limits. They are not domain
state, not StudentEducationalState fields, and not mastery estimates.
"""

from __future__ import annotations

from dataclasses import dataclass

from application.education.mission_generation.enums import LearningPace, MissionType
from application.education.mission_generation.errors import MissionInvariantViolation

# Default chunk size when splitting large missions (minutes).
DEFAULT_MAX_MISSION_MINUTES = 30


@dataclass(frozen=True, slots=True)
class PlanningConstraints:
    """Optional planning inputs supplied by the application caller.

    All fields are optional. Absent values mean "no additional constraint".
    """

    available_study_minutes: int | None = None
    target_examination: str | None = None
    preferred_mission_types: tuple[MissionType, ...] = ()
    learning_pace: LearningPace = LearningPace.NORMAL
    maximum_daily_workload_minutes: int | None = None
    maximum_mission_minutes: int = DEFAULT_MAX_MISSION_MINUTES

    def __post_init__(self) -> None:
        if self.available_study_minutes is not None:
            if isinstance(self.available_study_minutes, bool) or not isinstance(
                self.available_study_minutes, int
            ):
                raise MissionInvariantViolation(
                    "available_study_minutes must be an integer when provided",
                    invariant="PlanningConstraints.available_study_minutes.type",
                )
            if self.available_study_minutes < 1:
                raise MissionInvariantViolation(
                    "available_study_minutes must be >= 1 when provided",
                    invariant="PlanningConstraints.available_study_minutes.positive",
                )

        exam = (self.target_examination or "").strip() or None
        object.__setattr__(self, "target_examination", exam)

        preferred = tuple(self.preferred_mission_types)
        for mission_type in preferred:
            if not isinstance(mission_type, MissionType):
                raise MissionInvariantViolation(
                    "preferred_mission_types must contain MissionType values",
                    invariant="PlanningConstraints.preferred_mission_types.type",
                )
        object.__setattr__(self, "preferred_mission_types", preferred)

        if not isinstance(self.learning_pace, LearningPace):
            raise MissionInvariantViolation(
                "learning_pace must be a LearningPace",
                invariant="PlanningConstraints.learning_pace.type",
            )

        if self.maximum_daily_workload_minutes is not None:
            if isinstance(
                self.maximum_daily_workload_minutes, bool
            ) or not isinstance(self.maximum_daily_workload_minutes, int):
                raise MissionInvariantViolation(
                    "maximum_daily_workload_minutes must be an integer "
                    "when provided",
                    invariant=(
                        "PlanningConstraints.maximum_daily_workload_minutes.type"
                    ),
                )
            if self.maximum_daily_workload_minutes < 1:
                raise MissionInvariantViolation(
                    "maximum_daily_workload_minutes must be >= 1 when provided",
                    invariant=(
                        "PlanningConstraints.maximum_daily_workload_minutes.positive"
                    ),
                )

        if isinstance(self.maximum_mission_minutes, bool) or not isinstance(
            self.maximum_mission_minutes, int
        ):
            raise MissionInvariantViolation(
                "maximum_mission_minutes must be an integer",
                invariant="PlanningConstraints.maximum_mission_minutes.type",
            )
        if self.maximum_mission_minutes < 1:
            raise MissionInvariantViolation(
                "maximum_mission_minutes must be >= 1",
                invariant="PlanningConstraints.maximum_mission_minutes.positive",
            )

    def effective_daily_cap_minutes(self) -> int | None:
        """Return the tightest applicable daily time cap, if any."""
        caps = [
            minutes
            for minutes in (
                self.available_study_minutes,
                self.maximum_daily_workload_minutes,
            )
            if minutes is not None
        ]
        if not caps:
            return None
        return min(caps)
