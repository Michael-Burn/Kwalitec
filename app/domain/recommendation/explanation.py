"""Explanation-chain presentation slots for Recommendation packaging.

Completes Curriculum → Evidence → Twin → Readiness (when cited) → Decision
→ Recommendation. Citations come from Decision lineage only — never fabricated.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.decision.candidate import CandidateStatus
from app.domain.decision.decision import Decision, DecisionLineage
from app.domain.decision.reason_codes import ReasonCodeId
from app.domain.recommendation.reasons import ExplanationChainLayer


@dataclass(frozen=True)
class CurriculumLayerPresentation:
    """Curriculum factor presentation from Decision lineage / selected scope."""

    curriculum_entity_ids: tuple[str, ...] = ()
    curriculum_id: str | None = None
    curriculum_format: str | None = None
    cited: bool = False


@dataclass(frozen=True)
class EvidenceLayerPresentation:
    """Evidence presentation — ids from Decision lineage or honest absence."""

    evidence_ids: tuple[str, ...] = ()
    honest_absence: bool = False
    cited: bool = False


@dataclass(frozen=True)
class TwinLayerPresentation:
    """Twin domain factors Decision cited — disagreements preserved."""

    twin_domains: tuple[str, ...] = ()
    value_rationale_tags: tuple[str, ...] = ()
    cited: bool = False


@dataclass(frozen=True)
class ReadinessLayerPresentation:
    """Readiness factor posture + warrant only when Decision cites readiness."""

    readiness_factor_ids: tuple[str, ...] = ()
    overall_posture: str | None = None
    overall_warrant: str | None = None
    decision_warrant_posture: str | None = None
    cited: bool = False


@dataclass(frozen=True)
class DecisionLayerPresentation:
    """Decision authority presentation — selected, candidates, codes, acks."""

    selected_family: str
    selected_curriculum_entity_id: str | None
    reason_code_ids: tuple[str, ...]
    candidate_statuses: tuple[tuple[str, str], ...] = ()
    constraint_acknowledgement_tags: tuple[str, ...] = ()
    engine_version: str | None = None
    evaluation_id: str | None = None


@dataclass(frozen=True)
class ExplanationChainPresentation:
    """Layered Why? presentation completing the mandatory explainability chain.

    Attributes:
        curriculum: Official identity / weight context from Decision lineage.
        evidence: Evidence ids or honest absence under cold start.
        twin: Domain factors Decision cited.
        readiness: Factor posture + warrant only when Decision cites readiness.
        decision: Selected vs candidates + reason codes + acknowledgements.
        layers_present: Ordered layer identities supportable for this packaging.
    """

    curriculum: CurriculumLayerPresentation
    evidence: EvidenceLayerPresentation
    twin: TwinLayerPresentation
    readiness: ReadinessLayerPresentation | None
    decision: DecisionLayerPresentation
    layers_present: tuple[ExplanationChainLayer, ...]

    @classmethod
    def from_decision(cls, decision: Decision) -> ExplanationChainPresentation:
        """Build chain presentation solely from Decision authority + lineage."""
        lineage: DecisionLineage = decision.lineage
        curriculum = CurriculumLayerPresentation(
            curriculum_entity_ids=lineage.curriculum_entity_ids,
            curriculum_id=decision.scope.curriculum_id,
            curriculum_format=decision.curriculum_format.value,
            cited=bool(
                lineage.curriculum_entity_ids or decision.scope.curriculum_id
            ),
        )
        evidence_ids = lineage.evidence_ids
        evidence = EvidenceLayerPresentation(
            evidence_ids=evidence_ids,
            honest_absence=not evidence_ids,
            cited=bool(evidence_ids),
        )
        twin = TwinLayerPresentation(
            twin_domains=lineage.twin_domains,
            value_rationale_tags=lineage.value_rationale_tags,
            cited=bool(lineage.twin_domains),
        )

        cites_readiness = bool(lineage.readiness_factor_ids) or any(
            ref.inherits_warrant or ref.readiness_factor_ids
            for ref in decision.reason_codes
        )
        readiness: ReadinessLayerPresentation | None = None
        if cites_readiness:
            readiness = ReadinessLayerPresentation(
                readiness_factor_ids=lineage.readiness_factor_ids,
                overall_posture=decision.readiness_overall_posture.value,
                overall_warrant=decision.readiness_overall_warrant.value,
                decision_warrant_posture=decision.warrant_posture.value,
                cited=True,
            )

        candidate_statuses = tuple(
            (c.candidate_id, c.status.value) for c in decision.candidates
        )
        ack_tags: list[str] = []
        for ack in decision.constraint_acknowledgements:
            ack_tags.append(ack.constraint_class.value)
            for tag in ack.note_tags:
                if tag not in ack_tags:
                    ack_tags.append(tag)

        decision_layer = DecisionLayerPresentation(
            selected_family=decision.selected.family.value,
            selected_curriculum_entity_id=decision.selected.curriculum_entity_id,
            reason_code_ids=tuple(r.code_id.value for r in decision.reason_codes),
            candidate_statuses=candidate_statuses,
            constraint_acknowledgement_tags=tuple(ack_tags),
            engine_version=decision.engine_version,
            evaluation_id=decision.evaluation_id,
        )

        layers: list[ExplanationChainLayer] = [
            ExplanationChainLayer.CURRICULUM,
            ExplanationChainLayer.EVIDENCE,
            ExplanationChainLayer.TWIN,
        ]
        if readiness is not None and readiness.cited:
            layers.append(ExplanationChainLayer.READINESS)
        layers.append(ExplanationChainLayer.DECISION)
        layers.append(ExplanationChainLayer.RECOMMENDATION)

        return cls(
            curriculum=curriculum,
            evidence=evidence,
            twin=twin,
            readiness=readiness,
            decision=decision_layer,
            layers_present=tuple(layers),
        )

    @property
    def reason_code_ids(self) -> tuple[ReasonCodeId, ...]:
        """Decision reason codes presented on the Decision layer."""
        return tuple(ReasonCodeId(c) for c in self.decision.reason_code_ids)

    def candidate_status_map(self) -> dict[str, CandidateStatus]:
        """Map candidate_id → status from Decision presentation."""
        return {
            cid: CandidateStatus(status)
            for cid, status in self.decision.candidate_statuses
        }
