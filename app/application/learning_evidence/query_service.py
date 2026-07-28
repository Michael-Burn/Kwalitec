"""Read-side queries for Learning Evidence Engine (EI-005)."""

from __future__ import annotations

import json

from app.application.learning_evidence.dto import (
    EvidenceHistoryView,
    EvidenceSummaryView,
)
from app.application.learning_evidence.exceptions import InstanceNotFoundError
from app.domain.learning_evidence.evidence_event import EvidenceEvent
from app.domain.learning_evidence.evidence_type import (
    EvidenceType,
    normalise_evidence_type,
)
from app.domain.learning_evidence.summary import count_by_type
from app.models.learning_evidence import LeeEvidenceEvent
from app.models.student_curriculum_binding import SciStudentCurriculumInstance


class EvidenceQueryService:
    """Retrieve chronological educational evidence without inference."""

    def get_by_node(
        self,
        instance_id: str,
        node_stable_id: str,
        *,
        evidence_type: str | EvidenceType | None = None,
    ) -> EvidenceHistoryView:
        """Evidence for one curriculum node within an SCI (oldest first)."""
        self._require_instance(instance_id)
        return self._history(
            instance_id=instance_id,
            student_id=None,
            node_stable_id=node_stable_id,
            evidence_type=evidence_type,
        )

    def get_by_student(
        self,
        student_id: int,
        *,
        instance_id: str | None = None,
        evidence_type: str | EvidenceType | None = None,
    ) -> EvidenceHistoryView:
        """Evidence for a student across SCIs (or one instance)."""
        if instance_id is not None:
            instance = self._require_instance(instance_id)
            if instance.student_id != student_id:
                raise InstanceNotFoundError(
                    f"Instance {instance_id} does not belong to student {student_id}"
                )
        return self._history(
            instance_id=instance_id,
            student_id=student_id,
            node_stable_id=None,
            evidence_type=evidence_type,
        )

    def get_chronological_history(
        self,
        instance_id: str,
        *,
        evidence_type: str | EvidenceType | None = None,
    ) -> EvidenceHistoryView:
        """Full chronological history for one Student Curriculum Instance."""
        self._require_instance(instance_id)
        return self._history(
            instance_id=instance_id,
            student_id=None,
            node_stable_id=None,
            evidence_type=evidence_type,
        )

    def filter_by_type(
        self,
        instance_id: str,
        evidence_type: str | EvidenceType,
    ) -> EvidenceHistoryView:
        """Evidence of one type for an SCI (chronological)."""
        return self.get_chronological_history(
            instance_id, evidence_type=evidence_type
        )

    def summarise_counts(
        self,
        instance_id: str,
        *,
        node_stable_id: str | None = None,
    ) -> EvidenceSummaryView:
        """Count evidence events by type (deterministic key order)."""
        self._require_instance(instance_id)
        query = LeeEvidenceEvent.query.filter_by(instance_id=instance_id)
        if node_stable_id is not None:
            query = query.filter_by(node_stable_id=node_stable_id)
        types = [row.evidence_type for row in query.all()]
        return EvidenceSummaryView(
            instance_id=instance_id,
            node_stable_id=node_stable_id,
            summary=count_by_type(types),
        )

    def _history(
        self,
        *,
        instance_id: str | None,
        student_id: int | None,
        node_stable_id: str | None,
        evidence_type: str | EvidenceType | None,
    ) -> EvidenceHistoryView:
        query = LeeEvidenceEvent.query
        if instance_id is not None:
            query = query.filter_by(instance_id=instance_id)
        if student_id is not None:
            query = query.filter_by(student_id=student_id)
        if node_stable_id is not None:
            query = query.filter_by(node_stable_id=node_stable_id)
        type_filter: str | None = None
        if evidence_type is not None:
            type_filter = normalise_evidence_type(evidence_type)
            query = query.filter_by(evidence_type=type_filter)

        rows = query.order_by(
            LeeEvidenceEvent.occurred_at.asc(),
            LeeEvidenceEvent.id.asc(),
        ).all()
        return EvidenceHistoryView(
            instance_id=instance_id,
            student_id=student_id,
            node_stable_id=node_stable_id,
            evidence_type=type_filter,
            events=tuple(self._to_event(row) for row in rows),
        )

    @staticmethod
    def _require_instance(instance_id: str) -> SciStudentCurriculumInstance:
        instance = SciStudentCurriculumInstance.query.filter_by(
            instance_id=instance_id
        ).first()
        if instance is None:
            raise InstanceNotFoundError(f"Instance not found: {instance_id}")
        return instance

    @staticmethod
    def _to_event(row: LeeEvidenceEvent) -> EvidenceEvent:
        try:
            metadata = json.loads(row.metadata_json or "{}")
        except json.JSONDecodeError:
            metadata = {}
        if not isinstance(metadata, dict):
            metadata = {}
        return EvidenceEvent(
            evidence_id=row.evidence_id,
            instance_id=row.instance_id,
            node_stable_id=row.node_stable_id,
            evidence_type=row.evidence_type,
            occurred_at=row.occurred_at,
            source=row.source,
            recorded_at=row.recorded_at,
            metadata=metadata,
            corrects_evidence_id=row.corrects_evidence_id,
        )
