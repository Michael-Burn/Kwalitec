"""Educational Feedback Loop domain (ILE-005).

Evaluates educational effectiveness of Study Sensei guidance over time.
Measures and reflects on recommendation outcomes — never re-selects or
re-ranks recommendations. No second educational authority.
"""

from __future__ import annotations

from app.domain.educational_feedback_loop.enums import (
    EVIDENCE_QUALITY_LABELS,
    FORBIDDEN_CALIBRATION_TERMS,
    REFLECTION_ANSWER_LABELS,
    REFLECTION_PROMPT_TEXT,
    REVIEW_STATE_LABELS,
    EvidenceQualityBand,
    RecommendationReviewState,
    ReflectionAnswer,
    SenseiAssessmentFocus,
    StudentReflectionPromptId,
)
from app.domain.educational_feedback_loop.invariants import (
    FORBIDDEN_STUDENT_TERMS,
    assert_calibration_speech_safe,
    assert_student_safe_text,
)
from app.domain.educational_feedback_loop.reflection import (
    StudentReflectionInvite,
    StudentReflectionPrompt,
    compose_reflection_invite,
)
from app.domain.educational_feedback_loop.review import (
    FeedbackEvidenceInput,
    RecommendationReview,
    assess_recommendation_review,
    empty_recommendation_review,
    format_reflection_note,
    parse_reflection_answers_from_note,
)
from app.domain.educational_feedback_loop.sensei_reflection import (
    SenseiEducationalReview,
    compose_sensei_review,
    summarise_later_evidence,
)

__all__ = [
    "EVIDENCE_QUALITY_LABELS",
    "FORBIDDEN_CALIBRATION_TERMS",
    "FORBIDDEN_STUDENT_TERMS",
    "REFLECTION_ANSWER_LABELS",
    "REFLECTION_PROMPT_TEXT",
    "REVIEW_STATE_LABELS",
    "EvidenceQualityBand",
    "FeedbackEvidenceInput",
    "RecommendationReview",
    "RecommendationReviewState",
    "ReflectionAnswer",
    "SenseiAssessmentFocus",
    "SenseiEducationalReview",
    "StudentReflectionInvite",
    "StudentReflectionPrompt",
    "StudentReflectionPromptId",
    "assert_calibration_speech_safe",
    "assert_student_safe_text",
    "assess_recommendation_review",
    "compose_reflection_invite",
    "compose_sensei_review",
    "empty_recommendation_review",
    "format_reflection_note",
    "parse_reflection_answers_from_note",
    "summarise_later_evidence",
]
