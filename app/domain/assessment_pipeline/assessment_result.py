"""Assessment result — structured outcome of a validated assessment event."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any

from app.domain.assessment_pipeline.assessment_event import AssessmentEventType


def _freeze_metadata(metadata: Mapping[str, Any] | None) -> Mapping[str, Any]:
    return MappingProxyType(dict(metadata or {}))


@dataclass(frozen=True)
class AssessmentResult:
    """Immutable structured result derived from one assessment event.

    Records evidence metadata only — never Twin mastery or gap inferences.
    """

    result_id: str
    event_id: str
    twin_id: str
    event_type: AssessmentEventType
    observation_id: str
    performance_label: str
    evidence_generated: tuple[str, ...] = ()
    concepts_covered: tuple[str, ...] = ()
    confidence: float = 0.0
    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC).replace(tzinfo=None)
    )
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        if not (self.result_id or "").strip():
            raise ValueError("result_id is required")
        if not (self.event_id or "").strip():
            raise ValueError("event_id is required")
        if not (self.observation_id or "").strip():
            raise ValueError("observation_id is required")
        event_type = (
            self.event_type
            if isinstance(self.event_type, AssessmentEventType)
            else AssessmentEventType(str(self.event_type))
        )
        object.__setattr__(self, "event_type", event_type)
        when = self.created_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "created_at", when.astimezone(UTC).replace(tzinfo=None)
            )
        object.__setattr__(
            self, "evidence_generated", tuple(self.evidence_generated or ())
        )
        object.__setattr__(self, "concepts_covered", tuple(self.concepts_covered or ()))
        object.__setattr__(
            self, "confidence", max(0.0, min(1.0, float(self.confidence)))
        )
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))
