"""Persistence DTOs for EducationalDecision."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DecisionPriorityReferenceDTO:
    priority_id: str


@dataclass(frozen=True, slots=True)
class DecisionIntentionReferenceDTO:
    intention_id: str
    intention_type: str


@dataclass(frozen=True, slots=True)
class DecisionStrategyReferenceDTO:
    strategy_id: str
    strategy_type: str


@dataclass(frozen=True, slots=True)
class ReadinessIndicatorDTO:
    indicator_id: str
    kind: str
    description: str
    supports_readiness: bool
    weight: float


@dataclass(frozen=True, slots=True)
class ExecutionConstraintDTO:
    constraint_id: str
    kind: str
    statement: str
    related_indicator_kind: str | None = None
    min_readiness: str | None = None
    min_confidence: str | None = None
    forbidden_outcome: str | None = None


@dataclass(frozen=True, slots=True)
class DecisionReasonDTO:
    reason_id: str
    statement: str
    code: str | None = None


@dataclass(frozen=True, slots=True)
class DecisionConfidenceDTO:
    level: str
    ratio: float | None = None


@dataclass(frozen=True, slots=True)
class ReadinessLevelDTO:
    band: str
    ratio: float | None = None
    rationale: str | None = None


@dataclass(frozen=True, slots=True)
class DecisionDTO:
    decision_id: str
    student_id: str
    priority_references: tuple[DecisionPriorityReferenceDTO, ...]
    intention_references: tuple[DecisionIntentionReferenceDTO, ...]
    strategy_references: tuple[DecisionStrategyReferenceDTO, ...]
    indicators: tuple[ReadinessIndicatorDTO, ...]
    constraints: tuple[ExecutionConstraintDTO, ...]
    reasons: tuple[DecisionReasonDTO, ...]
    confidence: DecisionConfidenceDTO
    readiness: ReadinessLevelDTO
    status: str
    outcome: str | None = None
    reconsideration_reason: str | None = None
