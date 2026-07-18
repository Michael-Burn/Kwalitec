"""Stateless evidence admission policy."""

from __future__ import annotations

from app.application.student_twin.exceptions import EvidenceRejected, PolicyViolation
from app.domain.student_twin.digital_twin import DigitalTwin
from app.domain.student_twin.evidence_event import EvidenceEvent
from app.domain.student_twin.evidence_type import EvidenceType


class EvidencePolicy:
    """Deterministic rules for admitting evidence into the Twin."""

    MAX_METADATA_PAIRS = 32
    MAX_DURATION_SECONDS = 24 * 60 * 60

    @staticmethod
    def validate_event(event: EvidenceEvent) -> None:
        """Raise EvidenceRejected when the event is inadmissible."""
        if not isinstance(event.evidence_type, EvidenceType):
            raise EvidenceRejected("evidence_type must be a lawful EvidenceType")
        if event.duration_seconds is not None:
            if event.duration_seconds > EvidencePolicy.MAX_DURATION_SECONDS:
                raise EvidenceRejected(
                    f"duration_seconds exceeds maximum "
                    f"({EvidencePolicy.MAX_DURATION_SECONDS})"
                )
        if len(event.metadata) > EvidencePolicy.MAX_METADATA_PAIRS:
            raise EvidenceRejected("metadata exceeds maximum pair count")
        # Reject curriculum/PDF-shaped metadata keys.
        forbidden = {"pdf", "curriculum_json", "ai_response", "prompt"}
        for key, _ in event.metadata:
            if key.strip().lower() in forbidden:
                raise EvidenceRejected(
                    f"metadata key {key!r} is not lawful Twin evidence"
                )

    @staticmethod
    def assert_admissible(twin: DigitalTwin, event: EvidenceEvent) -> None:
        """Validate event and ensure it is not already in Twin history."""
        EvidencePolicy.validate_event(event)
        if event.event_id in twin.history.event_ids:
            raise PolicyViolation(f"duplicate evidence event_id: {event.event_id!r}")
        if twin.identity.learner_id and event.topic_id is None:
            # Topic-less events are allowed for session/time signals.
            return
