"""Checkpoint persistence for lifecycle operations (LP-001)."""

from __future__ import annotations

import json
from datetime import UTC, datetime

from app.application.learner_lifecycle.stages import (
    LifecycleStage,
    OperationStatus,
    OperationType,
)
from app.application.learner_lifecycle.versions import ORCHESTRATOR_VERSION
from app.extensions import db
from app.models.learner_lifecycle import LlpLifecycleOperation


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class LifecycleCheckpointStore:
    """Persist and update lifecycle operation checkpoints.

    Checkpoints are operational only — they never embed educational reasoning.
    """

    def start(
        self,
        *,
        operation_id: str,
        operation_type: OperationType,
        student_id: int | None = None,
        instance_id: str | None = None,
        correlation_id: str | None = None,
        attempt_count: int = 1,
    ) -> LlpLifecycleOperation:
        now = _utc_now()
        row = LlpLifecycleOperation(
            operation_id=operation_id,
            operation_type=operation_type.value,
            status=OperationStatus.IN_PROGRESS.value,
            student_id=student_id,
            instance_id=instance_id,
            correlation_id=correlation_id,
            completed_stages_json="[]",
            failed_stage=None,
            failure_cause=None,
            attempt_count=attempt_count,
            orchestrator_version=ORCHESTRATOR_VERSION,
            created_at=now,
            updated_at=now,
        )
        db.session.add(row)
        db.session.commit()
        return row

    def mark_stage_complete(
        self,
        operation_id: str,
        stage: LifecycleStage,
        *,
        instance_id: str | None = None,
        student_id: int | None = None,
    ) -> LlpLifecycleOperation:
        row = self.require(operation_id)
        completed = self._load_stages(row)
        if stage.value not in completed:
            completed.append(stage.value)
        row.completed_stages_json = json.dumps(completed)
        if instance_id is not None:
            row.instance_id = instance_id
        if student_id is not None:
            row.student_id = student_id
        row.updated_at = _utc_now()
        db.session.commit()
        return row

    def mark_failed(
        self,
        operation_id: str,
        *,
        stage: LifecycleStage,
        cause: str,
        instance_id: str | None = None,
    ) -> LlpLifecycleOperation:
        row = self.require(operation_id)
        row.status = OperationStatus.FAILED.value
        row.failed_stage = stage.value
        row.failure_cause = cause
        if instance_id is not None:
            row.instance_id = instance_id
        row.updated_at = _utc_now()
        db.session.commit()
        return row

    def mark_completed(self, operation_id: str) -> LlpLifecycleOperation:
        row = self.require(operation_id)
        row.status = OperationStatus.COMPLETED.value
        row.failed_stage = None
        row.failure_cause = None
        row.updated_at = _utc_now()
        db.session.commit()
        return row

    def require(self, operation_id: str) -> LlpLifecycleOperation:
        row = LlpLifecycleOperation.query.filter_by(operation_id=operation_id).first()
        if row is None:
            from app.application.learner_lifecycle.exceptions import (
                LifecycleNotFoundError,
            )

            raise LifecycleNotFoundError(
                f"Lifecycle operation not found: {operation_id}"
            )
        return row

    def latest_failed_for_instance(
        self, instance_id: str
    ) -> LlpLifecycleOperation | None:
        return (
            LlpLifecycleOperation.query.filter_by(
                instance_id=instance_id,
                status=OperationStatus.FAILED.value,
            )
            .order_by(LlpLifecycleOperation.id.desc())
            .first()
        )

    @staticmethod
    def _load_stages(row: LlpLifecycleOperation) -> list[str]:
        try:
            data = json.loads(row.completed_stages_json or "[]")
        except json.JSONDecodeError:
            data = []
        if not isinstance(data, list):
            return []
        return [str(x) for x in data if str(x).strip()]

    def completed_stages(self, operation_id: str) -> tuple[LifecycleStage, ...]:
        row = self.require(operation_id)
        return tuple(
            LifecycleStage(token)
            for token in self._load_stages(row)
            if token in {s.value for s in LifecycleStage}
        )
