"""Learner-facing application DTOs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LearnerStateDTO:
    """Read model of learner activity state from the Digital Twin."""

    twin_id: str
    student_id: str
    learner_state_id: str
    activity_status: str
    twin_status: str
    concept_count: int
    evidence_count: int
    intervention_count: int
