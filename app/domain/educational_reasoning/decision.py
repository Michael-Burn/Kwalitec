"""Educational decisions produced by reasoning rules."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Any

from app.domain.educational_reasoning.explanation import Explanation


class DecisionKind(StrEnum):
    """Kinds of educational decisions the engine may emit."""

    MASTERY_UPDATE = "mastery_update"
    CONFIDENCE_ADJUSTMENT = "confidence_adjustment"
    KNOWLEDGE_GAP = "knowledge_gap"
    PREREQUISITE = "prerequisite"
    RECOMMENDATION = "recommendation"
    MOMENTUM = "momentum"
    CONSISTENCY = "consistency"
    READINESS = "readiness"
    LEARNING_STATE = "learning_state"


@dataclass(frozen=True)
class EducationalDecision:
    """One structured educational decision from a rule execution."""

    decision_id: str
    kind: DecisionKind
    rule_code: str
    twin_id: str
    subject_ref: str
    value: float
    explanation: Explanation
    created_at: datetime
    observation_ids: tuple[str, ...] = ()
    curriculum_evidence_ids: tuple[str, ...] = ()
    payload: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        if not (self.decision_id or "").strip():
            raise ValueError("decision_id is required")
        kind = (
            self.kind
            if isinstance(self.kind, DecisionKind)
            else DecisionKind(str(self.kind))
        )
        object.__setattr__(self, "kind", kind)
        when = self.created_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "created_at", when.astimezone(UTC).replace(tzinfo=None)
            )
        object.__setattr__(self, "observation_ids", tuple(self.observation_ids or ()))
        object.__setattr__(
            self, "curriculum_evidence_ids", tuple(self.curriculum_evidence_ids or ())
        )
        object.__setattr__(self, "payload", MappingProxyType(dict(self.payload or {})))

    def as_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "kind": self.kind.value,
            "rule_code": self.rule_code,
            "twin_id": self.twin_id,
            "subject_ref": self.subject_ref,
            "value": self.value,
            "explanation": self.explanation.as_dict(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "observation_ids": list(self.observation_ids),
            "curriculum_evidence_ids": list(self.curriculum_evidence_ids),
            "payload": dict(self.payload),
        }
