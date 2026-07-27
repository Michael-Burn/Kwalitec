"""Assessment application commands (skeletons)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class CreateAssessmentSessionCommand:
    session_id: str
    student_id: str
    instrument_id: str
    twin_id: str | None = None
    mission_id: str | None = None


@dataclass(frozen=True, slots=True)
class StartAssessmentSessionCommand:
    session_id: str


@dataclass(frozen=True, slots=True)
class CommitAssessmentResponseCommand:
    session_id: str
    question_id: str
    response_payload: dict[str, Any] = field(default_factory=dict)
    confidence: int | None = None
    response_time_ms: int | None = None
    hints_used: int = 0
    retries: int = 0
    abandoned: bool = False
    skipped: bool = False


@dataclass(frozen=True, slots=True)
class SubmitAssessmentSessionCommand:
    session_id: str


@dataclass(frozen=True, slots=True)
class RecordAssessmentObservationCommand:
    observation_id: str
    session_id: str
    kind: str
    question_id: str | None = None
    provenance: dict[str, Any] = field(default_factory=dict)
