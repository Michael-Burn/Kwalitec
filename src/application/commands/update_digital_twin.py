"""UpdateDigitalTwin command."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class TwinUpdateKind(StrEnum):
    """Kinds of Twin memory updates coordinated by the application layer.

    Values are supplied by upstream educational processes; application does not
    compute mastery, retention, or confidence.
    """

    RECORD_EVIDENCE = "record_evidence"
    UPDATE_MASTERY = "update_mastery"
    UPDATE_RETENTION = "update_retention"
    UPDATE_CONFIDENCE = "update_confidence"
    UPDATE_ACTIVITY = "update_activity"


@dataclass(frozen=True, slots=True)
class UpdateDigitalTwin:
    """Apply a supplied Twin memory update and commit.

    Educational values (bands, ratios, evidence types) are inputs — never
    calculated here.
    """

    twin_id: str
    update_kind: TwinUpdateKind
    evidence_id: str | None = None
    evidence_type: str | None = None
    concept_id: str | None = None
    mastery_band: str | None = None
    mastery_ratio: float | None = None
    retention_band: str | None = None
    retention_ratio: float | None = None
    confidence_level: str | None = None
    confidence_ratio: float | None = None
    activity_status: str | None = None
    note: str | None = None
