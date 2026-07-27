"""PI-001A Founder Curriculum Studio foundation domain.

Lifecycle vocabulary and publication-safety invariants only.
No Flask, no SQLAlchemy, no teaching behaviour.
"""

from app.domain.curriculum_studio_foundation.lifecycle import (
    CANONICAL_FOUNDATION_STAGES,
    STAGE_LABELS,
    FoundationPublicationState,
    FoundationStage,
    has_reached,
    is_student_consumable,
    next_stage,
    resolve_foundation_stage,
    stage_index,
    stage_label,
)

__all__ = [
    "CANONICAL_FOUNDATION_STAGES",
    "STAGE_LABELS",
    "FoundationPublicationState",
    "FoundationStage",
    "has_reached",
    "is_student_consumable",
    "next_stage",
    "resolve_foundation_stage",
    "stage_index",
    "stage_label",
]
