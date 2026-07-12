"""Pure read-side Recommendation Engine.

Packages a Decision into an attributable Recommendation. Never re-selects,
never ranks, never mutates Twin, never recomputes readiness, never generates
missions, and never re-evaluates Decisions as a hidden selection side path.
"""

from __future__ import annotations

from app.domain.decision.decision import Decision
from app.domain.decision.reason_codes import REASON_CODE_VOCABULARY_VERSION
from app.domain.recommendation.affordances import ResponseAffordances
from app.domain.recommendation.context import RecommendationContext
from app.domain.recommendation.contrast import project_candidate_contrast
from app.domain.recommendation.explanation import ExplanationChainPresentation
from app.domain.recommendation.narration import (
    family_narration_tags,
    suggestion_presentation_tags,
    urgency_duration_tags,
)
from app.domain.recommendation.reasons import RecommendationReason
from app.domain.recommendation.recommendation import (
    PACKAGING_VERSION,
    DecisionReference,
    Recommendation,
)
from app.domain.recommendation.suggestion import ActionableSuggestion
from app.domain.recommendation.warrant import inherit_confidence_posture


class RecommendationEngine:
    """Pure package API for structural Recommendation Engine.

    Observational only: reads Decision (+ optional communication context);
    never calls Update Strategies, never mutates inputs, never re-selects.
    """

    @staticmethod
    def package(
        decision: Decision,
        *,
        communication_context: RecommendationContext | None = None,
    ) -> Recommendation:
        """Package a frozen ``Recommendation`` from Decision authority.

        Args:
            decision: Authoritative next-action Decision (read-only).
            communication_context: Optional Goals / journal / Confidence framing
                for phrasing tags only — never changes selected action.

        Returns:
            Immutable Recommendation projecting the Decision.

        Raises:
            ValueError: If Decision fails projection preconditions.
        """
        _validate_preconditions(decision)
        context = communication_context or RecommendationContext.empty()

        confidence = inherit_confidence_posture(decision.warrant_posture)
        presentation = suggestion_presentation_tags(decision, confidence)
        communication = _adapt_communication(context, decision)

        suggestion = ActionableSuggestion.from_selected(
            decision.selected,
            presentation_tags=presentation + communication,
        )
        reasons = _narrate_reasons(decision)
        explanation_chain = ExplanationChainPresentation.from_decision(decision)
        contrast = project_candidate_contrast(decision)
        urgency = urgency_duration_tags(decision)
        affordances = _build_affordances(decision, context)

        decision_ref = DecisionReference.create(
            engine_version=decision.engine_version,
            scope=decision.scope,
            selected_family=decision.selected.family.value,
            selected_curriculum_entity_id=decision.selected.curriculum_entity_id,
            evaluation_id=decision.evaluation_id,
        )

        return Recommendation.create(
            decision_ref=decision_ref,
            suggestion=suggestion,
            reasons=reasons,
            explanation_chain=explanation_chain,
            lineage=decision.lineage,
            confidence_posture=confidence,
            urgency_duration_tags=urgency,
            candidate_contrast=contrast,
            affordances=affordances,
            packaging_version=PACKAGING_VERSION,
            decision_engine_version=decision.engine_version,
            reason_code_vocabulary_version=REASON_CODE_VOCABULARY_VERSION,
            communication_tags=communication,
        )


# ---------------------------------------------------------------------------
# Pipeline helpers
# ---------------------------------------------------------------------------


def _validate_preconditions(decision: Decision) -> None:
    """Require selected action + ≥1 reason code + warrant posture."""
    if decision.selected is None:  # pragma: no cover - typed non-optional
        raise ValueError("Decision.selected action is required for packaging")
    if not decision.reason_codes:
        raise ValueError("Decision.reason_codes must contain at least one code")
    if decision.warrant_posture is None:  # pragma: no cover
        raise ValueError("Decision.warrant_posture is required for packaging")
    # Ensure selected is present in candidates (Decision contract already
    # enforces this; re-check for packaging honesty).
    _ = decision.selected_candidate


def _narrate_reasons(decision: Decision) -> tuple[RecommendationReason, ...]:
    """Map every Decision reason code into a Recommendation Reason."""
    reasons: list[RecommendationReason] = []
    for ref in decision.reason_codes:
        reason = RecommendationReason.from_decision_ref(ref)
        # Attach family narration tags without inventing new Decision codes.
        extra = family_narration_tags(ref.family)
        if extra:
            merged_notes = list(reason.note_tags)
            for tag in extra:
                if tag not in merged_notes:
                    merged_notes.append(tag)
            reason = RecommendationReason.create(
                reason.reason_id,
                decision_reason_codes=reason.decision_reason_codes,
                decision_reason_family=reason.decision_reason_family,
                chain_layers=reason.chain_layers,
                tension_tags=reason.tension_tags,
                note_tags=merged_notes,
            )
        reasons.append(reason)
    return tuple(reasons)


def _adapt_communication(
    context: RecommendationContext,
    decision: Decision,
) -> tuple[str, ...]:
    """Shape phrasing tags from communication context — never selection."""
    tags: list[str] = []
    for tag in context.goals_language_tags:
        tags.append(f"goals/{tag}")
    if context.goals_language_tags:
        tags.append("capacity_honest_duration")
        if decision.scope.sitting_date is not None:
            tags.append("toward_sitting")
    for ref in context.journal_history_refs:
        tags.append(f"journal/{ref}")
    if context.journal_history_refs:
        tags.append("prior_preference_acknowledged")
        tags.append("dismiss_not_mastery")
    for tag in context.confidence_framing:
        tags.append(f"confidence_framing/{tag}")
    if context.confidence_framing:
        tags.append("confidence_risk_framing_only")
        tags.append("confidence_not_mastery_upgrade")
    for note in context.notes:
        tags.append(f"context/{note}")
    # Context must not invent Mid readiness or ranking.
    tags.append("context_adapts_phrasing_only")
    tags.append("selection_authority_unchanged")
    seen: set[str] = set()
    unique: list[str] = []
    for tag in tags:
        if tag not in seen:
            seen.add(tag)
            unique.append(tag)
    return tuple(unique)


def _build_affordances(
    decision: Decision,
    context: RecommendationContext,
) -> ResponseAffordances:
    """Attach accept/dismiss/defer with preference-only journal hooks."""
    emphasis: list[str] = ["accept_is_commitment_not_competence"]
    code_ids = {r.code_id.value for r in decision.reason_codes}
    if "prior_dismiss_respected" in code_ids or any(
        "prior_dismiss" in t for t in decision.lineage.value_rationale_tags
    ):
        emphasis.append("prior_dismiss_respected")
    if context.journal_history_refs:
        emphasis.append("journal_aware_phrasing")
    if decision.constraint_acknowledgements:
        emphasis.append("feasibility_demotion_visible")
    return ResponseAffordances.create(emphasis_tags=emphasis)
