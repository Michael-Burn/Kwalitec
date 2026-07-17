"""Founder Research Command Centre Service — RIP-003.

Aggregates product research, manages feedback workflow, product findings,
and Founder actions. Consumes Research Intelligence only — never reads or
writes Educational Evidence, Twin state, or learning algorithms.
"""

from __future__ import annotations

import logging
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta

from sqlalchemy import func, or_

from app.extensions import db
from app.models.mission import Mission
from app.models.research_feedback import (
    FEATURE_AREA_CHOICES,
    FINDING_STATUSES,
    SEVERITY_CHOICES,
    WORKFLOW_STATUSES,
    ResearchContributorBadge,
    ResearchFeedbackReview,
    ResearchFeedbackStatusTransition,
    ResearchFeedbackSubmission,
    ResearchFounderNote,
    ResearchProductFinding,
    ResearchProductFindingLink,
    ResearchProductFindingStatusTransition,
)
from app.models.user import User
from app.services.contributor_recognition_service import (
    BADGE_PRODUCT_SHAPER,
    ContributorRecognitionService,
)
from app.services.research_feedback_service import (
    FEATURE_CHOICES,
)
from app.services.research_insight_service import (
    TIME_WINDOW_7_DAYS,
    InsightEngineResult,
    InsightFilters,
    ResearchInsightService,
    ResearchInsightsLegacy,
)

logger = logging.getLogger(__name__)

EXPERIENCE_SCORES: dict[str, float] = {
    "Excellent": 5.0,
    "Good": 4.0,
    "Okay": 3.0,
    "Frustrating": 2.0,
    "Poor": 1.0,
}

CONFIDENCE_SCORES: dict[str, float] = {
    "Very Low": 1.0,
    "Low": 2.0,
    "Neutral": 3.0,
    "High": 4.0,
    "Very High": 5.0,
}

POSITIVE_RETURN_INTENTS = frozenset({"Definitely", "Probably"})

WORKFLOW_LABELS: dict[str, str] = {
    "new": "New",
    "under_review": "Under Review",
    "accepted": "Accepted",
    "planned": "Planned",
    "implemented": "Implemented",
    "released": "Released",
    "verified": "Verified",
    "rejected": "Rejected",
    "clarification_requested": "Clarification Requested",
}


@dataclass(frozen=True)
class InternalAlphaSummary:
    """Home overview metrics for the Founder Command Centre."""

    active_participants: int
    completed_checkins: int
    participation_rate_pct: float | None
    avg_product_experience: float | None
    would_open_tomorrow_pct: float | None
    avg_confidence: float | None
    outstanding_reviews: int
    implemented_feedback: int
    product_shapers: int
    newest_contributions: tuple[ResearchFeedbackSubmission, ...] = ()


@dataclass(frozen=True)
class ChangeSinceYesterday:
    """Day-over-day deltas for the command centre home."""

    new_submissions: int
    submissions_yesterday: int
    submissions_prior_day: int
    avg_experience_yesterday: float | None
    avg_experience_prior_day: float | None
    new_friction_mentions: int


@dataclass(frozen=True)
class ProductHealth:
    """Aggregated product health signals."""

    most_loved_feature: str | None
    most_confusing_feature: str | None
    most_mentioned_friction: str | None
    fastest_growing_concern: str | None
    recently_improved_areas: tuple[str, ...]
    areas_with_no_feedback: tuple[str, ...]


ResearchInsights = ResearchInsightsLegacy


@dataclass(frozen=True)
class InboxFilters:
    """Optional filters for the research inbox."""

    version: str | None = None
    badge: str | None = None
    feature: str | None = None
    severity: str | None = None
    status: str | None = None
    classification: str | None = None
    date_from: date | None = None
    date_to: date | None = None
    submission_source: str | None = None
    keyword: str | None = None
    student: str | None = None


