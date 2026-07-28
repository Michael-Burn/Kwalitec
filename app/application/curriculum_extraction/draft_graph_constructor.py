"""Draft Curriculum Graph Construction — assemble CKG aggregate + provenance."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.curriculum_extraction.educational_object_extractor import (
    ExtractedCatalogue,
)
from app.application.curriculum_extraction.relationship_discovery_service import (
    DiscoveredRelationships,
)
from app.domain.curriculum_extraction.provenance import ExtractionProvenance
from app.domain.curriculum_knowledge_graph.graph.curriculum_knowledge_graph import (
    CurriculumKnowledgeGraph,
)


@dataclass
class DraftGraphBundle:
    """In-memory draft graph candidate prior to validation / persist."""

    graph: CurriculumKnowledgeGraph
    provenance: dict[str, ExtractionProvenance]
    explicit_requires_numbers: list[tuple[str, str]]
    diagnostics: list[str]


class DraftGraphConstructor:
    """Materialise CurriculumKnowledgeGraph from catalogue + relationships."""

    STAGE_ID = "draft_graph_construction"

    def construct(
        self,
        catalogue: ExtractedCatalogue,
        relationships: DiscoveredRelationships,
    ) -> DraftGraphBundle:
        """Assemble the draft CKG aggregate. Raises on duplicate/cycle."""
        graph = CurriculumKnowledgeGraph(subject=catalogue.subject)
        diagnostics = list(catalogue.diagnostics) + list(
            relationships.diagnostics
        )
        for node in catalogue.nodes:
            if node.stable_id.value == catalogue.subject.stable_id.value:
                continue
            graph.add_node(node)
        for edge in relationships.edges:
            try:
                graph.add_edge(edge)
            except ValueError as exc:
                diagnostics.append(f"Edge skipped: {edge.edge_id} ({exc})")

        # Ensure every node has provenance (fallback synthetic if missing).
        provenance = dict(catalogue.provenance)
        missing = [
            n.stable_id.value
            for n in graph.nodes()
            if n.stable_id.value not in provenance
        ]
        if missing:
            diagnostics.append(
                f"Missing provenance for {len(missing)} nodes after construct"
            )

        return DraftGraphBundle(
            graph=graph,
            provenance=provenance,
            explicit_requires_numbers=list(
                relationships.explicit_requires_numbers
            ),
            diagnostics=diagnostics,
        )
