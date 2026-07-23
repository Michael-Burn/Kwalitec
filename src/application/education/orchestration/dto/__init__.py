"""Immutable application DTOs for Educational Orchestration.

These are application objects — projections for workflow results — not
domain aggregates. They carry no educational reasoning.
"""

from __future__ import annotations

from application.education.orchestration.dto.educational_decision import (
    EducationalDecision,
)
from application.education.orchestration.dto.educational_evaluation import (
    EducationalEvaluation,
)
from application.education.orchestration.dto.evaluation_snapshot import (
    EvaluationSnapshot,
)
from application.education.orchestration.dto.evaluation_summary import (
    EvaluationSummary,
)
from application.education.orchestration.dto.interaction_requests import (
    CheckpointRequest,
    InteractionKind,
    QuestionAnswerRequest,
    ReflectionRequest,
    SessionCompletionRequest,
    StudentInteractionRequest,
)

__all__ = [
    "CheckpointRequest",
    "EducationalDecision",
    "EducationalEvaluation",
    "EvaluationSnapshot",
    "EvaluationSummary",
    "InteractionKind",
    "QuestionAnswerRequest",
    "ReflectionRequest",
    "SessionCompletionRequest",
    "StudentInteractionRequest",
]
