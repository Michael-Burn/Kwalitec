"""TwinUpdater — apply validated EducationalDecisionSet to Twin belief.

Only StudentReasoningService should invoke this pathway. Observations are
never stored on the Twin. Learning Graph / Mission / Tutor are untouched.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.application.reasoning.decisions.validator import DecisionValidator
from app.application.reasoning.decisions.versions import DECISION_VERSION
from app.domain.reasoning.decisions.category import DecisionCategory
from app.domain.reasoning.decisions.decision_set import EducationalDecisionSet
from app.domain.student_digital_twin.confidence import (
    ConfidenceState,
    confidence_band_from_score,
)
from app.domain.student_digital_twin.learning_state import LearningState
from app.domain.student_digital_twin.mastery import (
    MasteryMap,
    MasteryRecord,
    MasteryTrend,
)
from app.domain.student_digital_twin.reasoning import ReasoningRecord, ReasoningStep
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin
from app.domain.student_digital_twin.timeline import TimelineEvent, TimelineEventKind


class TwinUpdater:
    """Deterministically apply educational decisions onto Twin belief."""

    def __init__(self, *, validator: DecisionValidator | None = None) -> None:
        self._validator = validator or DecisionValidator()

    def apply(
        self,
        twin: StudentDigitalTwin,
        decision_set: EducationalDecisionSet,
        *,
        updated_at: datetime | None = None,
    ) -> StudentDigitalTwin:
        """Validate then apply. Rejects explicitly; never silently repairs."""
        validated = self._validator.validate(decision_set, twin=twin)
        when = updated_at or datetime.now(UTC).replace(tzinfo=None)

        mastery = twin.mastery or MasteryMap.empty()
        confidence = twin.confidence
        learning_state = twin.learning_state

        for decision in validated.decisions:
            if decision.category is DecisionCategory.MASTERY_BELIEF_UPDATE:
                mastery = _apply_mastery(mastery, decision, twin_id=twin.twin_id)
            elif decision.category is DecisionCategory.CONFIDENCE_BELIEF_UPDATE:
                confidence = _apply_confidence(decision, when=when)
            elif decision.category is DecisionCategory.UNCERTAINTY_PRESERVED:
                # Explicit no-op on mastery; preserve prior confidence honesty.
                pass
            elif decision.category is DecisionCategory.PROVENANCE_RECORDED:
                pass
            else:
                from app.domain.reasoning.decisions.errors import (
                    UnknownDecisionCategory,
                )

                raise UnknownDecisionCategory(
                    f"unsupported decision category at apply: {decision.category!r}"
                )

        learning_state = _learning_state_from_belief(
            prior=learning_state,
            mastery=mastery,
            confidence=confidence,
            decision_set=validated,
            when=when,
        )

        reasoning = _reasoning_record(
            twin=twin,
            decision_set=validated,
            when=when,
        )
        timeline_events = (
            TimelineEvent(
                event_id=f"tl-eds-{validated.set_id}",
                twin_id=twin.twin_id,
                kind=TimelineEventKind.REASONING,
                occurred_at=when,
                summary=reasoning.summary,
                reference_id=reasoning.reasoning_id,
            ),
            TimelineEvent(
                event_id=f"tl-state-{learning_state.snapshot_id}",
                twin_id=twin.twin_id,
                kind=TimelineEventKind.STATE_SNAPSHOT,
                occurred_at=when,
                summary="Learning state snapshot from educational decisions",
                reference_id=learning_state.snapshot_id,
            ),
        )

        return twin.with_inferences(
            learning_state=learning_state,
            mastery=mastery,
            confidence=confidence,
            # Explicitly preserve recommendations / gaps / predictions.
            knowledge_gaps=twin.knowledge_gaps,
            recommendations=twin.recommendations,
            predictions=twin.predictions,
            reasoning=reasoning,
            timeline_events=timeline_events,
            updated_at=when,
        )


def _apply_mastery(
    mastery: MasteryMap,
    decision,
    *,
    twin_id: str,
) -> MasteryMap:
    payload = dict(decision.payload or {})
    concept_id = decision.reference.concept_reference
    trend_raw = payload.get("trend", MasteryTrend.UNKNOWN.value)
    trend = (
        trend_raw
        if isinstance(trend_raw, MasteryTrend)
        else MasteryTrend(str(trend_raw))
    )
    record = MasteryRecord(
        mastery_id=str(payload.get("mastery_id") or f"mst-{concept_id}"),
        twin_id=twin_id,
        concept_id=concept_id,
        mastery_score=float(payload.get("mastery_score", decision.value)),
        confidence=float(payload.get("confidence", 0.0)),
        trend=trend,
        evidence_count=int(payload.get("evidence_count", 0)),
        supporting_evidence=tuple(payload.get("supporting_evidence") or ()),
        last_updated=decision.created_at,
        reason=decision.reason.detail or decision.reason.summary,
    )
    return mastery.with_record(record)


def _apply_confidence(decision, *, when: datetime) -> ConfidenceState:
    payload = dict(decision.payload or {})
    score = float(payload.get("score", decision.value))
    return ConfidenceState(
        score=score,
        band=confidence_band_from_score(score),
        evidence_count=int(payload.get("evidence_count", 0)),
        reason="deterministic_outcome_ratio_v1",
        updated_at=when,
    )


def _learning_state_from_belief(
    *,
    prior: LearningState,
    mastery: MasteryMap,
    confidence: ConfidenceState | None,
    decision_set: EducationalDecisionSet,
    when: datetime,
) -> LearningState:
    scores = [r.mastery_score for r in mastery.records]
    knowledge = round(sum(scores) / len(scores), 4) if scores else prior.knowledge
    conf_score = confidence.score if confidence is not None else prior.confidence
    # Preserve exam_readiness — D3 must not estimate readiness.
    snapshot_id = (
        f"lss-d3-{decision_set.context.reasoning_request_id}-"
        f"{decision_set.context.evidence_bundle_id}"
    )
    evidence_delta = len(decision_set.observation_ids)
    return LearningState(
        knowledge=knowledge,
        confidence=conf_score,
        retention=prior.retention,
        consistency=prior.consistency,
        momentum=prior.momentum,
        exam_readiness=prior.exam_readiness,
        snapshot_id=snapshot_id,
        computed_at=when,
        evidence_count=prior.evidence_count + evidence_delta,
        reason="ap002d3_decision_belief_update",
    )


def _reasoning_record(
    *,
    twin: StudentDigitalTwin,
    decision_set: EducationalDecisionSet,
    when: datetime,
) -> ReasoningRecord:
    context = decision_set.context
    decision_ids = list(decision_set.decision_ids)
    steps = (
        ReasoningStep(
            code="educational_decision_set",
            detail="Applied validated EducationalDecisionSet to Twin belief",
            inputs={
                "observation_set_id": context.observation_set_id,
                "evidence_bundle_id": context.evidence_bundle_id,
                "prior_twin_version": context.prior_twin_version,
            },
            outputs={
                "decision_ids": decision_ids,
                "decision_set_id": decision_set.set_id,
                "decision_version": DECISION_VERSION,
                "assessment_session_id": context.session_id,
                "correlation_id": context.correlation_id,
                "reasoning_request_id": context.reasoning_request_id,
            },
        ),
        *(
            ReasoningStep(
                code=decision.category.value,
                detail=decision.reason.summary,
                inputs={
                    "observation_ids": list(
                        decision.reference.educational_observation_ids
                    ),
                    "subject_ref": decision.subject_ref,
                },
                outputs={
                    "decision_id": decision.decision_id,
                    "value": decision.value
                    if not hasattr(decision.value, "keys")
                    else dict(decision.value),
                    "decision_version": decision.decision_version,
                    "evidence_bundle_id": decision.reference.evidence_bundle_id,
                },
            )
            for decision in decision_set.decisions
        ),
    )
    return ReasoningRecord(
        reasoning_id=(
            f"rr-{context.reasoning_request_id}-{context.evidence_bundle_id}"
        ),
        twin_id=twin.twin_id,
        triggered_by="assessment_evidence:decision_integration",
        observation_ids=decision_set.observation_ids,
        steps=steps,
        summary=(
            f"AP-002D3 Twin belief update from {len(decision_set)} decisions "
            f"(bundle={context.evidence_bundle_id})"
        ),
        created_at=when,
        reasoning_version=DECISION_VERSION,
    )
