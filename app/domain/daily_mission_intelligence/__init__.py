"""Daily Mission Intelligence domain (ILE-004).

Composes one primary daily educational mission from authorised
Recommendation / MES evidence. Never re-decides; never invents ranking;
never duplicates Twin, Decision Engine, or Recommendation Engine authority.
"""

from __future__ import annotations

from app.domain.daily_mission_intelligence.compose import (
    DailyMissionBrief,
    DailyMissionEvidenceInput,
    compose_daily_mission,
    empty_mission_brief,
)
from app.domain.daily_mission_intelligence.enums import (
    AXIS_LABELS,
    FORBIDDEN_OPTIMISATION_TERMS,
    MissionLifecyclePhase,
    MissionOptimisationAxis,
)
from app.domain.daily_mission_intelligence.invariants import (
    FORBIDDEN_STUDENT_TERMS,
    assert_mission_speech_safe,
    assert_student_safe_text,
)

__all__ = [
    "AXIS_LABELS",
    "FORBIDDEN_OPTIMISATION_TERMS",
    "FORBIDDEN_STUDENT_TERMS",
    "DailyMissionBrief",
    "DailyMissionEvidenceInput",
    "MissionLifecyclePhase",
    "MissionOptimisationAxis",
    "assert_mission_speech_safe",
    "assert_student_safe_text",
    "compose_daily_mission",
    "empty_mission_brief",
]
