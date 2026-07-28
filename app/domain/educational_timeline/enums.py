"""Educational Timeline enumerations (ILE-003).

Sections interpret Decision Journal educational memory. Labels are
learner-facing product vocabulary — never Twin, ranking, or analytics jargon.
"""

from __future__ import annotations

from enum import StrEnum


class TimelineSectionKind(StrEnum):
    """Narrative sections derived from journal evidence."""

    LEARNING_JOURNEY = "learning_journey"
    TURNING_POINTS = "turning_points"
    RECOVERIES = "recoveries"
    PERIODS_OF_CONSISTENCY = "periods_of_consistency"
    PERIODS_OF_UNCERTAINTY = "periods_of_uncertainty"
    MISSION_MILESTONES = "mission_milestones"
    REFLECTION_HIGHLIGHTS = "reflection_highlights"
    DECISION_MILESTONES = "decision_milestones"
    LEARNING_MOMENTUM = "learning_momentum"


class NarrativeCertainty(StrEnum):
    """How strongly the narrative may speak given available evidence."""

    INSUFFICIENT = "insufficient"
    SUGGESTIVE = "suggestive"
    SUPPORTED = "supported"


SECTION_LABELS: dict[TimelineSectionKind, str] = {
    TimelineSectionKind.LEARNING_JOURNEY: "Learning Journey",
    TimelineSectionKind.TURNING_POINTS: "Turning Points",
    TimelineSectionKind.RECOVERIES: "Recoveries",
    TimelineSectionKind.PERIODS_OF_CONSISTENCY: "Periods of Consistency",
    TimelineSectionKind.PERIODS_OF_UNCERTAINTY: "Periods of Uncertainty",
    TimelineSectionKind.MISSION_MILESTONES: "Mission Milestones",
    TimelineSectionKind.REFLECTION_HIGHLIGHTS: "Reflection Highlights",
    TimelineSectionKind.DECISION_MILESTONES: "Decision Milestones",
    TimelineSectionKind.LEARNING_MOMENTUM: "Learning Momentum",
}

SECTION_INTROS: dict[TimelineSectionKind, str] = {
    TimelineSectionKind.LEARNING_JOURNEY: (
        "A chronological reading of the guidance you have received and "
        "the choices you have made."
    ),
    TimelineSectionKind.TURNING_POINTS: (
        "Moments that appear to mark a change in how your learning unfolded."
    ),
    TimelineSectionKind.RECOVERIES: (
        "Times when study guidance suggested rebuilding after a difficult stretch."
    ),
    TimelineSectionKind.PERIODS_OF_CONSISTENCY: (
        "Stretches where accepted guidance appears steadily over time."
    ),
    TimelineSectionKind.PERIODS_OF_UNCERTAINTY: (
        "Periods where evidence was thin or confidence remained limited."
    ),
    TimelineSectionKind.MISSION_MILESTONES: (
        "Mission-related guidance that reached a clear stage in your journal."
    ),
    TimelineSectionKind.REFLECTION_HIGHLIGHTS: (
        "Entries where you closed the loop with reflection."
    ),
    TimelineSectionKind.DECISION_MILESTONES: (
        "Significant choices and what followed, as recorded in your journal."
    ),
    TimelineSectionKind.LEARNING_MOMENTUM: (
        "A cautious reading of recent study rhythm compared with earlier entries."
    ),
}
