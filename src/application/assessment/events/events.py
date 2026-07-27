"""Application-layer assessment events (lightweight records; no bus)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssessmentSessionCreatedApplicationEvent:
    session_id: str
    instrument_id: str
    purpose: str


@dataclass(frozen=True, slots=True)
class AssessmentSessionStartedApplicationEvent:
    session_id: str


@dataclass(frozen=True, slots=True)
class AssessmentResponseCommittedApplicationEvent:
    session_id: str
    question_id: str
    attempt_number: int


@dataclass(frozen=True, slots=True)
class AssessmentSessionSubmittedApplicationEvent:
    session_id: str
