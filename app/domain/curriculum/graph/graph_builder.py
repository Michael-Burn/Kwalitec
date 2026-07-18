"""GraphBuilder — construct a CurriculumGraph from curriculum entities."""

from __future__ import annotations

from app.domain.curriculum.entities.curriculum import Curriculum
from app.domain.curriculum.entities.dependency import Dependency
from app.domain.curriculum.entities.prerequisite import Prerequisite
from app.domain.curriculum.entities.revision_link import RevisionLink
from app.domain.curriculum.entities.topic import Topic
from app.domain.curriculum.graph.curriculum_graph import CurriculumGraph
from app.domain.curriculum.graph.graph_node import GraphNode
from app.domain.curriculum.value_objects.dependency_type import DependencyType


class GraphBuilder:
    """Deterministic builder from Curriculum / Topic collections to a graph."""

    def build_from_curriculum(self, curriculum: Curriculum) -> CurriculumGraph:
        """Build a graph from a Curriculum aggregate.

        Includes:
        - All topics as nodes
        - Explicit Dependency entities as edges
        - Prerequisite entities as REQUIRES edges
        - RevisionLink entities as bidirectional REVISION edges
        """
        graph = CurriculumGraph()
        for topic in curriculum.all_topics():
            graph.add_topic(GraphNode.from_topic(topic))

        for dep in curriculum.dependencies:
            self._add_dependency(graph, dep)

        for prereq in curriculum.prerequisites:
            self._add_prerequisite(graph, prereq)

        for link in curriculum.revision_links:
            self._add_revision_link(graph, link)

        return graph

    def build_from_topics(
        self,
        topics: list[Topic] | tuple[Topic, ...],
        *,
        dependencies: list[Dependency] | tuple[Dependency, ...] | None = None,
        prerequisites: list[Prerequisite] | tuple[Prerequisite, ...] | None = None,
        revision_links: list[RevisionLink] | tuple[RevisionLink, ...] | None = None,
    ) -> CurriculumGraph:
        """Build a graph from a flat topic list and relationship collections."""
        graph = CurriculumGraph()
        for topic in topics:
            graph.add_topic(GraphNode.from_topic(topic))
        for dep in dependencies or ():
            self._add_dependency(graph, dep)
        for prereq in prerequisites or ():
            self._add_prerequisite(graph, prereq)
        for link in revision_links or ():
            self._add_revision_link(graph, link)
        return graph

    def _add_dependency(self, graph: CurriculumGraph, dep: Dependency) -> None:
        graph.connect_topics(
            dep.source_topic_id,
            dep.target_topic_id,
            dep.dependency_type,
            edge_id=dep.dependency_id,
            rationale=dep.rationale,
        )

    def _add_prerequisite(
        self, graph: CurriculumGraph, prereq: Prerequisite
    ) -> None:
        # topic REQUIRES required_topic
        edge_id = prereq.as_dependency_id()
        key = (
            prereq.topic_id.value,
            prereq.required_topic_id.value,
            DependencyType.REQUIRES.value,
        )
        # Skip if an equivalent REQUIRES edge already exists from Dependency.
        existing = {
            (
                e.source_id.value,
                e.target_id.value,
                e.dependency_type.value,
            )
            for e in graph.edges()
        }
        if key in existing:
            return
        graph.connect_topics(
            prereq.topic_id,
            prereq.required_topic_id,
            DependencyType.REQUIRES,
            edge_id=edge_id,
            rationale=prereq.rationale,
        )

    def _add_revision_link(
        self, graph: CurriculumGraph, link: RevisionLink
    ) -> None:
        # Bidirectional REVISION edges for neighbour queries.
        a, b = link.topic_a_id, link.topic_b_id
        existing = {
            (
                e.source_id.value,
                e.target_id.value,
                e.dependency_type.value,
            )
            for e in graph.edges()
        }
        forward = (a.value, b.value, DependencyType.REVISION.value)
        reverse = (b.value, a.value, DependencyType.REVISION.value)
        if forward not in existing:
            graph.connect_topics(
                a,
                b,
                DependencyType.REVISION,
                edge_id=f"{link.revision_link_id}:a-b",
                rationale=link.rationale,
            )
        if reverse not in existing:
            graph.connect_topics(
                b,
                a,
                DependencyType.REVISION,
                edge_id=f"{link.revision_link_id}:b-a",
                rationale=link.rationale,
            )
