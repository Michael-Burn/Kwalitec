"""Deterministic progress derivation from educational events + progress model.

Does not invent curriculum structure. Topic order and membership come from the
published progress model (PI-001B).

Study Progress ownership (canonical): the Runtime C immutable event stream.
Coverage here is a plain historical fact about the learning loop, not Estimated
Knowledge, mastery, or evidence density.

Event roles:
- TOPIC_COMPLETED (non-baseline): Kwalitec-verified coverage (product recorded
  an authorised completion). Historical encounter/completion fact only.
- PRIOR_KNOWLEDGE_CLAIM: self-declared prior knowledge. Influences journey
  position (continue-from) but is never verified coverage.
- Legacy TOPIC_COMPLETED with baseline_self_declared / thin_self_declared
  payload: reclassified as prior-knowledge claims on read (no history rewrite).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.domain.educational_runtime_engine.events import (
    EducationalEventRecord,
    EducationalEventType,
)
from app.domain.educational_runtime_engine.state import (
    JourneyStage,
    next_journey_stage,
)

# Payload markers used by historical baseline seeds that wrote TOPIC_COMPLETED.
_BASELINE_SOURCES = frozenset({"baseline_self_declared"})
_BASELINE_WARRANTS = frozenset({"thin_self_declared"})


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
    """Derived Study Progress from the Runtime C event stream.

    ``completed_topic_ids`` aliases ``progressed_topic_ids`` this increment for
    back-compat (mission composition, Honest Progress numbers). It means
    progressed-past, not Kwalitec-verified coverage. Prefer
    ``verified_completed_topic_ids`` / ``prior_knowledge_claimed_topic_ids``
    when the distinction matters.
    """

    curriculum_identity: str
    topic_ids: tuple[str, ...]
    completed_topic_ids: tuple[str, ...]
    incomplete_topic_ids: tuple[str, ...]
    current_topic_id: str | None
    coverage_ratio: float
    journey_stage: JourneyStage
    syllabus_complete: bool
    verified_completed_topic_ids: tuple[str, ...] = ()
    prior_knowledge_claimed_topic_ids: tuple[str, ...] = ()
    progressed_topic_ids: tuple[str, ...] = ()
    verified_coverage_ratio: float = 0.0


def is_legacy_baseline_topic_completed(event: EducationalEventRecord) -> bool:
    """True when a TOPIC_COMPLETED row is a historical baseline self-declaration."""
    if event.event_type != EducationalEventType.TOPIC_COMPLETED:
        return False
    payload: dict[str, Any] = event.payload or {}
    source = str(payload.get("source") or "").strip()
    warrant = str(payload.get("warrant") or "").strip()
    return source in _BASELINE_SOURCES or warrant in _BASELINE_WARRANTS


def derive_progress(
    progress_model: ProgressModelSpec,
    events: tuple[EducationalEventRecord, ...] | list[EducationalEventRecord],
) -> DerivedProgress:
    """Derive student progress from immutable events and published structure.

    Verified coverage and prior-knowledge claims are classified separately.
    Journey position (current_topic_id) uses the progressed-past union so
    continue-from still works without treating claims as verified coverage.
    """
    topic_ids = tuple(progress_model.topic_ids)
    topic_id_set = set(topic_ids)
    topic_specs = {
        topic.topic_id: topic
        for topic in progress_model.topics
    }
    verified: set[str] = set()
    claimed: set[str] = set()
    for event in events:
        tid = (event.topic_id or "").strip()
        if not tid or tid not in topic_id_set:
            continue
        if event.event_type == EducationalEventType.PRIOR_KNOWLEDGE_CLAIM:
            claimed.add(tid)
        elif event.event_type == EducationalEventType.TOPIC_COMPLETED:
            if is_legacy_baseline_topic_completed(event):
                claimed.add(tid)
            else:
                verified.add(tid)

    progressed = verified | claimed
    progressed_ordered = tuple(tid for tid in topic_ids if tid in progressed)
    verified_ordered = tuple(tid for tid in topic_ids if tid in verified)
    claimed_ordered = tuple(tid for tid in topic_ids if tid in claimed)
    incomplete_ordered = tuple(tid for tid in topic_ids if tid not in progressed)
    current = _next_eligible_topic(incomplete_ordered, progressed, topic_specs)
    total = len(topic_ids)
    coverage = (len(progressed_ordered) / total) if total else 0.0
    verified_coverage = (len(verified_ordered) / total) if total else 0.0
    stage = next_journey_stage(
        completed_topic_count=len(progressed_ordered),
        total_topic_count=total,
    )
    syllabus_complete = stage == JourneyStage.SYLLABUS_COMPLETE
    return DerivedProgress(
        curriculum_identity=progress_model.curriculum_identity,
        topic_ids=topic_ids,
        completed_topic_ids=progressed_ordered,
        incomplete_topic_ids=incomplete_ordered,
        current_topic_id=None if syllabus_complete else current,
        coverage_ratio=coverage,
        journey_stage=stage,
        syllabus_complete=syllabus_complete,
        verified_completed_topic_ids=verified_ordered,
        prior_knowledge_claimed_topic_ids=claimed_ordered,
        progressed_topic_ids=progressed_ordered,
        verified_coverage_ratio=verified_coverage,
    )


def _next_eligible_topic(
    incomplete_ordered: tuple[str, ...],
    progressed: set[str],
    topic_specs: dict[str, ProgressTopicSpec],
) -> str | None:
    for topic_id in incomplete_ordered:
        spec = topic_specs.get(topic_id)
        prereqs = spec.prerequisite_ids if spec is not None else ()
        if all(prereq in progressed for prereq in prereqs):
            return topic_id
    return incomplete_ordered[0] if incomplete_ordered else None
