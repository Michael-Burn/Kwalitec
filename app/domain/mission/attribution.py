"""Decision attribution types for MissionTask explainability.

Every core educational MissionTask cites Decision selected action, reason codes,
lineage, and warrant — never private mission priority scores.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.domain.decision.action_types import ActionFamily, ActionIntent
from app.domain.decision.candidate import CandidateStatus
from app.domain.decision.decision import Decision, DecisionLineage, DecisionScope
from app.domain.decision.reason_codes import ReasonCodeId, ReasonCodeRef
from app.domain.mission.warrant import MissionWarrantPosture, inherit_mission_warrant


class MissionExplanationChainLayer(StrEnum):
    """Explainability-chain layers for MissionTask attribution.

    Completes Curriculum → Evidence → Twin → Readiness (when cited) → Decision
    → MissionTask. Optional Recommendation narration is a sibling packaging
    hook, not a required Mission layer.
    """

    CURRICULUM = "curriculum"
    EVIDENCE = "evidence"
    TWIN = "twin"
    READINESS = "readiness"
    DECISION = "decision"
    MISSION_TASK = "mission_task"


@dataclass(frozen=True)
class DecisionCitation:
    """Citation of the Decision that authorised a MissionTask.

    Attributes:
        engine_version: Decision engine version tag.
        scope: Student / curriculum / sitting scope from Decision.
        selected_family: Selected action family (authority citation).
        selected_curriculum_entity_id: Selected curriculum scope when present.
        selected_intent: Selected action intent from Decision.
        evaluation_id: Optional Decision evaluation identity.
        batch_index: Position within Decision batch (0-based).
    """

    engine_version: str
    scope: DecisionScope
    selected_family: ActionFamily
    selected_intent: ActionIntent
    selected_curriculum_entity_id: str | None = None
    evaluation_id: str | None = None
    batch_index: int = 0

    @classmethod
    def from_decision(
        cls,
        decision: Decision,
        *,
        batch_index: int = 0,
    ) -> DecisionCitation:
        """Build citation from Decision authority."""
        return cls(
            engine_version=decision.engine_version,
            scope=decision.scope,
            selected_family=decision.selected.family,
            selected_intent=decision.selected.intent,
            selected_curriculum_entity_id=decision.selected.curriculum_entity_id,
            evaluation_id=decision.evaluation_id,
            batch_index=batch_index,
        )


@dataclass(frozen=True)
class CandidateContrastHook:
    """“Why this task, not that?” hook from Decision candidates only.

    Never promotes rejected candidates as equal educational authority.
    """

    candidate_id: str
    family: ActionFamily
    status: CandidateStatus
    curriculum_entity_id: str | None = None
    note_tags: tuple[str, ...] = ()

    @classmethod
    def create(
        cls,
        candidate_id: str,
        family: ActionFamily | str,
        status: CandidateStatus | str,
        *,
        curriculum_entity_id: str | None = None,
        note_tags: list[str] | tuple[str, ...] | None = None,
    ) -> CandidateContrastHook:
        """Construct a CandidateContrastHook."""
        fam = family if isinstance(family, ActionFamily) else ActionFamily(family)
        stat = (
            status if isinstance(status, CandidateStatus) else CandidateStatus(status)
        )
        return cls(
            candidate_id=candidate_id,
            family=fam,
            status=stat,
            curriculum_entity_id=curriculum_entity_id,
            note_tags=tuple(note_tags or ()),
        )


@dataclass(frozen=True)
class MissionExplanationChain:
    """Explainability chain support for MissionTask attribution.

    Completes Curriculum → Evidence → Twin → Readiness (when cited) → Decision
    → MissionTask (+ optional Recommendation narration). Citations from Decision
    lineage only — never fabricated.
    """

    curriculum_entity_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    twin_domains: tuple[str, ...] = ()
    readiness_factor_ids: tuple[str, ...] = ()
    reason_code_ids: tuple[str, ...] = ()
    readiness_cited: bool = False
    evidence_honest_absence: bool = False
    layers_present: tuple[MissionExplanationChainLayer, ...] = ()
    value_rationale_tags: tuple[str, ...] = ()

    @classmethod
    def from_decision(cls, decision: Decision) -> MissionExplanationChain:
        """Build chain slots solely from Decision authority + lineage."""
        lineage: DecisionLineage = decision.lineage
        reason_ids = tuple(ref.code_id.value for ref in decision.reason_codes)
        cites_readiness = bool(lineage.readiness_factor_ids) or any(
            ref.inherits_warrant or ref.readiness_factor_ids
            for ref in decision.reason_codes
        )
        layers: list[MissionExplanationChainLayer] = [
            MissionExplanationChainLayer.CURRICULUM,
            MissionExplanationChainLayer.EVIDENCE,
            MissionExplanationChainLayer.TWIN,
        ]
        if cites_readiness:
            layers.append(MissionExplanationChainLayer.READINESS)
        layers.append(MissionExplanationChainLayer.DECISION)
        layers.append(MissionExplanationChainLayer.MISSION_TASK)
        return cls(
            curriculum_entity_ids=lineage.curriculum_entity_ids,
            evidence_ids=lineage.evidence_ids,
            twin_domains=lineage.twin_domains,
            readiness_factor_ids=lineage.readiness_factor_ids,
            reason_code_ids=reason_ids,
            readiness_cited=cites_readiness,
            evidence_honest_absence=not lineage.evidence_ids,
            layers_present=tuple(layers),
            value_rationale_tags=lineage.value_rationale_tags,
        )


@dataclass(frozen=True)
class DecisionAttribution:
    """Full Decision attribution bound onto a core educational MissionTask.

    Attributes:
        decision_citation: Decision that authorised this task.
        reason_code_citations: Decision reason codes (≥1).
        lineage: Twin / evidence / curriculum / readiness hooks from Decision.
        explanation_chain: Chain slots supporting “Why this task?”.
        candidate_contrast: Non-selected candidates for contrast only.
        warrant_posture: Inherited Mission warrant honesty.
        constraint_acknowledgement_tags: Upstream Decision constraint tags.
    """

    decision_citation: DecisionCitation
    reason_code_citations: tuple[ReasonCodeRef, ...]
    lineage: DecisionLineage
    explanation_chain: MissionExplanationChain
    candidate_contrast: tuple[CandidateContrastHook, ...]
    warrant_posture: MissionWarrantPosture
    constraint_acknowledgement_tags: tuple[str, ...] = ()

    @classmethod
    def from_decision(
        cls,
        decision: Decision,
        *,
        batch_index: int = 0,
    ) -> DecisionAttribution:
        """Build attribution from Decision — no invented codes or lineage."""
        if not decision.reason_codes:
            raise ValueError(
                "Decision.reason_codes must contain at least one code for attribution"
            )
        contrast = tuple(
            CandidateContrastHook.create(
                c.candidate_id,
                c.family,
                c.status,
                curriculum_entity_id=c.curriculum_entity_id,
                note_tags=c.note_tags,
            )
            for c in decision.candidates
            if c.status != CandidateStatus.SELECTED
        )
        ack_tags: list[str] = []
        for ack in decision.constraint_acknowledgements:
            ack_tags.append(f"constraint/{ack.constraint_class.value}")
            for note in ack.note_tags:
                ack_tags.append(note)
        return cls(
            decision_citation=DecisionCitation.from_decision(
                decision, batch_index=batch_index
            ),
            reason_code_citations=decision.reason_codes,
            lineage=decision.lineage,
            explanation_chain=MissionExplanationChain.from_decision(decision),
            candidate_contrast=contrast,
            warrant_posture=inherit_mission_warrant(decision.warrant_posture),
            constraint_acknowledgement_tags=tuple(ack_tags),
        )

    @property
    def reason_code_ids(self) -> tuple[ReasonCodeId, ...]:
        """Decision reason-code identities cited on this attribution."""
        return tuple(ref.code_id for ref in self.reason_code_citations)
