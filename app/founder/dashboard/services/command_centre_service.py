"""Founder Command Centre Overview service (IAHF-003).

Assembles the Overview homepage from live operational sources:
- Product Check-ins / research records (SQLAlchemy) — Internal Alpha SoT
- Operational State (Knowledge / Capability / engineering signals)
- Internal Alpha status (version / enablement)

Does not write educational evidence, Twin state, or learning algorithms.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta

from flask import url_for

from app.extensions import db
from app.founder.dashboard.dto.command_centre import (
    AttentionQueueItem,
    CommandCentreOverview,
    OperationalAlert,
    RecentFeedbackItem,
    VisionWidgetItem,
)
from app.founder.dashboard.providers import OperationalStateProvider
from app.founder.dashboard.providers.protocols import OperationalStateGate
from app.founder.dashboard.services.dashboard_service import (
    FounderDashboardService,
    _signal_health,
)
from app.models.research_feedback import (
    ResearchFeedbackSubmission,
    ResearchProductFinding,
)
from app.models.user import User
from app.models.vision_journal import (
    TARGET_VERSION_LABELS,
    VISION_STATUS_LABELS,
)
from app.services.founder_research_service import (
    WORKFLOW_LABELS,
    FounderResearchService,
)
from app.services.internal_alpha_status_service import (
    INTERNAL_ALPHA_VERSION,
    InternalAlphaStatusService,
)
from app.services.research_insight_service import TIME_WINDOW_7_DAYS
from app.services.vision_journal_service import VisionJournalService
from app.version import APP_VERSION

TIMEZONE_POLICY = "Calendar day (server local date)"
OUTSTANDING_REVIEW_ALERT_THRESHOLD = 5
STALE_UNDER_REVIEW_DAYS = 7
ATTENTION_QUEUE_LIMIT = 8
RECENT_FEEDBACK_LIMIT = 8
INBOX_DISPLAY_CAP = 50
OPEN_FINDING_STATUSES = frozenset(
    {"new", "under_review", "accepted", "planned"}
)
HIGH_SEVERITIES = frozenset({"Critical", "High"})


@dataclass(frozen=True)
class ParticipantRow:
    """One Alpha participant for the Participants section."""

    user_id: int
    email: str
    checkin_count: int
    last_checkin_at: str
    badge_labels: tuple[str, ...]


class CommandCentreService:
    """Build Founder Command Centre Overview and section helpers."""

    def __init__(
        self,
        *,
        operational_state: OperationalStateGate | None = None,
        founder_user_id: int | None = None,
    ) -> None:
        self._operational_state = operational_state or OperationalStateProvider()
        self._founder_user_id = founder_user_id

    def build_overview(
        self,
        *,
        on_date: date | None = None,
    ) -> CommandCentreOverview:
        """Assemble Overview from live operational data."""
        today = on_date or date.today()
        now = datetime.now(UTC)
        summary = FounderResearchService.get_internal_alpha_summary()
        product_health = FounderResearchService.get_product_health()

        checkins_today, participants_today = self._today_activity(today)
        checkins_7d = self._checkins_since(today - timedelta(days=6))
        open_high = self._open_high_severity_findings_count()
        needs_action = summary.outstanding_reviews + open_high

        alpha_status = self._alpha_status()
        alpha_label, alpha_detail = self._alpha_health_label(
            summary=summary,
            enabled=alpha_status["enabled"],
        )

        ops = self._ops_snapshot()
        alerts = self._build_alerts(
            outstanding=summary.outstanding_reviews,
            open_high=open_high,
            alpha_enabled=alpha_status["enabled"],
            system_unhealthy=bool(
                ops["available"]
                and ops["health_pct"] is not None
                and ops["health_pct"] < 100
            ),
            inbox_total=self._inbox_total(),
        )

        recent = self._recent_feedback(limit=RECENT_FEEDBACK_LIMIT)
        attention = self._attention_queue(limit=ATTENTION_QUEUE_LIMIT)

        insight_available = summary.completed_checkins > 0
        top_trend = None
        top_friction = product_health.most_mentioned_friction
        if insight_available:
            engine = FounderResearchService.get_insight_engine(
                time_window=TIME_WINDOW_7_DAYS,
                as_of=today,
            )
            if engine.top_trends:
                top_trend = engine.top_trends[0].title

        inbox_total = self._inbox_total()
        inbox_truncated = inbox_total > INBOX_DISPLAY_CAP
        vision = self._vision_widgets()

        return CommandCentreOverview(
            refreshed_at=now.strftime("%Y-%m-%d %H:%M UTC"),
            timezone_policy=TIMEZONE_POLICY,
            app_version=APP_VERSION,
            alpha_version=alpha_status["alpha_version"],
            build_number=alpha_status["build_number"],
            alpha_enabled=alpha_status["enabled"],
            checkins_today=checkins_today,
            participants_active_today=participants_today,
            outstanding_reviews=summary.outstanding_reviews,
            open_high_severity_findings=open_high,
            needs_action_count=needs_action,
            alpha_health_label=alpha_label,
            alpha_health_detail=alpha_detail,
            system_health_available=ops["available"],
            system_health_label=ops["label"],
            system_health_pct=ops["health_pct"],
            alerts=alerts,
            recent_feedback=recent,
            attention_queue=attention,
            active_participants=summary.active_participants,
            completed_checkins=summary.completed_checkins,
            participation_rate_pct=summary.participation_rate_pct,
            avg_product_experience=summary.avg_product_experience,
            would_open_tomorrow_pct=summary.would_open_tomorrow_pct,
            checkins_last_7_days=checkins_7d,
            research_top_trend=top_trend,
            research_top_friction=top_friction,
            research_available=insight_available,
            ops_available=ops["available"],
            capability_completed=ops["completed"],
            capability_active=ops["active"],
            inbox_truncated=inbox_truncated,
            inbox_shown=min(inbox_total, INBOX_DISPLAY_CAP),
            inbox_total=inbox_total,
            vision_recent=vision["recent"],
            vision_awaiting_validation=vision["awaiting"],
            vision_planned_next=vision["planned"],
            vision_recently_promoted=vision["promoted"],
        )

    def list_attention_items(
        self, *, limit: int = 50
    ) -> tuple[AttentionQueueItem, ...]:
        """Full Attention triage list."""
        return self._attention_queue(limit=limit)

    def list_participants(self) -> tuple[ParticipantRow, ...]:
        """Participants with check-in activity and badges."""
        from app.models.research_feedback import ResearchContributorBadge
        from app.services.contributor_recognition_service import BADGE_LABELS

        submissions = ResearchFeedbackSubmission.query.order_by(
            ResearchFeedbackSubmission.submitted_at.desc()
        ).all()
        by_user: dict[int, list[ResearchFeedbackSubmission]] = {}
        for sub in submissions:
            by_user.setdefault(sub.user_id, []).append(sub)

        rows: list[ParticipantRow] = []
        for user_id, subs in by_user.items():
            user = db.session.get(User, user_id)
            email = user.email if user is not None else f"user:{user_id}"
            badge_rows = ResearchContributorBadge.query.filter_by(
                user_id=user_id
            ).all()
            badge_labels = tuple(
                BADGE_LABELS[row.badge_slug]
                for row in badge_rows
                if row.badge_slug in BADGE_LABELS
            )
            last = subs[0].submitted_at
            rows.append(
                ParticipantRow(
                    user_id=user_id,
                    email=email,
                    checkin_count=len(subs),
                    last_checkin_at=last.strftime("%Y-%m-%d %H:%M")
                    if last
                    else "—",
                    badge_labels=badge_labels,
                )
            )
        rows.sort(key=lambda r: r.checkin_count, reverse=True)
        return tuple(rows)

    def _alpha_status(self) -> dict[str, object]:
        import os

        from app.application.config.internal_alpha import is_internal_alpha_enabled

        if self._founder_user_id is not None:
            status = InternalAlphaStatusService.build_status(self._founder_user_id)
            return {
                "enabled": status.internal_alpha_enabled,
                "alpha_version": status.internal_alpha_version,
                "build_number": status.build_number,
            }
        build = os.environ.get("KWALITEC_BUILD_NUMBER", "").strip() or "local"
        return {
            "enabled": is_internal_alpha_enabled(),
            "alpha_version": INTERNAL_ALPHA_VERSION,
            "build_number": build,
        }

    def _ops_snapshot(self) -> dict[str, object]:
        # Avoid expensive filesystem Knowledge/Capability scans under pytest.
        # Production Overview still reads live Operational State.
        try:
            from flask import current_app, has_app_context

            if has_app_context() and current_app.config.get("TESTING"):
                return {
                    "available": False,
                    "label": "Unavailable",
                    "health_pct": None,
                    "completed": None,
                    "active": None,
                }
        except RuntimeError:
            pass

        state = self._operational_state.get_state()
        if state is None:
            return {
                "available": False,
                "label": "Unavailable",
                "health_pct": None,
                "completed": None,
                "active": None,
            }
        health = _signal_health(
            tests_pass=state.engineering.tests_pass,
            validation_errors=state.engineering.validation_errors,
        )
        label = "Healthy" if health == 100 else "Needs attention"
        return {
            "available": True,
            "label": label,
            "health_pct": health,
            "completed": state.capability.completed_count,
            "active": state.capability.active_count,
        }

    @staticmethod
    def _alpha_health_label(*, summary, enabled: bool) -> tuple[str, str]:
        if not enabled:
            return "Disabled", "Internal Alpha enablement is off"
        if summary.completed_checkins == 0:
            return "No check-ins yet", "Waiting for first Product Check-in"
        if summary.participation_rate_pct is None:
            return "Active", f"{summary.completed_checkins} check-ins recorded"
        rate = summary.participation_rate_pct
        if rate >= 50:
            return "Healthy", f"Participation {rate}%"
        if rate >= 20:
            return "Watch", f"Participation {rate}%"
        return "Low participation", f"Participation {rate}%"

    def _build_alerts(
        self,
        *,
        outstanding: int,
        open_high: int,
        alpha_enabled: bool,
        system_unhealthy: bool,
        inbox_total: int,
    ) -> tuple[OperationalAlert, ...]:
        alerts: list[OperationalAlert] = []
        if outstanding >= OUTSTANDING_REVIEW_ALERT_THRESHOLD:
            alerts.append(
                OperationalAlert(
                    severity="high",
                    message=f"{outstanding} Product Check-ins awaiting review",
                    href=url_for("founder_dashboard.attention"),
                )
            )
        if open_high > 0:
            alerts.append(
                OperationalAlert(
                    severity="critical" if open_high >= 3 else "high",
                    message=f"{open_high} open High/Critical Product Findings",
                    href=url_for("founder_dashboard.findings", severity="High"),
                )
            )
        if not alpha_enabled:
            alerts.append(
                OperationalAlert(
                    severity="high",
                    message="Internal Alpha enablement is off",
                    href=url_for("founder_dashboard.internal_alpha"),
                )
            )
        if system_unhealthy:
            alerts.append(
                OperationalAlert(
                    severity="high",
                    message="System health signals need attention",
                    href=url_for("founder_dashboard.operations"),
                )
            )
        if inbox_total > INBOX_DISPLAY_CAP:
            alerts.append(
                OperationalAlert(
                    severity="high",
                    message=(
                        f"Inbox truncated — showing {INBOX_DISPLAY_CAP} of "
                        f"{inbox_total}. Open Feedback for filters."
                    ),
                    href=url_for("founder_dashboard.feedback"),
                )
            )
        stale = self._stale_under_review_count()
        if stale > 0:
            alerts.append(
                OperationalAlert(
                    severity="high",
                    message=(
                        f"{stale} under-review item(s) older than "
                        f"{STALE_UNDER_REVIEW_DAYS} days"
                    ),
                    href=url_for(
                        "founder_dashboard.feedback", status="under_review"
                    ),
                )
            )
        return tuple(alerts)

    @staticmethod
    def _today_activity(today: date) -> tuple[int, int]:
        start = datetime.combine(today, datetime.min.time())
        end = datetime.combine(today + timedelta(days=1), datetime.min.time())
        rows = ResearchFeedbackSubmission.query.filter(
            ResearchFeedbackSubmission.submitted_at >= start,
            ResearchFeedbackSubmission.submitted_at < end,
        ).all()
        return len(rows), len({r.user_id for r in rows})

    @staticmethod
    def _checkins_since(start_day: date) -> int:
        start = datetime.combine(start_day, datetime.min.time())
        return ResearchFeedbackSubmission.query.filter(
            ResearchFeedbackSubmission.submitted_at >= start
        ).count()

    @staticmethod
    def _inbox_total() -> int:
        return ResearchFeedbackSubmission.query.count()

    @staticmethod
    def _open_high_severity_findings_count() -> int:
        return ResearchProductFinding.query.filter(
            ResearchProductFinding.severity.in_(tuple(HIGH_SEVERITIES)),
            ResearchProductFinding.status.in_(tuple(OPEN_FINDING_STATUSES)),
        ).count()

    @staticmethod
    def _stale_under_review_count() -> int:
        cutoff = datetime.now(UTC).replace(tzinfo=None) - timedelta(
            days=STALE_UNDER_REVIEW_DAYS
        )
        return ResearchFeedbackSubmission.query.filter(
            ResearchFeedbackSubmission.workflow_status == "under_review",
            ResearchFeedbackSubmission.submitted_at < cutoff,
        ).count()

    def _recent_feedback(
        self, *, limit: int
    ) -> tuple[RecentFeedbackItem, ...]:
        from sqlalchemy.orm import joinedload

        newest = (
            ResearchFeedbackSubmission.query.options(
                joinedload(ResearchFeedbackSubmission.user)
            )
            .order_by(ResearchFeedbackSubmission.submitted_at.desc())
            .limit(limit)
            .all()
        )
        items: list[RecentFeedbackItem] = []
        for sub in newest:
            user = sub.user
            label = user.email if user is not None else f"user:{sub.user_id}"
            items.append(
                RecentFeedbackItem(
                    submission_id=sub.id,
                    student_label=label,
                    feature=sub.feature_helped_most or "—",
                    status=sub.workflow_status,
                    status_label=WORKFLOW_LABELS.get(
                        sub.workflow_status, sub.workflow_status
                    ),
                    submitted_at=sub.submitted_at.strftime("%Y-%m-%d %H:%M")
                    if sub.submitted_at
                    else "—",
                )
            )
        return tuple(items)

    def _attention_queue(
        self, *, limit: int
    ) -> tuple[AttentionQueueItem, ...]:
        items: list[AttentionQueueItem] = []

        new_subs = (
            ResearchFeedbackSubmission.query.filter_by(workflow_status="new")
            .order_by(ResearchFeedbackSubmission.submitted_at.desc())
            .limit(limit)
            .all()
        )
        for sub in new_subs:
            items.append(
                AttentionQueueItem(
                    kind="feedback",
                    item_id=sub.id,
                    title=f"Review check-in #{sub.id}",
                    urgency="new",
                    detail=sub.feature_helped_most or "Product Check-in",
                    href=url_for(
                        "founder_dashboard.feedback", submission=sub.id
                    ),
                )
            )

        clarify = (
            ResearchFeedbackSubmission.query.filter_by(
                workflow_status="clarification_requested"
            )
            .order_by(ResearchFeedbackSubmission.submitted_at.desc())
            .limit(limit)
            .all()
        )
        for sub in clarify:
            items.append(
                AttentionQueueItem(
                    kind="feedback",
                    item_id=sub.id,
                    title=f"Clarification for check-in #{sub.id}",
                    urgency="clarification",
                    detail=sub.feature_helped_most or "Needs clarification",
                    href=url_for(
                        "founder_dashboard.feedback", submission=sub.id
                    ),
                )
            )

        findings = (
            ResearchProductFinding.query.filter(
                ResearchProductFinding.severity.in_(tuple(HIGH_SEVERITIES)),
                ResearchProductFinding.status.in_(tuple(OPEN_FINDING_STATUSES)),
            )
            .order_by(ResearchProductFinding.created_at.desc())
            .limit(limit)
            .all()
        )
        for finding in findings:
            items.append(
                AttentionQueueItem(
                    kind="finding",
                    item_id=finding.id,
                    title=finding.title,
                    urgency=finding.severity.lower(),
                    detail=f"{finding.severity} · {finding.status}",
                    href=url_for(
                        "founder_dashboard.finding_detail",
                        finding_id=finding.id,
                    ),
                )
            )

        urgency_rank = {
            "critical": 0,
            "high": 1,
            "new": 2,
            "clarification": 3,
        }
        items.sort(key=lambda i: urgency_rank.get(i.urgency, 9))
        return tuple(items[:limit])

    def _vision_widgets(self) -> dict[str, tuple[VisionWidgetItem, ...]]:
        """Compact Vision Journal widgets for Overview."""
        widgets = VisionJournalService.overview_widgets(limit=5)

        def _item(entry, *, meta: str) -> VisionWidgetItem:
            return VisionWidgetItem(
                entry_id=entry.id,
                title=entry.title,
                status_label=VISION_STATUS_LABELS.get(
                    entry.status, entry.status
                ),
                meta=meta,
            )

        recent = tuple(
            _item(
                e,
                meta=(
                    f"{e.category} · "
                    f"{TARGET_VERSION_LABELS.get(e.target_version, e.target_version)}"
                ),
            )
            for e in widgets.recent_entries
        )
        awaiting = tuple(
            _item(
                e,
                meta=f"{e.category} · updated {e.updated_at.strftime('%Y-%m-%d')}",
            )
            for e in widgets.awaiting_validation
        )
        planned = tuple(
            _item(
                e,
                meta=TARGET_VERSION_LABELS.get(
                    e.target_version, e.target_version
                ),
            )
            for e in widgets.planned_next_version
        )
        promoted = tuple(
            VisionWidgetItem(
                entry_id=entry.id,
                title=entry.title,
                status_label=VISION_STATUS_LABELS.get(
                    entry.status, entry.status
                ),
                meta=promo.placeholder_ref,
            )
            for entry, promo in widgets.recently_promoted
        )
        return {
            "recent": recent,
            "awaiting": awaiting,
            "planned": planned,
            "promoted": promoted,
        }


def build_operations_page():
    """Reuse FOS dashboard page builder for Operations section."""
    return FounderDashboardService().build_page()
