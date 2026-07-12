"""Domain MissionTask — Decision-attributable executable unit.

Immutable projection of one authorised Decision action. Not a second Decision,
not Recommendation packaging ownership, not a mastery store, not filler.
Distinct from ``app.models.mission.MissionTask`` (ORM coexistence Stage A).
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.decision.action_types import ActionFamily, ActionIntent
from app.domain.mission.attribution import DecisionAttribution
from app.domain.mission.evidence_hooks import MissionEvidenceHooks
from app.domain.mission.feasibility import FeasibilityAcknowledgement
from app.domain.mission.warrant import MissionWarrantPosture


@dataclass(frozen=True)
class RecommendationLanguageHook:
    """Optional Recommendation packaging language already narrated from Decision.

    Communication only — never selection or sequencing authority.
    """

    packaging_version: str | None = None
    presentation_tags: tuple[str, ...] = ()
    communication_tags: tuple[str, ...] = ()
    suggestion_family: str | None = None
    suggestion_curriculum_entity_id: str | None = None

    @classmethod
    def create(
        cls,
        *,
        packaging_version: str | None = None,
        presentation_tags: list[str] | tuple[str, ...] | None = None,
        communication_tags: list[str] | tuple[str, ...] | None = None,
        suggestion_family: str | None = None,
        suggestion_curriculum_entity_id: str | None = None,
    ) -> RecommendationLanguageHook:
        """Construct optional Recommendation language hook."""
        return cls(
            packaging_version=packaging_version,
            presentation_tags=tuple(presentation_tags or ()),
            communication_tags=tuple(communication_tags or ()),
            suggestion_family=suggestion_family,
            suggestion_curriculum_entity_id=suggestion_curriculum_entity_id,
        )


@dataclass(frozen=True)
class MissionTask:
    """Atomic Decision-attributable executable unit within a Mission.

    Attributes:
        task_id: Stable id within Mission for execution / completion recording.
        sequence_position: Presentation order (Decision-authored batch order).
        family: Action family preserved from Decision selected action.
        curriculum_entity_id: Official syllabus identity when Decision scoped it.
        intent: Named educational tension from Decision.
        attribution: Decision reason codes + lineage + warrant (mandatory).
        warrant_posture: Inherited honesty from Decision warrant.
        feasibility: How capacity / sustainability shaped inclusion / intensity.
        evidence_hooks: Completion / Failure → Behaviour / planning only.
        recommendation_language: Optional 2.9 packaging language hook.
        intensity_demoted: True when sustainability demoted intensity (not family).
    """

    task_id: str
    sequence_position: int
    family: ActionFamily
    curriculum_entity_id: str | None
    intent: ActionIntent
    attribution: DecisionAttribution
    warrant_posture: MissionWarrantPosture
    feasibility: FeasibilityAcknowledgement
    evidence_hooks: MissionEvidenceHooks
    recommendation_language: RecommendationLanguageHook | None = None
    intensity_demoted: bool = False

    @classmethod
    def create(
        cls,
        *,
        task_id: str,
        sequence_position: int,
        family: ActionFamily | str,
        curriculum_entity_id: str | None,
        intent: ActionIntent | str,
        attribution: DecisionAttribution,
        warrant_posture: MissionWarrantPosture | str,
        feasibility: FeasibilityAcknowledgement,
        evidence_hooks: MissionEvidenceHooks,
        recommendation_language: RecommendationLanguageHook | None = None,
        intensity_demoted: bool = False,
    ) -> MissionTask:
        """Construct a MissionTask after validating attribution fidelity.

        Raises:
            ValueError: If task_id empty, attribution empty, or family mismatch.
        """
        normalized_id = task_id.strip() if isinstance(task_id, str) else ""
        if not normalized_id:
            raise ValueError("task_id must be a non-empty string")
        if sequence_position < 0:
            raise ValueError("sequence_position must be non-negative")
        fam = family if isinstance(family, ActionFamily) else ActionFamily(family)
        inten = intent if isinstance(intent, ActionIntent) else ActionIntent(intent)
        warrant = (
            warrant_posture
            if isinstance(warrant_posture, MissionWarrantPosture)
            else MissionWarrantPosture(warrant_posture)
        )
        if not attribution.reason_code_citations:
            raise ValueError(
                "MissionTask.attribution must cite at least one Decision reason code"
            )
        cited = attribution.decision_citation
        if fam != cited.selected_family:
            raise ValueError(
                "MissionTask.family must match Decision selected action family"
            )
        if curriculum_entity_id != cited.selected_curriculum_entity_id:
            raise ValueError(
                "MissionTask.curriculum_entity_id must match Decision selected scope"
            )
        if inten != cited.selected_intent:
            raise ValueError(
                "MissionTask.intent must match Decision selected action intent"
            )
        if warrant != attribution.warrant_posture:
            raise ValueError(
                "MissionTask.warrant_posture must match attribution warrant"
            )
        return cls(
            task_id=normalized_id,
            sequence_position=sequence_position,
            family=fam,
            curriculum_entity_id=curriculum_entity_id,
            intent=inten,
            attribution=attribution,
            warrant_posture=warrant,
            feasibility=feasibility,
            evidence_hooks=evidence_hooks,
            recommendation_language=recommendation_language,
            intensity_demoted=intensity_demoted,
        )
