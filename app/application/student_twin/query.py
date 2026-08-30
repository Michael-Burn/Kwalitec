"""Learner Twin Query Port (ADR-027 Phase 2 Stage 1).

Read-only questions about Estimated Knowledge and Study Progress coverage.
The Twin answers facts; it does not rank, weigh, prioritise, or recommend.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class TopicKnowledgeFact:
    """Per-topic Estimated Knowledge fact from the canonical Learner Twin."""

    topic_id: str
    has_estimated_knowledge: bool
    estimated_knowledge: float | None
    estimated_mastery: float | None
    evidence_count: int
    last_practised_at: datetime | None


@dataclass(frozen=True)
class LearnerKnowledgeSnapshot:
    """Subject-scoped Estimated Knowledge snapshot for one learner."""

    user_id: int
    subject_code: str
    curriculum_identity: str | None
    overall_estimated_knowledge: float | None
    topics: tuple[TopicKnowledgeFact, ...]


class LearnerTwinQueryPort(Protocol):
    """Narrow read-only Twin query surface (ADR-027 section 4.2)."""

    def knowledge_snapshot(
        self, *, user_id: int, subject_code: str
    ) -> LearnerKnowledgeSnapshot:
        """Return the full Estimated Knowledge snapshot for a learner/subject."""
        ...

    def topic_knowledge(
        self, *, user_id: int, subject_code: str, topic_id: str
    ) -> TopicKnowledgeFact:
        """Return Estimated Knowledge for one canonical topic id."""
        ...

    def topics_with_estimated_knowledge(
        self, *, user_id: int, subject_code: str
    ) -> tuple[TopicKnowledgeFact, ...]:
        """Return only topics that have Twin-admitted Estimated Knowledge."""
        ...

    def topic_covered(
        self, *, user_id: int, subject_code: str, topic_id: str
    ) -> bool:
        """Return Study Progress coverage (not Estimated Knowledge)."""
        ...


class StudyProgressPort(Protocol):
    """Study Progress coverage reader (Stack D). Never mints Estimated Knowledge."""

    def topic_covered(
        self, *, user_id: int, subject_code: str, topic_id: str
    ) -> bool:
        """True when Study Progress sources mark the topic covered."""
        ...


class AlwaysUncoveredStudyProgress:
    """Study Progress stub that never reports coverage (tests / empty default)."""

    def topic_covered(
        self, *, user_id: int, subject_code: str, topic_id: str
    ) -> bool:
        return False


class MapStudyProgress:
    """In-memory Study Progress map for isolated tests."""

    def __init__(self, covered: set[str] | frozenset[str] | None = None) -> None:
        self._covered = frozenset(covered or ())

    def topic_covered(
        self, *, user_id: int, subject_code: str, topic_id: str
    ) -> bool:
        return (topic_id or "").strip() in self._covered
