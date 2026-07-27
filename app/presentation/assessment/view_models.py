"""View models for Assessment Delivery templates."""

from __future__ import annotations

from dataclasses import dataclass

from application.assessment.dto.models import AssessmentDeliveryDTO

FORBIDDEN_LEARNER_TERMS = (
    "exam",
    "test score",
    "pass/fail",
    "failed",
    "digital twin",
    "mastery score",
    "mission engine",
)


@dataclass(frozen=True, slots=True)
class AssessmentShellViewModel:
    session_id: str
    page_title: str
    page_eyebrow: str
    page_description: str
    status: str
    allow_pause: bool


@dataclass(frozen=True, slots=True)
class AssessmentProgressViewModel:
    current_label: str
    remaining_label: str
    percent_complete: int
    current_index: int
    total_questions: int
    answered_count: int
    remaining_count: int
    can_go_previous: bool
    can_go_next: bool
    can_complete: bool
    is_complete: bool


@dataclass(frozen=True, slots=True)
class AssessmentQuestionViewModel:
    question_id: str
    item_type: str
    stem: str
    sequence_label: str
    options: tuple[dict[str, str], ...]
    hints: tuple[str, ...]
    placeholder: str | None
    unit_label: str | None
    accessibility_note: str | None
    input_name: str
    allows_multiple: bool
    is_numeric: bool
    is_text: bool
    is_confidence_only: bool
    invite_confidence: bool
    require_confidence: bool
    hints_available: bool
    hints_requested: int
    already_answered: bool
    renderer: str


@dataclass(frozen=True, slots=True)
class AssessmentPageViewModel:
    shell: AssessmentShellViewModel
    progress: AssessmentProgressViewModel
    purpose_label: str
    purpose_explanation: str
    after_completion: str
    question: AssessmentQuestionViewModel | None = None
    observation_count: int = 0
    result_id: str | None = None


_RENDERERS = {
    "multiple_choice": "multiple_choice",
    "multiple_response": "multiple_response",
    "numeric": "numeric",
    "formula": "text",
    "free_text": "text",
    "worked_solution": "text",
    "confidence_rating": "confidence",
    "reflection": "text",
    "concept_linking": "multiple_response",
}


def page_from_delivery(delivery: AssessmentDeliveryDTO) -> AssessmentPageViewModel:
    """Map delivery DTO to a template-friendly view model."""
    progress = delivery.progress
    current_label = (
        f"{progress.current_index + 1} of {progress.total_questions} checks"
        if progress.total_questions
        else "Learning check"
    )
    remaining_label = (
        f"{progress.remaining_count} remaining"
        if progress.remaining_count
        else "Ready to finish"
    )
    question_vm = None
    if delivery.question is not None:
        q = delivery.question
        question_vm = AssessmentQuestionViewModel(
            question_id=q.question_id,
            item_type=q.item_type,
            stem=q.stem,
            sequence_label=f"Check {q.sequence_index + 1}",
            options=q.options,
            hints=q.hints,
            placeholder=q.placeholder,
            unit_label=q.unit_label,
            accessibility_note=q.accessibility_note,
            input_name=q.input_name,
            allows_multiple=q.allows_multiple,
            is_numeric=q.is_numeric,
            is_text=q.is_text,
            is_confidence_only=q.is_confidence_only,
            invite_confidence=q.invite_confidence,
            require_confidence=q.require_confidence,
            hints_available=q.hints_available,
            hints_requested=q.hints_requested,
            already_answered=q.already_answered,
            renderer=_RENDERERS.get(q.item_type, "text"),
        )
    return AssessmentPageViewModel(
        shell=AssessmentShellViewModel(
            session_id=delivery.session.session_id,
            page_title=delivery.instrument_title,
            page_eyebrow=delivery.purpose_label,
            page_description=delivery.purpose_explanation,
            status=delivery.status,
            allow_pause=delivery.allow_pause,
        ),
        progress=AssessmentProgressViewModel(
            current_label=current_label,
            remaining_label=remaining_label,
            percent_complete=progress.percent_complete,
            current_index=progress.current_index,
            total_questions=progress.total_questions,
            answered_count=progress.answered_count,
            remaining_count=progress.remaining_count,
            can_go_previous=progress.can_go_previous,
            can_go_next=progress.can_go_next,
            can_complete=progress.can_complete,
            is_complete=progress.is_complete,
        ),
        purpose_label=delivery.purpose_label,
        purpose_explanation=delivery.purpose_explanation,
        after_completion=(
            "After you finish, Kwalitec uses what you shared to support "
            "your learning — not to grade you."
        ),
        question=question_vm,
        observation_count=delivery.observation_count,
        result_id=delivery.result.result_id if delivery.result else None,
    )
