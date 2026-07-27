"""Knowledge Gap Detection and Prerequisite Analysis rules.

Consume curriculum evidence from ReasoningContext — never retrieve directly.
"""

from __future__ import annotations

import hashlib

from app.domain.educational_reasoning.decision import DecisionKind, EducationalDecision
from app.domain.educational_reasoning.explanation import Explanation
from app.domain.educational_reasoning.reasoning_context import ReasoningContext
from app.domain.educational_reasoning.reasoning_rule import ReasoningRule, RuleExecution
from app.domain.student_digital_twin.knowledge_gap import GapSeverity, KnowledgeGap
from app.domain.student_digital_twin.mastery import MasteryRecord

GAP_MASTERY_THRESHOLD = 0.55
GAP_RULE_CODE = "knowledge_gap_detection"
PREREQ_RULE_CODE = "prerequisite_analysis"


class KnowledgeGapDetectionRule(ReasoningRule):
    """Identify knowledge gaps for weak concepts with retrieval-backed evidence."""

    code = GAP_RULE_CODE
    name = "Knowledge Gap Detection Rule"
    description = (
        "Flag concepts below mastery threshold when curriculum evidence exists"
    )
    threshold = GAP_MASTERY_THRESHOLD

    def apply(self, context: ReasoningContext) -> RuleExecution:
        mastery = context.effective_mastery
        if not (context.workspace_id or "").strip():
            explanation = Explanation(
                summary="No knowledge gaps: workspace_id missing",
                rule_code=self.code,
                observation_ids=context.observation_ids,
                detail="Gaps require a workspace for curriculum evidence",
            )
            return RuleExecution(
                rule_code=self.code,
                rule_name=self.name,
                explanation=explanation,
                gaps=(),
                outputs={"gap_count": 0},
            )

        candidates = [
            r
            for r in mastery.records
            if r.mastery_score < self.threshold and r.evidence_count > 0
        ]
        gaps: list[KnowledgeGap] = []
        decisions: list[EducationalDecision] = []
        evidence_ids_used: list[str] = []

        for record in sorted(candidates, key=lambda r: r.mastery_score):
            gap, evidence_ids = _candidate_gap(
                twin_id=context.twin_id,
                record=record,
                context=context,
                identified_at=context.computed_at,
            )
            if gap is None:
                continue
            gaps.append(gap)
            evidence_ids_used.extend(evidence_ids)
            explanation = Explanation(
                summary=(
                    f"Knowledge gap detected for "
                    f"{gap.concept_title or gap.concept_id} "
                    f"(severity={gap.severity.value})"
                ),
                rule_code=self.code,
                observation_ids=context.observation_ids,
                curriculum_evidence_ids=tuple(evidence_ids),
                detail=gap.reason,
                metadata={
                    "concept_id": gap.concept_id,
                    "severity": gap.severity.value,
                    "mastery_score": record.mastery_score,
                },
            )
            decisions.append(
                EducationalDecision(
                    decision_id=f"dec-{gap.gap_id}",
                    kind=DecisionKind.KNOWLEDGE_GAP,
                    rule_code=self.code,
                    twin_id=context.twin_id,
                    subject_ref=gap.concept_id,
                    value=record.mastery_score,
                    explanation=explanation,
                    created_at=context.computed_at,
                    observation_ids=context.observation_ids,
                    curriculum_evidence_ids=tuple(evidence_ids),
                    payload={
                        "gap_id": gap.gap_id,
                        "severity": gap.severity.value,
                    },
                )
            )

        cycle_explanation = Explanation(
            summary=f"Identified {len(gaps)} evidence-backed knowledge gaps",
            rule_code=self.code,
            observation_ids=context.observation_ids,
            curriculum_evidence_ids=tuple(dict.fromkeys(evidence_ids_used)),
            detail=self.description,
            metadata={"gap_count": len(gaps), "threshold": self.threshold},
        )
        return RuleExecution(
            rule_code=self.code,
            rule_name=self.name,
            explanation=cycle_explanation,
            decisions=tuple(decisions),
            gaps=tuple(gaps),
            inputs={
                "workspace_id": context.workspace_id,
                "candidate_count": len(candidates),
            },
            outputs={"gap_count": len(gaps)},
        )


