"""Educational Feedback Loop application DTOs (ILE-005)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ReflectionPromptSnapshot:
    """One optional reflective question for presentation."""

    prompt_id: str
    question: str
    answer_choices: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class StudentReflectionInviteSnapshot:
    """Optional reflection invite for a Decision Journal entry."""

    decision_id: str = ""
    recommendation_title: str = ""
    prompts: tuple[ReflectionPromptSnapshot, ...] = ()
    intro_line: str = ""
    optional_note_label: str = ""
    submit_label: str = "Save reflection"
    skip_label: str = "Skip for now"
    available: bool = False


@dataclass(frozen=True)
class RecommendationReviewSnapshot:
    """Educational review projection (governance / internal use).

    Not rendered on student Home as a Sensei score — student surfaces
    receive reflection invites only.
    """

    decision_id: str = ""
    review_state: str = ""
    review_state_label: str = ""
    evidence_quality: str = ""
    evidence_quality_label: str = ""
    educational_assessment: str = ""
    future_learning: str = ""
    rationale_points: tuple[str, ...] = ()
    empty: bool = True


@dataclass(frozen=True)
class EducationalFeedbackLoopSnapshot:
    """Application façade snapshot for feedback-loop operations."""

    review: RecommendationReviewSnapshot = field(
        default_factory=RecommendationReviewSnapshot
    )
    reflection_invite: StudentReflectionInviteSnapshot = field(
        default_factory=StudentReflectionInviteSnapshot
    )
    sensei_review_recorded: bool = False
    page_title: str = "Educational feedback"
    intro_line: str = (
        "Optional reflection helps Sensei record whether "
        "guidance was educationally useful; it never scores engagement."
    )
