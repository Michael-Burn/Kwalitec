"""M0 Adaptive Decision Engine types (ADR-027).

Operator/audit outcomes only. Never surface ADAPTIVE as student-facing speech.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum
from typing import Any


class DecisionOutcome(StrEnum):
    """Three-outcome contract for every Decision Engine invocation."""

    ADAPTIVE = "adaptive"
    SAFE_FALLBACK = "safe_fallback"
    BLOCKED = "blocked"


INTENT_DAILY_SITTING = "daily_sitting"
POLICY_V0_ID = "policy_v0"
POLICY_V1_ID = "policy_v1"
SEAM_RUNTIME_C_GENERATE = "runtime_c.generate_daily_mission"

REASON_NO_ADAPTIVE_POLICY_M0 = "no_adaptive_policy_m0"
REASON_POLICY_V0_CAMPAIGN_ORDER = "policy_v0_campaign_order"
REASON_POLICY_V1_BLOCK_WEAKNESS = "policy_v1_block_weakness"
REASON_POLICY_V1_INSUFFICIENT_EVIDENCE = "policy_v1_insufficient_evidence"
REASON_POLICY_V1_NOT_REVIEW_DAY = "policy_v1_not_review_day"

# Twin evidence floor for acting on Estimated Knowledge (ADR-027 Phase 3).
POLICY_V1_MIN_EVIDENCE = 3

BLOCK_SYLLABUS_COMPLETE = "syllabus_complete"
BLOCK_ENROLMENT_INACTIVE = "enrolment_inactive"
BLOCK_CERTIFIED_GUIDANCE_UNAVAILABLE = "certified_guidance_unavailable"
BLOCK_NO_MISSION_TEMPLATE = "no_mission_template"
BLOCK_UNSATISFIED_PREREQUISITES = "unsatisfied_prerequisites"


@dataclass(frozen=True)
class DailySittingRequest:
    """Daily-sitting Decision Engine inputs (M0 + Policy V1 exam proximity)."""

    user_id: int
    subject_code: str
    mission_date: date
    curriculum_identity: str | None = None
    exam_date: date | None = None


@dataclass(frozen=True)
class SittingDecision:
    """Decision Engine result for one daily-sitting evaluation."""

    outcome: DecisionOutcome
    intent: str
    policy_id: str
    decision_id: str
    topic_id: str | None
    topic_code: str | None
    educational_package_id: str | None
    educational_package_mode: str | None
    certified_mission_id: str | None
    objective_ids: tuple[str, ...]
    reason_codes: tuple[str, ...]
    block_reason: str | None
    selection_trace: dict[str, Any] = field(default_factory=dict)
    # Materialisation helpers (not student-facing decision identity)
    template_id: str | None = None
    educational_campaign_day: str | int | None = None
    selection_reasons: tuple[str, ...] = ()
    curriculum_provenance: dict[str, Any] | None = None
    calibration_notes: tuple[str, ...] = ()
    enrolment_id: str | None = None
    plan_instance_id: str | None = None
    curriculum_identity: str | None = None
    withhold_message: str | None = None
