"""Stable action-family catalogue for Decision Engine selection.

Structural identities only — no ranking scores or optimization weights.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ActionFamily(StrEnum):
    """Educational action families (architecture §3 / plan §5).

    Families remain separable: revise ≠ study; rest ≠ “do nothing”.
    """

    STUDY = "study"
    REVISE = "revise"
    ASSESS = "assess"
    DIAGNOSTIC = "diagnostic"
    REST_PROTECT_INTENSITY = "rest_protect_intensity"


# Ordered catalogue — used for deterministic nomination / fallback ordering.
ACTION_FAMILY_CATALOGUE: tuple[ActionFamily, ...] = (
    ActionFamily.DIAGNOSTIC,
    ActionFamily.STUDY,
    ActionFamily.REVISE,
    ActionFamily.ASSESS,
    ActionFamily.REST_PROTECT_INTENSITY,
)


class ActionIntent(StrEnum):
    """Named educational tension a candidate / selection addresses."""

    COVERAGE_GAP = "coverage_gap"
    RETENTION_RISK = "retention_risk"
    ASSESSMENT_WARRANT = "assessment_warrant"
    EVIDENCE_CREATING = "evidence_creating"
    FEASIBILITY_PROTECTION = "feasibility_protection"
    FACTOR_DISAGREEMENT = "factor_disagreement"
    TIME_GOAL_PRESSURE = "time_goal_pressure"
    HISTORY_ANTI_THRASH = "history_anti_thrash"
    CONFIDENCE_RISK_FRAMING = "confidence_risk_framing"


@dataclass(frozen=True)
class SelectedAction:
    """Canonical next learning action chosen by Decision Engine.

    Attributes:
        family: Action family from the stable catalogue.
        curriculum_entity_id: Official syllabus identity when applicable.
        intent: Named tension the selection addresses.
    """

    family: ActionFamily
    curriculum_entity_id: str | None = None
    intent: ActionIntent = ActionIntent.EVIDENCE_CREATING

    @classmethod
    def create(
        cls,
        family: ActionFamily | str,
        *,
        curriculum_entity_id: str | None = None,
        intent: ActionIntent | str = ActionIntent.EVIDENCE_CREATING,
    ) -> SelectedAction:
        """Construct a SelectedAction."""
        fam = family if isinstance(family, ActionFamily) else ActionFamily(family)
        inten = intent if isinstance(intent, ActionIntent) else ActionIntent(intent)
        entity = None
        if curriculum_entity_id is not None:
            normalized = curriculum_entity_id.strip()
            entity = normalized or None
        return cls(family=fam, curriculum_entity_id=entity, intent=inten)
