"""Source adapters for the Founder Feedback Hub (FH-001).

Each adapter loads one Source of Truth table and normalizes rows into
``FounderFeedbackItem``. Adapters never write, dual-write, or mutate storage.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, datetime, time, timedelta

from sqlalchemy.orm import joinedload

from app.models.alpha_infrastructure import AlphaFeedbackSubmission
from app.models.private_beta import PrivateBetaFeedback
from app.models.research_feedback import ResearchFeedbackSubmission
from app.models.user import User
from app.services.founder_feedback_hub.dto import (
    ORIGIN_COLOURS,
    ORIGIN_ICONS,
    SOURCE_ALPHA,
    SOURCE_LABELS,
    SOURCE_PRIVATE_BETA,
    SOURCE_RESEARCH,
    FounderFeedbackItem,
    HubFilters,
)

# Soft per-source cap — Founder Alpha/Beta volumes stay well below this.
_SOURCE_FETCH_CAP = 2000


def _preview(text: str | None, limit: int = 140) -> str | None:
    if text is None:
        return None
    cleaned = " ".join(str(text).split())
    if not cleaned:
        return None
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 1].rstrip() + "…"


def _email_of(user: User | None) -> str | None:
    if user is None:
        return None
    email = (getattr(user, "email", None) or "").strip()
    return email or None


def _student_label(user: User | None, user_id: int) -> str | None:
    email = _email_of(user)
    return email or f"user-{user_id}"


def _day_start(value: date) -> datetime:
    return datetime.combine(value, time.min)


def _day_end_exclusive(value: date) -> datetime:
    return datetime.combine(value + timedelta(days=1), time.min)


def _matches_keyword(item: FounderFeedbackItem, keyword: str) -> bool:
    needle = keyword.strip().lower()
    if not needle:
        return True
    haystacks = (
        item.message,
        item.summary,
        item.student,
        item.student_email,
        item.subject,
        item.category,
    )
    return any(h is not None and needle in str(h).lower() for h in haystacks)


def _matches_filters(item: FounderFeedbackItem, filters: HubFilters) -> bool:
    if filters.source and item.source != filters.source:
        return False
    if filters.severity:
        if not item.severity or item.severity.lower() != filters.severity.lower():
            return False
    if filters.status:
        if not item.status or item.status.lower() != filters.status.lower():
            return False
    if filters.subject:
        needle = filters.subject.strip().lower()
        if not item.subject or needle not in item.subject.lower():
            return False
    if filters.student:
        needle = filters.student.strip().lower()
        blob = " ".join(
            part
            for part in (item.student, item.student_email)
            if part
        ).lower()
        if needle not in blob:
            return False
    if filters.date_from and item.created_at is not None:
        if item.created_at < _day_start(filters.date_from):
            return False
    if filters.date_to and item.created_at is not None:
        if item.created_at >= _day_end_exclusive(filters.date_to):
            return False
    if filters.keyword and not _matches_keyword(item, filters.keyword):
        return False
    return True


def _apply_sql_date_filters(query, column, filters: HubFilters):
    if filters.date_from is not None:
        query = query.filter(column >= _day_start(filters.date_from))
    if filters.date_to is not None:
        query = query.filter(column < _day_end_exclusive(filters.date_to))
    return query


class FeedbackSourceAdapter(ABC):
    """Load and normalize one feedback Source of Truth."""

    source: str

    @abstractmethod
    def load(self, filters: HubFilters) -> list[FounderFeedbackItem]:
        """Return normalized items (caller applies final in-memory filters)."""


class PrivateBetaAdapter(FeedbackSourceAdapter):
    source = SOURCE_PRIVATE_BETA

    def load(self, filters: HubFilters) -> list[FounderFeedbackItem]:
        if filters.source and filters.source != self.source:
            return []

        query = PrivateBetaFeedback.query.options(
            joinedload(PrivateBetaFeedback.user)
        ).order_by(PrivateBetaFeedback.created_at.desc())
        query = _apply_sql_date_filters(
            query, PrivateBetaFeedback.created_at, filters
        )
        if filters.severity:
            query = query.filter(
                PrivateBetaFeedback.severity == filters.severity.strip().lower()
            )
        if filters.status:
            query = query.filter(
                PrivateBetaFeedback.status == filters.status.strip().lower()
            )
        if filters.subject:
            pattern = f"%{filters.subject.strip()}%"
            query = query.filter(PrivateBetaFeedback.subject_code.ilike(pattern))
        if filters.student:
            pattern = f"%{filters.student.strip()}%"
            query = query.join(User).filter(User.email.ilike(pattern))

        rows = query.limit(_SOURCE_FETCH_CAP).all()
        items: list[FounderFeedbackItem] = []
        for row in rows:
            email = _email_of(row.user)
            message = row.message
            items.append(
                FounderFeedbackItem(
                    id=f"{self.source}:{row.id}",
                    source=self.source,
                    source_label=SOURCE_LABELS[self.source],
                    student=_student_label(row.user, row.user_id),
                    student_email=email,
                    subject=row.subject_code,
                    category=row.category,
                    severity=row.severity,
                    status=row.status,
                    message=message,
                    summary=_preview(message),
                    created_at=row.created_at,
                    updated_at=None,
                    link_to_original=(
                        f"/console/beta?feedback_id={row.id}#feedback-{row.id}"
                    ),
                    origin_icon=ORIGIN_ICONS[self.source],
                    origin_colour=ORIGIN_COLOURS[self.source],
                    metadata={
                        "native_id": row.id,
                        "current_screen": row.current_screen,
                        "browser": row.browser,
                        "device": row.device,
                        "path": row.path,
                        "mission_id": row.mission_id,
                        "product_version": row.product_version,
                    },
                )
            )
        return items


class AlphaAdapter(FeedbackSourceAdapter):
    source = SOURCE_ALPHA

    def load(self, filters: HubFilters) -> list[FounderFeedbackItem]:
        if filters.source and filters.source != self.source:
            return []

        query = AlphaFeedbackSubmission.query.options(
            joinedload(AlphaFeedbackSubmission.user)
        ).order_by(AlphaFeedbackSubmission.created_at.desc())
        query = _apply_sql_date_filters(
            query, AlphaFeedbackSubmission.created_at, filters
        )
        if filters.status:
            query = query.filter(
                AlphaFeedbackSubmission.status == filters.status.strip().lower()
            )
        # Alpha has no severity / subject columns — skip SQL for those.
        if filters.severity:
            return []
        if filters.subject:
            return []
        if filters.student:
            pattern = f"%{filters.student.strip()}%"
            query = query.join(User).filter(User.email.ilike(pattern))

        rows = query.limit(_SOURCE_FETCH_CAP).all()
        items: list[FounderFeedbackItem] = []
        for row in rows:
            email = _email_of(row.user)
            message = row.message
            summary = _preview(message) or (
                f"{row.kind}: {row.rating}" if row.rating else row.kind
            )
            items.append(
                FounderFeedbackItem(
                    id=f"{self.source}:{row.id}",
                    source=self.source,
                    source_label=SOURCE_LABELS[self.source],
                    student=_student_label(row.user, row.user_id),
                    student_email=email,
                    subject=None,
                    category=row.kind,
                    severity=None,
                    status=row.status,
                    message=message,
                    summary=summary,
                    created_at=row.created_at,
                    updated_at=None,
                    link_to_original=(
                        f"/console/alpha-observability"
                        f"?feedback_id={row.id}#feedback-{row.id}"
                    ),
                    origin_icon=ORIGIN_ICONS[self.source],
                    origin_colour=ORIGIN_COLOURS[self.source],
                    metadata={
                        "native_id": row.id,
                        "kind": row.kind,
                        "rating": row.rating,
                        "surface": row.surface,
                        "mission_id": row.mission_id,
                        "product_version": row.product_version,
                        "correlation_id": row.correlation_id,
                    },
                )
            )
        return items


class ResearchAdapter(FeedbackSourceAdapter):
    source = SOURCE_RESEARCH

    def load(self, filters: HubFilters) -> list[FounderFeedbackItem]:
        if filters.source and filters.source != self.source:
            return []

        query = ResearchFeedbackSubmission.query.options(
            joinedload(ResearchFeedbackSubmission.user)
        ).order_by(ResearchFeedbackSubmission.submitted_at.desc())
        query = _apply_sql_date_filters(
            query, ResearchFeedbackSubmission.submitted_at, filters
        )
        if filters.status:
            query = query.filter(
                ResearchFeedbackSubmission.workflow_status
                == filters.status.strip().lower()
            )
        # Research has no severity / subject columns — skip SQL for those.
        if filters.severity:
            return []
        if filters.subject:
            return []
        if filters.student:
            pattern = f"%{filters.student.strip()}%"
            query = query.join(User).filter(User.email.ilike(pattern))

        rows = query.limit(_SOURCE_FETCH_CAP).all()
        items: list[FounderFeedbackItem] = []
        for row in rows:
            email = _email_of(row.user)
            message = row.free_text
            category = row.classification or row.friction_area
            summary = _preview(message) or (
                f"{row.feature_helped_most} · {row.friction_area}"
            )
            items.append(
                FounderFeedbackItem(
                    id=f"{self.source}:{row.id}",
                    source=self.source,
                    source_label=SOURCE_LABELS[self.source],
                    student=_student_label(row.user, row.user_id),
                    student_email=email,
                    subject=None,
                    category=category,
                    severity=None,
                    status=row.workflow_status,
                    message=message,
                    summary=summary,
                    created_at=row.submitted_at,
                    updated_at=None,
                    link_to_original=(
                        f"/console/feedback/checkins?submission={row.id}"
                    ),
                    origin_icon=ORIGIN_ICONS[self.source],
                    origin_colour=ORIGIN_COLOURS[self.source],
                    metadata={
                        "native_id": row.id,
                        "experience_rating": row.experience_rating,
                        "feature_helped_most": row.feature_helped_most,
                        "friction_area": row.friction_area,
                        "confidence_rating": row.confidence_rating,
                        "return_intent": row.return_intent,
                        "classification": row.classification,
                        "submission_source": row.submission_source,
                        "product_version": row.product_version,
                        "mission_id": row.mission_id,
                    },
                )
            )
        return items


DEFAULT_ADAPTERS: tuple[FeedbackSourceAdapter, ...] = (
    PrivateBetaAdapter(),
    AlphaAdapter(),
    ResearchAdapter(),
)


def apply_hub_filters(
    items: list[FounderFeedbackItem],
    filters: HubFilters,
) -> list[FounderFeedbackItem]:
    """Final in-memory filter pass (keyword + any residual constraints)."""
    return [item for item in items if _matches_filters(item, filters)]


def count_by_source(items: list[FounderFeedbackItem]) -> dict[str, int]:
    counts: dict[str, int] = {
        SOURCE_PRIVATE_BETA: 0,
        SOURCE_ALPHA: 0,
        SOURCE_RESEARCH: 0,
    }
    for item in items:
        counts[item.source] = counts.get(item.source, 0) + 1
    return counts


def sort_newest_first(
    items: list[FounderFeedbackItem],
) -> list[FounderFeedbackItem]:
    return sorted(
        items,
        key=lambda item: item.created_at or datetime.min,
        reverse=True,
    )
