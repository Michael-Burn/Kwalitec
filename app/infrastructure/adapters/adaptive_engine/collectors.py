"""Runtime A collectors for Adaptive Input Assembler (MS-003 A1).

Collectors perform read-only collection of authoritative educational data.
They must not estimate missing values, infer educational state beyond
pass-through projection, score topics, or mutate Runtime A.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Protocol, runtime_checkable

from app.infrastructure.adapters.adaptive_engine.provenance import (
    REASON_COLLECTOR_ERROR,
    REASON_NO_ACTIVE_PLAN,
    REASON_NO_CURRICULUM,
    REASON_NOT_FOUND,
    REASON_UNAVAILABLE,
)

logger = logging.getLogger(__name__)

# Hard caps (ADAPTIVE_DATA_FLOW.md) — bounded history, deterministic order.
DEFAULT_ATTEMPT_LIMIT = 50
DEFAULT_MISSION_LIMIT = 30


@dataclass(frozen=True)
class CollectorResult:
    """Result of one Runtime A input collector.

    ``available`` False means the field must be marked Unavailable with
    ``unavailable_reason``. Empty-but-available payloads (new learners) are
    honest emptiness, not Unavailable.
    """

    available: bool
    payload: Any
    source_service: str
    source_entity: str
    unavailable_reason: str = ""

    def __post_init__(self) -> None:
        if not self.available and not (self.unavailable_reason or "").strip():
            raise ValueError(
                "unavailable_reason required when collector result is unavailable"
            )


@runtime_checkable
class RuntimeACollector(Protocol):
    """Read-only collector Protocol for one Adaptive input field."""

    @property
    def field_name(self) -> str:
        """AdaptiveInputBundle field this collector feeds."""

    def collect(
        self,
        user_id: int,
        *,
        as_of: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> CollectorResult:
        """Collect authoritative Runtime A data for *user_id*."""


def parse_as_of_date(as_of: str | None) -> date | None:
    """Parse assembler ``as_of`` clock into a date (no wall-clock fallback)."""
    if as_of is None or not str(as_of).strip():
        return None
    text = str(as_of).strip()
    try:
        if "T" in text:
            return datetime.fromisoformat(text.replace("Z", "+00:00")).date()
        return date.fromisoformat(text[:10])
    except ValueError:
        return None


def read_active_study_plan(
    user_id: int,
    *,
    study_plan_model: Any | None = None,
) -> Any | None:
    """Read-only active StudyPlan lookup.

    Does **not** call ``StudyPlanService.get_user_active_plan`` (which may
    self-heal curriculum binding and commit). Assembler collectors must remain
    Runtime A write-free.
    """
    plan_cls = study_plan_model
    if plan_cls is None:
        from app.models.study_plan import StudyPlan

        plan_cls = StudyPlan
    return (
        plan_cls.query.filter_by(user_id=user_id, active=True)
        .order_by(plan_cls.id.asc())
        .first()
    )

def _iso_date(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


def _iso_datetime(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


class EvidenceCollector:
    """Collect authorised StudyAttempt evidence summary (read-only)."""

    field_name = "evidence"
    SOURCE_SERVICE = "educational_evidence_authority"
    SOURCE_ENTITY = "StudyAttempt"

    def __init__(
        self,
        *,
        attempt_limit: int = DEFAULT_ATTEMPT_LIMIT,
        study_attempt_model: Any | None = None,
        evidence_authority: Any | None = None,
    ) -> None:
        self._attempt_limit = max(1, int(attempt_limit))
        self._study_attempt_model = study_attempt_model
        self._evidence_authority = evidence_authority

    def collect(
        self,
        user_id: int,
        *,
        as_of: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> CollectorResult:
        _ = (as_of, context)
        try:
            attempt_cls = self._resolve_attempt_model()
            authority = self._resolve_authority()
            attempts = (
                attempt_cls.query.filter_by(user_id=user_id)
                .order_by(
                    attempt_cls.study_date.desc(),
                    attempt_cls.id.desc(),
                )
                .limit(self._attempt_limit)
                .all()
            )
            items: list[dict[str, Any]] = []
            authorised_count = 0
            for attempt in attempts:
                has_auth = authority.study_attempt_has_structured_question_results(
                    attempt
                )
                if has_auth:
                    authorised_count += 1
                accuracy = attempt.get_accuracy_percentage()
                items.append(
                    {
                        "attempt_id": str(attempt.id),
                        "mission_id": str(attempt.mission_id),
                        "topic_id": (
                            None
                            if attempt.topic_id is None
                            else str(attempt.topic_id)
                        ),
                        "study_date": _iso_date(attempt.study_date),
                        "authorised_structured_results": bool(has_auth),
                        "accuracy_pct": (
                            None if accuracy is None else round(float(accuracy), 4)
                        ),
                        "questions_attempted": attempt.questions_attempted,
                        "questions_correct": attempt.questions_correct,
                    }
                )
            # Stable ascending order for determinism (collect desc for recency bound).
            items.sort(
                key=lambda row: (
                    row.get("study_date") or "",
                    row.get("attempt_id") or "",
                )
            )
            return CollectorResult(
                available=True,
                payload={
                    "attempt_count": len(items),
                    "authorised_count": authorised_count,
                    "attempts": items,
                },
                source_service=self.SOURCE_SERVICE,
                source_entity=self.SOURCE_ENTITY,
            )
        except Exception as exc:  # noqa: BLE001
            logger.debug("evidence collect failed user_id=%s", user_id, exc_info=True)
            return CollectorResult(
                available=False,
                payload={},
                source_service=self.SOURCE_SERVICE,
                source_entity=self.SOURCE_ENTITY,
                unavailable_reason=f"{REASON_COLLECTOR_ERROR}:{type(exc).__name__}",
            )

    def _resolve_attempt_model(self) -> Any:
        if self._study_attempt_model is not None:
            return self._study_attempt_model
        from app.models.learning import StudyAttempt

        return StudyAttempt

    def _resolve_authority(self) -> Any:
        if self._evidence_authority is not None:
            return self._evidence_authority
        from app.services.educational_evidence_authority import (
            EducationalEvidenceAuthority,
        )

        return EducationalEvidenceAuthority


class TopicProgressCollector:
    """Collect TopicProgress rows (read-only)."""

    field_name = "topic_progress"
    SOURCE_SERVICE = "adaptive_learning_service"
    SOURCE_ENTITY = "TopicProgress"

    def __init__(self, *, topic_progress_model: Any | None = None) -> None:
        self._topic_progress_model = topic_progress_model

    def collect(
        self,
        user_id: int,
        *,
        as_of: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> CollectorResult:
        _ = (as_of, context)
        try:
            progress_cls = self._resolve_model()
            rows = (
                progress_cls.query.filter_by(user_id=user_id)
                .order_by(progress_cls.topic_id.asc(), progress_cls.id.asc())
                .all()
            )
            items: list[dict[str, Any]] = []
            for row in rows:
                topic = getattr(row, "topic", None)
                items.append(
                    {
                        "topic_progress_id": str(row.id),
                        "topic_id": str(row.topic_id),
                        "topic_name": (
                            ""
                            if topic is None
                            else str(getattr(topic, "name", "") or "")
                        ),
                        "mastery_score": float(row.mastery_score or 0.0),
                        "average_accuracy": (
                            None
                            if row.average_accuracy is None
                            else float(row.average_accuracy)
                        ),
                        "current_stage": str(row.current_stage or ""),
                        "confidence": str(row.confidence or ""),
                        "completed": bool(row.completed),
                        "revision_count": int(row.revision_count or 0),
                        "last_reviewed": _iso_datetime(row.last_reviewed),
                        "next_review_date": _iso_date(row.next_review_date),
                    }
                )
            return CollectorResult(
                available=True,
                payload=items,
                source_service=self.SOURCE_SERVICE,
                source_entity=self.SOURCE_ENTITY,
            )
        except Exception as exc:  # noqa: BLE001
            logger.debug(
                "topic_progress collect failed user_id=%s", user_id, exc_info=True
            )
            return CollectorResult(
                available=False,
                payload=[],
                source_service=self.SOURCE_SERVICE,
                source_entity=self.SOURCE_ENTITY,
                unavailable_reason=f"{REASON_COLLECTOR_ERROR}:{type(exc).__name__}",
            )

    def _resolve_model(self) -> Any:
        if self._topic_progress_model is not None:
            return self._topic_progress_model
        from app.models.topic_progress import TopicProgress

        return TopicProgress


class StudyAttemptCollector:
    """Collect bounded StudyAttempt history (read-only)."""

    field_name = "study_attempts"
    SOURCE_SERVICE = "learning_service"
    SOURCE_ENTITY = "StudyAttempt"

    def __init__(
        self,
        *,
        attempt_limit: int = DEFAULT_ATTEMPT_LIMIT,
        study_attempt_model: Any | None = None,
    ) -> None:
        self._attempt_limit = max(1, int(attempt_limit))
        self._study_attempt_model = study_attempt_model

    def collect(
        self,
        user_id: int,
        *,
        as_of: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> CollectorResult:
        _ = (as_of, context)
        try:
            attempt_cls = self._resolve_model()
            attempts = (
                attempt_cls.query.filter_by(user_id=user_id)
                .order_by(
                    attempt_cls.study_date.desc(),
                    attempt_cls.id.desc(),
                )
                .limit(self._attempt_limit)
                .all()
            )
            items: list[dict[str, Any]] = []
            for attempt in attempts:
                accuracy = attempt.get_accuracy_percentage()
                items.append(
                    {
                        "attempt_id": str(attempt.id),
                        "mission_id": str(attempt.mission_id),
                        "topic_id": (
                            None
                            if attempt.topic_id is None
                            else str(attempt.topic_id)
                        ),
                        "study_date": _iso_date(attempt.study_date),
                        "duration_minutes": attempt.duration_minutes,
                        "questions_attempted": attempt.questions_attempted,
                        "questions_correct": attempt.questions_correct,
                        "accuracy_pct": (
                            None if accuracy is None else round(float(accuracy), 4)
                        ),
                        "confidence_before": attempt.confidence_before or "",
                        "confidence_after": attempt.confidence_after or "",
                    }
                )
            items.sort(
                key=lambda row: (
                    row.get("study_date") or "",
                    row.get("attempt_id") or "",
                )
            )
            return CollectorResult(
                available=True,
                payload=items,
                source_service=self.SOURCE_SERVICE,
                source_entity=self.SOURCE_ENTITY,
            )
        except Exception as exc:  # noqa: BLE001
            logger.debug(
                "study_attempts collect failed user_id=%s", user_id, exc_info=True
            )
            return CollectorResult(
                available=False,
                payload=[],
                source_service=self.SOURCE_SERVICE,
                source_entity=self.SOURCE_ENTITY,
                unavailable_reason=f"{REASON_COLLECTOR_ERROR}:{type(exc).__name__}",
            )

    def _resolve_model(self) -> Any:
        if self._study_attempt_model is not None:
            return self._study_attempt_model
        from app.models.learning import StudyAttempt

        return StudyAttempt


class MissionCollector:
    """Collect bounded Mission history (read-only — no MissionService repair)."""

    field_name = "mission"
    SOURCE_SERVICE = "mission_service"
    SOURCE_ENTITY = "Mission"

    def __init__(
        self,
        *,
        mission_limit: int = DEFAULT_MISSION_LIMIT,
        mission_model: Any | None = None,
    ) -> None:
        self._mission_limit = max(1, int(mission_limit))
        self._mission_model = mission_model

    def collect(
        self,
        user_id: int,
        *,
        as_of: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> CollectorResult:
        context = context or {}
        try:
            mission_cls = self._resolve_model()
            query = mission_cls.query.filter_by(user_id=user_id)
            plan_id = context.get("study_plan_id")
            if plan_id is not None:
                query = query.filter_by(study_plan_id=plan_id)
            as_of_date = parse_as_of_date(as_of)
            missions = (
                query.order_by(
                    mission_cls.mission_date.desc(),
                    mission_cls.id.desc(),
                )
                .limit(self._mission_limit)
                .all()
            )
            items: list[dict[str, Any]] = []
            today_mission: dict[str, Any] | None = None
            for mission in missions:
                mapped = {
                    "mission_id": str(mission.id),
                    "mission_date": _iso_date(mission.mission_date),
                    "title": str(mission.title or ""),
                    "status": str(mission.status or ""),
                    "study_plan_id": (
                        None
                        if mission.study_plan_id is None
                        else str(mission.study_plan_id)
                    ),
                    "subject_id": str(mission.subject_id),
                }
                items.append(mapped)
                if (
                    as_of_date is not None
                    and today_mission is None
                    and _iso_date(mission.mission_date) == as_of_date.isoformat()
                ):
                    today_mission = mapped
            items.sort(
                key=lambda row: (
                    row.get("mission_date") or "",
                    row.get("mission_id") or "",
                )
            )
            return CollectorResult(
                available=True,
                payload={
                    "today": today_mission,
                    "history": items,
                    "history_count": len(items),
                },
                source_service=self.SOURCE_SERVICE,
                source_entity=self.SOURCE_ENTITY,
            )
        except Exception as exc:  # noqa: BLE001
            logger.debug("mission collect failed user_id=%s", user_id, exc_info=True)
            return CollectorResult(
                available=False,
                payload={},
                source_service=self.SOURCE_SERVICE,
                source_entity=self.SOURCE_ENTITY,
                unavailable_reason=f"{REASON_COLLECTOR_ERROR}:{type(exc).__name__}",
            )

    def _resolve_model(self) -> Any:
        if self._mission_model is not None:
            return self._mission_model
        from app.models.mission import Mission

        return Mission


class ReadinessCollector:
    """Collect ReadinessService aggregates (pass-through — no private formula)."""

    field_name = "readiness"
    SOURCE_SERVICE = "readiness_service"
    SOURCE_ENTITY = "ReadinessAggregate"

    def __init__(self, *, readiness_service: Any | None = None) -> None:
        self._readiness_service = readiness_service

    def collect(
        self,
        user_id: int,
        *,
        as_of: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> CollectorResult:
        _ = (as_of, context)
        try:
            service = self._resolve_service()
            overall = service.get_overall_readiness(user_id)
            coverage = service.get_curriculum_coverage(user_id)
            backlog = service.get_review_backlog(user_id)
            # EP-001.1: pass-through streak facts for Twin Foundation
            # (Runtime A ReadinessService — Twin does not invent streaks).
            current_streak = None
            longest_streak = None
            if hasattr(service, "get_current_streak"):
                current_streak = int(service.get_current_streak(user_id) or 0)
            if hasattr(service, "get_longest_streak"):
                longest_streak = int(service.get_longest_streak(user_id) or 0)
            payload = {
                "overall": dict(overall or {}),
                "coverage": dict(coverage or {}),
                "review_backlog": dict(backlog or {}),
                "streaks": {
                    "current_streak": current_streak,
                    "longest_streak": longest_streak,
                },
                "current_streak": current_streak,
                "longest_streak": longest_streak,
            }
            return CollectorResult(
                available=True,
                payload=payload,
                source_service=self.SOURCE_SERVICE,
                source_entity=self.SOURCE_ENTITY,
            )
        except Exception as exc:  # noqa: BLE001
            logger.debug(
                "readiness collect failed user_id=%s", user_id, exc_info=True
            )
            return CollectorResult(
                available=False,
                payload={},
                source_service=self.SOURCE_SERVICE,
                source_entity=self.SOURCE_ENTITY,
                unavailable_reason=f"{REASON_COLLECTOR_ERROR}:{type(exc).__name__}",
            )

    def _resolve_service(self) -> Any:
        if self._readiness_service is not None:
            return self._readiness_service
        from app.services.readiness_service import ReadinessService

        return ReadinessService


class CurriculumCollector:
    """Collect ordered curriculum leaves for the active plan syllabus."""

    field_name = "curriculum"
    SOURCE_SERVICE = "curriculum_service"
    SOURCE_ENTITY = "Curriculum"

    def __init__(
        self,
        *,
        curriculum_service: Any | None = None,
        study_plan_model: Any | None = None,
    ) -> None:
        self._curriculum_service = curriculum_service
        self._study_plan_model = study_plan_model

    def collect(
        self,
        user_id: int,
        *,
        as_of: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> CollectorResult:
        _ = as_of
        context = context or {}
        try:
            plan = context.get("active_plan")
            if plan is None:
                plan = read_active_study_plan(
                    user_id, study_plan_model=self._study_plan_model
                )
            if plan is None:
                return CollectorResult(
                    available=False,
                    payload={},
                    source_service=self.SOURCE_SERVICE,
                    source_entity=self.SOURCE_ENTITY,
                    unavailable_reason=REASON_NO_ACTIVE_PLAN,
                )
            curriculum_id = getattr(plan, "curriculum_id", None)
            if not curriculum_id:
                return CollectorResult(
                    available=False,
                    payload={},
                    source_service=self.SOURCE_SERVICE,
                    source_entity=self.SOURCE_ENTITY,
                    unavailable_reason=REASON_NO_CURRICULUM,
                )
            curriculum_service = self._resolve_curriculum_service()
            curriculum = curriculum_service.get_curriculum_by_id(curriculum_id)
            if curriculum is None:
                return CollectorResult(
                    available=False,
                    payload={},
                    source_service=self.SOURCE_SERVICE,
                    source_entity=self.SOURCE_ENTITY,
                    unavailable_reason=REASON_NOT_FOUND,
                )
            topics = curriculum_service.get_all_topics_ordered(curriculum)
            leaves: list[dict[str, Any]] = []
            for topic in topics:
                leaves.append(
                    {
                        "topic_id": str(topic.id),
                        "topic_name": str(topic.name or ""),
                        "order": int(getattr(topic, "order", 0) or 0),
                        "parent_topic_id": (
                            None
                            if topic.parent_topic_id is None
                            else str(topic.parent_topic_id)
                        ),
                        "section_id": (
                            None
                            if getattr(topic, "section_id", None) is None
                            else str(topic.section_id)
                        ),
                        "active": bool(getattr(topic, "active", True)),
                    }
                )
            return CollectorResult(
                available=True,
                payload={
                    "curriculum_id": str(curriculum.id),
                    "exam_name": str(curriculum.exam_name or ""),
                    "version": str(curriculum.version or ""),
                    "leaves": leaves,
                    "leaf_count": len(leaves),
                },
                source_service=self.SOURCE_SERVICE,
                source_entity=self.SOURCE_ENTITY,
            )
        except Exception as exc:  # noqa: BLE001
            logger.debug(
                "curriculum collect failed user_id=%s", user_id, exc_info=True
            )
            return CollectorResult(
                available=False,
                payload={},
                source_service=self.SOURCE_SERVICE,
                source_entity=self.SOURCE_ENTITY,
                unavailable_reason=f"{REASON_COLLECTOR_ERROR}:{type(exc).__name__}",
            )

    def _resolve_curriculum_service(self) -> Any:
        if self._curriculum_service is not None:
            return self._curriculum_service
        from app.services.curriculum_service import CurriculumService

        return CurriculumService


class StudentGoalsCollector:
    """Collect student goals from active StudyPlan (read-only)."""

    field_name = "student_goals"
    SOURCE_SERVICE = "study_plan_service"
    SOURCE_ENTITY = "StudyPlan"

    def __init__(self, *, study_plan_model: Any | None = None) -> None:
        self._study_plan_model = study_plan_model

    def collect(
        self,
        user_id: int,
        *,
        as_of: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> CollectorResult:
        _ = as_of
        context = context or {}
        try:
            plan = context.get("active_plan")
            if plan is None:
                plan = read_active_study_plan(
                    user_id, study_plan_model=self._study_plan_model
                )
            if plan is None:
                return CollectorResult(
                    available=False,
                    payload={},
                    source_service=self.SOURCE_SERVICE,
                    source_entity=self.SOURCE_ENTITY,
                    unavailable_reason=REASON_NO_ACTIVE_PLAN,
                )
            payload = {
                "study_plan_id": str(plan.id),
                "exam_name": str(plan.exam_name or ""),
                "exam_sitting": str(plan.exam_sitting or ""),
                "exam_date": _iso_date(plan.exam_date),
                "weekday_study_minutes": int(plan.weekday_study_minutes or 0),
                "weekend_study_minutes": int(plan.weekend_study_minutes or 0),
                "preferred_session_minutes": int(
                    plan.preferred_session_minutes or 0
                ),
                "current_stage": str(plan.current_stage or ""),
                "study_preference": str(plan.study_preference or ""),
                "target_grade": str(plan.target_grade or ""),
                "curriculum_id": (
                    None
                    if plan.curriculum_id is None
                    else str(plan.curriculum_id)
                ),
                "curriculum_version": plan.curriculum_version or "",
                "curriculum_topic_code": plan.curriculum_topic_code or "",
                "revision_entered_at": _iso_datetime(plan.revision_entered_at),
                "revision_acknowledged": bool(plan.revision_acknowledged),
            }
            return CollectorResult(
                available=True,
                payload=payload,
                source_service=self.SOURCE_SERVICE,
                source_entity=self.SOURCE_ENTITY,
            )
        except Exception as exc:  # noqa: BLE001
            logger.debug(
                "student_goals collect failed user_id=%s", user_id, exc_info=True
            )
            return CollectorResult(
                available=False,
                payload={},
                source_service=self.SOURCE_SERVICE,
                source_entity=self.SOURCE_ENTITY,
                unavailable_reason=f"{REASON_COLLECTOR_ERROR}:{type(exc).__name__}",
            )


class LifecycleStageCollector:
    """Collect lifecycle stage without writing revision_entered_at.

    Read-only derivation from StudyPlan + CurriculumService progress.
    Does **not** call ``LearningLifecycleService.resolve`` (which may stamp).
    """

    field_name = "lifecycle_stage"
    SOURCE_SERVICE = "learning_lifecycle_service"
    SOURCE_ENTITY = "LifecycleSnapshot"

    STAGE_NOT_STARTED = "not_started"
    STAGE_LEARNING = "learning"
    STAGE_REVISION = "revision"

    def __init__(
        self,
        *,
        study_plan_model: Any | None = None,
        curriculum_service: Any | None = None,
    ) -> None:
        self._study_plan_model = study_plan_model
        self._curriculum_service = curriculum_service

    def collect(
        self,
        user_id: int,
        *,
        as_of: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> CollectorResult:
        _ = as_of
        context = context or {}
        try:
            plan = context.get("active_plan")
            if plan is None:
                plan = read_active_study_plan(
                    user_id, study_plan_model=self._study_plan_model
                )
            if plan is None or not getattr(plan, "curriculum_id", None):
                return CollectorResult(
                    available=True,
                    payload={"stage": self.STAGE_NOT_STARTED},
                    source_service=self.SOURCE_SERVICE,
                    source_entity=self.SOURCE_ENTITY,
                )
            # Prefer already-stamped revision marker (no write).
            if getattr(plan, "revision_entered_at", None) is not None:
                return CollectorResult(
                    available=True,
                    payload={"stage": self.STAGE_REVISION},
                    source_service=self.SOURCE_SERVICE,
                    source_entity=self.SOURCE_ENTITY,
                )
            curriculum_service = self._resolve_curriculum_service()
            curriculum = curriculum_service.get_curriculum_by_id(plan.curriculum_id)
            if curriculum is None:
                return CollectorResult(
                    available=True,
                    payload={"stage": self.STAGE_NOT_STARTED},
                    source_service=self.SOURCE_SERVICE,
                    source_entity=self.SOURCE_ENTITY,
                )
            progress = curriculum_service.get_curriculum_progress(user_id, curriculum)
            total = int(progress.get("total_topics") or 0)
            completed = int(progress.get("completed_topics") or 0)
            if total > 0 and completed >= total:
                stage = self.STAGE_REVISION
            else:
                stage = self.STAGE_LEARNING
            return CollectorResult(
                available=True,
                payload={"stage": stage},
                source_service=self.SOURCE_SERVICE,
                source_entity=self.SOURCE_ENTITY,
            )
        except Exception as exc:  # noqa: BLE001
            logger.debug(
                "lifecycle_stage collect failed user_id=%s", user_id, exc_info=True
            )
            return CollectorResult(
                available=False,
                payload={},
                source_service=self.SOURCE_SERVICE,
                source_entity=self.SOURCE_ENTITY,
                unavailable_reason=f"{REASON_COLLECTOR_ERROR}:{type(exc).__name__}",
            )

    def _resolve_curriculum_service(self) -> Any:
        if self._curriculum_service is not None:
            return self._curriculum_service
        from app.services.curriculum_service import CurriculumService

        return CurriculumService

def build_default_collectors() -> dict[str, RuntimeACollector]:
    """Construct the default Runtime A collector set (ordered field map)."""
    return {
        "evidence": EvidenceCollector(),
        "topic_progress": TopicProgressCollector(),
        "study_attempts": StudyAttemptCollector(),
        "mission": MissionCollector(),
        "readiness": ReadinessCollector(),
        "curriculum": CurriculumCollector(),
        "student_goals": StudentGoalsCollector(),
        "lifecycle_stage": LifecycleStageCollector(),
    }


# Re-export reason constants for callers/tests.
__all__ = [
    "CollectorResult",
    "CurriculumCollector",
    "DEFAULT_ATTEMPT_LIMIT",
    "DEFAULT_MISSION_LIMIT",
    "EvidenceCollector",
    "LifecycleStageCollector",
    "MissionCollector",
    "ReadinessCollector",
    "REASON_COLLECTOR_ERROR",
    "REASON_NO_ACTIVE_PLAN",
    "REASON_NO_CURRICULUM",
    "REASON_NOT_FOUND",
    "REASON_UNAVAILABLE",
    "RuntimeACollector",
    "StudentGoalsCollector",
    "StudyAttemptCollector",
    "TopicProgressCollector",
    "build_default_collectors",
    "parse_as_of_date",
    "read_active_study_plan",
]
