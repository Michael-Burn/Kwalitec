"""Recommendation review composition (ILE-005).

Pure educational assessment of whether earlier guidance was useful.
Never re-ranks, never mutates Twin, never invents educational need.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from app.domain.decision_journal.enums import (
    QualitativeConfidence,
    ReflectionStatus,
    StudentAction,
)
from app.domain.educational_feedback_loop.enums import (
    EVIDENCE_QUALITY_LABELS,
    REVIEW_STATE_LABELS,
    EvidenceQualityBand,
    RecommendationReviewState,
    ReflectionAnswer,
)
from app.domain.educational_feedback_loop.invariants import (
    assert_calibration_speech_safe,
)


@dataclass(frozen=True)
class FeedbackEvidenceInput:
    """Opaque educational evidence for reviewing one recommendation record.

    Sourced from Decision Journal — never from engagement telemetry.
    """

    decision_id: str = ""
    recommendation: str = ""
    observation: str = ""
    meaning: str = ""
    expected_benefit: str = ""
    student_action: str = StudentAction.NONE_YET.value
    outcome_summary: str = ""
    reflection_status: str = ReflectionStatus.PENDING.value
    reflection_note: str = ""
    qualitative_confidence: str = QualitativeConfidence.EMERGING.value
    supporting_evidence_summary: str = ""
    evidence_update_count: int = 0
    evidence_update_summaries: tuple[str, ...] = ()
    helped_answer: str = ""
    timing_answer: str = ""
    understood_why_answer: str = ""
    same_decision_answer: str = ""


@dataclass(frozen=True)
class RecommendationReview:
    """Educational review of one significant recommendation.

    Append-only assessment — does not rewrite the original guidance.
    """

    decision_id: str
    review_state: RecommendationReviewState
    review_state_label: str
    evidence_quality: EvidenceQualityBand
    evidence_quality_label: str
    educational_assessment: str
    future_learning: str
    rationale_points: tuple[str, ...] = ()
    empty: bool = False
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)


def empty_recommendation_review(
    *,
    decision_id: str = "",
    reason: str = "",
) -> RecommendationReview:
    """Calm empty review when no recommendation record is available."""
    assessment = reason or (
        "No recommendation record is available to review yet."
    )
    return RecommendationReview(
        decision_id=decision_id or "",
        review_state=RecommendationReviewState.REQUIRES_FUTURE_OBSERVATION,
        review_state_label=REVIEW_STATE_LABELS[
            RecommendationReviewState.REQUIRES_FUTURE_OBSERVATION
        ],
        evidence_quality=EvidenceQualityBand.INSUFFICIENT,
        evidence_quality_label=EVIDENCE_QUALITY_LABELS[
            EvidenceQualityBand.INSUFFICIENT
        ],
        educational_assessment=assessment,
        future_learning=(
            "Wait for a significant recommendation and later educational "
            "evidence before calibrating guidance quality."
        ),
        rationale_points=(),
        empty=True,
        metadata=(("availability", "empty"),),
    )


def assess_recommendation_review(
    evidence: FeedbackEvidenceInput | Mapping[str, Any],
) -> RecommendationReview:
    """Assess whether earlier guidance was educationally useful.

    Deterministic from journal / reflection inputs. Never optimises for
    engagement, clicks, streaks, or screen time.

    Args:
        evidence: Journal-derived educational fragments.

    Returns:
        Immutable ``RecommendationReview``.
    """
    inp = _normalise_input(evidence)
    if not (inp.decision_id or inp.recommendation).strip():
        return empty_recommendation_review()

    quality = _evidence_quality(inp)
    state, points = _review_state(inp, quality)
    assessment = _educational_assessment(inp, state, quality)
    future = _future_learning(inp, state, quality)

    review = RecommendationReview(
        decision_id=inp.decision_id.strip(),
        review_state=state,
        review_state_label=REVIEW_STATE_LABELS[state],
        evidence_quality=quality,
        evidence_quality_label=EVIDENCE_QUALITY_LABELS[quality],
        educational_assessment=assessment,
        future_learning=future,
        rationale_points=tuple(points),
        empty=False,
        metadata=(
            ("source", "decision_journal"),
            ("student_action", inp.student_action),
        ),
    )
    _validate_review(review)
    return review


def _normalise_input(
    evidence: FeedbackEvidenceInput | Mapping[str, Any],
) -> FeedbackEvidenceInput:
    if isinstance(evidence, FeedbackEvidenceInput):
        return evidence
    updates = evidence.get("evidence_update_summaries") or ()
    if isinstance(updates, str):
        updates = (updates,)
    return FeedbackEvidenceInput(
        decision_id=str(evidence.get("decision_id") or ""),
        recommendation=str(evidence.get("recommendation") or ""),
        observation=str(evidence.get("observation") or ""),
        meaning=str(evidence.get("meaning") or ""),
        expected_benefit=str(evidence.get("expected_benefit") or ""),
        student_action=str(
            evidence.get("student_action") or StudentAction.NONE_YET.value
        ),
        outcome_summary=str(evidence.get("outcome_summary") or ""),
        reflection_status=str(
            evidence.get("reflection_status")
            or ReflectionStatus.PENDING.value
        ),
        reflection_note=str(evidence.get("reflection_note") or ""),
        qualitative_confidence=str(
            evidence.get("qualitative_confidence")
            or QualitativeConfidence.EMERGING.value
        ),
        supporting_evidence_summary=str(
            evidence.get("supporting_evidence_summary") or ""
        ),
        evidence_update_count=int(
            evidence.get("evidence_update_count") or len(tuple(updates))
        ),
        evidence_update_summaries=tuple(str(u) for u in updates),
        helped_answer=str(evidence.get("helped_answer") or ""),
        timing_answer=str(evidence.get("timing_answer") or ""),
        understood_why_answer=str(
            evidence.get("understood_why_answer") or ""
        ),
        same_decision_answer=str(
            evidence.get("same_decision_answer") or ""
        ),
    )


def _evidence_quality(inp: FeedbackEvidenceInput) -> EvidenceQualityBand:
    has_outcome = bool((inp.outcome_summary or "").strip())
    has_reflection = (
        inp.reflection_status == ReflectionStatus.REFLECTED.value
        or bool((inp.reflection_note or "").strip())
    )
    update_count = max(
        inp.evidence_update_count, len(inp.evidence_update_summaries)
    )
    has_prior = bool((inp.supporting_evidence_summary or "").strip())
    conf = (inp.qualitative_confidence or "").lower()

    if conf in (
        QualitativeConfidence.INSUFFICIENT.value,
        QualitativeConfidence.OBSERVATION_ONLY.value,
    ) and not has_outcome and not has_reflection and update_count == 0:
        return EvidenceQualityBand.INSUFFICIENT

    signals = sum(
        (
            1 if has_outcome else 0,
            1 if has_reflection else 0,
            1 if update_count > 0 else 0,
            1 if has_prior else 0,
            1
            if conf
            in (
                QualitativeConfidence.RELIABLE.value,
                QualitativeConfidence.HIGH.value,
            )
            else 0,
        )
    )
    if signals >= 4:
        return EvidenceQualityBand.STRONG
    if signals >= 3:
        return EvidenceQualityBand.ADEQUATE
    if signals >= 1:
        return EvidenceQualityBand.LIMITED
    return EvidenceQualityBand.INSUFFICIENT


def _review_state(
    inp: FeedbackEvidenceInput,
    quality: EvidenceQualityBand,
) -> tuple[RecommendationReviewState, list[str]]:
    points: list[str] = []
    action = inp.student_action or StudentAction.NONE_YET.value
    has_outcome = bool((inp.outcome_summary or "").strip())
    has_reflection = (
        inp.reflection_status == ReflectionStatus.REFLECTED.value
        or bool((inp.reflection_note or "").strip())
    )
    helped = _parse_answer(inp.helped_answer)
    timing = _parse_answer(inp.timing_answer)
    understood = _parse_answer(inp.understood_why_answer)
    same = _parse_answer(inp.same_decision_answer)
    affirmative = _affirmative_count(helped, timing, understood, same)
    negative = _negative_count(helped, timing, understood, same)

    if action == StudentAction.NONE_YET.value and not has_outcome:
        points.append("Learner response has not been recorded yet.")
        return (
            RecommendationReviewState.REQUIRES_FUTURE_OBSERVATION,
            points,
        )

    if quality == EvidenceQualityBand.INSUFFICIENT and not has_reflection:
        points.append("Educational evidence remains too thin to calibrate.")
        return RecommendationReviewState.EVIDENCE_INSUFFICIENT, points

    if not has_outcome and not has_reflection:
        points.append(
            "Student response is known, but later educational outcome "
            "and reflection are still absent."
        )
        return (
            RecommendationReviewState.REQUIRES_FUTURE_OBSERVATION,
            points,
        )

    if has_reflection and affirmative >= 3 and negative == 0 and has_outcome:
        points.append("Reflection and outcome both support the guidance.")
        return RecommendationReviewState.SUPPORTED, points

    if has_reflection and affirmative >= 2 and negative == 0:
        points.append("Reflection leans supportive; evidence is partial.")
        if has_outcome or quality in (
            EvidenceQualityBand.ADEQUATE,
            EvidenceQualityBand.STRONG,
        ):
            return RecommendationReviewState.SUPPORTED, points
        return RecommendationReviewState.PARTIALLY_SUPPORTED, points

    if has_reflection and negative >= 2:
        points.append(
            "Reflection suggests the guidance was less useful than hoped."
        )
        if affirmative >= 1 or has_outcome:
            return RecommendationReviewState.PARTIALLY_SUPPORTED, points
        return RecommendationReviewState.INCONCLUSIVE, points

    if has_outcome and has_reflection and affirmative >= 1 and negative >= 1:
        points.append("Later evidence is mixed.")
        return RecommendationReviewState.PARTIALLY_SUPPORTED, points

    if has_outcome and not has_reflection:
        points.append(
            "An outcome was recorded without learner reflection — "
            "usefulness remains provisional."
        )
        if quality in (
            EvidenceQualityBand.ADEQUATE,
            EvidenceQualityBand.STRONG,
        ):
            return RecommendationReviewState.PARTIALLY_SUPPORTED, points
        return RecommendationReviewState.INCONCLUSIVE, points

    if has_reflection and not has_outcome:
        points.append(
            "Reflection is present; educational outcome is still thin."
        )
        if affirmative >= 2:
            return RecommendationReviewState.PARTIALLY_SUPPORTED, points
        return RecommendationReviewState.INCONCLUSIVE, points

    points.append("Available signals do not yet support a firm judgement.")
    return RecommendationReviewState.INCONCLUSIVE, points


def _parse_answer(raw: str) -> ReflectionAnswer | None:
    value = (raw or "").strip().lower()
    if not value:
        return None
    try:
        return ReflectionAnswer(value)
    except ValueError:
        return None


def _affirmative_count(*answers: ReflectionAnswer | None) -> int:
    return sum(
        1
        for a in answers
        if a in (ReflectionAnswer.YES, ReflectionAnswer.MOSTLY)
    )


def _negative_count(*answers: ReflectionAnswer | None) -> int:
    return sum(1 for a in answers if a == ReflectionAnswer.NO)


def _educational_assessment(
    inp: FeedbackEvidenceInput,
    state: RecommendationReviewState,
    quality: EvidenceQualityBand,
) -> str:
    rec = (inp.recommendation or "this guidance").strip()
    if state == RecommendationReviewState.SUPPORTED:
        return (
            f"Later educational evidence supports that “{rec}” was a "
            "useful recommendation for the learner at the time."
        )
    if state == RecommendationReviewState.PARTIALLY_SUPPORTED:
        return (
            f"Later evidence partially supports “{rec}” — some educational "
            "benefit appears, but confidence remains measured."
        )
    if state == RecommendationReviewState.EVIDENCE_INSUFFICIENT:
        return (
            f"Evidence remains insufficient to judge whether “{rec}” "
            "was educationally useful."
        )
    if state == RecommendationReviewState.REQUIRES_FUTURE_OBSERVATION:
        return (
            f"“{rec}” still requires future observation before an "
            "educational usefulness judgement is honest."
        )
    return (
        f"Evidence around “{rec}” is inconclusive "
        f"({EVIDENCE_QUALITY_LABELS[quality].lower()}). "
        "Calibration should wait rather than overclaim."
    )


def _future_learning(
    inp: FeedbackEvidenceInput,
    state: RecommendationReviewState,
    quality: EvidenceQualityBand,
) -> str:
    if state == RecommendationReviewState.SUPPORTED:
        return (
            "Retain that similar evidence patterns can justify comparable "
            "guidance — without treating support as a licence to overclaim."
        )
    if state == RecommendationReviewState.PARTIALLY_SUPPORTED:
        return (
            "Note mixed usefulness. Prefer clearer timing, evidence, or "
            "explainability on similar future guidance."
        )
    if state == RecommendationReviewState.EVIDENCE_INSUFFICIENT:
        return (
            "Do not strengthen confidence language until more educational "
            "evidence is available."
        )
    if state == RecommendationReviewState.REQUIRES_FUTURE_OBSERVATION:
        return (
            "Keep watching for learner response, outcome, and optional "
            "reflection before revising educational judgement."
        )
    understood = _parse_answer(inp.understood_why_answer)
    if understood == ReflectionAnswer.NO:
        return (
            "Explainability may have been unclear — future guidance should "
            "state why more plainly without inventing certainty."
        )
    if quality == EvidenceQualityBand.LIMITED:
        return (
            "Limited evidence quality: prefer humble confidence and invite "
            "reflection rather than firmer claims."
        )
    return (
        "Treat this episode as inconclusive. Educational honesty beats "
        "premature calibration."
    )


def _validate_review(review: RecommendationReview) -> None:
    for field_name, text in (
        ("educational_assessment", review.educational_assessment),
        ("future_learning", review.future_learning),
    ):
        if text:
            assert_calibration_speech_safe(text, field=field_name)
    for point in review.rationale_points:
        assert_calibration_speech_safe(point, field="rationale")


def parse_reflection_answers_from_note(
    note: str,
) -> dict[str, str]:
    """Extract structured optional answers from a reflection note body."""
    mapping = {
        "did this recommendation help": "helped_answer",
        "was the timing appropriate": "timing_answer",
        "did you understand why": "understood_why_answer",
        "would you make the same decision": "same_decision_answer",
    }
    found: dict[str, str] = {}
    for line in (note or "").splitlines():
        lowered = line.strip().lower()
        for needle, key in mapping.items():
            if needle in lowered and ":" in line:
                raw = line.split(":", 1)[1].strip().lower()
                for answer in ReflectionAnswer:
                    if raw == answer.value or raw.startswith(answer.value):
                        found[key] = answer.value
                        break
                    label = {
                        ReflectionAnswer.YES: "yes",
                        ReflectionAnswer.MOSTLY: "mostly",
                        ReflectionAnswer.NO: "no",
                        ReflectionAnswer.SKIPPED: "prefer not",
                    }[answer]
                    if raw.startswith(label):
                        found[key] = answer.value
                        break
    return found


def format_reflection_note(
    *,
    helped: str = "",
    timing: str = "",
    understood_why: str = "",
    same_decision: str = "",
    free_text: str = "",
) -> str:
    """Compose a student-safe reflection note from optional answers."""
    lines: list[str] = []
    pairs: Sequence[tuple[str, str]] = (
        ("Did this recommendation help", helped),
        ("Was the timing appropriate", timing),
        ("Did you understand why it was recommended", understood_why),
        ("Would you make the same decision again", same_decision),
    )
    for prompt, raw in pairs:
        answer = _parse_answer(raw)
        if answer is None or answer == ReflectionAnswer.SKIPPED:
            continue
        label = {
            ReflectionAnswer.YES: "Yes",
            ReflectionAnswer.MOSTLY: "Mostly",
            ReflectionAnswer.NO: "No",
        }[answer]
        lines.append(f"{prompt}: {label}")
    extra = (free_text or "").strip()
    if extra:
        lines.append(extra)
    return "\n".join(lines)
