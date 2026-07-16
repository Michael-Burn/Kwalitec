"""Research Insight Engine — RIP-004.

Converts structured research observations into objective, reproducible
product insights via aggregation and trend analysis only.

Never uses AI, never makes product decisions, and never reads or writes
Educational Intelligence state.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, timedelta

from sqlalchemy import func, or_

from app.extensions import db
from app.models.mission import Mission
from app.models.research_feedback import (
    ResearchContributorBadge,
    ResearchFeedbackSubmission,
    ResearchProductFinding,
    ResearchProductFindingLink,
)
from app.models.user import User
from app.services.research_feedback_service import (
    CLASSIFICATION_CHOICES,
    FEATURE_CHOICES,
    PRODUCT_VERSION,
)

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

TIME_WINDOW_TODAY = "today"
TIME_WINDOW_7_DAYS = "7_days"
TIME_WINDOW_30_DAYS = "30_days"
TIME_WINDOW_CURRENT_RELEASE = "current_release"
TIME_WINDOW_PREVIOUS_RELEASE = "previous_release"
TIME_WINDOW_CUSTOM = "custom"

TIME_WINDOW_LABELS: dict[str, str] = {
    TIME_WINDOW_TODAY: "Today",
    TIME_WINDOW_7_DAYS: "7 days",
    TIME_WINDOW_30_DAYS: "30 days",
    TIME_WINDOW_CURRENT_RELEASE: "Current Release",
    TIME_WINDOW_PREVIOUS_RELEASE: "Previous Release",
    TIME_WINDOW_CUSTOM: "Custom",
}

COMPARISON_PREVIOUS_DAY = "previous_day"
COMPARISON_PREVIOUS_WEEK = "previous_week"
COMPARISON_PREVIOUS_RELEASE = "previous_release"

INSIGHT_FAMILY_EXPERIENCE = "experience"
INSIGHT_FAMILY_BEHAVIOUR = "behaviour"
INSIGHT_FAMILY_FRICTION = "friction"
INSIGHT_FAMILY_TREND = "trend"
INSIGHT_FAMILY_RELEASE = "release"
INSIGHT_FAMILY_RESEARCH = "research"

CONFIDENCE_LOW = "Low"
CONFIDENCE_MEDIUM = "Medium"
CONFIDENCE_HIGH = "High"

PRIORITY_CRITICAL = "Critical"
PRIORITY_HIGH = "High"
PRIORITY_MEDIUM = "Medium"
PRIORITY_LOW = "Low"


@dataclass(frozen=True)
class InsightFilters:
    """Optional filters applied before insight generation."""

    version: str | None = None
    badge: str | None = None
    feature: str | None = None
    severity: str | None = None
    status: str | None = None
    classification: str | None = None
    date_from: date | None = None
    date_to: date | None = None
    submission_source: str | None = None


@dataclass(frozen=True)
class InsightComparison:
    """Pure numeric comparison between two observation windows."""

    label: str
    current_value: float | int | None
    previous_value: float | int | None
    delta: float | int | None
    comparison_type: str


@dataclass(frozen=True)
class ResearchInsight:
    """One objective product insight derived from research observations."""

    family: str
    title: str
    summary: str
    supporting_observation_count: int
    supporting_submission_ids: tuple[int, ...]
    time_window: str
    confidence: str
    affected_feature: str | None
    related_finding_ids: tuple[int, ...]
    suggested_review_priority: str
    comparison: InsightComparison | None = None


@dataclass(frozen=True)
class ResearchInsightsLegacy:
    """Backward-compatible snapshot for RIP-003 dashboard sections."""

    most_common_feature: str | None
    most_common_friction: str | None
    most_common_suggestion_category: str | None
    participation_trend: tuple[tuple[str, int], ...]
    contribution_growth: tuple[tuple[str, int], ...]
    recently_awarded_badges: tuple[ResearchContributorBadge, ...]


@dataclass(frozen=True)
class InsightEngineResult:
    """Complete insight engine output for the Founder Command Centre."""

    time_window: str
    time_window_label: str
    filters: InsightFilters
    insights: tuple[ResearchInsight, ...]
    top_trends: tuple[ResearchInsight, ...]
    emerging_concerns: tuple[ResearchInsight, ...]
    most_improved_areas: tuple[ResearchInsight, ...]
    stable_areas: tuple[ResearchInsight, ...]
    participation: tuple[ResearchInsight, ...]
    release_comparison: tuple[ResearchInsight, ...]
    comparisons: tuple[InsightComparison, ...]
    legacy: ResearchInsightsLegacy


class ResearchInsightService:
    """Aggregation and trend analysis for research observations (RIP-004)."""

    @staticmethod
    def _confidence(count: int) -> str:
        if count >= 10:
            return CONFIDENCE_HIGH
        if count >= 3:
            return CONFIDENCE_MEDIUM
        return CONFIDENCE_LOW

    @staticmethod
    def _review_priority(
        *,
        observation_count: int,
        friction_signal: bool = False,
        declining_signal: bool = False,
        positive_signal: bool = False,
    ) -> str:
        if friction_signal and observation_count >= 5:
            return PRIORITY_CRITICAL
        if friction_signal or declining_signal:
            return PRIORITY_HIGH
        if positive_signal:
            return PRIORITY_LOW
        if observation_count >= 10:
            return PRIORITY_HIGH
        return PRIORITY_MEDIUM

    @staticmethod
    def _avg_score(values: list[float]) -> float | None:
        if not values:
            return None
        return round(sum(values) / len(values), 2)

    @staticmethod
    def _window_bounds(
        time_window: str,
        *,
        as_of: date,
        custom_date_from: date | None = None,
        custom_date_to: date | None = None,
        current_release: str | None = None,
        previous_release: str | None = None,
    ) -> tuple[datetime | None, datetime]:
        """Return (start, end) datetimes for the selected time window."""
        end_day = as_of + timedelta(days=1)
        end = datetime.combine(end_day, datetime.min.time())

        if time_window == TIME_WINDOW_TODAY:
            start = datetime.combine(as_of, datetime.min.time())
            return start, end

        if time_window == TIME_WINDOW_7_DAYS:
            start = datetime.combine(as_of - timedelta(days=6), datetime.min.time())
            return start, end

        if time_window == TIME_WINDOW_30_DAYS:
            start = datetime.combine(as_of - timedelta(days=29), datetime.min.time())
            return start, end

        if time_window == TIME_WINDOW_CUSTOM:
            if custom_date_from is None:
                start = datetime.combine(as_of - timedelta(days=6), datetime.min.time())
            else:
                start = datetime.combine(custom_date_from, datetime.min.time())
            if custom_date_to is not None:
                end = datetime.combine(
                    custom_date_to + timedelta(days=1), datetime.min.time()
                )
            return start, end

        if time_window == TIME_WINDOW_CURRENT_RELEASE:
            return None, end  # filtered by version in query

        if time_window == TIME_WINDOW_PREVIOUS_RELEASE:
            return None, end  # filtered by version in query

        start = datetime.combine(as_of - timedelta(days=6), datetime.min.time())
        return start, end

    @staticmethod
    def _comparison_bounds(
        time_window: str,
        *,
        as_of: date,
    ) -> tuple[datetime, datetime, datetime, datetime]:
        """Return (current_start, current_end, previous_start, previous_end)."""
        if time_window == TIME_WINDOW_TODAY:
            current_start = datetime.combine(as_of, datetime.min.time())
            current_end = datetime.combine(
                as_of + timedelta(days=1), datetime.min.time()
            )
            prior = as_of - timedelta(days=1)
            previous_start = datetime.combine(prior, datetime.min.time())
            previous_end = current_start
            return current_start, current_end, previous_start, previous_end

        days = 7 if time_window in {TIME_WINDOW_7_DAYS, TIME_WINDOW_CUSTOM} else 30
        if time_window == TIME_WINDOW_30_DAYS:
            days = 30

        current_start = datetime.combine(
            as_of - timedelta(days=days - 1), datetime.min.time()
        )
        current_end = datetime.combine(as_of + timedelta(days=1), datetime.min.time())
        previous_end = current_start
        previous_start = datetime.combine(
            as_of - timedelta(days=2 * days - 1), datetime.min.time()
        )
        return current_start, current_end, previous_start, previous_end

    @staticmethod
    def _apply_filters(query, filters: InsightFilters):
        if filters.version:
            query = query.filter(
                ResearchFeedbackSubmission.product_version == filters.version
            )
        if filters.feature:
            query = query.filter(
                or_(
                    ResearchFeedbackSubmission.feature_helped_most == filters.feature,
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
    def _fetch_submissions(
        filters: InsightFilters,
        *,
        window_start: datetime | None,
        window_end: datetime,
        release_version: str | None = None,
    ) -> list[ResearchFeedbackSubmission]:
        query = ResearchFeedbackSubmission.query
        query = ResearchInsightService._apply_filters(query, filters)
        if window_start is not None:
            query = query.filter(
                ResearchFeedbackSubmission.submitted_at >= window_start
            )
        query = query.filter(ResearchFeedbackSubmission.submitted_at < window_end)
        if release_version is not None:
            query = query.filter(
                ResearchFeedbackSubmission.product_version == release_version
            )
        return query.all()

    @staticmethod
    def _related_findings(
        submission_ids: tuple[int, ...],
    ) -> tuple[int, ...]:
        if not submission_ids:
            return ()
        rows = (
            ResearchProductFindingLink.query.filter(
                ResearchProductFindingLink.submission_id.in_(submission_ids)
            )
            .with_entities(ResearchProductFindingLink.finding_id)
            .distinct()
            .all()
        )
        return tuple(sorted({row[0] for row in rows}))

    @staticmethod
    def _submission_ids(
        submissions: list[ResearchFeedbackSubmission],
    ) -> tuple[int, ...]:
        return tuple(s.id for s in submissions)

    @staticmethod
    def _build_experience_insights(
        submissions: list[ResearchFeedbackSubmission],
        *,
        time_window_label: str,
        comparison_submissions: list[ResearchFeedbackSubmission] | None = None,
    ) -> tuple[ResearchInsight, ...]:
        if not submissions:
            return ()

        ids = ResearchInsightService._submission_ids(submissions)
        count = len(submissions)
        confidence = ResearchInsightService._confidence(count)
        finding_ids = ResearchInsightService._related_findings(ids)

        experience_scores = [
            EXPERIENCE_SCORES[s.experience_rating]
            for s in submissions
            if s.experience_rating in EXPERIENCE_SCORES
        ]
        avg_experience = ResearchInsightService._avg_score(experience_scores)

        confidence_scores = [
            CONFIDENCE_SCORES[s.confidence_rating]
            for s in submissions
            if s.confidence_rating in CONFIDENCE_SCORES
        ]
        avg_confidence = ResearchInsightService._avg_score(confidence_scores)

        positive_return = sum(
            1 for s in submissions if s.return_intent in POSITIVE_RETURN_INTENTS
        )
        would_open_pct: float | None = None
        if count > 0:
            would_open_pct = round(100.0 * positive_return / count, 1)

        feature_counts = Counter(s.feature_helped_most for s in submissions)
        top_feature = feature_counts.most_common(1)[0][0] if feature_counts else None

        insights: list[ResearchInsight] = []

        exp_summary = (
            f"Average product experience is {avg_experience}/5 "
            f"across {count} observation(s)."
            if avg_experience is not None
            else f"No experience scores in {count} observation(s)."
        )
        exp_comparison: InsightComparison | None = None
        if comparison_submissions is not None and comparison_submissions:
            prior_scores = [
                EXPERIENCE_SCORES[s.experience_rating]
                for s in comparison_submissions
                if s.experience_rating in EXPERIENCE_SCORES
            ]
            prior_avg = ResearchInsightService._avg_score(prior_scores)
            if avg_experience is not None and prior_avg is not None:
                exp_comparison = InsightComparison(
                    label="Average experience",
                    current_value=avg_experience,
                    previous_value=prior_avg,
                    delta=round(avg_experience - prior_avg, 2),
                    comparison_type=COMPARISON_PREVIOUS_WEEK,
                )

        insights.append(
            ResearchInsight(
                family=INSIGHT_FAMILY_EXPERIENCE,
                title="Average Product Experience",
                summary=exp_summary,
                supporting_observation_count=count,
                supporting_submission_ids=ids,
                time_window=time_window_label,
                confidence=confidence,
                affected_feature=top_feature,
                related_finding_ids=finding_ids,
                suggested_review_priority=ResearchInsightService._review_priority(
                    observation_count=count,
                    positive_signal=avg_experience is not None
                    and avg_experience >= 4.0,
                ),
                comparison=exp_comparison,
            )
        )

        conf_summary = (
            f"Average confidence is {avg_confidence}/5 "
            f"across {count} observation(s)."
            if avg_confidence is not None
            else "No confidence scores recorded."
        )
        insights.append(
            ResearchInsight(
                family=INSIGHT_FAMILY_EXPERIENCE,
                title="Average Confidence",
                summary=conf_summary,
                supporting_observation_count=count,
                supporting_submission_ids=ids,
                time_window=time_window_label,
                confidence=confidence,
                affected_feature=top_feature,
                related_finding_ids=finding_ids,
                suggested_review_priority=PRIORITY_MEDIUM,
            )
        )

        return_summary = (
            f"{would_open_pct}% of contributors would open Kwalitec again tomorrow "
            f"({positive_return}/{count})."
            if would_open_pct is not None
            else "No return-intent data."
        )
        insights.append(
            ResearchInsight(
                family=INSIGHT_FAMILY_EXPERIENCE,
                title="Would Open Tomorrow",
                summary=return_summary,
                supporting_observation_count=count,
                supporting_submission_ids=ids,
                time_window=time_window_label,
                confidence=confidence,
                affected_feature=top_feature,
                related_finding_ids=finding_ids,
                suggested_review_priority=ResearchInsightService._review_priority(
                    observation_count=count,
                    positive_signal=would_open_pct is not None and would_open_pct >= 70,
                ),
            )
        )

        if exp_comparison is not None:
            direction = "improved" if (exp_comparison.delta or 0) >= 0 else "declined"
            trend_summary = (
                f"Experience {direction} from {exp_comparison.previous_value}/5 "
                f"to {exp_comparison.current_value}/5 "
                f"(delta {exp_comparison.delta:+.2f})."
            )
            insights.append(
                ResearchInsight(
                    family=INSIGHT_FAMILY_EXPERIENCE,
                    title="Experience Trend",
                    summary=trend_summary,
                    supporting_observation_count=count,
                    supporting_submission_ids=ids,
                    time_window=time_window_label,
                    confidence=confidence,
                    affected_feature=top_feature,
                    related_finding_ids=finding_ids,
                    suggested_review_priority=ResearchInsightService._review_priority(
                        observation_count=count,
                        declining_signal=(exp_comparison.delta or 0) < 0,
                    ),
                    comparison=exp_comparison,
                )
            )

        return tuple(insights)

    @staticmethod
    def _build_behaviour_insights(
        submissions: list[ResearchFeedbackSubmission],
        *,
        time_window_label: str,
        as_of: date,
        comparison_submissions: list[ResearchFeedbackSubmission] | None = None,
    ) -> tuple[ResearchInsight, ...]:
        if not submissions:
            return ()

        ids = ResearchInsightService._submission_ids(submissions)
        count = len(submissions)
        confidence = ResearchInsightService._confidence(count)
        finding_ids = ResearchInsightService._related_findings(ids)

        participant_ids = {s.user_id for s in submissions}
        active_students = (
            db.session.query(func.count(func.distinct(Mission.user_id))).scalar() or 0
        )
        participation_rate: float | None = None
        if active_students > 0:
            participation_rate = round(
                100.0 * len(participant_ids) / active_students, 1
            )

        user_submission_counts = Counter(s.user_id for s in submissions)
        returning = sum(1 for c in user_submission_counts.values() if c > 1)

        completed = count
        participation_summary = (
            f"{len(participant_ids)} distinct contributor(s) submitted "
            f"{completed} check-in(s)"
            + (
                f"; participation rate {participation_rate}%."
                if participation_rate is not None
                else "."
            )
        )

        insights: list[ResearchInsight] = [
            ResearchInsight(
                family=INSIGHT_FAMILY_BEHAVIOUR,
                title="Participation",
                summary=participation_summary,
                supporting_observation_count=count,
                supporting_submission_ids=ids,
                time_window=time_window_label,
                confidence=confidence,
                affected_feature=None,
                related_finding_ids=finding_ids,
                suggested_review_priority=PRIORITY_MEDIUM,
            ),
            ResearchInsight(
                family=INSIGHT_FAMILY_BEHAVIOUR,
                title="Returning Contributors",
                summary=(
                    f"{returning} contributor(s) submitted more than once "
                    f"in this window."
                ),
                supporting_observation_count=returning,
                supporting_submission_ids=ids,
                time_window=time_window_label,
                confidence=ResearchInsightService._confidence(returning),
                affected_feature=None,
                related_finding_ids=finding_ids,
                suggested_review_priority=PRIORITY_LOW,
            ),
            ResearchInsight(
                family=INSIGHT_FAMILY_BEHAVIOUR,
                title="Completion Rate",
                summary=(
                    f"{completed} completed check-in(s) recorded "
                    f"in {time_window_label}."
                ),
                supporting_observation_count=completed,
                supporting_submission_ids=ids,
                time_window=time_window_label,
                confidence=confidence,
                affected_feature=None,
                related_finding_ids=finding_ids,
                suggested_review_priority=PRIORITY_MEDIUM,
            ),
        ]

        growth_comparison: InsightComparison | None = None
        if comparison_submissions is not None:
            prior_count = len(comparison_submissions)
            growth_comparison = InsightComparison(
                label="Submission count",
                current_value=count,
                previous_value=prior_count,
                delta=count - prior_count,
                comparison_type=COMPARISON_PREVIOUS_WEEK,
            )
            growth_summary = (
                f"Submissions moved from {prior_count} to {count} "
                f"(delta {count - prior_count:+d})."
            )
            insights.append(
                ResearchInsight(
                    family=INSIGHT_FAMILY_BEHAVIOUR,
                    title="Contribution Growth",
                    summary=growth_summary,
                    supporting_observation_count=count,
                    supporting_submission_ids=ids,
                    time_window=time_window_label,
                    confidence=confidence,
                    affected_feature=None,
                    related_finding_ids=finding_ids,
                    suggested_review_priority=PRIORITY_MEDIUM,
                    comparison=growth_comparison,
                )
            )

        return tuple(insights)

    @staticmethod
    def _build_friction_insights(
        submissions: list[ResearchFeedbackSubmission],
        *,
        time_window_label: str,
        prior_submissions: list[ResearchFeedbackSubmission] | None = None,
    ) -> tuple[ResearchInsight, ...]:
        if not submissions:
            return ()

        confusing_counts = Counter(
            s.feature_helped_most
            for s in submissions
            if s.classification == "Confusing" or s.friction_area not in {"", "Nothing"}
        )
        friction_counts = Counter(
            s.friction_area for s in submissions if s.friction_area != "Nothing"
        )
        category_counts = Counter(
            s.classification
            for s in submissions
            if s.classification in CLASSIFICATION_CHOICES
        )

        most_confusing = (
            confusing_counts.most_common(1)[0][0] if confusing_counts else None
        )
        most_friction = (
            friction_counts.most_common(1)[0][0] if friction_counts else None
        )
        most_category = (
            category_counts.most_common(1)[0][0] if category_counts else None
        )

        fastest_growing: str | None = None
        growth_delta = 0
        if prior_submissions is not None:
            prior_friction = Counter(
                s.friction_area
                for s in prior_submissions
                if s.friction_area != "Nothing"
            )
            for area, current in friction_counts.items():
                delta = current - prior_friction.get(area, 0)
                if delta > growth_delta:
                    growth_delta = delta
                    fastest_growing = area

        insights: list[ResearchInsight] = []

        if most_confusing:
            confusing_subs = [
                s
                for s in submissions
                if s.feature_helped_most == most_confusing
                and (
                    s.classification == "Confusing"
                    or s.friction_area not in {"", "Nothing"}
                )
            ]
            insights.append(
                ResearchInsight(
                    family=INSIGHT_FAMILY_FRICTION,
                    title="Most Confusing Feature",
                    summary=(
                        f"'{most_confusing}' appears most often in confusion "
                        f"or friction signals ({len(confusing_subs)} observation(s))."
                    ),
                    supporting_observation_count=len(confusing_subs),
                    supporting_submission_ids=tuple(s.id for s in confusing_subs),
                    time_window=time_window_label,
                    confidence=ResearchInsightService._confidence(len(confusing_subs)),
                    affected_feature=most_confusing,
                    related_finding_ids=ResearchInsightService._related_findings(
                        tuple(s.id for s in confusing_subs)
                    ),
                    suggested_review_priority=ResearchInsightService._review_priority(
                        observation_count=len(confusing_subs),
                        friction_signal=True,
                    ),
                )
            )

        if most_friction:
            friction_subs = [s for s in submissions if s.friction_area == most_friction]
            insights.append(
                ResearchInsight(
                    family=INSIGHT_FAMILY_FRICTION,
                    title="Most Reported Friction",
                    summary=(
                        f"'{most_friction}' is the most reported friction area "
                        f"({len(friction_subs)} mention(s))."
                    ),
                    supporting_observation_count=len(friction_subs),
                    supporting_submission_ids=tuple(s.id for s in friction_subs),
                    time_window=time_window_label,
                    confidence=ResearchInsightService._confidence(len(friction_subs)),
                    affected_feature=most_friction,
                    related_finding_ids=ResearchInsightService._related_findings(
                        tuple(s.id for s in friction_subs)
                    ),
                    suggested_review_priority=ResearchInsightService._review_priority(
                        observation_count=len(friction_subs),
                        friction_signal=True,
                    ),
                )
            )

        if most_category:
            cat_subs = [s for s in submissions if s.classification == most_category]
            insights.append(
                ResearchInsight(
                    family=INSIGHT_FAMILY_FRICTION,
                    title="Most Selected Issue Category",
                    summary=(
                        f"'{most_category}' is the most common classification "
                        f"({len(cat_subs)} observation(s))."
                    ),
                    supporting_observation_count=len(cat_subs),
                    supporting_submission_ids=tuple(s.id for s in cat_subs),
                    time_window=time_window_label,
                    confidence=ResearchInsightService._confidence(len(cat_subs)),
                    affected_feature=None,
                    related_finding_ids=ResearchInsightService._related_findings(
                        tuple(s.id for s in cat_subs)
                    ),
                    suggested_review_priority=PRIORITY_MEDIUM,
                )
            )

        if fastest_growing and growth_delta > 0:
            growing_subs = [
                s for s in submissions if s.friction_area == fastest_growing
            ]
            insights.append(
                ResearchInsight(
                    family=INSIGHT_FAMILY_FRICTION,
                    title="Fastest Growing Concern",
                    summary=(
                        f"'{fastest_growing}' increased by {growth_delta} "
                        f"mention(s) compared to the prior window."
                    ),
                    supporting_observation_count=len(growing_subs),
                    supporting_submission_ids=tuple(s.id for s in growing_subs),
                    time_window=time_window_label,
                    confidence=ResearchInsightService._confidence(len(growing_subs)),
                    affected_feature=fastest_growing,
                    related_finding_ids=ResearchInsightService._related_findings(
                        tuple(s.id for s in growing_subs)
                    ),
                    suggested_review_priority=ResearchInsightService._review_priority(
                        observation_count=len(growing_subs),
                        friction_signal=True,
                        declining_signal=True,
                    ),
                )
            )

        return tuple(insights)

    @staticmethod
    def _build_trend_insights(
        submissions: list[ResearchFeedbackSubmission],
        *,
        time_window_label: str,
        prior_submissions: list[ResearchFeedbackSubmission],
        version_submissions: dict[str, list[ResearchFeedbackSubmission]] | None = None,
    ) -> tuple[ResearchInsight, ...]:
        insights: list[ResearchInsight] = []
        count = len(submissions)
        ids = ResearchInsightService._submission_ids(submissions)
        confidence = ResearchInsightService._confidence(count)

        weekly_delta = count - len(prior_submissions)
        insights.append(
            ResearchInsight(
                family=INSIGHT_FAMILY_TREND,
                title="Weekly Movement",
                summary=(
                    f"Submission volume changed by {weekly_delta:+d} "
                    f"({len(prior_submissions)} → {count})."
                ),
                supporting_observation_count=count,
                supporting_submission_ids=ids,
                time_window=time_window_label,
                confidence=confidence,
                affected_feature=None,
                related_finding_ids=ResearchInsightService._related_findings(ids),
                suggested_review_priority=PRIORITY_MEDIUM,
                comparison=InsightComparison(
                    label="Weekly submissions",
                    current_value=count,
                    previous_value=len(prior_submissions),
                    delta=weekly_delta,
                    comparison_type=COMPARISON_PREVIOUS_WEEK,
                ),
            )
        )

        if version_submissions and len(version_submissions) >= 2:
            versions = sorted(version_submissions.keys())
            current_v = versions[-1]
            prior_v = versions[-2]
            current_list = version_submissions[current_v]
            prior_list = version_submissions[prior_v]
            current_avg = ResearchInsightService._avg_score(
                [
                    EXPERIENCE_SCORES[s.experience_rating]
                    for s in current_list
                    if s.experience_rating in EXPERIENCE_SCORES
                ]
            )
            prior_avg = ResearchInsightService._avg_score(
                [
                    EXPERIENCE_SCORES[s.experience_rating]
                    for s in prior_list
                    if s.experience_rating in EXPERIENCE_SCORES
                ]
            )
            version_summary = (
                f"Version {current_v}: avg experience {current_avg}/5 "
                f"({len(current_list)} obs); version {prior_v}: "
                f"{prior_avg}/5 ({len(prior_list)} obs)."
            )
            insights.append(
                ResearchInsight(
                    family=INSIGHT_FAMILY_TREND,
                    title="Version Comparison",
                    summary=version_summary,
                    supporting_observation_count=len(current_list) + len(prior_list),
                    supporting_submission_ids=ResearchInsightService._submission_ids(
                        current_list + prior_list
                    ),
                    time_window=time_window_label,
                    confidence=ResearchInsightService._confidence(
                        len(current_list) + len(prior_list)
                    ),
                    affected_feature=None,
                    related_finding_ids=ResearchInsightService._related_findings(
                        ResearchInsightService._submission_ids(
                            current_list + prior_list
                        )
                    ),
                    suggested_review_priority=PRIORITY_MEDIUM,
                    comparison=InsightComparison(
                        label=f"Experience {current_v} vs {prior_v}",
                        current_value=current_avg,
                        previous_value=prior_avg,
                        delta=(
                            round(current_avg - prior_avg, 2)
                            if current_avg is not None and prior_avg is not None
                            else None
                        ),
                        comparison_type=COMPARISON_PREVIOUS_RELEASE,
                    ),
                )
            )

        recent_features = {s.feature_helped_most for s in submissions}
        prior_avg_by_feature: dict[str, list[float]] = {}
        for s in prior_submissions:
            score = EXPERIENCE_SCORES.get(s.experience_rating)
            if score is not None:
                prior_avg_by_feature.setdefault(s.feature_helped_most, []).append(score)

        improved: list[str] = []
        for feat in recent_features:
            recent_scores = [
                EXPERIENCE_SCORES[s.experience_rating]
                for s in submissions
                if s.feature_helped_most == feat
                and s.experience_rating in EXPERIENCE_SCORES
            ]
            prior_scores = prior_avg_by_feature.get(feat, [])
            if recent_scores and prior_scores:
                if sum(recent_scores) / len(recent_scores) > sum(prior_scores) / len(
                    prior_scores
                ):
                    improved.append(feat)

        if improved:
            improved_subs = [
                s for s in submissions if s.feature_helped_most in improved
            ]
            insights.append(
                ResearchInsight(
                    family=INSIGHT_FAMILY_TREND,
                    title="Feature Improvement",
                    summary=(f"Experience scores improved for: {', '.join(improved)}."),
                    supporting_observation_count=len(improved_subs),
                    supporting_submission_ids=tuple(s.id for s in improved_subs),
                    time_window=time_window_label,
                    confidence=ResearchInsightService._confidence(len(improved_subs)),
                    affected_feature=improved[0],
                    related_finding_ids=ResearchInsightService._related_findings(
                        tuple(s.id for s in improved_subs)
                    ),
                    suggested_review_priority=PRIORITY_LOW,
                )
            )

        declining_friction = Counter(
            s.friction_area for s in submissions if s.friction_area != "Nothing"
        )
        prior_friction = Counter(
            s.friction_area for s in prior_submissions if s.friction_area != "Nothing"
        )
        declining: list[str] = []
        for area, prior_count in prior_friction.items():
            current_count = declining_friction.get(area, 0)
            if prior_count > 0 and current_count < prior_count:
                declining.append(area)

        if declining:
            declining_subs = [
                s for s in prior_submissions if s.friction_area in declining
            ]
            insights.append(
                ResearchInsight(
                    family=INSIGHT_FAMILY_TREND,
                    title="Declining Issues",
                    summary=(
                        f"Friction mentions declined for: {', '.join(declining)}."
                    ),
                    supporting_observation_count=len(declining_subs),
                    supporting_submission_ids=tuple(s.id for s in declining_subs),
                    time_window=time_window_label,
                    confidence=ResearchInsightService._confidence(len(declining_subs)),
                    affected_feature=declining[0],
                    related_finding_ids=ResearchInsightService._related_findings(
                        tuple(s.id for s in declining_subs)
                    ),
                    suggested_review_priority=PRIORITY_LOW,
                )
            )

        return tuple(insights)

    @staticmethod
    def _build_release_insights(
        *,
        time_window_label: str,
        current_release: str,
        previous_release: str | None,
        filters: InsightFilters,
        as_of: date,
    ) -> tuple[ResearchInsight, ...]:
        window_end = datetime.combine(as_of + timedelta(days=1), datetime.min.time())
        current_subs = ResearchInsightService._fetch_submissions(
            filters,
            window_start=None,
            window_end=window_end,
            release_version=current_release,
        )
        if not current_subs:
            return ()

        ids = ResearchInsightService._submission_ids(current_subs)

        resolved = sum(
            1 for s in current_subs if s.workflow_status in {"released", "verified"}
        )
        new_findings = ResearchProductFinding.query.filter_by(status="new").count()
        verified_findings = ResearchProductFinding.query.filter_by(
            status="verified"
        ).count()
        introduced = sum(
            1
            for s in current_subs
            if s.workflow_status == "new" and s.classification in {"Bug", "Confusing"}
        )

        insights: list[ResearchInsight] = [
            ResearchInsight(
                family=INSIGHT_FAMILY_RELEASE,
                title="Findings Resolved",
                summary=(
                    f"{resolved} submission(s) in release {current_release} "
                    f"reached released or verified status."
                ),
                supporting_observation_count=resolved,
                supporting_submission_ids=tuple(
                    s.id
                    for s in current_subs
                    if s.workflow_status in {"released", "verified"}
                ),
                time_window=time_window_label,
                confidence=ResearchInsightService._confidence(resolved),
                affected_feature=None,
                related_finding_ids=tuple(
                    f.id
                    for f in ResearchProductFinding.query.filter(
                        ResearchProductFinding.status.in_(("released", "verified"))
                    ).all()
                ),
                suggested_review_priority=PRIORITY_LOW,
            ),
            ResearchInsight(
                family=INSIGHT_FAMILY_RELEASE,
                title="New Findings",
                summary=f"{new_findings} product finding(s) in new status.",
                supporting_observation_count=new_findings,
                supporting_submission_ids=(),
                time_window=time_window_label,
                confidence=ResearchInsightService._confidence(new_findings),
                affected_feature=None,
                related_finding_ids=tuple(
                    f.id
                    for f in ResearchProductFinding.query.filter_by(status="new").all()
                ),
                suggested_review_priority=PRIORITY_HIGH,
            ),
            ResearchInsight(
                family=INSIGHT_FAMILY_RELEASE,
                title="Verified Findings",
                summary=f"{verified_findings} product finding(s) verified.",
                supporting_observation_count=verified_findings,
                supporting_submission_ids=(),
                time_window=time_window_label,
                confidence=ResearchInsightService._confidence(verified_findings),
                affected_feature=None,
                related_finding_ids=tuple(
                    f.id
                    for f in ResearchProductFinding.query.filter_by(
                        status="verified"
                    ).all()
                ),
                suggested_review_priority=PRIORITY_LOW,
            ),
            ResearchInsight(
                family=INSIGHT_FAMILY_RELEASE,
                title="Issues Introduced",
                summary=(
                    f"{introduced} new bug or confusion submission(s) "
                    f"in release {current_release}."
                ),
                supporting_observation_count=introduced,
                supporting_submission_ids=tuple(
                    s.id
                    for s in current_subs
                    if s.workflow_status == "new"
                    and s.classification in {"Bug", "Confusing"}
                ),
                time_window=time_window_label,
                confidence=ResearchInsightService._confidence(introduced),
                affected_feature=None,
                related_finding_ids=ResearchInsightService._related_findings(ids),
                suggested_review_priority=ResearchInsightService._review_priority(
                    observation_count=introduced,
                    friction_signal=introduced > 0,
                ),
            ),
        ]

        if previous_release:
            prior_subs = ResearchInsightService._fetch_submissions(
                filters,
                window_start=None,
                window_end=window_end,
                release_version=previous_release,
            )
            current_avg = ResearchInsightService._avg_score(
                [
                    EXPERIENCE_SCORES[s.experience_rating]
                    for s in current_subs
                    if s.experience_rating in EXPERIENCE_SCORES
                ]
            )
            prior_avg = ResearchInsightService._avg_score(
                [
                    EXPERIENCE_SCORES[s.experience_rating]
                    for s in prior_subs
                    if s.experience_rating in EXPERIENCE_SCORES
                ]
            )
            insights = list(insights)
            insights.append(
                ResearchInsight(
                    family=INSIGHT_FAMILY_RELEASE,
                    title="Release Comparison",
                    summary=(
                        f"Release {current_release} avg experience "
                        f"{current_avg}/5 vs {previous_release} {prior_avg}/5."
                    ),
                    supporting_observation_count=len(current_subs) + len(prior_subs),
                    supporting_submission_ids=ResearchInsightService._submission_ids(
                        current_subs + prior_subs
                    ),
                    time_window=time_window_label,
                    confidence=ResearchInsightService._confidence(
                        len(current_subs) + len(prior_subs)
                    ),
                    affected_feature=None,
                    related_finding_ids=ResearchInsightService._related_findings(
                        ResearchInsightService._submission_ids(
                            current_subs + prior_subs
                        )
                    ),
                    suggested_review_priority=PRIORITY_MEDIUM,
                    comparison=InsightComparison(
                        label=f"Release {current_release} vs {previous_release}",
                        current_value=current_avg,
                        previous_value=prior_avg,
                        delta=(
                            round(current_avg - prior_avg, 2)
                            if current_avg is not None and prior_avg is not None
                            else None
                        ),
                        comparison_type=COMPARISON_PREVIOUS_RELEASE,
                    ),
                )
            )

        return tuple(insights)

    @staticmethod
    def _build_research_insights(
        submissions: list[ResearchFeedbackSubmission],
        *,
        time_window_label: str,
        window_start: datetime | None,
        window_end: datetime,
    ) -> tuple[ResearchInsight, ...]:
        if not submissions:
            return ()

        ids = ResearchInsightService._submission_ids(submissions)
        count = len(submissions)
        confidence = ResearchInsightService._confidence(count)
        finding_ids = ResearchInsightService._related_findings(ids)

        feature_counts = Counter(s.feature_helped_most for s in submissions)
        most_active = feature_counts.most_common(1)[0][0] if feature_counts else None

        user_counts = Counter(s.user_id for s in submissions)
        distribution_summary = (
            f"{len(user_counts)} contributor(s) produced {count} submission(s); "
            f"top contributor submitted {max(user_counts.values())} time(s)."
        )

        implemented = sum(
            1
            for s in submissions
            if s.workflow_status in {"implemented", "released", "verified"}
        )

        badge_query = ResearchContributorBadge.query
        if window_start is not None:
            badge_query = badge_query.filter(
                ResearchContributorBadge.awarded_at >= window_start
            )
        badge_query = badge_query.filter(
            ResearchContributorBadge.awarded_at < window_end
        )
        badges = badge_query.all()
        badge_counts = Counter(b.badge_slug for b in badges)
        badge_summary = (
            ", ".join(f"{slug}: {cnt}" for slug, cnt in badge_counts.most_common())
            if badge_counts
            else "No badges awarded in this window."
        )

        return (
            ResearchInsight(
                family=INSIGHT_FAMILY_RESEARCH,
                title="Most Active Feature",
                summary=(
                    f"'{most_active}' received the most positive feature mentions "
                    f"({feature_counts[most_active]} observation(s))."
                    if most_active
                    else "No feature mentions recorded."
                ),
                supporting_observation_count=feature_counts[most_active]
                if most_active
                else 0,
                supporting_submission_ids=tuple(
                    s.id for s in submissions if s.feature_helped_most == most_active
                )
                if most_active
                else (),
                time_window=time_window_label,
                confidence=ResearchInsightService._confidence(
                    feature_counts[most_active] if most_active else 0
                ),
                affected_feature=most_active,
                related_finding_ids=finding_ids,
                suggested_review_priority=PRIORITY_LOW,
            ),
            ResearchInsight(
                family=INSIGHT_FAMILY_RESEARCH,
                title="Contribution Distribution",
                summary=distribution_summary,
                supporting_observation_count=count,
                supporting_submission_ids=ids,
                time_window=time_window_label,
                confidence=confidence,
                affected_feature=None,
                related_finding_ids=finding_ids,
                suggested_review_priority=PRIORITY_MEDIUM,
            ),
            ResearchInsight(
                family=INSIGHT_FAMILY_RESEARCH,
                title="Implemented Contributions",
                summary=(
                    f"{implemented} submission(s) reached implemented, "
                    f"released, or verified status."
                ),
                supporting_observation_count=implemented,
                supporting_submission_ids=tuple(
                    s.id
                    for s in submissions
                    if s.workflow_status in {"implemented", "released", "verified"}
                ),
                time_window=time_window_label,
                confidence=ResearchInsightService._confidence(implemented),
                affected_feature=None,
                related_finding_ids=finding_ids,
                suggested_review_priority=PRIORITY_LOW,
            ),
            ResearchInsight(
                family=INSIGHT_FAMILY_RESEARCH,
                title="Badge Distribution",
                summary=badge_summary,
                supporting_observation_count=len(badges),
                supporting_submission_ids=(),
                time_window=time_window_label,
                confidence=ResearchInsightService._confidence(len(badges)),
                affected_feature=None,
                related_finding_ids=(),
                suggested_review_priority=PRIORITY_LOW,
            ),
        )

    @staticmethod
    def _stable_areas(
        submissions: list[ResearchFeedbackSubmission],
        prior_submissions: list[ResearchFeedbackSubmission],
    ) -> tuple[ResearchInsight, ...]:
        """Features with unchanged average experience between windows."""
        stable: list[str] = []
        for feat in FEATURE_CHOICES:
            current_scores = [
                EXPERIENCE_SCORES[s.experience_rating]
                for s in submissions
                if s.feature_helped_most == feat
                and s.experience_rating in EXPERIENCE_SCORES
            ]
            prior_scores = [
                EXPERIENCE_SCORES[s.experience_rating]
                for s in prior_submissions
                if s.feature_helped_most == feat
                and s.experience_rating in EXPERIENCE_SCORES
            ]
            if not current_scores or not prior_scores:
                continue
            current_avg = sum(current_scores) / len(current_scores)
            prior_avg = sum(prior_scores) / len(prior_scores)
            if abs(current_avg - prior_avg) < 0.25:
                stable.append(feat)

        if not stable:
            return ()

        stable_subs = [s for s in submissions if s.feature_helped_most in stable]
        return (
            ResearchInsight(
                family=INSIGHT_FAMILY_TREND,
                title="Stable Areas",
                summary=(
                    f"Experience scores remained stable for: {', '.join(stable)}."
                ),
                supporting_observation_count=len(stable_subs),
                supporting_submission_ids=tuple(s.id for s in stable_subs),
                time_window="comparison",
                confidence=ResearchInsightService._confidence(len(stable_subs)),
                affected_feature=stable[0],
                related_finding_ids=ResearchInsightService._related_findings(
                    tuple(s.id for s in stable_subs)
                ),
                suggested_review_priority=PRIORITY_LOW,
            ),
        )

    @staticmethod
    def _legacy_snapshot(
        submissions: list[ResearchFeedbackSubmission],
        *,
        as_of: date,
    ) -> ResearchInsightsLegacy:
        feature_counts = Counter(s.feature_helped_most for s in submissions)
        friction_counts = Counter(
            s.friction_area for s in submissions if s.friction_area != "Nothing"
        )
        suggestion_counts = Counter(
            s.classification
            for s in submissions
            if s.classification in CLASSIFICATION_CHOICES
        )

        participation_trend: list[tuple[str, int]] = []
        contribution_growth: list[tuple[str, int]] = []
        for offset in range(6, -1, -1):
            day = as_of - timedelta(days=offset)
            start = datetime.combine(day, datetime.min.time())
            end = datetime.combine(day + timedelta(days=1), datetime.min.time())
            day_subs = [s for s in submissions if start <= s.submitted_at < end]
            label = day.isoformat()
            participation_trend.append((label, len({s.user_id for s in day_subs})))
            contribution_growth.append((label, len(day_subs)))

        week_ago = datetime.combine(as_of - timedelta(days=7), datetime.min.time())
        recent_badges = (
            ResearchContributorBadge.query.filter(
                ResearchContributorBadge.awarded_at >= week_ago
            )
            .order_by(ResearchContributorBadge.awarded_at.desc())
            .limit(10)
            .all()
        )

        return ResearchInsightsLegacy(
            most_common_feature=(
                feature_counts.most_common(1)[0][0] if feature_counts else None
            ),
            most_common_friction=(
                friction_counts.most_common(1)[0][0] if friction_counts else None
            ),
            most_common_suggestion_category=(
                suggestion_counts.most_common(1)[0][0] if suggestion_counts else None
            ),
            participation_trend=tuple(participation_trend),
            contribution_growth=tuple(contribution_growth),
            recently_awarded_badges=tuple(recent_badges),
        )

    @staticmethod
    def generate_insights(
        filters: InsightFilters | None = None,
        *,
        time_window: str = TIME_WINDOW_7_DAYS,
        as_of: date | None = None,
        custom_date_from: date | None = None,
        custom_date_to: date | None = None,
        current_release: str | None = None,
        previous_release: str | None = None,
    ) -> InsightEngineResult:
        """Generate objective product insights from research observations.

        Pure aggregation — no AI, no product decisions, no educational writes.
        """
        filters = filters or InsightFilters()
        as_of = as_of or date.today()
        time_window_label = TIME_WINDOW_LABELS.get(time_window, time_window)

        window_start, window_end = ResearchInsightService._window_bounds(
            time_window,
            as_of=as_of,
            custom_date_from=custom_date_from,
            custom_date_to=custom_date_to,
            current_release=current_release,
            previous_release=previous_release,
        )

        release_version: str | None = None
        if time_window == TIME_WINDOW_CURRENT_RELEASE:
            release_version = current_release or PRODUCT_VERSION
        elif time_window == TIME_WINDOW_PREVIOUS_RELEASE:
            release_version = previous_release
            if release_version is None:
                all_versions = (
                    db.session.query(ResearchFeedbackSubmission.product_version)
                    .distinct()
                    .order_by(ResearchFeedbackSubmission.product_version)
                    .all()
                )
                versions = [v[0] for v in all_versions if v[0]]
                if len(versions) >= 2:
                    release_version = versions[-2]
                elif versions:
                    release_version = versions[0]

        submissions = ResearchInsightService._fetch_submissions(
            filters,
            window_start=window_start,
            window_end=window_end,
            release_version=release_version,
        )

        (
            current_start,
            current_end,
            previous_start,
            previous_end,
        ) = ResearchInsightService._comparison_bounds(time_window, as_of=as_of)

        prior_submissions = ResearchInsightService._fetch_submissions(
            filters,
            window_start=previous_start,
            window_end=previous_end,
            release_version=release_version,
        )

        version_groups: dict[str, list[ResearchFeedbackSubmission]] = {}
        for sub in ResearchFeedbackSubmission.query.all():
            version_groups.setdefault(sub.product_version, []).append(sub)

        experience = ResearchInsightService._build_experience_insights(
            submissions,
            time_window_label=time_window_label,
            comparison_submissions=prior_submissions,
        )
        behaviour = ResearchInsightService._build_behaviour_insights(
            submissions,
            time_window_label=time_window_label,
            as_of=as_of,
            comparison_submissions=prior_submissions,
        )
        friction = ResearchInsightService._build_friction_insights(
            submissions,
            time_window_label=time_window_label,
            prior_submissions=prior_submissions,
        )
        trend = ResearchInsightService._build_trend_insights(
            submissions,
            time_window_label=time_window_label,
            prior_submissions=prior_submissions,
            version_submissions=version_groups if len(version_groups) >= 2 else None,
        )
        release = ResearchInsightService._build_release_insights(
            time_window_label=time_window_label,
            current_release=current_release or PRODUCT_VERSION,
            previous_release=previous_release,
            filters=filters,
            as_of=as_of,
        )
        research = ResearchInsightService._build_research_insights(
            submissions,
            time_window_label=time_window_label,
            window_start=window_start,
            window_end=window_end,
        )
        stable = ResearchInsightService._stable_areas(submissions, prior_submissions)

        all_insights = experience + behaviour + friction + trend + release + research

        comparisons = tuple(
            i.comparison for i in all_insights if i.comparison is not None
        )

        emerging = tuple(i for i in friction if "Growing" in i.title)
        improved = tuple(i for i in trend if "Improvement" in i.title)
        top_trends = tuple(
            i for i in trend if i.title in {"Weekly Movement", "Version Comparison"}
        )

        return InsightEngineResult(
            time_window=time_window,
            time_window_label=time_window_label,
            filters=filters,
            insights=all_insights,
            top_trends=top_trends,
            emerging_concerns=emerging,
            most_improved_areas=improved,
            stable_areas=stable,
            participation=tuple(
                i for i in behaviour if i.family == INSIGHT_FAMILY_BEHAVIOUR
            ),
            release_comparison=tuple(
                i for i in release if "Release" in i.title or "Findings" in i.title
            ),
            comparisons=comparisons,
            legacy=ResearchInsightService._legacy_snapshot(submissions, as_of=as_of),
        )

    @staticmethod
    def get_legacy_insights(
        filters: InsightFilters | None = None,
        *,
        as_of: date | None = None,
    ) -> ResearchInsightsLegacy:
        """Return RIP-003-compatible insight snapshot."""
        as_of = as_of or date.today()
        filters = filters or InsightFilters()
        window_end = datetime.combine(as_of + timedelta(days=1), datetime.min.time())
        submissions = ResearchInsightService._fetch_submissions(
            filters,
            window_start=None,
            window_end=window_end,
        )
        return ResearchInsightService._legacy_snapshot(submissions, as_of=as_of)
