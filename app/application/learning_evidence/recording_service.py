"""Append-only recording of educational evidence (EI-005)."""

from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from typing import Any

from app.application.learning_evidence.dto import RecordEvidenceResult
from app.application.learning_evidence.exceptions import (
    EvidenceGateError,
    EvidenceNotFoundError,
    gate_from_invariant,
)
from app.domain.learning_evidence.evidence_event import EvidenceEvent
from app.domain.learning_evidence.evidence_type import EvidenceSource, EvidenceType
from app.domain.learning_evidence.invariants import (
    EvidenceInvariantError,
    assert_can_record,
)
from app.domain.learning_evidence.payload_schema import assert_payload_schema
from app.extensions import db
from app.models.learning_evidence import LeeEvidenceEvent
from app.models.student_curriculum_binding import (
    SciCurriculumNodeState,
    SciStudentCurriculumInstance,
)


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class EvidenceRecordingService:
    """Persist immutable educational evidence events against an SCI."""

    def record_evidence(
        self,
        *,
        instance_id: str,
        node_stable_id: str,
        evidence_type: str | EvidenceType,
        source: str | EvidenceSource,
        occurred_at: datetime | None = None,
        metadata: dict[str, Any] | None = None,
        corrects_evidence_id: str | None = None,
    ) -> RecordEvidenceResult:
        """Append one educational observation.

        Does not calculate mastery, update confidence, generate recommendations,
        or modify curriculum content. Optionally increments the SCI node-state
        ``evidence_count`` counter (observation bookkeeping only).

        Args:
            instance_id: Active Student Curriculum Instance id.
            node_stable_id: Curriculum node within the bound edition.
            evidence_type: Catalogue or extensible snake_case type.
            source: Observation source channel.
            occurred_at: When the activity occurred (defaults to now).
            metadata: Observational payload (JSON object).
            corrects_evidence_id: Optional prior evidence id this event corrects.

        Returns:
            RecordEvidenceResult with the immutable event view.

        Raises:
            EvidenceGateError: Integrity or payload validation failed.
            EvidenceNotFoundError: Correction target does not exist.
        """
        instance = SciStudentCurriculumInstance.query.filter_by(
            instance_id=instance_id
        ).first()
        node_state = None
        if instance is not None:
            node_state = SciCurriculumNodeState.query.filter_by(
                instance_id=instance_id,
                node_stable_id=node_stable_id,
            ).first()

        when = occurred_at if occurred_at is not None else _utc_now()
        source_value = (
            source.value if isinstance(source, EvidenceSource) else source
        )

        try:
            normalised_type = assert_can_record(
                instance_id=instance_id,
                instance_is_active=(
                    None if instance is None else bool(instance.is_active)
                ),
                node_stable_id=node_stable_id,
                node_belongs_to_instance=node_state is not None,
                evidence_type=evidence_type,
                source=source_value,
                occurred_at=when,
            )
            payload = assert_payload_schema(normalised_type, metadata)
        except EvidenceInvariantError as exc:
            raise gate_from_invariant(exc) from exc

        if corrects_evidence_id:
            prior = LeeEvidenceEvent.query.filter_by(
                evidence_id=corrects_evidence_id
            ).first()
            if prior is None:
                raise EvidenceNotFoundError(
                    f"Correction target not found: {corrects_evidence_id}"
                )
            if prior.instance_id != instance_id:
                raise EvidenceGateError(
                    f"Correction target {corrects_evidence_id} belongs to a "
                    f"different Student Curriculum Instance"
                )

        assert instance is not None  # gated above
        evidence_id = f"lee-{uuid.uuid4().hex[:16]}"
        recorded_at = _utc_now()
        row = LeeEvidenceEvent(
            evidence_id=evidence_id,
            instance_id=instance_id,
            student_id=instance.student_id,
            node_stable_id=node_stable_id.strip(),
            evidence_type=normalised_type,
            occurred_at=when.replace(tzinfo=None) if when.tzinfo else when,
            recorded_at=recorded_at,
            source=(
                source_value.value
                if isinstance(source_value, EvidenceSource)
                else str(source_value).strip()
            ),
            metadata_json=json.dumps(payload, sort_keys=True),
            corrects_evidence_id=corrects_evidence_id,
        )
        db.session.add(row)

        # Observation bookkeeping only — never mastery / confidence / completion.
        if node_state is not None:
            node_state.evidence_count = int(node_state.evidence_count or 0) + 1
            node_state.last_interaction_at = row.occurred_at
            node_state.updated_at = recorded_at

        db.session.commit()

        return RecordEvidenceResult(
            event=self._to_event(row),
            created=True,
        )

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
