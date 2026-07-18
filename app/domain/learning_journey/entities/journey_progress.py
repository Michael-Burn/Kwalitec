"""Derived educational progress for a Learning Journey.

Models objectives addressed, evidence accumulated, sessions completed,
consistency, and confidence of available evidence. Does not estimate mastery
or assign unsupported competence scores.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.domain.learning_journey.value_objects.completion_status import CompletionStatus


class ConsistencyPosture(StrEnum):
    """Qualitative consistency of engagement across sessions.

    Derived from completed-session spacing patterns — not a streak game score.
    """

    NONE = "none"
    SPARSE = "sparse"
    REGULAR = "regular"
    UNKNOWN = "unknown"


class EvidenceConfidencePosture(StrEnum):
    """Aggregate qualitative confidence of accumulated journey evidence.

    Mirrors Learning Evidence Model confidence vocabulary honesty — not a
    numeric warrant weight or mastery estimate.
    """

    UNKNOWN = "unknown"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    THIN = "thin"


@dataclass(frozen=True)
class JourneyProgress:
    """Evidence-aware educational progress posture for a journey.

    Attributes:
        objectives_total: Objectives bound to the journey.
        objectives_addressed: Objectives with at least one session or evidence.
        sessions_completed: Count of COMPLETED sessions.
        sessions_planned: Count of non-skipped sessions (including completed).
        evidence_count: Journey-scoped evidence attributions.
        reflections_captured: CAPTURED reflections.
        consistency: Engagement consistency posture.
        evidence_confidence: Aggregate evidence confidence posture.
        completion_status: Coverage / obligation completion posture.
        meets_completion_criteria: Whether READY_FOR_COMPLETION is warranted.
    """

    objectives_total: int
    objectives_addressed: int
    sessions_completed: int
    sessions_planned: int
    evidence_count: int
    reflections_captured: int
    consistency: ConsistencyPosture
    evidence_confidence: EvidenceConfidencePosture
    completion_status: CompletionStatus
    meets_completion_criteria: bool = False

    @classmethod
    def create(
        cls,
        *,
        objectives_total: int,
        objectives_addressed: int,
        sessions_completed: int,
        sessions_planned: int,
        evidence_count: int,
        reflections_captured: int,
        consistency: ConsistencyPosture | str = ConsistencyPosture.UNKNOWN,
        evidence_confidence: EvidenceConfidencePosture
        | str = EvidenceConfidencePosture.UNKNOWN,
        completion_status: CompletionStatus | str = CompletionStatus.NOT_STARTED,
        meets_completion_criteria: bool = False,
    ) -> JourneyProgress:
        """Construct JourneyProgress after validating non-negative counts.

        Raises:
            ValueError: When counts are negative or addressed exceeds total.
        """
        for name, value in (
            ("objectives_total", objectives_total),
            ("objectives_addressed", objectives_addressed),
            ("sessions_completed", sessions_completed),
            ("sessions_planned", sessions_planned),
            ("evidence_count", evidence_count),
            ("reflections_captured", reflections_captured),
        ):
            if value < 0:
                raise ValueError(f"{name} must be non-negative")
        if objectives_addressed > objectives_total:
            raise ValueError("objectives_addressed cannot exceed objectives_total")
        if sessions_completed > sessions_planned and sessions_planned > 0:
            raise ValueError("sessions_completed cannot exceed sessions_planned")
        cons = (
            consistency
            if isinstance(consistency, ConsistencyPosture)
            else ConsistencyPosture(consistency)
        )
        conf = (
            evidence_confidence
            if isinstance(evidence_confidence, EvidenceConfidencePosture)
            else EvidenceConfidencePosture(evidence_confidence)
        )
        status = (
            completion_status
            if isinstance(completion_status, CompletionStatus)
            else CompletionStatus(completion_status)
        )
        return cls(
            objectives_total=objectives_total,
            objectives_addressed=objectives_addressed,
            sessions_completed=sessions_completed,
            sessions_planned=sessions_planned,
            evidence_count=evidence_count,
            reflections_captured=reflections_captured,
            consistency=cons,
            evidence_confidence=conf,
            completion_status=status,
            meets_completion_criteria=meets_completion_criteria,
        )

    @classmethod
    def empty(cls) -> JourneyProgress:
        """Zero-progress posture for a newly created journey."""
        return cls.create(
            objectives_total=0,
            objectives_addressed=0,
            sessions_completed=0,
            sessions_planned=0,
            evidence_count=0,
            reflections_captured=0,
            consistency=ConsistencyPosture.NONE,
            evidence_confidence=EvidenceConfidencePosture.UNKNOWN,
            completion_status=CompletionStatus.NOT_STARTED,
            meets_completion_criteria=False,
        )
