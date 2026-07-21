"""Persistence DTOs for onboarding draft sessions (BR-004)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class OnboardingSessionDTO:
    onboarding_id: str
    student_id: str
    status: str
    current_step: str
    payloads: dict[str, dict[str, Any]]
    saved_steps: list[str]
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None = None
    row_version: int = 1


@dataclass(frozen=True, slots=True)
class SessionCheckpointDTO:
    session_id: str
    events: list[dict[str, Any]] = field(default_factory=list)
    updated_at: datetime | None = None
    row_version: int = 1
