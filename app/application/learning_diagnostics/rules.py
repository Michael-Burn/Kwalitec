"""Deterministic Learning Diagnostics rules (KWP-008).

Identifies probable learning *causes* from existing evidence signals.
Reuses Learning Strategy calibration / performance helpers — does not
re-validate evidence or redesign Twin / Progress / Runtime.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.learning_diagnostics.dto import (
    DiagnosticCategory,
    DiagnosticEvidenceInput,
    DiagnosticFinding,
)
from app.application.learning_diagnostics.guidance import (
    explanation_for,
    guidance_for,
)
from app.application.learning_strategy.calibration import (
    calibrate,
    performance_band,
)
from app.application.learning_strategy.dto import (
    ConfidenceCalibration,
    StrategyEvidenceInput,
)

_LONG_GAP_DAYS = 14
_REPEATED_INCORRECT_MIN = 2

_FORMULA_TOKENS: tuple[str, ...] = (
    "formula",
    "recall",
    "remember",
    "v =",
    "discount factor",
    "force of interest",
    "pv =",
    "memor",
)


@dataclass(frozen=True)
class DiagnosticDecision:
    """Internal decision before guidance packaging."""

    category: DiagnosticCategory
    rule_id: str
    evidence_codes: tuple[str, ...]
    related_topic: str = ""
    mismatch_polarity: str = ""


def diagnose(evidence: DiagnosticEvidenceInput) -> tuple[DiagnosticDecision, ...]:
    """Return priority-ordered diagnostic decisions (primary first).

    Multiple supporting causes may be returned; callers take [0] as primary.
    """
    decisions: list[DiagnosticDecision] = []
    strategy = _as_strategy(evidence)
    calibration = calibrate(strategy)
    perf = performance_band(strategy)
    correct = evidence.practice_correct
    incorrect = evidence.practice_incorrect

    # 1. Retention decay
    if evidence.retention_risk and (
        evidence.weak_topic or incorrect > 0 or perf == "weak"
    ):
        decisions.append(
            DiagnosticDecision(
                category=DiagnosticCategory.RETENTION_DECAY,
                rule_id="retention_risk_weak",
                evidence_codes=("retention_risk", "weak_or_incorrect"),
            )
        )
    elif (
        evidence.days_since_topic_practice is not None
        and evidence.days_since_topic_practice >= _LONG_GAP_DAYS
        and (evidence.weak_topic or incorrect > correct or perf == "weak")
    ):
        decisions.append(
            DiagnosticDecision(
                category=DiagnosticCategory.RETENTION_DECAY,
                rule_id="retention_long_gap",
                evidence_codes=("long_gap", "weak_signal"),
            )
        )

    # 2. Prerequisite weakness / transfer
    if _prerequisite_pattern(evidence, incorrect=incorrect, correct=correct):
        codes = ["repeated_incorrect", "prerequisite_signal"]
        if evidence.strong_prerequisite:
            codes.append("prerequisite_transfer")
        decisions.append(
            DiagnosticDecision(
                category=DiagnosticCategory.PREREQUISITE_WEAKNESS,
                rule_id=(
                    "prerequisite_transfer"
                    if evidence.strong_prerequisite
                    else "prerequisite_weakness"
                ),
                evidence_codes=tuple(codes),
                related_topic=evidence.prerequisite_title,
            )
        )

    # 3. Confidence mismatch (reuse KWP-007 calibration)
    if calibration is ConfidenceCalibration.OVER_CONFIDENT:
        decisions.append(
            DiagnosticDecision(
                category=DiagnosticCategory.CONFIDENCE_MISMATCH,
                rule_id="confidence_over_vs_performance",
                evidence_codes=(
                    "high_confidence",
                    "weak_or_mixed_practice",
                ),
                mismatch_polarity="over",
            )
        )
    elif calibration is ConfidenceCalibration.UNDER_CONFIDENT:
        decisions.append(
            DiagnosticDecision(
                category=DiagnosticCategory.CONFIDENCE_MISMATCH,
                rule_id="confidence_under_vs_performance",
                evidence_codes=(
                    "low_confidence",
                    "strong_practice",
                ),
                mismatch_polarity="under",
            )
        )

    # 4. Conceptual misunderstanding
    if incorrect > 0 and calibration is ConfidenceCalibration.OVER_CONFIDENT:
        decisions.append(
            DiagnosticDecision(
                category=DiagnosticCategory.CONCEPTUAL_MISUNDERSTANDING,
                rule_id="conceptual_overconfident_errors",
                evidence_codes=(
                    "incorrect_outcomes",
                    "confidence_performance_mismatch",
                ),
            )
        )
    elif (
        incorrect >= _REPEATED_INCORRECT_MIN
        and incorrect > correct
        and not _formula_pattern(evidence)
        and not _calculation_pattern(evidence)
    ):
        decisions.append(
            DiagnosticDecision(
                category=DiagnosticCategory.CONCEPTUAL_MISUNDERSTANDING,
                rule_id="conceptual_repeated_incorrect",
                evidence_codes=("repeated_incorrect", "conceptual_check"),
            )
        )

    # 5. Formula recall vs calculation accuracy
    if _formula_pattern(evidence) and incorrect > 0:
        decisions.append(
            DiagnosticDecision(
                category=DiagnosticCategory.FORMULA_RECALL_WEAKNESS,
                rule_id="formula_recall_numeric_misses",
                evidence_codes=("numeric_misses", "formula_signal"),
            )
        )
    elif _calculation_pattern(evidence) and incorrect > 0:
        decisions.append(
            DiagnosticDecision(
                category=DiagnosticCategory.CALCULATION_ACCURACY,
                rule_id="calculation_numeric_misses",
                evidence_codes=("numeric_misses", "calculation_signal"),
            )
        )

    # 6. Reading interpretation
    if incorrect > 0 and (evidence.reading_skipped or (
        evidence.reading_completed
        and incorrect >= correct
        and evidence.mcq_incorrect > 0
    )):
        decisions.append(
            DiagnosticDecision(
                category=DiagnosticCategory.READING_INTERPRETATION,
                rule_id=(
                    "reading_skipped_weak_practice"
                    if evidence.reading_skipped
                    else "reading_completed_practice_misses"
                ),
                evidence_codes=(
                    "practice_incorrect",
                    "reading_signal",
                ),
            )
        )

    # 7. Exam technique
    if (
        evidence.finish_verdict in {"partially", "no"}
        and (incorrect > 0 or evidence.practice_unscored > 0)
    ) or evidence.consecutive_partial_finishes >= 2:
        decisions.append(
            DiagnosticDecision(
                category=DiagnosticCategory.EXAM_TECHNIQUE,
                rule_id="exam_technique_partial_mixed",
                evidence_codes=("partial_or_incomplete", "mixed_practice"),
            )
        )

    # 8. Inconsistent practice
    if evidence.consecutive_partial_finishes >= 2 or (
        evidence.streak_days is not None
        and evidence.streak_days == 0
        and evidence.recent_session_count is not None
        and evidence.recent_session_count <= 1
        and (incorrect > 0 or evidence.finish_verdict == "partially")
    ):
        decisions.append(
            DiagnosticDecision(
                category=DiagnosticCategory.INCONSISTENT_PRACTICE,
                rule_id="inconsistent_cadence_or_partials",
                evidence_codes=("uneven_cadence", "partial_finishes"),
            )
        )

    # 9. Improving understanding (success cause)
    if evidence.recovered_after_misses and correct > 0 and incorrect > 0:
        decisions.append(
            DiagnosticDecision(
                category=DiagnosticCategory.IMPROVING_UNDERSTANDING,
                rule_id="improving_after_misses",
                evidence_codes=("correct_after_misses", "improving"),
            )
        )

    # 10. Strong performance (success cause)
    if (
        correct > 0
        and incorrect == 0
        and evidence.finish_verdict in {"yes", ""}
        and (
            evidence.progress_advanced
            or evidence.mission_completed
            or calibration
            in {
                ConfidenceCalibration.HEALTHY,
                ConfidenceCalibration.UNKNOWN,
            }
        )
    ):
        decisions.append(
            DiagnosticDecision(
                category=DiagnosticCategory.STRONG_PERFORMANCE,
                rule_id="strong_accepted_practice",
                evidence_codes=("strong_practice", "accepted_study"),
            )
        )

    if not decisions:
        decisions.append(
            DiagnosticDecision(
                category=DiagnosticCategory.INSUFFICIENT_SIGNAL,
                rule_id="insufficient_signal",
                evidence_codes=("thin_evidence",),
            )
        )

    return _dedupe(tuple(decisions))


def finding_from_decision(
    decision: DiagnosticDecision,
    evidence: DiagnosticEvidenceInput,
) -> DiagnosticFinding:
    """Package a decision into a student-safe finding."""
    guidance = guidance_for(
        decision.category,
        evidence,
        related_topic=decision.related_topic,
        mismatch_polarity=decision.mismatch_polarity,
    )
    explanation = explanation_for(
        decision.category,
        evidence,
        related_topic=decision.related_topic,
        mismatch_polarity=decision.mismatch_polarity,
    )
    return DiagnosticFinding(
        category=decision.category,
        guidance=guidance,
        explanation=explanation,
        rule_id=decision.rule_id,
        evidence_codes=decision.evidence_codes,
        focus_topic=evidence.topic_title,
        related_topic=decision.related_topic,
        mismatch_polarity=decision.mismatch_polarity,
    )


def _as_strategy(evidence: DiagnosticEvidenceInput) -> StrategyEvidenceInput:
    return StrategyEvidenceInput(
        topic_title=evidence.topic_title,
        learning_objectives=evidence.learning_objectives,
        practice_correct=evidence.practice_correct,
        practice_incorrect=evidence.practice_incorrect,
        practice_attempted=evidence.practice_attempted,
        practice_unscored=evidence.practice_unscored,
        finish_verdict=evidence.finish_verdict,
        progress_advanced=evidence.progress_advanced,
        mission_completed=evidence.mission_completed,
        has_reflection=evidence.has_reflection,
        abandoned=evidence.abandoned,
        reported_confidence=evidence.reported_confidence,
        twin_confidence_band=evidence.twin_confidence_band,
        days_since_topic_practice=evidence.days_since_topic_practice,
        retention_risk=evidence.retention_risk,
        weak_topic=evidence.weak_topic,
        recent_session_count=evidence.recent_session_count,
        streak_days=evidence.streak_days,
        consecutive_partial_finishes=evidence.consecutive_partial_finishes,
        consecutive_strong_sittings=evidence.consecutive_strong_sittings,
        next_topic_title=evidence.next_topic_title,
    )


def _prerequisite_pattern(
    evidence: DiagnosticEvidenceInput,
    *,
    incorrect: int,
    correct: int,
) -> bool:
    if evidence.prerequisite_title and incorrect >= _REPEATED_INCORRECT_MIN:
        return True
    if (
        evidence.weak_topic
        and incorrect >= _REPEATED_INCORRECT_MIN
        and incorrect > correct
    ):
        return True
    if (
        evidence.strong_prerequisite
        and incorrect > 0
        and (evidence.dependent_topic_title or evidence.topic_title)
    ):
        return True
    return False


def _formula_pattern(evidence: DiagnosticEvidenceInput) -> bool:
    if evidence.numeric_incorrect <= 0 and evidence.short_structured_incorrect <= 0:
        # Allow hint-only formula signal when any incorrect practice exists.
        if evidence.practice_incorrect <= 0:
            return False
    blob = " ".join(
        [
            *evidence.learning_objectives,
            *evidence.common_mistake_hints,
            *evidence.practice_hints,
            evidence.topic_title,
        ]
    ).lower()
    if any(token in blob for token in _FORMULA_TOKENS):
        return True
    # Numeric misses without calculation-only signal + short structured misses
    # that mention recall-like mistakes.
    if evidence.numeric_incorrect > 0 and any(
        token in blob for token in ("formula", "recall", "v ", "discount")
    ):
        return True
    return False


def _calculation_pattern(evidence: DiagnosticEvidenceInput) -> bool:
    if evidence.numeric_incorrect <= 0:
        return False
    if _formula_pattern(evidence):
        # Prefer formula when formula tokens dominate.
        blob = " ".join(evidence.common_mistake_hints).lower()
        calc_tokens = ("arithmetic", "rounding", "calculation", "slip")
        if any(token in blob for token in calc_tokens):
            return True
        return False
    # Numeric incorrect with some numeric correct → method present, calc slips.
    if evidence.numeric_correct > 0 and evidence.numeric_incorrect > 0:
        return True
    if evidence.numeric_incorrect > 0 and evidence.mcq_incorrect == 0:
        return True
    return False


def _dedupe(
    decisions: tuple[DiagnosticDecision, ...],
) -> tuple[DiagnosticDecision, ...]:
    seen: set[DiagnosticCategory] = set()
    out: list[DiagnosticDecision] = []
    for decision in decisions:
        if decision.category in seen:
            continue
        seen.add(decision.category)
        out.append(decision)
    return tuple(out)
