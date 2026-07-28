"""Learner Lifecycle Orchestration — automate Educational Intelligence (LP-001).

Coordinates existing EI-004…EI-007 and EX-001 services. No educational
reasoning lives here. Runtime Integration remains the Preferred Authority
read path for student surfaces.
"""

from __future__ import annotations

from app.application.learner_lifecycle.checkpoint_store import LifecycleCheckpointStore
from app.application.learner_lifecycle.consistency import LifecycleConsistencyService
from app.application.learner_lifecycle.dto import (
    ConsistencyReport,
    LifecycleResult,
    StageExecutionRecord,
)
from app.application.learner_lifecycle.exceptions import (
    LifecycleError,
    LifecycleInconsistentError,
    LifecycleNotFoundError,
    LifecycleRetryExhaustedError,
    LifecycleStageError,
)
from app.application.learner_lifecycle.orchestrator import LearnerLifecycleOrchestrator
from app.application.learner_lifecycle.retry import LifecycleRetryPolicy
from app.application.learner_lifecycle.stages import (
    LifecycleStage,
    OperationStatus,
    OperationType,
)
from app.application.learner_lifecycle.versions import (
    CERTIFICATION_PROGRAMME,
    CERTIFICATION_STATUS,
    EVIDENCE_RECORD_STAGE_ORDER,
    EVIDENCE_STAGE_ORDER,
    ONBOARDING_STAGE_ORDER,
    ORCHESTRATOR_VERSION,
)

__all__ = [
    "CERTIFICATION_PROGRAMME",
    "CERTIFICATION_STATUS",
    "EVIDENCE_RECORD_STAGE_ORDER",
    "EVIDENCE_STAGE_ORDER",
    "ONBOARDING_STAGE_ORDER",
    "ORCHESTRATOR_VERSION",
    "ConsistencyReport",
    "LifecycleCheckpointStore",
    "LifecycleConsistencyService",
    "LifecycleError",
    "LifecycleInconsistentError",
    "LifecycleNotFoundError",
    "LifecycleResult",
    "LifecycleRetryExhaustedError",
    "LifecycleRetryPolicy",
    "LifecycleStage",
    "LifecycleStageError",
    "LearnerLifecycleOrchestrator",
    "OperationStatus",
    "OperationType",
    "StageExecutionRecord",
]
