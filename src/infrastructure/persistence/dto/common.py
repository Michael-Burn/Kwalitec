"""Shared persistence DTO primitives for educational references."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ConceptReferenceDTO:
    concept_id: str
    label: str | None = None


@dataclass(frozen=True, slots=True)
class LearningObjectiveReferenceDTO:
    objective_id: str
    label: str | None = None


@dataclass(frozen=True, slots=True)
class MisconceptionReferenceDTO:
    misconception_id: str
    related_concept_id: str | None = None
    label: str | None = None
