"""Persistence DTOs for TeachingStrategy."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StrategyIntentionReferenceDTO:
    intention_id: str
    intention_type: str


@dataclass(frozen=True, slots=True)
class StrategyDiagnosisReferenceDTO:
    diagnosis_id: str
    diagnosis_type: str


@dataclass(frozen=True, slots=True)
class StrategyHypothesisReferenceDTO:
    hypothesis_id: str


@dataclass(frozen=True, slots=True)
class SecondaryStrategyReferenceDTO:
    strategy_type: str
    sequence_order: int


@dataclass(frozen=True, slots=True)
class StrategyGoalDTO:
    goal_id: str
    statement: str
    strategy_type: str
    expected_evidence_hint: str | None = None


@dataclass(frozen=True, slots=True)
class StrategyRationaleDTO:
    rationale_id: str
    statement: str
    diagnosis_link: str | None = None
    hypothesis_link: str | None = None
    intention_link: str | None = None


@dataclass(frozen=True, slots=True)
class StrategyEffectivenessDTO:
    level: str
    rationale: str | None = None


@dataclass(frozen=True, slots=True)
class InstructionalComplexityDTO:
    level: str
    rationale: str | None = None


@dataclass(frozen=True, slots=True)
class StrategyConstraintDTO:
    constraint_id: str
    kind: str
    statement: str
    forbidden_strategy_type: str | None = None
    max_complexity: str | None = None


@dataclass(frozen=True, slots=True)
class TeachingStrategyDTO:
    strategy_id: str
    student_id: str
    primary_strategy: str
    goal: StrategyGoalDTO
    rationale: StrategyRationaleDTO
    effectiveness: StrategyEffectivenessDTO
    complexity: InstructionalComplexityDTO
    intention_references: tuple[StrategyIntentionReferenceDTO, ...]
    diagnosis_references: tuple[StrategyDiagnosisReferenceDTO, ...]
    hypothesis_references: tuple[StrategyHypothesisReferenceDTO, ...]
    secondary_strategies: tuple[SecondaryStrategyReferenceDTO, ...]
    constraints: tuple[StrategyConstraintDTO, ...]
    composition_pattern: str | None
    status: str
    retire_reason: str | None = None
