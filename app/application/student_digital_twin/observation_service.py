"""Observation recording — append-only educational facts."""

from __future__ import annotations

import uuid
from collections.abc import Mapping
from datetime import datetime
from typing import Any

from app.application.student_digital_twin.persistence import TwinPersistenceService
from app.domain.student_digital_twin.observation import Observation, ObservationKind
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin
from app.extensions import db


class ObservationService:
    """Append immutable observations to a Twin."""

    def __init__(self, *, persistence: TwinPersistenceService | None = None) -> None:
        self._persistence = persistence or TwinPersistenceService()

    def record(
        self,
        twin: StudentDigitalTwin,
        *,
        kind: ObservationKind | str,
        curriculum_entity_id: str = "",
        curriculum_entity_kind: str = "",
        evidence_reference: str = "",
        provenance: str = "",
        metadata: Mapping[str, Any] | None = None,
        recorded_at: datetime | None = None,
        observation_id: str | None = None,
        persist: bool = True,
    ) -> tuple[StudentDigitalTwin, Observation]:
        """Append one observation; optionally persist immediately."""
        obs = Observation.create(
            observation_id=observation_id or f"obs-{uuid.uuid4().hex[:16]}",
            kind=kind,
            twin_id=twin.twin_id,
            student_id=twin.student.student_id,
            recorded_at=recorded_at,
            curriculum_entity_id=curriculum_entity_id,
            curriculum_entity_kind=curriculum_entity_kind,
            evidence_reference=evidence_reference,
            provenance=provenance,
            metadata=metadata,
        )
        updated = twin.append_observation(obs)
        if persist:
            self._persistence.save_twin_root(updated)
            self._persistence.append_observation(obs)
            db.session.commit()
        return updated, obs