@dataclass(frozen=True)
class SubmissionDetail:
    """Full detail view for one feedback submission."""

    submission: ResearchFeedbackSubmission
    student: User
    contributor_journey: object
    previous_submissions: tuple[ResearchFeedbackSubmission, ...]
    review: ResearchFeedbackReview | None
    status_history: tuple[ResearchFeedbackStatusTransition, ...]
    founder_notes: tuple[ResearchFounderNote, ...]
    linked_findings: tuple[ResearchProductFinding, ...]


@dataclass(frozen=True)
class TransitionResult:
    """Result of a workflow status transition."""

    submission: ResearchFeedbackSubmission
    transition: ResearchFeedbackStatusTransition
    newly_earned_badges: tuple[str, ...] = ()


@dataclass(frozen=True)
class FindingDetail:
    """Detail view for one product finding."""

    finding: ResearchProductFinding
    linked_submissions: tuple[ResearchFeedbackSubmission, ...]
    status_history: tuple[ResearchProductFindingStatusTransition, ...]


@dataclass(frozen=True)
class DashboardContext:
    """Complete data bundle for the Founder dashboard template."""

    summary: InternalAlphaSummary
    changes: ChangeSinceYesterday
    product_health: ProductHealth
    insights: ResearchInsights
    insight_engine: InsightEngineResult
    inbox: tuple[ResearchFeedbackSubmission, ...]
    findings: tuple[ResearchProductFinding, ...]
    filters: InboxFilters
    selected_submission: SubmissionDetail | None = None
    inbox_page: int = 1
    inbox_per_page: int = 50
    inbox_total: int = 0

    @property
    def inbox_total_pages(self) -> int:
        if self.inbox_per_page <= 0:
            return 1
        pages = (self.inbox_total + self.inbox_per_page - 1) // self.inbox_per_page
        return max(1, pages)

    @property
    def inbox_has_prev(self) -> bool:
        return self.inbox_page > 1

    @property
    def inbox_has_next(self) -> bool:
        return self.inbox_page < self.inbox_total_pages


