"""CurriculumNavigationService — deterministic topic sequencing helpers."""

from __future__ import annotations

from app.domain.curriculum.entities.curriculum import Curriculum
from app.domain.curriculum.entities.learning_path import LearningPath
from app.domain.curriculum.graph.curriculum_graph import CurriculumGraph
from app.domain.curriculum.value_objects.dependency_type import DependencyType
from app.domain.curriculum.value_objects.topic_id import TopicId
from app.domain.curriculum.value_objects.topic_status import TopicStatus


class CurriculumNavigationService:
    """Navigate curriculum structure and graph neighbourhoods.

    Pure / deterministic. Consumes Curriculum + CurriculumGraph; does not
    mutate learner state. Future Learning Journey Engine calls this layer
    rather than reading the graph directly.
    """

    def __init__(
        self,
        curriculum: Curriculum,
        graph: CurriculumGraph,
    ) -> None:
        self._curriculum = curriculum
        self._graph = graph

    @property
    def curriculum(self) -> Curriculum:
        """Bound curriculum aggregate."""
        return self._curriculum

    @property
    def graph(self) -> CurriculumGraph:
        """Bound curriculum graph."""
        return self._graph

    def ordered_topics(self) -> tuple[TopicId, ...]:
        """Canonical hierarchy order: subject → module → topic sequence."""
        return self._curriculum.topic_ids()

    def next_topic(self, topic_id: str | TopicId) -> TopicId | None:
        """Next topic in hierarchy order, or None at end / absent."""
        tid = TopicId.of(topic_id)
        ordered = self.ordered_topics()
        try:
            idx = ordered.index(tid)
        except ValueError:
            return None
        if idx + 1 >= len(ordered):
            return None
        return ordered[idx + 1]

    def previous_topic(self, topic_id: str | TopicId) -> TopicId | None:
        """Previous topic in hierarchy order, or None at start / absent."""
        tid = TopicId.of(topic_id)
        ordered = self.ordered_topics()
        try:
            idx = ordered.index(tid)
        except ValueError:
            return None
        if idx == 0:
            return None
        return ordered[idx - 1]

    def available_topics(
        self,
        completed: set[str] | set[TopicId] | frozenset[str] | frozenset[TopicId],
        *,
        active: set[str] | set[TopicId] | frozenset[str] | frozenset[TopicId]
        | None = None,
    ) -> tuple[TopicId, ...]:
        """Topics whose hard prerequisites are all completed and not active.

        Locked when any REQUIRES prerequisite is incomplete. Active topics
        are excluded from the available set (they are already in progress).
        """
        completed_ids = {TopicId.of(t).value for t in completed}
        active_ids = {TopicId.of(t).value for t in (active or set())}
        available: list[TopicId] = []
        for tid in self.ordered_topics():
            if tid.value in completed_ids or tid.value in active_ids:
                continue
            prereqs = self._graph.find_prerequisites(tid)
            if all(p.value in completed_ids for p in prereqs):
                available.append(tid)
        return tuple(available)

    def recommended_topics(
        self,
        completed: set[str] | set[TopicId] | frozenset[str] | frozenset[TopicId],
        *,
        limit: int | None = None,
    ) -> tuple[TopicId, ...]:
        """Eligible topics preferring those with RECOMMENDS from completed.

        Deterministic: hierarchy order, with recommend-boosted topics first
        (still stable by hierarchy index among equals).
        """
        if limit is not None and limit < 0:
            raise ValueError("limit must be non-negative")
        completed_ids = {TopicId.of(t).value for t in completed}
        available = self.available_topics(completed_ids)
        boosted: list[TopicId] = []
        plain: list[TopicId] = []
        for tid in available:
            recommends = self._graph.neighbours(
                tid,
                dependency_type=DependencyType.RECOMMENDS,
                direction="out",
            )
            if any(r.value in completed_ids for r in recommends):
                boosted.append(tid)
            else:
                plain.append(tid)
        ordered = tuple(boosted + plain)
        if limit is None:
            return ordered
        return ordered[:limit]

    def learning_path(self, path_id: str) -> LearningPath | None:
        """Locate a named learning path on the curriculum."""
        for path in self._curriculum.learning_paths:
            if path.path_id == path_id:
                return path
        return None

    def next_on_path(
        self, path_id: str, topic_id: str | TopicId
    ) -> TopicId | None:
        """Next topic along a named learning path."""
        path = self.learning_path(path_id)
        if path is None:
            return None
        return path.next_after(topic_id)

    def previous_on_path(
        self, path_id: str, topic_id: str | TopicId
    ) -> TopicId | None:
        """Previous topic along a named learning path."""
        path = self.learning_path(path_id)
        if path is None:
            return None
        return path.previous_before(topic_id)

    def status_for(
        self,
        topic_id: str | TopicId,
        *,
        completed: set[str] | set[TopicId] | frozenset[str] | frozenset[TopicId],
        active: set[str] | set[TopicId] | frozenset[str] | frozenset[TopicId]
        | None = None,
        archived: set[str] | set[TopicId] | frozenset[str] | frozenset[TopicId]
        | None = None,
    ) -> TopicStatus:
        """Derive TopicStatus from completion / activity sets and prerequisites."""
        tid = TopicId.of(topic_id)
        completed_ids = {TopicId.of(t).value for t in completed}
        active_ids = {TopicId.of(t).value for t in (active or set())}
        archived_ids = {TopicId.of(t).value for t in (archived or set())}
        if tid.value in archived_ids:
            return TopicStatus.ARCHIVED
        if tid.value in completed_ids:
            return TopicStatus.COMPLETED
        if tid.value in active_ids:
            return TopicStatus.ACTIVE
        prereqs = self._graph.find_prerequisites(tid)
        if all(p.value in completed_ids for p in prereqs):
            return TopicStatus.AVAILABLE
        return TopicStatus.LOCKED

    def topological_study_order(self) -> tuple[TopicId, ...]:
        """Topological order of topics under REQUIRES constraints."""
        return self._graph.topological_ordering()
