"""EI-001 Curriculum Intelligence Engine — immutable generation contracts.

Snapshots are frozen; rejected nodes are inactive, never deleted.
Phase B adds generation hashes and Curriculum Memory accessors on nodes.
Phase C renames Gen 4 to Concept Formation and adds evidence grading.
Phase D extends CertificationDecision with evidence / decision quality scores.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import IntEnum, StrEnum

from app.domain.curriculum_intelligence.confidence import ConfidenceRecord
from app.domain.curriculum_intelligence.evidence import EvidenceGrade
from app.domain.curriculum_intelligence.provenance import ProvenanceRecord


class GenerationIndex(IntEnum):
    """Ordered educational generation indices (1..7)."""

    RAW_GRAPH = 1
    NOISE_ELIMINATION = 2
    HIERARCHY = 3
    CONCEPT_FORMATION = 4
    TOPIC_CONSOLIDATION = 4  # Alias — renamed Concept Formation (EI-001C)
    OBJECTIVE_INTELLIGENCE = 5
    RECONCILIATION = 6
    CERTIFICATION = 7


GENERATION_PURPOSES: dict[GenerationIndex, str] = {
    GenerationIndex.RAW_GRAPH: "raw_educational_graph",
    GenerationIndex.NOISE_ELIMINATION: "noise_elimination",
    GenerationIndex.HIERARCHY: "hierarchy_construction",
    GenerationIndex.CONCEPT_FORMATION: "concept_formation",
    GenerationIndex.OBJECTIVE_INTELLIGENCE: "objective_intelligence",
    GenerationIndex.RECONCILIATION: "educational_reconciliation",
    GenerationIndex.CERTIFICATION: "educational_certification",
}


class SnapshotStatus(StrEnum):
    """Lifecycle status for an immutable generation snapshot."""

    ACCEPTED = "accepted"
    REJECTED_BY_REGRESSION = "rejected_by_regression"
    SUPERSEDED = "superseded"


class LineageOperationKind(StrEnum):
    """Append-only lineage operation kinds."""

    CREATED = "created"
    ROLE_CHANGED = "role_changed"
    REPARENTED = "reparented"
    MERGED = "merged"
    SPLIT = "split"
    REJECTED = "rejected"
    RESTORED = "restored"


class CertificationOutcome(StrEnum):
    """Generation 7 certification decisions."""

    CERTIFIED = "CERTIFIED"
    CERTIFIED_WITH_WARNINGS = "CERTIFIED_WITH_WARNINGS"
    NOT_CERTIFIED = "NOT_CERTIFIED"


class GranularityStyle(StrEnum):
    """Founder calibration — topic granularity."""

    VERY_DETAILED = "very_detailed"
    BALANCED = "balanced"
    CONCEPT_FOCUSED = "concept_focused"


class HierarchyStyle(StrEnum):
    """Founder calibration — hierarchy preference."""

    STRICT_SYLLABUS = "strict_syllabus"
    BALANCED = "balanced"
    TEACHING_OPTIMISED = "teaching_optimised"


class TopicDensityStyle(StrEnum):
    """Founder calibration — topic density."""

    FINE = "fine"
    BALANCED = "balanced"
    CONSOLIDATED = "consolidated"


class DifficultyBiasStyle(StrEnum):
    """Founder calibration — difficulty bias."""

    EXAM_FOCUSED = "exam_focused"
    CONCEPTUAL = "conceptual"
    BALANCED = "balanced"


@dataclass(frozen=True)
class LineageOperation:
    """One append-only lineage event for an educational node."""

    operation_id: str
    kind: LineageOperationKind
    generation_id: str
    generation_index: int
    reason_code: str
    reason_label: str
    related_node_ids: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    confidence: float | None = None
    created_at_iso: str = ""


@dataclass(frozen=True)
class LineageRecord:
    """Curriculum Memory lineage for one educational identity."""

    created_generation: str
    created_generation_index: int
    last_modified_generation: str
    last_modified_generation_index: int
    operations: tuple[LineageOperation, ...]
    related_node_ids: tuple[str, ...] = ()
    syllabus_refs: tuple[str, ...] = ()
    cmp_evidence: tuple[str, ...] = ()
    parent_history: tuple[str | None, ...] = ()
    merged_from: tuple[str, ...] = ()
    split_into: tuple[str, ...] = ()
    rejection_reason_code: str | None = None
    rejection_reason_label: str | None = None

    def with_appended(self, operation: LineageOperation) -> LineageRecord:
        """Return a new lineage with one more operation (never mutates self)."""
        merged_from = self.merged_from
        split_into = self.split_into
        if operation.kind is LineageOperationKind.MERGED:
            merged_from = tuple(
                dict.fromkeys(self.merged_from + operation.related_node_ids)
            )
        if operation.kind is LineageOperationKind.SPLIT:
            split_into = tuple(
                dict.fromkeys(self.split_into + operation.related_node_ids)
            )
        return replace(
            self,
            last_modified_generation=operation.generation_id,
            last_modified_generation_index=operation.generation_index,
            operations=self.operations + (operation,),
            related_node_ids=tuple(
                dict.fromkeys(self.related_node_ids + operation.related_node_ids)
            ),
            merged_from=merged_from,
            split_into=split_into,
            rejection_reason_code=(
                operation.reason_code
                if operation.kind is LineageOperationKind.REJECTED
                else self.rejection_reason_code
            ),
            rejection_reason_label=(
                operation.reason_label
                if operation.kind is LineageOperationKind.REJECTED
                else self.rejection_reason_label
            ),
        )


@dataclass(frozen=True)
class EducationalNode:
    """Stable educational identity within a generation snapshot.

    Curriculum Memory fields:
    - created_generation / current_generation (via lineage)
    - evidence (provenance)
    - confidence
    - role
    - active status
    """

    node_id: str
    generation_local_id: str
    title: str
    kind: str
    role: str | None
    parent_node_id: str | None
    confidence: ConfidenceRecord
    lineage: LineageRecord
    active: bool
    provenance_id: str | None = None
    provenance: ProvenanceRecord | None = None
    body: str = ""
    attributes: tuple[tuple[str, str], ...] = ()
    evidence_grade: EvidenceGrade | None = None
    policy_id: str | None = None

    @property
    def created_generation(self) -> str:
        """Generation id that first created this educational identity."""
        return self.lineage.created_generation

    @property
    def current_generation(self) -> str:
        """Generation id of the latest lineage mutation for this node."""
        return self.lineage.last_modified_generation

    @property
    def evidence(self) -> ProvenanceRecord | None:
        """Source evidence bound to this node (CIP-002 provenance atom)."""
        return self.provenance


@dataclass(frozen=True)
class RejectedNode:
    """Soft-deleted educational node retained for comparison."""

    node: EducationalNode
    rejected_at_generation: str
    reason_code: str
    reason_label: str
    confidence: float
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class QualitySnapshot:
    """Comparable educational quality vector for one generation."""

    coverage: float
    hierarchy: float
    duplicates: float
    noise: float
    granularity: float
    confidence: float
    active_node_count: int = 0
    rejected_node_count: int = 0
    low_confidence_share: float = 0.0
    chapters: int = 0
    sections: int = 0
    topics: int = 0
    objectives: int = 0
    evidence_quality: float = 0.0

    def as_vector(self) -> dict[str, float]:
        """Return primary educational metrics as a plain dict."""
        return {
            "coverage": self.coverage,
            "hierarchy": self.hierarchy,
            "duplicates": self.duplicates,
            "noise": self.noise,
            "granularity": self.granularity,
            "confidence": self.confidence,
            "evidence_quality": self.evidence_quality,
        }


@dataclass(frozen=True)
class RegressionPolicy:
    """Weighted lexicographic gates for RegressionGuard.

    Phase C hard-gates coverage, hierarchy, granularity, evidence quality,
    and confidence (plus noise from Phase B). Soft notes remain available
    when a dimension is configured as soft-only.
    """

    coverage_epsilon: float = 0.0
    noise_epsilon: float = 0.0
    hierarchy_epsilon: float = 0.0
    granularity_epsilon: float = 0.0
    evidence_quality_epsilon: float = 0.0
    # Allow a small Gen2 confidence dip when noise elimination removes
    # high-confidence chrome whose mean inflated the prior generation
    # (PL-001A CMP probe: ~0.011). Educational-node confidence scoring is
    # the primary fix; this epsilon is a residual production tolerance.
    confidence_epsilon: float = 0.015
    reject_on_granularity: bool = True
    reject_on_evidence_quality: bool = True
    reject_on_confidence: bool = True
    prefer_granularity: bool = True
    prefer_confidence: bool = True


@dataclass(frozen=True)
class RegressionReport:
    """Record of an accept/reject regression decision."""

    report_id: str
    chain_id: str
    candidate_generation_id: str
    candidate_snapshot_id: str
    baseline_generation_ids: tuple[str, ...]
    accepted: bool
    reason: str
    candidate_metrics: QualitySnapshot
    baseline_metrics: QualitySnapshot
    gate_failures: tuple[str, ...]
    created_at_iso: str


@dataclass(frozen=True)
class Generation:
    """One educational generation within an engine chain."""

    generation_id: str
    chain_id: str
    generation_index: int
    purpose: str
    parent_generation_ids: tuple[str, ...]
    source_document_ids: tuple[int, ...]
    workspace_id: str
    created_at_iso: str
    calibration_profile_id: str | None = None

    def __post_init__(self) -> None:
        if self.generation_index < 1 or self.generation_index > 7:
            raise ValueError(
                f"generation_index must be 1..7, got {self.generation_index}"
            )


@dataclass(frozen=True)
class CurriculumGenerationSnapshot:
    """Immutable checkpoint produced by one generation."""

    snapshot_id: str
    generation: Generation
    nodes: tuple[EducationalNode, ...]
    rejected_nodes: tuple[RejectedNode, ...]
    metrics: QualitySnapshot
    provenance_bundle_id: str
    created_at_iso: str
    status: SnapshotStatus
    generation_hash: str = ""
    agent_id: str = ""
    agent_version: str = ""

    @property
    def generation_id(self) -> str:
        return self.generation.generation_id

    @property
    def generation_index(self) -> int:
        return self.generation.generation_index

    @property
    def chain_id(self) -> str:
        return self.generation.chain_id

    def with_status(self, status: SnapshotStatus) -> CurriculumGenerationSnapshot:
        """Return a copy with a new lifecycle status (content unchanged)."""
        return replace(self, status=status)

    def active_nodes(self) -> tuple[EducationalNode, ...]:
        """Nodes still in the active hierarchy."""
        return tuple(n for n in self.nodes if n.active)


@dataclass(frozen=True)
class CertificationDecision:
    """Generation 7 certification artefact (scores + decision).

    Phase D adds evidence quality, reasoning confidence, and decision quality.
    ``certification_status`` mirrors ``outcome`` for Founder Preview consumers.
    """

    decision_id: str
    chain_id: str
    snapshot_id: str
    outcome: CertificationOutcome
    quality_score: float
    confidence: float
    coverage: float
    hierarchy_score: float
    granularity_score: float
    warnings: tuple[str, ...]
    hard_gate_failures: tuple[str, ...]
    created_at_iso: str
    evidence_quality: float = 0.0
    reasoning_confidence: float = 0.0
    decision_quality: float = 0.0
    failure_reasons: tuple[str, ...] = ()

    @property
    def certification_status(self) -> CertificationOutcome:
        """Alias for Founder Preview / Review Pack consumers."""
        return self.outcome


@dataclass(frozen=True)
class CalibrationProfile:
    """Founder educational-style settings (not node editing)."""

    profile_id: str
    workspace_id: str
    granularity: GranularityStyle
    hierarchy: HierarchyStyle
    topic_density: TopicDensityStyle
    difficulty_bias: DifficultyBiasStyle
    created_at_iso: str


def purpose_for_index(index: int) -> str:
    """Map generation index to its single educational purpose."""
    return GENERATION_PURPOSES[GenerationIndex(index)]
