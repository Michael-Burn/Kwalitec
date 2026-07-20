"""SQLAlchemy persistence models for Education OS aggregates.

Storage mapping and repository adapters. Models hold no behaviour.
Repositories translate only — no educational intelligence.
"""

from __future__ import annotations

from infrastructure.persistence.sqlalchemy.base import NAMING_CONVENTION, Base, metadata
from infrastructure.persistence.sqlalchemy.models import (
    ConceptModel,
    DecisionModel,
    DiagnosisModel,
    DigitalTwinModel,
    EvidenceModel,
    HypothesisModel,
    LearningEpisodeModel,
    OrchestratorModel,
    PriorityModel,
    TeachingIntentionModel,
    TeachingPlanModel,
    TeachingStrategyModel,
)
from infrastructure.persistence.sqlalchemy.session import create_session_factory
from infrastructure.persistence.sqlalchemy.unit_of_work import SqlAlchemyUnitOfWork

__all__ = [
    "Base",
    "NAMING_CONVENTION",
    "metadata",
    "create_session_factory",
    "SqlAlchemyUnitOfWork",
    "DigitalTwinModel",
    "LearningEpisodeModel",
    "EvidenceModel",
    "ConceptModel",
    "TeachingPlanModel",
    "DiagnosisModel",
    "HypothesisModel",
    "PriorityModel",
    "TeachingIntentionModel",
    "TeachingStrategyModel",
    "DecisionModel",
    "OrchestratorModel",
]
