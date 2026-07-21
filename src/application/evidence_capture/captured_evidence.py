"""CapturedEvidence — timestamped, auditable wrapper around a session outcome.

Immutable educational evidence cargo. Does not persist, diagnose, or evolve
Twin state. Callers own any storage or downstream transformation.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.evidence_capture.learning_session_outcome import (
    LearningSessionOutcome,
)

_DEFAULT_PROVENANCE = "study_session_reflection"


@dataclass(frozen=True, slots=True)
class CapturedEvidence:
    """Immutable, timestamped capture of a ``LearningSessionOutcome``.

    Attributes:
        evidence_id: Stable correlation identity for this capture.
        captured_at: When the outcome was recorded as evidence.
        outcome: Observational session outcome facts.
        provenance: Attributable capture channel (not educational meaning).
    """

    evidence_id: str
    captured_at: datetime
    outcome: LearningSessionOutcome
    provenance: str = _DEFAULT_PROVENANCE

    def __post_init__(self) -> None:
        evidence_id = (self.evidence_id or "").strip()
        if not evidence_id:
            raise ValueError("evidence_id is required")
        object.__setattr__(self, "evidence_id", evidence_id)

        if not isinstance(self.captured_at, datetime):
            raise ValueError("captured_at must be a datetime")

        if not isinstance(self.outcome, LearningSessionOutcome):
            raise ValueError("outcome must be a LearningSessionOutcome")

        provenance = (self.provenance or "").strip() or _DEFAULT_PROVENANCE
        object.__setattr__(self, "provenance", provenance)
