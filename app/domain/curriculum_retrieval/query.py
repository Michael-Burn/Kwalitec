"""Retrieval query contract."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.curriculum_retrieval.intent import QueryIntent
from app.domain.curriculum_retrieval.profile import RetrievalProfile


@dataclass(frozen=True)
class RetrievalQuery:
    """Input to CurriculumRetrievalService.

    Consumers supply educational intent; they must not specify vector tech.
    """

    text: str
    workspace_id: str
    profile: RetrievalProfile = RetrievalProfile.KNOWLEDGE_SEARCH
    intent: QueryIntent | None = None
    document_id: int | None = None
    subject_code: str = ""
    version_label: str = ""
    entity_kinds: tuple[str, ...] = ()
    require_verified: bool = False
    min_confidence: float = 0.0
    limit: int = 10
    expand_graph_hops: int = 1
    seed_entity_id: str | None = None
    include_diagnostics: bool = False
