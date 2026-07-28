"""Session → Learner Lifecycle evidence hook (VP-001 / LP-001).

Records Learning Evidence and refreshes Twin / Decisions / Experience Models
after study activity. Fail-open: never breaks the session UX.
"""

from __future__ import annotations

import logging
from typing import Any

from app.application.runtime_integration.routing import resolve_active_instance
from app.domain.learning_evidence.evidence_type import EvidenceSource, EvidenceType
from app.models.student_curriculum_binding import SciCurriculumNodeState

logger = logging.getLogger(__name__)


def _resolve_node_stable_id(instance_id: str) -> str | None:
    """Pick a curriculum node for session evidence.

    Prefer the primary Educational Decision target when available; otherwise
    the first node state on the SCI.
    """
    try:
        from app.application.educational_reasoning_engine.query_service import (
            DecisionQueryService,
        )

        views = DecisionQueryService().highest_value_actions(instance_id, limit=1)
        if views:
            target = str(views[0].decision.curriculum_target or "").strip()
            if target:
                return target
    except Exception:  # noqa: BLE001 — fall through to node scan
        logger.debug(
            "VP-001 evidence node from decision failed instance=%s",
            instance_id,
            exc_info=True,
        )

    row = (
        SciCurriculumNodeState.query.filter_by(instance_id=instance_id)
        .order_by(SciCurriculumNodeState.id.asc())
        .first()
    )
    if row is None:
        return None
    return str(row.node_stable_id or "").strip() or None


def record_session_evidence(
    *,
    student_id: int,
    session_id: str,
    activity_id: str | None = None,
    event: str = "practice_attempt",
    metadata: dict[str, Any] | None = None,
    subject_code: str | None = None,
) -> Any | None:
    """Record session evidence via LP-001 when an active SCI exists.

    Args:
        student_id: Authenticated user id.
        session_id: Canonical session workspace id.
        activity_id: Optional activity identifier.
        event: ``practice_attempt`` (answer) or ``study_session`` (complete).
        metadata: Optional evidence metadata payload.
        subject_code: Optional SCI subject filter.

    Returns:
        ``LifecycleResult`` on success, ``None`` when skipped or failed open.
    """
    sid = int(student_id)
    instance = resolve_active_instance(sid, subject_code=subject_code)
    if instance is None:
        logger.debug(
            "VP-001 evidence skipped student=%s session=%s reason=no_active_sci",
            sid,
            session_id,
        )
        return None

    node_id = _resolve_node_stable_id(instance.instance_id)
    if not node_id:
        logger.info(
            "VP-001 evidence skipped student=%s instance=%s reason=no_node",
            sid,
            instance.instance_id,
        )
        return None

    event_key = (event or "practice_attempt").strip().lower()
    if event_key in {"complete", "study_session", "session_complete"}:
        evidence_type = EvidenceType.STUDY_SESSION.value
    else:
        evidence_type = EvidenceType.PRACTICE_ATTEMPT.value

    payload: dict[str, Any] = {
        "session_id": session_id,
        "source_surface": "session",
    }
    if activity_id:
        payload["activity_id"] = activity_id
        payload["item_id"] = activity_id
    if metadata:
        payload.update(metadata)

    correlation = f"vp001-session-{session_id}"
    try:
        from app.application.founder_validation.telemetry import (
            DEFAULT_FV_TELEMETRY,
            decision_refresh_ms_from_result,
            total_duration_ms_from_result,
        )
        from app.application.learner_lifecycle import LearnerLifecycleOrchestrator

        result = LearnerLifecycleOrchestrator().process_evidence(
            instance_id=instance.instance_id,
            node_stable_id=node_id,
            evidence_type=evidence_type,
            source=EvidenceSource.SESSION_RUNTIME.value,
            metadata=payload,
            correlation_id=correlation,
        )
        DEFAULT_FV_TELEMETRY.record_lifecycle_outcome(
            kind="evidence",
            succeeded=bool(result.succeeded),
            student_id=sid,
            operation_type="evidence_refresh",
            duration_ms=total_duration_ms_from_result(result),
            decision_refresh_ms=decision_refresh_ms_from_result(result),
            failure_cause=result.failure_cause,
            correlation_id=correlation,
        )
        if result.succeeded:
            logger.info(
                "VP-001 evidence recorded student=%s instance=%s type=%s",
                sid,
                instance.instance_id,
                evidence_type,
            )
        else:
            logger.warning(
                "VP-001 evidence incomplete student=%s instance=%s status=%s",
                sid,
                instance.instance_id,
                result.status,
            )
        return result
    except Exception as exc:  # noqa: BLE001 — session UX must not fail open
        try:
            from app.application.founder_validation.telemetry import (
                DEFAULT_FV_TELEMETRY,
            )

            DEFAULT_FV_TELEMETRY.record_system_failure(
                kind="evidence",
                student_id=sid,
                cause=exc.__class__.__name__,
                correlation_id=correlation,
            )
        except Exception:  # noqa: BLE001 — telemetry must never raise
            pass
        logger.exception(
            "VP-001 evidence failed open student=%s session=%s",
            sid,
            session_id,
        )
        return None
