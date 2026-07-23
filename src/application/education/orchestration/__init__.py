"""Educational Orchestration Layer — EDU-003.6.

Application composition over Education OS bounded contexts:

- ``student_state``
- ``educational_evidence``
- ``knowledge_graph``
- ``mastery_estimation``
- ``recommendation_engine``

The orchestrator coordinates. It never estimates mastery, never generates
recommendations, never persists, and never invokes AI. Domain engines remain
the sole educational reasoners; ports supply inputs and publish outputs.
"""

from __future__ import annotations

from application.education.orchestration.dto import (
    EducationalDecision,
    EducationalEvaluation,
    EvaluationSnapshot,
    EvaluationSummary,
    InteractionKind,
    StudentInteractionRequest,
)
from application.education.orchestration.educational_orchestrator import (
    EducationalOrchestrator,
)
from application.education.orchestration.ports import (
    AssessmentPublisher,
    EvidenceProvider,
    KnowledgeGraphProvider,
    RecommendationPublisher,
    StudentStateProvider,
)
from application.education.orchestration.stages import OrchestrationStage

__all__ = [
    "AssessmentPublisher",
    "EducationalDecision",
    "EducationalEvaluation",
    "EducationalOrchestrator",
    "EvaluationSnapshot",
    "EvaluationSummary",
    "EvidenceProvider",
    "InteractionKind",
    "KnowledgeGraphProvider",
    "OrchestrationStage",
    "RecommendationPublisher",
    "StudentInteractionRequest",
    "StudentStateProvider",
]
