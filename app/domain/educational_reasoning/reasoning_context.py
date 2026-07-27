"""Reasoning context — structured inputs for the Educational Reasoning Engine."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any

from app.domain.curriculum_retrieval.result import RankedEvidence, RetrievalResult
from app.domain.learning_graph.learning_graph import LearningGraph
from app.domain.student_digital_twin.confidence import ConfidenceState
from app.domain.student_digital_twin.knowledge_gap import KnowledgeGap
from app.domain.student_digital_twin.mastery import MasteryMap
from app.domain.student_digital_twin.observation import Observation
from app.domain.student_digital_twin.recommendation import Recommendation


@dataclass(frozen=True)
class CurriculumEvidenceBundle:
    """Curriculum evidence retrieved before educational rules execute.

    Stage 2 of the educational pipeline. Rules must not retrieve curriculum
    evidence independently — they consume this bundle.
    """

    by_concept: Mapping[str, RetrievalResult] = field(
        default_factory=lambda: MappingProxyType({})
    )
    all_evidence_ids: tuple[str, ...] = ()
    retrieval_log_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "by_concept", MappingProxyType(dict(self.by_concept or {}))
        )
        object.__setattr__(
            self, "all_evidence_ids", tuple(self.all_evidence_ids or ())
        )
        object.__setattr__(
            self, "retrieval_log_ids", tuple(self.retrieval_log_ids or ())
        )

    def for_concept(self, concept_id: str) -> RetrievalResult | None:
        return self.by_concept.get(concept_id)

    def top_for_concept(self, concept_id: str) -> RankedEvidence | None:
        result = self.for_concept(concept_id)
        if result is None or not result.results:
            return None
        return result.results[0]

    @classmethod
    def empty(cls) -> CurriculumEvidenceBundle:
        return cls()


@dataclass(frozen=True)
class ReasoningContext:
    """Immutable inputs plus accumulators for a single reasoning cycle.

    Rules receive this context and return updates; the registry merges outputs
    into a new context for subsequent rules.
    """

    twin_id: str
    student_id: str
    workspace_id: str
    subject_code: str
    observations: tuple[Observation, ...]
    observation_ids: tuple[str, ...]
    prior_mastery: MasteryMap
    curriculum_evidence: CurriculumEvidenceBundle
    triggered_by: str
    computed_at: datetime
    # Learner knowledge interconnection (SDT-003). Optional for backward compat;
    # when present, prerequisite / recovery rules prefer graph traversal.
    learning_graph: LearningGraph | None = None
    # Accumulators (filled by prior rules in the same cycle)
    mastery: MasteryMap | None = None
    confidence: ConfidenceState | None = None
    knowledge: float | None = None
    retention: float | None = None
    consistency: float | None = None
    momentum: float | None = None
    exam_readiness: float | None = None
    gaps: tuple[KnowledgeGap, ...] = ()
    recommendations: tuple[Recommendation, ...] = ()
    scratch: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        if not (self.twin_id or "").strip():
            raise ValueError("twin_id is required")
        when = self.computed_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "computed_at", when.astimezone(UTC).replace(tzinfo=None)
            )
        object.__setattr__(self, "observations", tuple(self.observations or ()))
        object.__setattr__(
            self, "observation_ids", tuple(self.observation_ids or ())
        )
        object.__setattr__(self, "gaps", tuple(self.gaps or ()))
        object.__setattr__(
            self, "recommendations", tuple(self.recommendations or ())
        )
        object.__setattr__(self, "scratch", MappingProxyType(dict(self.scratch or {})))

    def with_updates(self, **kwargs: Any) -> ReasoningContext:
        """Return a new context with selected fields replaced."""
        return replace(self, **kwargs)

    @property
    def effective_mastery(self) -> MasteryMap:
        return self.mastery if self.mastery is not None else self.prior_mastery
