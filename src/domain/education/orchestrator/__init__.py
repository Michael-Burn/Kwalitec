"""Educational Orchestrator bounded context — pure educational domain model.

IMP-012 implementation of Educational Orchestrator architecture.

Pure Domain-Driven Design only: aggregates, entities, value objects, policies,
specifications, and lightweight domain events. No persistence, Flask, ORM,
HTTP APIs, repositories, serialization, or DTOs.

This domain coordinates approved educational decisions into executable
learning episodes. It does not reason, diagnose, reprioritize, or select
strategies.
"""

from __future__ import annotations

from domain.education.foundation.ids import OrchestratorId
from domain.education.orchestrator.aggregates.educational_orchestrator import (
    EducationalOrchestrator,
)
from domain.education.orchestrator.entities.orchestration_plan import (
    OrchestrationPlan,
    OrchestrationPlanId,
)
from domain.education.orchestrator.entities.orchestration_reference import (
    ApprovedDecisionReference,
    EpisodeReference,
    StrategyReference,
)
from domain.education.orchestrator.entities.orchestration_stage import (
    OrchestrationStage,
    OrchestrationStageId,
)
from domain.education.orchestrator.enums import (
    EvidenceCollectionPointKind,
    OrchestrationStageKind,
    OrchestrationStatus,
    StageStatus,
)
from domain.education.orchestrator.events.orchestration_completed import (
    OrchestrationCompleted,
)
from domain.education.orchestrator.events.orchestration_paused import (
    OrchestrationPaused,
)
from domain.education.orchestrator.events.orchestration_started import (
    OrchestrationStarted,
)
from domain.education.orchestrator.policies.orchestration_policy import (
    OrchestrationPolicy,
)
from domain.education.orchestrator.policies.sequencing_policy import (
    SequencingPolicy,
)
from domain.education.orchestrator.specifications.orchestration_is_valid import (
    OrchestrationIsValidSpecification,
)
from domain.education.orchestrator.specifications.stage_is_executable import (
    StageIsExecutableSpecification,
)
from domain.education.orchestrator.value_objects.orchestration_progress import (
    OrchestrationProgress,
)
from domain.education.orchestrator.value_objects.orchestration_state import (
    OrchestrationState,
)

__all__ = [
    # Aggregate
    "EducationalOrchestrator",
    # Entities
    "OrchestrationPlan",
    "OrchestrationPlanId",
    "OrchestrationStage",
    "OrchestrationStageId",
    "ApprovedDecisionReference",
    "StrategyReference",
    "EpisodeReference",
    # Value objects / identity
    "OrchestrationState",
    "OrchestrationProgress",
    "OrchestratorId",
    # Enums
    "OrchestrationStatus",
    "StageStatus",
    "OrchestrationStageKind",
    "EvidenceCollectionPointKind",
    # Policies
    "OrchestrationPolicy",
    "SequencingPolicy",
    # Specifications
    "OrchestrationIsValidSpecification",
    "StageIsExecutableSpecification",
    # Events
    "OrchestrationStarted",
    "OrchestrationCompleted",
    "OrchestrationPaused",
]
