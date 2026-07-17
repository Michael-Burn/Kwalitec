"""Operational Health service (V1SP-001C).

Assembles deterministic Founder operational insights from existing Version 1
data only. Every rule is a plain count with an explainable definition —
no weighting, scoring, ranking, forecasting, or educational intelligence.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta

from flask import url_for
from sqlalchemy import func

from app.extensions import db
from app.founder.dashboard.dto.operational_health import (
    HealthyActivityMetric,
    OperationalHealthPage,
    OperationalInsightCard,
    TrendSeries,
)
from app.models.learning import StudyAttempt
from app.models.mission import Mission
from app.models.research_feedback import ResearchFeedbackSubmission
from app.models.study_plan import StudyPlan
from app.models.vision_journal import (
    VisionEntry,
    VisionEntryPromotion,
    VisionEntryStatusTransition,
)

TIMEZONE_POLICY = "Calendar day (server local date)"

# Deterministic thresholds (documented in release report).
INACTIVE_DAYS = 7
PROLONGED_INACTIVE_DAYS = 14
HELP_SEEKING_MIN = 2
REPEATED_FEEDBACK_MIN = 3
NEGATIVE_EXPERIENCE = frozenset({"Frustrating", "Poor"})
HELP_CLASSIFICATIONS = frozenset({"Question", "Confusing", "Bug"})
TRIAGE_STATUSES = frozenset({"new", "clarification_requested"})
TREND_DAYS = 7


@dataclass(frozen=True)
class _UserActivity:
    """Last observed study date and whether any session ever completed."""

    user_id: int
    last_activity: date | None
    has_started: bool


class OperationalHealthService:
    """Build the Founder Operational Health decision page."""

    def build_page(self, *, on_date: date | None = None) -> OperationalHealthPage:
        """Assemble Needs Attention, Healthy Activity, and Trends.

        Args:
            on_date: Anchor calendar day (defaults to today). Injected for tests.

        Returns:
            OperationalHealthPage ready for template rendering.
        """
        today = on_date or date.today()
        now = datetime.now(UTC)

        needs = self._needs_attention(today)
        healthy = self._healthy_activity(today)
        trends = self._trends(today)

        return OperationalHealthPage(
            refreshed_at=now.strftime("%Y-%m-%d %H:%M UTC"),
            timezone_policy=TIMEZONE_POLICY,
            needs_attention=needs,
            healthy_activity=healthy,
            trends=trends,
            attention_total=sum(card.count for card in needs),
        )

    # ── Needs Attention ───────────────────────────────────────────────────

    def _needs_attention(self, today: date) -> tuple[OperationalInsightCard, ...]:
        cards: list[OperationalInsightCard] = []
        cards.extend(self._student_activity_insights(today))
        cards.extend(self._engagement_insights())
        cards.extend(self._product_ops_insights())
        return tuple(card for card in cards if card.count > 0)

    def _student_activity_insights(
        self, today: date
    ) -> list[OperationalInsightCard]:
        activity = self._user_activity_map()
        plan_users = self._users_with_active_plans()
        never_started = self._never_started_plan_users(activity)
        inactive_7 = 0
        prolonged = 0
        for user_id in plan_users:
            info = activity.get(user_id)
            if info is None or not info.has_started:
                continue
            assert info.last_activity is not None
            gap = (today - info.last_activity).days
            if gap >= INACTIVE_DAYS:
                inactive_7 += 1
            if gap >= PROLONGED_INACTIVE_DAYS:
                prolonged += 1

        revision_idle = self._revision_without_sessions_count()

        cards: list[OperationalInsightCard] = []
        if inactive_7:
            cards.append(
                OperationalInsightCard(
                    rule_id="no_study_activity_7d",
                    group="Student Activity",
                    title="No study activity for 7+ days",
                    count=inactive_7,
                    explanation=(
                        f"{inactive_7} learner(s) with an active study plan have "
                        f"not completed a study session for {INACTIVE_DAYS}+ days."
                    ),
                    why_it_matters=(
                        "Prolonged silence after starting reduces Alpha signal "
                        "quality and may indicate friction."
                    ),
                    primary_action_label="Open Participants",
                    href=url_for("founder_dashboard.participants"),
                )
            )
        if never_started:
            cards.append(
                OperationalInsightCard(
                    rule_id="plan_never_started",
                    group="Student Activity",
                    title="Study plan created but never started",
                    count=never_started,
                    explanation=(
                        f"{never_started} learner(s) have a non-archived study "
                        "plan with no completed study session or recorded attempt."
                    ),
                    why_it_matters=(
                        "Plans without a first session never generate learning "
                        "or Product Check-in evidence."
                    ),
                    primary_action_label="Open Participants",
                    href=url_for("founder_dashboard.participants"),
                )
            )
        if prolonged:
            cards.append(
                OperationalInsightCard(
                    rule_id="prolonged_inactivity",
                    group="Student Activity",
                    title="Active plan with prolonged inactivity",
                    count=prolonged,
                    explanation=(
                        f"{prolonged} learner(s) started studying but have been "
                        f"inactive for {PROLONGED_INACTIVE_DAYS}+ days while "
                        "keeping an active plan."
                    ),
                    why_it_matters=(
                        "Long gaps after a start often mean drop-off or a "
                        "product obstacle worth reviewing."
                    ),
                    primary_action_label="Open Participants",
                    href=url_for("founder_dashboard.participants"),
                )
            )
        if revision_idle:
            cards.append(
                OperationalInsightCard(
                    rule_id="revision_no_sessions",
                    group="Student Activity",
                    title="Revision mode with no revision sessions",
                    count=revision_idle,
                    explanation=(
                        f"{revision_idle} active plan(s) entered Revision "
                        "(syllabus complete) but have no completed revision "
                        "sessions since entry."
                    ),
                    why_it_matters=(
                        "Syllabus completion without revision activity leaves "
                        "the Version 1 lifecycle unfinished."
                    ),
                    primary_action_label="Open Participants",
                    href=url_for("founder_dashboard.participants"),
                )
            )
        return cards

    def _engagement_insights(self) -> list[OperationalInsightCard]:
        help_count = self._help_seeking_checkin_count()
        negative_users = self._consecutive_negative_sentiment_users()
        repeated_users = self._repeated_feedback_users()

        cards: list[OperationalInsightCard] = []
        if help_count >= HELP_SEEKING_MIN:
            cards.append(
                OperationalInsightCard(
                    rule_id="help_seeking_checkins",
                    group="Engagement",
                    title="Product Check-ins requesting help",
                    count=help_count,
                    explanation=(
                        f"{help_count} open Product Check-in(s) classified as "
                        "Question, Confusing, or Bug still await triage."
                    ),
                    why_it_matters=(
                        "Help-seeking check-ins are direct product friction "
                        "signals for Internal Alpha."
                    ),
                    primary_action_label="Review Feedback",
                    href=url_for("founder_dashboard.feedback", status="new"),
                )
            )
        if negative_users:
            cards.append(
                OperationalInsightCard(
                    rule_id="consecutive_negative_sentiment",
                    group="Engagement",
                    title="Consecutive negative sentiment",
                    count=negative_users,
                    explanation=(
                        f"{negative_users} learner(s) recorded Frustrating or "
                        "Poor on their two most recent Product Check-ins."
                    ),
                    why_it_matters=(
                        "Repeated negative experience ratings indicate "
                        "unresolved product pain."
                    ),
                    primary_action_label="Review Feedback",
                    href=url_for("founder_dashboard.feedback"),
                )
            )
        if repeated_users:
            cards.append(
                OperationalInsightCard(
                    rule_id="repeated_feedback",
                    group="Engagement",
                    title="Repeated feedback from the same learner",
                    count=repeated_users,
                    explanation=(
                        f"{repeated_users} learner(s) have submitted "
                        f"{REPEATED_FEEDBACK_MIN}+ Product Check-ins."
                    ),
                    why_it_matters=(
                        "Heavy contributors often surface recurring themes "
                        "worth recognising or investigating."
                    ),
                    primary_action_label="Open Participants",
                    href=url_for("founder_dashboard.participants"),
                )
            )
        return cards

    def _product_ops_insights(self) -> list[OperationalInsightCard]:
        awaiting_review = (
            db.session.query(
                func.count(func.distinct(ResearchFeedbackSubmission.user_id))
            )
            .filter(ResearchFeedbackSubmission.workflow_status == "new")
            .scalar()
            or 0
        )
        awaiting_triage = (
            db.session.query(func.count(ResearchFeedbackSubmission.id))
            .filter(ResearchFeedbackSubmission.workflow_status.in_(TRIAGE_STATUSES))
            .scalar()
            or 0
        )
        promoted_unresearched = self._promoted_vision_not_researched()

        cards: list[OperationalInsightCard] = []
        if awaiting_review:
            cards.append(
                OperationalInsightCard(
                    rule_id="alpha_awaiting_review",
                    group="Product Operations",
                    title="Internal Alpha participants awaiting review",
                    count=awaiting_review,
                    explanation=(
                        f"{awaiting_review} participant(s) have Product "
                        "Check-in(s) still in workflow status New."
                    ),
                    why_it_matters=(
                        "Unreviewed Alpha feedback stalls the research loop "
                        "and contributor recognition."
                    ),
                    primary_action_label="Open Internal Alpha",
                    href=url_for("founder_dashboard.internal_alpha"),
                )
            )
        if awaiting_triage:
            cards.append(
                OperationalInsightCard(
                    rule_id="feedback_awaiting_triage",
                    group="Product Operations",
                    title="Feedback awaiting triage",
                    count=awaiting_triage,
                    explanation=(
                        f"{awaiting_triage} submission(s) are New or "
                        "Clarification Requested."
                    ),
                    why_it_matters=(
                        "Triage backlog is the Founder's primary daily "
                        "operational queue."
                    ),
                    primary_action_label="Review Feedback",
                    href=url_for("founder_dashboard.feedback", status="new"),
                )
            )
        if promoted_unresearched:
            cards.append(
                OperationalInsightCard(
                    rule_id="vision_promoted_not_researched",
                    group="Product Operations",
                    title="Vision entries promoted but not researched",
                    count=promoted_unresearched,
                    explanation=(
                        f"{promoted_unresearched} Vision Journal entr(y/ies) "
                        "have a promotion placeholder but no Research status "
                        "transition in their history."
                    ),
                    why_it_matters=(
                        "Promotions that skip Research lose the intended "
                        "strategic validation step before development."
                    ),
                    primary_action_label="View Vision Journal",
                    href=url_for("founder_dashboard.vision_journal"),
                )
            )
        # Release task due dates are not modelled in Version 1 — omitted.
        return cards

    # ── Healthy Activity ──────────────────────────────────────────────────

    def _healthy_activity(self, today: date) -> tuple[HealthyActivityMetric, ...]:
        week_start = today - timedelta(days=6)

        active_today = self._active_learners_on(today)
        sessions_week = self._completed_missions_between(week_start, today)
        revision_week = self._revision_sessions_between(week_start, today)
        missions_week = sessions_week
        vision_week = (
            db.session.query(func.count(VisionEntry.id))
            .filter(
                VisionEntry.deleted_at.is_(None),
                VisionEntry.created_at
                >= datetime.combine(week_start, datetime.min.time()),
            )
            .scalar()
            or 0
        )
        feedback_week = (
            db.session.query(func.count(ResearchFeedbackSubmission.id))
            .filter(
                ResearchFeedbackSubmission.submitted_at
                >= datetime.combine(week_start, datetime.min.time()),
            )
            .scalar()
            or 0
        )
        completed_plans = (
            db.session.query(func.count(StudyPlan.id))
            .filter(
                StudyPlan.revision_entered_at.isnot(None),
                StudyPlan.revision_entered_at
                >= datetime.combine(week_start, datetime.min.time()),
                StudyPlan.archived.is_(False),
            )
            .scalar()
            or 0
        )

        return (
            HealthyActivityMetric(
                metric_id="active_learners_today",
                label="Active learners today",
                value=active_today,
                explanation=(
                    "Distinct learners with a completed study session or "
                    "recorded study attempt today."
                ),
                href=url_for("founder_dashboard.participants"),
            ),
            HealthyActivityMetric(
                metric_id="study_sessions_week",
                label="Study sessions completed this week",
                value=sessions_week,
                explanation=(
                    "Completed missions in the last 7 calendar days "
                    "(including today)."
                ),
            ),
            HealthyActivityMetric(
                metric_id="revision_sessions_week",
                label="Revision sessions completed",
                value=revision_week,
                explanation=(
                    "Completed missions on or after Revision entry within "
                    "the last 7 days."
                ),
            ),
            HealthyActivityMetric(
                metric_id="missions_completed_week",
                label="Missions completed",
                value=missions_week,
                explanation=(
                    "Same window as study sessions — daily mission "
                    "completions across Alpha learners."
                ),
            ),
            HealthyActivityMetric(
                metric_id="vision_entries_week",
                label="New Vision Journal entries",
                value=vision_week,
                explanation="Vision entries created in the last 7 days.",
                href=url_for("founder_dashboard.vision_journal"),
            ),
            HealthyActivityMetric(
                metric_id="alpha_feedback_week",
                label="New Internal Alpha feedback",
                value=feedback_week,
                explanation="Product Check-ins submitted in the last 7 days.",
                href=url_for("founder_dashboard.internal_alpha"),
            ),
            HealthyActivityMetric(
                metric_id="plans_completed_week",
                label="Recently completed study plans",
                value=completed_plans,
                explanation=(
                    "Active plans that entered Revision (syllabus complete) "
                    "in the last 7 days."
                ),
            ),
        )

    # ── Trends ────────────────────────────────────────────────────────────

    def _trends(self, today: date) -> tuple[TrendSeries, ...]:
        day_offsets = range(TREND_DAYS - 1, -1, -1)
        days = [today - timedelta(days=offset) for offset in day_offsets]
        day_labels = tuple(d.strftime("%a %d") for d in days)

        study_by_day = self._completed_missions_by_day(days[0], today)
        revision_by_day = self._revision_sessions_by_day(days[0], today)
        feedback_by_day = self._feedback_by_day(days[0], today)
        learners_by_day = self._active_learners_by_day(days[0], today)
        vision_by_day = self._vision_entries_by_day(days[0], today)

        study_vals = tuple(study_by_day.get(d, 0) for d in days)
        revision_vals = tuple(revision_by_day.get(d, 0) for d in days)
        feedback_vals = tuple(feedback_by_day.get(d, 0) for d in days)
        learner_vals = tuple(learners_by_day.get(d, 0) for d in days)
        vision_vals = tuple(vision_by_day.get(d, 0) for d in days)
        # Cumulative Vision Journal growth over the window.
        vision_growth: list[int] = []
        running = 0
        for v in vision_vals:
            running += v
            vision_growth.append(running)

        return (
            TrendSeries(
                series_id="daily_study_sessions",
                label="Daily study sessions (7 days)",
                labels=day_labels,
                values=study_vals,
                summary=self._trend_summary("study sessions", study_vals, days),
            ),
            TrendSeries(
                series_id="revision_activity",
                label="Revision activity (7 days)",
                labels=day_labels,
                values=revision_vals,
                summary=self._trend_summary(
                    "revision sessions", revision_vals, days
                ),
            ),
            TrendSeries(
                series_id="feedback_volume",
                label="Feedback volume (7 days)",
                labels=day_labels,
                values=feedback_vals,
                summary=self._trend_summary(
                    "Product Check-ins", feedback_vals, days
                ),
            ),
            TrendSeries(
                series_id="active_learners",
                label="Active learners (7 days)",
                labels=day_labels,
                values=learner_vals,
                summary=self._trend_summary(
                    "active learners", learner_vals, days
                ),
            ),
            TrendSeries(
                series_id="product_checkins",
                label="Product Check-ins (7 days)",
                labels=day_labels,
                values=feedback_vals,
                summary=self._trend_summary(
                    "Product Check-ins", feedback_vals, days
                ),
            ),
            TrendSeries(
                series_id="vision_growth",
                label="Vision Journal growth (7 days)",
                labels=day_labels,
                values=tuple(vision_growth),
                summary=(
                    f"Cumulative new Vision entries over 7 days: "
                    f"{vision_growth[-1] if vision_growth else 0} "
                    f"(daily new: {', '.join(str(v) for v in vision_vals)})."
                ),
            ),
        )

    @staticmethod
    def _trend_summary(
        noun: str, values: tuple[int, ...], days: list[date]
    ) -> str:
        total = sum(values)
        peak = max(values) if values else 0
        peak_day = days[values.index(peak)].strftime("%a %d") if values else "—"
        return (
            f"{total} {noun} across 7 days; peak {peak} on {peak_day}; "
            f"daily counts: {', '.join(str(v) for v in values)}."
        )

    # ── Query helpers ─────────────────────────────────────────────────────

    def _user_activity_map(self) -> dict[int, _UserActivity]:
        """Aggregate last study activity per user (missions + attempts)."""
        mission_rows = (
            db.session.query(
                Mission.user_id,
                func.max(Mission.mission_date).label("last_date"),
                func.count(Mission.id).label("cnt"),
            )
            .filter(Mission.status == "Completed")
            .group_by(Mission.user_id)
            .all()
        )
        attempt_rows = (
            db.session.query(
                StudyAttempt.user_id,
                func.max(StudyAttempt.study_date).label("last_date"),
                func.count(StudyAttempt.id).label("cnt"),
            )
            .group_by(StudyAttempt.user_id)
            .all()
        )

        last_dates: dict[int, date] = {}
        started: set[int] = set()
        for user_id, last_date, cnt in mission_rows:
            if cnt:
                started.add(user_id)
            if last_date is not None:
                last_dates[user_id] = last_date
        for user_id, last_date, cnt in attempt_rows:
            if cnt:
                started.add(user_id)
            if last_date is None:
                continue
            prev = last_dates.get(user_id)
            if prev is None or last_date > prev:
                last_dates[user_id] = last_date

        result: dict[int, _UserActivity] = {}
        for user_id in started | set(last_dates):
            result[user_id] = _UserActivity(
                user_id=user_id,
                last_activity=last_dates.get(user_id),
                has_started=user_id in started,
            )
        return result

    @staticmethod
    def _users_with_active_plans() -> set[int]:
        rows = (
            db.session.query(StudyPlan.user_id)
            .filter(
                StudyPlan.active.is_(True),
                StudyPlan.archived.is_(False),
            )
            .distinct()
            .all()
        )
        return {row[0] for row in rows}

    def _never_started_plan_users(
        self, activity: dict[int, _UserActivity]
    ) -> int:
        """Count learners with a non-archived plan and zero study evidence."""
        plan_users = (
            db.session.query(StudyPlan.user_id)
            .filter(StudyPlan.archived.is_(False))
            .distinct()
            .all()
        )
        count = 0
        for (user_id,) in plan_users:
            info = activity.get(user_id)
            if info is None or not info.has_started:
                count += 1
        return count

    @staticmethod
    def _revision_without_sessions_count() -> int:
        """Active plans in Revision with no completed mission since entry."""
        plans = (
            StudyPlan.query.filter(
                StudyPlan.active.is_(True),
                StudyPlan.archived.is_(False),
                StudyPlan.revision_entered_at.isnot(None),
            )
            .all()
        )
        idle = 0
        for plan in plans:
            entered = plan.revision_entered_at
            entered_date = entered.date() if isinstance(entered, datetime) else entered
            completed = (
                db.session.query(func.count(Mission.id))
                .filter(
                    Mission.user_id == plan.user_id,
                    Mission.study_plan_id == plan.id,
                    Mission.mission_date >= entered_date,
                    Mission.status == "Completed",
                )
                .scalar()
                or 0
            )
            if completed == 0:
                idle += 1
        return idle

    @staticmethod
    def _help_seeking_checkin_count() -> int:
        return (
            db.session.query(func.count(ResearchFeedbackSubmission.id))
            .filter(
                ResearchFeedbackSubmission.classification.in_(HELP_CLASSIFICATIONS),
                ResearchFeedbackSubmission.workflow_status.in_(
                    {"new", "under_review", "clarification_requested"}
                ),
            )
            .scalar()
            or 0
        )

    @staticmethod
    def _consecutive_negative_sentiment_users() -> int:
        """Users whose two most recent check-ins are both Frustrating/Poor."""
        rows = (
            db.session.query(
                ResearchFeedbackSubmission.user_id,
                ResearchFeedbackSubmission.experience_rating,
                ResearchFeedbackSubmission.submitted_at,
            )
            .order_by(
                ResearchFeedbackSubmission.user_id.asc(),
                ResearchFeedbackSubmission.submitted_at.desc(),
            )
            .all()
        )
        by_user: dict[int, list[str]] = defaultdict(list)
        for user_id, rating, _submitted in rows:
            if len(by_user[user_id]) >= 2:
                continue
            by_user[user_id].append(rating)

        return sum(
            1
            for ratings in by_user.values()
            if len(ratings) >= 2
            and ratings[0] in NEGATIVE_EXPERIENCE
            and ratings[1] in NEGATIVE_EXPERIENCE
        )

    @staticmethod
    def _repeated_feedback_users() -> int:
        rows = (
            db.session.query(
                ResearchFeedbackSubmission.user_id,
                func.count(ResearchFeedbackSubmission.id),
            )
            .group_by(ResearchFeedbackSubmission.user_id)
            .having(
                func.count(ResearchFeedbackSubmission.id) >= REPEATED_FEEDBACK_MIN
            )
            .all()
        )
        return len(rows)

    @staticmethod
    def _promoted_vision_not_researched() -> int:
        """Count promoted entries that never entered Research status.

        Promotion placeholders may jump straight to In Development. This rule
        surfaces promotions that skipped the Research stage in journal history.
        """
        researched = (
            db.session.query(VisionEntryStatusTransition.entry_id)
            .filter(VisionEntryStatusTransition.to_status == "research")
            .distinct()
        )
        return (
            db.session.query(func.count(func.distinct(VisionEntry.id)))
            .join(
                VisionEntryPromotion,
                VisionEntryPromotion.entry_id == VisionEntry.id,
            )
            .filter(
                VisionEntry.deleted_at.is_(None),
                VisionEntry.status.notin_(("rejected", "archived")),
                ~VisionEntry.id.in_(researched),
            )
            .scalar()
            or 0
        )

    @staticmethod
    def _active_learners_on(day: date) -> int:
        mission_users = {
            row[0]
            for row in db.session.query(Mission.user_id)
            .filter(Mission.mission_date == day, Mission.status == "Completed")
            .distinct()
            .all()
        }
        attempt_users = {
            row[0]
            for row in db.session.query(StudyAttempt.user_id)
            .filter(StudyAttempt.study_date == day)
            .distinct()
            .all()
        }
        return len(mission_users | attempt_users)

    @staticmethod
    def _completed_missions_between(start: date, end: date) -> int:
        return (
            db.session.query(func.count(Mission.id))
            .filter(
                Mission.status == "Completed",
                Mission.mission_date >= start,
                Mission.mission_date <= end,
            )
            .scalar()
            or 0
        )

    @staticmethod
    def _revision_sessions_between(start: date, end: date) -> int:
        """Completed missions on/after plan Revision entry within the window."""
        return (
            db.session.query(func.count(Mission.id))
            .join(StudyPlan, StudyPlan.id == Mission.study_plan_id)
            .filter(
                Mission.status == "Completed",
                Mission.mission_date >= start,
                Mission.mission_date <= end,
                StudyPlan.revision_entered_at.isnot(None),
                Mission.mission_date
                >= func.date(StudyPlan.revision_entered_at),
            )
            .scalar()
            or 0
        )

    @staticmethod
    def _completed_missions_by_day(
        start: date, end: date
    ) -> dict[date, int]:
        rows = (
            db.session.query(Mission.mission_date, func.count(Mission.id))
            .filter(
                Mission.status == "Completed",
                Mission.mission_date >= start,
                Mission.mission_date <= end,
            )
            .group_by(Mission.mission_date)
            .all()
        )
        return {row[0]: int(row[1]) for row in rows}

    @staticmethod
    def _revision_sessions_by_day(start: date, end: date) -> dict[date, int]:
        rows = (
            db.session.query(Mission.mission_date, func.count(Mission.id))
            .join(StudyPlan, StudyPlan.id == Mission.study_plan_id)
            .filter(
                Mission.status == "Completed",
                Mission.mission_date >= start,
                Mission.mission_date <= end,
                StudyPlan.revision_entered_at.isnot(None),
                Mission.mission_date
                >= func.date(StudyPlan.revision_entered_at),
            )
            .group_by(Mission.mission_date)
            .all()
        )
        return {row[0]: int(row[1]) for row in rows}

    @staticmethod
    def _feedback_by_day(start: date, end: date) -> dict[date, int]:
        start_dt = datetime.combine(start, datetime.min.time())
        end_dt = datetime.combine(end + timedelta(days=1), datetime.min.time())
        rows = (
            db.session.query(
                func.date(ResearchFeedbackSubmission.submitted_at),
                func.count(ResearchFeedbackSubmission.id),
            )
            .filter(
                ResearchFeedbackSubmission.submitted_at >= start_dt,
                ResearchFeedbackSubmission.submitted_at < end_dt,
            )
            .group_by(func.date(ResearchFeedbackSubmission.submitted_at))
            .all()
        )
        result: dict[date, int] = {}
        for raw_day, cnt in rows:
            day = _as_date(raw_day)
            if day is not None:
                result[day] = int(cnt)
        return result

    def _active_learners_by_day(
        self, start: date, end: date
    ) -> dict[date, int]:
        mission_rows = (
            db.session.query(Mission.mission_date, Mission.user_id)
            .filter(
                Mission.status == "Completed",
                Mission.mission_date >= start,
                Mission.mission_date <= end,
            )
            .distinct()
            .all()
        )
        attempt_rows = (
            db.session.query(StudyAttempt.study_date, StudyAttempt.user_id)
            .filter(
                StudyAttempt.study_date >= start,
                StudyAttempt.study_date <= end,
            )
            .distinct()
            .all()
        )
        by_day: dict[date, set[int]] = defaultdict(set)
        for day, user_id in mission_rows:
            by_day[day].add(user_id)
        for day, user_id in attempt_rows:
            by_day[day].add(user_id)
        return {day: len(users) for day, users in by_day.items()}

    @staticmethod
    def _vision_entries_by_day(start: date, end: date) -> dict[date, int]:
        start_dt = datetime.combine(start, datetime.min.time())
        end_dt = datetime.combine(end + timedelta(days=1), datetime.min.time())
        rows = (
            db.session.query(
                func.date(VisionEntry.created_at),
                func.count(VisionEntry.id),
            )
            .filter(
                VisionEntry.deleted_at.is_(None),
                VisionEntry.created_at >= start_dt,
                VisionEntry.created_at < end_dt,
            )
            .group_by(func.date(VisionEntry.created_at))
            .all()
        )
        result: dict[date, int] = {}
        for raw_day, cnt in rows:
            day = _as_date(raw_day)
            if day is not None:
                result[day] = int(cnt)
        return result


def _as_date(value: object) -> date | None:
    """Normalise SQL date/string results to ``date``."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return date.fromisoformat(value[:10])
    return None
