"""SQLAlchemy EvidenceRepository — durable append-only evidence."""

from __future__ import annotations

import json
import uuid
from typing import Any

from app.extensions import db
from app.infrastructure.persistence.unit_of_work import UnitOfWork
from app.infrastructure.repositories.contracts import EvidenceRepository
from app.models.v2_aggregate import V2EvidenceEvent


class SqlAlchemyEvidenceRepository(EvidenceRepository):
    """Persist evidence in ``v2_evidence_events``."""

    def __init__(self, *, uow: UnitOfWork | None = None) -> None:
        self._uow = uow
        self._available = True

    @property
    def repository_id(self) -> str:
        return "sqlalchemy_evidence_repository"

    def is_available(self) -> bool:
        return self._available

    def set_available(self, available: bool) -> None:
        self._available = available

    def append_evidence(
        self,
        *,
        learner_id: str,
        subject_id: str,
        evidence_type: str,
        payload: dict[str, Any] | None = None,
        correlation_id: str = "",
        causation_id: str = "",
    ) -> dict[str, Any]:
        record_id = uuid.uuid4().hex
        row = V2EvidenceEvent(
            record_id=record_id,
            learner_id=learner_id,
            subject_id=subject_id,
            evidence_type=evidence_type,
            payload=json.dumps(payload or {}, default=str, sort_keys=True),
            correlation_id=correlation_id or "",
            causation_id=causation_id or "",
        )
        db.session.add(row)
        if self._uow is not None and self._uow.is_active:
            self._uow.register(
                self.repository_id,
                "append_evidence",
                {"record_id": record_id},
            )
            db.session.flush()
        else:
            db.session.commit()
        return {
            "record_id": record_id,
            "learner_id": learner_id,
            "subject_id": subject_id,
            "evidence_type": evidence_type,
            "recorded_at": row.recorded_at.isoformat(),
            "correlation_id": correlation_id or "",
            "causation_id": causation_id or "",
        }

    def list_evidence(
        self, learner_id: str, *, subject_id: str | None = None
    ) -> tuple[dict[str, Any], ...]:
        query = db.session.query(V2EvidenceEvent).filter_by(learner_id=learner_id)
        if subject_id is not None:
            query = query.filter_by(subject_id=subject_id)
        rows = query.order_by(V2EvidenceEvent.recorded_at.asc()).all()
        return tuple(
            {
                "record_id": r.record_id,
                "learner_id": r.learner_id,
                "subject_id": r.subject_id,
                "evidence_type": r.evidence_type,
                "payload": json.loads(r.payload),
                "recorded_at": r.recorded_at.isoformat(),
                "correlation_id": r.correlation_id,
                "causation_id": r.causation_id,
                "source": "sqlalchemy",
                "metadata": {},
            }
            for r in rows
        )
