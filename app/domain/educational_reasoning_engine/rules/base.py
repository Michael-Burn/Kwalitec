"""Reasoning context and rule proposal protocol (EI-007)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from app.domain.educational_reasoning_engine.context import ReasoningContext


@dataclass(frozen=True)
class RuleProposal:
    """Atomic, explainable proposal emitted by one reasoning rule.

    Proposals with a decision_type seed a candidate decision. Proposals with
    ``decision_type=None`` contribute priority (and optional effort) to any
    merged candidate sharing the same curriculum_target.
    """

    rule_id: str
    curriculum_target: str
    priority_delta: float
    decision_type: str | None = None
    rationale: str = ""
    prerequisite_chain: tuple[str, ...] = ()
    estimated_effort_minutes: int | None = None
    expected_educational_outcome: str = ""
    supporting_belief_ids: tuple[str, ...] = ()
    supporting_curriculum_refs: tuple[str, ...] = ()
    supporting_evidence_ids: tuple[str, ...] = ()
    detail: str = ""


class ReasoningRule(Protocol):
    """Modular, independently testable reasoning rule."""

    @property
    def rule_id(self) -> str:
        """Stable rule identifier for explainability."""

    def apply(self, context: ReasoningContext) -> tuple[RuleProposal, ...]:
        """Return zero or more deterministic proposals for the context."""
