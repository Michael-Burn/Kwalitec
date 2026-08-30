"""Audit helper for DECISION_RECORDED on the Runtime C event spine."""

from __future__ import annotations

import json
import logging
import uuid
from datetime import UTC, datetime
from typing import Any

from app.application.adaptive_decision.types import SittingDecision
from app.domain.educational_runtime_engine.events import EducationalEventType
from app.extensions import db
from app.models.educational_runtime_engine import RuntimeEducationalEvent

logger = logging.getLogger(__name__)


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:16]}"


def record_decision_recorded(
    *,
    decision: SittingDecision,
    user_id: int,
    subject_code: str,
    curriculum_identity: str | None,
    flag_enabled: bool,
    mission_instance_id: str | None = None,
    enrolment_id: str | None = None,
    plan_instance_id: str | None = None,
) -> RuntimeEducationalEvent:
    """Append one DECISION_RECORDED event for this engine invocation."""
    occurred_at = datetime.now(UTC)
    payload: dict[str, Any] = {
        "decision_id": decision.decision_id,
        "occurred_at": occurred_at.isoformat(),
        "user_id": user_id,
        "subject_code": subject_code,
        "curriculum_identity": curriculum_identity,
        "intent": decision.intent,
        "seam": "runtime_c.generate_daily_mission",
        "outcome": decision.outcome.value,
        "policy_id": decision.policy_id,
        "block_reason": decision.block_reason,
        "topic_id": decision.topic_id,
        "topic_code": decision.topic_code,
        "educational_package_id": decision.educational_package_id,
        "educational_package_mode": decision.educational_package_mode,
        "educational_campaign_day": decision.educational_campaign_day,
        "certified_mission_id": decision.certified_mission_id,
        "objective_ids": list(decision.objective_ids),
        "reason_codes": list(decision.reason_codes),
        "mission_instance_id": mission_instance_id,
        "flag_enabled": flag_enabled,
        "selection_trace": dict(decision.selection_trace or {}),
    }
    row = RuntimeEducationalEvent(
        event_id=_new_id("evt"),
        event_type=EducationalEventType.DECISION_RECORDED.value,
        user_id=user_id,
        enrolment_id=enrolment_id or decision.enrolment_id,
        plan_instance_id=plan_instance_id or decision.plan_instance_id,
        curriculum_identity=curriculum_identity
        or decision.curriculum_identity
        or "",
        topic_id=decision.topic_id,
        mission_instance_id=mission_instance_id,
        payload_json=json.dumps(payload),
        occurred_at=occurred_at,
    )
    db.session.add(row)
    logger.info(
        "adr027_m0_decision_recorded decision_id=%s outcome=%s "
        "block_reason=%s user_id=%s subject=%s",
        decision.decision_id,
        decision.outcome.value,
        decision.block_reason,
        user_id,
        subject_code,
    )
    return row
