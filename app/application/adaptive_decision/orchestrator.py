"""SittingDecisionOrchestrator: thin ADR-027 M0 coordinator.

Calls AdaptiveDecisionEngine, records DECISION_RECORDED, hands an execution
spec to Runtime C materialisation. Not the Epic-2 LearningOrchestrator.
"""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from app.application.adaptive_decision.audit import record_decision_recorded
from app.application.adaptive_decision.policy_v0 import (
    PolicyV0AdaptiveDecisionEngine,
)
from app.application.adaptive_decision.types import (
    BLOCK_CERTIFIED_GUIDANCE_UNAVAILABLE,
    BLOCK_ENROLMENT_INACTIVE,
    BLOCK_NO_MISSION_TEMPLATE,
    BLOCK_SYLLABUS_COMPLETE,
    BLOCK_UNSATISFIED_PREREQUISITES,
    DailySittingRequest,
    DecisionOutcome,
    SittingDecision,
)
from app.application.educational_runtime_engine.dto import SittingExecutionSpec
from app.application.educational_runtime_engine.exceptions import (
    CertifiedGuidanceUnavailable,
    IllegalRuntimeState,
    SyllabusAlreadyComplete,
)

if TYPE_CHECKING:
    from app.application.adaptive_decision.protocol import (
        AdaptiveDecisionEngine,
    )
    from app.application.educational_runtime_engine.dto import (
        MissionInstanceSnapshot,
    )
    from app.application.educational_runtime_engine.service import (
        EducationalRuntimeEngineService,
    )


class SittingDecisionOrchestrator:
    """Ensure today's Runtime C sitting via Decision Engine then materialise."""

    def __init__(
        self,
        *,
        runtime: EducationalRuntimeEngineService | None = None,
        engine: AdaptiveDecisionEngine | None = None,
    ) -> None:
        if runtime is None:
            from app.application.educational_runtime_engine.service import (
                EducationalRuntimeEngineService,
            )

            runtime = EducationalRuntimeEngineService()
        self._runtime = runtime
        self._engine = engine or PolicyV0AdaptiveDecisionEngine(runtime=runtime)

    def ensure_todays_sitting(
        self,
        *,
        user_id: int,
        subject_code: str,
        mission_date: date | None = None,
    ) -> MissionInstanceSnapshot:
        """Ops short-circuit, then decide + audit + materialise."""
        day = mission_date or date.today()
        existing = self._runtime.try_return_existing_daily_mission(
            user_id=user_id,
            subject_code=subject_code,
            mission_date=day,
        )
        if existing is not None:
            return existing

        enrolment = self._runtime._require_enrolment(user_id, subject_code)
        request = DailySittingRequest(
            user_id=user_id,
            subject_code=subject_code,
            mission_date=day,
            curriculum_identity=enrolment.curriculum_identity,
        )
        decision = self._engine.decide_daily_sitting(request)

        if decision.outcome == DecisionOutcome.BLOCKED:
            record_decision_recorded(
                decision=decision,
                user_id=user_id,
                subject_code=subject_code,
                curriculum_identity=enrolment.curriculum_identity,
                flag_enabled=True,
                enrolment_id=decision.enrolment_id or enrolment.enrolment_id,
                plan_instance_id=decision.plan_instance_id,
            )
            from app.extensions import db

            db.session.commit()
            _raise_for_blocked(decision)

        if decision.outcome == DecisionOutcome.ADAPTIVE:
            raise IllegalRuntimeState(
                "ADR-027 M0 forbids ADAPTIVE outcomes from Policy V0"
            )

        spec = _spec_from_decision(
            decision,
            user_id=user_id,
            subject_code=subject_code,
            mission_date=day,
            curriculum_identity=enrolment.curriculum_identity,
            enrolment_id=decision.enrolment_id or enrolment.enrolment_id,
        )
        mission = self._runtime.materialise_daily_mission_from_spec(spec)
        record_decision_recorded(
            decision=decision,
            user_id=user_id,
            subject_code=subject_code,
            curriculum_identity=enrolment.curriculum_identity,
            flag_enabled=True,
            mission_instance_id=mission.mission_instance_id,
            enrolment_id=decision.enrolment_id or enrolment.enrolment_id,
            plan_instance_id=decision.plan_instance_id
            or mission.plan_instance_id,
        )
        from app.extensions import db

        db.session.commit()
        return mission


def _spec_from_decision(
    decision: SittingDecision,
    *,
    user_id: int,
    subject_code: str,
    mission_date: date,
    curriculum_identity: str,
    enrolment_id: str,
) -> SittingExecutionSpec:
    if not decision.topic_id or not decision.template_id:
        raise IllegalRuntimeState(
            "SittingDecision missing topic_id/template_id for materialisation"
        )
    return SittingExecutionSpec(
        user_id=user_id,
        subject_code=subject_code,
        mission_date=mission_date,
        curriculum_identity=curriculum_identity
        or decision.curriculum_identity
        or "",
        enrolment_id=enrolment_id,
        plan_instance_id=decision.plan_instance_id or "",
        topic_id=decision.topic_id,
        topic_code=decision.topic_code or "",
        template_id=decision.template_id,
        objective_ids=tuple(decision.objective_ids),
        educational_package_id=decision.educational_package_id,
        educational_package_mode=decision.educational_package_mode,
        educational_campaign_day=decision.educational_campaign_day,
        certified_mission_id=decision.certified_mission_id,
        selection_reasons=tuple(decision.selection_reasons),
        curriculum_provenance=decision.curriculum_provenance,
        calibration_notes=tuple(decision.calibration_notes),
        selection_trace=dict(decision.selection_trace),
    )


def _raise_for_blocked(decision: SittingDecision) -> None:
    reason = decision.block_reason or ""
    if reason == BLOCK_SYLLABUS_COMPLETE:
        raise SyllabusAlreadyComplete(
            f"syllabus complete ({decision.curriculum_identity or ''})"
        )
    if reason == BLOCK_CERTIFIED_GUIDANCE_UNAVAILABLE:
        raise CertifiedGuidanceUnavailable(
            decision.withhold_message or "Certified guidance unavailable",
            topic_code=decision.topic_code or "",
            subject_code="",
        )
    if reason == BLOCK_NO_MISSION_TEMPLATE:
        raise IllegalRuntimeState(
            f"no mission template for topic {decision.topic_id}"
        )
    if reason == BLOCK_UNSATISFIED_PREREQUISITES:
        detail = (decision.selection_trace or {}).get("illegal_detail") or (
            "unsatisfied prerequisites"
        )
        raise IllegalRuntimeState(str(detail))
    if reason == BLOCK_ENROLMENT_INACTIVE:
        detail = (decision.selection_trace or {}).get("illegal_detail") or (
            "enrolment inactive"
        )
        raise IllegalRuntimeState(str(detail))
    raise IllegalRuntimeState(f"daily sitting blocked: {reason or 'unknown'}")
