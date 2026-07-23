"""Lightweight Internal Alpha product onboarding — ALPHA-001.

Explains what Kwalitec is, how missions work, why recommendations are
explainable, and how reflection works. Presentation preference only —
never influences Twin, readiness, or recommendations.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.extensions import db
from app.models.user import User

ONBOARDING_STEPS: tuple[dict[str, str], ...] = (
    {
        "id": "what",
        "title": "What Kwalitec is",
        "body": (
            "Kwalitec is an Education Operating System for demanding exams. "
            "It answers the daily question of what to study next — calmly, "
            "from your plan and your progress."
        ),
    },
    {
        "id": "missions",
        "title": "How missions work",
        "body": (
            "Each day Kwalitec prepares a focused study mission. Open today's "
            "session, study the topic, and record what you did. Missions keep "
            "study decisions small so learning can stay large."
        ),
    },
    {
        "id": "explainable",
        "title": "Why recommendations are explainable",
        "body": (
            "Recommendations come from your syllabus structure, available time, "
            "and study history — not a black box. When you expand “why”, you "
            "see the reasons Kwalitec used."
        ),
    },
    {
        "id": "reflection",
        "title": "How reflection works",
        "body": (
            "After a session, a short reflection closes the loop. It helps "
            "Kwalitec understand how the session felt and keeps tomorrow's "
            "guidance honest."
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
