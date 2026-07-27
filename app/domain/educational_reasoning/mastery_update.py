"""Mastery Update Rule — evidence-weighted mastery from observations."""

from __future__ import annotations

import hashlib

from app.domain.educational_reasoning.decision import DecisionKind, EducationalDecision
from app.domain.educational_reasoning.explanation import Explanation
from app.domain.educational_reasoning.reasoning_context import ReasoningContext
from app.domain.educational_reasoning.reasoning_rule import ReasoningRule, RuleExecution
from app.domain.student_digital_twin.mastery import (
    MasteryMap,
    MasteryRecord,
    MasteryTrend,
)
from app.domain.student_digital_twin.observation import Observation

RULE_CODE = "mastery_update"
LEARNING_RATE = 0.28
PRIOR = 0.35


class MasteryUpdateRule(ReasoningRule):
    """Derive mastery records from observation outcomes (deterministic)."""

    code = RULE_CODE
    name = "Mastery Update Rule"
    description = (
        "Evidence-weighted exponential mastery update from observation outcomes"
    )
    learning_rate = LEARNING_RATE
    prior = PRIOR

    def apply(self, context: ReasoningContext) -> RuleExecution:
        by_concept: dict[str, list[Observation]] = {}
        for obs in context.observations:
            concept = (obs.curriculum_entity_id or "").strip()
            if not concept:
                continue
            by_concept.setdefault(concept, []).append(obs)

        result = context.prior_mastery or MasteryMap.empty()
        decisions: list[EducationalDecision] = []
        obs_ids = list(context.observation_ids)

        for concept_id, concept_obs in sorted(by_concept.items()):
            outcomes: list[bool] = []
            evidence_ids: list[str] = []
            title = ""
            concept_obs_ids: list[str] = []
            for obs in concept_obs:
                outcome = obs.is_positive_outcome
                if outcome is None:
                    continue
                outcomes.append(outcome)
                evidence_ids.append(obs.evidence_reference or obs.observation_id)
                concept_obs_ids.append(obs.observation_id)
                title = title or str(obs.metadata.get("concept_title") or "")

            if not outcomes:
                continue

            score = self.prior
            for positive in outcomes:
                target = 1.0 if positive else 0.0
                score = score + self.learning_rate * (target - score)

            confidence = min(0.95, 0.35 + 0.12 * len(outcomes))
            trend = _trend(outcomes)
            mastery_id = _mastery_id(context.twin_id, concept_id)
            record = MasteryRecord(
                mastery_id=mastery_id,
                twin_id=context.twin_id,
                concept_id=concept_id,
                concept_title=title,
                mastery_score=round(score, 4),
                confidence=round(confidence, 4),
                trend=trend,
                evidence_count=len(outcomes),
                supporting_evidence=tuple(dict.fromkeys(evidence_ids)),
                last_updated=context.computed_at,
                reason=(
                    f"evidence_weighted_update n={len(outcomes)} "
                    f"rate={self.learning_rate} prior={self.prior}"
                ),
            )
            result = result.with_record(record)

            explanation = Explanation(
                summary=(
                    f"Mastery for {title or concept_id} updated to "
                    f"{record.mastery_score:.3f} from {len(outcomes)} outcomes"
                ),
                rule_code=self.code,
                observation_ids=tuple(concept_obs_ids),
                detail=record.reason,
                metadata={
                    "concept_id": concept_id,
                    "mastery_score": record.mastery_score,
                    "trend": record.trend.value,
                },
            )
            decisions.append(
                EducationalDecision(
                    decision_id=f"dec-{mastery_id}",
                    kind=DecisionKind.MASTERY_UPDATE,
                    rule_code=self.code,
                    twin_id=context.twin_id,
                    subject_ref=concept_id,
                    value=record.mastery_score,
                    explanation=explanation,
                    created_at=context.computed_at,
                    observation_ids=tuple(concept_obs_ids),
                    payload={
                        "mastery_id": mastery_id,
                        "confidence": record.confidence,
                        "trend": record.trend.value,
                    },
                )
            )

        scores = [r.mastery_score for r in result.records]
        knowledge = round(sum(scores) / len(scores), 4) if scores else 0.0

        cycle_explanation = Explanation(
            summary=(
                f"Mastery recomputed for {len(result.records)} concepts "
                f"(knowledge={knowledge:.3f})"
            ),
            rule_code=self.code,
            observation_ids=tuple(obs_ids),
            detail=self.description,
            metadata={"concept_count": len(result.records), "knowledge": knowledge},
        )

        return RuleExecution(
            rule_code=self.code,
            rule_name=self.name,
            explanation=cycle_explanation,
            decisions=tuple(decisions),
            mastery=result,
            knowledge=knowledge,
            inputs={"observation_count": len(context.observations)},
            outputs={"concept_count": len(result.records), "knowledge": knowledge},
        )


def _trend(outcomes: list[bool]) -> MasteryTrend:
    if len(outcomes) < 2:
        return MasteryTrend.UNKNOWN
    window = outcomes[-3:]
    positives = sum(1 for o in window if o)
    ratio = positives / len(window)
    if ratio >= 0.67:
        return MasteryTrend.IMPROVING
    if ratio <= 0.33:
        return MasteryTrend.DECLINING
    return MasteryTrend.STABLE


def _mastery_id(twin_id: str, concept_id: str) -> str:
    digest = hashlib.sha256(f"{twin_id}:{concept_id}".encode()).hexdigest()[:16]
    return f"mst-{digest}"
