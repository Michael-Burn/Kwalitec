"""Outbound ports — repository and infrastructure interfaces only."""

from __future__ import annotations

from application.ports.clock import Clock
from application.ports.event_publisher import ApplicationEventPublisher
from application.ports.repositories import (
    DecisionRepository,
    DiagnosisRepository,
    DigitalTwinRepository,
    EvidenceRepository,
    HypothesisRepository,
    LearningEpisodeRepository,
    OrchestratorRepository,
    PriorityRepository,
    SubjectKnowledgeRepository,
    TeachingIntentionRepository,
    TeachingPlanRepository,
    TeachingStrategyRepository,
)
from application.ports.transaction_manager import TransactionManager
from application.ports.unit_of_work import UnitOfWork
from application.ports.uuid_generator import UUIDGenerator

__all__ = [
    "ApplicationEventPublisher",
    "Clock",
    "DecisionRepository",
    "DiagnosisRepository",
    "DigitalTwinRepository",
    "EvidenceRepository",
    "HypothesisRepository",
    "LearningEpisodeRepository",
    "OrchestratorRepository",
    "PriorityRepository",
    "SubjectKnowledgeRepository",
    "TeachingIntentionRepository",
    "TeachingPlanRepository",
    "TeachingStrategyRepository",
    "TransactionManager",
    "UUIDGenerator",
    "UnitOfWork",
]
