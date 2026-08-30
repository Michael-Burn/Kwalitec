"""Policy V0: behavioural wrap of Runtime C daily sitting selection (ADR-027 M0).

No Twin / Estimated Knowledge / Cap 2.8 DecisionEngine branches. Adaptive stage
always declines; successful Policy V0 yields SAFE_FALLBACK; inability yields
BLOCKED with stable block_reason codes from ADR027 §4.2.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from app.application.adaptive_decision.types import (
    BLOCK_CERTIFIED_GUIDANCE_UNAVAILABLE,
    BLOCK_ENROLMENT_INACTIVE,
    BLOCK_NO_MISSION_TEMPLATE,
    BLOCK_SYLLABUS_COMPLETE,
    BLOCK_UNSATISFIED_PREREQUISITES,
    INTENT_DAILY_SITTING,
    POLICY_V0_ID,
    REASON_NO_ADAPTIVE_POLICY_M0,
    REASON_POLICY_V0_CAMPAIGN_ORDER,
    DailySittingRequest,
    DecisionOutcome,
    SittingDecision,
)
from app.application.educational_runtime_engine.exceptions import (
    CertifiedGuidanceUnavailable,
    IllegalRuntimeState,
    SyllabusAlreadyComplete,
)

if TYPE_CHECKING:
    from app.application.educational_runtime_engine.service import (
        EducationalRuntimeEngineService,
    )


def _new_decision_id() -> str:
    return f"dec_{uuid.uuid4().hex[:16]}"


class PolicyV0AdaptiveDecisionEngine:
    """AdaptiveDecisionEngine implementation for M0 Policy V0."""

    def __init__(
        self,
        *,
        runtime: EducationalRuntimeEngineService | None = None,
    ) -> None:
        if runtime is None:
            from app.application.educational_runtime_engine.service import (
                EducationalRuntimeEngineService,
            )

            runtime = EducationalRuntimeEngineService()
        self._runtime = runtime

    def decide_daily_sitting(
        self, request: DailySittingRequest
    ) -> SittingDecision:
        """Run adaptive decline then Policy V0 deterministic selection."""
        decision_id = _new_decision_id()
        # Stage 1: adaptive attempt always declines in M0 (never ADAPTIVE).
        adaptive_declined = (
            REASON_NO_ADAPTIVE_POLICY_M0,
            "adaptive_attempted=false",
        )
        try:
            spec = self._runtime.compute_daily_sitting_selection(
                user_id=request.user_id,
                subject_code=request.subject_code,
                mission_date=request.mission_date,
            )
        except SyllabusAlreadyComplete:
            return SittingDecision(
                outcome=DecisionOutcome.BLOCKED,
                intent=INTENT_DAILY_SITTING,
                policy_id=POLICY_V0_ID,
                decision_id=decision_id,
                topic_id=None,
                topic_code=None,
                educational_package_id=None,
                educational_package_mode=None,
                certified_mission_id=None,
                objective_ids=(),
                reason_codes=(*adaptive_declined, BLOCK_SYLLABUS_COMPLETE),
                block_reason=BLOCK_SYLLABUS_COMPLETE,
                selection_trace={"adaptive_attempted": False},
                curriculum_identity=request.curriculum_identity,
            )
        except CertifiedGuidanceUnavailable as exc:
            return SittingDecision(
                outcome=DecisionOutcome.BLOCKED,
                intent=INTENT_DAILY_SITTING,
                policy_id=POLICY_V0_ID,
                decision_id=decision_id,
                topic_id=None,
                topic_code=exc.topic_code or None,
                educational_package_id=None,
                educational_package_mode=None,
                certified_mission_id=None,
                objective_ids=(),
                reason_codes=(
                    *adaptive_declined,
                    BLOCK_CERTIFIED_GUIDANCE_UNAVAILABLE,
                ),
                block_reason=BLOCK_CERTIFIED_GUIDANCE_UNAVAILABLE,
                selection_trace={"adaptive_attempted": False},
                curriculum_identity=request.curriculum_identity,
                withhold_message=str(exc),
            )
        except IllegalRuntimeState as exc:
            block_reason = _map_illegal_runtime_state(str(exc))
            return SittingDecision(
                outcome=DecisionOutcome.BLOCKED,
                intent=INTENT_DAILY_SITTING,
                policy_id=POLICY_V0_ID,
                decision_id=decision_id,
                topic_id=None,
                topic_code=None,
                educational_package_id=None,
                educational_package_mode=None,
                certified_mission_id=None,
                objective_ids=(),
                reason_codes=(*adaptive_declined, block_reason),
                block_reason=block_reason,
                selection_trace={
                    "adaptive_attempted": False,
                    "illegal_detail": str(exc),
                },
                curriculum_identity=request.curriculum_identity,
            )

        return SittingDecision(
            outcome=DecisionOutcome.SAFE_FALLBACK,
            intent=INTENT_DAILY_SITTING,
            policy_id=POLICY_V0_ID,
            decision_id=decision_id,
            topic_id=spec.topic_id,
            topic_code=spec.topic_code,
            educational_package_id=spec.educational_package_id,
            educational_package_mode=spec.educational_package_mode,
            certified_mission_id=spec.certified_mission_id,
            objective_ids=tuple(spec.objective_ids),
            reason_codes=(
                *adaptive_declined,
                REASON_POLICY_V0_CAMPAIGN_ORDER,
            ),
            block_reason=None,
            selection_trace=dict(spec.selection_trace),
            template_id=spec.template_id,
            educational_campaign_day=spec.educational_campaign_day,
            selection_reasons=tuple(spec.selection_reasons),
            curriculum_provenance=spec.curriculum_provenance,
            calibration_notes=tuple(spec.calibration_notes),
            enrolment_id=spec.enrolment_id,
            plan_instance_id=spec.plan_instance_id,
            curriculum_identity=spec.curriculum_identity,
        )


def _map_illegal_runtime_state(message: str) -> str:
    text = (message or "").lower()
    if "enrolment" in text and (
        "inactive" in text
        or "completed" in text
        or " is " in text
    ):
        # Messages like: enrolment {id} is completed / deferred / ...
        if "no mission template" not in text and "prerequisite" not in text:
            return BLOCK_ENROLMENT_INACTIVE
    if "no mission template" in text:
        return BLOCK_NO_MISSION_TEMPLATE
    if "unsatisfied prerequisites" in text or "prerequisite" in text:
        return BLOCK_UNSATISFIED_PREREQUISITES
    if "enrolment" in text:
        return BLOCK_ENROLMENT_INACTIVE
    return BLOCK_ENROLMENT_INACTIVE
