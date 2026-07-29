"""Lightweight Internal Alpha product onboarding — ALPHA-001.

Explains what Kwalitec is, introduces Study Sensei (mandatory handoff),
how Missions and Sessions differ, why recommendations are explainable,
and how reflection works. Presentation preference only — never influences
Twin, readiness, or recommendations.

RR-001.3A / EGC-R01 / EGC-R02 — educational identity + lexicon application.
RR-001.3B / EGC-R03 / EGC-R04 — reflection family orientation.
RR-001.3C / EGC-R06 / EGC-R12 — educational memory coherence.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.extensions import db
from app.models.user import User

# Kept for Help / orientation surfaces that still introduce Study Sensei.
SENSEI_HANDOFF_SENTENCE = (
    "Study Sensei is how Kwalitec guides your daily learning decisions."
)

ONBOARDING_STEPS: tuple[dict[str, str], ...] = (
    {
        "id": "what",
        "title": "What Kwalitec is",
        "body": (
            "Kwalitec helps you prepare for demanding exams with a clear "
            "Study Plan, focused daily study, and progress you can trust — "
            "built from verified curriculum and your recorded practice."
        ),
    },
    {
        "id": "choose",
        "title": "Choose your exam",
        "body": (
            "Pick a Ready subject from the Subject Catalogue, enter your exam "
            "date and study availability, then begin learning. Coming Soon "
            "subjects are under preparation and cannot be selected yet."
        ),
    },
    {
        "id": "focus",
        "title": "Today's Focus",
        "body": (
            "Each day, Home shows Today's Focus — what to study now and why. "
            "Start today's Session to practice, then see what changed and "
            "what comes next."
        ),
    },
    {
        "id": "explainable",
        "title": "Guidance you can understand",
        "body": (
            "Recommendations come from your syllabus structure, available time, "
            "and study history — not a black box. When you expand “why”, you "
            "see the reasons behind the guidance."
        ),
    },
)


@dataclass(frozen=True)
class AlphaOnboardingState:
    """Whether the student should see alpha onboarding."""

    should_show: bool
    completed: bool
    skipped: bool


class AlphaOnboardingService:
    """Track one-time Internal Alpha product onboarding completion."""

    @staticmethod
    def state_for(user: User) -> AlphaOnboardingState:
        """Return onboarding visibility state for *user*."""
        completed = bool(getattr(user, "alpha_onboarding_completed", False))
        skipped = bool(getattr(user, "alpha_onboarding_skipped", False))
        return AlphaOnboardingState(
            should_show=not completed and not skipped,
            completed=completed,
            skipped=skipped,
        )

    @staticmethod
    def should_show(user: User) -> bool:
        """Return True when onboarding should be offered."""
        return AlphaOnboardingService.state_for(user).should_show

    @staticmethod
    def complete(user_id: int) -> bool:
        """Mark onboarding completed. Returns False if user missing."""
        user = db.session.get(User, user_id)
        if user is None:
            return False
        user.alpha_onboarding_completed = True
        user.alpha_onboarding_skipped = False
        db.session.commit()
        return True

    @staticmethod
    def skip(user_id: int) -> bool:
        """Skip onboarding without blocking later revisit via Help."""
        user = db.session.get(User, user_id)
        if user is None:
            return False
        user.alpha_onboarding_skipped = True
        db.session.commit()
        return True

    @staticmethod
    def steps() -> tuple[dict[str, str], ...]:
        """Return the fixed onboarding step copy."""
        return ONBOARDING_STEPS
