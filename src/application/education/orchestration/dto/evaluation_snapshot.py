"""EvaluationSnapshot — immutable application capture of one evaluation turn."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.education.orchestration.dto.educational_decision import (
    EducationalDecision,
)
from application.education.orchestration.dto.evaluation_summary import (
    EvaluationSummary,
)


@dataclass(frozen=True, slots=True)
class EvaluationSnapshot:
    """Frozen application view of a completed (or partial) evaluation.

    Mirrors orchestration outputs for callers. Does not reason educationally.
    """

    student_id: str
    evaluated_at: datetime
    stages_completed: tuple[str, ...]
    summary: EvaluationSummary
    decisions: tuple[EducationalDecision, ...]
    evidence_id: str | None = None

    def __post_init__(self) -> None:
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise ValueError("student_id is required")
        object.__setattr__(self, "student_id", student_id)

        if not isinstance(self.evaluated_at, datetime):
            raise ValueError("evaluated_at must be a datetime")

        stages = tuple(self.stages_completed or ())
        cleaned_stages: list[str] = []
        for stage in stages:
            if not isinstance(stage, str) or not stage.strip():
                raise ValueError("stages_completed must contain non-empty strings")
            cleaned_stages.append(stage.strip())
        object.__setattr__(self, "stages_completed", tuple(cleaned_stages))

        if not isinstance(self.summary, EvaluationSummary):
            raise ValueError("summary must be an EvaluationSummary")

        decisions = tuple(self.decisions or ())
        for decision in decisions:
            if not isinstance(decision, EducationalDecision):
                raise ValueError(
                    "decisions must contain EducationalDecision instances"
                )
        object.__setattr__(self, "decisions", decisions)

        evidence_id = (self.evidence_id or "").strip() or None
        object.__setattr__(self, "evidence_id", evidence_id)

    def decision_count(self) -> int:
        return len(self.decisions)

    def top_decision(self) -> EducationalDecision | None:
        if not self.decisions:
            return None
        return self.decisions[0]
