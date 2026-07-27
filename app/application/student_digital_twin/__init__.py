"""Student Digital Twin application package (SDT-001 / SDT-002).

StudentReasoningService orchestrates Twin updates by delegating educational
inference to the Educational Reasoning Engine (RuleRegistry). Curriculum
evidence is retrieved exclusively through CurriculumRetrievalService.
"""

from __future__ import annotations

from app.application.student_digital_twin.knowledge_gap_service import (
    KnowledgeGapService,
)
from app.application.student_digital_twin.learning_state_service import (
    LearningStateService,
)
from app.application.student_digital_twin.mastery_service import MasteryService
from app.application.student_digital_twin.observation_service import ObservationService
from app.application.student_digital_twin.persistence import TwinPersistenceService
from app.application.student_digital_twin.prediction_service import PredictionService
from app.application.student_digital_twin.recommendation_service import (
    RecommendationService,
)
from app.application.student_digital_twin.student_digital_twin_service import (
    StudentDigitalTwinService,
)
from app.application.student_digital_twin.student_reasoning_service import (
    StudentReasoningService,
)

__all__ = [
    "KnowledgeGapService",
    "LearningStateService",
    "MasteryService",
    "ObservationService",
    "PredictionService",
    "RecommendationService",
    "StudentDigitalTwinService",
    "StudentReasoningService",
    "TwinPersistenceService",
]
