"""Persistence DTOs for EducationalOrchestrator."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ApprovedDecisionReferenceDTO:
    decision_id: str
    approved: bool


@dataclass(frozen=True, slots=True)
class OrchestratorStrategyReferenceDTO:
    strategy_id: str
    strategy_type: str


@dataclass(frozen=True, slots=True)
class EpisodeReferenceDTO:
    episode_id: str


@dataclass(frozen=True, slots=True)
class OrchestrationStageDTO:
    stage_id: str
    kind: str
    sequence_index: int
    label: str
    required: bool
    status: str
    evidence_collection_point: str | None = None
    episode_id: str | None = None


@dataclass(frozen=True, slots=True)
class OrchestrationPlanDTO:
    plan_id: str
    stages: tuple[OrchestrationStageDTO, ...]
    label: str


@dataclass(frozen=True, slots=True)
class OrchestrationStateDTO:
    status: str
    current_stage_id: str | None = None
    pause_reason: str | None = None


@dataclass(frozen=True, slots=True)
class OrchestratorDTO:
    orchestrator_id: str
    student_id: str
    decision_reference: ApprovedDecisionReferenceDTO
    strategy_references: tuple[OrchestratorStrategyReferenceDTO, ...]
    plan: OrchestrationPlanDTO
    episode_references: tuple[EpisodeReferenceDTO, ...]
    state: OrchestrationStateDTO
