"""SQL evidence write-through for Runtime C sittings (Phase 2 + Phase 3).

Aggregates scored practice responses from a sitting and records them as a
Runtime A ``StudyAttempt`` on the Phase 1 companion Mission via the existing
``StudySessionService.record_practice_outcome`` path (Evidence Authority +
``AdaptiveLearningService.update_mastery_after_attempt``).

Phase 3: at first scored-practice completion, resolve
``RuntimeMissionInstance.topic_code`` → SQL ``Topic.id`` (syllabus map →
ensure curriculum rows → official-code resolver), create TopicProgress for
**only** that practiced topic, then pass ``topic_id`` into
``record_practice_outcome``. Fail-open: on any resolution failure keep Phase 2
behaviour (``topic_id=None``, write attempt without mastery).

Does not replace Runtime C evidence-gate / Twin-consume / mission-complete
behaviour.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.student_runtime.syllabus_engine_map import (
    map_runtime_syllabus_to_engine,
)
from app.extensions import db
from app.infrastructure.adapters.learning_session.package_activity_engine import (
    PackageActivityEngine,
)
from app.infrastructure.session.store import SessionDocumentStore
from app.models.educational_runtime_engine import (
    RuntimeMissionInstance,
    RuntimeStudyPlanInstance,
)
from app.models.learning import StudyAttempt
from app.models.mission import Mission
from app.services.curriculum_service import CurriculumService
from app.services.educational_evidence_authority import EducationalEvidenceAuthority
from app.services.study_session_service import StudySessionService

logger = logging.getLogger(__name__)

_PRACTICE_STAGE = "practice"


@dataclass(frozen=True)
class ScoredPracticeCounts:
    """Aggregated scored practice outcome counts for one sitting."""

    questions_attempted: int
    questions_correct: int


def aggregate_scored_practice_responses(
    items: list[dict[str, Any]] | tuple[dict[str, Any], ...] | None,
) -> ScoredPracticeCounts:
    """Count scored practice items only (stage==practice, scored_correct set).

    Unscored practice, read, worked-example, and other stages are ignored.
    """
    attempted = 0
    correct = 0
    for raw in items or ():
        if not isinstance(raw, dict):
            continue
        stage = str(raw.get("stage") or "").strip().lower()
        if stage != _PRACTICE_STAGE:
            continue
        scored = raw.get("scored_correct")
        if scored is None:
            continue
        attempted += 1
        if scored is True:
            correct += 1
    return ScoredPracticeCounts(
        questions_attempted=attempted,
        questions_correct=correct,
    )


def load_sitting_response_items(
    store: SessionDocumentStore,
    *,
    student_id: str,
    session_id: str,
) -> list[dict[str, Any]]:
    """Load opaque activity response items for a sitting (best-effort)."""
    key = PackageActivityEngine._key(student_id, session_id)
    doc = store.get(PackageActivityEngine.NS_RESPONSES, key)
    if not isinstance(doc, dict):
        return []
    items = doc.get("items") or []
    return [dict(i) for i in items if isinstance(i, dict)]


def optional_sql_topic_id(raw: Any) -> int | None:
    """Coerce an already-numeric topic id; otherwise None."""
    if raw is None or raw == "":
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def _subject_and_version_from_mission(
    *,
    user_id: int,
    row: RuntimeMissionInstance,
) -> tuple[str | None, str | None]:
    """Read Runtime C syllabus identity from the plan instance (or identity)."""
    plan = RuntimeStudyPlanInstance.query.filter_by(
        plan_instance_id=row.plan_instance_id,
        user_id=user_id,
    ).first()
    if plan is not None:
        return (
            (plan.subject_code or "").strip() or None,
            (plan.version_label or "").strip() or None,
        )

    identity = (row.curriculum_identity or "").strip()
    if ":" in identity:
        subject, version = identity.split(":", 1)
        return subject.strip() or None, version.strip() or None
    return identity or None, None


def _educational_package_id_for_sitting(
    store: SessionDocumentStore,
    *,
    student_id: str,
    session_id: str,
) -> str:
    """Best-effort educational package id from the LSR session handle."""
    try:
        from app.infrastructure.adapters.learning_session.persistence import (
            LearningSessionPersistenceAdapter,
        )

        handle = LearningSessionPersistenceAdapter(store=store).load(
            session_id=session_id
        ) or {}
        return str(handle.get("educational_package_id") or "").strip()
    except Exception:  # noqa: BLE001 — fail-open
        logger.debug(
            "sql_topic_resolve package_id load failed session=%s student=%s",
            session_id,
            student_id,
            exc_info=True,
        )
        return ""


def _sql_topic_id_for_official_code(
    *,
    user_id: int,
    row: RuntimeMissionInstance,
    official_code: str,
    raw_topic_id: Any = None,
) -> int | None:
    """Resolve one syllabus official code to SQL Topic.id (Phase 3 chain)."""
    code = (official_code or "").strip()
    if not code:
        return optional_sql_topic_id(raw_topic_id)

    subject_code, version_label = _subject_and_version_from_mission(
        user_id=user_id,
        row=row,
    )
    mapped = map_runtime_syllabus_to_engine(subject_code, version_label)
    if mapped is None:
        logger.info(
            "sql_topic_resolve_unmapped subject=%s version_label=%s "
            "topic_code=%s mid=%s",
            subject_code,
            version_label,
            code,
            row.mission_instance_id,
        )
        return optional_sql_topic_id(raw_topic_id)

    curriculum = CurriculumService.ensure_curriculum_rows(
        mapped.exam_name,
        mapped.version,
    )
    if curriculum is None:
        logger.info(
            "sql_topic_resolve_ensure_failed exam=%s version=%s "
            "topic_code=%s mid=%s",
            mapped.exam_name,
            mapped.version,
            code,
            row.mission_instance_id,
        )
        return None

    topic_id = CurriculumService.resolve_topic_id_for_official_code(
        curriculum,
        code,
    )
    if topic_id is None:
        logger.info(
            "sql_topic_resolve_code_unresolved exam=%s version=%s "
            "topic_code=%s mid=%s",
            mapped.exam_name,
            mapped.version,
            code,
            row.mission_instance_id,
        )
        return None

    CurriculumService.get_or_create_topic_progress(user_id, topic_id)
    return topic_id


def resolve_sql_topic_ids_for_practice(
    *,
    user_id: int,
    row: RuntimeMissionInstance,
    raw_topic_id: Any = None,
    educational_package_id: str | None = None,
) -> tuple[list[int], str]:
    """Resolve SQL Topic.id values for scored-practice write-through.

    When the sitting package names real ``return_targets``, those are mapped
    through Policy V1's Twin-key resolver to unique parent topics, then to SQL
    Topic ids. Tip-surrogate ``row.topic_code`` is never used in that case.

    Returns ``(topic_ids, disposition)`` where disposition is one of:
    ``return_targets``, ``return_targets_unresolved``, ``mission_topic_code``.
    """
    try:
        from app.application.student_twin.practiced_identity import (
            resolve_practiced_twin_keys,
            subject_code_from_curriculum_identity,
            syllabus_code_for_twin_key,
        )

        pack_id = (educational_package_id or "").strip()
        subject = subject_code_from_curriculum_identity(
            row.curriculum_identity or ""
        )
        plan_subject, _version = _subject_and_version_from_mission(
            user_id=user_id, row=row
        )
        if plan_subject:
            subject = plan_subject

        resolution = resolve_practiced_twin_keys(
            educational_package_id=pack_id,
            subject_code=subject,
        )
        if resolution.has_return_targets:
            if resolution.unresolved or not resolution.twin_keys:
                logger.info(
                    "sql_topic_resolve tip_surrogate_blocked mid=%s package=%s",
                    row.mission_instance_id,
                    pack_id,
                )
                return [], "return_targets_unresolved"

            ids: list[int] = []
            seen: set[int] = set()
            for twin_key in resolution.twin_keys:
                official = syllabus_code_for_twin_key(
                    twin_key, subject_code=subject
                )
                if not official:
                    continue
                sql_id = _sql_topic_id_for_official_code(
                    user_id=user_id,
                    row=row,
                    official_code=official,
                    raw_topic_id=None,
                )
                if sql_id is not None and sql_id not in seen:
                    seen.add(sql_id)
                    ids.append(sql_id)
            if not ids:
                logger.info(
                    "sql_topic_resolve tip_surrogate_blocked mid=%s package=%s "
                    "reason=twin_keys_unmapped_to_sql",
                    row.mission_instance_id,
                    pack_id,
                )
                return [], "return_targets_unresolved"
            return ids, "return_targets"

        # Ordinary packages: prefer mission topic_code (human syllabus code).
        official_code = (row.topic_code or "").strip()
        if not official_code:
            coerced = optional_sql_topic_id(raw_topic_id)
            return ([coerced] if coerced is not None else []), "mission_topic_code"
        sql_id = _sql_topic_id_for_official_code(
            user_id=user_id,
            row=row,
            official_code=official_code,
            raw_topic_id=raw_topic_id,
        )
        return ([sql_id] if sql_id is not None else []), "mission_topic_code"
    except Exception:
        logger.exception(
            "sql_topic_resolve_failed mid=%s user=%s",
            getattr(row, "mission_instance_id", None),
            user_id,
        )
        return [], "return_targets_unresolved"


def resolve_sql_topic_id_for_practice(
    *,
    user_id: int,
    row: RuntimeMissionInstance,
    raw_topic_id: Any = None,
    educational_package_id: str | None = None,
) -> int | None:
    """Resolve a single SQL Topic.id for scored-practice write-through.

    Prefer ``return_targets`` when present. When multiple distinct parent
    topics resolve, returns ``None`` so callers fan-out via
    ``resolve_sql_topic_ids_for_practice`` rather than collapsing arbitrarily.
    On tip-surrogate block, returns ``None`` (never the tip topic).
    """
    ids, disposition = resolve_sql_topic_ids_for_practice(
        user_id=user_id,
        row=row,
        raw_topic_id=raw_topic_id,
        educational_package_id=educational_package_id,
    )
    if disposition == "return_targets_unresolved":
        return None
    if len(ids) == 1:
        return ids[0]
    if len(ids) > 1:
        return None
    return None


def maybe_write_sql_evidence_from_sitting(
    *,
    user_id: int,
    session_id: str,
    mission_instance_id: str,
    store: SessionDocumentStore,
    topic_id: Any = None,
    duration_minutes: int | None = None,
) -> StudyAttempt | None:
    """Write aggregated practice counts onto the companion Mission when eligible.

    Conditions (all required):
    - ``SR_SESSION_SQL_EVIDENCE_COMPANION`` is ON
    - companion ``sql_mission_id`` is bound and Mission exists
    - scored practice ``questions_attempted`` > 0

    Idempotent: if the companion already has structured question results (or
    is already Completed from a prior write), returns the existing attempt
    without creating another.

    Fail-open: unexpected errors are logged and return ``None`` so Runtime C
    completion is never blocked by this additive path.
    """
    try:
        return _write_sql_evidence_from_sitting(
            user_id=user_id,
            session_id=session_id,
            mission_instance_id=mission_instance_id,
            store=store,
            topic_id=topic_id,
            duration_minutes=duration_minutes,
        )
    except Exception as exc:
        logger.exception(
            "sql_evidence_write_through_failed session=%s mid=%s user=%s",
            session_id,
            mission_instance_id,
            user_id,
        )
        try:
            from app.application.founder_validation.telemetry import (
                DEFAULT_FV_TELEMETRY,
            )

            DEFAULT_FV_TELEMETRY.record_system_failure(
                kind="sql_evidence_write_through_failed",
                student_id=int(user_id) if user_id is not None else None,
                cause=exc.__class__.__name__,
            )
        except Exception:  # noqa: BLE001 - telemetry must never raise
            pass
        return None


def _write_sql_evidence_from_sitting(
    *,
    user_id: int,
    session_id: str,
    mission_instance_id: str,
    store: SessionDocumentStore,
    topic_id: Any = None,
    duration_minutes: int | None = None,
) -> StudyAttempt | None:
    flags = resolve_v2_feature_flags()
    if not bool(getattr(flags, "SR_SESSION_SQL_EVIDENCE_COMPANION", False)):
        return None

    mid = (mission_instance_id or "").strip()
    if not mid:
        return None

    row = RuntimeMissionInstance.query.filter_by(
        mission_instance_id=mid,
        user_id=user_id,
    ).first()
    if row is None or row.sql_mission_id is None:
        return None

    companion = Mission.query.get(int(row.sql_mission_id))
    if companion is None or int(companion.user_id) != int(user_id):
        logger.warning(
            "sql_evidence_companion_missing mid=%s sql_mission_id=%s",
            mid,
            row.sql_mission_id,
        )
        return None

    existing = StudySessionService._find_latest_attempt_for_mission(
        user_id, companion.id
    )
    if existing is not None and (
        EducationalEvidenceAuthority.study_attempt_has_structured_question_results(
            existing
        )
    ):
        return existing
    if companion.status == "Completed":
        return existing

    items = load_sitting_response_items(
        store,
        student_id=str(user_id),
        session_id=session_id,
    )
    counts = aggregate_scored_practice_responses(items)
    if counts.questions_attempted <= 0:
        return None

    # Phase 3 resolution only when scored practice exists (Session complete).
    pack_id = _educational_package_id_for_sitting(
        store,
        student_id=str(user_id),
        session_id=session_id,
    )
    topic_ids, disposition = resolve_sql_topic_ids_for_practice(
        user_id=user_id,
        row=row,
        raw_topic_id=topic_id,
        educational_package_id=pack_id,
    )
    # Single parent topic: existing StudyAttempt.topic_id path.
    # Multiple return_target parents: write the attempt without collapsing to
    # one arbitrary topic, then fan-out TopicProgress / mastery for each.
    # Unresolved return_targets: never attribute to tip-surrogate topic_code.
    primary_topic = topic_ids[0] if len(topic_ids) == 1 else None
    result = StudySessionService.record_practice_outcome(
        mission_id=int(companion.id),
        user_id=user_id,
        questions_attempted=counts.questions_attempted,
        questions_correct=counts.questions_correct,
        duration_minutes=duration_minutes,
        notes=None,
        topic_id=primary_topic,
    )
    if len(topic_ids) > 1:
        from app.services.adaptive_learning_service import AdaptiveLearningService

        for sql_topic in topic_ids:
            CurriculumService.get_or_create_topic_progress(user_id, sql_topic)
            AdaptiveLearningService.update_mastery_after_attempt(
                user_id=user_id,
                topic_id=sql_topic,
            )
    db.session.flush()
    logger.info(
        "sql_evidence_write_through session=%s mid=%s sql_mission_id=%s "
        "attempted=%s correct=%s topic_ids=%s disposition=%s",
        session_id,
        mid,
        companion.id,
        counts.questions_attempted,
        counts.questions_correct,
        topic_ids,
        disposition,
    )
    return result.study_attempt
