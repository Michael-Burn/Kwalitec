"""Aggregated result of one Educational Reasoning Engine cycle."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.educational_reasoning.decision import EducationalDecision
from app.domain.educational_reasoning.explanation import Explanation
from app.domain.educational_reasoning.reasoning_context import (
    CurriculumEvidenceBundle,
    ReasoningContext,
)
from app.domain.educational_reasoning.reasoning_rule import RuleExecution
from app.domain.student_digital_twin.confidence import ConfidenceState
from app.domain.student_digital_twin.knowledge_gap import KnowledgeGap
from app.domain.student_digital_twin.learning_state import LearningState
from app.domain.student_digital_twin.mastery import MasteryMap
from app.domain.student_digital_twin.recommendation import Recommendation


@dataclass(frozen=True)
class ReasoningResult:
    """Immutable record of one complete reasoning cycle.

    Contains triggering observations, curriculum evidence, rules executed,
    outputs, explanations, and timestamp — the auditable reasoning history unit.
    """

    run_id: str
    twin_id: str
    triggered_by: str
    observation_ids: tuple[str, ...]
    curriculum_evidence: CurriculumEvidenceBundle
    executions: tuple[RuleExecution, ...]
    decisions: tuple[EducationalDecision, ...]
    explanations: tuple[Explanation, ...]
    mastery: MasteryMap
    confidence: ConfidenceState
    learning_state: LearningState
    gaps: tuple[KnowledgeGap, ...]
    recommendations: tuple[Recommendation, ...]
    summary: str
    created_at: datetime
    engine_version: str
    final_context: ReasoningContext | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        if not (self.run_id or "").strip():
            raise ValueError("run_id is required")
        when = self.created_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "created_at", when.astimezone(UTC).replace(tzinfo=None)
            )
        object.__setattr__(
            self, "observation_ids", tuple(self.observation_ids or ())
        )
        object.__setattr__(self, "executions", tuple(self.executions or ()))
        object.__setattr__(self, "decisions", tuple(self.decisions or ()))
        object.__setattr__(self, "explanations", tuple(self.explanations or ()))
        object.__setattr__(self, "gaps", tuple(self.gaps or ()))
        object.__setattr__(
            self, "recommendations", tuple(self.recommendations or ())
        )
