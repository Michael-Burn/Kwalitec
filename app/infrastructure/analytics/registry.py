"""Analytics event type registry (allowlist catalogue).

Phase A registers infrastructure probe types only. Domain event types
(Session, reflection, journey, ESS snapshot, Twin evolved) are added in
Phases B–E — not emitted here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.infrastructure.analytics.versioning import AnalyticsEventVersion

# Infrastructure-only probe for Phase A tests / health checks.
# Never used as a student-facing learning metric.
INFRASTRUCTURE_PROBE = "analytics.infrastructure_probe"

PHASE_A_EVENT_TYPES: tuple[str, ...] = (INFRASTRUCTURE_PROBE,)


@dataclass(frozen=True)
class EventTypeRegistration:
    """Registration record for one allowlisted analytics event type."""

    event_type: str
    current_version: AnalyticsEventVersion = AnalyticsEventVersion.V1
    description: str = ""
    # Reserved required payload keys for future domain contracts (Phase A: empty).
    required_payload_keys: tuple[str, ...] = ()


class AnalyticsEventRegistry:
    """Allowlist catalogue of known analytics event types."""

    def __init__(self) -> None:
        self._types: dict[str, EventTypeRegistration] = {}

    @classmethod
    def phase_a_default(cls) -> AnalyticsEventRegistry:
        """Build the Phase A default registry (infrastructure probe only)."""
        registry = cls()
        registry.register(
            EventTypeRegistration(
                event_type=INFRASTRUCTURE_PROBE,
                current_version=AnalyticsEventVersion.V1,
                description="Phase A infrastructure probe — not a learning metric",
            )
        )
        return registry

    def register(self, registration: EventTypeRegistration) -> None:
        """Register or replace an event type registration."""
        etype = (registration.event_type or "").strip()
        if not etype:
            raise ValueError("event_type is required")
        self._types[etype] = EventTypeRegistration(
            event_type=etype,
            current_version=registration.current_version,
            description=registration.description,
            required_payload_keys=tuple(registration.required_payload_keys),
        )

    def is_known(self, event_type: str) -> bool:
        """True when ``event_type`` is in the allowlist."""
        return (event_type or "").strip() in self._types

    def get(self, event_type: str) -> EventTypeRegistration | None:
        """Return registration or None."""
        return self._types.get((event_type or "").strip())

    @property
    def known_types(self) -> tuple[str, ...]:
        """Return known event types in registration order."""
        return tuple(self._types.keys())

    def diagnostics(self) -> dict[str, Any]:
        """Operational diagnostics for the registry."""
        return {
            "known_types": list(self.known_types),
            "count": len(self._types),
        }
