"""ExperienceObservationPublisher — one-way Experience → Evidence (P2-MS006).

Publishes immutable ExperienceObservation records through the Learning
Evidence Platform public observation interface only. Never writes
persistence, never interprets educationally, never changes authority.

Optional P2-MS007 diagnostics hooks record JourneyTrace / counters when
``ENABLE_EXPERIENCE_DIAGNOSTICS`` is wired — observational only.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from app.application.unified_journey.events import JourneyEvent
from app.application.unified_journey.reflection_experience import (
    ReflectionExperience,
)
from app.application.unified_journey.session_outcome import SessionOutcome
from app.infrastructure.adapters.experience_observation.assembler import (
    ObservationAssembler,
)
from app.infrastructure.adapters.experience_observation.contracts import (
    PUBLISH_STATUS_FAILED,
    PUBLISH_STATUS_PUBLISHED,
    PUBLISH_STATUS_SKIPPED,
    REASON_EVIDENCE_REJECTED,
    REASON_EVIDENCE_UNAVAILABLE,
    REASON_FLAG_OFF,
    REASON_NOT_OBSERVABLE,
    EvidenceObservationPort,
    ExperienceObservation,
    ObservationPublishResult,
)
from app.infrastructure.adapters.experience_observation.evidence_mapper import (
    observation_to_observed_event,
)
from app.infrastructure.diagnostics.correlation import CorrelationContext

if TYPE_CHECKING:
    from app.infrastructure.adapters.experience_observation.diagnostics import (
        ObservationDiagnosticsService,
    )

logger = logging.getLogger(__name__)


class ExperienceObservationPublisher:
    """Publish immutable Experience observations to Evidence.

    Responsibilities:
    - publish immutable observations
    - respect feature flags
    - support dependency injection
    - optionally emit operational JourneyTrace / diagnostics (P2-MS007)

    Non-responsibilities: persistence, educational interpretation,
    recommendation generation, Evidence scoring / analytics, direct
    repository access.
    """

    PUBLISHER_ID = "experience_observation_publisher"
    PUBLISHER_VERSION = "1.0.0-p2.ms006"

    def __init__(
        self,
        *,
        enabled: bool = True,
        evidence: EvidenceObservationPort | None = None,
        assembler: ObservationAssembler | None = None,
        diagnostics: ObservationDiagnosticsService | None = None,
    ) -> None:
        self._enabled = bool(enabled)
        self._evidence = evidence
        self._assembler = assembler or ObservationAssembler()
        self._diagnostics = diagnostics

    @property
    def publisher_id(self) -> str:
        return self.PUBLISHER_ID

    @property
    def publisher_version(self) -> str:
        return self.PUBLISHER_VERSION

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def evidence(self) -> EvidenceObservationPort | None:
        return self._evidence

    @property
    def assembler(self) -> ObservationAssembler:
        return self._assembler

    @property
    def diagnostics(self) -> ObservationDiagnosticsService | None:
        return self._diagnostics

    def bind_diagnostics(
        self, diagnostics: ObservationDiagnosticsService | None
    ) -> None:
        """Late-bind diagnostics after DI construction (composition)."""
        self._diagnostics = diagnostics

    def _record_diagnostics(
        self,
        result: ObservationPublishResult,
        *,
        timestamp: str | None = None,
        latency_ms: float | None = None,
    ) -> None:
        if self._diagnostics is None:
            return
        try:
            self._diagnostics.record_publish(
                result, timestamp=timestamp, latency_ms=latency_ms
            )
        except Exception as exc:  # noqa: BLE001 — diagnostics must not break publish
            logger.warning(
                "experience_diagnostics_record_failed error=%s",
                exc,
            )

    def _record_journey_event(
        self,
        *,
        experience_event: str,
        journey_stage: str,
        timestamp: str,
        correlation_id: str,
        observation_id: str = "",
    ) -> None:
        if self._diagnostics is None:
            return
        try:
            self._diagnostics.record_journey_event(
                experience_event=experience_event,
                journey_stage=journey_stage,
                timestamp=timestamp,
                correlation_id=correlation_id,
                observation_id=observation_id,
            )
        except Exception as exc:  # noqa: BLE001 — diagnostics must not break publish
            logger.warning(
                "experience_diagnostics_journey_trace_failed error=%s",
                exc,
            )

    def publish(
        self, observation: ExperienceObservation
    ) -> ObservationPublishResult:
        """Publish one observation through Evidence's public intake API."""
        if not isinstance(observation, ExperienceObservation):
            raise TypeError("observation must be an ExperienceObservation")
        if not self._enabled:
            result = ObservationPublishResult(
                ok=False,
                status=PUBLISH_STATUS_SKIPPED,
                observation=observation,
                reason=REASON_FLAG_OFF,
                message="ENABLE_EXPERIENCE_OBSERVATION is OFF",
            )
            self._record_diagnostics(result)
            return result
        if not self._assembler.is_observable_event(observation.experience_event):
            result = ObservationPublishResult(
                ok=False,
                status=PUBLISH_STATUS_SKIPPED,
                observation=observation,
                reason=REASON_NOT_OBSERVABLE,
                message=(
                    f"experience_event {observation.experience_event!r} "
                    "is outside the P2-MS006 observation set"
                ),
            )
            self._record_diagnostics(result)
            return result
        if self._evidence is None:
            result = ObservationPublishResult(
                ok=False,
                status=PUBLISH_STATUS_SKIPPED,
                observation=observation,
                reason=REASON_EVIDENCE_UNAVAILABLE,
                message=(
                    "Evidence observation port unavailable "
                    "(ENABLE_EVIDENCE_PLATFORM OFF or not injected)"
                ),
            )
            self._record_diagnostics(result)
            return result
        latency_ms: float | None = None
        try:
            observed_event = observation_to_observed_event(observation)
            started = time.perf_counter()
            record = self._evidence.collect_event(observed_event)
            latency_ms = round((time.perf_counter() - started) * 1000.0, 3)
        except Exception as exc:  # noqa: BLE001 — observational bridge must not raise
            logger.warning(
                "experience_observation_publish_failed observation_id=%s error=%s",
                observation.observation_id,
                exc,
            )
            result = ObservationPublishResult(
                ok=False,
                status=PUBLISH_STATUS_FAILED,
                observation=observation,
                reason=REASON_EVIDENCE_REJECTED,
                message=str(exc),
            )
            self._record_diagnostics(result, latency_ms=latency_ms)
            return result
        evidence_id = str(getattr(record, "evidence_id", "") or "").strip()
        result = ObservationPublishResult(
            ok=True,
            status=PUBLISH_STATUS_PUBLISHED,
            observation=observation,
            evidence_id=evidence_id,
            message="published via EvidencePlatformAdapter.collect_event",
        )
        self._record_diagnostics(result, latency_ms=latency_ms)
        return result

    def publish_journey_event(
        self,
        event: JourneyEvent,
        *,
        student_id: str,
        timestamp: str,
        correlation_id: str | None = None,
        presentation_state: Mapping[str, Any] | None = None,
        metadata: Mapping[str, str] | tuple[tuple[str, str], ...] | None = None,
    ) -> ObservationPublishResult:
        """Assemble a JourneyEvent observation and publish it."""
        corr = (correlation_id or "").strip() or CorrelationContext.get_correlation_id()
        if not self._enabled:
            self._record_journey_event(
                experience_event=str(event.event_type),
                journey_stage=str(event.stage),
                timestamp=timestamp,
                correlation_id=corr,
            )
            result = ObservationPublishResult(
                ok=False,
                status=PUBLISH_STATUS_SKIPPED,
                reason=REASON_FLAG_OFF,
                message="ENABLE_EXPERIENCE_OBSERVATION is OFF",
            )
            self._record_diagnostics(result, timestamp=timestamp)
            return result
        observation = self._assembler.assemble_from_journey_event(
            event,
            student_id=student_id,
            timestamp=timestamp,
            correlation_id=corr,
            presentation_state=presentation_state,
            metadata=metadata,
        )
        self._record_journey_event(
            experience_event=observation.experience_event,
            journey_stage=observation.journey_stage,
            timestamp=timestamp,
            correlation_id=corr,
            observation_id=observation.observation_id,
        )
        return self.publish(observation)

    def publish_session_outcome(
        self,
        outcome: SessionOutcome,
        *,
        student_id: str,
        timestamp: str,
        experience_event: str,
        journey_stage: str = "study_session",
        correlation_id: str | None = None,
        presentation_state: Mapping[str, Any] | None = None,
        metadata: Mapping[str, str] | tuple[tuple[str, str], ...] | None = None,
    ) -> ObservationPublishResult:
        """Assemble a SessionOutcome observation and publish it."""
        corr = (correlation_id or "").strip() or CorrelationContext.get_correlation_id()
        if not self._enabled:
            self._record_journey_event(
                experience_event=experience_event,
                journey_stage=journey_stage,
                timestamp=timestamp,
                correlation_id=corr,
            )
            result = ObservationPublishResult(
                ok=False,
                status=PUBLISH_STATUS_SKIPPED,
                reason=REASON_FLAG_OFF,
                message="ENABLE_EXPERIENCE_OBSERVATION is OFF",
            )
            self._record_diagnostics(result, timestamp=timestamp)
            return result
        observation = self._assembler.assemble_from_session_outcome(
            outcome,
            student_id=student_id,
            timestamp=timestamp,
            experience_event=experience_event,
            journey_stage=journey_stage,
            correlation_id=corr,
            presentation_state=presentation_state,
            metadata=metadata,
        )
        self._record_journey_event(
            experience_event=observation.experience_event,
            journey_stage=observation.journey_stage,
            timestamp=timestamp,
            correlation_id=corr,
            observation_id=observation.observation_id,
        )
        return self.publish(observation)

    def publish_reflection(
        self,
        reflection: ReflectionExperience,
        *,
        student_id: str,
        timestamp: str,
        experience_event: str,
        journey_stage: str = "session_reflection",
        correlation_id: str | None = None,
        presentation_state: Mapping[str, Any] | None = None,
        metadata: Mapping[str, str] | tuple[tuple[str, str], ...] | None = None,
    ) -> ObservationPublishResult:
        """Assemble a ReflectionExperience observation and publish it."""
        corr = (correlation_id or "").strip() or CorrelationContext.get_correlation_id()
        if not self._enabled:
            self._record_journey_event(
                experience_event=experience_event,
                journey_stage=journey_stage,
                timestamp=timestamp,
                correlation_id=corr,
            )
            result = ObservationPublishResult(
                ok=False,
                status=PUBLISH_STATUS_SKIPPED,
                reason=REASON_FLAG_OFF,
                message="ENABLE_EXPERIENCE_OBSERVATION is OFF",
            )
            self._record_diagnostics(result, timestamp=timestamp)
            return result
        observation = self._assembler.assemble_from_reflection(
            reflection,
            student_id=student_id,
            timestamp=timestamp,
            experience_event=experience_event,
            journey_stage=journey_stage,
            correlation_id=corr,
            presentation_state=presentation_state,
            metadata=metadata,
        )
        self._record_journey_event(
            experience_event=observation.experience_event,
            journey_stage=observation.journey_stage,
            timestamp=timestamp,
            correlation_id=corr,
            observation_id=observation.observation_id,
        )
        return self.publish(observation)


def build_experience_observation_publisher(
    *,
    enabled: bool,
    evidence: EvidenceObservationPort | None = None,
    assembler: ObservationAssembler | None = None,
    diagnostics: ObservationDiagnosticsService | None = None,
) -> ExperienceObservationPublisher | None:
    """DI helper — construct publisher only when ENABLE_EXPERIENCE_OBSERVATION is ON."""
    if not enabled:
        return None
    return ExperienceObservationPublisher(
        enabled=True,
        evidence=evidence,
        assembler=assembler or ObservationAssembler(),
        diagnostics=diagnostics,
    )
