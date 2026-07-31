"""Central flash copy for Learning Session Experience UI.

Presentation messaging only — no educational authority.
Aligned with knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md.
"""

from __future__ import annotations

FLASH_SUCCESS = {
    "resumed": "Welcome back — continuing where you left off.",
    "begun": "Session started. Stay focused — one activity at a time.",
    "paused": "Session paused. You can resume from Home whenever you're ready.",
    "activities_complete": (
        "Activities complete — a short reflection closes today's practice."
    ),
    "ready_to_finish": (
        "Ready to finish — tell us honestly how today's planned study went."
    ),
    "completed": (
        "Session complete. Your Journey and Home are ready with today's next step."
    ),
    "checklist_updated": "Plan checklist updated.",
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
    "pause_failed": "We couldn't pause this session. Please try again.",
    "resume_failed": "We couldn't resume this session. Please try again.",
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
    "finish_review_required": (
        "Please choose Yes, Partially, or No before finishing. Try again."
    ),
    "evidence_rejected": (
        "We need a bit more practice before counting this topic complete. "
        "Continue with practice, or choose Partially / No if today's planned "
        "study did not fully happen. Try again when you're ready."
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
