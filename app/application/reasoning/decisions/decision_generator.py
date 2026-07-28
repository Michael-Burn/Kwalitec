"""DecisionGenerator — EducationalObservationSet → EducationalDecisionSet.

Uses only approved MasteryUpdateRule / ConfidenceAdjustmentRule semantics.
Does not generate recommendations, exam readiness, Mission priorities, or
Learning Graph updates. Soft signals alone never author mastery belief.
"""

from __future__ import annotations

import hashlib
from collections import defaultdict
from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any

from app.application.reasoning.builders.decision_builder import DecisionBuilder
from app.application.reasoning.decisions.versions import (
    APPROVED_MASTERY_CONFIDENCE_BASE,
    APPROVED_MASTERY_CONFIDENCE_CAP,
    APPROVED_MASTERY_CONFIDENCE_STEP,
    APPROVED_MASTERY_LEARNING_RATE,
    APPROVED_MASTERY_PRIOR,
    DECISION_VERSION,
)
from app.domain.educational_reasoning.mastery_update import MasteryUpdateRule
from app.domain.reasoning.decisions.category import DecisionCategory
from app.domain.reasoning.decisions.context import DecisionContext
from app.domain.reasoning.decisions.decision_set import EducationalDecisionSet
from app.domain.reasoning.decisions.reason import DecisionReason
from app.domain.reasoning.decisions.result import DecisionResult
from app.domain.reasoning.observations.category import ObservationCategory
from app.domain.reasoning.observations.observation import EducationalObservation
from app.domain.reasoning.observations.observation_set import EducationalObservationSet
from app.domain.student_digital_twin.mastery import MasteryMap, MasteryTrend
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin

# Guard: approved constants must remain identical to MasteryUpdateRule.
assert APPROVED_MASTERY_LEARNING_RATE == MasteryUpdateRule.learning_rate
assert APPROVED_MASTERY_PRIOR == MasteryUpdateRule.prior


