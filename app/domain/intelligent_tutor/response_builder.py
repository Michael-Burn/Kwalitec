"""Response builder — constructs structured Tutor response blueprints.

Every recommendation in the blueprint references assembled educational
evidence. Prose generation is deferred to TutorGenerationPort.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.intelligent_tutor.coaching_message import CoachingMessage, CoachingTone
from app.domain.intelligent_tutor.explanation import Explanation, ExplanationKind
from app.domain.intelligent_tutor.learning_hint import LearningHint
from app.domain.intelligent_tutor.response_evidence import (
    AssembledEvidence,
    EvidenceCategory,
)
from app.domain.intelligent_tutor.tutor_context import TutorContext
from app.domain.intelligent_tutor.tutor_question import TutorQuestionKind

_KIND_TO_EXPLANATION: dict[TutorQuestionKind, ExplanationKind] = {
    TutorQuestionKind.DAILY_MISSION: ExplanationKind.MISSION,
    TutorQuestionKind.KNOWLEDGE_GAP: ExplanationKind.GAP,
    TutorQuestionKind.WEAK_CONCEPT: ExplanationKind.WEAK_CONCEPT,
    TutorQuestionKind.PREREQUISITE: ExplanationKind.PREREQUISITE,
    TutorQuestionKind.LEARNING_PATH: ExplanationKind.LEARNING_PATH,
    TutorQuestionKind.RECOVERY_PLAN: ExplanationKind.RECOVERY,
    TutorQuestionKind.STUDY_STRATEGY: ExplanationKind.STRATEGY,
    TutorQuestionKind.CONFIDENCE_TREND: ExplanationKind.CONFIDENCE,
    TutorQuestionKind.MASTERY_CHANGE: ExplanationKind.MASTERY,
    TutorQuestionKind.ASSESSMENT_FEEDBACK: ExplanationKind.ASSESSMENT,
    TutorQuestionKind.GENERAL: ExplanationKind.GENERAL,
}


@dataclass(frozen=True)
class ResponseBlueprint:
    """Deterministic structure for a Tutor response before prose generation."""

    explanation: Explanation
    supporting_evidence_ids: tuple[str, ...]
    suggested_next_action: str
    related_concepts: tuple[str, ...]
    recovery_guidance: str
    reflection_prompt: str
    hints: tuple[LearningHint, ...]
    coaching: tuple[CoachingMessage, ...]
    evidence_summaries: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "supporting_evidence_ids",
            tuple(self.supporting_evidence_ids or ()),
        )
        object.__setattr__(self, "related_concepts", tuple(self.related_concepts or ()))
        object.__setattr__(self, "hints", tuple(self.hints or ()))
        object.__setattr__(self, "coaching", tuple(self.coaching or ()))
        object.__setattr__(
            self, "evidence_summaries", tuple(self.evidence_summaries or ())
        )


def build_response_blueprint(
    *,
    context: TutorContext,
    evidence: AssembledEvidence,
    question_kind: TutorQuestionKind,
    explanation_id: str,
    response_seed: str = "resp",
) -> ResponseBlueprint:
    """Build an evidence-backed response blueprint (no LLM)."""
    exp_kind = _KIND_TO_EXPLANATION.get(question_kind, ExplanationKind.GENERAL)
    evidence_ids = evidence.evidence_ids
    summaries = tuple(item.summary for item in evidence.items[:8])

    summary = _summary_for(question_kind, context)
    detail = _detail_for(question_kind, context, summaries)
    next_action = _next_action(context)
    recovery = _recovery_guidance(context)
    reflection = _reflection_prompt(question_kind, context)
    related = tuple(
        dict.fromkeys(
            list(context.related_concept_ids)
            + list(context.prerequisite_ids)[:3]
            + list(context.concept_ids)[:3]
        )
    )[:6]

    hints = _hints(context, evidence, response_seed)
    coaching = _coaching(context, evidence, response_seed)

    explanation = Explanation(
        explanation_id=explanation_id,
        twin_id=context.twin_id,
        kind=exp_kind,
        summary=summary,
        detail=detail,
        evidence_ids=evidence_ids,
        concept_ids=tuple(
            dict.fromkeys(
                [context.primary_concept_id, *context.concept_ids]
            )
        )
        if context.primary_concept_id or context.concept_ids
        else (),
        reasoning_run_id=context.reasoning_run_id,
        mission_id=context.active_mission_id,
    )

    return ResponseBlueprint(
        explanation=explanation,
        supporting_evidence_ids=evidence_ids,
        suggested_next_action=next_action,
        related_concepts=related,
        recovery_guidance=recovery,
        reflection_prompt=reflection,
        hints=hints,
        coaching=coaching,
        evidence_summaries=summaries,
    )


def _summary_for(kind: TutorQuestionKind, context: TutorContext) -> str:
    concept = context.primary_concept_id or "your current focus"
    if kind == TutorQuestionKind.DAILY_MISSION and context.active_mission_goal:
        return f"Today's mission focuses on {context.active_mission_goal}."
    if kind == TutorQuestionKind.KNOWLEDGE_GAP and context.knowledge_gap_summaries:
        return f"Your Twin shows a knowledge gap around {concept}."
    if kind == TutorQuestionKind.RECOVERY_PLAN and context.recovery_path:
        return f"A recovery path is available for {concept}."
    if kind == TutorQuestionKind.PREREQUISITE and context.prerequisite_ids:
        return f"Prerequisites for {concept} should be strengthened first."
    if kind == TutorQuestionKind.CONFIDENCE_TREND and context.confidence_notes:
        return context.confidence_notes[0]
    if kind == TutorQuestionKind.MASTERY_CHANGE and context.mastery_notes:
        return context.mastery_notes[0]
    if (
        kind == TutorQuestionKind.ASSESSMENT_FEEDBACK
        and context.assessment_feedback_summaries
    ):
        return context.assessment_feedback_summaries[0]
    if context.recommendation_summaries:
        return (
            "Educational reasoning recommends: "
            f"{context.recommendation_summaries[0]}"
        )
    if context.active_mission_goal:
        return f"Today's mission focuses on {context.active_mission_goal}."
    return f"Here is evidence-backed guidance for {concept}."


def _detail_for(
    kind: TutorQuestionKind,
    context: TutorContext,
    summaries: tuple[str, ...],
) -> str:
    parts: list[str] = []
    if context.active_mission_reason:
        parts.append(context.active_mission_reason)
    if kind in {
        TutorQuestionKind.KNOWLEDGE_GAP,
        TutorQuestionKind.WEAK_CONCEPT,
        TutorQuestionKind.RECOVERY_PLAN,
    } and context.knowledge_gap_summaries:
        parts.append("Gaps: " + "; ".join(context.knowledge_gap_summaries[:3]))
    if context.recovery_path:
        parts.append("Recovery path: " + " → ".join(context.recovery_path))
    if summaries:
        parts.append("Evidence: " + " | ".join(summaries[:4]))
    if not parts and context.learning_state_summary:
        parts.append(context.learning_state_summary)
    if not parts:
        return "No additional educational detail is available yet."
    return " ".join(parts)

def _next_action(context: TutorContext) -> str:
    if context.active_mission_goal:
        return (
            f"Continue today's mission: {context.active_mission_goal}"
            + (
                f" (mission {context.active_mission_id})."
                if context.active_mission_id
                else "."
            )
        )
    if context.recommendation_summaries:
        return f"Follow the Twin recommendation: {context.recommendation_summaries[0]}"
    if context.recovery_path:
        return f"Start recovery with {context.recovery_path[0]}."
    if context.prerequisite_ids:
        return f"Review prerequisite {context.prerequisite_ids[0]} before advancing."
    return "Review your latest Twin recommendation and complete today's mission step."


def _recovery_guidance(context: TutorContext) -> str:
    if context.recovery_path:
        return (
            "Repair foundations in order: "
            + " → ".join(context.recovery_path)
            + "."
        )
    if context.prerequisite_ids:
        return (
            "Strengthen prerequisites first: "
            + ", ".join(context.prerequisite_ids[:4])
            + "."
        )
    if context.knowledge_gap_summaries:
        return f"Address the open gap: {context.knowledge_gap_summaries[0]}"
    return "No recovery path is required for the current focus."


def _reflection_prompt(kind: TutorQuestionKind, context: TutorContext) -> str:
    concept = context.primary_concept_id or "this concept"
    if kind == TutorQuestionKind.ASSESSMENT_FEEDBACK:
        return (
            "What evidence from your last attempt changes how you "
            f"approach {concept}?"
        )
    if kind in {TutorQuestionKind.RECOVERY_PLAN, TutorQuestionKind.PREREQUISITE}:
        return f"Which prerequisite for {concept} feels least solid right now?"
    if kind == TutorQuestionKind.CONFIDENCE_TREND:
        return "Where does your confidence feel mismatched with recent performance?"
    return f"After today's work on {concept}, what still feels unclear?"


def _hints(
    context: TutorContext,
    evidence: AssembledEvidence,
    seed: str,
) -> tuple[LearningHint, ...]:
    hints: list[LearningHint] = []
    ev_ids = evidence.evidence_ids[:3]
    if context.curriculum_excerpts:
        hints.append(
            LearningHint(
                hint_id=f"{seed}-hint-1",
                text=f"Re-read: {context.curriculum_excerpts[0][:180]}",
                concept_id=context.primary_concept_id,
                evidence_ids=ev_ids,
                priority=1,
            )
        )
    if context.prerequisite_ids:
        hints.append(
            LearningHint(
                hint_id=f"{seed}-hint-2",
                text=(
                    f"Check prerequisite {context.prerequisite_ids[0]} "
                    "briefly before continuing."
                ),
                concept_id=context.prerequisite_ids[0],
                evidence_ids=ev_ids,
                priority=2,
            )
        )
    graph = evidence.by_category(EvidenceCategory.LEARNING_GRAPH)
    if graph and len(hints) < 3:
        hints.append(
            LearningHint(
                hint_id=f"{seed}-hint-3",
                text=graph[0].summary,
                concept_id=graph[0].concept_id,
                evidence_ids=(graph[0].evidence_id,),
                priority=3,
            )
        )
    return tuple(hints)


def _coaching(
    context: TutorContext,
    evidence: AssembledEvidence,
    seed: str,
) -> tuple[CoachingMessage, ...]:
    messages: list[CoachingMessage] = []
    ev_ids = evidence.evidence_ids[:2]
    if context.active_mission_reason:
        messages.append(
            CoachingMessage(
                message_id=f"{seed}-coach-1",
                text=context.active_mission_reason,
                tone=CoachingTone.GUIDE,
                evidence_ids=ev_ids,
            )
        )
    if context.recommendation_summaries:
        messages.append(
            CoachingMessage(
                message_id=f"{seed}-coach-2",
                text=f"Reasoning decision: {context.recommendation_summaries[0]}",
                tone=CoachingTone.EXPLAIN,
                evidence_ids=ev_ids,
            )
        )
    if context.recovery_path:
        messages.append(
            CoachingMessage(
                message_id=f"{seed}-coach-3",
                text="Follow the Learning Graph recovery path before advancing.",
                tone=CoachingTone.RECOVER,
                evidence_ids=ev_ids,
            )
        )
    if not messages:
        messages.append(
            CoachingMessage(
                message_id=f"{seed}-coach-1",
                text="I will explain the educational decisions already on your Twin.",
                tone=CoachingTone.EXPLAIN,
                evidence_ids=ev_ids,
            )
        )
    return tuple(messages)
