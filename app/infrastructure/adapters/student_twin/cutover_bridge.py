"""Infrastructure helpers for ADR-027 Phase 2 Twin cutover.

Subject resolution, ORM↔Twin mapping, and LearnerTwinQueryPort access live
here so application/student_twin stays free of models, services, and
infrastructure imports.
"""

from __future__ import annotations

from typing import Any

from app.application.student_twin.canonical_topic_id import CanonicalTopicId
from app.application.student_twin.cutover import ek_display_0_100
from app.application.student_twin.query import TopicKnowledgeFact
from app.infrastructure.adapters.student_twin.query_adapter import (
    DailyLoopLearnerTwinQueryAdapter,
)
from app.models.curriculum import Topic


def learner_twin_query() -> DailyLoopLearnerTwinQueryAdapter:
    """Return the Stage 1 DailyLoop Learner Twin query adapter."""
    return DailyLoopLearnerTwinQueryAdapter()


def subject_code_for_user(user_id: int) -> str | None:
    """Resolve a published subject code for Twin queries.

    Prefers active StudyPlan paper, then latest RuntimeEnrolment subject_code.
    """
    try:
        from app.services.examination_catalogue import parse_exam_name
        from app.services.study_plan_service import StudyPlanService

        plan = StudyPlanService.get_user_active_plan(user_id)
        if plan is not None:
            _org, paper = parse_exam_name(plan.exam_name or "")
            if paper:
                return str(paper).strip().upper()
    except Exception:
        pass

    try:
        from app.models.educational_runtime_engine import RuntimeEnrolment

        enrolment = (
            RuntimeEnrolment.query.filter_by(user_id=user_id)
            .order_by(RuntimeEnrolment.id.desc())
            .first()
        )
        if enrolment is not None:
            code = (enrolment.subject_code or "").strip().upper()
            return code or None
    except Exception:
        pass
    return None


def topic_ek_by_orm_id(
    *,
    user_id: int,
    subject_code: str | None = None,
    topics: list[Any] | tuple[Any, ...] | None = None,
) -> dict[int, TopicKnowledgeFact]:
    """Map ORM topic id -> Twin TopicKnowledgeFact for topics with evidence."""
    code = (subject_code or subject_code_for_user(user_id) or "").strip()
    if not code:
        return {}

    query = learner_twin_query()
    snap = query.knowledge_snapshot(user_id=user_id, subject_code=code)
    if not snap.topics:
        return {}

    if topics is None:
        topics = _orm_topics_for_subject(code)
    if not topics:
        return {}

    canonical = CanonicalTopicId()
    by_published: dict[str, Any] = {}
    for topic in topics:
        published = canonical.resolve_from_orm_topic(topic, subject_code=code)
        if published:
            by_published[published] = topic

    out: dict[int, TopicKnowledgeFact] = {}
    for fact in snap.topics:
        if not fact.has_estimated_knowledge:
            continue
        topic = by_published.get(fact.topic_id)
        if topic is None:
            continue
        orm_id = getattr(topic, "id", None)
        if orm_id is None:
            continue
        out[int(orm_id)] = fact
    return out


def twin_fact_for_orm_topic(
    *,
    user_id: int,
    topic: Any,
    subject_code: str | None = None,
) -> TopicKnowledgeFact | None:
    """Return Twin EK fact for one ORM topic, or None when unresolved / empty."""
    code = (subject_code or subject_code_for_user(user_id) or "").strip()
    if not code or topic is None:
        return None
    published = CanonicalTopicId().resolve_from_orm_topic(topic, subject_code=code)
    if not published:
        return None
    return learner_twin_query().topic_knowledge(
        user_id=user_id, subject_code=code, topic_id=published
    )


def study_plan_progress_display_map(
    *,
    user_id: int,
    topic_progress_rows: list[Any] | tuple[Any, ...],
    topics: list[Any] | tuple[Any, ...] | None = None,
) -> dict[int, Any]:
    """Build ORM-topic-id -> display progress for study_plan/view.html."""
    from types import SimpleNamespace

    code = subject_code_for_user(user_id)
    ek_map = topic_ek_by_orm_id(
        user_id=user_id, subject_code=code, topics=topics
    )

    display: dict[int, Any] = {}
    for row in topic_progress_rows:
        tid = int(row.topic_id)
        fact = ek_map.get(tid)
        score = ek_display_0_100(fact)
        has_ek = bool(fact is not None and fact.has_estimated_knowledge)
        display[tid] = SimpleNamespace(
            topic_id=tid,
            completed=bool(row.completed),
            current_stage=row.current_stage,
            revision_count=row.revision_count,
            mastery_score=score if score is not None else 0.0,
            has_estimated_knowledge=has_ek,
            average_accuracy=(
                round(float(fact.estimated_knowledge) * 100.0, 1)
                if fact is not None and fact.estimated_knowledge is not None
                else None
            ),
        )
    for tid, fact in ek_map.items():
        if tid in display:
            continue
        score = ek_display_0_100(fact)
        display[tid] = SimpleNamespace(
            topic_id=tid,
            completed=False,
            current_stage="Not Started",
            revision_count=0,
            mastery_score=score if score is not None else 0.0,
            has_estimated_knowledge=True,
            average_accuracy=(
                round(float(fact.estimated_knowledge) * 100.0, 1)
                if fact.estimated_knowledge is not None
                else None
            ),
        )
    return display


def _orm_topics_for_subject(subject_code: str) -> list[Topic]:
    code = (subject_code or "").strip().upper()
    if not code:
        return []
    try:
        from app.models.curriculum import Curriculum

        curricula = Curriculum.query.filter(Curriculum.active.is_(True)).all()
        matched: list[Topic] = []
        for curriculum in curricula:
            paper = (getattr(curriculum, "paper", None) or "").strip().upper()
            name = (getattr(curriculum, "name", None) or "").strip().upper()
            if code not in paper and code not in name and paper != code:
                if code not in f"{paper} {name}":
                    continue
            matched.extend(
                Topic.query.filter_by(
                    curriculum_id=curriculum.id, active=True
                ).all()
            )
        return matched
    except Exception:
        return []


__all__ = [
    "learner_twin_query",
    "study_plan_progress_display_map",
    "subject_code_for_user",
    "topic_ek_by_orm_id",
    "twin_fact_for_orm_topic",
]
