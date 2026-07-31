"""Knowledge Architecture Engine — Curriculum Intelligence Phase 1 (KWP-014).

Models curriculum topics as a structured graph and answers
"Why does this topic matter?" from explicit relationships.

Educational Intelligence *uses* the graph — this module does not replace
Learning Runtime, Evidence, Progress, Strategy, Diagnostics, Difficulty,
Intervention Effectiveness, Educational Memory, Forecast, Adaptive
Workspace internals, or Mission Runtime.
"""

from __future__ import annotations

import logging
from typing import Any

from app.application.knowledge_architecture.curriculum_map import (
    build_curriculum_map,
)
from app.application.knowledge_architecture.difficulty_propagation import (
    propagate_difficulty_attention,
)
from app.application.knowledge_architecture.dto import (
    CurriculumMap,
    CurriculumPathway,
    DifficultyAttention,
    KnowledgeArchitectureSnapshot,
    LearnerGraphContext,
    PrerequisiteExplanation,
    RevisionPathway,
    TopicEdgeView,
    TopicNodeView,
)
from app.application.knowledge_architecture.graph_adapter import (
    graph_from_learner_package,
    graph_from_topic_specs,
)
from app.application.knowledge_architecture.pathways import (
    pathways_from_curriculum,
    pathways_from_graph,
)
from app.application.knowledge_architecture.prerequisite_reasoning import (
    explain_topic,
    why_topic_matters,
)
from app.application.knowledge_architecture.relationships import educational_for
from app.application.knowledge_architecture.revision_paths import (
    generate_revision_paths,
)
from app.domain.curriculum.entities.curriculum import Curriculum
from app.domain.curriculum.graph.curriculum_graph import CurriculumGraph
from app.domain.curriculum.graph.graph_builder import GraphBuilder
from app.domain.curriculum.value_objects.dependency_type import DependencyType

logger = logging.getLogger(__name__)


