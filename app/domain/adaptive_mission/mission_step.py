"""Mission steps and abstract learning activities."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ActivityType(StrEnum):
    """Abstract learning activities supported by the Mission Engine.

    Activities remain abstract — no calendar scheduling in AME-001.
    """

    REVIEW = "review"
    PRACTICE = "practice"
    REVISION = "revision"
    WORKED_EXAMPLE = "worked_example"
    FORMULA_RECALL = "formula_recall"
    MIXED_QUESTIONS = "mixed_questions"
    CONCEPT_RECOVERY = "concept_recovery"
    PREREQUISITE_REVIEW = "prerequisite_review"
    REFLECTION = "reflection"


@dataclass(frozen=True)
class MissionActivity:
    """One abstract activity within a mission step."""

    activity_type: ActivityType
    concept_id: str
    title: str
    estimated_minutes: int = 10
    reason: str = ""
    evidence_references: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        activity = (
            self.activity_type
            if isinstance(self.activity_type, ActivityType)
            else ActivityType(str(self.activity_type))
        )
        object.__setattr__(self, "activity_type", activity)
        object.__setattr__(
            self, "evidence_references", tuple(self.evidence_references or ())
        )
        object.__setattr__(
            self, "estimated_minutes", max(1, int(self.estimated_minutes))
        )


@dataclass(frozen=True)
class MissionStep:
    """Ordered step in an adaptive mission."""

    step_id: str
    order: int
    activity: MissionActivity
    success_criterion: str = ""
    completed: bool = False

    def __post_init__(self) -> None:
        if not (self.step_id or "").strip():
            raise ValueError("step_id is required")
        object.__setattr__(self, "order", int(self.order))
