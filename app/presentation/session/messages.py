"""Central flash copy for Learning Session Experience UI.

Presentation messaging only — no educational authority.
Aligned with knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md.
"""

from __future__ import annotations

FLASH_SUCCESS = {
    "resumed": "Welcome back — continuing where you left off.",
    "begun": "Session started. Stay focused — one activity at a time.",
    "completed": "Session complete. Your home view is ready with today's updates.",
}

FLASH_WARNING = {
    "missing": (
        "That session could not be found. "
        "Return home and start today's session again."
    ),
    "begin_invalid": "We couldn't start this session. Please try again.",
    "begin_unavailable": (
        "This session is temporarily unavailable. Please try again shortly."
    ),
    "begin_failed": (
        "We couldn't start this session. Please try again from the overview."
    ),
    "answer_required": "Please enter an answer before continuing.",
    "activity_unavailable": (
        "This activity is temporarily unavailable. Please try again shortly."
    ),
    "answer_failed": (
        "We couldn't submit your answer. Check your response and try again."
    ),
    "continue_invalid": "We couldn't continue. Please try again.",
    "continue_failed": (
        "We couldn't continue. Please try again from this activity."
    ),
    "reflection_unavailable": (
        "Reflection is temporarily unavailable. Please try again shortly."
    ),
    "reflection_failed": (
        "We couldn't continue from reflection. Please try again."
    ),
    "complete_invalid": (
        "We couldn't complete this session. Please try again."
    ),
    "complete_unavailable": (
        "Session completion is temporarily unavailable. Please try again shortly."
    ),
    "complete_failed": (
        "We couldn't complete this session. Please try again from this page."
    ),
}
