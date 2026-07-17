"""Founder Command Centre Overview DTOs (IAHF-003 / POP-002)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OperationalAlert:
    """Actionable alert for the Overview alerts strip."""

    severity: str
    message: str
    href: str


@dataclass(frozen=True)
class RecentFeedbackItem:
    """Newest Product Check-in row for Overview."""

    submission_id: int
    student_label: str
    feature: str
    status: str
    status_label: str
    submitted_at: str


@dataclass(frozen=True)
class AttentionQueueItem:
    """One triage item for Overview / Attention."""

    kind: str
    item_id: int
    title: str
    urgency: str
    detail: str
    href: str


@dataclass(frozen=True)
class CommandCentreOverview:
    """Homepage model for the Founder Command Centre Overview."""

    refreshed_at: str
    timezone_policy: str
    app_version: str
    alpha_version: str
    build_number: str
    alpha_enabled: bool
    checkins_today: int
    participants_active_today: int
    outstanding_reviews: int
    open_high_severity_findings: int
    needs_action_count: int
    alpha_health_label: str
    alpha_health_detail: str
    system_health_available: bool
    system_health_label: str
    system_health_pct: int | None
    alerts: tuple[OperationalAlert, ...]
    recent_feedback: tuple[RecentFeedbackItem, ...]
    attention_queue: tuple[AttentionQueueItem, ...]
    active_participants: int
    completed_checkins: int
    participation_rate_pct: float | None
    avg_product_experience: float | None
    would_open_tomorrow_pct: float | None
    checkins_last_7_days: int
    research_top_trend: str | None
    research_top_friction: str | None
    research_available: bool
    ops_available: bool
    capability_completed: int | None
    capability_active: int | None
    inbox_truncated: bool
    inbox_shown: int
    inbox_total: int
