"""Curriculum Knowledge Graph package."""

from __future__ import annotations

from app.domain.curriculum_knowledge_graph.graph.curriculum_knowledge_graph import (
    CurriculumKnowledgeGraph,
)
from app.domain.curriculum_knowledge_graph.graph.edge import CkgEdge

__all__ = ["CkgEdge", "CurriculumKnowledgeGraph"]
