"""Session-instance provenance: why this sitting exists.

Belongs to the session instance, not the topic. Study owns entry
eligibility; the Decision Engine owns today's recommendation. These
registers must stay separate.
"""

from __future__ import annotations

SESSION_ORIGIN_STUDENT_SELECTED = "student_selected"
SESSION_ORIGIN_DAILY_MISSION = "daily_mission"

STUDENT_SELECTED_WHY = "You chose to study this."
UNREACHED_TOPIC_COPY = (
    "Available once you reach it in your learning path."
)


def why_studying_for_origin(origin: str, *, topic_title: str = "") -> str:
    """Honest, plain why-copy for Session Overview.

    Sequential / daily sittings keep the existing register. Student-selected
    sittings use a third register that does not claim a recommendation.
    """
    if (origin or "").strip() == SESSION_ORIGIN_STUDENT_SELECTED:
        return STUDENT_SELECTED_WHY
    topic = (topic_title or "").strip()
    if topic:
        return f"Today's Mission focuses on {topic}."
    return "This Session is today's recommended next step."


def is_student_selected_origin(origin: str) -> bool:
    return (origin or "").strip() == SESSION_ORIGIN_STUDENT_SELECTED
