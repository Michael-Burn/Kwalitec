"""MissionConstraint — executable boundary on mission planning."""

from __future__ import annotations

from dataclasses import dataclass

from application.education.mission_generation.enums import MissionConstraintKind
from application.education.mission_generation.errors import MissionInvariantViolation


@dataclass(frozen=True, slots=True)
class MissionConstraint:
    """Immutable constraint attached to a mission or plan.

    Constraints encode planning boundaries such as prerequisite-first
    ordering or daily workload caps — never UI locks or persistence rules.
    """

    kind: MissionConstraintKind
    subject_id: str | None = None
    competency_id: str | None = None
    detail: float | None = None
    label: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.kind, MissionConstraintKind):
            raise MissionInvariantViolation(
                "kind must be a MissionConstraintKind",
                invariant="MissionConstraint.kind.type",
            )
        subject_id = (self.subject_id or "").strip() or None
        object.__setattr__(self, "subject_id", subject_id)
        competency_id = (self.competency_id or "").strip() or None
        object.__setattr__(self, "competency_id", competency_id)
        if self.detail is not None:
            if isinstance(self.detail, bool) or not isinstance(
                self.detail, int | float
            ):
                raise MissionInvariantViolation(
                    "detail must be a real number when provided",
                    invariant="MissionConstraint.detail.type",
                )
            object.__setattr__(self, "detail", round(float(self.detail), 4))
        label = (self.label or "").strip() or None
        object.__setattr__(self, "label", label)

    def requires_prerequisite_first(self) -> bool:
        return self.kind is MissionConstraintKind.REQUIRE_PREREQUISITE_FIRST

    def limits_workload(self) -> bool:
        return self.kind in {
            MissionConstraintKind.LIMIT_DAILY_WORKLOAD,
            MissionConstraintKind.RESPECT_AVAILABLE_TIME,
        }
