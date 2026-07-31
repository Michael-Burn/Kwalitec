"""Educational Memory — persistence of educational intelligence (KWP-011).

Stores Strategy / Diagnostics / Difficulty / Effectiveness outcomes onto
Evidence Packages so sittings become a continuous learning narrative.

This is a persistence and projection layer — not a reasoning engine.
Reasoning remains inside Strategy, Diagnostics, Difficulty, and Effectiveness.
"""

from __future__ import annotations

from app.application.educational_memory.dto import (
    IntelligenceSnapshot,
    LearningJourneyNarrative,
    LearningMilestone,
    LongitudinalPattern,
    TimelineEntry,
)
from app.application.educational_memory.service import (
    EducationalMemoryService,
    get_educational_memory_service,
)

__all__ = [
    "EducationalMemoryService",
    "IntelligenceSnapshot",
    "LearningJourneyNarrative",
    "LearningMilestone",
    "LongitudinalPattern",
    "TimelineEntry",
    "get_educational_memory_service",
]
