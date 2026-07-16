"""Research Feedback Service — RIP-001 Daily Reflection & Product Check-in.

Owns eligibility, persistence of structured product feedback, and
Contribution creation. Never reads or writes Educational Evidence, Twin
state, readiness, recommendations, or study algorithms.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import UTC, date, datetime

from app.extensions import db
from app.models.mission import Mission
from app.models.research_feedback import (
    ResearchContribution,
    ResearchFeedbackSubmission,
)
from app.models.study_plan import StudyPlan
from app.services.mission_service import MissionService
from app.services.study_plan_service import StudyPlanService
from app.version import APP_VERSION

logger = logging.getLogger(__name__)

PRODUCT_VERSION = APP_VERSION

SOURCE_STUDY_SESSION = "study_session"
SOURCE_SETTINGS = "settings"

EXPERIENCE_CHOICES = (
    "Excellent",
    "Good",
    "Okay",
    "Frustrating",
    "Poor",
)

FEATURE_CHOICES = (
    "Study Session",
    "Today's Study Session",
    "Dashboard",
    "Study Plan",
    "Recommendations",
    "Analytics",
    "Settings",
    "Other",
)

FRICTION_CHOICES = (
    "Nothing",
    "Navigation",
    "Terminology",
    "Study Plan",
    "Dashboard",
    "Recommendations",
    "Analytics",
    "Study Session",
    "Performance",
    "Other",
)

CONFIDENCE_CHOICES = (
    "Very Low",
    "Low",
    "Neutral",
    "High",
    "Very High",
)

RETURN_INTENT_CHOICES = (
    "Definitely",
    "Probably",
    "Not Sure",
    "Probably Not",
    "Definitely Not",
)

CLASSIFICATION_CHOICES = (
    "Bug",
    "Suggestion",
    "Praise",
    "Question",
    "Confusing",
    "Other",
)

# Generic bucket when free-text is present but the student skips classification.
DEFAULT_FREE_TEXT_CLASSIFICATION = "Other"

VALID_SOURCES = frozenset({SOURCE_STUDY_SESSION, SOURCE_SETTINGS})


@dataclass(frozen=True)
class CheckinEligibility:
    """Whether the student may see the post-study product check-in invitation."""

    eligible: bool
    reason: str
    mission: Mission | None = None
    study_plan: StudyPlan | None = None


@dataclass(frozen=True)
class CheckinSubmitResult:
    """Result of persisting a completed Product Check-in."""

    submission: ResearchFeedbackSubmission
    contribution: ResearchContribution
    newly_earned_badges: tuple[str, ...] = ()


class ResearchFeedbackService:
    """Service for product research check-ins (Research Intelligence only)."""

    @staticmethod
    def _eligibility_from_mission(
        mission: Mission,
        active_plan: StudyPlan | None,
    ) -> CheckinEligibility | None:
        """Return an eligible verdict when a mission shows study activity.

        A mission counts as study activity when it is Completed or has any
        task marked done. Returns ``None`` when the mission shows no activity
        so callers can continue with their fallback logic.
        """
        session_completed = mission.status == "Completed"
        partial_task_progress = any(t.completed for t in mission.tasks)
        if not (session_completed or partial_task_progress):
            return None

        plan = active_plan
        if mission.study_plan_id is not None and (
            plan is None or plan.id != mission.study_plan_id
        ):
            owned_plan = StudyPlan.query.filter_by(
                id=mission.study_plan_id, user_id=mission.user_id
            ).first()
            if owned_plan is not None:
                plan = owned_plan

        return CheckinEligibility(
            eligible=True,
            reason="session_completed" if session_completed else "mission_partial",
            mission=mission,
            study_plan=plan,
        )

    @staticmethod
    def is_eligible_for_invitation(
        user_id: int,
        *,
        on_date: date | None = None,
        mission_id: int | None = None,
    ) -> CheckinEligibility:
        """Return whether the post-study invitation should be offered.

        Eligible when today's Study Session has been completed, or at least
        part of today's mission has been completed (any task marked done, or
        mission status In Progress / Completed after study activity).

        When ``mission_id`` is supplied (the student arriving directly from a
        just-finished Study Session), an owned mission with study activity is
        honoured directly. This makes the post-session invitation deterministic
        even when today's date/active-plan lookup would resolve to a different
        mission (RR-001D — post-session check-in reliability).

        Args:
            user_id: Authenticated student id.
            on_date: Calendar day to evaluate (defaults to today).
            mission_id: Optional explicit mission the invitation came from.

        Returns:
            CheckinEligibility with mission/plan context when available.
        """
        day = on_date or date.today()
        active_plan = StudyPlanService.get_user_active_plan(user_id)

        # Trust the explicit mission the student just finished, when owned and
        # showing study activity — regardless of date/active-plan scoping.
        if mission_id is not None:
            referenced = Mission.query.filter_by(
                id=mission_id, user_id=user_id
            ).first()
            if referenced is not None:
                verdict = ResearchFeedbackService._eligibility_from_mission(
                    referenced, active_plan
                )
                if verdict is not None:
                    return verdict

        today_mission = MissionService.get_today_mission(
            user_id,
            mission_date=day,
            study_plan_id=active_plan.id if active_plan else None,
        )

        if today_mission is None:
            return CheckinEligibility(
                eligible=False,
                reason="no_mission_today",
                study_plan=active_plan,
            )

        verdict = ResearchFeedbackService._eligibility_from_mission(
            today_mission, active_plan
        )
        if verdict is not None:
            return verdict

        return CheckinEligibility(
            eligible=False,
            reason="no_study_activity",
            mission=today_mission,
            study_plan=active_plan,
        )

    @staticmethod
    def resolve_context(
        user_id: int,
        *,
        mission_id: int | None = None,
        study_plan_id: int | None = None,
    ) -> tuple[StudyPlan | None, Mission | None]:
        """Resolve study plan / mission context for a submission.

        Owns ownership checks. Does not mutate educational state.

        Args:
            user_id: Authenticated student id.
            mission_id: Optional mission to attach.
            study_plan_id: Optional study plan to attach.

        Returns:
            (study_plan, mission) owned by the user, or None when missing.
        """
        mission: Mission | None = None
        if mission_id is not None:
            mission = Mission.query.filter_by(id=mission_id, user_id=user_id).first()

        plan: StudyPlan | None = None
        if study_plan_id is not None:
            plan = StudyPlan.query.filter_by(
                id=study_plan_id, user_id=user_id
            ).first()
        elif mission is not None and mission.study_plan_id is not None:
            plan = StudyPlan.query.filter_by(
                id=mission.study_plan_id, user_id=user_id
            ).first()
        else:
            plan = StudyPlanService.get_user_active_plan(user_id)

        return plan, mission

    @staticmethod
    def submit_checkin(
        user_id: int,
        *,
        experience_rating: str,
        feature_helped_most: str,
        friction_area: str,
        confidence_rating: str,
        return_intent: str,
        submission_source: str,
        free_text: str | None = None,
        classification: str | None = None,
        study_plan_id: int | None = None,
        mission_id: int | None = None,
        product_version: str = PRODUCT_VERSION,
        submitted_at: datetime | None = None,
    ) -> CheckinSubmitResult:
        """Persist a completed Product Check-in and create one Contribution.

        Unlimited submissions are allowed. Free-text is optional; when
        present without an explicit classification, defaults to
        ``DEFAULT_FREE_TEXT_CLASSIFICATION`` (``Other``).

        Args:
            user_id: Authenticated student id.
            experience_rating: Q1 answer.
            feature_helped_most: Q2 answer.
            friction_area: Q3 answer.
            confidence_rating: Q4 answer.
            return_intent: Q5 answer.
            submission_source: ``study_session`` or ``settings``.
            free_text: Optional comment (max 300 chars).
            classification: Optional; when free-text is non-empty and this is
                omitted, defaults to ``Other``. Explicit values are preserved.
            study_plan_id: Optional study plan context.
            mission_id: Optional mission context.
            product_version: Product version string for RIP-003.
            submitted_at: Optional timestamp override (tests).

        Returns:
            CheckinSubmitResult with submission and contribution.

        Raises:
            ValueError: On invalid choices, source, or classification rules.
        """
        if submission_source not in VALID_SOURCES:
            raise ValueError(f"Invalid submission_source: {submission_source}")
        if experience_rating not in EXPERIENCE_CHOICES:
            raise ValueError(f"Invalid experience_rating: {experience_rating}")
        if feature_helped_most not in FEATURE_CHOICES:
            raise ValueError(f"Invalid feature_helped_most: {feature_helped_most}")
        if friction_area not in FRICTION_CHOICES:
            raise ValueError(f"Invalid friction_area: {friction_area}")
        if confidence_rating not in CONFIDENCE_CHOICES:
            raise ValueError(f"Invalid confidence_rating: {confidence_rating}")
        if return_intent not in RETURN_INTENT_CHOICES:
            raise ValueError(f"Invalid return_intent: {return_intent}")

        cleaned_text = (free_text or "").strip() or None
        if cleaned_text is not None and len(cleaned_text) > 300:
            raise ValueError("free_text must be at most 300 characters")

        cleaned_classification = (classification or "").strip() or None
        if cleaned_text is not None:
            if cleaned_classification is None:
                cleaned_classification = DEFAULT_FREE_TEXT_CLASSIFICATION
            elif cleaned_classification not in CLASSIFICATION_CHOICES:
                raise ValueError(
                    f"Invalid classification: {cleaned_classification}"
                )
        else:
            cleaned_classification = None

        plan, mission = ResearchFeedbackService.resolve_context(
            user_id,
            mission_id=mission_id,
            study_plan_id=study_plan_id,
        )

        when = submitted_at or datetime.now(UTC).replace(tzinfo=None)
        submission = ResearchFeedbackSubmission(
            user_id=user_id,
            submitted_at=when,
            product_version=product_version,
            study_plan_id=plan.id if plan else None,
            mission_id=mission.id if mission else None,
            experience_rating=experience_rating,
            feature_helped_most=feature_helped_most,
            friction_area=friction_area,
            confidence_rating=confidence_rating,
            return_intent=return_intent,
            free_text=cleaned_text,
            classification=cleaned_classification,
            submission_source=submission_source,
        )
        db.session.add(submission)
        db.session.flush()

        contribution = ResearchContribution(
            user_id=user_id,
            submission_id=submission.id,
            created_at=when,
        )
        db.session.add(contribution)
        db.session.commit()

        from app.services.contributor_recognition_service import (
            ContributorRecognitionService,
        )

        newly_earned = ContributorRecognitionService.evaluate_automatic_badges(
            user_id,
            latest_contribution_id=contribution.id,
        )

        logger.info(
            "RIP-001 check-in user=%s submission=%s contribution=%s source=%s",
            user_id,
            submission.id,
            contribution.id,
            submission_source,
        )
        return CheckinSubmitResult(
            submission=submission,
            contribution=contribution,
            newly_earned_badges=newly_earned,
        )
