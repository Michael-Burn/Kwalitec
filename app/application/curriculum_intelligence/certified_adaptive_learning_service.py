"""EI-002B — Adaptive learning signals from certified curriculum + progress.

Uses certification metadata and Curriculum Memory identifiers (stable node
ids) to surface weak concepts, missed objectives, revision priorities, and
concept dependencies. Does not invent a new decision engine — ranks existing
progress gaps against the certified learner graph.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from app.application.curriculum_intelligence.certified_progress_engine import (
    CertifiedProgressEngine,
)
from app.application.curriculum_intelligence.learner_knowledge_graph_service import (
    LearnerKnowledgeGraphBuilder,
    assert_certified_package,
)
from app.domain.curriculum_intelligence.certified_learning import (
    AdaptiveLearningPlan,
    AdaptiveLearningSignal,
    CertifiedProgressSnapshot,
)


class CertifiedAdaptiveLearningService:
    """Identify weak / missed / revision / dependency signals on certified nodes."""

    def __init__(
        self,
        *,
        progress_engine: CertifiedProgressEngine | None = None,
        graph_builder: LearnerKnowledgeGraphBuilder | None = None,
    ) -> None:
        self._progress = progress_engine or CertifiedProgressEngine()
        self._graph = graph_builder or LearnerKnowledgeGraphBuilder()

    def plan(
        self,
        package: dict[str, Any],
        *,
        progress: CertifiedProgressSnapshot | None = None,
        completed_node_ids: tuple[str, ...] | list[str] = (),
        objective_mastery: dict[str, float] | None = None,
        topic_mastery: dict[str, float] | None = None,
        weakness_threshold: float = 0.55,
    ) -> AdaptiveLearningPlan:
        provenance = assert_certified_package(package)
        graph = self._graph.build(package)
        snap = progress or self._progress.snapshot(
            package,
            completed_node_ids=completed_node_ids,
            objective_mastery=objective_mastery,
            topic_mastery=topic_mastery,
        )

        weak: list[AdaptiveLearningSignal] = []
        for record in (*snap.topic_records, *snap.concept_records):
            if record.mastery < weakness_threshold:
                deps = graph.prerequisites(record.node_id)
                weak.append(
                    AdaptiveLearningSignal(
                        signal_id=f"weak_{uuid4().hex[:8]}",
                        kind="weak_concept",
                        node_id=record.node_id,
                        priority=round(1.0 - record.mastery, 4),
                        rationale=(
                            f"{record.kind.value} mastery {record.mastery:.2f} "
                            f"below threshold {weakness_threshold:.2f}"
                        ),
                        related_node_ids=deps,
                    )
                )

        missed: list[AdaptiveLearningSignal] = []
        for oid in snap.missed_objective_ids:
            node = graph.node(oid)
            parent = node.parent_node_id if node else ""
            missed.append(
                AdaptiveLearningSignal(
                    signal_id=f"miss_{uuid4().hex[:8]}",
                    kind="missed_objective",
                    node_id=oid,
                    priority=0.85,
                    rationale="certified learning objective not yet covered",
                    related_node_ids=(parent,) if parent else (),
                )
            )

        # Revision priorities: weak topics whose prerequisites are satisfied.
        completed = set(snap.completed_node_ids)
        revision: list[AdaptiveLearningSignal] = []
        for signal in weak:
            prereqs = graph.prerequisites(signal.node_id)
            if all(p in completed or _mastery_ok(snap, p) for p in prereqs):
                revision.append(
                    AdaptiveLearningSignal(
                        signal_id=f"rev_{uuid4().hex[:8]}",
                        kind="revision_priority",
                        node_id=signal.node_id,
                        priority=round(signal.priority + 0.1, 4),
                        rationale=(
                            "revision ready: prerequisites satisfied; "
                            f"weak mastery on {signal.node_id}"
                        ),
                        related_node_ids=prereqs,
                    )
                )

        # Concept / topic dependency blockers for missed objectives.
        dependencies: list[AdaptiveLearningSignal] = []
        for oid in snap.missed_objective_ids:
            node = graph.node(oid)
            if node is None or not node.parent_node_id:
                continue
            topic_id = node.parent_node_id
            for prereq in graph.prerequisites(topic_id):
                if prereq not in completed and not _mastery_ok(snap, prereq):
                    dependencies.append(
                        AdaptiveLearningSignal(
                            signal_id=f"dep_{uuid4().hex[:8]}",
                            kind="concept_dependency",
                            node_id=prereq,
                            priority=0.9,
                            rationale=(
                                f"blocks objective {oid} via topic {topic_id}"
                            ),
                            related_node_ids=(topic_id, oid),
                        )
                    )

        weak.sort(key=lambda s: (-s.priority, s.node_id))
        missed.sort(key=lambda s: (-s.priority, s.node_id))
        revision.sort(key=lambda s: (-s.priority, s.node_id))
        dependencies.sort(key=lambda s: (-s.priority, s.node_id))

        return AdaptiveLearningPlan(
            curriculum_identity=graph.curriculum_identity,
            provenance=provenance,
            weak_concepts=tuple(weak),
            missed_objectives=tuple(missed),
            revision_priorities=tuple(revision),
            concept_dependencies=tuple(dependencies),
        )


def _mastery_ok(snap: CertifiedProgressSnapshot, node_id: str) -> bool:
    for record in (
        *snap.topic_records,
        *snap.concept_records,
        *snap.objective_records,
        *snap.chapter_records,
    ):
        if record.node_id == node_id and record.mastery >= 0.7:
            return True
    return False


__all__ = ["CertifiedAdaptiveLearningService"]
