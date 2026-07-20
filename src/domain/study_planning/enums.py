"""Study planning enumerations.

Vocabulary for deterministic StudyPlan projections. Session kinds and review
offsets are instructional scheduling signals — not mastery claims.
"""

from __future__ import annotations

from enum import StrEnum


class SessionKind(StrEnum):
    """Kind of scheduled study sitting within a StudyPlan."""

    WORK = "work"
    REVIEW = "review"
    RECOVERY = "recovery"


class PlanningHorizonBand(StrEnum):
    """Illustrative horizon of a generated study plan in relative days."""

    COMPACT = "compact"  # ≤ 3 planning days with sessions
    STANDARD = "standard"  # 4–7 days
    EXTENDED = "extended"  # > 7 days
