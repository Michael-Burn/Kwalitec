"""KnowledgeGraphProvider — load KnowledgeGraph for orchestration."""

from __future__ import annotations

from abc import ABC, abstractmethod

from domain.education.knowledge_graph.aggregates.knowledge_graph import (
    KnowledgeGraph,
)


class KnowledgeGraphProvider(ABC):
    """Outbound port for reading the educational knowledge graph.

    Implementations live in infrastructure. This package defines the
    interface only — no SQLAlchemy, no graph databases here.
    """

    @abstractmethod
    def get_knowledge_graph(self, student_id: str) -> KnowledgeGraph:
        """Return the knowledge graph applicable to ``student_id``.

        Raises:
            application.errors.NotFoundError: When no graph is available.
            application.errors.ApplicationError: On coordination failure.
        """
