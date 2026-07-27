"""Recommendation Rule — recommendations from evidence-backed knowledge gaps."""

from __future__ import annotations

import hashlib

from app.domain.educational_reasoning.decision import DecisionKind, EducationalDecision
from app.domain.educational_reasoning.explanation import Explanation
from app.domain.educational_reasoning.reasoning_context import ReasoningContext
from app.domain.educational_reasoning.reasoning_rule import ReasoningRule, RuleExecution
from app.domain.student_digital_twin.knowledge_gap import GapSeverity, KnowledgeGap
from app.domain.student_digital_twin.recommendation import (
    Recommendation,
    RecommendationPriority,
)

RULE_CODE = "recommendation"


class RecommendationRule(ReasoningRule):
    """Explainable recommendations from gaps; prefer graph recovery paths."""

    code = RULE_CODE
    name = "Recommendation Rule"
    description = (
        "Generate study recommendations from evidence-backed knowledge gaps; "
        "recovery targets are graph-driven when a Learning Graph is present"
    )

    def apply(self, context: ReasoningContext) -> RuleExecution:
        recommendations: list[Recommendation] = []
        decisions: list[EducationalDecision] = []
        graph_driven = 0

        for gap in context.gaps:
            target_id, target_title, path_ids, source = _recovery_target(gap, context)
            title = _title(gap, target_id=target_id, target_title=target_title)
            reason = _reason(
                gap,
                target_id=target_id,
                target_title=target_title,
                path_ids=path_ids,
                source=source,
            )
            if source == "learning_graph":
                graph_driven += 1
            priority = _priority(gap.severity)
            rec_id = _rec_id(context.twin_id, gap.gap_id)
            rec = Recommendation(
                recommendation_id=rec_id,
                twin_id=context.twin_id,
                title=title,
                reason=reason,
                priority=priority,
                confidence=gap.confidence,
                curriculum_entity_id=target_id or gap.concept_id,
                supporting_evidence=gap.supporting_evidence,
                related_gap_id=gap.gap_id,
                created_at=context.computed_at,
                status="active",
            )
            recommendations.append(rec)

            explanation = Explanation(
                summary=f"Recommend: {title}",
                rule_code=self.code,
                observation_ids=context.observation_ids,
                curriculum_evidence_ids=gap.supporting_evidence,
                detail=reason,
                metadata={
                    "recommendation_id": rec_id,
                    "gap_id": gap.gap_id,
                    "priority": priority.value,
                    "source": source,
                    "recovery_path": list(path_ids),
                },
            )
            decisions.append(
                EducationalDecision(
                    decision_id=f"dec-{rec_id}",
                    kind=DecisionKind.RECOMMENDATION,
                    rule_code=self.code,
                    twin_id=context.twin_id,
                    subject_ref=gap.concept_id,
                    value=gap.confidence,
                    explanation=explanation,
                    created_at=context.computed_at,
                    observation_ids=context.observation_ids,
                    curriculum_evidence_ids=gap.supporting_evidence,
                    payload={
                        "recommendation_id": rec_id,
                        "title": title,
                        "priority": priority.value,
                        "related_gap_id": gap.gap_id,
                        "source": source,
                        "recovery_path": list(path_ids),
                    },
                )
            )

        cycle_explanation = Explanation(
            summary=(
                f"Generated {len(recommendations)} recommendations from "
                f"{len(context.gaps)} gaps ({graph_driven} graph-driven)"
            ),
            rule_code=self.code,
            observation_ids=context.observation_ids,
            curriculum_evidence_ids=tuple(
                eid
                for g in context.gaps
                for eid in g.supporting_evidence
            ),
            detail=self.description,
            metadata={
                "recommendation_count": len(recommendations),
                "graph_driven": graph_driven,
            },
        )
        return RuleExecution(
            rule_code=self.code,
            rule_name=self.name,
            explanation=cycle_explanation,
            decisions=tuple(decisions),
            recommendations=tuple(recommendations),
            inputs={
                "gap_count": len(context.gaps),
                "has_learning_graph": context.learning_graph is not None,
            },
            outputs={
                "recommendation_count": len(recommendations),
                "graph_driven": graph_driven,
            },
        )


def _recovery_target(
    gap: KnowledgeGap,
    context: ReasoningContext,
) -> tuple[str, str, tuple[str, ...], str]:
    """Return (target_id, target_title, path_ids, source)."""
    graph = context.learning_graph
    if graph is not None:
        path = graph.recovery_path(gap.concept_id)
        # Prefer first foundation on the path (deepest weak prerequisite).
        for hop in path.hops:
            if hop.concept_id == gap.concept_id:
                continue
            title = hop.concept_title or hop.concept_id
            return hop.concept_id, title, path.concept_ids, "learning_graph"

    target_id = gap.likely_prerequisite_id or gap.concept_id
    target_title = gap.likely_prerequisite_title or gap.concept_title or target_id
    return target_id, target_title, (target_id,), "gap_prerequisite"


def _title(
    gap: KnowledgeGap,
    *,
    target_id: str,
    target_title: str,
) -> str:
    if target_title and target_id != gap.concept_id:
        return f"Review {target_title}"
    if gap.likely_prerequisite_title:
        return f"Review {gap.likely_prerequisite_title}"
    if gap.likely_prerequisite_id:
        return f"Review prerequisite {gap.likely_prerequisite_id}"
    label = gap.concept_title or gap.concept_id
    return f"Strengthen {label}"


def _reason(
    gap: KnowledgeGap,
    *,
    target_id: str,
    target_title: str,
    path_ids: tuple[str, ...],
    source: str,
) -> str:
    concept = gap.concept_title or gap.concept_id
    if source == "learning_graph" and len(path_ids) > 1:
        path_label = " → ".join(path_ids)
        return (
            f"Graph recovery path for {concept}: {path_label}. "
            f"Begin with {target_title or target_id}. {gap.reason}"
        )
    if target_title and target_id != gap.concept_id:
        return f"{concept} depends upon {target_title}. {gap.reason}"
    return f"Knowledge gap identified for {concept}. {gap.reason}"


def _priority(severity: GapSeverity) -> RecommendationPriority:
    mapping = {
        GapSeverity.CRITICAL: RecommendationPriority.CRITICAL,
        GapSeverity.HIGH: RecommendationPriority.HIGH,
        GapSeverity.MEDIUM: RecommendationPriority.MEDIUM,
        GapSeverity.LOW: RecommendationPriority.LOW,
    }
    return mapping[severity]


def _rec_id(twin_id: str, gap_id: str) -> str:
    digest = hashlib.sha256(f"rec:{twin_id}:{gap_id}".encode()).hexdigest()[:16]
    return f"rec-{digest}"
