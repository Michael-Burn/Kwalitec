"""Deterministic progress aggregation services (EI-004)."""

from __future__ import annotations

from app.application.student_curriculum_binding.dto import ProgressAggregationView
from app.application.student_curriculum_binding.exceptions import (
    InstanceNotFoundError,
)
from app.domain.curriculum_knowledge_graph.value_objects.node_kind import (
    CkgNodeKind,
)
from app.domain.curriculum_knowledge_graph.value_objects.stable_curriculum_id import (
    StableCurriculumId,
)
from app.domain.student_curriculum_binding.aggregation import (
    ProgressAggregate,
    aggregate_progress,
)
from app.domain.student_curriculum_binding.node_state import NodeStateSnapshot
from app.models.student_curriculum_binding import (
    SciCurriculumNodeState,
    SciStudentCurriculumInstance,
)

_LEVEL_KINDS = {
    "subsection": CkgNodeKind.SUBSECTION.value,
    "section": CkgNodeKind.SECTION.value,
    "topic": CkgNodeKind.TOPIC.value,
    "subject": CkgNodeKind.SUBJECT.value,
}


class ProgressAggregationService:
    """Aggregate node-level educational state upwards through the hierarchy."""

    def aggregate_for_node(
        self,
        instance_id: str,
        stable_id: str,
    ) -> ProgressAggregate:
        """Aggregate progress under a single structural node."""
        self._require_instance(instance_id)
        try:
            kind = StableCurriculumId.of(stable_id).kind.value
        except ValueError as exc:
            raise ValueError(f"Invalid curriculum stable id: {stable_id}") from exc
        if kind not in {
            CkgNodeKind.SUBSECTION.value,
            CkgNodeKind.SECTION.value,
            CkgNodeKind.TOPIC.value,
            CkgNodeKind.SUBJECT.value,
        }:
            raise ValueError(
                f"Aggregation requires a structural node; got kind={kind!r}"
            )
        states = self._load_states(instance_id)
        return aggregate_progress(stable_id, kind, states)

    def aggregate_level(
        self,
        instance_id: str,
        level: str,
    ) -> ProgressAggregationView:
        """Aggregate every node at the given structural level.

        Args:
            instance_id: Student Curriculum Instance id.
            level: One of ``subsection``, ``section``, ``topic``, ``subject``.
        """
        self._require_instance(instance_id)
        kind = _LEVEL_KINDS.get(level.strip().lower())
        if kind is None:
            raise ValueError(
                f"Unsupported aggregation level {level!r}; "
                f"expected one of {sorted(_LEVEL_KINDS)}"
            )

        states = self._load_states(instance_id)
        roots = sorted(
            (s for s in states if s.node_kind == kind),
            key=lambda s: s.node_stable_id,
        )
        aggregates = tuple(
            aggregate_progress(root.node_stable_id, kind, states) for root in roots
        )
        return ProgressAggregationView(
            instance_id=instance_id,
            aggregates=aggregates,
        )

    def aggregate_all_levels(self, instance_id: str) -> ProgressAggregationView:
        """Aggregate subject, topic, section, and subsection levels."""
        self._require_instance(instance_id)
        states = self._load_states(instance_id)
        aggregates: list[ProgressAggregate] = []
        for level in ("subject", "topic", "section", "subsection"):
            kind = _LEVEL_KINDS[level]
            roots = sorted(
                (s for s in states if s.node_kind == kind),
                key=lambda s: s.node_stable_id,
            )
            aggregates.extend(
                aggregate_progress(root.node_stable_id, kind, states)
                for root in roots
            )
        return ProgressAggregationView(
            instance_id=instance_id,
            aggregates=tuple(aggregates),
        )

    def _require_instance(self, instance_id: str) -> SciStudentCurriculumInstance:
        instance = SciStudentCurriculumInstance.query.filter_by(
            instance_id=instance_id
        ).first()
        if instance is None:
            raise InstanceNotFoundError(f"Instance not found: {instance_id}")
        return instance

    def _load_states(self, instance_id: str) -> list[NodeStateSnapshot]:
        rows = (
            SciCurriculumNodeState.query.filter_by(instance_id=instance_id)
            .order_by(SciCurriculumNodeState.node_stable_id.asc())
            .all()
        )
        return [
            NodeStateSnapshot(
                node_stable_id=row.node_stable_id,
                node_kind=row.node_kind,
                mastery=float(row.mastery),
                confidence=float(row.confidence),
                revision_status=row.revision_status,
                attempts=int(row.attempts),
                total_study_time_minutes=int(row.total_study_time_minutes),
                last_interaction_at=row.last_interaction_at,
                completion_status=row.completion_status,
                evidence_count=int(row.evidence_count),
            )
            for row in rows
        ]