class PrerequisiteAnalysisRule(ReasoningRule):
    """Enrich gaps with prerequisites via Learning Graph (preferred) or evidence.

    When a Learning Graph is attached to the reasoning context, traverse
    prerequisite edges rather than hardcoding curriculum adjacency. Falls back
    to CurriculumEvidenceBundle when the graph has no edges for the concept.
    """

    code = PREREQ_RULE_CODE
    name = "Prerequisite Analysis Rule"
    description = (
        "Attach likely prerequisite entities from Learning Graph traversal "
        "(or retrieved curriculum evidence when graph edges are absent)"
    )

    def apply(self, context: ReasoningContext) -> RuleExecution:
        prior_gaps = context.gaps
        if not prior_gaps:
            explanation = Explanation(
                summary="No prerequisites analysed (no active gaps)",
                rule_code=self.code,
                observation_ids=context.observation_ids,
            )
            return RuleExecution(
                rule_code=self.code,
                rule_name=self.name,
                explanation=explanation,
                gaps=(),
                outputs={"enriched_count": 0},
            )

        enriched: list[KnowledgeGap] = []
        decisions: list[EducationalDecision] = []
        evidence_ids_used: list[str] = []
        graph_sourced = 0

        for gap in prior_gaps:
            evidence_ids: list[str] = list(gap.supporting_evidence)
            prereq_id, prereq_title, source = _resolve_prerequisite(gap, context)
            if source == "learning_graph":
                graph_sourced += 1

            updated = KnowledgeGap(
                gap_id=gap.gap_id,
                twin_id=gap.twin_id,
                concept_id=gap.concept_id,
                concept_title=gap.concept_title,
                severity=gap.severity,
                confidence=gap.confidence,
                likely_prerequisite_id=prereq_id,
                likely_prerequisite_title=prereq_title,
                supporting_evidence=gap.supporting_evidence,
                retrieval_log_id=gap.retrieval_log_id,
                estimated_recovery_effort=gap.estimated_recovery_effort,
                reason=gap.reason,
                identified_at=gap.identified_at,
            )
            enriched.append(updated)
            evidence_ids_used.extend(evidence_ids)

            explanation = Explanation(
                summary=(
                    f"Prerequisite for {gap.concept_title or gap.concept_id}: "
                    f"{prereq_title or prereq_id or 'none identified'} "
                    f"(via {source})"
                ),
                rule_code=self.code,
                observation_ids=context.observation_ids,
                curriculum_evidence_ids=tuple(evidence_ids),
                detail=self.description,
                metadata={
                    "concept_id": gap.concept_id,
                    "prerequisite_id": prereq_id,
                    "prerequisite_title": prereq_title,
                    "source": source,
                },
            )
            decisions.append(
                EducationalDecision(
                    decision_id=f"dec-prereq-{gap.gap_id}",
                    kind=DecisionKind.PREREQUISITE,
                    rule_code=self.code,
                    twin_id=context.twin_id,
                    subject_ref=gap.concept_id,
                    value=gap.confidence,
                    explanation=explanation,
                    created_at=context.computed_at,
                    observation_ids=context.observation_ids,
                    curriculum_evidence_ids=tuple(evidence_ids),
                    payload={
                        "gap_id": gap.gap_id,
                        "prerequisite_id": prereq_id,
                        "prerequisite_title": prereq_title,
                        "source": source,
                    },
                )
            )

        cycle_explanation = Explanation(
            summary=(
                f"Prerequisite analysis completed for {len(enriched)} gaps "
                f"({graph_sourced} graph-sourced)"
            ),
            rule_code=self.code,
            observation_ids=context.observation_ids,
            curriculum_evidence_ids=tuple(dict.fromkeys(evidence_ids_used)),
            detail=self.description,
            metadata={
                "enriched_count": len(enriched),
                "graph_sourced": graph_sourced,
            },
        )
        return RuleExecution(
            rule_code=self.code,
            rule_name=self.name,
            explanation=cycle_explanation,
            decisions=tuple(decisions),
            gaps=tuple(enriched),
            inputs={
                "gap_count": len(prior_gaps),
                "has_learning_graph": context.learning_graph is not None,
            },
            outputs={
                "enriched_count": len(enriched),
                "graph_sourced": graph_sourced,
            },
        )


