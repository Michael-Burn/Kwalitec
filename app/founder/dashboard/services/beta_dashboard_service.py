"""PB-001 — Founder Private Beta Validation dashboard projection."""

from __future__ import annotations

from dataclasses import dataclass

from app.services.private_beta.feedback_service import PrivateBetaFeedbackService
from app.services.private_beta.first_session_service import (
    FirstSessionStudyService,
    FirstSessionTiming,
)
from app.services.private_beta.metrics_service import (
    PrivateBetaMetricsService,
    PrivateBetaMetricsSnapshot,
    QualityGateResult,
    ScreenVisitStat,
)
from app.services.private_beta.observation_service import PrivateBetaObservationService
from app.services.private_beta.participant_service import PrivateBetaParticipantService


@dataclass(frozen=True)
class BetaMetricCard:
    label: str
    value: str
    detail: str = ""


@dataclass(frozen=True)
class BetaFeedbackItem:
    id: int
    category: str
    severity: str
    screen: str
    message: str
    created_at: str


@dataclass(frozen=True)
class BetaParticipantRow:
    user_id: int
    email: str
    enrolled_at: str
    device_preference: str
    minutes_to_first_mission: str
    drop_off: str


@dataclass(frozen=True)
class FounderBetaDashboardPage:
    page_title: str
    page_support: str
    go_recommendation: str
    metrics: tuple[BetaMetricCard, ...]
    quality_gates: tuple[QualityGateResult, ...]
    latest_feedback: tuple[BetaFeedbackItem, ...]
    participants: tuple[BetaParticipantRow, ...]
    most_visited: tuple[ScreenVisitStat, ...]
    least_visited: tuple[ScreenVisitStat, ...]
    first_session_timings: tuple[FirstSessionTiming, ...]
    observations_count: int
    stuck_count: int
    empty_reason: str
    snapshot: PrivateBetaMetricsSnapshot


class FounderBetaDashboardService:
    """Aggregate PB-001 evidence for the Founder Beta Dashboard."""

    def build(self) -> FounderBetaDashboardPage:
        snapshot = PrivateBetaMetricsService().build()
        timings = FirstSessionStudyService().for_cohort()
        participants = PrivateBetaParticipantService.active_participants()
        timing_by_user = {t.user_id: t for t in timings}

        rows: list[BetaParticipantRow] = []
        for p in participants:
            user = p.user
            email = str(getattr(user, "email", "") or f"user-{p.user_id}")
            timing = timing_by_user.get(p.user_id)
            rows.append(
                BetaParticipantRow(
                    user_id=p.user_id,
                    email=email,
                    enrolled_at=p.enrolled_at.strftime("%Y-%m-%d %H:%M")
                    if p.enrolled_at
                    else "—",
                    device_preference=p.device_preference or "—",
                    minutes_to_first_mission=(
                        str(timing.minutes_to_first_mission)
                        if timing and timing.minutes_to_first_mission is not None
                        else "—"
                    ),
                    drop_off=(
                        timing.drop_off_location
                        if timing and timing.drop_off_location
                        else "—"
                    ),
                )
            )

        feedback_items = tuple(
            BetaFeedbackItem(
                id=item.id,
                category=item.category,
                severity=item.severity,
                screen=item.current_screen or "—",
                message=(item.message or "")[:160],
                created_at=item.created_at.strftime("%Y-%m-%d %H:%M")
                if item.created_at
                else "—",
            )
            for item in PrivateBetaFeedbackService.recent(limit=12)
        )

        observations = PrivateBetaObservationService.recent(limit=200)
        stuck = sum(1 for o in observations if o.became_stuck)

        metrics = (
            BetaMetricCard("Total beta users", str(snapshot.total_beta_users)),
            BetaMetricCard("Daily active", str(snapshot.daily_active_users)),
            BetaMetricCard("Weekly active", str(snapshot.weekly_active_users)),
            BetaMetricCard(
                "Current sessions", str(snapshot.current_study_sessions)
            ),
            BetaMetricCard(
                "Mission completion",
                f"{snapshot.mission_completion_pct}%",
            ),
            BetaMetricCard("Tutor activity", str(snapshot.tutor_activity)),
            BetaMetricCard(
                "Knowledge Map", str(snapshot.knowledge_map_usage)
            ),
            BetaMetricCard("Avg streak", str(snapshot.average_streak)),
            BetaMetricCard(
                "Avg session (min)",
                str(snapshot.average_session_duration_minutes),
            ),
            BetaMetricCard(
                "Weekly return",
                f"{snapshot.weekly_return_rate_pct}%",
            ),
            BetaMetricCard("Critical bugs", str(snapshot.critical_bugs)),
            BetaMetricCard("Feature requests", str(snapshot.feature_requests)),
        )

        empty = ""
        if snapshot.total_beta_users == 0:
            empty = (
                "No private-beta participants enrolled yet. "
                "Enrol students below to begin evidence capture."
            )

        return FounderBetaDashboardPage(
            page_title="Private Beta",
            page_support=(
                "PB-001 validation evidence — adoption, retention, feedback, "
                "and first-session hesitation. No new educational architecture."
            ),
            go_recommendation=snapshot.go_recommendation,
            metrics=metrics,
            quality_gates=snapshot.quality_gates,
            latest_feedback=feedback_items,
            participants=tuple(rows),
            most_visited=snapshot.most_visited_screens,
            least_visited=snapshot.least_visited_screens,
            first_session_timings=timings,
            observations_count=len(observations),
            stuck_count=stuck,
            empty_reason=empty,
            snapshot=snapshot,
        )
