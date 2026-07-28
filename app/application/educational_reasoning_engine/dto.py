"""DTOs for Educational Reasoning Engine services (EI-007)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.domain.educational_reasoning_engine.decision import EducationalDecision
from app.domain.educational_reasoning_engine.engine import (
    ReasoningResult,
    ReasoningResultItem,
)
from app.domain.educational_reasoning_engine.explanation import DecisionExplanation


@dataclass(frozen=True)
class DecisionView:
    """Decision plus explanation for API/service consumers."""

    decision: EducationalDecision
    explanation: DecisionExplanation

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision.to_dict(),
            "explanation": self.explanation.to_dict(),
        }

    @classmethod
    def from_item(cls, item: ReasoningResultItem) -> DecisionView:
        return cls(decision=item.decision, explanation=item.explanation)


@dataclass(frozen=True)
class EvaluateDecisionsResult:
    """Outcome of evaluating / rebuilding decisions for one SCI."""

    instance_id: str
    decision_count: int
    reasoning_version: str
    decisions: tuple[DecisionView, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "decision_count": self.decision_count,
            "reasoning_version": self.reasoning_version,
            "decisions": [d.to_dict() for d in self.decisions],
        }

    @classmethod
    def from_result(cls, result: ReasoningResult) -> EvaluateDecisionsResult:
        views = tuple(DecisionView.from_item(i) for i in result.items)
        return cls(
            instance_id=result.instance_id,
            decision_count=len(views),
            reasoning_version=result.reasoning_version,
            decisions=views,
        )