class DecisionGenerator:
    """Derive immutable educational decisions from an observation set."""

    def generate(
        self,
        observation_set: EducationalObservationSet,
        *,
        twin: StudentDigitalTwin,
        correlation_id: str,
        session_id: str | None = None,
        decided_at: datetime | None = None,
    ) -> DecisionResult:
        """Produce an EducationalDecisionSet for Twin application."""
        if not isinstance(observation_set, EducationalObservationSet):
            from app.domain.reasoning.decisions.errors import InvalidDecisionSchema

            raise InvalidDecisionSchema("observation_set is required")
        if not (correlation_id or "").strip():
            from app.domain.reasoning.decisions.errors import BrokenDecisionProvenance

            raise BrokenDecisionProvenance("missing correlation_id")

        when = decided_at or datetime.now(UTC).replace(tzinfo=None)
        session = (session_id or "").strip()
        if not session:
            session = _session_from_observations(observation_set)

        context = DecisionContext(
            twin_id=twin.twin_id,
            reasoning_request_id=observation_set.reasoning_request_id,
            evidence_bundle_id=observation_set.evidence_bundle_id,
            session_id=session,
            correlation_id=correlation_id.strip(),
            decision_version=DECISION_VERSION,
            prior_twin_version=twin.version,
            observation_set_id=observation_set.set_id,
        )
        builder = DecisionBuilder(context=context, created_at=when)
        decisions: list = []

        correctness = observation_set.by_category(
            ObservationCategory.OBSERVED_CORRECTNESS.value
        )
        if correctness:
            decisions.extend(
                self._mastery_decisions(
                    builder=builder,
                    observations=correctness,
                    prior_mastery=twin.mastery or MasteryMap.empty(),
                )
            )
            decisions.append(
                self._confidence_decision(
                    builder=builder,
                    observations=correctness,
                    all_observation_ids=observation_set.observation_ids,
                    prior_score=(twin.confidence.score if twin.confidence else 0.0),
                    prior_evidence=(
                        twin.confidence.evidence_count if twin.confidence else 0
                    ),
                )
            )
        else:
            # Soft signals / coverage alone: preserve uncertainty (no mastery).
            soft_ids = observation_set.observation_ids
            lo_ref, concept_ref = _curriculum_refs(observation_set.observations)
            decisions.append(
                builder.build(
                    category=DecisionCategory.UNCERTAINTY_PRESERVED,
                    subject_ref=concept_ref or twin.twin_id,
                    value={
                        "mastery_unchanged": True,
                        "reason": "no_correctness_evidence",
                    },
                    reason=DecisionReason(
                        code="uncertainty_preserved",
                        summary=(
                            "Educational uncertainty preserved: soft signals "
                            "alone do not author mastery belief"
                        ),
                        detail="approved_honesty_no_soft_signal_mastery",
                        observation_ids=soft_ids,
                        rule_code="confidence_adjustment",
                    ),
                    observation_ids=soft_ids,
                    learning_objective_reference=lo_ref or "unspecified",
                    concept_reference=concept_ref,
                    decision_key="uncertainty",
                )
            )

        # Always record provenance decision for the cycle.
        lo_ref, concept_ref = _curriculum_refs(observation_set.observations)
        decisions.append(
            builder.build(
                category=DecisionCategory.PROVENANCE_RECORDED,
                subject_ref=twin.twin_id,
                value={
                    "evidence_bundle_id": observation_set.evidence_bundle_id,
                    "observation_count": len(observation_set),
                },
                reason=DecisionReason(
                    code="provenance_recorded",
                    summary="Evidence provenance recorded for Twin explainability",
                    detail=observation_set.set_id,
                    observation_ids=observation_set.observation_ids,
                    rule_code="student_reasoning",
                ),
                observation_ids=observation_set.observation_ids,
                learning_objective_reference=lo_ref or "unspecified",
                concept_reference=concept_ref,
                decision_key="provenance",
                payload={
                    "interpretation_version": observation_set.interpretation_version,
                },
            )
        )

        decision_set = EducationalDecisionSet(
            set_id=(
                f"eds:{observation_set.evidence_bundle_id}:"
                f"{observation_set.reasoning_request_id}"
            ),
            decisions=tuple(decisions),
            context=context,
            decision_version=DECISION_VERSION,
        )
        return DecisionResult(
            context=context,
            decision_set=decision_set,
            decided_at=when,
        )

    def _mastery_decisions(
        self,
        *,
        builder: DecisionBuilder,
        observations: tuple[EducationalObservation, ...],
        prior_mastery: MasteryMap,
    ) -> list:
        by_concept: dict[str, list[EducationalObservation]] = defaultdict(list)
        for obs in observations:
            concept = (obs.concept_reference or "").strip()
            if not concept:
                from app.domain.reasoning.decisions.errors import (
                    UnknownConceptReference,
                )

                raise UnknownConceptReference(
                    "mastery decision requires concept_reference "
                    f"(observation={obs.observation_id!r})"
                )
            lo = (obs.learning_objective_reference or "").strip()
            if not lo:
                from app.domain.reasoning.decisions.errors import (
                    InvalidLearningObjectiveReference,
                )

                raise InvalidLearningObjectiveReference(
                    "mastery decision requires learning_objective_reference "
                    f"(observation={obs.observation_id!r})"
                )
            by_concept[concept].append(obs)

        decisions = []
        for concept_id, concept_obs in sorted(by_concept.items()):
            outcomes: list[bool] = []
            obs_ids: list[str] = []
            lo_ref = ""
            for obs in concept_obs:
                outcome = _correctness_outcome(obs.value)
                if outcome is None:
                    continue
                outcomes.append(outcome)
                obs_ids.append(obs.observation_id)
                lo_ref = obs.learning_objective_reference

            if not outcomes:
                continue

            prior_record = prior_mastery.get(concept_id)
            score = (
                prior_record.mastery_score
                if prior_record is not None
                else APPROVED_MASTERY_PRIOR
            )
            prior_evidence = prior_record.evidence_count if prior_record else 0
            prior_supporting = (
                list(prior_record.supporting_evidence) if prior_record else []
            )

            for positive in outcomes:
                target = 1.0 if positive else 0.0
                score = score + APPROVED_MASTERY_LEARNING_RATE * (target - score)

            evidence_count = prior_evidence + len(outcomes)
            confidence = min(
                APPROVED_MASTERY_CONFIDENCE_CAP,
                APPROVED_MASTERY_CONFIDENCE_BASE
                + APPROVED_MASTERY_CONFIDENCE_STEP * evidence_count,
            )
            trend = _trend(outcomes, prior_record.trend if prior_record else None)
            mastery_id = _mastery_id(builder.context.twin_id, concept_id)
            supporting = tuple(
                dict.fromkeys(
                    [
                        *prior_supporting,
                        *[o.evidence_reference for o in concept_obs],
                        *obs_ids,
                    ]
                )
            )
            payload: dict[str, Any] = {
                "mastery_id": mastery_id,
                "mastery_score": round(score, 4),
                "confidence": round(confidence, 4),
                "trend": trend.value,
                "evidence_count": evidence_count,
                "supporting_evidence": list(supporting),
                "learning_rate": APPROVED_MASTERY_LEARNING_RATE,
                "prior": APPROVED_MASTERY_PRIOR,
            }
            decisions.append(
                builder.build(
                    category=DecisionCategory.MASTERY_BELIEF_UPDATE,
                    subject_ref=concept_id,
                    value=round(score, 4),
                    reason=DecisionReason(
                        code="mastery_belief_update",
                        summary=(
                            f"Mastery belief for {concept_id} updated to "
                            f"{round(score, 4):.3f} from {len(outcomes)} "
                            "new correctness outcomes"
                        ),
                        detail=(
                            f"evidence_weighted_update n={evidence_count} "
                            f"rate={APPROVED_MASTERY_LEARNING_RATE} "
                            f"prior={APPROVED_MASTERY_PRIOR}"
                        ),
                        observation_ids=tuple(obs_ids),
                        rule_code=MasteryUpdateRule.code,
                    ),
                    observation_ids=tuple(obs_ids),
                    learning_objective_reference=lo_ref,
                    concept_reference=concept_id,
                    payload=payload,
                    decision_key=concept_id,
                )
            )
        return decisions

    def _confidence_decision(
        self,
        *,
        builder: DecisionBuilder,
        observations: tuple[EducationalObservation, ...],
        all_observation_ids: tuple[str, ...],
        prior_score: float,
        prior_evidence: int,
    ):
        outcomes = [
            outcome
            for obs in observations
            if (outcome := _correctness_outcome(obs.value)) is not None
        ]
        cycle_score = (
            sum(1 for o in outcomes if o) / len(outcomes) if outcomes else 0.0
        )
        # Blend prior belief with cycle outcomes without inventing certainty.
        total_n = prior_evidence + len(outcomes)
        if total_n == 0:
            score = 0.0
        elif prior_evidence == 0:
            score = cycle_score
        else:
            score = (
                (prior_score * prior_evidence) + (cycle_score * len(outcomes))
            ) / total_n
        score = round(score, 4)
        lo_ref, concept_ref = _curriculum_refs(observations)
        return builder.build(
            category=DecisionCategory.CONFIDENCE_BELIEF_UPDATE,
            subject_ref=builder.context.twin_id,
            value=score,
            reason=DecisionReason(
                code="confidence_belief_update",
                summary=(
                    f"Confidence belief adjusted to {score:.3f} from "
                    f"{len(outcomes)} known outcomes this cycle"
                ),
                detail="deterministic_outcome_ratio_v1",
                observation_ids=all_observation_ids,
                rule_code="confidence_adjustment",
            ),
            observation_ids=all_observation_ids,
            learning_objective_reference=lo_ref or "unspecified",
            concept_reference=concept_ref,
            payload={
                "score": score,
                "evidence_count": total_n,
                "cycle_outcomes": len(outcomes),
            },
            decision_key="confidence",
        )


