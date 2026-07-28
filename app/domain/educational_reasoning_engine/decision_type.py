"""Educational decision type catalogue (EI-007).

Decision types name educational actions only — never mission text or UI.
"""

from __future__ import annotations

from enum import StrEnum


class DecisionType(StrEnum):
    """Highest-value educational action categories."""

    STUDY_NEW = "study_new"
    REVISE = "revise"
    STRENGTHEN_CONFIDENCE = "strengthen_confidence"
    SATISFY_PREREQUISITE = "satisfy_prerequisite"
    CONTINUE_PATH = "continue_path"


class ExpectedOutcome(StrEnum):
    """Structured expected educational outcomes (not student-facing copy)."""

    INTRODUCE_NODE = "introduce_node"
    ADVANCE_MASTERY = "advance_mastery"
    RESTORE_RETENTION = "restore_retention"
    RAISE_CONFIDENCE = "raise_confidence"
    UNLOCK_DEPENDENT = "unlock_dependent"
    MAINTAIN_MOMENTUM = "maintain_momentum"
