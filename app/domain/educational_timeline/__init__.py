"""Educational Timeline domain (ILE-003).

Interprets Decision Journal educational memory into a reflective
chronological narrative. Stores nothing; invents no second brain.
"""

from __future__ import annotations

from app.domain.educational_timeline.enums import (
    SECTION_INTROS,
    SECTION_LABELS,
    NarrativeCertainty,
    TimelineSectionKind,
)
from app.domain.educational_timeline.invariants import (
    FORBIDDEN_STUDENT_TERMS,
    OVERCLAIM_PHRASES,
    assert_narrative_humble,
    assert_student_safe_text,
)
from app.domain.educational_timeline.narrative import (
    EducationalNarrative,
    NarrativeMoment,
    TimelineSection,
    build_educational_narrative,
)

__all__ = [
    "SECTION_INTROS",
    "SECTION_LABELS",
    "NarrativeCertainty",
    "TimelineSectionKind",
    "FORBIDDEN_STUDENT_TERMS",
    "OVERCLAIM_PHRASES",
    "assert_narrative_humble",
    "assert_student_safe_text",
    "EducationalNarrative",
    "NarrativeMoment",
    "TimelineSection",
    "build_educational_narrative",
]
