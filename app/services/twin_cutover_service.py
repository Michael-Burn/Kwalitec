"""Service facade for ADR-027 Phase 2 Twin cutover readers.

Keeps ``app.application`` free of infrastructure imports while Stage A /
Runtime C consumers resolve Twin Estimated Knowledge.
"""

from __future__ import annotations

from typing import Any

from app.application.student_twin.cutover import (
    ek_display_0_100,
    phase2_twin_cutover_enabled,
)
from app.application.student_twin.query import TopicKnowledgeFact
from app.infrastructure.adapters.student_twin import cutover_bridge


def is_cutover_enabled() -> bool:
    return phase2_twin_cutover_enabled()


def display_ek_0_100(fact: TopicKnowledgeFact | None) -> float | None:
    return ek_display_0_100(fact)


def learner_twin_query():
    return cutover_bridge.learner_twin_query()


def subject_code_for_user(user_id: int) -> str | None:
    return cutover_bridge.subject_code_for_user(user_id)


def topic_ek_by_orm_id(
    *,
    user_id: int,
    subject_code: str | None = None,
    topics: list[Any] | tuple[Any, ...] | None = None,
) -> dict[int, TopicKnowledgeFact]:
    return cutover_bridge.topic_ek_by_orm_id(
        user_id=user_id, subject_code=subject_code, topics=topics
    )


def twin_fact_for_orm_topic(
    *,
    user_id: int,
    topic: Any,
    subject_code: str | None = None,
) -> TopicKnowledgeFact | None:
    return cutover_bridge.twin_fact_for_orm_topic(
        user_id=user_id, topic=topic, subject_code=subject_code
    )


def study_plan_progress_display_map(
    *,
    user_id: int,
    topic_progress_rows: list[Any] | tuple[Any, ...],
    topics: list[Any] | tuple[Any, ...] | None = None,
) -> dict[int, Any]:
    return cutover_bridge.study_plan_progress_display_map(
        user_id=user_id,
        topic_progress_rows=topic_progress_rows,
        topics=topics,
    )
