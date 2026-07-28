"""Inference context and rule contribution protocol (EI-006)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Protocol

from app.domain.learning_evidence.evidence_event import EvidenceEvent


@dataclass(frozen=True)
class RuleContribution:
    """Atomic, explainable effect emitted by one inference rule."""

    rule_id: str
    mastery_delta: float
    confidence_delta: float
    weight: float
    evidence_ids: tuple[str, ...] = ()
    detail: str = ""

    def weighted_mastery(self) -> float:
        return float(self.mastery_delta) * float(self.weight)

    def weighted_confidence(self) -> float:
        return float(self.confidence_delta) * float(self.weight)


@dataclass(frozen=True)
class InferenceContext:
    """Immutable inputs for a single node inference pass.

    Evidence must already be filtered (e.g. corrected rows excluded) and
    ordered chronologically. Prerequisite mastery map is optional and used by
    the prerequisite-awareness rule only.
    """

    instance_id: str
    node_stable_id: str
    evidence: tuple[EvidenceEvent, ...]
    as_of: datetime
    prerequisite_mastery: dict[str, float] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


class InferenceRule(Protocol):
    """Modular, independently testable inference rule."""

    @property
    def rule_id(self) -> str:
        """Stable rule identifier for explainability."""

    def apply(self, context: InferenceContext) -> tuple[RuleContribution, ...]:
        """Return zero or more deterministic contributions for the context."""