class FounderResearchService:
    """Operational workspace for Founder product research (RIP-003)."""

    @staticmethod
    def _avg_score(values: list[float]) -> float | None:
        if not values:
            return None
        return round(sum(values) / len(values), 2)

    @staticmethod
    def _active_student_count() -> int:
        """Distinct users with mission activity as participation denominator."""
        return (
            db.session.query(func.count(func.distinct(Mission.user_id)))
            .scalar()
            or 0
        )

    @staticmethod
    def get_internal_alpha_summary() -> InternalAlphaSummary:
        """Build home overview metrics from stored research data."""
        submissions = ResearchFeedbackSubmission.query.all()
        completed = len(submissions)
        participant_ids = {s.user_id for s in submissions}
        active_participants = len(participant_ids)

        active_students = FounderResearchService._active_student_count()
        participation_rate: float | None = None
        if active_students > 0:
            participation_rate = round(
                100.0 * active_participants / active_students, 1
            )

        experience_scores = [
            EXPERIENCE_SCORES[s.experience_rating]
            for s in submissions
            if s.experience_rating in EXPERIENCE_SCORES
        ]
        confidence_scores = [
            CONFIDENCE_SCORES[s.confidence_rating]
            for s in submissions
            if s.confidence_rating in CONFIDENCE_SCORES
        ]
        positive_return = sum(
            1 for s in submissions if s.return_intent in POSITIVE_RETURN_INTENTS
        )
        would_open_pct: float | None = None
        if completed > 0:
            would_open_pct = round(100.0 * positive_return / completed, 1)

        outstanding = sum(1 for s in submissions if s.workflow_status == "new")
        implemented = sum(
            1
            for s in submissions
            if s.workflow_status in {"implemented", "released", "verified"}
        )
        product_shapers = ResearchContributorBadge.query.filter_by(
            badge_slug=BADGE_PRODUCT_SHAPER
        ).count()

        newest = (
            ResearchFeedbackSubmission.query.order_by(
                ResearchFeedbackSubmission.submitted_at.desc()
            )
            .limit(5)
            .all()
        )

        return InternalAlphaSummary(
            active_participants=active_participants,
            completed_checkins=completed,
            participation_rate_pct=participation_rate,
            avg_product_experience=FounderResearchService._avg_score(
                experience_scores
            ),
            would_open_tomorrow_pct=would_open_pct,
            avg_confidence=FounderResearchService._avg_score(confidence_scores),
            outstanding_reviews=outstanding,
            implemented_feedback=implemented,
            product_shapers=product_shapers,
            newest_contributions=tuple(newest),
        )

    @staticmethod
    def get_changes_since_yesterday(
        *,
        on_date: date | None = None,
    ) -> ChangeSinceYesterday:
        """Compare yesterday vs the prior day for key signals."""
        today = on_date or date.today()
        yesterday = today - timedelta(days=1)
        prior = today - timedelta(days=2)

        def _submissions_on(day: date) -> list[ResearchFeedbackSubmission]:
            start = datetime.combine(day, datetime.min.time())
            end = datetime.combine(day + timedelta(days=1), datetime.min.time())
            return ResearchFeedbackSubmission.query.filter(
                ResearchFeedbackSubmission.submitted_at >= start,
                ResearchFeedbackSubmission.submitted_at < end,
            ).all()

        subs_yesterday = _submissions_on(yesterday)
        subs_prior = _submissions_on(prior)

        exp_yesterday = FounderResearchService._avg_score(
            [
                EXPERIENCE_SCORES[s.experience_rating]
                for s in subs_yesterday
                if s.experience_rating in EXPERIENCE_SCORES
            ]
        )
        exp_prior = FounderResearchService._avg_score(
            [
                EXPERIENCE_SCORES[s.experience_rating]
                for s in subs_prior
                if s.experience_rating in EXPERIENCE_SCORES
            ]
        )

        new_friction = sum(
            1 for s in subs_yesterday if s.friction_area not in {"", "Nothing"}
        )

        return ChangeSinceYesterday(
            new_submissions=len(subs_yesterday),
            submissions_yesterday=len(subs_yesterday),
            submissions_prior_day=len(subs_prior),
            avg_experience_yesterday=exp_yesterday,
            avg_experience_prior_day=exp_prior,
            new_friction_mentions=new_friction,
        )

    @staticmethod
    def get_product_health() -> ProductHealth:
        """Aggregate loved, confusing, friction, and coverage signals."""
        submissions = ResearchFeedbackSubmission.query.all()
        if not submissions:
            return ProductHealth(
                most_loved_feature=None,
                most_confusing_feature=None,
                most_mentioned_friction=None,
                fastest_growing_concern=None,
                recently_improved_areas=(),
                areas_with_no_feedback=tuple(FEATURE_CHOICES),
            )

        feature_counts = Counter(s.feature_helped_most for s in submissions)
        friction_counts = Counter(
            s.friction_area for s in submissions if s.friction_area != "Nothing"
        )
        confusing_counts = Counter(
            s.feature_helped_most
            for s in submissions
            if s.classification == "Confusing"
            or s.friction_area not in {"", "Nothing"}
        )

        most_loved = feature_counts.most_common(1)[0][0] if feature_counts else None
        most_friction = (
            friction_counts.most_common(1)[0][0] if friction_counts else None
        )
        most_confusing = (
            confusing_counts.most_common(1)[0][0] if confusing_counts else None
        )

        week_ago = datetime.now(UTC).replace(tzinfo=None) - timedelta(days=7)
        two_weeks_ago = datetime.now(UTC).replace(tzinfo=None) - timedelta(days=14)
        recent_friction = Counter(
            s.friction_area
            for s in submissions
            if s.submitted_at >= week_ago and s.friction_area != "Nothing"
        )
        prior_friction = Counter(
            s.friction_area
            for s in submissions
            if two_weeks_ago <= s.submitted_at < week_ago
            and s.friction_area != "Nothing"
        )
        growth: list[tuple[str, int]] = []
        for area, count in recent_friction.items():
            delta = count - prior_friction.get(area, 0)
            if delta > 0:
                growth.append((area, delta))
        growth.sort(key=lambda item: item[1], reverse=True)
        fastest_growing = growth[0][0] if growth else None

        recent_week = [
            s
            for s in submissions
            if s.submitted_at >= week_ago
            and s.experience_rating in {"Excellent", "Good"}
        ]
        prior_week = [
            s
            for s in submissions
            if two_weeks_ago <= s.submitted_at < week_ago
        ]
        recent_features = {s.feature_helped_most for s in recent_week}
        prior_avg_by_feature: dict[str, list[float]] = {}
        for s in prior_week:
            score = EXPERIENCE_SCORES.get(s.experience_rating)
            if score is not None:
                prior_avg_by_feature.setdefault(s.feature_helped_most, []).append(
                    score
                )
        improved: list[str] = []
        for feat in recent_features:
            recent_scores = [
                EXPERIENCE_SCORES[s.experience_rating]
                for s in recent_week
                if s.feature_helped_most == feat
                and s.experience_rating in EXPERIENCE_SCORES
            ]
            prior_scores = prior_avg_by_feature.get(feat, [])
            if recent_scores and prior_scores:
                if (
                    sum(recent_scores) / len(recent_scores)
                    > sum(prior_scores) / len(prior_scores)
                ):
                    improved.append(feat)

        mentioned_features = {s.feature_helped_most for s in submissions}
        no_feedback = tuple(f for f in FEATURE_CHOICES if f not in mentioned_features)

        return ProductHealth(
            most_loved_feature=most_loved,
            most_confusing_feature=most_confusing,
            most_mentioned_friction=most_friction,
            fastest_growing_concern=fastest_growing,
            recently_improved_areas=tuple(improved),
            areas_with_no_feedback=no_feedback,
        )

    @staticmethod
    def _insight_filters_from_inbox(filters: InboxFilters) -> InsightFilters:
        return InsightFilters(
            version=filters.version,
            badge=filters.badge,
            feature=filters.feature,
            severity=filters.severity,
            status=filters.status,
            classification=filters.classification,
            date_from=filters.date_from,
            date_to=filters.date_to,
            submission_source=filters.submission_source,
        )

    @staticmethod
    def get_insights(
        filters: InboxFilters | None = None,
    ) -> ResearchInsights:
        """Pure aggregation insights for the command centre (RIP-004 legacy)."""
        insight_filters = FounderResearchService._insight_filters_from_inbox(
            filters or InboxFilters()
        )
        return ResearchInsightService.get_legacy_insights(insight_filters)

    @staticmethod
    def get_insight_engine(
        filters: InboxFilters | None = None,
        *,
        time_window: str = TIME_WINDOW_7_DAYS,
        as_of: date | None = None,
        custom_date_from: date | None = None,
        custom_date_to: date | None = None,
        current_release: str | None = None,
        previous_release: str | None = None,
    ) -> InsightEngineResult:
        """Generate full RIP-004 insight engine output."""
        insight_filters = FounderResearchService._insight_filters_from_inbox(
            filters or InboxFilters()
        )
        return ResearchInsightService.generate_insights(
            insight_filters,
            time_window=time_window,
            as_of=as_of,
            custom_date_from=custom_date_from,
            custom_date_to=custom_date_to,
            current_release=current_release,
            previous_release=previous_release,
        )

    @staticmethod
    def _apply_inbox_filters(
        query,
        filters: InboxFilters,
    ):
        """Apply optional inbox filters to a submission query."""
        if filters.version:
            query = query.filter(
                ResearchFeedbackSubmission.product_version == filters.version
            )
        if filters.feature:
            query = query.filter(
                or_(
                    ResearchFeedbackSubmission.feature_helped_most
                    == filters.feature,
                    ResearchFeedbackSubmission.friction_area == filters.feature,
                )
            )
        if filters.status:
            query = query.filter(
                ResearchFeedbackSubmission.workflow_status == filters.status
            )
        if filters.classification:
            query = query.filter(
                ResearchFeedbackSubmission.classification == filters.classification
            )
        if filters.submission_source:
            query = query.filter(
                ResearchFeedbackSubmission.submission_source
                == filters.submission_source
            )
        if filters.date_from:
            start = datetime.combine(filters.date_from, datetime.min.time())
            query = query.filter(ResearchFeedbackSubmission.submitted_at >= start)
        if filters.date_to:
            end = datetime.combine(
                filters.date_to + timedelta(days=1), datetime.min.time()
            )
            query = query.filter(ResearchFeedbackSubmission.submitted_at < end)
        if filters.keyword:
            pattern = f"%{filters.keyword.strip()}%"
            query = query.filter(
                or_(
                    ResearchFeedbackSubmission.free_text.ilike(pattern),
                    ResearchFeedbackSubmission.feature_helped_most.ilike(pattern),
                    ResearchFeedbackSubmission.friction_area.ilike(pattern),
                    ResearchFeedbackSubmission.product_version.ilike(pattern),
                )
            )
        if filters.student:
            pattern = f"%{filters.student.strip()}%"
            query = query.join(User).filter(User.email.ilike(pattern))
        if filters.badge:
            query = (
                query.join(User)
                .join(
                    ResearchContributorBadge,
                    ResearchContributorBadge.user_id == User.id,
                )
                .filter(ResearchContributorBadge.badge_slug == filters.badge)
            )
        if filters.severity:
            query = (
                query.join(ResearchProductFindingLink)
                .join(ResearchProductFinding)
                .filter(ResearchProductFinding.severity == filters.severity)
            )
        return query

    @staticmethod
    def count_inbox(filters: InboxFilters | None = None) -> int:
        """Return the number of submissions matching inbox filters."""
        filters = filters or InboxFilters()
        query = ResearchFeedbackSubmission.query
        query = FounderResearchService._apply_inbox_filters(query, filters)
        return int(query.count())

    @staticmethod
    def list_inbox(
        filters: InboxFilters | None = None,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[ResearchFeedbackSubmission, ...]:
        """Return filtered research inbox submissions (paginated)."""
        filters = filters or InboxFilters()
        query = ResearchFeedbackSubmission.query.order_by(
            ResearchFeedbackSubmission.submitted_at.desc()
        )
        query = FounderResearchService._apply_inbox_filters(query, filters)
        if offset > 0:
            query = query.offset(offset)
        return tuple(query.limit(limit).all())

    @staticmethod
    def get_submission_detail(submission_id: int) -> SubmissionDetail | None:
        """Build full detail for one feedback submission."""
        submission = db.session.get(ResearchFeedbackSubmission, submission_id)
        if submission is None:
            return None

        student = db.session.get(User, submission.user_id)
        if student is None:
            return None

        journey = ContributorRecognitionService.get_journey_summary(submission.user_id)
        previous = tuple(
            ResearchFeedbackSubmission.query.filter(
                ResearchFeedbackSubmission.user_id == submission.user_id,
                ResearchFeedbackSubmission.id != submission.id,
            )
            .order_by(ResearchFeedbackSubmission.submitted_at.desc())
            .limit(10)
            .all()
        )
        review = ResearchFeedbackReview.query.filter_by(
            submission_id=submission_id
        ).first()
        history = tuple(
            ResearchFeedbackStatusTransition.query.filter_by(
                submission_id=submission_id
            )
            .order_by(ResearchFeedbackStatusTransition.transitioned_at)
            .all()
        )
        notes = tuple(
            ResearchFounderNote.query.filter_by(submission_id=submission_id)
            .order_by(ResearchFounderNote.created_at)
            .all()
        )
        linked = tuple(
            link.finding
            for link in ResearchProductFindingLink.query.filter_by(
                submission_id=submission_id
            ).all()
        )

        return SubmissionDetail(
            submission=submission,
            student=student,
            contributor_journey=journey,
            previous_submissions=previous,
            review=review,
            status_history=history,
            founder_notes=notes,
            linked_findings=linked,
        )

    @staticmethod
    def _record_status_transition(
        submission: ResearchFeedbackSubmission,
        founder_user_id: int,
        to_status: str,
        *,
        rationale: str | None = None,
        transitioned_at: datetime | None = None,
    ) -> ResearchFeedbackStatusTransition:
        """Append a workflow transition without overwriting history."""
        if to_status not in WORKFLOW_STATUSES:
            raise ValueError(f"Invalid workflow status: {to_status}")

        when = transitioned_at or datetime.now(UTC).replace(tzinfo=None)
        from_status = submission.workflow_status
        transition = ResearchFeedbackStatusTransition(
            submission_id=submission.id,
            from_status=from_status,
            to_status=to_status,
            reviewer_user_id=founder_user_id,
            rationale=(rationale or "").strip() or None,
            transitioned_at=when,
        )
        submission.workflow_status = to_status
        db.session.add(transition)
        return transition

    @staticmethod
    def transition_submission_status(
        submission_id: int,
        founder_user_id: int,
        to_status: str,
        *,
        rationale: str | None = None,
    ) -> TransitionResult:
        """Move a submission through the research workflow."""
        submission = db.session.get(ResearchFeedbackSubmission, submission_id)
        if submission is None:
            raise ValueError(f"Submission not found: {submission_id}")

        transition = FounderResearchService._record_status_transition(
            submission,
            founder_user_id,
            to_status,
            rationale=rationale,
        )

        newly_earned: tuple[str, ...] = ()
        if to_status == "implemented":
            review = ContributorRecognitionService.founder_review_submission(
                submission_id,
                founder_user_id,
                helpful=bool(
                    submission.founder_review and submission.founder_review.is_helpful
                ),
                insightful=bool(
                    submission.founder_review
                    and submission.founder_review.is_insightful
                ),
                implemented=True,
            )
            newly_earned = review.newly_earned_badges
        else:
            db.session.commit()

        logger.info(
            "RIP-003 status transition submission=%s %s->%s founder=%s",
            submission_id,
            transition.from_status,
            to_status,
            founder_user_id,
        )
        return TransitionResult(
            submission=submission,
            transition=transition,
            newly_earned_badges=newly_earned,
        )

    @staticmethod
    def apply_founder_marks(
        submission_id: int,
        founder_user_id: int,
        *,
        helpful: bool | None = None,
        insightful: bool | None = None,
    ) -> ResearchFeedbackReview:
        """Mark submission helpful and/or insightful (RIP-002 integration)."""
        submission = db.session.get(ResearchFeedbackSubmission, submission_id)
        if submission is None:
            raise ValueError(f"Submission not found: {submission_id}")

        existing = ResearchFeedbackReview.query.filter_by(
            submission_id=submission_id
        ).first()
        helpful_val = helpful if helpful is not None else (
            existing.is_helpful if existing else False
        )
        insightful_val = (
            insightful
            if insightful is not None
            else (existing.is_insightful if existing else False)
        )
        implemented_val = existing.is_implemented if existing else False

        result = ContributorRecognitionService.founder_review_submission(
            submission_id,
            founder_user_id,
            helpful=helpful_val,
            insightful=insightful_val,
            implemented=implemented_val,
        )
        return result.review

    @staticmethod
    def add_founder_note(
        submission_id: int,
        founder_user_id: int,
        note_text: str,
    ) -> ResearchFounderNote:
        """Append an internal Founder note to a submission."""
        submission = db.session.get(ResearchFeedbackSubmission, submission_id)
        if submission is None:
            raise ValueError(f"Submission not found: {submission_id}")

        cleaned = note_text.strip()
        if not cleaned:
            raise ValueError("Note text is required")
        if len(cleaned) > 1000:
            raise ValueError("Note text must be at most 1000 characters")

        note = ResearchFounderNote(
            submission_id=submission_id,
            founder_user_id=founder_user_id,
            note_text=cleaned,
        )
        db.session.add(note)
        db.session.commit()
        return note

    @staticmethod
    def create_product_finding(
        founder_user_id: int,
        *,
        title: str,
        summary: str,
        severity: str,
        feature_area: str,
        status: str = "new",
        target_release: str | None = None,
        notes: str | None = None,
        linked_submission_ids: tuple[int, ...] = (),
    ) -> ResearchProductFinding:
        """Create a product finding optionally linked to feedback."""
        cleaned_title = title.strip()
        cleaned_summary = summary.strip()
        if not cleaned_title:
            raise ValueError("Title is required")
        if not cleaned_summary:
            raise ValueError("Summary is required")
        if severity not in SEVERITY_CHOICES:
            raise ValueError(f"Invalid severity: {severity}")
        if feature_area not in FEATURE_AREA_CHOICES:
            raise ValueError(f"Invalid feature_area: {feature_area}")
        if status not in FINDING_STATUSES:
            raise ValueError(f"Invalid status: {status}")

        finding = ResearchProductFinding(
            title=cleaned_title,
            summary=cleaned_summary,
            severity=severity,
            feature_area=feature_area,
            status=status,
            target_release=(target_release or "").strip() or None,
            notes=(notes or "").strip() or None,
            created_by_user_id=founder_user_id,
        )
        db.session.add(finding)
        db.session.flush()

        initial = ResearchProductFindingStatusTransition(
            finding_id=finding.id,
            from_status=None,
            to_status=status,
            reviewer_user_id=founder_user_id,
        )
        db.session.add(initial)

        for sub_id in linked_submission_ids:
            submission = db.session.get(ResearchFeedbackSubmission, sub_id)
            if submission is None:
                raise ValueError(f"Submission not found: {sub_id}")
            db.session.add(
                ResearchProductFindingLink(
                    finding_id=finding.id,
                    submission_id=sub_id,
                )
            )

        db.session.commit()
        logger.info(
            "RIP-003 finding created id=%s founder=%s",
            finding.id,
            founder_user_id,
        )
        return finding

    @staticmethod
    def get_finding_detail(finding_id: int) -> FindingDetail | None:
        """Return one product finding with linked feedback and history."""
        finding = db.session.get(ResearchProductFinding, finding_id)
        if finding is None:
            return None

        links = ResearchProductFindingLink.query.filter_by(
            finding_id=finding_id
        ).all()
        submissions = tuple(
            db.session.get(ResearchFeedbackSubmission, link.submission_id)
            for link in links
        )
        submissions = tuple(s for s in submissions if s is not None)
        history = tuple(
            ResearchProductFindingStatusTransition.query.filter_by(
                finding_id=finding_id
            )
            .order_by(ResearchProductFindingStatusTransition.transitioned_at)
            .all()
        )
        return FindingDetail(
            finding=finding,
            linked_submissions=submissions,
            status_history=history,
        )

    @staticmethod
    def transition_finding_status(
        finding_id: int,
        founder_user_id: int,
        to_status: str,
        *,
        rationale: str | None = None,
        target_release: str | None = None,
    ) -> ResearchProductFinding:
        """Move a product finding through its lifecycle."""
        finding = db.session.get(ResearchProductFinding, finding_id)
        if finding is None:
            raise ValueError(f"Finding not found: {finding_id}")
        if to_status not in FINDING_STATUSES:
            raise ValueError(f"Invalid status: {to_status}")

        when = datetime.now(UTC).replace(tzinfo=None)
        transition = ResearchProductFindingStatusTransition(
            finding_id=finding_id,
            from_status=finding.status,
            to_status=to_status,
            reviewer_user_id=founder_user_id,
            rationale=(rationale or "").strip() or None,
            transitioned_at=when,
        )
        finding.status = to_status
        finding.updated_at = when
        if target_release is not None:
            finding.target_release = target_release.strip() or None
        db.session.add(transition)
        db.session.commit()
        return finding

    @staticmethod
    def link_submission_to_finding(
        finding_id: int,
        submission_id: int,
    ) -> ResearchProductFindingLink:
        """Link an additional feedback submission to a finding."""
        finding = db.session.get(ResearchProductFinding, finding_id)
        if finding is None:
            raise ValueError(f"Finding not found: {finding_id}")
        submission = db.session.get(ResearchFeedbackSubmission, submission_id)
        if submission is None:
            raise ValueError(f"Submission not found: {submission_id}")

        existing = ResearchProductFindingLink.query.filter_by(
            finding_id=finding_id,
            submission_id=submission_id,
        ).first()
        if existing is not None:
            return existing

        link = ResearchProductFindingLink(
            finding_id=finding_id,
            submission_id=submission_id,
        )
        db.session.add(link)
        db.session.commit()
        return link

    @staticmethod
    def list_findings(
        *,
        status: str | None = None,
        severity: str | None = None,
        feature_area: str | None = None,
        limit: int = 50,
    ) -> tuple[ResearchProductFinding, ...]:
        """Return product findings with optional filters."""
        query = ResearchProductFinding.query.order_by(
            ResearchProductFinding.created_at.desc()
        )
        if status:
            query = query.filter(ResearchProductFinding.status == status)
        if severity:
            query = query.filter(ResearchProductFinding.severity == severity)
        if feature_area:
            query = query.filter(ResearchProductFinding.feature_area == feature_area)
        return tuple(query.limit(limit).all())

    @staticmethod
    def build_dashboard_context(
        filters: InboxFilters | None = None,
        *,
        selected_submission_id: int | None = None,
        time_window: str = TIME_WINDOW_7_DAYS,
        as_of: date | None = None,
        custom_date_from: date | None = None,
        custom_date_to: date | None = None,
        current_release: str | None = None,
        previous_release: str | None = None,
        inbox_page: int = 1,
        inbox_per_page: int = 50,
    ) -> DashboardContext:
        """Assemble all data for the Founder Research Command Centre."""
        filters = filters or InboxFilters()
        selected: SubmissionDetail | None = None
        if selected_submission_id is not None:
            selected = FounderResearchService.get_submission_detail(
                selected_submission_id
            )

        insight_engine = FounderResearchService.get_insight_engine(
            filters,
            time_window=time_window,
            as_of=as_of,
            custom_date_from=custom_date_from,
            custom_date_to=custom_date_to,
            current_release=current_release,
            previous_release=previous_release,
        )

        per_page = max(1, min(inbox_per_page, 100))
        page = max(1, inbox_page)
        inbox_total = FounderResearchService.count_inbox(filters)
        if inbox_total:
            total_pages = max(1, (inbox_total + per_page - 1) // per_page)
        else:
            total_pages = 1
        if page > total_pages:
            page = total_pages
        offset = (page - 1) * per_page

        return DashboardContext(
            summary=FounderResearchService.get_internal_alpha_summary(),
            changes=FounderResearchService.get_changes_since_yesterday(on_date=as_of),
            product_health=FounderResearchService.get_product_health(),
            insights=insight_engine.legacy,
            insight_engine=insight_engine,
            inbox=FounderResearchService.list_inbox(
                filters, limit=per_page, offset=offset
            ),
            findings=FounderResearchService.list_findings(),
            filters=filters,
            selected_submission=selected,
            inbox_page=page,
            inbox_per_page=per_page,
            inbox_total=inbox_total,
        )
