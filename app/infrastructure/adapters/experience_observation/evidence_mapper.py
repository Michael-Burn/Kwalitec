"""Map ExperienceObservation → Evidence ObservedEvent (P2-MS006).

Factual projection only. No educational interpretation, scoring, or
enrichment beyond Evidence intake contract requirements.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.infrastructure.adapters.evidence_platform.contracts import (
    CLAIM_ORGANISATION,
    CLASS_DELIVERY_EVENT,
    REF_KIND_EXPERIENCE,
    ObservationRef,
    ObservedEvent,
)
from app.infrastructure.adapters.experience_observation.contracts import (
    ExperienceObservation,
)


def observation_to_observed_event(
    observation: ExperienceObservation,
    *,
    ingested_at: str | None = None,
) -> ObservedEvent:
    """Project an ExperienceObservation onto Evidence ObservedEvent.

    Uses Evidence public intake fields only. Claim boundary remains
    ``organisation`` — presentation facts, not learning-depth claims.
    """
    if not isinstance(observation, ExperienceObservation):
        raise TypeError("observation must be an ExperienceObservation")
    ts = observation.timestamp
    ingested = (ingested_at or ts or "").strip() or None
    presentation = dict(observation.presentation_state)
    metadata = {k: v for k, v in observation.metadata}
    experience_block: dict[str, Any] = {
        "observation_id": observation.observation_id,
        "journey_stage": observation.journey_stage,
        "experience_event": observation.experience_event,
        "presentation_state": presentation,
        "contract_version": observation.contract_version,
        "authority": observation.authority,
        "correlation_id": observation.correlation_id,
        "metadata": metadata,
    }
    payload_summary: dict[str, Any] = {
        "observation_id": observation.observation_id,
        "experience_event": observation.experience_event,
        "journey_stage": observation.journey_stage,
        "correlation_id": observation.correlation_id,
    }
    source_ref = ObservationRef(
        ref_kind=REF_KIND_EXPERIENCE,
        entity_kind="experience_observation",
        entity_id=observation.observation_id,
        fingerprint=observation.observation_id,
        observed_at=ts or None,
        as_of=ts or None,
        student_id=observation.student_id,
        claim_boundary=CLAIM_ORGANISATION,
    )
    return ObservedEvent(
        student_id=observation.student_id,
        event_type=observation.experience_event,
        observed_at=ts or None,
        ingested_at=ingested,
        as_of=ts or None,
        claim_boundary=CLAIM_ORGANISATION,
        evidence_class=CLASS_DELIVERY_EVENT,
        source_refs=(source_ref,),
        experience=experience_block,
        payload_summary=payload_summary,
        limitations=("experience_observation_bridge",),
    )


def presentation_state_from_mapping(
    value: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Copy a presentation-state mapping without mutation."""
    return {str(k): v for k, v in dict(value or {}).items()}
