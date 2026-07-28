"""Deterministic learning-state derivation (EI-006)."""

from __future__ import annotations

from app.domain.learning_evidence.evidence_event import EvidenceEvent
from app.domain.learning_evidence.evidence_type import EvidenceType
from app.domain.twin_inference.learning_state import LearningState


def derive_learning_state(
    *,
    mastery: float,
    confidence: float,
    evidence: tuple[EvidenceEvent, ...],
) -> tuple[str, str]:
    """Return ``(learning_state, reason)`` using fixed precedence.

    Precedence (first match wins):
    1. unknown — no evidence
    2. struggling — repeated failures with low mastery
    3. revising — recent revision with mid/high mastery
    4. mastered — high mastery and confidence
    5. consolidating / developing / exploring by mastery bands
    """
    if not evidence:
        return (
            LearningState.UNKNOWN.value,
            "No usable evidence; learning state is unknown",
        )

    practice = [
        e
        for e in evidence
        if e.evidence_type == EvidenceType.PRACTICE_ATTEMPT.value
    ]
    failed_practice = sum(1 for e in practice if e.metadata.get("correct") is False)
    failed_assessments = sum(
        1
        for e in evidence
        if e.evidence_type == EvidenceType.ASSESSMENT_RESULT.value
        and e.metadata.get("passed") is False
    )
    if (
        mastery < 0.40
        and len(practice) + failed_assessments >= 3
        and (failed_practice + failed_assessments) >= 2
    ):
        return (
            LearningState.STRUGGLING.value,
            (
                f"Repeated unsuccessful attempts "
                f"(failed_practice={failed_practice}, "
                f"failed_assessments={failed_assessments}) "
                f"with mastery {mastery:.4f}"
            ),
        )

    has_revision = any(
        e.evidence_type == EvidenceType.REVISION_SESSION.value for e in evidence
    )
    if has_revision and mastery >= 0.40:
        return (
            LearningState.REVISING.value,
            f"Revision evidence present with mastery {mastery:.4f}",
        )

    if mastery >= 0.75 and confidence >= 0.50:
        return (
            LearningState.MASTERED.value,
            f"Mastery {mastery:.4f} and confidence {confidence:.4f} "
            "meet mastered thresholds",
        )
    if mastery >= 0.50:
        return (
            LearningState.CONSOLIDATING.value,
            f"Mastery {mastery:.4f} in consolidating band [0.50, 0.75)",
        )
    if mastery >= 0.20:
        return (
            LearningState.DEVELOPING.value,
            f"Mastery {mastery:.4f} in developing band [0.20, 0.50)",
        )
    return (
        LearningState.EXPLORING.value,
        f"Mastery {mastery:.4f} in exploring band [0.00, 0.20)",
    )
