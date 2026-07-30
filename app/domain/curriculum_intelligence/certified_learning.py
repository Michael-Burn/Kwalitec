"""EI-002B — Certified Learning Experience domain contracts.

Student Twin / Mission / Tutor / Progress consume published certified
curriculum only. These types carry no educational reasoning of their own —
they bind existing student engines to stable certified node identifiers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class CertifiedNodeKind(StrEnum):
    """Learner-facing hierarchy levels tied to certified EducationalNode kinds."""

    SUBJECT = "subject"
    CHAPTER = "chapter"
    SECTION = "section"
    TOPIC = "topic"
    CONCEPT = "concept"
    LEARNING_OBJECTIVE = "learning_objective"


class MissionSelectionReason(StrEnum):
    """Explainable reason a certified LO / topic was selected for a mission."""

    NEXT_UNCOVERED_OBJECTIVE = "next_uncovered_objective"
    PREREQUISITE_READY = "prerequisite_ready"
    DIFFICULTY_MATCH = "difficulty_match"
    CALIBRATION_BIAS = "calibration_bias"
    REVISION_PRIORITY = "revision_priority"
    PROGRESS_ADVANCE = "progress_advance"


@dataclass(frozen=True)
class CurriculumProvenanceRef:
    """Provenance of the certified curriculum powering a student artefact."""

    chain_id: str = ""
    snapshot_id: str = ""
    authority: str = ""
    status: str = ""
    subject_code: str = ""
    version_label: str = ""
    curriculum_identity: str = ""

    @property
    def is_certified(self) -> bool:
        auth = (self.authority or "").strip().lower()
        status = (self.status or "").strip().lower()
        if auth in {"certified_snapshot", ""} and status in {
            "certified",
            "certified_with_warnings",
            "",
        }:
            return bool(self.snapshot_id or self.chain_id or status)
        return status in {"certified", "certified_with_warnings"}


@dataclass(frozen=True)
class LearnerGraphNode:
    """One learner-facing node projected from a certified EducationalNode."""

    node_id: str
    title: str
    kind: CertifiedNodeKind
    parent_node_id: str | None = None
    difficulty: str = ""
    estimated_minutes: int = 0
    objective_ids: tuple[str, ...] = ()
    prerequisite_ids: tuple[str, ...] = ()
    attributes: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class LearnerGraphEdge:
    """Directed relationship in the learner-facing certified knowledge graph."""

    edge_id: str
    relation: str
    from_node_id: str
    to_node_id: str


@dataclass(frozen=True)
class LearnerKnowledgeGraph:
    """Learner-facing graph constructed exclusively from certified nodes."""

    curriculum_identity: str
    provenance: CurriculumProvenanceRef
    nodes: tuple[LearnerGraphNode, ...]
    edges: tuple[LearnerGraphEdge, ...] = ()

    def node(self, node_id: str) -> LearnerGraphNode | None:
        for n in self.nodes:
            if n.node_id == node_id:
                return n
        return None

    def prerequisites(self, node_id: str) -> tuple[str, ...]:
        return tuple(
            e.to_node_id
            for e in self.edges
            if e.from_node_id == node_id
            and e.relation in {"requires", "depends_on", "prerequisite"}
        )

    def children(self, node_id: str) -> tuple[str, ...]:
        return tuple(
            e.to_node_id
            for e in self.edges
            if e.from_node_id == node_id and e.relation in {"parent_of", "contains"}
        )

    def objectives(self) -> tuple[LearnerGraphNode, ...]:
        return tuple(
            n for n in self.nodes if n.kind is CertifiedNodeKind.LEARNING_OBJECTIVE
        )

    def topics(self) -> tuple[LearnerGraphNode, ...]:
        return tuple(
            n
            for n in self.nodes
            if n.kind in {CertifiedNodeKind.TOPIC, CertifiedNodeKind.CONCEPT}
        )


@dataclass(frozen=True)
class CertifiedMissionSpec:
    """Daily Mission generated exclusively from certified Learning Objectives."""

    mission_id: str
    curriculum_identity: str
    topic_id: str
    topic_title: str
    objective_ids: tuple[str, ...]
    objective_titles: tuple[str, ...]
    prerequisite_ids: tuple[str, ...]
    estimated_minutes: int
    difficulty: str
    selection_reasons: tuple[MissionSelectionReason, ...]
    provenance: CurriculumProvenanceRef
    task_descriptions: tuple[str, ...] = ()
    calibration_notes: tuple[str, ...] = ()
    coverage_ratio_before: float = 0.0


@dataclass(frozen=True)
class CertifiedTutorContext:
    """Tutor context constrained to certified curriculum nodes."""

    context_id: str
    curriculum_identity: str
    primary_node_id: str
    allowed_node_ids: tuple[str, ...]
    excerpts: tuple[tuple[str, str], ...]  # (node_id, text)
    prerequisite_ids: tuple[str, ...]
    related_node_ids: tuple[str, ...]
    provenance: CurriculumProvenanceRef
    rejected_foreign_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class NodeMasteryRecord:
    """Mastery at one certified node (stable across curriculum revisions)."""

    node_id: str
    kind: CertifiedNodeKind
    mastery: float
    coverage: float
    attempts: int = 0
    last_event: str = ""


@dataclass(frozen=True)
class CertifiedProgressSnapshot:
    """Progress tracked against certified node identifiers."""

    curriculum_identity: str
    provenance: CurriculumProvenanceRef
    subject_mastery: float
    chapter_records: tuple[NodeMasteryRecord, ...] = ()
    topic_records: tuple[NodeMasteryRecord, ...] = ()
    objective_records: tuple[NodeMasteryRecord, ...] = ()
    concept_records: tuple[NodeMasteryRecord, ...] = ()
    completed_node_ids: tuple[str, ...] = ()
    missed_objective_ids: tuple[str, ...] = ()
    coverage_ratio: float = 0.0


@dataclass(frozen=True)
class AdaptiveLearningSignal:
    """Adaptive signal derived from certification metadata + Curriculum Memory."""

    signal_id: str
    kind: str  # weak_concept | missed_objective | revision_priority | dependency
    node_id: str
    priority: float
    rationale: str
    related_node_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class AdaptiveLearningPlan:
    """Revision / weakness priorities from certified curriculum + progress."""

    curriculum_identity: str
    provenance: CurriculumProvenanceRef
    weak_concepts: tuple[AdaptiveLearningSignal, ...] = ()
    missed_objectives: tuple[AdaptiveLearningSignal, ...] = ()
    revision_priorities: tuple[AdaptiveLearningSignal, ...] = ()
    concept_dependencies: tuple[AdaptiveLearningSignal, ...] = ()


@dataclass(frozen=True)
class ObservatoryMetric:
    """One named operational metric for the Curriculum Observatory."""

    name: str
    value: float
    unit: str = ""
    notes: str = ""


@dataclass(frozen=True)
class CurriculumObservatoryReport:
    """Operational analytics for the Curriculum Intelligence Engine."""

    report_id: str
    chain_id: str = ""
    certification_trends: tuple[ObservatoryMetric, ...] = ()
    calibration_frequency: tuple[ObservatoryMetric, ...] = ()
    policy_warnings: tuple[str, ...] = ()
    decision_quality: tuple[ObservatoryMetric, ...] = ()
    evidence_quality: tuple[ObservatoryMetric, ...] = ()
    coverage_metrics: tuple[ObservatoryMetric, ...] = ()
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)
