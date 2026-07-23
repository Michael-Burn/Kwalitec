"""Provenance kind catalogue — presentation labels for existing evidence.

Kinds name already-produced Education OS / Application evidence categories.
They do not introduce new educational concepts or decision logic.
"""

from __future__ import annotations

from enum import StrEnum


class ProvenanceKind(StrEnum):
    """Deterministic provenance category for one student-facing reason."""

    WEAK_TOPIC = "weak_topic"
    RECENT_CHECKPOINT = "recent_checkpoint"
    MASTERY_TREND = "mastery_trend"
    PREREQUISITE_DEPENDENCY = "prerequisite_dependency"
    REVISION_SPACING = "revision_spacing"
    UPCOMING_MILESTONE = "upcoming_milestone"
    EVIDENCE_FRESHNESS = "evidence_freshness"
    CURRICULUM_DEPENDENCY = "curriculum_dependency"
    MISSION_PURPOSE = "mission_purpose"
    RECOMMENDATION = "recommendation"
    JOURNEY = "journey"
    READINESS = "readiness"
    COACH = "coach"
    REFLECTION = "reflection"
