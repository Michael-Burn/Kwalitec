"""Study environment tips — coaching presentation only.

Rotating tips help students prepare for an effective session. This module
must never influence Educational Intelligence, Twin, Decision, Recommendation,
Mission composition, or readiness scoring.
"""

from __future__ import annotations

from datetime import date

# Ordered tips rotate by calendar day. Content is educational coaching only.
_STUDY_TIPS: tuple[str, ...] = (
    "Find a quiet environment before you begin.",
    "Turn off notifications for the length of this session.",
    "Aim for adequate sleep — tired study rarely sticks.",
    "Keep water nearby and take regular breaks on long sessions.",
    "Practice questions improve retention more than re-reading alone.",
    "Clear your desk of unrelated tabs and materials.",
    "Decide your stop time before you start, then honour it.",
    "Start with one clear topic — avoid multitasking.",
    "If focus slips, stand up for two minutes, then return.",
)


class StudyTipsService:
    """Provide a deterministic daily study tip for presentation surfaces."""

    @staticmethod
    def tip_for_day(on_date: date | None = None) -> str:
        """Return the study tip for *on_date* (defaults to today).

        Rotation is date-stable so the same tip appears all day for a learner,
        without personalisation or Educational Intelligence inputs.
        """
        day = on_date or date.today()
        return _STUDY_TIPS[day.toordinal() % len(_STUDY_TIPS)]

    @staticmethod
    def all_tips() -> tuple[str, ...]:
        """Return the full tip catalogue (tests / Internal Alpha preview)."""
        return _STUDY_TIPS
