"""Session → Learner Lifecycle evidence hook (VP-001 / LP-001).

Records Learning Evidence and refreshes Twin / Decisions / Experience Models
after study activity. Fail-open: never breaks the session UX.

Attribution prefers the curriculum node the student actually practiced in the
session (LSR handle topic / package identity), not a decision target or an
arbitrary lowest-id SCI node.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from app.application.runtime_integration.routing import resolve_active_instance
from app.domain.learning_evidence.evidence_type import EvidenceSource, EvidenceType
from app.models.student_curriculum_binding import (
    SciCurriculumNodeState,
    SciStudentCurriculumInstance,
)

logger = logging.getLogger(__name__)

# Distinguishable attribution provenance written into evidence metadata.
ATTRIBUTION_SESSION_PRACTICED = "session_practiced"
ATTRIBUTION_DECISION_TARGET = "decision_target"
ATTRIBUTION_SCI_FIRST_NODE = "sci_first_node"

_SYLLABUS_CODE_RE = re.compile(r"^\d+(?:\.\d+)+$")


def _sci_has_node(instance_id: str, node_stable_id: str) -> bool:
    token = (node_stable_id or "").strip()
    if not token:
        return False
    return (
        SciCurriculumNodeState.query.filter_by(
            instance_id=instance_id,
            node_stable_id=token,
        ).first()
        is not None
    )


def _try_stable_curriculum_id(token: str) -> str | None:
    raw = (token or "").strip()
    if not raw:
        return None
    try:
        from app.domain.curriculum_knowledge_graph.value_objects import (
            StableCurriculumId,
        )

        return StableCurriculumId.of(raw).value
    except Exception:  # noqa: BLE001 — not a CKG stable id
        return None


def _load_session_practiced_identity(session_id: str) -> dict[str, Any]:
    """Load practiced topic/package identity from the LSR session handle.

    Same identity fields Twin and Spacing already trust on the live session
    document (``topic_id``, ``educational_package_id``, mission fallback).
    """
    identity: dict[str, Any] = {
        "topic_id": "",
        "educational_package_id": "",
        "topic_code": "",
        "objective_ids": [],
        "mission_instance_id": "",
        "has_session_document": False,
    }
    sid = (session_id or "").strip()
    if not sid:
        return identity

    try:
        from app.infrastructure.adapters.learning_session.persistence import (
            LearningSessionPersistenceAdapter,
        )

        handle = LearningSessionPersistenceAdapter().load(session_id=sid) or {}
    except Exception:  # noqa: BLE001 — fail-open to empty identity
        logger.debug(
            "VP-001 session handle load failed session=%s",
            sid,
            exc_info=True,
        )
        return identity

    if not handle:
        return identity

    identity["has_session_document"] = True
    identity["topic_id"] = str(handle.get("topic_id") or "").strip()
    identity["educational_package_id"] = str(
        handle.get("educational_package_id") or ""
    ).strip()
    identity["mission_instance_id"] = str(
        handle.get("mission_instance_id") or ""
    ).strip()
    raw_objectives = handle.get("objective_ids") or []
    if isinstance(raw_objectives, list | tuple):
        identity["objective_ids"] = [
            str(item).strip()
            for item in raw_objectives
            if str(item or "").strip()
        ]

    mission_id = identity["mission_instance_id"]
    if mission_id and (
        not identity["topic_id"]
        or not identity["educational_package_id"]
        or not identity["topic_code"]
    ):
        try:
            from app.models.educational_runtime_engine import RuntimeMissionInstance

            row = RuntimeMissionInstance.query.filter_by(
                mission_instance_id=mission_id
            ).first()
            if row is not None:
                if not identity["topic_id"]:
                    identity["topic_id"] = str(row.topic_id or "").strip()
                if not identity["topic_code"]:
                    identity["topic_code"] = str(row.topic_code or "").strip()
        except Exception:  # noqa: BLE001 — optional mission enrichment
            logger.debug(
                "VP-001 mission identity fallback failed mission=%s",
                mission_id,
                exc_info=True,
            )

    return identity


def _resolve_from_syllabus_code(
    instance_id: str,
    *,
    subject_code: str,
    syllabus_code: str,
) -> str | None:
    """Map a syllabus number (topic or LO) onto an SCI-resident CKG stable id."""
    code = (syllabus_code or "").strip()
    subject = (subject_code or "").strip().upper()
    if not code or not subject:
        return None
    prefix = f"{subject}."

    try:
        from app.models.curriculum_knowledge_graph import (
            CkgLearningObjective,
            CkgSection,
            CkgSubsection,
            CkgTopic,
        )
    except Exception:  # noqa: BLE001
        return None

    # Prefer the deepest match: LO → subsection → section → topic.
    for model in (CkgLearningObjective, CkgSubsection, CkgSection, CkgTopic):
        rows = model.query.filter_by(code=code).all()
        for row in rows:
            stable = str(getattr(row, "stable_id", "") or "").strip()
            if not stable.startswith(prefix):
                continue
            if _sci_has_node(instance_id, stable):
                return stable
    return None


def _syllabus_codes_from_package(package_id: str) -> list[str]:
    """Return preferred syllabus codes from a certified package (LO then topic)."""
    pid = (package_id or "").strip()
    if not pid:
        return []
    try:
        from app.application.educational_packages.loader import find_package_by_id

        pack = find_package_by_id(pid)
    except Exception:  # noqa: BLE001
        logger.debug(
            "VP-001 package lookup failed package=%s",
            pid,
            exc_info=True,
        )
        return []
    if pack is None:
        return []
    codes: list[str] = []
    focus = str(getattr(pack, "topic_focus_lo", "") or "").strip()
    topic_code = str(getattr(pack, "topic_code", "") or "").strip()
    if focus:
        codes.append(focus)
    if topic_code and topic_code not in codes:
        codes.append(topic_code)
    return codes


def _syllabus_code_from_published_topic(
    topic_id: str,
    *,
    subject_code: str,
) -> str | None:
    """Resolve a Runtime published topic id to a syllabus topic code."""
    token = (topic_id or "").strip()
    subject = (subject_code or "").strip()
    if not token or not subject:
        return None
    try:
        from app.application.student_twin.canonical_topic_id import CanonicalTopicId

        published = CanonicalTopicId().resolve_from_runtime_topic_id(
            token, subject_code=subject
        )
        if not published:
            return None
        from app.application.educational_engine_foundation.service import (
            EducationalEngineFoundationService,
        )

        artefacts = EducationalEngineFoundationService().derive_active(subject)
        if artefacts is None:
            return None
        for raw in artefacts.topics or ():
            if not isinstance(raw, dict):
                continue
            if str(raw.get("topic_id") or "").strip() != published:
                continue
            code = str(raw.get("code") or raw.get("topic_code") or "").strip()
            if code:
                return code
    except Exception:  # noqa: BLE001
        logger.debug(
            "VP-001 published topic→code failed topic=%s subject=%s",
            token,
            subject,
            exc_info=True,
        )
    return None


def _resolve_practiced_node_stable_id(
    instance_id: str,
    *,
    subject_code: str,
    identity: dict[str, Any],
) -> str | None:
    """Resolve the SCI node the student practiced from session identity."""
    candidates: list[str] = []

    topic_id = str(identity.get("topic_id") or "").strip()
    pack_id = str(identity.get("educational_package_id") or "").strip()
    topic_code = str(identity.get("topic_code") or "").strip()
    objective_ids = identity.get("objective_ids") or []

    # 1. Direct CKG stable ids already on the session (rare but authoritative).
    for raw in (topic_id, *list(objective_ids)):
        stable = _try_stable_curriculum_id(str(raw))
        if stable and _sci_has_node(instance_id, stable):
            return stable

    # 2. Package focus LO / topic_code (Spacing's identity unit → CKG code).
    for code in _syllabus_codes_from_package(pack_id):
        if code not in candidates:
            candidates.append(code)

    # 3. Mission / handle syllabus codes.
    if topic_code and topic_code not in candidates:
        candidates.append(topic_code)
    if (
        topic_id
        and _SYLLABUS_CODE_RE.fullmatch(topic_id)
        and topic_id not in candidates
    ):
        candidates.append(topic_id)

    # 4. Published Runtime topic id → artefact syllabus code.
    published_code = _syllabus_code_from_published_topic(
        topic_id, subject_code=subject_code
    )
    if published_code and published_code not in candidates:
        candidates.append(published_code)

    for code in candidates:
        resolved = _resolve_from_syllabus_code(
            instance_id,
            subject_code=subject_code,
            syllabus_code=code,
        )
        if resolved:
            return resolved
    return None


def _resolve_fallback_node_stable_id(
    instance_id: str,
) -> tuple[str | None, str | None]:
    """Legacy fallback when no practiced session identity is available.

    Returns ``(node_stable_id, attribution_source)``. Source is always one of
    the fallback markers so consumers can distrust these attributions.
    """
    try:
        from app.application.educational_reasoning_engine.query_service import (
            DecisionQueryService,
        )

        views = DecisionQueryService().highest_value_actions(instance_id, limit=1)
        if views:
            target = str(views[0].decision.curriculum_target or "").strip()
            if target and _sci_has_node(instance_id, target):
                return target, ATTRIBUTION_DECISION_TARGET
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
        return None, None
    node = str(row.node_stable_id or "").strip() or None
    if not node:
        return None, None
    return node, ATTRIBUTION_SCI_FIRST_NODE


def _has_practiced_identity(identity: dict[str, Any]) -> bool:
    """True when the session carries a genuine practiced topic/package hint."""
    if str(identity.get("topic_id") or "").strip():
        return True
    if str(identity.get("educational_package_id") or "").strip():
        return True
    if str(identity.get("topic_code") or "").strip():
        return True
    objectives = identity.get("objective_ids") or []
    return any(str(item or "").strip() for item in objectives)


def _resolve_node_for_evidence(
    instance_id: str,
    *,
    subject_code: str,
    session_id: str,
) -> tuple[str | None, str | None, dict[str, Any]]:
    """Choose the evidence node and provenance for a session event.

    Prefer session-practiced identity. When a practiced hint exists but cannot
    be mapped onto the SCI, skip (return None) rather than fabricating a node.
    Only when no practiced identity is available do we keep the legacy
    decision-target / lowest-id fallbacks, marked as untrusted sources.
    """
    identity = _load_session_practiced_identity(session_id)
    if _has_practiced_identity(identity):
        node = _resolve_practiced_node_stable_id(
            instance_id,
            subject_code=subject_code,
            identity=identity,
        )
        if node:
            return node, ATTRIBUTION_SESSION_PRACTICED, identity
        return None, None, identity

    node, source = _resolve_fallback_node_stable_id(instance_id)
    return node, source, identity


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
        # V1S-007: attempt SCI ensure for Runtime C students before skipping.
        try:
            from app.application.educational_experience import (
                EducationalExperienceService,
            )
            from app.application.educational_runtime_engine import ensure_active_sci

            enrolment = EducationalExperienceService().find_enrolment_for_experience(
                sid
            )
            if enrolment is not None:
                ensure_active_sci(
                    student_id=sid,
                    subject_code=subject_code or enrolment.subject_code,
                    correlation_id=f"v1s007-evidence-{session_id}",
                    require=False,
                )
                instance = resolve_active_instance(
                    sid, subject_code=subject_code or enrolment.subject_code
                )
        except Exception:  # noqa: BLE001 — evidence remains fail-open
            logger.debug(
                "VP-001 SCI ensure before evidence failed student=%s",
                sid,
                exc_info=True,
            )
    if instance is None:
        logger.debug(
            "VP-001 evidence skipped student=%s session=%s reason=no_active_sci",
            sid,
            session_id,
        )
        return None

    sci_subject = str(
        subject_code
        or getattr(instance, "subject_code", "")
        or ""
    ).strip()
    if not sci_subject:
        row = SciStudentCurriculumInstance.query.filter_by(
            instance_id=instance.instance_id
        ).first()
        sci_subject = str(getattr(row, "subject_code", "") or "").strip()

    node_id, attribution_source, identity = _resolve_node_for_evidence(
        instance.instance_id,
        subject_code=sci_subject,
        session_id=session_id,
    )
    if not node_id:
        if _has_practiced_identity(identity):
            logger.info(
                "VP-001 evidence skipped student=%s instance=%s "
                "reason=unresolved_practiced_identity topic=%s package=%s",
                sid,
                instance.instance_id,
                identity.get("topic_id") or "",
                identity.get("educational_package_id") or "",
            )
        else:
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
        "attribution_source": attribution_source or ATTRIBUTION_SCI_FIRST_NODE,
    }
    practiced_topic = str(identity.get("topic_id") or "").strip()
    practiced_pack = str(identity.get("educational_package_id") or "").strip()
    if practiced_topic:
        payload["practiced_topic_id"] = practiced_topic
    if practiced_pack:
        payload["practiced_educational_package_id"] = practiced_pack
    if activity_id:
        payload["activity_id"] = activity_id
        payload["item_id"] = activity_id
    if metadata:
        payload.update(metadata)
        # Session-derived provenance must win over caller metadata.
        payload["attribution_source"] = (
            attribution_source or ATTRIBUTION_SCI_FIRST_NODE
        )

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
                "VP-001 evidence recorded student=%s instance=%s type=%s "
                "node=%s attribution=%s",
                sid,
                instance.instance_id,
                evidence_type,
                node_id,
                attribution_source,
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
