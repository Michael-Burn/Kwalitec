"""Study Recovery Planner Adapter (P2-MS010).

Implements ``RecoveryPlannerPort`` with a structural placeholder candidate.
No recovery algorithms, schedule optimisation, or educational writes.
"""

from __future__ import annotations

import hashlib
import logging
from typing import Any

from .contracts import (
    AUTHORITY_RECOVERY_PLANNER,
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    INVALID_STATE,
    RECOVERY_VERSION,
    STRATEGY_STRUCTURAL_PLACEHOLDER,
    UNAVAILABLE,
    RecoveryContext,
    RecoveryPlanCandidate,
    RecoveryResult,
    serialize_canonical,
)

logger = logging.getLogger(__name__)

PORT_ID = "recovery_planner_port"
ADAPTER_ID = "study_recovery_planner_adapter"
SOURCE_SERVICE = "study_recovery_planner"
PLACEHOLDER_RATIONALE = (
    "Structural recovery candidate placeholder only. No recovery algorithm "
    "or schedule optimisation was applied. Runtime A must ignore this "
    "candidate for educational decisions in P2-MS010."
)


def deterministic_candidate_id(context: RecoveryContext) -> str:
    """Deterministic candidate id from material RecoveryContext fields."""
    material = {
        "available_study_capacity": (
            context.available_study_capacity.to_canonical_dict()
        ),
        "current_plan_version": context.current_plan_version,
        "disruption_summary": context.disruption_summary.to_canonical_dict(),
        "missed_sessions": [
            item.to_canonical_dict() for item in context.missed_sessions
        ],
        "recovery_id": context.recovery_id,
        "reporting_period": context.reporting_period,
        "student_id": context.student_id,
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()[:16]
    return f"rcv-cand-{digest}"


def deterministic_recovery_id(
    *,
    student_id: str,
    reporting_period: str,
    current_plan_version: str,
    generated_at: str | None,
) -> str:
    """Deterministic recovery_id when callers omit one."""
    material = {
        "current_plan_version": (current_plan_version or "").strip(),
        "generated_at": generated_at,
        "reporting_period": (reporting_period or "").strip().lower(),
        "student_id": (student_id or "").strip(),
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()[:16]
    return f"rcv-{digest}"


class StudyRecoveryPlannerAdapter:
    """RecoveryPlannerPort implementation — structural placeholder only.

    Returns advisory_only candidates. Does not optimise schedules, change
    recommendations, or write educational state.
    """

    ADAPTER_VERSION = "1.0.0-p2.ms010"

    def __init__(self, *, enabled: bool = True) -> None:
        self._enabled = bool(enabled)

    @property
    def adapter_id(self) -> str:
        return ADAPTER_ID

    @property
    def port_id(self) -> str:
        return PORT_ID

    def is_available(self) -> bool:
        return self._enabled

    def plan_recovery(self, context: RecoveryContext) -> RecoveryResult:
        """Produce a structural RecoveryPlanCandidate from RecoveryContext."""
        if not self._enabled:
            return RecoveryResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_RECOVERY_PLANNER is OFF",
            )
        if not isinstance(context, RecoveryContext):
            return RecoveryResult(
                ok=False,
                error_code=INVALID_STATE,
                message="context must be a RecoveryContext",
            )
        try:
            candidate = self._build_placeholder(context)
        except Exception as exc:
            logger.warning(
                "recovery_plan_failed student_id=%s error=%s",
                getattr(context, "student_id", ""),
                exc,
                exc_info=True,
            )
            return RecoveryResult(
                ok=False,
                error_code=INVALID_STATE,
                message=str(exc) or "recovery planning failed",
            )
        if not isinstance(candidate, RecoveryPlanCandidate):
            return RecoveryResult(
                ok=False,
                error_code=INVALID_STATE,
                message="placeholder assembly did not return RecoveryPlanCandidate",
            )
        return RecoveryResult(ok=True, value=candidate)

    def _build_placeholder(self, context: RecoveryContext) -> RecoveryPlanCandidate:
        recovery_id = context.recovery_id or deterministic_recovery_id(
            student_id=context.student_id,
            reporting_period=context.reporting_period,
            current_plan_version=context.current_plan_version,
            generated_at=context.generated_at,
        )
        candidate_id = deterministic_candidate_id(context)
        availability = context.availability or AVAILABILITY_AVAILABLE
        if availability == AVAILABILITY_UNAVAILABLE:
            rationale = (
                context.unavailable_reason
                or "Recovery context marked unavailable; placeholder retained."
            )
        else:
            rationale = PLACEHOLDER_RATIONALE

        provenance: dict[str, Any] = {
            "adapter_id": self.adapter_id,
            "adapter_version": self.ADAPTER_VERSION,
            "authority": AUTHORITY_RECOVERY_PLANNER,
            "context_recovery_id": recovery_id,
            "context_version": context.recovery_version or RECOVERY_VERSION,
            "current_plan_version": context.current_plan_version,
            "evidence_provenance": dict(context.evidence_provenance),
            "field_provenance": {
                "affected_period": "Copied from RecoveryContext.reporting_period",
                "candidate_id": "Deterministic hash of material RecoveryContext fields",
                "rationale": "Structural placeholder rationale (no optimisation)",
                "strategy_type": "Fixed structural_placeholder for P2-MS010",
            },
            "missed_session_refs": [
                item.session_ref for item in context.missed_sessions
            ],
            "reporting_period": context.reporting_period,
            "source_service": SOURCE_SERVICE,
        }

        return RecoveryPlanCandidate(
            candidate_id=candidate_id,
            strategy_type=STRATEGY_STRUCTURAL_PLACEHOLDER,
            affected_period=context.reporting_period,
            rationale=rationale,
            provenance=provenance,
            advisory_only=True,
            recovery_id=recovery_id,
            student_id=context.student_id,
            generated_at=context.generated_at,
            authority=AUTHORITY_RECOVERY_PLANNER,
            availability=availability,
            unavailable_reason=context.unavailable_reason,
            recovery_version=RECOVERY_VERSION,
        )


def build_study_recovery_planner_adapter(
    *,
    enabled: bool,
) -> StudyRecoveryPlannerAdapter | None:
    """DI helper — construct adapter only when ENABLE_RECOVERY_PLANNER is ON."""
    if not enabled:
        return None
    return StudyRecoveryPlannerAdapter(enabled=True)


__all__ = [
    "ADAPTER_ID",
    "PLACEHOLDER_RATIONALE",
    "PORT_ID",
    "SOURCE_SERVICE",
    "StudyRecoveryPlannerAdapter",
    "build_study_recovery_planner_adapter",
    "deterministic_candidate_id",
    "deterministic_recovery_id",
]
