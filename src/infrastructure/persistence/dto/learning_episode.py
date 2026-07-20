"""Persistence DTOs for LearningEpisode."""

from __future__ import annotations

from dataclasses import dataclass

from infrastructure.persistence.dto.common import (
    ConceptReferenceDTO,
    LearningObjectiveReferenceDTO,
)


@dataclass(frozen=True, slots=True)
class EpisodeGoalDTO:
    goal_id: str
    statement: str
    educational_purpose: str
    primary_dimension: str


@dataclass(frozen=True, slots=True)
class EpisodeStepDTO:
    step_id: str
    kind: str
    sequence_index: int
    label: str
    required: bool
    status: str


@dataclass(frozen=True, slots=True)
class EpisodeDurationDTO:
    planned_minutes: int | None = None
    band: str | None = None


@dataclass(frozen=True, slots=True)
class EpisodeReflectionDTO:
    reflection_id: str
    reflection_type: str
    content: str
    perceived_difficulty: str | None = None
    perceived_understanding: str | None = None


@dataclass(frozen=True, slots=True)
class EpisodeOutcomeDTO:
    outcome_id: str
    kind: str
    summary: str


@dataclass(frozen=True, slots=True)
class LearningEpisodeDTO:
    episode_id: str
    student_id: str
    teaching_goal: EpisodeGoalDTO
    teaching_strategy_id: str
    learning_objectives: tuple[LearningObjectiveReferenceDTO, ...]
    steps: tuple[EpisodeStepDTO, ...]
    concept_references: tuple[ConceptReferenceDTO, ...]
    primary_dimension: str
    duration: EpisodeDurationDTO | None
    selection_rationale: str | None
    status: str
    reflection: EpisodeReflectionDTO | None
    outcome: EpisodeOutcomeDTO | None
    evidence_ids: tuple[str, ...]
