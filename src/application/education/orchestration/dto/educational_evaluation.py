"""EducationalEvaluation — primary application result of orchestration.

Success and failure are both represented as immutable results. No HTTP
exceptions, no retries, no logging side effects.
"""

from __future__ import annotations

from dataclasses import dataclass

from application.education.orchestration.dto.educational_decision import (
    EducationalDecision,
)
from application.education.orchestration.dto.evaluation_snapshot import (
    EvaluationSnapshot,
)
from application.education.orchestration.dto.evaluation_summary import (
    EvaluationSummary,
)


@dataclass(frozen=True, slots=True)
class EducationalEvaluation:
    """Deterministic application outcome of an orchestration turn.

    On success, ``summary``, ``snapshot``, and ``decisions`` are populated.
    On failure, ``failure_code`` / ``failure_message`` explain the stop,
    and ``stages_completed`` records how far composition progressed.
    """

    success: bool
    student_id: str
    stages_completed: tuple[str, ...]
    summary: EvaluationSummary | None = None
    snapshot: EvaluationSnapshot | None = None
    decisions: tuple[EducationalDecision, ...] = ()
    evidence_id: str | None = None
    failure_code: str | None = None
    failure_message: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.success, bool):
            raise ValueError("success must be a bool")

        student_id = (self.student_id or "").strip()
        if not student_id:
            raise ValueError("student_id is required")
        object.__setattr__(self, "student_id", student_id)

        stages = tuple(self.stages_completed or ())
        cleaned_stages: list[str] = []
        for stage in stages:
            if not isinstance(stage, str) or not stage.strip():
                raise ValueError("stages_completed must contain non-empty strings")
            cleaned_stages.append(stage.strip())
        object.__setattr__(self, "stages_completed", tuple(cleaned_stages))

        if self.summary is not None and not isinstance(
            self.summary, EvaluationSummary
        ):
            raise ValueError("summary must be an EvaluationSummary or None")

        if self.snapshot is not None and not isinstance(
            self.snapshot, EvaluationSnapshot
        ):
            raise ValueError("snapshot must be an EvaluationSnapshot or None")

        decisions = tuple(self.decisions or ())
        for decision in decisions:
            if not isinstance(decision, EducationalDecision):
                raise ValueError(
                    "decisions must contain EducationalDecision instances"
                )
        object.__setattr__(self, "decisions", decisions)

        evidence_id = (self.evidence_id or "").strip() or None
        object.__setattr__(self, "evidence_id", evidence_id)

        failure_code = (self.failure_code or "").strip() or None
        failure_message = (self.failure_message or "").strip() or None
        object.__setattr__(self, "failure_code", failure_code)
        object.__setattr__(self, "failure_message", failure_message)

        if self.success:
            if self.summary is None or self.snapshot is None:
                raise ValueError(
                    "successful evaluation requires summary and snapshot"
                )
            if failure_code is not None or failure_message is not None:
                raise ValueError(
                    "successful evaluation must not carry failure fields"
                )
        else:
            if failure_code is None:
                raise ValueError("failed evaluation requires failure_code")

    @classmethod
    def succeeded(
        cls,
        *,
        student_id: str,
        stages_completed: tuple[str, ...],
        summary: EvaluationSummary,
        snapshot: EvaluationSnapshot,
        decisions: tuple[EducationalDecision, ...],
        evidence_id: str | None = None,
    ) -> EducationalEvaluation:
        """Build a successful evaluation result."""
        return cls(
            success=True,
            student_id=student_id,
            stages_completed=stages_completed,
            summary=summary,
            snapshot=snapshot,
            decisions=decisions,
            evidence_id=evidence_id,
        )

    @classmethod
    def failed(
        cls,
        *,
        student_id: str,
        stages_completed: tuple[str, ...],
        failure_code: str,
        failure_message: str,
        evidence_id: str | None = None,
    ) -> EducationalEvaluation:
        """Build a failed evaluation result with honest progress."""
        return cls(
            success=False,
            student_id=student_id,
            stages_completed=stages_completed,
            evidence_id=evidence_id,
            failure_code=failure_code,
            failure_message=failure_message,
        )

    @property
    def failed_result(self) -> bool:
        """True when orchestration stopped without a full evaluation."""
        return not self.success
