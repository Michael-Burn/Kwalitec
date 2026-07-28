"""Immutable EducationalDecision — reasoning output, not Twin state."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any

from app.domain.reasoning.decisions.category import (
    DecisionCategory,
    parse_decision_category,
)
from app.domain.reasoning.decisions.reason import DecisionReason
from app.domain.reasoning.decisions.reference import DecisionReference


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    return MappingProxyType(dict(value or {}))


@dataclass(frozen=True)
class EducationalDecision:
    """One immutable educational decision derived from observations.

    Decisions request Twin belief updates. They never schedule Missions,
    trigger Tutor, or estimate exam readiness.
    """

    decision_id: str
    category: DecisionCategory
    twin_id: str
    subject_ref: str
    value: Any
    reason: DecisionReason
    reference: DecisionReference
    decision_version: str
    created_at: datetime
    provenance: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )
    traceability: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )
    payload: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        if not (self.decision_id or "").strip():
            raise ValueError("decision_id is required")
        if not (self.twin_id or "").strip():
            raise ValueError("twin_id is required")
        if not (self.decision_version or "").strip():
            raise ValueError("decision_version is required")
        if not isinstance(self.reason, DecisionReason):
            raise TypeError("reason must be DecisionReason")
        if not isinstance(self.reference, DecisionReference):
            raise TypeError("reference must be DecisionReference")

        category = parse_decision_category(self.category)
        object.__setattr__(self, "category", category)

        when = self.created_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "created_at", when.astimezone(UTC).replace(tzinfo=None)
            )

        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))
        object.__setattr__(self, "traceability", _freeze_mapping(self.traceability))
        object.__setattr__(self, "payload", _freeze_mapping(self.payload))
        if isinstance(self.value, Mapping):
            object.__setattr__(self, "value", _freeze_mapping(self.value))
