"""Confidence calibration — internal labels → natural student guidance (KWP-007).

Never expose Healthy / Over-confident / Under-confident to learners.
"""

from __future__ import annotations

from app.application.learning_strategy.dto import (
    ConfidenceCalibration,
    StrategyEvidenceInput,
)
from app.domain.student_twin.confidence_band import (
    ConfidenceBand,
    confidence_band_from_score,
    resolve_confidence_band,
)

# Performance bands derived from sitting practice (not Twin mastery scores).
_PERF_STRONG = "strong"
_PERF_MIXED = "mixed"
_PERF_WEAK = "weak"
_PERF_UNKNOWN = "unknown"


def performance_band(evidence: StrategyEvidenceInput) -> str:
    """Classify sitting practice strength from Educational+ outcomes."""
    correct = evidence.practice_correct
    incorrect = evidence.practice_incorrect
    if correct <= 0 and incorrect <= 0:
        return _PERF_UNKNOWN
    if incorrect == 0 and correct > 0:
        return _PERF_STRONG
    if correct == 0 and incorrect > 0:
        return _PERF_WEAK
    if incorrect > correct:
        return _PERF_WEAK
    if correct > incorrect:
        return _PERF_STRONG
    return _PERF_MIXED


def calibrate(evidence: StrategyEvidenceInput) -> ConfidenceCalibration:
    """Determine internal confidence calibration from evidence + confidence.

    Uses reported confidence and/or Twin confidence band against practice
    performance. Returns UNKNOWN when confidence signal is absent.
    """
    perf = performance_band(evidence)
    high_conf = _is_high_confidence(evidence)
    low_conf = _is_low_confidence(evidence)
    if high_conf is None and low_conf is None:
        return ConfidenceCalibration.UNKNOWN

    if high_conf and perf == _PERF_WEAK:
        return ConfidenceCalibration.OVER_CONFIDENT
    if high_conf and perf == _PERF_MIXED:
        return ConfidenceCalibration.OVER_CONFIDENT
    if low_conf and perf == _PERF_STRONG:
        return ConfidenceCalibration.UNDER_CONFIDENT
    if high_conf is False and low_conf is False and perf in {
        _PERF_STRONG,
        _PERF_MIXED,
        _PERF_WEAK,
    }:
        return ConfidenceCalibration.HEALTHY
    if high_conf and perf == _PERF_STRONG:
        return ConfidenceCalibration.HEALTHY
    if low_conf and perf == _PERF_WEAK:
        return ConfidenceCalibration.HEALTHY
    return ConfidenceCalibration.UNKNOWN


def guidance_for(
    calibration: ConfidenceCalibration,
    *,
    topic: str,
) -> str:
    """Translate calibration into natural guidance — never label names."""
    focus = topic or "this topic"
    if calibration is ConfidenceCalibration.OVER_CONFIDENT:
        return (
            f"Today's practice on {focus} suggests checking assumptions "
            "carefully before moving on — certainty alone is not understanding."
        )
    if calibration is ConfidenceCalibration.UNDER_CONFIDENT:
        return (
            f"Your answers on {focus} were stronger than how sure you felt — "
            "a little more practice will help your certainty catch up."
        )
    if calibration is ConfidenceCalibration.HEALTHY:
        return (
            f"Your confidence and practice on {focus} are aligned — "
            "keep using that honest self-check."
        )
    return ""


def _is_high_confidence(evidence: StrategyEvidenceInput) -> bool | None:
    score = evidence.reported_confidence
    if score is not None:
        band = confidence_band_from_score(score)
        return band in (ConfidenceBand.HIGH, ConfidenceBand.VERY_HIGH)
    band_token = (evidence.twin_confidence_band or "").strip().lower()
    if not band_token:
        return None
    try:
        band = resolve_confidence_band(band_token)
    except ValueError:
        if any(
            token in band_token
            for token in ("high", "rising", "confident", "overconfident")
        ):
            return True
        if any(
            token in band_token
            for token in ("low", "falling", "uncertain", "cautious", "very_low")
        ):
            return False
        return None
    return band in (ConfidenceBand.HIGH, ConfidenceBand.VERY_HIGH)


def _is_low_confidence(evidence: StrategyEvidenceInput) -> bool | None:
    score = evidence.reported_confidence
    if score is not None:
        band = confidence_band_from_score(score)
        return band in (ConfidenceBand.LOW, ConfidenceBand.VERY_LOW)
    band_token = (evidence.twin_confidence_band or "").strip().lower()
    if not band_token:
        return None
    try:
        band = resolve_confidence_band(band_token)
    except ValueError:
        if any(
            token in band_token
            for token in ("low", "falling", "uncertain", "cautious", "very_low")
        ):
            return True
        if any(
            token in band_token
            for token in ("high", "rising", "confident", "overconfident")
        ):
            return False
        return None
    return band in (ConfidenceBand.LOW, ConfidenceBand.VERY_LOW)
