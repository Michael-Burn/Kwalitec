"""Create Student Curriculum Instances and initialise node states (EI-004)."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from app.application.curriculum_publishing.edition_graph_loader import (
    EditionGraphLoader,
)
from app.application.student_curriculum_binding.dto import (
    BindingResult,
    InstanceSummary,
    format_dt,
)
from app.application.student_curriculum_binding.exceptions import (
    BindingGateError,
    EditionNotFoundError,
    gate_from_invariant,
)
from app.domain.curriculum_extraction.publication_state import PublicationState
from app.domain.curriculum_knowledge_graph.value_objects.stable_curriculum_id import (
    StableCurriculumId,
)
from app.domain.student_curriculum_binding.invariants import (
    BindingInvariantError,
    assert_can_bind,
)
from app.domain.student_curriculum_binding.node_state import initial_node_state
from app.extensions import db
from app.models.curriculum_knowledge_graph import CkgGraphEdition
from app.models.student_curriculum_binding import (
    SciCurriculumNodeState,
    SciStudentCurriculumInstance,
)


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class StudentCurriculumBindingService:
    """Bind a student to a Published Curriculum Edition and seed node states."""

    def __init__(self, graph_loader: EditionGraphLoader | None = None) -> None:
        self._loader = graph_loader or EditionGraphLoader()

    def create_instance(
        self,
        *,
        student_id: int,
        edition_id: str,
        subject_code: str | None = None,
    ) -> BindingResult:
        """Create a Student Curriculum Instance against a published edition.

        Idempotent when the same student already has an active binding to the
        same edition — returns the existing instance without duplicating nodes.

        Args:
            student_id: Application user id (student).
            edition_id: Published CKG edition id.
            subject_code: Optional subject override; defaults to edition subject.

        Returns:
            BindingResult with instance summary and initialisation counts.

        Raises:
            EditionNotFoundError: Edition does not exist.
            BindingGateError: Draft/archived edition, subject mismatch, or
                conflicting active binding to a different edition.
        """
        edition = CkgGraphEdition.query.filter_by(edition_id=edition_id).first()
        if edition is None:
            raise EditionNotFoundError(f"Edition not found: {edition_id}")

        requested_subject = (subject_code or edition.subject_code).strip().upper()
        existing = (
            SciStudentCurriculumInstance.query.filter_by(
                student_id=student_id,
                subject_code=requested_subject,
                is_active=True,
            )
            .order_by(SciStudentCurriculumInstance.id.asc())
            .first()
        )

        try:
            assert_can_bind(
                student_id=student_id,
                edition_id=edition_id,
                publication_state=edition.publication_state,
                edition_subject_code=edition.subject_code,
                requested_subject_code=requested_subject,
                existing_active_instance_id=(
                    existing.instance_id if existing else None
                ),
                existing_active_edition_id=existing.edition_id if existing else None,
            )
        except BindingInvariantError as exc:
            raise gate_from_invariant(exc) from exc

        if existing is not None and existing.edition_id == edition_id:
            count = SciCurriculumNodeState.query.filter_by(
                instance_id=existing.instance_id
            ).count()
            return BindingResult(
                instance=self._summary(existing, node_state_count=count),
                created=False,
                node_states_initialised=0,
            )

        if edition.publication_state != PublicationState.PUBLISHED.value:
            raise BindingGateError(
                f"Edition {edition_id} is not published "
                f"(state={edition.publication_state})"
            )

        instance_id = f"sci-{uuid.uuid4().hex[:16]}"
        now = _utc_now()
        instance = SciStudentCurriculumInstance(
            instance_id=instance_id,
            student_id=student_id,
            subject_code=requested_subject,
            edition_id=edition_id,
            enrolled_at=now,
            is_active=True,
            is_completed=False,
            completed_at=None,
            created_at=now,
            updated_at=now,
        )
        db.session.add(instance)
        db.session.flush()

        initialised = self.initialise_node_states(instance_id)
        db.session.commit()

        return BindingResult(
            instance=self._summary(instance, node_state_count=initialised),
            created=True,
            node_states_initialised=initialised,
        )

    def initialise_node_states(self, instance_id: str) -> int:
        """Create default educational state rows for every curriculum node.

        Idempotent: existing ``(instance_id, node_stable_id)`` rows are skipped.
        Does not modify curriculum knowledge graph rows.

        Returns:
            Number of newly created node state rows.
        """
        instance = SciStudentCurriculumInstance.query.filter_by(
            instance_id=instance_id
        ).first()
        if instance is None:
            raise BindingGateError(f"Instance not found: {instance_id}")

        stable_ids = self._loader.collect_stable_ids(instance.edition_id)
        if not stable_ids:
            return 0

        existing = {
            row.node_stable_id
            for row in SciCurriculumNodeState.query.filter_by(
                instance_id=instance_id
            ).all()
        }

        created = 0
        now = _utc_now()
        for stable_id in sorted(stable_ids):
            if stable_id in existing:
                continue
            try:
                kind = StableCurriculumId.of(stable_id).kind.value
            except ValueError:
                kind = "unknown"
            snapshot = initial_node_state(stable_id, kind)
            db.session.add(
                SciCurriculumNodeState(
                    instance_id=instance_id,
                    node_stable_id=snapshot.node_stable_id,
                    node_kind=snapshot.node_kind,
                    mastery=snapshot.mastery,
                    confidence=snapshot.confidence,
                    revision_status=snapshot.revision_status,
                    attempts=snapshot.attempts,
                    total_study_time_minutes=snapshot.total_study_time_minutes,
                    last_interaction_at=snapshot.last_interaction_at,
                    completion_status=snapshot.completion_status,
                    evidence_count=snapshot.evidence_count,
                    created_at=now,
                    updated_at=now,
                )
            )
            created += 1
        db.session.flush()
        return created

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
