"""Knowledge Architecture — Curriculum Intelligence Phase 1 (KWP-014).

Represents educational knowledge as a structured curriculum graph.
Educational Intelligence uses the graph; it does not replace it.

Does not redesign Learning Runtime, Evidence, Progress, Strategy,
Diagnostics, Difficulty, Intervention Effectiveness, Educational Memory,
Forecast, Adaptive Workspace, or Mission Runtime.
"""

from __future__ import annotations

from app.application.knowledge_architecture.dto import (
    MAP_STATUS_TITLES,
    RELATIONSHIP_TITLES,
    REVISION_PATH_TITLES,
    CurriculumMap,
    CurriculumMapNode,
    CurriculumPathway,
    DifficultyAttention,
    EducationalRelationship,
    KnowledgeArchitectureSnapshot,
    LearnerGraphContext,
    MapTopicStatus,
    PrerequisiteExplanation,
    RevisionPathKind,
    RevisionPathway,
    TopicEdgeView,
    TopicNodeView,
)
from app.application.knowledge_architecture.engine import (
    KnowledgeArchitectureEngine,
    get_knowledge_architecture_engine,
    reset_knowledge_architecture_engine,
)

__all__ = [
    "MAP_STATUS_TITLES",
    "RELATIONSHIP_TITLES",
    "REVISION_PATH_TITLES",
    "CurriculumMap",
    "CurriculumMapNode",
    "CurriculumPathway",
    "DifficultyAttention",
    "EducationalRelationship",
    "KnowledgeArchitectureEngine",
    "KnowledgeArchitectureSnapshot",
    "LearnerGraphContext",
    "MapTopicStatus",
    "PrerequisiteExplanation",
    "RevisionPathKind",
    "RevisionPathway",
    "TopicEdgeView",
    "TopicNodeView",
    "get_knowledge_architecture_engine",
    "reset_knowledge_architecture_engine",
]
