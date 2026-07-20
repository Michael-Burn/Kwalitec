"""Mission Generation Engine — deterministic Educational OS mission projection.

EDU-001: Generate MissionSpecifications from Digital Twin, Diagnosis,
Priority, Teaching Strategy, and Learning Trajectory.

Pure domain logic only. No AI, no prompting, no randomness, no persistence,
Flask, ORM, HTTP, or DTOs.
"""

from __future__ import annotations

from domain.mission_generation.enums import (
    CompletionConditionCode,
    MissionDurationBand,
    MissionPriorityBand,
)
from domain.mission_generation.ids import (
    MissionObjectiveId,
    MissionSpecificationId,
    MissionTaskId,
)
from domain.mission_generation.mission_duration import MissionDuration
from domain.mission_generation.mission_generator import (
    MissionGenerator,
    base_minutes_for,
    map_priority_band,
)
from domain.mission_generation.mission_objective import MissionObjective
from domain.mission_generation.mission_priority import MissionPriority
from domain.mission_generation.mission_sequence import MissionSequence
from domain.mission_generation.mission_specification import (
    CompletionCondition,
    MissionSpecification,
    SuccessCriterion,
)
from domain.mission_generation.mission_task import MissionTask

__all__ = [
    # Aggregate / specification
    "MissionSpecification",
    "SuccessCriterion",
    "CompletionCondition",
    # Value objects / entities
    "MissionObjective",
    "MissionTask",
    "MissionSequence",
    "MissionDuration",
    "MissionPriority",
    # Identities
    "MissionSpecificationId",
    "MissionTaskId",
    "MissionObjectiveId",
    # Enums
    "MissionDurationBand",
    "MissionPriorityBand",
    "CompletionConditionCode",
    # Generator
    "MissionGenerator",
    "map_priority_band",
    "base_minutes_for",
]
