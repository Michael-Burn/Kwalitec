"""Curriculum Engine data models.

Pure-dataclass representations of curriculum data. These are NOT SQLAlchemy
models — they serve as the in-memory, deterministic curriculum structure that
can be serialized, validated and cached independently of the database.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class LearningOutcome:
    """A single, auditable learning outcome within a topic.

    Attributes:
        id: Unique identifier within the topic.
        code: Human-readable code (e.g. ``CS1-2026-1-1-1``).
        description: Full text of the learning outcome.
        suggested_revision_days: Days before exam this outcome should be revised.
    """

    id: str
    code: str
    description: str
    suggested_revision_days: int = 14


@dataclass(frozen=True)
class Topic:
    """A topic node within a curriculum.

    Topics form a flat list keyed by ``id``; the ``prerequisites`` field
    references other topic IDs to express dependencies.  No parent/child
    nesting is stored — ordering and grouping are handled externally.

    Attributes:
        id: Unique identifier within the curriculum (e.g. ``cs1-2026-1``).
        code: Human-readable topic code (e.g. ``CS1‑A``).
        title: Short, display-friendly title.
        description: Extended description of what the topic covers.
        weighting: Percentage contribution to the overall examination.
        estimated_hours: Recommended study hours for this topic.
        difficulty: One of ``foundational``, ``intermediate``, or ``advanced``.
        prerequisites: List of topic IDs that should be studied first.
        learning_outcomes: Ordered list of learning outcomes.
    """

    id: str
    code: str
    title: str
    description: str
    weighting: float = 0.0
    estimated_hours: float = 0.0
    difficulty: str = "intermediate"
    prerequisites: list[str] = field(default_factory=list)
    learning_outcomes: list[LearningOutcome] = field(default_factory=list)

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass(frozen=True)
class Curriculum:
    """A complete, versioned curriculum for a single examination paper.

    Attributes:
        organisation: Examining body (e.g. ``IFoA``).
        examination: Overall qualification (e.g. ``Actuarial Practice``).
        paper: Paper code (e.g. ``CS1``).
        syllabus_version: Syllabus year (e.g. ``2026``).
        effective_from: Date the syllabus becomes active.
        effective_to: Optional date the syllabus is superseded.
        total_weight: Sum of all topic weightings (should ≈ 100).
        estimated_total_hours: Sum of all topic estimated hours.
        topics: Ordered list of topics.
        metadata: Arbitrary key-value metadata for future extensibility.
    """

    organisation: str
    examination: str
    paper: str
    syllabus_version: str
    effective_from: date
    effective_to: Optional[date]
    total_weight: float
    estimated_total_hours: float
    topics: list[Topic] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)

    @property
    def exam_key(self) -> str:
        """Canonical key used for lookups (e.g. ``ifoa/cs1``)."""
        return f"{self.organisation.lower()}/{self.paper.lower()}"

    @property
    def version_key(self) -> str:
        """Fully-qualified version key (e.g. ``ifoa/cs1/2026``)."""
        return f"{self.exam_key}/{self.syllabus_version}"