def _correctness_outcome(value: Any) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalised = value.strip().lower()
        if normalised in {"correct", "true", "1", "yes"}:
            return True
        if normalised in {"incorrect", "false", "0", "no", "partial"}:
            return False
        return None
    if isinstance(value, Mapping):
        if "correct" in value:
            return bool(value["correct"])
        if "correctness" in value:
            return _correctness_outcome(value["correctness"])
    return None


def _trend(
    outcomes: list[bool], prior: MasteryTrend | None
) -> MasteryTrend:
    if len(outcomes) < 2:
        return prior if prior is not None else MasteryTrend.UNKNOWN
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


def _curriculum_refs(
    observations: tuple[EducationalObservation, ...],
) -> tuple[str, str]:
    lo = ""
    concept = ""
    for obs in observations:
        if not lo and (obs.learning_objective_reference or "").strip():
            lo = obs.learning_objective_reference.strip()
        if not concept and (obs.concept_reference or "").strip():
            concept = obs.concept_reference.strip()
        if lo and concept:
            break
    return lo, concept


def _session_from_observations(observation_set: EducationalObservationSet) -> str:
    for obs in observation_set.observations:
        if (obs.session_id or "").strip():
            return obs.session_id.strip()
    from app.domain.reasoning.decisions.errors import BrokenDecisionProvenance

    raise BrokenDecisionProvenance("missing assessment session id on observations")
