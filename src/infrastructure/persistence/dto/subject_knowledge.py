"""Persistence DTOs for Subject Knowledge Concept aggregates."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ConceptBoundaryDTO:
    inclusion: str
    exclusion: str
    key_contrast: str | None = None


@dataclass(frozen=True, slots=True)
class MasteryIndicatorDTO:
    description: str
    observable_signal: str
    dimension: str | None = None


@dataclass(frozen=True, slots=True)
class LearningObjectiveDTO:
    objective_id: str
    concept_id: str
    statement: str
    success_criteria: tuple[str, ...]
    mastery_indicators: tuple[MasteryIndicatorDTO, ...]


@dataclass(frozen=True, slots=True)
class RepresentationDTO:
    representation_id: str
    concept_id: str
    kind: str
    description: str
    educational_purpose: str


@dataclass(frozen=True, slots=True)
class MisconceptionDTO:
    misconception_id: str
    concept_id: str
    description: str
    incorrect_reasoning: str
    likely_causes: tuple[str, ...]
    observable_evidence: tuple[str, ...]
    recommended_teaching_intentions: tuple[str, ...]
    recommended_strategies: tuple[str, ...]
    repair_evidence: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ApplicationContextDTO:
    context_id: str
    concept_id: str
    description: str
    task_demand: str
    assumptions: str | None = None
    constraints: str | None = None


@dataclass(frozen=True, slots=True)
class TransferContextDTO:
    context_id: str
    concept_id: str
    description: str
    surface_variation: str
    underlying_demand: str
    transfer_level: str
    base_application_context_id: str | None = None


@dataclass(frozen=True, slots=True)
class DependencyDTO:
    target_concept_id: str
    kind: str
    description: str


@dataclass(frozen=True, slots=True)
class ConceptDTO:
    concept_id: str
    canonical_name: str
    core_meaning: str
    boundary: ConceptBoundaryDTO
    learning_objectives: tuple[LearningObjectiveDTO, ...]
    representations: tuple[RepresentationDTO, ...]
    misconceptions: tuple[MisconceptionDTO, ...]
    application_contexts: tuple[ApplicationContextDTO, ...]
    transfer_contexts: tuple[TransferContextDTO, ...]
    dependencies: tuple[DependencyDTO, ...]
