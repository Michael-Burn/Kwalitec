"""Structured educational evidence returned by retrieval — never raw vector hits."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.curriculum_retrieval.intent import QueryIntent
from app.domain.curriculum_retrieval.profile import RetrievalProfile
from app.domain.curriculum_retrieval.ranking import RankingBreakdown


@dataclass(frozen=True)
class EvidenceItem:
    """One supporting educational evidence fragment."""

    evidence_id: str
    role: str
    excerpt: str
    page_number: int | None = None
    provenance_id: str | None = None
    entity_id: str | None = None


@dataclass(frozen=True)
class RankedEvidence:
    """One ranked educational entity with trust and ranking metadata."""

    entity_id: str
    kind: str
    title: str
    body: str
    document_id: int
    version_label: str
    confidence: float
    confidence_band: str
    verified: bool
    provenance_id: str | None
    rank_score: float
    ranking: RankingBreakdown
    evidence: tuple[EvidenceItem, ...]
    prerequisites: tuple[str, ...]
    related_concepts: tuple[str, ...]
    supporting_formulae: tuple[str, ...]
    worked_examples: tuple[str, ...]
    practice_questions: tuple[str, ...]
    learning_objectives: tuple[str, ...]
    graph_distance: int | None = None
    source_pages: tuple[int, ...] = ()


@dataclass(frozen=True)
class RetrievalDiagnostics:
    """Explainable retrieval trace for Founder diagnostics (no vector internals)."""

    intent: QueryIntent
    profile: RetrievalProfile
    candidate_count: int
    graph_expanded_count: int
    metadata_filtered_count: int
    vector_hit_count: int
    ranked_count: int
    seed_entity_ids: tuple[str, ...]
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class RetrievalResult:
    """Rich educational retrieval result for one query.

    Represents curriculum knowledge rather than text snippets alone.
    """

    query_text: str
    intent: QueryIntent
    profile: RetrievalProfile
    results: tuple[RankedEvidence, ...]
    concept_ids: tuple[str, ...]
    learning_objective_ids: tuple[str, ...]
    definition_ids: tuple[str, ...]
    formula_ids: tuple[str, ...]
    example_ids: tuple[str, ...]
    practice_question_ids: tuple[str, ...]
    prerequisite_ids: tuple[str, ...]
    related_concept_ids: tuple[str, ...]
    diagnostics: RetrievalDiagnostics | None = None
    retrieval_log_id: str | None = None