def _resolve_prerequisite(
    gap: KnowledgeGap,
    context: ReasoningContext,
) -> tuple[str, str, str]:
    """Return (prerequisite_id, prerequisite_title, source)."""
    prereq_id = gap.likely_prerequisite_id or ""
    prereq_title = gap.likely_prerequisite_title or ""

    graph = context.learning_graph
    if graph is not None:
        direct = graph.direct_prerequisites(gap.concept_id)
        if direct:
            # Prefer the weakest direct prerequisite (lowest mastery projection).
            ranked = sorted(
                direct,
                key=lambda cid: (
                    (
                        graph.get_node(cid).mastery_score
                        if graph.get_node(cid) is not None
                        else 0.0
                    ),
                    cid,
                ),
            )
            chosen = ranked[0]
            node = graph.get_node(chosen)
            return (
                chosen,
                (node.concept_title if node and node.concept_title else prereq_title),
                "learning_graph",
            )
        # Try recovery path: first hop after seed (deepest weak foundation).
        recovery = graph.recovery_path(gap.concept_id)
        if len(recovery.concept_ids) > 1:
            # recovery is foundations → seed; first entry is deepest foundation.
            chosen = recovery.concept_ids[0]
            if chosen != gap.concept_id:
                node = graph.get_node(chosen)
                return (
                    chosen,
                    (
                        node.concept_title
                        if node and node.concept_title
                        else prereq_title
                    ),
                    "learning_graph",
                )

    # Fallback: curriculum evidence (SDT-002 behaviour).
    result = context.curriculum_evidence.for_concept(gap.concept_id)
    if result is not None and result.results:
        top = result.results[0]
        if top.prerequisites and not prereq_id:
            prereq_id = top.prerequisites[0]
        if prereq_id and not prereq_title:
            for ranked in result.results:
                if ranked.entity_id == prereq_id:
                    prereq_title = ranked.title
                    break
        if not prereq_title and result.prerequisite_ids:
            prereq_id = prereq_id or result.prerequisite_ids[0]
    return prereq_id, prereq_title, "curriculum_evidence"


def _candidate_gap(
    *,
    twin_id: str,
    record: MasteryRecord,
    context: ReasoningContext,
    identified_at,
) -> tuple[KnowledgeGap | None, list[str]]:
    result = context.curriculum_evidence.for_concept(record.concept_id)
    if result is None or not result.results:
        return None, []

    top = result.results[0]
    evidence_ids = [e.evidence_id for e in top.evidence if e.evidence_id]
    if not evidence_ids:
        evidence_ids = [f"entity:{top.entity_id}"]
    evidence_ids.append(f"ranked:{top.entity_id}")
    if result.retrieval_log_id:
        evidence_ids.append(f"retrieval:{result.retrieval_log_id}")

    prereq_id = ""
    prereq_title = ""
    if top.prerequisites:
        prereq_id = top.prerequisites[0]
        for ranked in result.results:
            if ranked.entity_id == prereq_id:
                prereq_title = ranked.title
                break

    severity = _severity(record.mastery_score)
    recovery = round((1.0 - record.mastery_score) * 4.0, 2)
    gap_id = _gap_id(twin_id, record.concept_id)

    gap = KnowledgeGap(
        gap_id=gap_id,
        twin_id=twin_id,
        concept_id=record.concept_id,
        concept_title=record.concept_title or top.title,
        severity=severity,
        confidence=round(
            min(0.95, top.confidence * 0.7 + record.confidence * 0.3), 4
        ),
        likely_prerequisite_id=prereq_id,
        likely_prerequisite_title=prereq_title,
        supporting_evidence=tuple(dict.fromkeys(evidence_ids)),
        retrieval_log_id=result.retrieval_log_id,
        estimated_recovery_effort=recovery,
        reason=(
            f"mastery={record.mastery_score:.3f} below {GAP_MASTERY_THRESHOLD}; "
            f"retrieval rank={top.rank_score:.3f}"
        ),
        identified_at=identified_at,
    )
    return gap, evidence_ids


def _severity(mastery_score: float) -> GapSeverity:
    if mastery_score < 0.25:
        return GapSeverity.CRITICAL
    if mastery_score < 0.40:
        return GapSeverity.HIGH
    if mastery_score < 0.50:
        return GapSeverity.MEDIUM
    return GapSeverity.LOW


def _gap_id(twin_id: str, concept_id: str) -> str:
    digest = hashlib.sha256(f"gap:{twin_id}:{concept_id}".encode()).hexdigest()[:16]
    return f"gap-{digest}"
