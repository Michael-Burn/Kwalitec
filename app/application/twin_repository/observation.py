"""Fail-open Twin evolution observation after durable persist (PRD-001 Phase E).

Called by TwinRepository adapters after successful commit. Passes only
metadata + snapshot_hash into analytics — never Twin aggregates.
"""

from __future__ import annotations

import logging
from typing import Protocol, runtime_checkable

from app.application.twin_repository.content_hash import compute_twin_snapshot_hash
from app.application.twin_repository.types import (
    PersistAcknowledgement,
    TwinAuthorship,
)

logger = logging.getLogger(__name__)


@runtime_checkable
class TwinAnalyticsPort(Protocol):
    """Structural contract for Twin evolution analytics."""

    def emit_evolved(
        self,
        *,
        user_id: int,
        twin_snapshot_id: str,
        twin_version: str,
        evolution_reason: str,
        snapshot_hash: str,
    ) -> None:
        """Emit ``twin.evolved`` (fail-open; dispatch owned by infra)."""


# Process-local analytics port (bound by infrastructure composition / tests).
_analytics_port: TwinAnalyticsPort | None = None


def bind_twin_analytics_port(port: TwinAnalyticsPort | None) -> None:
    """Bind the process-local Twin analytics port."""
    global _analytics_port
    _analytics_port = port


def get_twin_analytics_port() -> TwinAnalyticsPort | None:
    """Return the bound Twin analytics port, or None."""
    return _analytics_port


def observe_twin_evolved_after_persist(
    ack: PersistAcknowledgement,
    *,
    encoded_twin_payload: str,
) -> None:
    """Emit ``twin.evolved`` after successful Twin snapshot persistence.

    Fail-open: analytics errors never affect Twin persistence results.
    Non-integer ``student_id`` scopes skip emit (analytics identity is
    opaque integer only).
    """
    try:
        sid = (ack.scope.student_id or "").strip()
        if not sid:
            return
        try:
            user_id = int(sid)
        except (TypeError, ValueError):
            return

        snapshot_hash = compute_twin_snapshot_hash(encoded_twin_payload)
        evolution_reason = (
            "birth"
            if ack.authorship is TwinAuthorship.BIRTH
            else "successor"
        )

        port = get_twin_analytics_port()
        if port is None:
            return
        port.emit_evolved(
            user_id=user_id,
            twin_snapshot_id=ack.snapshot_id,
            twin_version=str(ack.sequence),
            evolution_reason=evolution_reason,
            snapshot_hash=snapshot_hash,
        )
    except Exception:  # noqa: BLE001 — analytics must never break Twin persist
        logger.exception(
            "analytics.emit_failed twin.evolved snapshot=%s",
            getattr(ack, "snapshot_id", ""),
        )
