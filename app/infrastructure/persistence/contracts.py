"""Persistence contracts for Version 2 aggregates.

Repositories hold no business rules. Unit-of-work owns transaction boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AggregateOwner(str, Enum):
    """Which bounded context owns an aggregate root."""

    CURRICULUM_MANAGEMENT = "curriculum_management"
    CURRICULUM_INGESTION = "curriculum_ingestion"
    STUDENT_TWIN = "student_twin"
    ADAPTIVE_LEARNING = "adaptive_learning"
    MISSION = "mission"
    LEARNING_JOURNEY = "learning_journey"
    LEARNING_SESSION = "learning_session"
    EDUCATION_PLATFORM = "education_platform"
    LEARNING_ORCHESTRATOR = "learning_orchestrator"
    CURRICULUM_STUDIO = "curriculum_studio"


@dataclass(frozen=True)
class AggregateContract:
    """Declarative ownership and persistence posture for one aggregate."""

    name: str
    owner: AggregateOwner
    append_only: bool = False
    optimistic_locking: bool = True
    snapshot_eligible: bool = False
    evidence_eligible: bool = False


AGGREGATE_CONTRACTS: tuple[AggregateContract, ...] = (
    AggregateContract(
        "Subject",
        AggregateOwner.CURRICULUM_MANAGEMENT,
        optimistic_locking=True,
    ),
    AggregateContract(
        "SubjectVersion",
        AggregateOwner.CURRICULUM_MANAGEMENT,
        optimistic_locking=True,
        snapshot_eligible=True,
    ),
    AggregateContract(
        "Publication",
        AggregateOwner.CURRICULUM_MANAGEMENT,
        optimistic_locking=True,
    ),
    AggregateContract(
        "IngestionJob",
        AggregateOwner.CURRICULUM_INGESTION,
        optimistic_locking=True,
        snapshot_eligible=True,
    ),
    AggregateContract(
        "DigitalTwin",
        AggregateOwner.STUDENT_TWIN,
        optimistic_locking=True,
        snapshot_eligible=True,
    ),
    AggregateContract(
        "EvidenceEvent",
        AggregateOwner.STUDENT_TWIN,
        append_only=True,
        optimistic_locking=False,
        evidence_eligible=True,
    ),
    AggregateContract(
        "AdaptiveDecision",
        AggregateOwner.ADAPTIVE_LEARNING,
        append_only=True,
        snapshot_eligible=True,
    ),
    AggregateContract(
        "DailyMission",
        AggregateOwner.MISSION,
        optimistic_locking=True,
    ),
    AggregateContract(
        "LearningJourney",
        AggregateOwner.LEARNING_JOURNEY,
        optimistic_locking=True,
        snapshot_eligible=True,
    ),
    AggregateContract(
        "LearningSession",
        AggregateOwner.LEARNING_SESSION,
        optimistic_locking=True,
    ),
    AggregateContract(
        "IntegrationEvent",
        AggregateOwner.LEARNING_ORCHESTRATOR,
        append_only=True,
        optimistic_locking=False,
    ),
)


def contract_for(name: str) -> AggregateContract | None:
    """Look up an aggregate contract by aggregate name."""
    needle = name.strip()
    for item in AGGREGATE_CONTRACTS:
        if item.name == needle:
            return item
    return None


def owner_for(name: str) -> AggregateOwner | None:
    """Return the owning bounded context for an aggregate name."""
    contract = contract_for(name)
    return None if contract is None else contract.owner
