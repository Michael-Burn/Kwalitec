"""SQL evidence write-through for Runtime C sittings (Phase 2).

Aggregates scored practice responses from a sitting and records them as a
Runtime A ``StudyAttempt`` on the Phase 1 companion Mission via the existing
``StudySessionService.record_practice_outcome`` path (Evidence Authority +
``AdaptiveLearningService.update_mastery_after_attempt``).

Does not resolve topic codes to SQL ``Topic.id`` (Phase 3). Does not replace
Runtime C evidence-gate / Twin-consume / mission-complete behaviour.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.extensions import db
from app.infrastructure.adapters.learning_session.package_activity_engine import (
    PackageActivityEngine,
)
from app.infrastructure.session.store import SessionDocumentStore
from app.models.educational_runtime_engine import RuntimeMissionInstance
from app.models.learning import StudyAttempt
from app.models.mission import Mission
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
    """Coerce an already-numeric topic id; otherwise None (Phase 3 resolves codes)."""
    if raw is None or raw == "":
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
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
    except Exception:
        logger.exception(
            "sql_evidence_write_through_failed session=%s mid=%s user=%s",
            session_id,
            mission_instance_id,
            user_id,
        )
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

    resolved_topic = optional_sql_topic_id(topic_id)
    result = StudySessionService.record_practice_outcome(
        mission_id=int(companion.id),
        user_id=user_id,
        questions_attempted=counts.questions_attempted,
        questions_correct=counts.questions_correct,
        duration_minutes=duration_minutes,
        notes=None,
        topic_id=resolved_topic,
    )
    db.session.flush()
    logger.info(
        "sql_evidence_write_through session=%s mid=%s sql_mission_id=%s "
        "attempted=%s correct=%s topic_id=%s",
        session_id,
        mid,
        companion.id,
        counts.questions_attempted,
        counts.questions_correct,
        resolved_topic,
    )
    return result.study_attempt
