"""Relationship Discovery — wire EI-001 typed educational edges."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.application.curriculum_extraction.educational_object_extractor import (
    ExtractedCatalogue,
)
from app.application.curriculum_extraction.models import CurriculumSegmentTree
from app.domain.curriculum_knowledge_graph.entities.definition import Definition
from app.domain.curriculum_knowledge_graph.entities.formula import Formula
from app.domain.curriculum_knowledge_graph.entities.learning_objective import (
    LearningObjective,
)
from app.domain.curriculum_knowledge_graph.entities.practice_exercise import (
    PracticeExercise,
)
from app.domain.curriculum_knowledge_graph.entities.reading_reference import (
    ReadingReference,
)
from app.domain.curriculum_knowledge_graph.entities.section import Section
from app.domain.curriculum_knowledge_graph.entities.subsection import Subsection
from app.domain.curriculum_knowledge_graph.entities.syllabus_outcome import (
    SyllabusOutcome,
)
from app.domain.curriculum_knowledge_graph.entities.topic import Topic
from app.domain.curriculum_knowledge_graph.entities.worked_example import (
    WorkedExample,
)
from app.domain.curriculum_knowledge_graph.graph.edge import CkgEdge
from app.domain.curriculum_knowledge_graph.value_objects.relationship_type import (
    CkgRelationshipType,
)
from app.domain.curriculum_knowledge_graph.value_objects.stable_curriculum_id import (
    StableCurriculumId,
    StableIdDepth,
)


@dataclass
class DiscoveredRelationships:
    """Typed edges ready for graph construction."""

    edges: list[CkgEdge] = field(default_factory=list)
    explicit_requires_numbers: list[tuple[str, str]] = field(
        default_factory=list
    )
    diagnostics: list[str] = field(default_factory=list)


class RelationshipDiscoveryService:
    """Derive contains / references / requires / cross_references edges."""

    STAGE_ID = "relationship_discovery"

    def discover(
        self,
        catalogue: ExtractedCatalogue,
        tree: CurriculumSegmentTree,
    ) -> DiscoveredRelationships:
        """Build educational relationships from ownership and cues."""
        result = DiscoveredRelationships()
        self._containment_edges(catalogue, result)
        self._object_reference_edges(catalogue, result)
        self._prerequisite_edges(catalogue, tree, result)
        self._cross_reference_edges(catalogue, tree, result)
        return result

    def _containment_edges(
        self, catalogue: ExtractedCatalogue, result: DiscoveredRelationships
    ) -> None:
        subject_id = catalogue.subject.stable_id.value
        for node in catalogue.nodes:
            if isinstance(node, Topic):
                result.edges.append(
                    CkgEdge.create(
                        subject_id,
                        node.stable_id,
                        CkgRelationshipType.CONTAINS,
                    )
                )
            elif isinstance(node, Section):
                result.edges.append(
                    CkgEdge.create(
                        node.topic_id,
                        node.stable_id,
                        CkgRelationshipType.CONTAINS,
                    )
                )
            elif isinstance(node, Subsection):
                result.edges.append(
                    CkgEdge.create(
                        node.section_id,
                        node.stable_id,
                        CkgRelationshipType.CONTAINS,
                    )
                )
            elif isinstance(node, LearningObjective):
                result.edges.append(
                    CkgEdge.create(
                        node.subsection_id,
                        node.stable_id,
                        CkgRelationshipType.CONTAINS,
                    )
                )
            elif isinstance(
                node,
                Definition
                | Formula
                | WorkedExample
                | PracticeExercise
                | ReadingReference
                | SyllabusOutcome,
            ):
                result.edges.append(
                    CkgEdge.create(
                        node.owner_id,
                        node.stable_id,
                        CkgRelationshipType.CONTAINS,
                    )
                )

    def _object_reference_edges(
        self, catalogue: ExtractedCatalogue, result: DiscoveredRelationships
    ) -> None:
        objects_by_owner = catalogue.object_ids_by_owner
        seen: set[tuple[str, str, str]] = set()

        def add_ref(lo_id: str, target: str) -> None:
            key = (lo_id, target, CkgRelationshipType.REFERENCES.value)
            if key in seen:
                return
            seen.add(key)
            result.edges.append(
                CkgEdge.create(lo_id, target, CkgRelationshipType.REFERENCES)
            )
            self._role_edge(catalogue, lo_id, target, result)

        for lo_id in catalogue.lo_ids:
            for target in objects_by_owner.get(lo_id, []):
                add_ref(lo_id, target)
            lo_node = next(
                (
                    n
                    for n in catalogue.nodes
                    if isinstance(n, LearningObjective)
                    and n.stable_id.value == lo_id
                ),
                None,
            )
            if lo_node is None:
                continue
            ss_id = lo_node.subsection_id.value
            for target in objects_by_owner.get(ss_id, []):
                add_ref(lo_id, target)

    def _role_edge(
        self,
        catalogue: ExtractedCatalogue,
        lo_id: str,
        target_id: str,
        result: DiscoveredRelationships,
    ) -> None:
        node = next(
            (n for n in catalogue.nodes if n.stable_id.value == target_id),
            None,
        )
        if isinstance(node, Definition):
            result.edges.append(
                CkgEdge.create(target_id, lo_id, CkgRelationshipType.DEFINES)
            )
        elif isinstance(node, WorkedExample):
            result.edges.append(
                CkgEdge.create(
                    target_id, lo_id, CkgRelationshipType.EXEMPLIFIES
                )
            )
        elif isinstance(node, PracticeExercise):
            result.edges.append(
                CkgEdge.create(target_id, lo_id, CkgRelationshipType.ASSESSES)
            )
        elif isinstance(node, ReadingReference):
            result.edges.append(
                CkgEdge.create(target_id, lo_id, CkgRelationshipType.READS)
            )

    def _prerequisite_edges(
        self,
        catalogue: ExtractedCatalogue,
        tree: CurriculumSegmentTree,
        result: DiscoveredRelationships,
    ) -> None:
        for cue in tree.prerequisite_cues:
            result.explicit_requires_numbers.append(
                (cue.from_number, cue.to_number)
            )
            src = catalogue.number_to_stable_id.get(cue.from_number)
            tgt = catalogue.number_to_stable_id.get(cue.to_number)
            if not src or not tgt:
                result.diagnostics.append(
                    f"Prerequisite cue unresolved: {cue.from_number}→"
                    f"{cue.to_number}"
                )
                continue
            src_lo = self._first_lo_under(catalogue, src)
            tgt_lo = self._first_lo_under(catalogue, tgt)
            if src_lo and tgt_lo and src_lo != tgt_lo:
                result.edges.append(
                    CkgEdge.create(
                        src_lo, tgt_lo, CkgRelationshipType.REQUIRES
                    )
                )

        if not tree.prerequisite_cues and len(catalogue.lo_ids) >= 2:
            by_ss: dict[str, list[str]] = {}
            for lo_id in catalogue.lo_ids:
                parent = ".".join(lo_id.split(".")[:-1])
                by_ss.setdefault(parent, []).append(lo_id)
            for los in by_ss.values():
                ordered = sorted(los)
                for earlier, later in zip(ordered, ordered[1:], strict=False):
                    result.edges.append(
                        CkgEdge.create(
                            later,
                            earlier,
                            CkgRelationshipType.REQUIRES,
                            rationale="sequential_within_subsection",
                        )
                    )

    def _cross_reference_edges(
        self,
        catalogue: ExtractedCatalogue,
        tree: CurriculumSegmentTree,
        result: DiscoveredRelationships,
    ) -> None:
        for cue in tree.cross_reference_cues:
            src = catalogue.number_to_stable_id.get(cue.from_number)
            tgt = catalogue.number_to_stable_id.get(cue.to_number)
            if not src or not tgt:
                result.diagnostics.append(
                    f"Cross-reference unresolved: {cue.from_number}→"
                    f"{cue.to_number}"
                )
                continue
            result.edges.append(
                CkgEdge.create(
                    src, tgt, CkgRelationshipType.CROSS_REFERENCES
                )
            )

    def _first_lo_under(
        self, catalogue: ExtractedCatalogue, stable_id: str
    ) -> str | None:
        depth = StableCurriculumId.of(stable_id).depth
        if depth is StableIdDepth.LEARNING_OBJECTIVE:
            return stable_id
        prefix = stable_id + "."
        for lo_id in catalogue.lo_ids:
            if lo_id.startswith(prefix):
                return lo_id
        return None
