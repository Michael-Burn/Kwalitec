"""Validation for assessment events and learning feedback."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.domain.assessment_pipeline.assessment_event import AssessmentEvent
from app.domain.assessment_pipeline.learning_feedback import LearningFeedback


class ValidationSeverity(StrEnum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class FeedbackValidationIssue:
    code: str
    message: str
    severity: ValidationSeverity = ValidationSeverity.ERROR


@dataclass(frozen=True)
class FeedbackValidationResult:
    passed: bool
    summary: str
    issues: tuple[FeedbackValidationIssue, ...] = ()

    @property
    def errors(self) -> tuple[FeedbackValidationIssue, ...]:
        return tuple(
            i for i in self.issues if i.severity == ValidationSeverity.ERROR
        )


def validate_assessment_event(event: AssessmentEvent) -> FeedbackValidationResult:
    """Validate that an assessment event is structurally sound evidence."""
    issues: list[FeedbackValidationIssue] = []

    if not (event.event_id or "").strip():
        issues.append(
            FeedbackValidationIssue(
                code="missing_event_id",
                message="Assessment event requires event_id.",
            )
        )
    if not (event.twin_id or "").strip():
        issues.append(
            FeedbackValidationIssue(
                code="missing_twin_id",
                message="Assessment event requires twin_id.",
            )
        )
    if not (event.student_id or "").strip():
        issues.append(
            FeedbackValidationIssue(
                code="missing_student_id",
                message="Assessment event requires student_id.",
            )
        )

    if event.event_type.value in {
        "question_attempt",
        "quiz_submission",
        "formula_recall",
    }:
        if event.correct is None and event.score is None:
            issues.append(
                FeedbackValidationIssue(
                    code="missing_performance",
                    message=(
                        f"{event.event_type.value} requires correct and/or score."
                    ),
                    severity=ValidationSeverity.WARNING,
                )
            )

    if event.event_type.value in {
        "mission_step_completion",
        "mission_completion",
    } and not (event.mission_id or "").strip():
        issues.append(
            FeedbackValidationIssue(
                code="missing_mission_id",
                message=f"{event.event_type.value} requires mission_id.",
            )
        )

    if (
        event.event_type.value == "mission_step_completion"
        and not (event.step_id or "").strip()
    ):
        issues.append(
            FeedbackValidationIssue(
                code="missing_step_id",
                message="mission_step_completion requires step_id.",
            )
        )

    if event.score is not None and not (0.0 <= float(event.score) <= 1.0):
        issues.append(
            FeedbackValidationIssue(
                code="score_out_of_range",
                message="score must be between 0.0 and 1.0 inclusive.",
            )
        )

    errors = [i for i in issues if i.severity == ValidationSeverity.ERROR]
    if errors:
        return FeedbackValidationResult(
            passed=False,
            summary=f"Assessment event validation failed ({len(errors)} error(s)).",
            issues=tuple(issues),
        )
    if issues:
        return FeedbackValidationResult(
            passed=True,
            summary="Assessment event valid with warnings.",
            issues=tuple(issues),
        )
    return FeedbackValidationResult(
        passed=True,
        summary="Assessment event valid.",
        issues=(),
    )


def validate_learning_feedback(
    feedback: LearningFeedback,
) -> FeedbackValidationResult:
    """Validate structured learning feedback completeness."""
    issues: list[FeedbackValidationIssue] = []
    if not (feedback.activity or "").strip():
        issues.append(
            FeedbackValidationIssue(
                code="missing_activity",
                message="Learning feedback requires activity description.",
            )
        )
    if not (feedback.performance or "").strip():
        issues.append(
            FeedbackValidationIssue(
                code="missing_performance",
                message="Learning feedback requires performance label.",
            )
        )
    if not (feedback.suggested_next_action or "").strip():
        issues.append(
            FeedbackValidationIssue(
                code="missing_next_action",
                message="Learning feedback requires suggested_next_action.",
            )
        )
    if not (0.0 <= float(feedback.confidence) <= 1.0):
        issues.append(
            FeedbackValidationIssue(
                code="confidence_out_of_range",
                message="confidence must be between 0.0 and 1.0.",
            )
        )

    errors = [i for i in issues if i.severity == ValidationSeverity.ERROR]
    if errors:
        return FeedbackValidationResult(
            passed=False,
            summary=f"Learning feedback validation failed ({len(errors)} error(s)).",
            issues=tuple(issues),
        )
    return FeedbackValidationResult(
        passed=True,
        summary="Learning feedback valid.",
        issues=tuple(issues),
    )
