"""Privacy operations — retention cascade, deletion, export, consent (EP-002 WS4).

Implements operational executability for every PRD-001 §7–§8 policy.
Does not modify Twin, Educational State, or Learning Evidence.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Protocol

from app.infrastructure.analytics.metrics import (
    ANALYTICS_METRICS,
    AnalyticsOperationalMetrics,
)

logger = logging.getLogger(__name__)


class UserEventStorePort(Protocol):
    def delete_for_user(self, user_id: int) -> int:
        ...

    def list_for_user(self, user_id: int, *, limit: int = 10_000) -> list[dict]:
        ...


class UserOutboxPort(Protocol):
    def delete_for_user(self, user_id: int) -> int:
        ...


class AuditAppendPort(Protocol):
    def append(
        self,
        *,
        action: str,
        user_id: int | None = None,
        detail: dict | None = None,
    ) -> str:
        ...

    def list_actions(
        self,
        *,
        action: str | None = None,
        user_id: int | None = None,
        limit: int = 500,
    ) -> list[dict]:
        ...

    def export_jsonl(
        self,
        *,
        action: str | None = None,
        user_id: int | None = None,
        limit: int = 10_000,
    ) -> str:
        ...


@dataclass(frozen=True)
class ConsentVerdict:
    """Result of consent verification for analytics collection."""

    allowed: bool
    basis: str
    notes: str = ""


@dataclass(frozen=True)
class DeletionResult:
    """Outcome of student analytics cascade deletion (PRD-001 §7.2)."""

    user_id: int
    events_deleted: int = 0
    outbox_deleted: int = 0
    audit_id: str = ""


@dataclass(frozen=True)
class ExportResult:
    """Student or audit export package."""

    export_type: str
    user_id: int | None
    payload: str
    audit_id: str = ""
    event_count: int = 0


class AnalyticsConsentPolicy:
    """PRD-001 §8 consent assumptions — invite-only private beta.

    No separate marketing consent. Purpose limitation: product validation only.
    Expanding jurisdictions requires Privacy Review update.
    """

    PURPOSE = "private_beta_product_validation"
    BASIS = "invite_only_account_plus_privacy_notice"

    def verify(
        self,
        *,
        user_id: int,
        invite_only_cohort: bool = True,
        privacy_notice_acknowledged: bool = True,
        marketing_use: bool = False,
    ) -> ConsentVerdict:
        """Verify whether analytics collection is permitted for ``user_id``.

        Args:
            user_id: Opaque student id (must be positive).
            invite_only_cohort: Account is invite-only private beta.
            privacy_notice_acknowledged: Privacy notice covering first-party
                learning analytics was presented / accepted at invitation.
            marketing_use: If True, collection is forbidden (purpose limitation).
        """
        if user_id is None or int(user_id) < 1:
            return ConsentVerdict(
                allowed=False,
                basis="invalid_user",
                notes="user_id must be a positive integer",
            )
        if marketing_use:
            return ConsentVerdict(
                allowed=False,
                basis="purpose_limitation",
                notes="analytics must not be used for advertising or resale",
            )
        if not invite_only_cohort:
            return ConsentVerdict(
                allowed=False,
                basis="cohort_requires_privacy_review",
                notes="expanding beyond invite-only requires Privacy Review",
            )
        if not privacy_notice_acknowledged:
            return ConsentVerdict(
                allowed=False,
                basis="privacy_notice_required",
                notes="privacy notice stating first-party analytics is required",
            )
        return ConsentVerdict(
            allowed=True,
            basis=self.BASIS,
            notes=f"purpose={self.PURPOSE}",
        )


class AnalyticsPrivacyService:
    """Executable privacy workflows for PRD-001 §7.2–§7.3 / §8."""

    def __init__(
        self,
        *,
        event_store: UserEventStorePort,
        outbox: UserOutboxPort | None = None,
        audit: AuditAppendPort | None = None,
        consent: AnalyticsConsentPolicy | None = None,
        metrics: AnalyticsOperationalMetrics | None = None,
    ) -> None:
        self._events = event_store
        self._outbox = outbox
        self._audit = audit
        self._consent = consent or AnalyticsConsentPolicy()
        self._metrics = metrics if metrics is not None else ANALYTICS_METRICS

    def verify_consent(self, **kwargs: Any) -> ConsentVerdict:
        """Delegate to :class:`AnalyticsConsentPolicy`."""
        return self._consent.verify(**kwargs)

    def delete_user_analytics(
        self,
        user_id: int,
        *,
        requested_by: str = "support",
    ) -> DeletionResult:
        """Cascade-delete analytics rows for ``user_id`` (PRD §7.2).

        Educational domain deletion remains out of scope — callers must use
        existing account/support workflows for Twin / ESS / Evidence.
        """
        if user_id is None or int(user_id) < 1:
            raise ValueError("user_id must be a positive integer")
        events_deleted = self._events.delete_for_user(int(user_id))
        outbox_deleted = 0
        if self._outbox is not None:
            outbox_deleted = self._outbox.delete_for_user(int(user_id))
        audit_id = ""
        if self._audit is not None:
            audit_id = self._audit.append(
                action="analytics.user_deleted",
                user_id=int(user_id),
                detail={
                    "events_deleted": events_deleted,
                    "outbox_deleted": outbox_deleted,
                    "requested_by": requested_by,
                    "occurred_at": datetime.now(tz=UTC).isoformat(),
                },
            )
        self._metrics.record_user_deletion()
        logger.info(
            "analytics.user_deleted user_id=%s events=%s outbox=%s",
            user_id,
            events_deleted,
            outbox_deleted,
        )
        return DeletionResult(
            user_id=int(user_id),
            events_deleted=events_deleted,
            outbox_deleted=outbox_deleted,
            audit_id=audit_id,
        )

    def export_student(
        self,
        user_id: int,
        *,
        requested_by: str = "support",
        limit: int = 10_000,
    ) -> ExportResult:
        """Export one student's raw analytics events as UTF-8 JSON (PRD §7.3)."""
        if user_id is None or int(user_id) < 1:
            raise ValueError("user_id must be a positive integer")
        events = self._events.list_for_user(int(user_id), limit=limit)
        package = {
            "export_type": "student",
            "user_id": int(user_id),
            "exported_at": datetime.now(tz=UTC).isoformat(),
            "event_count": len(events),
            "events": events,
            "aggregates": [],  # weekly rollups not yet persisted in Phase 1 store
            "notes": "hashes as stored; not reversed; no other users included",
        }
        payload = json.dumps(package, indent=2, sort_keys=True)
        audit_id = ""
        if self._audit is not None:
            audit_id = self._audit.append(
                action="analytics.export_student",
                user_id=int(user_id),
                detail={
                    "event_count": len(events),
                    "requested_by": requested_by,
                },
            )
        self._metrics.record_export()
        return ExportResult(
            export_type="student",
            user_id=int(user_id),
            payload=payload,
            audit_id=audit_id,
            event_count=len(events),
        )

    def export_audit(
        self,
        *,
        action: str | None = None,
        user_id: int | None = None,
        requested_by: str = "security",
        limit: int = 10_000,
    ) -> ExportResult:
        """Export audit log as JSON lines (PRD §7.3)."""
        if self._audit is None:
            raise RuntimeError("audit log is not bound")
        payload = self._audit.export_jsonl(
            action=action, user_id=user_id, limit=limit
        )
        audit_id = self._audit.append(
            action="analytics.export_audit",
            user_id=user_id,
            detail={"requested_by": requested_by, "filter_action": action},
        )
        self._metrics.record_export()
        return ExportResult(
            export_type="audit",
            user_id=user_id,
            payload=payload,
            audit_id=audit_id,
            event_count=payload.count("\n") + (1 if payload else 0),
        )

    def retrieve_audit(
        self,
        *,
        action: str | None = None,
        user_id: int | None = None,
        limit: int = 500,
    ) -> list[dict]:
        """Retrieve audit entries for ops / security review."""
        if self._audit is None:
            raise RuntimeError("audit log is not bound")
        return self._audit.list_actions(
            action=action, user_id=user_id, limit=limit
        )
