"""Deterministic progress derivation from educational events + progress model.

Does not invent curriculum structure. Topic order and membership come from the
published progress model (PI-001B). Completion comes only from TOPIC_COMPLETED
events in the immutable event stream.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.educational_runtime_engine.events import (
    EducationalEventRecord,
    EducationalEventType,
)
from app.domain.educational_runtime_engine.state import (
    JourneyStage,
    next_journey_stage,
)


@dataclass(frozen=True)
class ProgressTopicSpec:
    topic_id: str
    topic_code: str = ""
    objective_ids: tuple[str, ...] = field(default_factory=tuple)
    prerequisite_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ProgressModelSpec:
    """Structural progress model derived from published curriculum."""

    curriculum_identity: str
    topic_ids: tuple[str, ...]
    topics: tuple[ProgressTopicSpec, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class DerivedProgress:
    curriculum_identity: str
    topic_ids: tuple[str, ...]
    completed_topic_ids: tuple[str, ...]
    incomplete_topic_ids: tuple[str, ...]
    current_topic_id: str | None
    coverage_ratio: float
    journey_stage: JourneyStage
    syllabus_complete: bool


def derive_progress(
    progress_model: ProgressModelSpec,
    events: tuple[EducationalEventRecord, ...] | list[EducationalEventRecord],
) -> DerivedProgress:
    """Derive student progress from immutable events and published structure."""
    topic_ids = tuple(progress_model.topic_ids)
    topic_specs = {
        topic.topic_id: topic
        for topic in progress_model.topics
    }
    completed: set[str] = set()
    for event in events:
        if event.event_type != EducationalEventType.TOPIC_COMPLETED:
            continue
        if event.topic_id and event.topic_id in topic_ids:
            completed.add(event.topic_id)

    completed_ordered = tuple(tid for tid in topic_ids if tid in completed)
    incomplete_ordered = tuple(tid for tid in topic_ids if tid not in completed)
    current = _next_eligible_topic(incomplete_ordered, completed, topic_specs)
    total = len(topic_ids)
    coverage = (len(completed_ordered) / total) if total else 0.0
    stage = next_journey_stage(
        completed_topic_count=len(completed_ordered),
        total_topic_count=total,
    )
    syllabus_complete = stage == JourneyStage.SYLLABUS_COMPLETE
    return DerivedProgress(
        curriculum_identity=progress_model.curriculum_identity,
        topic_ids=topic_ids,
        completed_topic_ids=completed_ordered,
        incomplete_topic_ids=incomplete_ordered,
        current_topic_id=None if syllabus_complete else current,
        coverage_ratio=coverage,
        journey_stage=stage,
        syllabus_complete=syllabus_complete,
    )


def _next_eligible_topic(
    incomplete_ordered: tuple[str, ...],
    completed: set[str],
    topic_specs: dict[str, ProgressTopicSpec],
) -> str | None:
    for topic_id in incomplete_ordered:
        spec = topic_specs.get(topic_id)
        prereqs = spec.prerequisite_ids if spec is not None else ()
        if all(prereq in completed for prereq in prereqs):
            return topic_id
    return incomplete_ordered[0] if incomplete_ordered else None
