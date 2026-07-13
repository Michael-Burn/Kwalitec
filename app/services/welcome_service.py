"""First-time welcome modal — presentation preference only.

Marks eligibility after Study Plan + Calibration and records dismissal.
Never influences Educational Intelligence, Twin beliefs, or recommendations.
"""

from __future__ import annotations

from app.extensions import db
from app.models.user import User


class WelcomeService:
    """Persist welcome-modal eligibility and dismissal for a user."""

    @staticmethod
    def mark_eligible(user_id: int) -> None:
        """Enable the welcome modal after first successful setup."""
        user = db.session.get(User, user_id)
        if user is None:
            return
        if user.welcome_dismissed:
            return
        user.welcome_eligible = True
        db.session.commit()

    @staticmethod
    def should_show(user: User) -> bool:
        """Return True when the welcome modal should appear."""
        return bool(user.welcome_eligible) and not bool(user.welcome_dismissed)

    @staticmethod
    def dismiss(user_id: int) -> bool:
        """Dismiss permanently. Returns True when the user existed."""
        user = db.session.get(User, user_id)
        if user is None:
            return False
        user.welcome_dismissed = True
        user.welcome_eligible = False
        db.session.commit()
        return True
