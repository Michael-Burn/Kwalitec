"""ExamTarget — optional examination deadline input for scheduling."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from application.education.revision_planner.errors import ScheduleInvariantViolation


@dataclass(frozen=True, slots=True)
class ExamTarget:
    """Optional examination target that bounds the planning horizon."""

    examination_id: str
    exam_date: date
    subject_id: str | None = None

    def __post_init__(self) -> None:
        examination_id = (self.examination_id or "").strip()
        if not examination_id:
            raise ScheduleInvariantViolation(
                "examination_id must be a non-empty string",
                invariant="ExamTarget.examination_id.required",
            )
        object.__setattr__(self, "examination_id", examination_id)
        if not isinstance(self.exam_date, date):
            raise ScheduleInvariantViolation(
                "exam_date must be a date",
                invariant="ExamTarget.exam_date.type",
            )
        subject_id = (self.subject_id or "").strip() or None
        object.__setattr__(self, "subject_id", subject_id)
