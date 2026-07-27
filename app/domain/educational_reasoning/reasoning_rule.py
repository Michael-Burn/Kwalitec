"""Base contract for deterministic educational reasoning rules."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from app.domain.educational_reasoning.decision import EducationalDecision
from app.domain.educational_reasoning.explanation import Explanation
from app.domain.educational_reasoning.reasoning_context import ReasoningContext
from app.domain.student_digital_twin.confidence import ConfidenceState
from app.domain.student_digital_twin.knowledge_gap import KnowledgeGap
from app.domain.student_digital_twin.mastery import MasteryMap
from app.domain.student_digital_twin.recommendation import Recommendation


@dataclass(frozen=True)
class RuleExecution:
    """Structured output of one rule application."""

    rule_code: str
    rule_name: str
    explanation: Explanation
    decisions: tuple[EducationalDecision, ...] = ()
    mastery: MasteryMap | None = None
    confidence: ConfidenceState | None = None
    knowledge: float | None = None
    retention: float | None = None
    consistency: float | None = None
    momentum: float | None = None
    exam_readiness: float | None = None
    gaps: tuple[KnowledgeGap, ...] | None = None
    recommendations: tuple[Recommendation, ...] | None = None
    outputs: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    inputs: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        object.__setattr__(self, "decisions", tuple(self.decisions or ()))
        if self.gaps is not None:
            object.__setattr__(self, "gaps", tuple(self.gaps))
        if self.recommendations is not None:
            object.__setattr__(self, "recommendations", tuple(self.recommendations))
        object.__setattr__(self, "outputs", MappingProxyType(dict(self.outputs or {})))
        object.__setattr__(self, "inputs", MappingProxyType(dict(self.inputs or {})))


class ReasoningRule(ABC):
    """Deterministic educational rule — receive structured inputs, return outputs.

    Independently testable. Must produce a human-readable explanation.
    No LLM. No probabilistic AI. No direct database access.
    """

    code: str = ""
    name: str = ""
    description: str = ""

    @abstractmethod
    def apply(self, context: ReasoningContext) -> RuleExecution:
        """Apply this rule to the current reasoning context."""

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} code={self.code!r}>"
