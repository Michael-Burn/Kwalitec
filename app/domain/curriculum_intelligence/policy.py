"""Educational Policy contracts — deterministic decision rules (EI-001C).

Policies define educational decision rules. Agents execute those policies.
No LLM. Same inputs → same decisions.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.domain.curriculum_intelligence.evidence import EvidenceGrade


class ConceptAction(StrEnum):
    """Concept Formation outcomes for a learning unit."""

    MERGE = "merge"
    SPLIT = "split"
    RETAIN = "retain"


class ObjectiveKind(StrEnum):
    """Kinds of educational associations attached in Generation 5."""

    LEARNING_OBJECTIVE = "learning_objective"
    COMPETENCY = "competency"
    KNOWLEDGE_STATEMENT = "knowledge_statement"
    EXAM_EXPECTATION = "exam_expectation"


@dataclass(frozen=True)
class EducationalDecision:
    """Explainable outcome of applying an Educational Policy.

    Every decision includes reason, evidence, confidence, policy id,
    and the highest supporting Evidence Grade.
    """

    decision_id: str
    action: str
    subject_node_ids: tuple[str, ...]
    reason: str
    evidence_refs: tuple[str, ...]
    confidence: float
    policy_id: str
    evidence_grade: EvidenceGrade
    related_node_ids: tuple[str, ...] = ()
    detail: str = ""
    syllabus_ref: str | None = None


@dataclass(frozen=True)
class PolicyDescriptor:
    """Metadata every Educational Policy must expose."""

    policy_id: str
    name: str
    purpose: str
    version: str
    deterministic: bool
    generation_index: int
