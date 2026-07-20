"""Mission generation enumerations.

Vocabulary for MissionSpecification projections derived from the Educational
Operating System. Bands are instructional estimates — not mastery claims.
"""

from __future__ import annotations

from enum import StrEnum


class MissionDurationBand(StrEnum):
    """Estimated sitting duration band for a generated mission.

    Aligns with Learning Episode Types illustrative bands:
    short 5–15, medium 15–35, long 35–60 minutes.
    """

    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"


class MissionPriorityBand(StrEnum):
    """Instructional-ordering band projected onto a mission.

    Mapped from Educational Priority score bands. Distinct from diagnosis
    severity and from teaching-strategy selection.
    """

    NEGLIGIBLE = "negligible"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CompletionConditionCode(StrEnum):
    """Deterministic completion-condition catalogue codes."""

    ALL_TASKS_COMPLETED = "all_tasks_completed"
    PRIMARY_STRATEGY_ENGAGED = "primary_strategy_engaged"
    SUCCESS_CRITERIA_MET = "success_criteria_met"
    EVIDENCE_CAPTURED = "evidence_captured"
