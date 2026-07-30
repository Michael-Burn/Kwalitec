"""Evidence grading for Curriculum Intelligence educational decisions (EI-001C).

Every educational decision carries its highest supporting Evidence Grade.
Grades are ordered A (strongest official authority) → D (weakest heuristic).
"""

from __future__ import annotations

from enum import StrEnum


class EvidenceGrade(StrEnum):
    """Highest supporting evidence quality for an educational decision."""

    A = "A"  # Official syllabus / official learning objectives
    B = "B"  # CMP headings / definitions / worked examples
    C = "C"  # Paragraph inference / examples
    D = "D"  # Heuristic inference / AI-supported reasoning (presentation only)


# Numeric weights for QualitySnapshot.evidence_quality (A strongest).
EVIDENCE_GRADE_WEIGHT: dict[EvidenceGrade, float] = {
    EvidenceGrade.A: 1.0,
    EvidenceGrade.B: 0.75,
    EvidenceGrade.C: 0.5,
    EvidenceGrade.D: 0.25,
}


def evidence_grade_weight(grade: EvidenceGrade | str | None) -> float:
    """Map an evidence grade to its quality weight (0 when missing)."""
    if grade is None:
        return 0.0
    try:
        return EVIDENCE_GRADE_WEIGHT[EvidenceGrade(grade)]
    except ValueError:
        return 0.0


def best_evidence_grade(
    *grades: EvidenceGrade | str | None,
) -> EvidenceGrade | None:
    """Return the strongest (highest weight) grade among candidates."""
    present = [EvidenceGrade(g) for g in grades if g is not None]
    if not present:
        return None
    return max(present, key=lambda g: EVIDENCE_GRADE_WEIGHT[g])
