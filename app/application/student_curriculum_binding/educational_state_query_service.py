"""Read-side educational state queries for Student Curriculum Binding (EI-004)."""

from __future__ import annotations

from app.application.student_curriculum_binding.dto import (
    CurriculumNodeFilterResult,
    EducationalStateView,
    InstanceSummary,
    format_dt,
)
from app.application.student_curriculum_binding.exceptions import (
    InstanceNotFoundError,
)
from app.domain.student_curriculum_binding.node_state import (
    CompletionStatus,
    NodeStateSnapshot,
)
from app.models.student_curriculum_binding import (
    SciCurriculumNodeState,
    SciStudentCurriculumInstance,
)


class EducationalStateQueryService:
    """Retrieve current educational state and completion filters."""

    def get_active_instance(
        self,
        *,
        student_id: int,
        subject_code: str,
    ) -> InstanceSummary | None:
        """Return the active binding for a student+subject, if any."""
        instance = (
            SciStudentCurriculumInstance.query.filter_by(
                student_id=student_id,
                subject_code=subject_code.strip().upper(),
                is_active=True,
            )
            .order_by(SciStudentCurriculumInstance.id.asc())
            .first()
        )
        if instance is None:
            return None
        count = SciCurriculumNodeState.query.filter_by(
            instance_id=instance.instance_id
        ).count()
        return self._summary(instance, node_state_count=count)

    def get_instance(self, instance_id: str) -> InstanceSummary:
        """Return instance summary or raise if missing."""
        instance = self._require_instance(instance_id)
        count = SciCurriculumNodeState.query.filter_by(
            instance_id=instance_id
        ).count()
        return self._summary(instance, node_state_count=count)

    def get_educational_state(self, instance_id: str) -> EducationalStateView:
        """Full educational state: instance + all node states (stable-id order)."""
        instance = self._require_instance(instance_id)
        rows = (
            SciCurriculumNodeState.query.filter_by(instance_id=instance_id)
            .order_by(SciCurriculumNodeState.node_stable_id.asc())
            .all()
        )
        snapshots = tuple(self._to_snapshot(row) for row in rows)
        return EducationalStateView(
            instance=self._summary(instance, node_state_count=len(snapshots)),
            node_states=snapshots,
        )

    def query_incomplete_curriculum(
        self,
        instance_id: str,
    ) -> CurriculumNodeFilterResult:
        """Nodes that are not completed (not_started or in_progress)."""
        self._require_instance(instance_id)
        rows = (
            SciCurriculumNodeState.query.filter(
                SciCurriculumNodeState.instance_id == instance_id,
                SciCurriculumNodeState.completion_status
                != CompletionStatus.COMPLETED.value,
            )
            .order_by(SciCurriculumNodeState.node_stable_id.asc())
            .all()
        )
        return CurriculumNodeFilterResult(
            instance_id=instance_id,
            completion_status="incomplete",
            nodes=tuple(self._to_snapshot(r) for r in rows),
        )

    def query_completed_curriculum(
        self,
        instance_id: str,
    ) -> CurriculumNodeFilterResult:
        """Nodes marked completed."""
        self._require_instance(instance_id)
        rows = (
            SciCurriculumNodeState.query.filter_by(
                instance_id=instance_id,
                completion_status=CompletionStatus.COMPLETED.value,
            )
            .order_by(SciCurriculumNodeState.node_stable_id.asc())
            .all()
        )
        return CurriculumNodeFilterResult(
            instance_id=instance_id,
            completion_status=CompletionStatus.COMPLETED.value,
            nodes=tuple(self._to_snapshot(r) for r in rows),
        )

    def _require_instance(self, instance_id: str) -> SciStudentCurriculumInstance:
        instance = SciStudentCurriculumInstance.query.filter_by(
            instance_id=instance_id
        ).first()
        if instance is None:
            raise InstanceNotFoundError(f"Instance not found: {instance_id}")
        return instance

    @staticmethod
    def _summary(
        instance: SciStudentCurriculumInstance,
        *,
        node_state_count: int,
    ) -> InstanceSummary:
        return InstanceSummary(
            instance_id=instance.instance_id,
            student_id=instance.student_id,
            subject_code=instance.subject_code,
            edition_id=instance.edition_id,
            enrolled_at=format_dt(instance.enrolled_at) or "",
            is_active=bool(instance.is_active),
            is_completed=bool(instance.is_completed),
            completed_at=format_dt(instance.completed_at),
            node_state_count=node_state_count,
        )

    @staticmethod
    def _to_snapshot(row: SciCurriculumNodeState) -> NodeStateSnapshot:
        return NodeStateSnapshot(
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
