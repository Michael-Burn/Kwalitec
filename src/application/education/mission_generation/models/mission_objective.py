"""MissionObjective — structured goal of an executable mission."""

from __future__ import annotations

from dataclasses import dataclass

from application.education.mission_generation.enums import MissionObjectiveCode
from application.education.mission_generation.errors import MissionInvariantViolation


@dataclass(frozen=True, slots=True)
class MissionObjective:
    """Immutable structured objective for one mission.

    Objectives are machine-readable codes with optional curriculum scope.
    They never carry free-form natural language or mastery estimates.
    """

    code: MissionObjectiveCode
    subject_id: str | None = None
    competency_id: str | None = None
    coverage_weight: float = 1.0

    def __post_init__(self) -> None:
        if not isinstance(self.code, MissionObjectiveCode):
            raise MissionInvariantViolation(
                "code must be a MissionObjectiveCode",
                invariant="MissionObjective.code.type",
            )
        subject_id = (self.subject_id or "").strip() or None
        object.__setattr__(self, "subject_id", subject_id)
        competency_id = (self.competency_id or "").strip() or None
        object.__setattr__(self, "competency_id", competency_id)
        if isinstance(self.coverage_weight, bool) or not isinstance(
            self.coverage_weight, int | float
        ):
            raise MissionInvariantViolation(
                "coverage_weight must be a real number",
                invariant="MissionObjective.coverage_weight.type",
            )
        weight = float(self.coverage_weight)
        if weight <= 0.0 or weight > 1.0:
            raise MissionInvariantViolation(
                "coverage_weight must be in (0.0, 1.0]",
                invariant="MissionObjective.coverage_weight.range",
            )
        object.__setattr__(self, "coverage_weight", round(weight, 4))

    def correlation_key(self) -> str:
        return (
            f"{self.code.value}:"
            f"{self.subject_id or '-'}:"
            f"{self.competency_id or '-'}"
        )
