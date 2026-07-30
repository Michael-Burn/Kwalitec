"""Aggregate private-beta validation metrics (PB-001).

Composes existing Mission / StudyAttempt / PresentationEvent / Twin streak
signals with PB-001 cohort, feedback, and observation tables.
No new educational architecture.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta

from sqlalchemy import func

from app.extensions import db
from app.models.alpha_infrastructure import PresentationEvent
from app.models.learning import StudyAttempt
from app.models.mission import Mission
from app.models.private_beta import (
    PrivateBetaFeedback,
    PrivateBetaObservation,
    PrivateBetaParticipant,
)
from app.models.study_plan import StudyPlan
from app.services.private_beta.first_session_service import (
    EVENT_KNOWLEDGE_MAP_OPENED,
    EVENT_TUTOR_OPENED,
    EVENT_TUTOR_QUESTION,
)

# Closed-beta quality gates (PB-001).
GATE_STUDY_PLAN_PCT = 90.0
GATE_MISSION_START_PCT = 90.0
GATE_SESSION_COMPLETE_PCT = 80.0
GATE_WEEKLY_RETURN_PCT = 70.0
GATE_CRITICAL_BUGS_MAX = 5


@dataclass(frozen=True)
class QualityGateResult:
    gate_id: str
    label: str
    actual: float | int
    threshold: float | int
    unit: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class ScreenVisitStat:
    path: str
    visits: int


@dataclass(frozen=True)
class PrivateBetaMetricsSnapshot:
    """Point-in-time private beta evidence snapshot."""

    as_of: datetime
    total_beta_users: int
    daily_active_users: int
    weekly_active_users: int
    current_study_sessions: int
    mission_completion_pct: float
    missions_started: int
    missions_completed: int
    tutor_activity: int
    knowledge_map_usage: int
    average_streak: float
    average_session_duration_minutes: float
    daily_return_rate_pct: float
    weekly_return_rate_pct: float
    study_plan_completion_pct: float
    first_mission_start_pct: float
    session_completion_pct: float
    critical_bugs: int
    major_bugs: int
    feature_requests: int
    feedback_total: int
    observations_total: int
    stuck_observations: int
    most_visited_screens: tuple[ScreenVisitStat, ...]
    least_visited_screens: tuple[ScreenVisitStat, ...]
    average_missions_per_user: float
    mission_abandonment_pct: float
    tutor_adoption_pct: float
    knowledge_map_adoption_pct: float
    progress_usage: int
    quality_gates: tuple[QualityGateResult, ...]
    gates_passed: bool
    go_recommendation: str


def _day_start(d: date) -> datetime:
    return datetime.combine(d, datetime.min.time())


def _cohort_user_ids() -> set[int]:
    rows = (
        db.session.query(PrivateBetaParticipant.user_id)
        .filter_by(is_active=True)
        .all()
    )
    return {int(r[0]) for r in rows}


def _active_users_between(user_ids: set[int], start: datetime, end: datetime) -> int:
    if not user_ids:
        return 0
    mission_users = {
        int(r[0])
        for r in (
            db.session.query(Mission.user_id)
            .filter(
                Mission.user_id.in_(user_ids),
                Mission.status == "Completed",
                Mission.created_at >= start,
                Mission.created_at < end,
            )
            .distinct()
            .all()
        )
    }
    attempt_users = {
        int(r[0])
        for r in (
            db.session.query(StudyAttempt.user_id)
            .filter(
                StudyAttempt.user_id.in_(user_ids),
                StudyAttempt.study_date >= start.date(),
                StudyAttempt.study_date < end.date(),
            )
            .distinct()
            .all()
        )
    }
    event_users = {
        int(r[0])
        for r in (
            db.session.query(PresentationEvent.user_id)
            .filter(
                PresentationEvent.user_id.in_(user_ids),
                PresentationEvent.created_at >= start,
                PresentationEvent.created_at < end,
            )
            .distinct()
            .all()
        )
        if r[0] is not None
    }
    return len(mission_users | attempt_users | event_users)


def _pct(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return round(100.0 * numerator / denominator, 1)


class PrivateBetaMetricsService:
    """Build deterministic private-beta KPI snapshot."""

    def build(self, *, on_date: date | None = None) -> PrivateBetaMetricsSnapshot:
        today = on_date or date.today()
        now = datetime.now(UTC).replace(tzinfo=None)
        user_ids = _cohort_user_ids()
        n = len(user_ids)

        day0 = _day_start(today)
        day1 = day0 + timedelta(days=1)
        week0 = day0 - timedelta(days=6)

        dau = _active_users_between(user_ids, day0, day1)
        wau = _active_users_between(user_ids, week0, day1)

        current_sessions = 0
        if user_ids:
            current_sessions = (
                db.session.query(func.count(Mission.id))
                .filter(
                    Mission.user_id.in_(user_ids),
                    Mission.status == "In Progress",
                )
                .scalar()
                or 0
            )

        missions_started = 0
        missions_completed = 0
        if user_ids:
            missions_started = (
                db.session.query(func.count(Mission.id))
                .filter(
                    Mission.user_id.in_(user_ids),
                    Mission.status.in_(("In Progress", "Completed")),
                )
                .scalar()
                or 0
            )
            missions_completed = (
                db.session.query(func.count(Mission.id))
                .filter(
                    Mission.user_id.in_(user_ids),
                    Mission.status == "Completed",
                )
                .scalar()
                or 0
            )

        users_with_plan = 0
        users_started_mission = 0
        users_completed_session = 0
        if user_ids:
            users_with_plan = (
                db.session.query(func.count(func.distinct(StudyPlan.user_id)))
                .filter(
                    StudyPlan.user_id.in_(user_ids),
                    StudyPlan.archived.is_(False),
                )
                .scalar()
                or 0
            )
            users_started_mission = (
                db.session.query(func.count(func.distinct(Mission.user_id)))
                .filter(
                    Mission.user_id.in_(user_ids),
                    Mission.status.in_(("In Progress", "Completed")),
                )
                .scalar()
                or 0
            )
            users_completed_session = (
                db.session.query(func.count(func.distinct(Mission.user_id)))
                .filter(
                    Mission.user_id.in_(user_ids),
                    Mission.status == "Completed",
                )
                .scalar()
                or 0
            )

        tutor_events = 0
        kg_events = 0
        progress_events = 0
        tutor_users = 0
        kg_users = 0
        if user_ids:
            tutor_events = (
                db.session.query(func.count(PresentationEvent.id))
                .filter(
                    PresentationEvent.user_id.in_(user_ids),
                    PresentationEvent.event_type.in_(
                        (EVENT_TUTOR_OPENED, EVENT_TUTOR_QUESTION)
                    ),
                )
                .scalar()
                or 0
            )
            kg_events = (
                db.session.query(func.count(PresentationEvent.id))
                .filter(
                    PresentationEvent.user_id.in_(user_ids),
                    PresentationEvent.event_type == EVENT_KNOWLEDGE_MAP_OPENED,
                )
                .scalar()
                or 0
            )
            progress_events = (
                db.session.query(func.count(PresentationEvent.id))
                .filter(
                    PresentationEvent.user_id.in_(user_ids),
                    PresentationEvent.event_type == "journey_opened",
                )
                .scalar()
                or 0
            )
            tutor_users = (
                db.session.query(func.count(func.distinct(PresentationEvent.user_id)))
                .filter(
                    PresentationEvent.user_id.in_(user_ids),
                    PresentationEvent.event_type.in_(
                        (EVENT_TUTOR_OPENED, EVENT_TUTOR_QUESTION)
                    ),
                )
                .scalar()
                or 0
            )
            kg_users = (
                db.session.query(func.count(func.distinct(PresentationEvent.user_id)))
                .filter(
                    PresentationEvent.user_id.in_(user_ids),
                    PresentationEvent.event_type == EVENT_KNOWLEDGE_MAP_OPENED,
                )
                .scalar()
                or 0
            )

        avg_duration = 0.0
        if user_ids:
            avg_duration = float(
                db.session.query(func.avg(StudyAttempt.duration_minutes))
                .filter(
                    StudyAttempt.user_id.in_(user_ids),
                    StudyAttempt.duration_minutes.isnot(None),
                )
                .scalar()
                or 0.0
            )
            avg_duration = round(avg_duration, 1)

        # Streak: average of Twin / readiness is expensive; approximate from
        # distinct active study days in last 14 days for cohort members.
        avg_streak = self._approximate_avg_streak(user_ids, today)

        # Return rates: share of cohort active yesterday / in prior week window.
        yesterday = today - timedelta(days=1)
        y0, y1 = _day_start(yesterday), _day_start(yesterday) + timedelta(days=1)
        daily_return = _pct(_active_users_between(user_ids, y0, y1), n)
        prior_week_start = day0 - timedelta(days=13)
        prior_week_end = day0 - timedelta(days=6)
        weekly_return = _pct(
            _active_users_between(user_ids, prior_week_start, prior_week_end), n
        )

        severity = dict(
            db.session.query(
                PrivateBetaFeedback.severity,
                func.count(PrivateBetaFeedback.id),
            )
            .group_by(PrivateBetaFeedback.severity)
            .all()
        )
        critical = int(severity.get("critical", 0))
        major = int(severity.get("major", 0))
        feature_requests = (
            db.session.query(func.count(PrivateBetaFeedback.id))
            .filter(
                PrivateBetaFeedback.category.in_(
                    ("suggestion", "missing_feature")
                )
            )
            .scalar()
            or 0
        )
        feedback_total = (
            db.session.query(func.count(PrivateBetaFeedback.id)).scalar() or 0
        )
        observations_total = (
            db.session.query(func.count(PrivateBetaObservation.id)).scalar() or 0
        )
        stuck_observations = (
            db.session.query(func.count(PrivateBetaObservation.id))
            .filter(PrivateBetaObservation.became_stuck.is_(True))
            .scalar()
            or 0
        )

        screen_rows = (
            db.session.query(
                PresentationEvent.path,
                func.count(PresentationEvent.id),
            )
            .filter(PresentationEvent.path.isnot(None))
            .group_by(PresentationEvent.path)
            .order_by(func.count(PresentationEvent.id).desc())
            .limit(20)
            .all()
        )
        screens = [
            ScreenVisitStat(path=str(path), visits=int(count))
            for path, count in screen_rows
            if path
        ]
        most = tuple(screens[:5])
        least = tuple(sorted(screens, key=lambda s: s.visits)[:5]) if screens else ()

        avg_missions = round(missions_completed / n, 2) if n else 0.0
        abandonment = _pct(
            max(missions_started - missions_completed, 0), missions_started
        )

        plan_pct = _pct(users_with_plan, n)
        start_pct = _pct(users_started_mission, n)
        session_pct = _pct(users_completed_session, n)
        mission_completion_pct = _pct(missions_completed, missions_started)

        gates = (
            QualityGateResult(
                gate_id="study_plans",
                label="Create study plans",
                actual=plan_pct,
                threshold=GATE_STUDY_PLAN_PCT,
                unit="%",
                passed=plan_pct >= GATE_STUDY_PLAN_PCT if n else False,
                detail=f"{users_with_plan}/{n} enrolled users have an active plan",
            ),
            QualityGateResult(
                gate_id="mission_start",
                label="Start a mission",
                actual=start_pct,
                threshold=GATE_MISSION_START_PCT,
                unit="%",
                passed=start_pct >= GATE_MISSION_START_PCT if n else False,
                detail=f"{users_started_mission}/{n} started at least one mission",
            ),
            QualityGateResult(
                gate_id="session_complete",
                label="Complete a study session",
                actual=session_pct,
                threshold=GATE_SESSION_COMPLETE_PCT,
                unit="%",
                passed=session_pct >= GATE_SESSION_COMPLETE_PCT if n else False,
                detail=(
                    f"{users_completed_session}/{n} completed at least one session"
                ),
            ),
            QualityGateResult(
                gate_id="weekly_return",
                label="Return within one week",
                actual=weekly_return,
                threshold=GATE_WEEKLY_RETURN_PCT,
                unit="%",
                passed=weekly_return >= GATE_WEEKLY_RETURN_PCT if n else False,
                detail="Share of cohort active in the prior 7-day window",
            ),
            QualityGateResult(
                gate_id="critical_bugs",
                label="Critical bugs",
                actual=critical,
                threshold=GATE_CRITICAL_BUGS_MAX,
                unit="count",
                passed=critical < GATE_CRITICAL_BUGS_MAX,
                detail=(
                    f"{critical} critical reports "
                    f"(threshold < {GATE_CRITICAL_BUGS_MAX})"
                ),
            ),
        )
        gates_passed = all(g.passed for g in gates) and n >= 10
        if n == 0 or not gates_passed:
            go = "PRIVATE BETA EXTENSION REQUIRED"
        else:
            go = "READY FOR PUBLIC BETA"

        return PrivateBetaMetricsSnapshot(
            as_of=now,
            total_beta_users=n,
            daily_active_users=dau,
            weekly_active_users=wau,
            current_study_sessions=int(current_sessions),
            mission_completion_pct=mission_completion_pct,
            missions_started=int(missions_started),
            missions_completed=int(missions_completed),
            tutor_activity=int(tutor_events),
            knowledge_map_usage=int(kg_events),
            average_streak=avg_streak,
            average_session_duration_minutes=avg_duration,
            daily_return_rate_pct=daily_return,
            weekly_return_rate_pct=weekly_return,
            study_plan_completion_pct=plan_pct,
            first_mission_start_pct=start_pct,
            session_completion_pct=session_pct,
            critical_bugs=critical,
            major_bugs=major,
            feature_requests=int(feature_requests),
            feedback_total=int(feedback_total),
            observations_total=int(observations_total),
            stuck_observations=int(stuck_observations),
            most_visited_screens=most,
            least_visited_screens=least,
            average_missions_per_user=avg_missions,
            mission_abandonment_pct=abandonment,
            tutor_adoption_pct=_pct(tutor_users, n),
            knowledge_map_adoption_pct=_pct(kg_users, n),
            progress_usage=int(progress_events),
            quality_gates=gates,
            gates_passed=gates_passed,
            go_recommendation=go,
        )

    @staticmethod
    def _approximate_avg_streak(user_ids: set[int], today: date) -> float:
        if not user_ids:
            return 0.0
        start = today - timedelta(days=13)
        rows = (
            db.session.query(StudyAttempt.user_id, StudyAttempt.study_date)
            .filter(
                StudyAttempt.user_id.in_(user_ids),
                StudyAttempt.study_date >= start,
                StudyAttempt.study_date <= today,
            )
            .distinct()
            .all()
        )
        by_user: dict[int, set[date]] = {}
        for uid, study_date in rows:
            by_user.setdefault(int(uid), set()).add(study_date)
        if not by_user:
            return 0.0
        # Approximate streak as max consecutive days ending at today (or last day).
        streaks: list[int] = []
        for days in by_user.values():
            streak = 0
            cursor = today
            while cursor in days:
                streak += 1
                cursor = cursor - timedelta(days=1)
            streaks.append(streak)
        if not streaks:
            return 0.0
        # Average across active studiers only, then dilute by full cohort.
        avg_active = sum(streaks) / len(streaks)
        return round(avg_active * len(by_user) / len(user_ids), 1)
