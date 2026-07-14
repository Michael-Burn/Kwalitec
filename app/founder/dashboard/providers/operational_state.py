"""Operational State provider — wraps FOS-005 public service (FSI-002)."""

from __future__ import annotations

import logging
from typing import Protocol

from app.founder.operational_state import (
    FounderOperationalState,
    FounderOperationalStateService,
)

logger = logging.getLogger(__name__)


class OperationalStateServiceGate(Protocol):
    """Minimal surface required from FounderOperationalStateService."""

    def get_state(
        self, *, generated_at=None
    ) -> FounderOperationalState:
        """Return the current FounderOperationalState."""


class OperationalStateProvider:
    """Retrieve FounderOperationalState for dashboard presentation.

    Coordinator wrapper only. Does not aggregate subsystems, score health,
    or access the filesystem.
    """

    def __init__(
        self, *, service: OperationalStateServiceGate | None = None
    ) -> None:
        self._service: OperationalStateServiceGate = (
            service or FounderOperationalStateService()
        )

    def get_state(self) -> FounderOperationalState | None:
        """Return the current operational snapshot, or None on failure."""
        try:
            return self._service.get_state()
        except Exception:
            logger.exception(
                "Founder Dashboard: operational state unavailable"
            )
            return None
