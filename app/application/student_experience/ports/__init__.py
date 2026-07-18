"""Student Experience ports package."""

from __future__ import annotations

from app.application.student_experience.ports.adaptive_decision_port import (
    AdaptiveDecisionPort,
)
from app.application.student_experience.ports.learning_journey_port import (
    LearningJourneyPort,
)
from app.application.student_experience.ports.learning_orchestrator_port import (
    LearningOrchestratorPort,
)
from app.application.student_experience.ports.mission_port import MissionPort
from app.application.student_experience.ports.student_twin_port import (
    StudentTwinPort,
)

PORT_NAMES: tuple[str, ...] = (
    "student_twin",
    "adaptive_decision",
    "mission",
    "learning_journey",
    "learning_orchestrator",
)

__all__ = [
    "PORT_NAMES",
    "AdaptiveDecisionPort",
    "LearningJourneyPort",
    "LearningOrchestratorPort",
    "MissionPort",
    "StudentTwinPort",
]
