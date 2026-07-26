"""Student Digital Twin Authority seam (EP-001.1).

When ``ENABLE_DIGITAL_TWIN_AUTHORITY`` is ON (and Digital Twin is ON),
Experience ``StudentTwinPort`` serves Runtime-A-grounded Foundation state.
Falls back to the prior Experience Twin adapter on assemble failure.
Default remains OFF — no UX cutover without explicit flag.
"""

from __future__ import annotations

import logging
from typing import Any

from app.infrastructure.adapters.digital_twin.foundation import (
    CanonicalLearnerState,
    StudentDigitalTwinFoundation,
)

logger = logging.getLogger(__name__)

AUTHORITY_ADAPTER_ID = "student_twin_foundation_authority"
AUTHORITY_ADAPTER_VERSION = "ep001.1.0"


class StudentTwinFoundationAuthorityPort:
    """StudentTwinPort backed by Student Digital Twin Foundation.

    Rules:
    - MAY assemble Foundation / serve opaque summaries
    - MUST NOT write Runtime A or invent educational scores
    - MUST fall back to ``fallback`` when Foundation is unavailable
    """

    ADAPTER_ID = AUTHORITY_ADAPTER_ID
    ADAPTER_VERSION = AUTHORITY_ADAPTER_VERSION

    def __init__(
        self,
        *,
        foundation: StudentDigitalTwinFoundation,
        fallback: Any | None = None,
        enabled: bool = True,
    ) -> None:
        self._foundation = foundation
        self._fallback = fallback
        self._enabled = bool(enabled)

    @property
    def component_id(self) -> str:
        return self.ADAPTER_ID

    @property
    def component_version(self) -> str:
        return self.ADAPTER_VERSION

    def is_available(self) -> bool:
        return self._enabled and self._foundation.is_enabled()

    def foundation(self) -> StudentDigitalTwinFoundation:
        return self._foundation

    def get_canonical_state(self, student_id: str) -> CanonicalLearnerState | None:
        """Return Foundation state, or None when authority is unavailable."""
        if not self.is_available():
            return None
        try:
            return self._foundation.assemble(student_id)
        except Exception:  # noqa: BLE001
            logger.debug(
                "foundation assemble failed student_id=%s",
                student_id,
                exc_info=True,
            )
            return None

    def get_learner_summary(self, student_id: str) -> dict[str, Any] | None:
        state = self.get_canonical_state(student_id)
        if state is not None and state.availability == "available":
            return state.to_learner_summary_opaque()
        if self._fallback is not None:
            return self._fallback.get_learner_summary(student_id)
        if state is not None:
            return state.to_learner_summary_opaque()
        return None

    def get_readiness_summary(self, student_id: str) -> dict[str, Any] | None:
        state = self.get_canonical_state(student_id)
        if state is not None and state.availability == "available":
            return state.to_readiness_summary_opaque()
        if self._fallback is not None:
            return self._fallback.get_readiness_summary(student_id)
        if state is not None:
            return state.to_readiness_summary_opaque()
        return None

    def get_learning_insights(self, student_id: str) -> dict[str, Any] | None:
        state = self.get_canonical_state(student_id)
        if state is not None and state.availability == "available":
            return state.to_learning_insights_opaque()
        if self._fallback is not None:
            return self._fallback.get_learning_insights(student_id)
        if state is not None:
            return state.to_learning_insights_opaque()
        return None


def build_student_twin_foundation_authority_port(
    *,
    enabled: bool,
    foundation: StudentDigitalTwinFoundation | None,
    fallback: Any | None = None,
) -> StudentTwinFoundationAuthorityPort | None:
    """DI helper — construct Authority port only when Authority flag is ON."""
    if not enabled or foundation is None:
        return None
    return StudentTwinFoundationAuthorityPort(
        foundation=foundation,
        fallback=fallback,
        enabled=True,
    )


__all__ = [
    "AUTHORITY_ADAPTER_ID",
    "AUTHORITY_ADAPTER_VERSION",
    "StudentTwinFoundationAuthorityPort",
    "build_student_twin_foundation_authority_port",
]
