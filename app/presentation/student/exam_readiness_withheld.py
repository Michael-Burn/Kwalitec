"""Student-facing Exam Readiness claim withhold (Phase 3 decision).

Semantic definition of Exam Readiness remains valid in
``knowledge/product/student_progress_semantics/SEMANTIC_CONTRACT.md``.
Live numerical claims are withheld until evidence architecture is reconciled.

This module is presentation/policy only. It does not change Twin internals,
Progression Readiness, Policy V1, numeric assessment, or arbitration.
"""

from __future__ import annotations

import re
from typing import Any

# Student-facing copy: must never read as "you are unprepared."
EXAM_READINESS_NOT_YET_ASSESSABLE = (
    "Not yet assessable: Kwalitec does not yet have enough reliable evidence "
    "for this estimate."
)

EXAM_READINESS_NOT_YET_ASSESSABLE_SHORT = "Not yet assessable"

EXAM_READINESS_WITHHELD_BASIS = (
    "Exam Readiness is defined, but the evidence architecture that would "
    "warrant a numerical estimate is still being reconciled. No live engine "
    "may show a confident Exam Readiness percentage until that work lands."
)


def exam_readiness_numeric_claims_withheld() -> bool:
    """True while learner-facing Exam Readiness percentages stay withheld."""
    return True


def student_facing_exam_readiness_claim(
    *args: Any,
    **kwargs: Any,
) -> str:
    """Return the only lawful student-facing Exam Readiness claim today.

    Accepts arbitrary evidence inputs (coverage, overall score, Twin score,
    calculate_readiness output, etc.) and ignores them. Coverage alone, or any
    Phase 3 competing engine, must never mint a confident-looking percentage
    through this path.
    """
    return EXAM_READINESS_NOT_YET_ASSESSABLE


def student_facing_exam_readiness_percentage(
    *args: Any,
    **kwargs: Any,
) -> None:
    """Student-facing Exam Readiness percentage is always withheld (None)."""
    return None


def assert_no_confident_exam_readiness_percent(text: str) -> None:
    """Raise AssertionError if ``text`` looks like a confident Exam Readiness %."""
    claim = (text or "").strip()
    if not claim:
        return
    lowered = claim.lower()
    if EXAM_READINESS_NOT_YET_ASSESSABLE_SHORT.lower() in lowered:
        return
    if "not yet assessable" in lowered:
        return
    if re.search(r"\b\d{1,3}\s*%", claim):
        raise AssertionError(
            f"Confident Exam Readiness percentage must not display: {claim!r}"
        )
