"""ObservationAssembler — Experience facts → ExperienceObservation (P2-MS006).

Translates JourneyEvent / SessionOutcome / ReflectionExperience into
immutable factual observations. No interpretation, enrichment, scoring,
or educational conclusions.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.application.unified_journey.events import JourneyEvent, JourneyEventType
from app.application.unified_journey.reflection_experience import (
    ReflectionExperience,
)
from app.application.unified_journey.session_outcome import SessionOutcome
from app.infrastructure.adapters.experience_observation.contracts import (
    CONTRACT_VERSION,
    OBSERVABLE_EXPERIENCE_EVENTS,
    ExperienceObservation,
    deterministic_observation_id,
)

_ASSEMBLER_VIA = "observation_assembler"


class ObservationAssembler:
    """Translate Experience presentation artefacts into factual observations.

    Responsibilities:
    - consume JourneyEvent
    - consume SessionOutcome
    - consume ReflectionExperience
    - produce immutable ExperienceObservation

    Non-responsibilities: interpretation, enrichment, scoring, persistence,
    recommendation generation, Evidence writes.
    """

    ASSEMBLER_VERSION = "1.0.0-p2.ms006"

    def assemble_from_journey_event(
        self,
        event: JourneyEvent,
        *,
        student_id: str,
        timestamp: str,
        correlation_id: str = "",
        presentation_state: Mapping[str, Any] | None = None,
        metadata: Mapping[str, str] | tuple[tuple[str, str], ...] | None = None,
    ) -> ExperienceObservation:
        """Map a JourneyEvent into an immutable ExperienceObservation."""
        if not isinstance(event, JourneyEvent):
            raise TypeError("event must be a JourneyEvent")
        experience_event = str(event.event_type.value)
        state = {
            "journey_stage": str(event.stage.value),
            "experience_event": experience_event,
            "message": event.message,
            "contract_version": event.contract_version,
        }
        if presentation_state:
            state.update({str(k): v for k, v in presentation_state.items()})
        return self._build(
            student_id=student_id,
            timestamp=timestamp,
            journey_stage=str(event.stage.value),
            experience_event=experience_event,
            presentation_state=state,
            metadata=self._merge_metadata(
                event.metadata,
                metadata,
                source="journey_event",
            ),
            correlation_id=correlation_id,
        )

    def assemble_from_session_outcome(
        self,
        outcome: SessionOutcome,
        *,
        student_id: str,
        timestamp: str,
        experience_event: str,
        journey_stage: str = "study_session",
        correlation_id: str = "",
        presentation_state: Mapping[str, Any] | None = None,
        metadata: Mapping[str, str] | tuple[tuple[str, str], ...] | None = None,
    ) -> ExperienceObservation:
        """Map a SessionOutcome into an immutable ExperienceObservation."""
        if not isinstance(outcome, SessionOutcome):
            raise TypeError("outcome must be a SessionOutcome")
        event_name = (experience_event or "").strip().lower()
        state = {
            "mission_title": outcome.mission_title,
            "completion_status": outcome.completion_status,
            "reflection_available": outcome.reflection_available,
            "summary_message": outcome.summary_message,
            "next_transition": outcome.next_transition,
            "upcoming_action": outcome.upcoming_action,
            "contract_version": outcome.contract_version,
        }
        if presentation_state:
            state.update({str(k): v for k, v in presentation_state.items()})
        return self._build(
            student_id=student_id,
            timestamp=timestamp,
            journey_stage=journey_stage,
            experience_event=event_name,
            presentation_state=state,
            metadata=self._merge_metadata(
                outcome.metadata,
                metadata,
                source="session_outcome",
            ),
            correlation_id=correlation_id,
        )

    def assemble_from_reflection(
        self,
        reflection: ReflectionExperience,
        *,
        student_id: str,
        timestamp: str,
        experience_event: str,
        journey_stage: str = "session_reflection",
        correlation_id: str = "",
        presentation_state: Mapping[str, Any] | None = None,
        metadata: Mapping[str, str] | tuple[tuple[str, str], ...] | None = None,
    ) -> ExperienceObservation:
        """Map a ReflectionExperience into an immutable ExperienceObservation."""
        if not isinstance(reflection, ReflectionExperience):
            raise TypeError("reflection must be a ReflectionExperience")
        event_name = (experience_event or "").strip().lower()
        state = {
            "reflection_state": str(reflection.reflection_state.value),
            "headline": reflection.headline,
            "supporting_message": reflection.supporting_message,
            "next_transition": reflection.next_transition,
            "skip_available": reflection.skip_available,
            "prompt_count": len(reflection.prompts),
            "completion_status": reflection.session_outcome.completion_status,
            "contract_version": reflection.contract_version,
        }
        if presentation_state:
            state.update({str(k): v for k, v in presentation_state.items()})
        return self._build(
            student_id=student_id,
            timestamp=timestamp,
            journey_stage=journey_stage,
            experience_event=event_name,
            presentation_state=state,
            metadata=self._merge_metadata(
                reflection.metadata,
                metadata,
                source="reflection_experience",
            ),
            correlation_id=correlation_id,
        )

    def is_observable_event(self, experience_event: str | JourneyEventType) -> bool:
        """Return True when the event is in the P2-MS006 observation set."""
        if isinstance(experience_event, JourneyEventType):
            value = experience_event.value
        else:
            value = (experience_event or "").strip().lower()
        return value in OBSERVABLE_EXPERIENCE_EVENTS

    def _build(
        self,
        *,
        student_id: str,
        timestamp: str,
        journey_stage: str,
        experience_event: str,
        presentation_state: Mapping[str, Any],
        metadata: tuple[tuple[str, str], ...],
        correlation_id: str,
    ) -> ExperienceObservation:
        sid = (student_id or "").strip()
        ts = (timestamp or "").strip()
        stage = (journey_stage or "").strip().lower()
        event_name = (experience_event or "").strip().lower()
        corr = (correlation_id or "").strip()
        observation_id = deterministic_observation_id(
            student_id=sid,
            timestamp=ts,
            journey_stage=stage,
            experience_event=event_name,
            presentation_state=presentation_state,
            metadata=metadata,
            correlation_id=corr,
        )
        return ExperienceObservation(
            observation_id=observation_id,
            timestamp=ts,
            journey_stage=stage,
            experience_event=event_name,
            presentation_state=presentation_state,
            metadata=metadata,
            correlation_id=corr,
            student_id=sid,
            contract_version=CONTRACT_VERSION,
        )

    @staticmethod
    def _merge_metadata(
        source_meta: tuple[tuple[str, str], ...],
        extra: Mapping[str, str] | tuple[tuple[str, str], ...] | None,
        *,
        source: str,
    ) -> tuple[tuple[str, str], ...]:
        merged: list[tuple[str, str]] = list(source_meta or ())
        if isinstance(extra, Mapping):
            merged.extend((str(k), str(v)) for k, v in sorted(extra.items()))
        elif extra:
            merged.extend((str(k), str(v)) for k, v in extra)
        merged.append(("via", _ASSEMBLER_VIA))
        merged.append(("source", source))
        # Preserve insertion order while dropping exact duplicates.
        seen: set[tuple[str, str]] = set()
        unique: list[tuple[str, str]] = []
        for item in merged:
            if item in seen:
                continue
            seen.add(item)
            unique.append(item)
        return tuple(unique)


def build_observation_assembler(
    *,
    enabled: bool = True,
) -> ObservationAssembler | None:
    """DI helper — construct ObservationAssembler when the flag is on."""
    if not enabled:
        return None
    return ObservationAssembler()
