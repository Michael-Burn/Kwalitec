"""Educational Digital Twin bounded context — pure educational domain model.

IMP-013 implementation of the Educational Digital Twin architecture.

Pure Domain-Driven Design only: aggregates, entities, value objects, policies,
specifications, and lightweight domain events. No persistence, Flask, ORM,
HTTP APIs, repositories, serialization, or DTOs.

The Digital Twin remembers the evolving educational state of a learner.
It does not reason, diagnose, interpret evidence, create hypotheses, choose
priorities or strategies, approve interventions, or orchestrate sessions.
"""

from __future__ import annotations

from domain.education.digital_twin.aggregates.educational_digital_twin import (
    EducationalDigitalTwin,
)
from domain.education.digital_twin.entities.concept_state import (
    ConceptState,
    ConceptStateId,
)
from domain.education.digital_twin.entities.evidence_history import (
    EvidenceHistoryEntry,
    EvidenceHistoryEntryId,
)
from domain.education.digital_twin.entities.intervention_history import (
    InterventionHistoryEntry,
    InterventionHistoryEntryId,
)
from domain.education.digital_twin.entities.learner_state import (
    LearnerState,
    LearnerStateId,
)
from domain.education.digital_twin.entities.misconception_state import (
    MisconceptionState,
    MisconceptionStateId,
)
from domain.education.digital_twin.enums import (
    LearnerActivityStatus,
    MasteryBand,
    MisconceptionPresence,
    RetentionBand,
    TrajectoryPointKind,
    TwinStatus,
    TwinUpdateKind,
)
from domain.education.digital_twin.events.mastery_changed import MasteryChanged
from domain.education.digital_twin.events.twin_created import TwinCreated
from domain.education.digital_twin.events.twin_updated import TwinUpdated
from domain.education.digital_twin.policies.state_validation_policy import (
    StateValidationPolicy,
)
from domain.education.digital_twin.policies.twin_update_policy import TwinUpdatePolicy
from domain.education.digital_twin.specifications.state_transition_is_valid import (
    StateTransitionIsValidSpecification,
)
from domain.education.digital_twin.specifications.twin_is_consistent import (
    TwinIsConsistentSpecification,
)
from domain.education.digital_twin.value_objects.confidence_profile import (
    ConfidenceProfile,
)
from domain.education.digital_twin.value_objects.learning_trajectory import (
    LearningTrajectory,
    TrajectoryPoint,
)
from domain.education.digital_twin.value_objects.mastery_state import MasteryState
from domain.education.digital_twin.value_objects.retention_state import RetentionState
from domain.education.foundation.ids import DigitalTwinId

__all__ = [
    # Aggregate
    "EducationalDigitalTwin",
    # Entities
    "LearnerState",
    "LearnerStateId",
    "ConceptState",
    "ConceptStateId",
    "MisconceptionState",
    "MisconceptionStateId",
    "EvidenceHistoryEntry",
    "EvidenceHistoryEntryId",
    "InterventionHistoryEntry",
    "InterventionHistoryEntryId",
    # Value objects / identity
    "MasteryState",
    "RetentionState",
    "ConfidenceProfile",
    "LearningTrajectory",
    "TrajectoryPoint",
    "DigitalTwinId",
    # Enums
    "TwinStatus",
    "LearnerActivityStatus",
    "MasteryBand",
    "RetentionBand",
    "MisconceptionPresence",
    "TwinUpdateKind",
    "TrajectoryPointKind",
    # Policies
    "TwinUpdatePolicy",
    "StateValidationPolicy",
    # Specifications
    "TwinIsConsistentSpecification",
    "StateTransitionIsValidSpecification",
    # Events
    "TwinCreated",
    "TwinUpdated",
    "MasteryChanged",
]
