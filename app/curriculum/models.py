"""Curriculum Engine data models.

Pure-dataclass representations of curriculum data. These are NOT SQLAlchemy
models — they serve as the in-memory, deterministic curriculum structure that
can be serialized, validated and cached independently of the database.

Supports both V1 (flat) and V2 (hierarchical) formats.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

# ═══════════════════════════════════════════════════════════════════════════════
# V2 Canonical Format Models
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class LearningObjectiveDefinition:
    """A single, measurable learning objective within a topic (V2 format).

    Attributes:
        id: Stable identifier (e.g. ``CS1-A-T01-LO01``).
        topic_id: Parent topic identifier.
        code: Official syllabus code (e.g. ``2.1.1``).
        description: Full text of the learning objective.
        cognitive_level: Bloom's taxonomy level (remember, understand, apply, etc.).
        estimated_minutes: Estimated study time in minutes.
        learning_type: Type of learning outcome (concept, procedure, etc.).
        display_order: Sequential order within topic (1-based).
        metadata: Optional non-hierarchical metadata (syllabus_code, difficulty, etc.).
    """

    id: str
    topic_id: str
    code: str
    description: str
    cognitive_level: str
    estimated_minutes: int
    learning_type: str
    display_order: int = 1
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class TopicDefinition:
    """A topic node within a section (V2 format).

    Attributes:
        id: Stable identifier (e.g. ``CS1-A-T01``).
        section_id: Parent section identifier.
        code: Human-readable topic code (e.g. ``CS1-A.1``).
        title: Short, display-friendly title.
        description: Extended description of what the topic covers.
        estimated_minutes: Recommended study time in minutes.
        difficulty: One of ``foundational``, ``intermediate``, or ``advanced``.
        display_order: Sequential order within section (1-based).
        learning_objectives: Ordered list of learning objectives.
    """

    id: str
    section_id: str
    code: str
    title: str
    description: str
    estimated_minutes: int
    difficulty: str
    display_order: int = 1
    learning_objectives: list[LearningObjectiveDefinition] = field(default_factory=list)

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass(frozen=True)
class SectionDefinition:
    """A section node within a curriculum (V2 format).

    Attributes:
        id: Stable section identifier (e.g. ``CS1-A``).
        code: Official section code (e.g. ``CS1-A``).
        title: Section title.
        description: Detailed section description.
        exam_weight: Assessment weighting percentage (0-100).
        estimated_hours: Recommended study hours for this section.
        difficulty: Overall section difficulty level.
        display_order: Sequential display order (1-based).
        topics: Ordered list of topics.
    """

    id: str
    code: str
    title: str
    description: str
    exam_weight: float
    estimated_hours: float
    difficulty: str
    display_order: int = 1
    topics: list[TopicDefinition] = field(default_factory=list)

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass(frozen=True)
class CurriculumDefinition:
    """A complete, versioned curriculum in V2 canonical format.

    Attributes:
        exam_code: Unique exam identifier (e.g. ``CS1``).
        exam_name: Full examination name (e.g. ``Actuarial Statistics``).
        provider: Examining body (e.g. ``IFoA``).
        version: Syllabus version year (e.g. ``2026``).
        effective_date: Date the syllabus becomes active.
        superseded_date: Optional date the syllabus is superseded.
        total_estimated_hours: Total recommended study hours for entire exam.
        description: Overall exam description and objectives.
        sections: Ordered list of sections.
        metadata: Arbitrary key-value metadata for future extensibility.
    """

    exam_code: str
    exam_name: str
    provider: str
    version: str
    effective_date: date
    superseded_date: date | None
    total_estimated_hours: float
    description: str
    sections: list[SectionDefinition] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)

    @property
    def exam_key(self) -> str:
        """Canonical key used for lookups (e.g. ``ifoa/cs1``)."""
        return f"{self.provider.lower()}/{self.exam_code.lower()}"

    @property
    def version_key(self) -> str:
        """Fully-qualified version key (e.g. ``ifoa/cs1/2026``)."""
        return f"{self.exam_key}/{self.version}"


# ═══════════════════════════════════════════════════════════════════════════════
# V1 Legacy Format Models (preserved for backwards compatibility)
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class LearningOutcome:
    """A single, auditable learning outcome within a topic (V1 format).

    Attributes:
        id: Unique identifier within the topic.
        code: Human-readable code (e.g. ``CS1-A-1``).
        description: Full text of the learning outcome.
        suggested_revision_days: Days before exam this outcome should be revised.
    """

    id: str
    code: str
    description: str
    suggested_revision_days: int = 14


@dataclass(frozen=True)
class Topic:
    """A topic node within a curriculum (V1 format).

    Topics form a flat list keyed by ``id``; the ``prerequisites`` field
    references other topic IDs to express dependencies.

    Attributes:
        id: Unique identifier within the curriculum (e.g. ``cs1-2026-1``).
        code: Human-readable topic code (e.g. ``CS1-A``).
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
    """A complete, versioned curriculum for a single examination paper (V1 format).

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
    effective_to: date | None
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
