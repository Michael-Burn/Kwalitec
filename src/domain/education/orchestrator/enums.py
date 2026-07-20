"""Educational Orchestrator domain enumerations.

Architecture Source
    EDUCATIONAL_ORCHESTRATION_MODEL.md
    ORCHESTRATION_INVARIANTS.md
Concept
    Orchestration Status / Stage Kind / Stage Status / Evidence Collection Point
"""

from __future__ import annotations

from enum import StrEnum


class OrchestrationStatus(StrEnum):
    """Lifecycle status of an EducationalOrchestrator aggregate.

    The orchestrator coordinates approved decisions into executable learning
    episodes. It does not diagnose, select strategies, or reprioritize.
    PLANNED holds a coordinated plan; ACTIVE executes stages; PAUSED suspends
    coordination; COMPLETED terminates the turn correctly.
    """

    PLANNED = "planned"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"


class StageStatus(StrEnum):
    """Progress status of an individual orchestration stage."""

    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"


class OrchestrationStageKind(StrEnum):
    """Kinds of coordination stages within an orchestration turn.

    Stages mark *where coordination is* in the tutoring flow. They are not
    diagnoses, hypotheses, strategy choices, or priority rankings.
    """

    EPISODE_CREATION = "episode_creation"
    EPISODE_DELIVERY = "episode_delivery"
    EVIDENCE_COLLECTION = "evidence_collection"
    REFLECTION = "reflection"
    TWIN_UPDATE = "twin_update"
    NEXT_RECOMMENDATION = "next_recommendation"


class EvidenceCollectionPointKind(StrEnum):
    """Where evidence collection is coordinated within orchestration.

    Marks collection *points* for later observation. Does not interpret
    evidence or invent observations.
    """

    AFTER_EPISODE = "after_episode"
    DURING_DELIVERY = "during_delivery"
    AT_STAGE = "at_stage"
    DEFERRED = "deferred"
