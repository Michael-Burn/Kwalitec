"""Sensei self-reflection records (ILE-005).

Internal educational review composition. Not exposed directly to learners.
Improves educational quality governance — never recommendation re-ranking.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.educational_feedback_loop.enums import (
    EvidenceQualityBand,
    RecommendationReviewState,
    SenseiAssessmentFocus,
)
from app.domain.educational_feedback_loop.invariants import (
    assert_calibration_speech_safe,
)
from app.domain.educational_feedback_loop.review import RecommendationReview


@dataclass(frozen=True)
class SenseiEducationalReview:
    """Internal Sensei educational review for one recommendation record.

    Observation → Original recommendation → Later evidence →
    Educational assessment → Future learning.
    """

    decision_id: str
    observation: str
    original_recommendation: str
    later_evidence: str
    educational_assessment: str
    future_learning: str
    review_state: RecommendationReviewState
    evidence_quality: EvidenceQualityBand
    assessment_focus: SenseiAssessmentFocus
    rationale_points: tuple[str, ...] = ()
    learner_visible: bool = False
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)


def compose_sensei_review(
    *,
    review: RecommendationReview,
    observation: str = "",
    original_recommendation: str = "",
    later_evidence: str = "",
    assessment_focus: SenseiAssessmentFocus = (
        SenseiAssessmentFocus.EDUCATIONAL_USEFULNESS
    ),
) -> SenseiEducationalReview:
    """Compose an internal Sensei educational review from a domain review.

    Args:
        review: Assessed recommendation review.
        observation: Original educational observation.
        original_recommendation: Guidance offered at the time.
        later_evidence: Appended outcome / reflection / evidence summary.
        assessment_focus: Primary calibration focus.

    Returns:
        Immutable internal review — ``learner_visible`` is always False.
    """
    obs = (observation or "").strip() or (
        "Educational observation was not recorded for this episode."
    )
    original = (original_recommendation or "").strip() or (
        "Original recommendation text was not available."
    )
    later = (later_evidence or "").strip() or (
        "No later educational evidence has been appended yet."
    )
    focus = assessment_focus
    if review.review_state == RecommendationReviewState.EVIDENCE_INSUFFICIENT:
        focus = SenseiAssessmentFocus.EVIDENCE_QUALITY

    record = SenseiEducationalReview(
        decision_id=review.decision_id,
        observation=obs,
        original_recommendation=original,
        later_evidence=later,
        educational_assessment=review.educational_assessment,
        future_learning=review.future_learning,
        review_state=review.review_state,
        evidence_quality=review.evidence_quality,
        assessment_focus=focus,
        rationale_points=review.rationale_points,
        learner_visible=False,
        metadata=(
            ("governance", "educational_quality"),
            ("learner_visible", "false"),
        ),
    )
    _validate_sensei_review(record)
    return record


def summarise_later_evidence(
    *,
    outcome_summary: str = "",
    reflection_note: str = "",
    evidence_updates: tuple[str, ...] | list[str] = (),
) -> str:
    """Build a compact later-evidence paragraph for Sensei review."""
    parts: list[str] = []
    if (outcome_summary or "").strip():
        parts.append(f"Outcome: {outcome_summary.strip()}")
    if (reflection_note or "").strip():
        parts.append(f"Reflection: {reflection_note.strip()}")
    for item in evidence_updates or ():
        if (item or "").strip():
            parts.append(f"Evidence update: {item.strip()}")
    return " | ".join(parts) if parts else ""


def _validate_sensei_review(record: SenseiEducationalReview) -> None:
    for field_name, text in (
        ("observation", record.observation),
        ("original_recommendation", record.original_recommendation),
        ("later_evidence", record.later_evidence),
        ("educational_assessment", record.educational_assessment),
        ("future_learning", record.future_learning),
    ):
        if text:
            assert_calibration_speech_safe(text, field=field_name)
    if record.learner_visible:
        raise ValueError(
            "Sensei educational reviews must not be learner-visible"
        )
