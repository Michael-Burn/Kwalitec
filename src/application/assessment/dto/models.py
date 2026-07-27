"""Assessment application DTOs — boundary types only."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class QuestionReferenceDTO:
    question_id: str
    item_type: str
    version: str
    learning_objective_id: str
    learning_objective_label: str | None = None
    curriculum_entity_id: str | None = None
    knowledge_level: str | None = None
    difficulty: str | None = None
    estimated_time_seconds: int | None = None


@dataclass(frozen=True, slots=True)
class AssessmentInstrumentDTO:
    instrument_id: str
    assessment_type: str
    purpose: str
    title: str
    version: str
    question_count: int
    learning_objective_ids: tuple[str, ...] = ()
    questions: tuple[QuestionReferenceDTO, ...] = ()


@dataclass(frozen=True, slots=True)
class AssessmentAttemptDTO:
    session_id: str
    question_id: str
    attempt_number: int
    committed: bool
    response_payload: dict[str, Any] = field(default_factory=dict)
    confidence: int | None = None
    response_time_ms: int | None = None
    hints_used: int = 0
    retries: int = 0
    outcome: str | None = None
    abandoned: bool = False
    skipped: bool = False


@dataclass(frozen=True, slots=True)
class AssessmentSessionDTO:
    session_id: str
    student_id: str
    instrument_id: str
    purpose: str
    assessment_type: str
    status: str
    question_ids: tuple[str, ...] = ()
    twin_id: str | None = None
    mission_id: str | None = None
    attempt_count: int = 0
    observation_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class AssessmentObservationDTO:
    observation_id: str
    session_id: str
    kind: str
    evidence_source: str
    question_id: str | None = None
    provenance: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AssessmentResultDTO:
    result_id: str
    session_id: str
    observation_ids: tuple[str, ...] = ()
    evidence_strength: str | None = None