class KnowledgeArchitectureEngine:
    """Deterministic curriculum knowledge architecture over CurriculumGraph."""

    AUTHORITY_ID = "knowledge_architecture_engine"
    AUTHORITY_VERSION = "1.0.0"

    def __init__(self, graph: CurriculumGraph | None = None) -> None:
        self._graph = graph if graph is not None else CurriculumGraph()

    @property
    def graph(self) -> CurriculumGraph:
        return self._graph

    @classmethod
    def from_topic_specs(
        cls, topics: list[dict[str, Any]] | tuple[dict[str, Any], ...]
    ) -> KnowledgeArchitectureEngine:
        return cls(graph_from_topic_specs(topics))

    @classmethod
    def from_learner_package(
        cls, package: dict[str, Any] | None
    ) -> KnowledgeArchitectureEngine:
        return cls(graph_from_learner_package(package))

    @classmethod
    def from_curriculum(cls, curriculum: Curriculum) -> KnowledgeArchitectureEngine:
        return cls(GraphBuilder().build_from_curriculum(curriculum))

    def nodes(self) -> tuple[TopicNodeView, ...]:
        views: list[TopicNodeView] = []
        for node in self._graph.nodes():
            tid = node.topic_id.value
            views.append(
                TopicNodeView(
                    topic_id=tid,
                    title=node.name,
                    difficulty=node.difficulty.value,
                    estimated_minutes=node.estimated_effort_minutes,
                    prerequisite_ids=tuple(
                        p.value for p in self._graph.find_prerequisites(tid)
                    ),
                    successor_ids=tuple(
                        s.value for s in self._graph.find_successors(tid)
                    ),
                )
            )
        return tuple(views)

    def edges(self) -> tuple[TopicEdgeView, ...]:
        views: list[TopicEdgeView] = []
        for edge in self._graph.edges():
            views.append(
                TopicEdgeView(
                    from_topic_id=edge.source_id.value,
                    to_topic_id=edge.target_id.value,
                    relationship=educational_for(edge.dependency_type),
                    rationale=edge.rationale or "",
                )
            )
        return tuple(views)

    def explain(
        self,
        topic_id: str,
        *,
        context: LearnerGraphContext | None = None,
    ) -> PrerequisiteExplanation:
        return explain_topic(self._graph, topic_id, context=context)

    def why_matters(
        self,
        topic_id: str,
        *,
        context: LearnerGraphContext | None = None,
    ) -> str:
        return why_topic_matters(self._graph, topic_id, context=context)

    def pathways(
        self, curriculum: Curriculum | None = None
    ) -> tuple[CurriculumPathway, ...]:
        if curriculum is not None:
            return pathways_from_curriculum(curriculum, self._graph)
        return pathways_from_graph(self._graph)

    def revision_paths(
        self,
        *,
        context: LearnerGraphContext | None = None,
        seed_topic_id: str = "",
        limit: int = 4,
    ) -> tuple[RevisionPathway, ...]:
        return generate_revision_paths(
            self._graph,
            context=context,
            seed_topic_id=seed_topic_id,
            limit=limit,
        )

    def difficulty_attention(
        self,
        *,
        context: LearnerGraphContext | None = None,
        source_topic_id: str = "",
    ) -> DifficultyAttention:
        return propagate_difficulty_attention(
            self._graph,
            context=context,
            source_topic_id=source_topic_id,
        )

    def curriculum_map(
        self,
        *,
        context: LearnerGraphContext | None = None,
        subject_label: str = "",
        curriculum: Curriculum | None = None,
    ) -> CurriculumMap:
        return build_curriculum_map(
            self._graph,
            context=context,
            subject_label=subject_label,
            pathways=self.pathways(curriculum),
        )

    def completeness_ratio(self) -> float:
        """Share of topics that participate in at least one relationship."""
        total = self._graph.topic_count()
        if total == 0:
            return 0.0
        connected: set[str] = set()
        for edge in self._graph.edges():
            connected.add(edge.source_id.value)
            connected.add(edge.target_id.value)
        return len(connected) / total

    def dependency_bottlenecks(self, *, limit: int = 5) -> tuple[str, ...]:
        """Topics with the most dependents (prerequisite bottlenecks)."""
        scored: list[tuple[int, str]] = []
        for node in self._graph.nodes():
            tid = node.topic_id.value
            score = len(self._graph.find_successors(tid))
            if score > 0:
                scored.append((score, tid))
        scored.sort(key=lambda x: (-x[0], x[1]))
        return tuple(tid for _, tid in scored[:limit])

    def difficult_prerequisite_chains(
        self, *, limit: int = 5
    ) -> tuple[tuple[str, ...], ...]:
        """Longest REQUIRES chains (by ancestor depth)."""
        chains: list[tuple[str, ...]] = []
        for node in self._graph.nodes():
            tid = node.topic_id.value
            ancestors = self._graph.all_prerequisites(tid, transitive=True)
            if not ancestors:
                continue
            chain = tuple(a.value for a in ancestors) + (tid,)
            chains.append(chain)
        chains.sort(key=lambda c: (-len(c), c))
        return tuple(chains[:limit])

    def snapshot(
        self,
        *,
        subject_label: str = "",
        context: LearnerGraphContext | None = None,
        curriculum: Curriculum | None = None,
    ) -> KnowledgeArchitectureSnapshot:
        paths = self.pathways(curriculum)
        revision = self.revision_paths(context=context)
        prereq_edges = sum(
            1
            for e in self._graph.edges()
            if e.dependency_type is DependencyType.REQUIRES
        )
        revision_edges = sum(
            1
            for e in self._graph.edges()
            if e.dependency_type is DependencyType.REVISION
        )
        recovery_ids = tuple(
            p.kind.value for p in revision if p.kind.value == "recovery"
        )
        return KnowledgeArchitectureSnapshot(
            subject_label=subject_label,
            node_count=self._graph.topic_count(),
            edge_count=self._graph.edge_count(),
            prerequisite_edge_count=prereq_edges,
            revision_edge_count=revision_edges,
            pathway_count=len(paths),
            revision_paths_generated=len(revision),
            completeness_ratio=self.completeness_ratio(),
            bottleneck_topic_ids=self.dependency_bottlenecks(),
            common_recovery_path_ids=recovery_ids,
        )


_ENGINE: KnowledgeArchitectureEngine | None = None


def get_knowledge_architecture_engine() -> KnowledgeArchitectureEngine:
    """Process-wide default engine (empty until loaded from curriculum)."""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = KnowledgeArchitectureEngine()
    return _ENGINE


def reset_knowledge_architecture_engine() -> None:
    """Test helper — clear the process-wide engine."""
    global _ENGINE
    _ENGINE = None
