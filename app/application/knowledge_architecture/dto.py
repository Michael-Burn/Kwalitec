"""Knowledge Architecture DTOs (KWP-014).

Immutable projections over curriculum structure. Educational Intelligence
consumes these; this layer never authors Evidence, Progress, Strategy,
Diagnostics, Difficulty, Effectiveness, Memory, Forecast, Twin, or Mission.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class EducationalRelationship(StrEnum):
    """Student-facing educational relationship labels (map onto DependencyType)."""

    PREREQUISITE = "prerequisite"
    FOUNDATION = "foundation"
    EXTENSION = "extension"
    FREQUENTLY_REVISED_TOGETHER = "frequently_revised_together"
    HIGH_DEPENDENCY = "high_dependency"
    OPTIONAL_REINFORCEMENT = "optional_reinforcement"


class RevisionPathKind(StrEnum):
    """Deterministic revision pathway kinds."""

    WEAK_PREREQUISITE = "weak_prerequisite"
    RECOVERY = "recovery"
    EXAM_REVISION = "exam_revision"
    MASTERY_REINFORCEMENT = "mastery_reinforcement"


class MapTopicStatus(StrEnum):
    """Curriculum Map highlight status for one topic."""

    COMPLETED = "completed"
    CURRENT = "current"
    FUTURE = "future"
    WEAK_PREREQUISITE = "weak_prerequisite"
    ATTENTION = "attention"


RELATIONSHIP_TITLES: dict[EducationalRelationship, str] = {
    EducationalRelationship.PREREQUISITE: "Prerequisite",
    EducationalRelationship.FOUNDATION: "Foundation",
    EducationalRelationship.EXTENSION: "Extension",
    EducationalRelationship.FREQUENTLY_REVISED_TOGETHER: (
        "Frequently revised together"
    ),
    EducationalRelationship.HIGH_DEPENDENCY: "High dependency",
    EducationalRelationship.OPTIONAL_REINFORCEMENT: "Optional reinforcement",
}

REVISION_PATH_TITLES: dict[RevisionPathKind, str] = {
    RevisionPathKind.WEAK_PREREQUISITE: "Weak prerequisite path",
    RevisionPathKind.RECOVERY: "Recovery path",
    RevisionPathKind.EXAM_REVISION: "Exam revision path",
    RevisionPathKind.MASTERY_REINFORCEMENT: "Mastery reinforcement path",
}

MAP_STATUS_TITLES: dict[MapTopicStatus, str] = {
    MapTopicStatus.COMPLETED: "Completed",
    MapTopicStatus.CURRENT: "Current",
    MapTopicStatus.FUTURE: "Future",
    MapTopicStatus.WEAK_PREREQUISITE: "Weak prerequisite",
    MapTopicStatus.ATTENTION: "Needs attention",
}


@dataclass(frozen=True)
class TopicNodeView:
    """Curriculum topic as a knowledge-graph node (no duplicated metadata)."""

    topic_id: str
    title: str
    difficulty: str = "foundational"
    estimated_minutes: int = 0
    prerequisite_ids: tuple[str, ...] = ()
    successor_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class TopicEdgeView:
    """Directed educational relationship between two topics."""

    from_topic_id: str
    to_topic_id: str
    relationship: EducationalRelationship
    rationale: str = ""

    @property
    def title(self) -> str:
        return RELATIONSHIP_TITLES[self.relationship]


@dataclass(frozen=True)
class PrerequisiteExplanation:
    """Explain why a topic matters via explicit curriculum relationships."""

    topic_id: str
    topic_title: str
    explanation: str
    relies_on: tuple[str, ...] = ()
    strengthens: tuple[str, ...] = ()
    relationship_codes: tuple[str, ...] = ()
    has_explanation: bool = False


@dataclass(frozen=True)
class CurriculumPathway:
    """Ordered educational path through curriculum topics (no AI)."""

    path_id: str
    name: str
    topic_ids: tuple[str, ...] = ()
    topic_titles: tuple[str, ...] = ()
    description: str = ""

    @property
    def length(self) -> int:
        return len(self.topic_ids)


@dataclass(frozen=True)
class RevisionPathway:
    """Deterministic revision path derived from graph + EI signals."""

    kind: RevisionPathKind
    title: str
    topic_ids: tuple[str, ...] = ()
    topic_titles: tuple[str, ...] = ()
    rationale: str = ""
    seed_topic_id: str = ""
    evidence_codes: tuple[str, ...] = ()

    @property
    def has_path(self) -> bool:
        return len(self.topic_ids) > 0


@dataclass(frozen=True)
class DifficultyAttention:
    """Difficulty propagation: weak foundation → successor attention."""

    source_topic_id: str
    source_title: str
    attention_topic_ids: tuple[str, ...] = ()
    attention_titles: tuple[str, ...] = ()
    guidance: str = ""
    has_attention: bool = False


@dataclass(frozen=True)
class CurriculumMapNode:
    """One topic on the student Curriculum Map."""

    topic_id: str
    title: str
    status: MapTopicStatus
    status_label: str
    difficulty: str = ""
    prerequisite_titles: tuple[str, ...] = ()
    is_current: bool = False


@dataclass(frozen=True)
class CurriculumMap:
    """Visual learning map — where today's topic sits in the qualification."""

    subject_label: str = ""
    current_topic_id: str = ""
    current_topic_title: str = ""
    nodes: tuple[CurriculumMapNode, ...] = ()
    pathway: CurriculumPathway | None = None
    why_current_matters: str = ""
    node_count: int = 0
    edge_count: int = 0
    has_map: bool = False
    empty_reason: str = ""


@dataclass(frozen=True)
class KnowledgeArchitectureSnapshot:
    """Founder / continuity opaque for knowledge-architecture usage."""

    subject_label: str = ""
    node_count: int = 0
    edge_count: int = 0
    prerequisite_edge_count: int = 0
    revision_edge_count: int = 0
    pathway_count: int = 0
    revision_paths_generated: int = 0
    completeness_ratio: float = 0.0
    bottleneck_topic_ids: tuple[str, ...] = ()
    common_recovery_path_ids: tuple[str, ...] = ()

    def to_opaque(self) -> dict[str, Any]:
        return {
            "subject_label": self.subject_label,
            "node_count": self.node_count,
            "edge_count": self.edge_count,
            "prerequisite_edge_count": self.prerequisite_edge_count,
            "revision_edge_count": self.revision_edge_count,
            "pathway_count": self.pathway_count,
            "revision_paths_generated": self.revision_paths_generated,
            "completeness_ratio": round(self.completeness_ratio, 4),
            "bottleneck_topic_ids": list(self.bottleneck_topic_ids),
            "common_recovery_path_ids": list(self.common_recovery_path_ids),
        }


@dataclass(frozen=True)
class LearnerGraphContext:
    """Learner state overlays used with curriculum structure (not ownership)."""

    completed_topic_ids: frozenset[str] = field(default_factory=frozenset)
    weak_topic_ids: frozenset[str] = field(default_factory=frozenset)
    current_topic_id: str = ""
    recently_strengthened_ids: frozenset[str] = field(default_factory=frozenset)
    days_to_exam: int | None = None
