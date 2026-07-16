"""Contributor Recognition Service — RIP-002.

Awards and surfaces research journey badges for Internal Alpha participants.
Celebrates consistency and constructive participation — never volume, competition,
or leaderboards. Never reads or writes educational state.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import UTC, datetime

from app.extensions import db
from app.models.research_feedback import (
    ResearchContribution,
    ResearchContributorBadge,
    ResearchFeedbackReview,
    ResearchFeedbackSubmission,
)

logger = logging.getLogger(__name__)

BADGE_EXPLORER = "explorer"
BADGE_RESEARCH_PARTNER = "research_partner"
BADGE_CORE_CONTRIBUTOR = "core_contributor"
BADGE_PRODUCT_SHAPER = "product_shaper"
BADGE_FOUNDERS_CIRCLE = "founders_circle"

BADGE_LABELS: dict[str, str] = {
    BADGE_EXPLORER: "Explorer",
    BADGE_RESEARCH_PARTNER: "Research Partner",
    BADGE_CORE_CONTRIBUTOR: "Core Contributor",
    BADGE_PRODUCT_SHAPER: "Product Shaper",
    BADGE_FOUNDERS_CIRCLE: "Founder's Circle",
}

BADGE_HIERARCHY: tuple[str, ...] = (
    BADGE_EXPLORER,
    BADGE_RESEARCH_PARTNER,
    BADGE_CORE_CONTRIBUTOR,
    BADGE_PRODUCT_SHAPER,
    BADGE_FOUNDERS_CIRCLE,
)

AUTOMATIC_THRESHOLDS: dict[str, int] = {
    BADGE_EXPLORER: 1,
    BADGE_RESEARCH_PARTNER: 10,
    BADGE_CORE_CONTRIBUTOR: 25,
}

MANUAL_BADGES: frozenset[str] = frozenset(
    {BADGE_PRODUCT_SHAPER, BADGE_FOUNDERS_CIRCLE}
)


@dataclass(frozen=True)
class BadgeInfo:
    """Display metadata for one contributor badge."""

    slug: str
    label: str


@dataclass(frozen=True)
class ContributorJourney:
    """Student-facing research journey summary (no rankings)."""

    contribution_count: int
    current_badge: BadgeInfo | None
    next_badge: BadgeInfo | None
    progress_current: int
    progress_target: int | None
    progress_label: str
    appreciation_message: str


@dataclass(frozen=True)
class FounderReviewResult:
    """Result of a Founder review on one feedback submission."""

    review: ResearchFeedbackReview
    newly_earned_badges: tuple[str, ...]


class ContributorRecognitionService:
    """Recognition for meaningful product research contribution (RIP-002)."""

    @staticmethod
    def contribution_count(user_id: int) -> int:
        """Return how many Product Check-ins the student has completed."""
        return ResearchContribution.query.filter_by(user_id=user_id).count()

    @staticmethod
    def _badge_info(slug: str) -> BadgeInfo:
        return BadgeInfo(slug=slug, label=BADGE_LABELS[slug])

    @staticmethod
    def _user_badge_slugs(user_id: int) -> set[str]:
        rows = ResearchContributorBadge.query.filter_by(user_id=user_id).all()
        return {row.badge_slug for row in rows}

    @staticmethod
    def _highest_badge(slugs: set[str]) -> str | None:
        highest: str | None = None
        for slug in BADGE_HIERARCHY:
            if slug in slugs:
                highest = slug
        return highest

    @staticmethod
    def _next_automatic_badge(count: int) -> tuple[str | None, int, int | None]:
        """Return next automatic badge slug and progress toward it."""
        if count < AUTOMATIC_THRESHOLDS[BADGE_EXPLORER]:
            return BADGE_EXPLORER, count, AUTOMATIC_THRESHOLDS[BADGE_EXPLORER]
        if count < AUTOMATIC_THRESHOLDS[BADGE_RESEARCH_PARTNER]:
            return (
                BADGE_RESEARCH_PARTNER,
                count,
                AUTOMATIC_THRESHOLDS[BADGE_RESEARCH_PARTNER],
            )
        if count < AUTOMATIC_THRESHOLDS[BADGE_CORE_CONTRIBUTOR]:
            return (
                BADGE_CORE_CONTRIBUTOR,
                count,
                AUTOMATIC_THRESHOLDS[BADGE_CORE_CONTRIBUTOR],
            )
        return None, count, None

    @staticmethod
    def _appreciation_message(
        *,
        count: int,
        current_slug: str | None,
        next_slug: str | None,
    ) -> str:
        if count == 0:
            return (
                "Your first Product Check-in begins your research journey with us."
            )
        if current_slug == BADGE_FOUNDERS_CIRCLE:
            return "Thank you for helping shape Kwalitec from the inside."
        if current_slug == BADGE_PRODUCT_SHAPER:
            return "Your feedback has directly influenced a shipped improvement."
        if next_slug == BADGE_PRODUCT_SHAPER:
            return (
                "Thank you for your steady, thoughtful contributions to Kwalitec."
            )
        if next_slug in AUTOMATIC_THRESHOLDS:
            return "Thank you for helping us improve Kwalitec, one check-in at a time."
        return "Thank you for being part of the Internal Alpha research community."

    @staticmethod
    def get_journey_summary(user_id: int) -> ContributorJourney:
        """Build the student profile / thank-you journey summary."""
        count = ContributorRecognitionService.contribution_count(user_id)
        earned = ContributorRecognitionService._user_badge_slugs(user_id)
        current_slug = ContributorRecognitionService._highest_badge(earned)

        next_slug: str | None
        progress_current: int
        progress_target: int | None
        progress_label: str

        if current_slug == BADGE_FOUNDERS_CIRCLE:
            next_slug = None
            progress_current = count
            progress_target = None
            progress_label = "Highest recognition"
        elif current_slug == BADGE_PRODUCT_SHAPER:
            next_slug = BADGE_FOUNDERS_CIRCLE
            progress_current = count
            progress_target = None
            progress_label = "Invitation only"
        elif current_slug == BADGE_CORE_CONTRIBUTOR:
            next_slug = BADGE_PRODUCT_SHAPER
            progress_current = count
            progress_target = None
            progress_label = "Awarded when feedback shapes a release"
        else:
            auto_next, progress_current, progress_target = (
                ContributorRecognitionService._next_automatic_badge(count)
            )
            next_slug = auto_next
            if progress_target is not None:
                progress_label = (
                    f"{progress_current} of {progress_target} check-ins"
                )
            else:
                progress_label = "Keep contributing thoughtfully"

        current_badge = (
            ContributorRecognitionService._badge_info(current_slug)
            if current_slug
            else None
        )
        next_badge = (
            ContributorRecognitionService._badge_info(next_slug)
            if next_slug
            else None
        )

        return ContributorJourney(
            contribution_count=count,
            current_badge=current_badge,
            next_badge=next_badge,
            progress_current=progress_current,
            progress_target=progress_target,
            progress_label=progress_label,
            appreciation_message=ContributorRecognitionService._appreciation_message(
                count=count,
                current_slug=current_slug,
                next_slug=next_slug,
            ),
        )

    @staticmethod
    def _award_badge(
        user_id: int,
        badge_slug: str,
        *,
        trigger_contribution_id: int | None = None,
        trigger_submission_id: int | None = None,
        awarded_by_user_id: int | None = None,
        awarded_at: datetime | None = None,
    ) -> ResearchContributorBadge | None:
        """Award a badge if the student does not already hold it."""
        if badge_slug not in BADGE_LABELS:
            raise ValueError(f"Unknown badge_slug: {badge_slug}")

        existing = ResearchContributorBadge.query.filter_by(
            user_id=user_id,
            badge_slug=badge_slug,
        ).first()
        if existing is not None:
            return None

        when = awarded_at or datetime.now(UTC).replace(tzinfo=None)
        badge = ResearchContributorBadge(
            user_id=user_id,
            badge_slug=badge_slug,
            awarded_at=when,
            trigger_contribution_id=trigger_contribution_id,
            trigger_submission_id=trigger_submission_id,
            awarded_by_user_id=awarded_by_user_id,
        )
        db.session.add(badge)
        db.session.flush()
        logger.info(
            "RIP-002 badge awarded user=%s badge=%s founder=%s",
            user_id,
            badge_slug,
            awarded_by_user_id,
        )
        return badge

    @staticmethod
    def evaluate_automatic_badges(
        user_id: int,
        *,
        latest_contribution_id: int | None = None,
    ) -> tuple[str, ...]:
        """Award automatic badges based on contribution count."""
        count = ContributorRecognitionService.contribution_count(user_id)
        earned: list[str] = []
        for slug, threshold in AUTOMATIC_THRESHOLDS.items():
            if count < threshold:
                continue
            badge = ContributorRecognitionService._award_badge(
                user_id,
                slug,
                trigger_contribution_id=latest_contribution_id,
            )
            if badge is not None:
                earned.append(slug)
        if earned:
            db.session.commit()
        return tuple(earned)

    @staticmethod
    def founder_review_submission(
        submission_id: int,
        founder_user_id: int,
        *,
        helpful: bool = False,
        insightful: bool = False,
        implemented: bool = False,
    ) -> FounderReviewResult:
        """Record Founder marks on feedback. Implemented may award Product Shaper.

        Args:
            submission_id: Target feedback submission.
            founder_user_id: Authenticated Founder user id.
            helpful: Founder marked feedback as helpful.
            insightful: Founder marked feedback as insightful.
            implemented: Founder marked feedback as implemented in a release.

        Returns:
            FounderReviewResult with review row and any new badges.

        Raises:
            ValueError: When submission does not exist.
        """
        submission = db.session.get(ResearchFeedbackSubmission, submission_id)
        if submission is None:
            raise ValueError(f"Submission not found: {submission_id}")

        review = ResearchFeedbackReview.query.filter_by(
            submission_id=submission_id
        ).first()
        when = datetime.now(UTC).replace(tzinfo=None)
        if review is None:
            review = ResearchFeedbackReview(
                submission_id=submission_id,
                founder_user_id=founder_user_id,
                is_helpful=helpful,
                is_insightful=insightful,
                is_implemented=implemented,
                reviewed_at=when,
            )
            db.session.add(review)
        else:
            review.founder_user_id = founder_user_id
            review.is_helpful = helpful
            review.is_insightful = insightful
            review.is_implemented = implemented
            review.reviewed_at = when

        newly_earned: list[str] = []
        if implemented:
            badge = ContributorRecognitionService._award_badge(
                submission.user_id,
                BADGE_PRODUCT_SHAPER,
                trigger_submission_id=submission_id,
                awarded_by_user_id=founder_user_id,
                awarded_at=when,
            )
            if badge is not None:
                newly_earned.append(BADGE_PRODUCT_SHAPER)

        db.session.commit()
        return FounderReviewResult(
            review=review,
            newly_earned_badges=tuple(newly_earned),
        )

    @staticmethod
    def award_founders_circle(
        user_id: int,
        founder_user_id: int,
    ) -> ResearchContributorBadge | None:
        """Invitation-only Founder's Circle award (Founder manual)."""
        badge = ContributorRecognitionService._award_badge(
            user_id,
            BADGE_FOUNDERS_CIRCLE,
            awarded_by_user_id=founder_user_id,
        )
        if badge is not None:
            db.session.commit()
        return badge
