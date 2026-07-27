"""Assessment application queries (skeletons)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetAssessmentSessionQuery:
    session_id: str


@dataclass(frozen=True, slots=True)
class ListStudentAssessmentSessionsQuery:
    student_id: str


@dataclass(frozen=True, slots=True)
class GetAssessmentInstrumentQuery:
    instrument_id: str


@dataclass(frozen=True, slots=True)
class ListObservationsForSessionQuery:
    session_id: str
