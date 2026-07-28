"""Immutable EducationalObservation — interpreted evidence, not belief."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any

from app.domain.reasoning.observations.category import (
    ObservationCategory,
    parse_observation_category,
)


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    return MappingProxyType(dict(value or {}))


@dataclass(frozen=True)
class EducationalObservation:
    """One immutable educational observation derived from assessment evidence.

    Observations give educational meaning to organised facts. They never
    estimate mastery, update learner state, or author recommendations.
    """

    observation_id: str
    evidence_reference: str
    learning_objective_reference: str
    concept_reference: str
    category: ObservationCategory
    value: Any
    provenance: str
    interpretation_version: str
    recorded_at: datetime
    reasoning_request_id: str
    evidence_bundle_id: str
    session_id: str
    correlation_id: str
    source_observation_id: str = ""
    question_reference: str | None = None
    traceability: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not (self.observation_id or "").strip():
            raise ValueError("observation_id is required")
        if not (self.evidence_reference or "").strip():
            raise ValueError("evidence_reference is required")
        if not (self.learning_objective_reference or "").strip():
            raise ValueError("learning_objective_reference is required")
        if not (self.provenance or "").strip():
            raise ValueError("provenance is required")
        if not (self.interpretation_version or "").strip():
            raise ValueError("interpretation_version is required")
        if not (self.reasoning_request_id or "").strip():
            raise ValueError("reasoning_request_id is required")
        if not (self.evidence_bundle_id or "").strip():
            raise ValueError("evidence_bundle_id is required")
        if not (self.session_id or "").strip():
            raise ValueError("session_id is required")
        if not (self.correlation_id or "").strip():
            raise ValueError("correlation_id is required")

        category = parse_observation_category(self.category)
        object.__setattr__(self, "category", category)

        when = self.recorded_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "recorded_at", when.astimezone(UTC).replace(tzinfo=None)
            )

        object.__setattr__(self, "traceability", _freeze_mapping(self.traceability))
        if isinstance(self.value, Mapping):
            object.__setattr__(self, "value", _freeze_mapping(self.value))
