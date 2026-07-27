"""Centralized flash copy for Assessment Delivery (UX_PRINCIPLES.md)."""

from __future__ import annotations

FLASH_SUCCESS = {
    "started": "Your learning check is ready — take your time.",
    "begun": "Let's begin. Your answers help keep today's support accurate.",
    "saved": "Progress saved.",
    "paused": "Paused. Your progress is saved.",
    "resumed": "Welcome back — picking up where you left off.",
    "completed": "Check complete. Thanks — that helps Kwalitec support you.",
    "cancelled": "Check closed. You can start another whenever you're ready.",
    "hint": "Hint revealed — using a hint is allowed.",
}

FLASH_WARNING = {
    "missing": "We couldn't find that learning check.",
    "invalid": "Please check your answer and try again.",
    "state": "That step isn't available right now.",
    "expired": "This learning check has ended. Start a fresh one when ready.",
    "ownership": "You don't have access to that learning check.",
    "duplicate": "You've already answered this one.",
}
