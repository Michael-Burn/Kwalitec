"""TwinUpdateResult — honest Twin Update Coordinator outcomes.

Success carries the persisted Successor Twin acknowledgement. Failure never
fabricates educational state or partial successors (Capability 4.9.6).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from app.application.twin_repository.types import PersistAcknowledgement
from app.domain.twin.digital_twin import DigitalTwin


class TwinUpdateFailureReason(str, Enum):
    """Honest Twin Update Coordinator failure postures."""

    MISSING_CURRENT_TWIN = "missing_current_twin"
    INVALID_EVIDENCE = "invalid_evidence"
    STRATEGY_FAILURE = "strategy_failure"
    COMPOSER_FAILURE = "composer_failure"
    REPOSITORY_FAILURE = "repository_failure"


@dataclass(frozen=True)
class TwinUpdateSuccess:
    """Success cargo after Strategy → Composer → Repository persistence."""

    successor_twin: DigitalTwin
    acknowledgement: PersistAcknowledgement
    strategy_identities: tuple[str, ...]


@dataclass(frozen=True)
class TwinUpdateFailure:
    """Honesty cargo when Twin Update cannot complete lawfully."""

    reason: TwinUpdateFailureReason
    detail: str | None = None


TwinUpdateResult = TwinUpdateSuccess | TwinUpdateFailure
