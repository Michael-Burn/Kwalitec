"""StudentDigitalTwinService — Twin lifecycle (create / load)."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from app.application.learning_graph.learning_graph_service import LearningGraphService
from app.application.student_digital_twin.persistence import TwinPersistenceService
from app.domain.student_digital_twin.student import Student
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin
from app.extensions import db
from app.models.student_digital_twin import SdtStudentDigitalTwin


class StudentDigitalTwinService:
    """Create and load Student Digital Twin aggregates."""

    def __init__(
        self,
        *,
        persistence: TwinPersistenceService | None = None,
        learning_graph: LearningGraphService | None = None,
    ) -> None:
        self._persistence = persistence or TwinPersistenceService()
        self._learning_graph = learning_graph or LearningGraphService()

    def create(
        self,
        *,
        student_id: str,
        display_name: str = "",
        subject_code: str = "",
        workspace_id: str = "",
        external_user_id: str | None = None,
        twin_id: str | None = None,
        created_at: datetime | None = None,
    ) -> StudentDigitalTwin:
        """Create and persist a new Twin for a learner scope."""
        existing = (
            SdtStudentDigitalTwin.query.filter_by(
                student_id=student_id,
                workspace_id=workspace_id or "",
                subject_code=subject_code or "",
            ).first()
        )
        if existing is not None:
            loaded = self._persistence.load_twin(existing.twin_id)
            if loaded is not None:
                # Ensure Learning Graph exists for legacy Twins created before SDT-003.
                self._learning_graph.get_or_create_for_twin(loaded, persist=True)
                return loaded

        student = Student(
            student_id=student_id,
            display_name=display_name,
            subject_code=subject_code or "",
            workspace_id=workspace_id or "",
            external_user_id=external_user_id,
        )
        twin = StudentDigitalTwin.create(
            twin_id=twin_id or f"twin-{uuid.uuid4().hex[:16]}",
            student=student,
            created_at=created_at or datetime.now(UTC).replace(tzinfo=None),
        )
        self._persistence.save_twin_root(twin)
        self._learning_graph.create_for_twin(twin, persist=False)
        db.session.commit()
        return twin

    def get(self, twin_id: str) -> StudentDigitalTwin | None:
        """Load a Twin aggregate by id."""
        return self._persistence.load_twin(twin_id)

    def get_or_create(
        self,
        *,
        student_id: str,
        workspace_id: str = "",
        subject_code: str = "",
        **kwargs: object,
    ) -> StudentDigitalTwin:
        """Idempotent Twin bootstrap for a learner scope."""
        return self.create(
            student_id=student_id,
            workspace_id=workspace_id,
            subject_code=subject_code,
            **kwargs,  # type: ignore[arg-type]
        )

    def list_twins_for_student(self, student_id: str) -> list[StudentDigitalTwin]:
        rows = SdtStudentDigitalTwin.query.filter_by(student_id=student_id).all()
        twins: list[StudentDigitalTwin] = []
        for row in rows:
            twin = self._persistence.load_twin(row.twin_id)
            if twin is not None:
                twins.append(twin)
        return twins
