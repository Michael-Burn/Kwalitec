"""Approved activity catalogue for Twin→Mission planning (AP-002D5).

Planning maps Twin decisions onto existing activity kinds only.
No new educational heuristics — activity selection reuses Adaptive Mission
construction semantics (practice / recovery / review / reflection).
"""

from __future__ import annotations

from enum import StrEnum


class PlanningActivityType(StrEnum):
    """Activity kinds the Mission Engine may schedule from Twin decisions."""

    PRACTICE = "practice"
    RECOVERY = "recovery"
    REVIEW = "review"
    REFLECTION = "reflection"
    CONFIDENCE_PRACTICE = "confidence_practice"


KNOWN_PLANNING_ACTIVITY_TYPES: frozenset[str] = frozenset(
    t.value for t in PlanningActivityType
)


def parse_planning_activity_type(
    value: PlanningActivityType | str,
) -> PlanningActivityType:
    """Parse activity type; fail closed on unknown values."""
    if isinstance(value, PlanningActivityType):
        return value
    text = str(value or "").strip()
    try:
        return PlanningActivityType(text)
    except ValueError as exc:
        from app.domain.mission.planning.errors import PlanningRejected

        raise PlanningRejected(f"unknown planning activity type: {text!r}") from exc
