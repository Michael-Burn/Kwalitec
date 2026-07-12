"""Recommendation Reasons — narration of Decision reason codes.

Narration only. Decision Engine alone authors reason codes. Packaging never
invents ranking codes that contradict Decision.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.domain.decision.reason_codes import (
    ReasonCodeFamily,
    ReasonCodeId,
    ReasonCodeRef,
)


class ExplanationChainLayer(StrEnum):
    """Mandatory explainability-chain layers for reason narration."""

    CURRICULUM = "curriculum"
    EVIDENCE = "evidence"
    TWIN = "twin"
    READINESS = "readiness"
    DECISION = "decision"
    RECOMMENDATION = "recommendation"


# Tension-preserving tags keyed by Decision reason-code identity.
_TENSION_TAGS_BY_CODE: dict[ReasonCodeId, tuple[str, ...]] = {
    ReasonCodeId.KNOWS_NOW_MAY_NOT_RETAIN: (
        "knowledge_vs_memory_tension",
        "factor_disagreement",
    ),
    ReasonCodeId.BEHAVIOUR_STRONG_PERFORMANCE_THIN: (
        "behaviour_vs_performance_tension",
        "streaks_not_value",
    ),
    ReasonCodeId.CONFIDENCE_NOT_MASTERY: (
        "confidence_risk_framing_only",
        "confidence_not_mastery",
    ),
    ReasonCodeId.INSUFFICIENT_WARRANT: ("warrant_honesty", "thin_evidence"),
    ReasonCodeId.NOT_YET_KNOWABLE_CONTEXT: (
        "not_yet_knowable",
        "no_mid_coercion",
    ),
    ReasonCodeId.PREFER_EVIDENCE_CREATING: (
        "diagnostic_framing",
        "evidence_creating",
    ),
    ReasonCodeId.PRIOR_DISMISS_RESPECTED: (
        "dismiss_not_mastery",
        "preference_respected",
    ),
}


def _chain_layers_for(ref: ReasonCodeRef) -> tuple[ExplanationChainLayer, ...]:
    layers: list[ExplanationChainLayer] = [ExplanationChainLayer.DECISION]
    if ref.curriculum_entity_ids:
        layers.insert(0, ExplanationChainLayer.CURRICULUM)
    if ref.twin_domains:
        layers.append(ExplanationChainLayer.TWIN)
    if ref.readiness_factor_ids or ref.inherits_warrant:
        layers.append(ExplanationChainLayer.READINESS)
    layers.append(ExplanationChainLayer.RECOMMENDATION)
    # Preserve order uniqueness.
    seen: set[ExplanationChainLayer] = set()
    unique: list[ExplanationChainLayer] = []
    for layer in layers:
        if layer not in seen:
            seen.add(layer)
            unique.append(layer)
    return tuple(unique)


@dataclass(frozen=True)
class RecommendationReason:
    """One narrated Recommendation Reason mapped to Decision reason codes.

    Attributes:
        reason_id: Packaging reason identity (versionable; mirrors Decision code).
        decision_reason_codes: Decision ReasonCodeId identities narrated (≥1).
        decision_reason_family: Educational family from the primary Decision code.
        chain_layers: Explainability layers this reason narrates.
        tension_tags: Preserve Knowledge vs Memory etc. — never collapse.
        note_tags: Structural narration tags from Decision — not marketing.
    """

    reason_id: str
    decision_reason_codes: tuple[ReasonCodeId, ...]
    decision_reason_family: ReasonCodeFamily
    chain_layers: tuple[ExplanationChainLayer, ...]
    tension_tags: tuple[str, ...] = ()
    note_tags: tuple[str, ...] = ()

    @classmethod
    def create(
        cls,
        reason_id: str,
        *,
        decision_reason_codes: list[ReasonCodeId]
        | tuple[ReasonCodeId, ...]
        | list[str]
        | tuple[str, ...],
        decision_reason_family: ReasonCodeFamily | str,
        chain_layers: list[ExplanationChainLayer]
        | tuple[ExplanationChainLayer, ...]
        | list[str]
        | tuple[str, ...]
        | None = None,
        tension_tags: list[str] | tuple[str, ...] | None = None,
        note_tags: list[str] | tuple[str, ...] | None = None,
    ) -> RecommendationReason:
        """Construct a RecommendationReason after validating code mapping."""
        codes = tuple(
            c if isinstance(c, ReasonCodeId) else ReasonCodeId(c)
            for c in decision_reason_codes
        )
        if not codes:
            raise ValueError(
                "RecommendationReason.decision_reason_codes must contain ≥1 code"
            )
        family = (
            decision_reason_family
            if isinstance(decision_reason_family, ReasonCodeFamily)
            else ReasonCodeFamily(decision_reason_family)
        )
        layers_raw = chain_layers or (
            ExplanationChainLayer.DECISION,
            ExplanationChainLayer.RECOMMENDATION,
        )
        layers = tuple(
            layer
            if isinstance(layer, ExplanationChainLayer)
            else ExplanationChainLayer(layer)
            for layer in layers_raw
        )
        rid = reason_id.strip() if isinstance(reason_id, str) else ""
        if not rid:
            raise ValueError("reason_id must be a non-empty string")
        return cls(
            reason_id=rid,
            decision_reason_codes=codes,
            decision_reason_family=family,
            chain_layers=layers,
            tension_tags=tuple(tension_tags or ()),
            note_tags=tuple(note_tags or ()),
        )

    @classmethod
    def from_decision_ref(cls, ref: ReasonCodeRef) -> RecommendationReason:
        """Narrate one Decision ReasonCodeRef into a RecommendationReason."""
        tension = list(_TENSION_TAGS_BY_CODE.get(ref.code_id, ()))
        for tag in ref.note_tags:
            if tag not in tension and tag in {
                "factor_disagreement",
                "streaks_not_value",
                "warrant_honesty",
                "cold_start_posture",
                "no_mid_coercion",
                "dismiss_not_mastery",
                "risk_framing_only",
            }:
                tension.append(tag)
        return cls.create(
            f"rec-reason/{ref.code_id.value}",
            decision_reason_codes=(ref.code_id,),
            decision_reason_family=ref.family,
            chain_layers=_chain_layers_for(ref),
            tension_tags=tension,
            note_tags=ref.note_tags,
        )
