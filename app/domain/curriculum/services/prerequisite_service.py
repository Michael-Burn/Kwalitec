"""PrerequisiteService — eligibility and missing-prerequisite evaluation."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.curriculum.graph.curriculum_graph import CurriculumGraph
from app.domain.curriculum.value_objects.topic_id import TopicId


@dataclass(frozen=True)
class PrerequisiteEvaluation:
    """Result of evaluating prerequisites for one topic.

    Attributes:
        topic_id: Evaluated topic.
        is_eligible: True when all hard prerequisites are satisfied.
        missing: Prerequisites not yet completed.
        satisfied: Prerequisites already completed.
        blockers: Topics that hard-depend on this topic (dependents) —
            informational for sequencing, not eligibility blockers for self.
    """

    topic_id: TopicId
    is_eligible: bool
    missing: tuple[TopicId, ...]
    satisfied: tuple[TopicId, ...]
    blockers: tuple[TopicId, ...] = ()


class PrerequisiteService:
    """Determine eligible, missing, and blocked topics from a CurriculumGraph.

    Uses REQUIRES edges only. Deterministic; no heuristics.
    """

    def __init__(self, graph: CurriculumGraph) -> None:
        self._graph = graph

    def evaluate(
        self,
        topic_id: str | TopicId,
        completed: set[str] | set[TopicId] | frozenset[str] | frozenset[TopicId],
    ) -> PrerequisiteEvaluation:
        """Evaluate hard prerequisites for a single topic."""
        tid = TopicId.of(topic_id)
        if not self._graph.has_topic(tid):
            raise ValueError(f"topic not in graph: {tid.value}")
        completed_ids = {TopicId.of(t).value for t in completed}
        prereqs = self._graph.find_prerequisites(tid)
        missing = tuple(p for p in prereqs if p.value not in completed_ids)
        satisfied = tuple(p for p in prereqs if p.value in completed_ids)
        blockers = self._graph.find_successors(tid)
        return PrerequisiteEvaluation(
            topic_id=tid,
            is_eligible=len(missing) == 0,
            missing=missing,
            satisfied=satisfied,
            blockers=blockers,
        )

    def eligible_topics(
        self,
        completed: set[str] | set[TopicId] | frozenset[str] | frozenset[TopicId],
    ) -> tuple[TopicId, ...]:
        """Topics whose hard prerequisites are all completed (incl. roots).

        Completed topics themselves are excluded.
        """
        completed_ids = {TopicId.of(t).value for t in completed}
        eligible: list[TopicId] = []
        for node in self._graph.nodes():
            tid = node.topic_id
            if tid.value in completed_ids:
                continue
            if self.evaluate(tid, completed_ids).is_eligible:
                eligible.append(tid)
        return tuple(eligible)

    def missing_prerequisites(
        self,
        topic_id: str | TopicId,
        completed: set[str] | set[TopicId] | frozenset[str] | frozenset[TopicId],
    ) -> tuple[TopicId, ...]:
        """Direct hard prerequisites not yet completed."""
        return self.evaluate(topic_id, completed).missing

    def blocked_topics(
        self,
        completed: set[str] | set[TopicId] | frozenset[str] | frozenset[TopicId],
    ) -> tuple[TopicId, ...]:
        """Topics that are not eligible and not already completed."""
        completed_ids = {TopicId.of(t).value for t in completed}
        blocked: list[TopicId] = []
        for node in self._graph.nodes():
            tid = node.topic_id
            if tid.value in completed_ids:
                continue
            if not self.evaluate(tid, completed_ids).is_eligible:
                blocked.append(tid)
        return tuple(blocked)

    def transitive_missing(
        self,
        topic_id: str | TopicId,
        completed: set[str] | set[TopicId] | frozenset[str] | frozenset[TopicId],
    ) -> tuple[TopicId, ...]:
        """All incomplete ancestors on the REQUIRES DAG (excluding self)."""
        tid = TopicId.of(topic_id)
        completed_ids = {TopicId.of(t).value for t in completed}
        ancestors = self._graph.all_prerequisites(tid, transitive=True)
        return tuple(a for a in ancestors if a.value not in completed_ids)
