"""Analytics event type registry (allowlist catalogue).

Phase A: infrastructure probe only.
Phase B: Study Session events (``session.started`` / ``session.completed``).
Phase C: Reflection events (``reflection.submitted`` / ``reflection.completed``).
Phase D: Educational State snapshot (``educational_state.snapshot`` hash + metadata).
Phase E: Journey progression + Twin evolution (``journey.progressed`` /
``twin.evolved``) — Twin emitted after persist; Journey production emit
deferred pending durable repository (ADR-026).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.infrastructure.analytics.versioning import AnalyticsEventVersion

# Infrastructure-only probe for Phase A tests / health checks.
# Never used as a student-facing learning metric.
INFRASTRUCTURE_PROBE = "analytics.infrastructure_probe"

# PRD-001 Phase B — Study Session lifecycle (metadata only).
SESSION_STARTED = "session.started"
SESSION_COMPLETED = "session.completed"

# PRD-001 Phase C — Reflection lifecycle (metadata only; no body text).
REFLECTION_SUBMITTED = "reflection.submitted"
REFLECTION_COMPLETED = "reflection.completed"

# PRD-001 Phase D — Educational State observation (hash + metadata only).
EDUCATIONAL_STATE_SNAPSHOT = "educational_state.snapshot"

# PRD-001 Phase E — Journey progression + Twin evolution (metadata only).
JOURNEY_PROGRESSED = "journey.progressed"
TWIN_EVOLVED = "twin.evolved"

PHASE_A_EVENT_TYPES: tuple[str, ...] = (INFRASTRUCTURE_PROBE,)
PHASE_B_EVENT_TYPES: tuple[str, ...] = (SESSION_STARTED, SESSION_COMPLETED)
PHASE_C_EVENT_TYPES: tuple[str, ...] = (REFLECTION_SUBMITTED, REFLECTION_COMPLETED)
PHASE_D_EVENT_TYPES: tuple[str, ...] = (EDUCATIONAL_STATE_SNAPSHOT,)
PHASE_E_EVENT_TYPES: tuple[str, ...] = (JOURNEY_PROGRESSED, TWIN_EVOLVED)


@dataclass(frozen=True)
class EventTypeRegistration:
    """Registration record for one allowlisted analytics event type."""

    event_type: str
    current_version: AnalyticsEventVersion = AnalyticsEventVersion.V1
    description: str = ""
    # Required payload keys enforced by the validator at dispatch time.
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

    @classmethod
    def phase_b_default(cls) -> AnalyticsEventRegistry:
        """Build the Phase B registry (probe + Study Session events)."""
        registry = cls.phase_a_default()
        registry.register(
            EventTypeRegistration(
                event_type=SESSION_STARTED,
                current_version=AnalyticsEventVersion.V1,
                description="Student begins a Study Session (O1/O2)",
                required_payload_keys=("session_id", "mission_id"),
            )
        )
        registry.register(
            EventTypeRegistration(
                event_type=SESSION_COMPLETED,
                current_version=AnalyticsEventVersion.V1,
                description=(
                    "Student closes a Study Session — completion_status is "
                    "completed or abandoned_after_start (canonical cancel)"
                ),
                required_payload_keys=(
                    "session_id",
                    "mission_id",
                    "completion_status",
                ),
            )
        )
        return registry

    @classmethod
    def phase_c_default(cls) -> AnalyticsEventRegistry:
        """Build the Phase C registry (probe + Session + Reflection events)."""
        registry = cls.phase_b_default()
        registry.register(
            EventTypeRegistration(
                event_type=REFLECTION_SUBMITTED,
                current_version=AnalyticsEventVersion.V1,
                description="Student submits a structured reflection (O7)",
                required_payload_keys=(
                    "reflection_id",
                    "session_id",
                    "student_id",
                    "reflection_type",
                ),
            )
        )
        registry.register(
            EventTypeRegistration(
                event_type=REFLECTION_COMPLETED,
                current_version=AnalyticsEventVersion.V1,
                description=(
                    "Reflection reaches canonical completed processing_status"
                ),
                required_payload_keys=("reflection_id", "processing_status"),
            )
        )
        return registry

    @classmethod
    def phase_d_default(cls) -> AnalyticsEventRegistry:
        """Build the Phase D registry (A–C + Educational State snapshot)."""
        registry = cls.phase_c_default()
        registry.register(
            EventTypeRegistration(
                event_type=EDUCATIONAL_STATE_SNAPSHOT,
                current_version=AnalyticsEventVersion.V1,
                description=(
                    "Material Educational State assembly change — "
                    "content_hash + metadata only (no ESS payload)"
                ),
                required_payload_keys=("snapshot_id", "content_hash"),
            )
        )
        return registry

    @classmethod
    def phase_e_default(cls) -> AnalyticsEventRegistry:
        """Build the Phase E registry (A–D + Journey + Twin observation)."""
        registry = cls.phase_d_default()
        registry.register(
            EventTypeRegistration(
                event_type=JOURNEY_PROGRESSED,
                current_version=AnalyticsEventVersion.V1,
                description=(
                    "Learning Journey lawful transition after durable save — "
                    "metadata only (ADR-026; production emit deferred)"
                ),
                required_payload_keys=(
                    "journey_id",
                    "curriculum_node_id",
                    "transition_id",
                ),
            )
        )
        registry.register(
            EventTypeRegistration(
                event_type=TWIN_EVOLVED,
                current_version=AnalyticsEventVersion.V1,
                description=(
                    "Durable Twin snapshot succession — "
                    "snapshot_hash + metadata only (no Twin payload)"
                ),
                required_payload_keys=(
                    "twin_snapshot_id",
                    "twin_version",
                    "evolution_reason",
                    "snapshot_hash",
                ),
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
