"""Thin command and query handlers."""

from __future__ import annotations

from application.handlers.command_handlers import (
    CompleteLearningEpisodeHandler,
    GenerateTeachingPlanHandler,
    RecordEvidenceHandler,
    StartLearningSessionHandler,
    UpdateDigitalTwinHandler,
)
from application.handlers.query_handlers import (
    GetEvidenceHistoryHandler,
    GetLearnerStateHandler,
    GetLearningTrajectoryHandler,
    GetTeachingPlanHandler,
)

__all__ = [
    "CompleteLearningEpisodeHandler",
    "GenerateTeachingPlanHandler",
    "GetEvidenceHistoryHandler",
    "GetLearnerStateHandler",
    "GetLearningTrajectoryHandler",
    "GetTeachingPlanHandler",
    "RecordEvidenceHandler",
    "StartLearningSessionHandler",
    "UpdateDigitalTwinHandler",
]
