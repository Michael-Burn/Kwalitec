"""Recommendation model — live read-side packaging of a Decision.

Immutable, explainable, Decision-bound. Not a Twin write-domain peer.
Not selection authority. Not Mission generation. Not ranking.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.decision.decision import DecisionLineage, DecisionScope
from app.domain.recommendation.affordances import ResponseAffordances
from app.domain.recommendation.contrast import CandidateContrast
from app.domain.recommendation.explanation import ExplanationChainPresentation
from app.domain.recommendation.reasons import RecommendationReason
from app.domain.recommendation.suggestion import ActionableSuggestion
from app.domain.recommendation.warrant import RecommendationConfidencePosture

# Packaging version tag for audit lineage.
PACKAGING_VERSION = "recommendation-engine/2.9.4-structural"


@dataclass(frozen=True)
class DecisionReference:
    """Citation of the Decision that is selection authority for this packaging.

    Attributes:
        evaluation_id: Optional Decision evaluation identity.
        engine_version: Decision engine version tag.
        scope: Student / curriculum / sitting scope from Decision.
        selected_family: Selected action family (authority citation).
        selected_curriculum_entity_id: Selected curriculum scope when present.
    """

    engine_version: str
    scope: DecisionScope
    selected_family: str
    selected_curriculum_entity_id: str | None = None
    evaluation_id: str | None = None

    @classmethod
    def create(
        cls,
        *,
        engine_version: str,
        scope: DecisionScope,
        selected_family: str,
        selected_curriculum_entity_id: str | None = None,
        evaluation_id: str | None = None,
    ) -> DecisionReference:
        """Construct a DecisionReference."""
        return cls(
            engine_version=engine_version,
            scope=scope,
            selected_family=selected_family,
            selected_curriculum_entity_id=selected_curriculum_entity_id,
            evaluation_id=evaluation_id,
        )


@dataclass(frozen=True)
class Recommendation:
    """Product projection of one Decision — attributable student-facing suggestion.

    Produced only by Recommendation Engine packaging. Never writes Twin beliefs.
    Never recomputes readiness. Never re-selects actions. Never generates missions.

    Attributes:
        decision_ref: Selection authority citation (exactly one Decision).
        suggestion: Actionable suggestion projected from Decision selected action.
        reasons: Narration of Decision reason codes (≥1).
        explanation_chain: Mandatory explainability-chain presentation.
        lineage: Citations copied from Decision lineage — never fabricated.
        confidence_posture: Warrant-honest Recommendation Confidence.
        urgency_duration_tags: Decision-derived feasibility presentation.
        candidate_contrast: “Why not Y?” from Decision candidates only.
        affordances: Accept / dismiss / defer (preference / intent only).
        packaging_version: Recommendation packaging audit tag.
        decision_engine_version: Decision engine version from Decision.
        reason_code_vocabulary_version: Decision reason-code vocabulary version.
        communication_tags: Optional context adaptation phrasing tags.
    """

    decision_ref: DecisionReference
    suggestion: ActionableSuggestion
    reasons: tuple[RecommendationReason, ...]
    explanation_chain: ExplanationChainPresentation
    lineage: DecisionLineage
    confidence_posture: RecommendationConfidencePosture
    urgency_duration_tags: tuple[str, ...]
    candidate_contrast: tuple[CandidateContrast, ...]
    affordances: ResponseAffordances
    packaging_version: str
    decision_engine_version: str
    reason_code_vocabulary_version: str
    communication_tags: tuple[str, ...] = ()

    @classmethod
    def create(
        cls,
        *,
        decision_ref: DecisionReference,
        suggestion: ActionableSuggestion,
        reasons: list[RecommendationReason] | tuple[RecommendationReason, ...],
        explanation_chain: ExplanationChainPresentation,
        lineage: DecisionLineage,
        confidence_posture: RecommendationConfidencePosture | str,
        urgency_duration_tags: list[str] | tuple[str, ...] | None = None,
        candidate_contrast: list[CandidateContrast]
        | tuple[CandidateContrast, ...]
        | None = None,
        affordances: ResponseAffordances | None = None,
        packaging_version: str = PACKAGING_VERSION,
        decision_engine_version: str,
        reason_code_vocabulary_version: str,
        communication_tags: list[str] | tuple[str, ...] | None = None,
    ) -> Recommendation:
        """Construct a Recommendation after validating packaging contracts.

        Raises:
            ValueError: If reasons empty or suggestion family mismatches ref.
        """
        reason_tuple = tuple(reasons)
        if not reason_tuple:
            raise ValueError("Recommendation.reasons must contain at least one reason")
        if suggestion.family.value != decision_ref.selected_family:
            raise ValueError(
                "suggestion.family must match decision_ref.selected_family"
            )
        if (
            suggestion.curriculum_entity_id
            != decision_ref.selected_curriculum_entity_id
        ):
            raise ValueError(
                "suggestion.curriculum_entity_id must match decision_ref"
            )
        confidence = (
            confidence_posture
            if isinstance(confidence_posture, RecommendationConfidencePosture)
            else RecommendationConfidencePosture(confidence_posture)
        )
        return cls(
            decision_ref=decision_ref,
            suggestion=suggestion,
            reasons=reason_tuple,
            explanation_chain=explanation_chain,
            lineage=lineage,
            confidence_posture=confidence,
            urgency_duration_tags=tuple(urgency_duration_tags or ()),
            candidate_contrast=tuple(candidate_contrast or ()),
            affordances=affordances or ResponseAffordances.create(),
            packaging_version=packaging_version,
            decision_engine_version=decision_engine_version,
            reason_code_vocabulary_version=reason_code_vocabulary_version,
            communication_tags=tuple(communication_tags or ()),
        )

    @property
    def decision_reason_code_ids(self) -> tuple[str, ...]:
        """Flattened Decision reason-code ids narrated by Recommendation Reasons."""
        ids: list[str] = []
        for reason in self.reasons:
            for code in reason.decision_reason_codes:
                if code.value not in ids:
                    ids.append(code.value)
        return tuple(ids)
