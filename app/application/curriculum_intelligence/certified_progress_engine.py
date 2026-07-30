"""EI-002B — Progress tracking against stable certified node identifiers."""

from __future__ import annotations

from typing import Any

from app.application.curriculum_intelligence.learner_knowledge_graph_service import (
    LearnerKnowledgeGraphBuilder,
    assert_certified_package,
)
from app.domain.curriculum_intelligence.certified_learning import (
    CertifiedNodeKind,
    CertifiedProgressSnapshot,
    LearnerKnowledgeGraph,
    NodeMasteryRecord,
)


class CertifiedProgressEngine:
    """Track mastery at subject / chapter / topic / LO / concept levels.

    Progress keys are certified node identifiers so mastery remains stable
    across curriculum revisions that preserve node identity.
    """

    def __init__(
        self, graph_builder: LearnerKnowledgeGraphBuilder | None = None
    ) -> None:
        self._graph = graph_builder or LearnerKnowledgeGraphBuilder()

    def snapshot(
        self,
        package: dict[str, Any],
        *,
        completed_node_ids: tuple[str, ...] | list[str] = (),
        objective_mastery: dict[str, float] | None = None,
        topic_mastery: dict[str, float] | None = None,
        concept_mastery: dict[str, float] | None = None,
        attempts_by_node: dict[str, int] | None = None,
    ) -> CertifiedProgressSnapshot:
        provenance = assert_certified_package(package)
        graph = self._graph.build(package)
        completed = {str(x).strip() for x in completed_node_ids if str(x).strip()}
        obj_m = {str(k): float(v) for k, v in (objective_mastery or {}).items()}
        topic_m = {str(k): float(v) for k, v in (topic_mastery or {}).items()}
        concept_m = {str(k): float(v) for k, v in (concept_mastery or {}).items()}
        attempts = {str(k): int(v) for k, v in (attempts_by_node or {}).items()}

        objective_records = _records_for(
            graph,
            kinds={CertifiedNodeKind.LEARNING_OBJECTIVE},
            mastery_map=obj_m,
            completed=completed,
            attempts=attempts,
            default_mastery_if_completed=1.0,
        )
        topic_records = _records_for(
            graph,
            kinds={CertifiedNodeKind.TOPIC},
            mastery_map=topic_m,
            completed=completed,
            attempts=attempts,
            default_mastery_if_completed=1.0,
            child_kind=CertifiedNodeKind.LEARNING_OBJECTIVE,
            child_mastery=obj_m,
        )
        concept_records = _records_for(
            graph,
            kinds={CertifiedNodeKind.CONCEPT},
            mastery_map=concept_m,
            completed=completed,
            attempts=attempts,
            default_mastery_if_completed=1.0,
        )
        chapter_records = _records_for(
            graph,
            kinds={CertifiedNodeKind.CHAPTER, CertifiedNodeKind.SECTION},
            mastery_map={},
            completed=completed,
            attempts=attempts,
            default_mastery_if_completed=1.0,
            child_kind=CertifiedNodeKind.TOPIC,
            child_mastery={
                **{r.node_id: r.mastery for r in topic_records},
            },
        )

        all_objectives = [
            n.node_id
            for n in graph.nodes
            if n.kind is CertifiedNodeKind.LEARNING_OBJECTIVE
        ]
        covered_objectives = [
            r.node_id
            for r in objective_records
            if r.mastery >= 0.7 or r.coverage >= 1.0
        ]
        missed = tuple(
            oid
            for oid in all_objectives
            if oid not in covered_objectives and oid not in completed
        )
        coverage_ratio = (
            len(covered_objectives) / len(all_objectives) if all_objectives else 0.0
        )
        subject_mastery = round(
            (
                sum(r.mastery for r in topic_records) / len(topic_records)
                if topic_records
                else coverage_ratio
            ),
            4,
        )

        return CertifiedProgressSnapshot(
            curriculum_identity=graph.curriculum_identity,
            provenance=provenance,
            subject_mastery=subject_mastery,
            chapter_records=chapter_records,
            topic_records=topic_records,
            objective_records=objective_records,
            concept_records=concept_records,
            completed_node_ids=tuple(sorted(completed)),
            missed_objective_ids=missed,
            coverage_ratio=round(coverage_ratio, 4),
        )


def _records_for(
    graph: LearnerKnowledgeGraph,
    *,
    kinds: set[CertifiedNodeKind],
    mastery_map: dict[str, float],
    completed: set[str],
    attempts: dict[str, int],
    default_mastery_if_completed: float,
    child_kind: CertifiedNodeKind | None = None,
    child_mastery: dict[str, float] | None = None,
) -> tuple[NodeMasteryRecord, ...]:
    records: list[NodeMasteryRecord] = []
    for node in graph.nodes:
        if node.kind not in kinds:
            continue
        mastery = mastery_map.get(node.node_id)
        if mastery is None and node.node_id in completed:
            mastery = default_mastery_if_completed
        if mastery is None and child_kind is not None:
            children = [
                n.node_id
                for n in graph.nodes
                if n.parent_node_id == node.node_id and n.kind is child_kind
            ]
            if children and child_mastery is not None:
                vals = [
                    float(child_mastery.get(cid, 1.0 if cid in completed else 0.0))
                    for cid in children
                ]
                mastery = sum(vals) / len(vals) if vals else 0.0
            else:
                mastery = 0.0
        if mastery is None:
            mastery = 0.0
        mastery = max(0.0, min(1.0, float(mastery)))
        coverage = 1.0 if node.node_id in completed or mastery >= 0.7 else mastery
        records.append(
            NodeMasteryRecord(
                node_id=node.node_id,
                kind=node.kind,
                mastery=round(mastery, 4),
                coverage=round(coverage, 4),
                attempts=int(attempts.get(node.node_id, 0)),
            )
        )
    return tuple(records)
