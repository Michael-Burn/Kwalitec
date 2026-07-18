"""Immutable plan describing instructional activity flow structure.

Produces activity plans and session skeletons — never questions or prose.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.instructional_blueprint.blueprint_type import BlueprintType
from app.domain.instructional_blueprint.effort_band import EffortBand


@dataclass(frozen=True)
class ActivityPlanSlot:
    """One planned activity slot (structural; not study content).

    Attributes:
        activity_kind: Structural activity kind token.
        sequence_index: 0-based order.
        role: Optional pedagogical role tag.
        effort_weight: Relative effort contribution.
        objective_id: Optional objective identity this slot addresses.
        metadata: Immutable structural tags.
    """

    activity_kind: str
    sequence_index: int
    role: str | None = None
    effort_weight: int = 1
    objective_id: str | None = None
    metadata: tuple[str, ...] = ()


@dataclass(frozen=True)
class SessionSkeleton:
    """Session-shaped instructional skeleton without educational content.

    Attributes:
        slot_count: Number of activity slots.
        phase_labels: Ordered structural phase labels.
        estimated_effort_units: Relative effort units for the session skeleton.
        metadata: Immutable structural tags.
    """

    slot_count: int
    phase_labels: tuple[str, ...]
    estimated_effort_units: int
    metadata: tuple[str, ...] = ()


@dataclass(frozen=True)
class LearningSequenceEntry:
    """One entry in a compiled learning sequence (structure only)."""

    sequence_index: int
    activity_kind: str
    role: str | None = None
    step_id: str | None = None


@dataclass(frozen=True)
class BlueprintPlan:
    """Deterministic instructional plan produced by the Blueprint Engine.

    Attributes:
        blueprint_id: Source blueprint identity.
        blueprint_type: Source blueprint type.
        activity_slots: Ordered planned activity slots.
        session_skeleton: Session-shaped skeleton derived from slots.
        learning_sequence: Ordered learning sequence entries.
        estimated_effort_band: Relative effort band.
        estimated_effort_units: Relative effort units.
        rationale_tags: Explainable planning rationale tags.
        objective_ids: Optional objective identities addressed structurally.
    """

    blueprint_id: str
    blueprint_type: BlueprintType
    activity_slots: tuple[ActivityPlanSlot, ...]
    session_skeleton: SessionSkeleton
    learning_sequence: tuple[LearningSequenceEntry, ...]
    estimated_effort_band: EffortBand
    estimated_effort_units: int
    rationale_tags: tuple[str, ...]
    objective_ids: tuple[str, ...] = ()
