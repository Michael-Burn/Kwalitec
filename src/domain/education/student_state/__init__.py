"""Student Educational State bounded context — pure educational domain model.

EDU-003.1 implementation of the Student Educational State aggregate.

Pure Domain-Driven Design only: an aggregate, value objects, policies, and
specifications. No persistence, Flask, ORM, HTTP APIs, repositories,
serialization, or DTOs.

StudentEducationalState models the student's current educational condition
— subject and competency states, mastery/confidence summaries, overall
educational health, and lightweight references to the active learning
episode, current mission, current checkpoint, and educational timeline. It
does not estimate mastery, run recommendation logic, build knowledge graphs,
model forgetting curves, or invoke AI.
"""

from __future__ import annotations

from domain.education.student_state.aggregates.student_educational_state import (
    StudentEducationalState,
)
from domain.education.student_state.enums import (
    EducationalHealthBand,
    MasteryBand,
    SubjectStatus,
)
from domain.education.student_state.ids import (
    CheckpointId,
    CompetencyId,
    EducationalTimelineId,
    MissionId,
    StudentEducationalStateId,
    SubjectId,
)
from domain.education.student_state.policies.state_validation_policy import (
    StateValidationPolicy,
)
from domain.education.student_state.specifications.snapshot_reflects_state import (
    SnapshotReflectsStateSpecification,
)
from domain.education.student_state.specifications.state_is_consistent import (
    StudentEducationalStateIsConsistentSpecification,
)
from domain.education.student_state.value_objects.competency_state import (
    CompetencyState,
)
from domain.education.student_state.value_objects.confidence_summary import (
    ConfidenceSummary,
)
from domain.education.student_state.value_objects.educational_health import (
    EducationalHealth,
)
from domain.education.student_state.value_objects.educational_state_snapshot import (
    EducationalStateSnapshot,
)
from domain.education.student_state.value_objects.mastery_summary import (
    MasterySummary,
)
from domain.education.student_state.value_objects.state_references import (
    CheckpointReference,
    EducationalTimelineReference,
    MissionReference,
)
from domain.education.student_state.value_objects.subject_state import SubjectState

__all__ = [
    # Aggregate
    "StudentEducationalState",
    # Value objects
    "SubjectState",
    "CompetencyState",
    "MasterySummary",
    "ConfidenceSummary",
    "EducationalHealth",
    "MissionReference",
    "CheckpointReference",
    "EducationalTimelineReference",
    "EducationalStateSnapshot",
    # Identity
    "StudentEducationalStateId",
    "SubjectId",
    "CompetencyId",
    "MissionId",
    "CheckpointId",
    "EducationalTimelineId",
    # Enums
    "SubjectStatus",
    "MasteryBand",
    "EducationalHealthBand",
    # Policies
    "StateValidationPolicy",
    # Specifications
    "StudentEducationalStateIsConsistentSpecification",
    "SnapshotReflectsStateSpecification",
]
