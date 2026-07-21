"""Education OS SQLAlchemy persistence models."""

from __future__ import annotations

from infrastructure.persistence.sqlalchemy.models.auth_token import AuthTokenModel
from infrastructure.persistence.sqlalchemy.models.decision import DecisionModel
from infrastructure.persistence.sqlalchemy.models.diagnosis import DiagnosisModel
from infrastructure.persistence.sqlalchemy.models.digital_twin import DigitalTwinModel
from infrastructure.persistence.sqlalchemy.models.evidence import EvidenceModel
from infrastructure.persistence.sqlalchemy.models.hypothesis import HypothesisModel
from infrastructure.persistence.sqlalchemy.models.learning_episode import (
    LearningEpisodeModel,
)
from infrastructure.persistence.sqlalchemy.models.onboarding_session import (
    OnboardingSessionModel,
)
from infrastructure.persistence.sqlalchemy.models.orchestrator import OrchestratorModel
from infrastructure.persistence.sqlalchemy.models.priority import PriorityModel
from infrastructure.persistence.sqlalchemy.models.session_checkpoint import (
    SessionCheckpointModel,
)
from infrastructure.persistence.sqlalchemy.models.subject_knowledge import ConceptModel
from infrastructure.persistence.sqlalchemy.models.teaching_intention import (
    TeachingIntentionModel,
)
from infrastructure.persistence.sqlalchemy.models.teaching_plan import TeachingPlanModel
from infrastructure.persistence.sqlalchemy.models.teaching_strategy import (
    TeachingStrategyModel,
)
from infrastructure.persistence.sqlalchemy.models.user_account import UserAccountModel

__all__ = [
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
    "UserAccountModel",
    "AuthTokenModel",
    "OnboardingSessionModel",
    "SessionCheckpointModel",
]
