"""Enrolment → Learner Lifecycle onboard hook (VP-001 / LP-001).

Resolves a published CKG edition and invokes ``onboard_student`` so Preferred
Authority (RI-001) can serve Experience Models. Fail-open: never blocks
enrolment when Educational Intelligence prerequisites are absent.
"""

from __future__ import annotations

import logging
from typing import Any

from app.domain.curriculum_extraction.publication_state import PublicationState
from app.models.curriculum_knowledge_graph import CkgGraphEdition

logger = logging.getLogger(__name__)


def resolve_published_edition_id(
    subject_code: str | None = None,
) -> str | None:
    """Return the latest published CKG edition id, optionally for a subject.

    Args:
        subject_code: Optional subject filter (e.g. ``CS1``).

    Returns:
        Edition id string, or ``None`` when no published edition matches.
    """
    query = CkgGraphEdition.query.filter_by(
        publication_state=PublicationState.PUBLISHED.value,
    )
    if subject_code and str(subject_code).strip():
        wanted = str(subject_code).strip().upper()
        query = query.filter_by(subject_code=wanted)
    edition = query.order_by(CkgGraphEdition.id.desc()).first()
    if edition is None:
        return None
    return str(edition.edition_id)


def onboard_after_enrolment(
    *,
    student_id: int,
    subject_code: str | None = None,
    edition_id: str | None = None,
    correlation_id: str | None = None,
) -> Any | None:
    """Run LP-001 onboarding when a published CKG edition is available.

    Idempotent via LP-001 / EI-004. Soft-skips (returns ``None``) when no
    published edition exists so Runtime A JSON enrolment remains valid.

    Args:
        student_id: Authenticated user id.
        subject_code: Optional subject hint for edition resolution and SCI.
        edition_id: Explicit edition; when omitted, resolves latest published.
        correlation_id: Optional lifecycle correlation token.

    Returns:
        ``LifecycleResult`` on success, ``None`` when skipped or failed open.
    """
    sid = int(student_id)
    resolved = (edition_id or "").strip() or resolve_published_edition_id(
        subject_code
    )
    if not resolved:
        logger.info(
            "VP-001 lifecycle onboard skipped student=%s subject=%s "
            "reason=no_published_edition",
            sid,
            subject_code,
        )
        return None

    try:
        from app.application.founder_validation.telemetry import (
            DEFAULT_FV_TELEMETRY,
            decision_refresh_ms_from_result,
            total_duration_ms_from_result,
        )
        from app.application.learner_lifecycle import LearnerLifecycleOrchestrator

        result = LearnerLifecycleOrchestrator().onboard_student(
            student_id=sid,
            edition_id=resolved,
            subject_code=subject_code,
            correlation_id=correlation_id,
        )
        DEFAULT_FV_TELEMETRY.record_lifecycle_outcome(
            kind="onboard",
            succeeded=bool(result.succeeded),
            student_id=sid,
            operation_type="onboard",
            duration_ms=total_duration_ms_from_result(result),
            decision_refresh_ms=decision_refresh_ms_from_result(result),
            failure_cause=result.failure_cause,
            correlation_id=correlation_id,
        )
        if result.succeeded:
            logger.info(
                "VP-001 lifecycle onboard complete student=%s edition=%s "
                "instance=%s",
                sid,
                resolved,
                result.instance_id,
            )
        else:
            logger.warning(
                "VP-001 lifecycle onboard incomplete student=%s edition=%s "
                "status=%s stage=%s",
                sid,
                resolved,
                result.status,
                result.failed_stage,
            )
        return result
    except Exception as exc:  # noqa: BLE001 — enrolment must not fail open
        try:
            from app.application.founder_validation.telemetry import (
                DEFAULT_FV_TELEMETRY,
            )

            DEFAULT_FV_TELEMETRY.record_system_failure(
                kind="onboard",
                student_id=sid,
                cause=exc.__class__.__name__,
                correlation_id=correlation_id,
            )
        except Exception:  # noqa: BLE001 — telemetry must never raise
            pass
        logger.exception(
            "VP-001 lifecycle onboard failed open student=%s edition=%s",
            sid,
            resolved,
        )
        return None
