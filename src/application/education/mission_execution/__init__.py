"""Mission Execution Engine — PRD-001.5.

Application-layer runtime capability that executes MissionPlans and
converts execution events into structured EducationalEvidence.

Manages student interaction with generated mission work.

Does not estimate mastery, generate recommendations, generate missions,
mutate MissionPlan or StudentEducationalState, persist, call
Flask/SQLAlchemy, or invoke AI.
"""

from __future__ import annotations

from application.education.mission_execution.enums import (
    ConfidenceTrend,
    ExecutionEventKind,
    ExecutionStatus,
    StepOutcome,
)
from application.education.mission_execution.errors import (
    MissionExecutionError,
    MissionExecutionInvariantViolation,
)
from application.education.mission_execution.events import (
    ConfidenceRecorded,
    MissionAbandoned,
    MissionCompleted,
    MissionExecutionEvent,
    MissionExpired,
    MissionPaused,
    MissionResumed,
    MissionStarted,
    ReflectionRecorded,
    StepCompleted,
    StepSkipped,
)
from application.education.mission_execution.execution_command_result import (
    ExecutionCommandResult,
)
from application.education.mission_execution.ids import ExecutionId, StudentId
from application.education.mission_execution.mission_execution_engine import (
    MissionExecutionEngine,
)
from application.education.mission_execution.models import (
    ConfidenceRecord,
    ExecutionMetrics,
    ExecutionProgress,
    ExecutionSnapshot,
    ExecutionSummary,
    MissionExecution,
    ReflectionRecord,
)
from application.education.mission_execution.ports import (
    Clock,
    EducationalEvidencePublisher,
    MissionExecutionPublisher,
    MissionExecutionStore,
)
from application.education.mission_execution.rules.evidence_mapping_rules import (
    EvidenceMappingRules,
)
from application.education.mission_execution.rules.lifecycle_rules import (
    LifecycleRules,
)
from application.education.mission_execution.rules.metrics_rules import MetricsRules
from application.education.mission_execution.rules.progress_rules import ProgressRules

__all__ = [
    # Engine
    "MissionExecutionEngine",
    "ExecutionCommandResult",
    # Aggregate / models
    "MissionExecution",
    "ExecutionProgress",
    "ExecutionMetrics",
    "ExecutionSummary",
    "ExecutionSnapshot",
    "ConfidenceRecord",
    "ReflectionRecord",
    # Identity
    "ExecutionId",
    "StudentId",
    # Enums
    "ExecutionStatus",
    "ExecutionEventKind",
    "ConfidenceTrend",
    "StepOutcome",
    # Events
    "MissionExecutionEvent",
    "MissionStarted",
    "MissionPaused",
    "MissionResumed",
    "StepCompleted",
    "StepSkipped",
    "ConfidenceRecorded",
    "ReflectionRecorded",
    "MissionCompleted",
    "MissionAbandoned",
    "MissionExpired",
    # Errors
    "MissionExecutionError",
    "MissionExecutionInvariantViolation",
    # Rules
    "LifecycleRules",
    "ProgressRules",
    "MetricsRules",
    "EvidenceMappingRules",
    # Ports
    "Clock",
    "MissionExecutionPublisher",
    "EducationalEvidencePublisher",
    "MissionExecutionStore",
]
