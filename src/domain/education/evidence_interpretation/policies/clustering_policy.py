"""Policy governing clustering of educational evidence for interpretation.

Architecture Source
    EDUCATIONAL_EVIDENCE_MODEL.md /
    CAPABILITY_4_8_2_EDUCATIONAL_EVIDENCE_ANALYSIS.md
Concept
    Clustering Policy
"""

from __future__ import annotations

from domain.education.evidence_interpretation.entities.evidence_cluster import (
    EvidenceCluster,
)
from domain.education.evidence_interpretation.entities.interpreted_pattern import (
    REPEATED_PATTERN_KINDS,
    InterpretedPattern,
)
from domain.education.evidence_interpretation.enums import PatternKind
from domain.education.evidence_interpretation.value_objects.interpretation_confidence import (  # noqa: E501
    InterpretationConfidence,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import EvidenceId

# Repeated pattern kinds require a cluster of at least this many evidence ids.
_MIN_CLUSTER_SIZE_FOR_REPEATED = 2

# Soft / metacognitive pattern kinds cannot alone warrant very high confidence.
_SOFT_PATTERN_KINDS = frozenset(
    {
        PatternKind.REPEATED_REFLECTION_THEME,
        PatternKind.REPEATED_CONFIDENCE_MISMATCH,
    }
)

_CONFIDENCE_FLOOR_FOR_REPEATED: dict[PatternKind, ConfidenceLevel] = {
    PatternKind.REPEATED_RETRIEVAL_FAILURE: ConfidenceLevel.LOW,
    PatternKind.REPEATED_TRANSFER_FAILURE: ConfidenceLevel.LOW,
    PatternKind.REPEATED_CONFIDENCE_MISMATCH: ConfidenceLevel.VERY_LOW,
    PatternKind.REPEATED_MISCONCEPTION_INDICATOR: ConfidenceLevel.LOW,
    PatternKind.REPEATED_PROCEDURAL_ERROR: ConfidenceLevel.LOW,
    PatternKind.REPEATED_REFLECTION_THEME: ConfidenceLevel.VERY_LOW,
    PatternKind.EVIDENCE_CONSISTENCY: ConfidenceLevel.LOW,
    PatternKind.EVIDENCE_SUFFICIENCY: ConfidenceLevel.LOW,
    PatternKind.TREND_STABILITY: ConfidenceLevel.MEDIUM,
}


class ClusteringPolicy:
    """Enforces educational clustering and pattern–evidence alignment.

    Clustering organises observational evidence for pattern recognition. It
    does not diagnose learners or recommend actions.
    """

    @staticmethod
    def assert_cluster_size_for_patterns(
        clusters: tuple[EvidenceCluster, ...] | list[EvidenceCluster],
        patterns: tuple[InterpretedPattern, ...] | list[InterpretedPattern],
    ) -> None:
        """Repeated patterns require at least one cluster of sufficient size."""
        has_repeated = any(p.kind in REPEATED_PATTERN_KINDS for p in patterns)
        if not has_repeated:
            return
        if not any(c.size() >= _MIN_CLUSTER_SIZE_FOR_REPEATED for c in clusters):
            raise EducationalInvariantViolation(
                "repeated patterns require at least one cluster with "
                f"{_MIN_CLUSTER_SIZE_FOR_REPEATED} or more evidence references",
                invariant="ClusteringPolicy.cluster.size.repeated",
            )

    @staticmethod
    def assert_pattern_evidence_in_clusters(
        clusters: tuple[EvidenceCluster, ...] | list[EvidenceCluster],
        patterns: tuple[InterpretedPattern, ...] | list[InterpretedPattern],
    ) -> None:
        """Every pattern evidence id must appear in at least one cluster."""
        clustered: set[EvidenceId] = set()
        for cluster in clusters:
            clustered.update(cluster.evidence_ids)
        for pattern in patterns:
            for evidence_id in pattern.evidence_ids:
                if evidence_id not in clustered:
                    raise EducationalInvariantViolation(
                        f"pattern evidence {evidence_id.value} is not present "
                        "in any evidence cluster",
                        invariant="ClusteringPolicy.pattern_evidence.in_cluster",
                    )

    @staticmethod
    def assert_no_orphan_clusters(
        clusters: tuple[EvidenceCluster, ...] | list[EvidenceCluster],
        patterns: tuple[InterpretedPattern, ...] | list[InterpretedPattern],
    ) -> None:
        """Every cluster must contribute at least one evidence id to a pattern."""
        patterned: set[EvidenceId] = set()
        for pattern in patterns:
            patterned.update(pattern.evidence_ids)
        for cluster in clusters:
            if not any(eid in patterned for eid in cluster.evidence_ids):
                raise EducationalInvariantViolation(
                    f"evidence cluster {cluster.cluster_id.value} contributes "
                    "no evidence to any interpreted pattern",
                    invariant="ClusteringPolicy.cluster.orphan",
                )

    @staticmethod
    def assert_confidence_consistent_with_patterns(
        confidence: InterpretationConfidence,
        patterns: tuple[InterpretedPattern, ...] | list[InterpretedPattern],
    ) -> None:
        """Soft-only patterns cannot claim very high interpretive confidence."""
        if not patterns:
            return
        only_soft = all(p.kind in _SOFT_PATTERN_KINDS for p in patterns)
        if only_soft and confidence.level is ConfidenceLevel.VERY_HIGH:
            raise EducationalInvariantViolation(
                "soft patterns alone cannot warrant very high interpretation "
                "confidence",
                invariant="ClusteringPolicy.confidence.soft_ceiling",
            )
        # Floor: confidence must meet the strictest pattern floor among present.
        floors = [
            _CONFIDENCE_FLOOR_FOR_REPEATED[p.kind]
            for p in patterns
            if p.kind in _CONFIDENCE_FLOOR_FOR_REPEATED
        ]
        if not floors:
            return
        order = (
            ConfidenceLevel.VERY_LOW,
            ConfidenceLevel.LOW,
            ConfidenceLevel.MEDIUM,
            ConfidenceLevel.HIGH,
            ConfidenceLevel.VERY_HIGH,
        )
        # Soft patterns lower the floor; use the minimum floor among patterns
        # so mixed soft+hard is not blocked by soft alone.
        min_floor = min(floors, key=lambda level: order.index(level))
        if not confidence.is_at_least(min_floor):
            raise EducationalInvariantViolation(
                f"confidence {confidence.level.value} is too low for the "
                "identified pattern set",
                invariant="ClusteringPolicy.confidence.pattern_floor",
            )

    @staticmethod
    def assert_merge_compatible(
        student_id: str,
        other_student_id: str,
    ) -> None:
        if student_id != other_student_id:
            raise EducationalInvariantViolation(
                "cannot merge interpretations belonging to different students",
                invariant="ClusteringPolicy.merge.same_student",
            )

    @staticmethod
    def assert_consistent(
        clusters: tuple[EvidenceCluster, ...] | list[EvidenceCluster],
        patterns: tuple[InterpretedPattern, ...] | list[InterpretedPattern],
        confidence: InterpretationConfidence,
    ) -> None:
        ClusteringPolicy.assert_cluster_size_for_patterns(clusters, patterns)
        ClusteringPolicy.assert_pattern_evidence_in_clusters(clusters, patterns)
        ClusteringPolicy.assert_no_orphan_clusters(clusters, patterns)
        ClusteringPolicy.assert_confidence_consistent_with_patterns(
            confidence, patterns
        )
