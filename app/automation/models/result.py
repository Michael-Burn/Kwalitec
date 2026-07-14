"""AutomationResult — immutable outcome of one automation execution."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from types import MappingProxyType
from typing import Any


class AutomationStatus(str, Enum):
    """Version 1 execution statuses."""

    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"


ALLOWED_STATUSES: frozenset[AutomationStatus] = frozenset(AutomationStatus)


@dataclass(frozen=True)
class AutomationResult:
    """Immutable cargo returned by AutomationExecutor / AutomationService."""

    workflow_id: str
    status: AutomationStatus
    started_at: datetime
    completed_at: datetime
    duration_ms: int
    warnings: tuple[str, ...]
    errors: tuple[str, ...]
    outputs: MappingProxyType[str, Any]
