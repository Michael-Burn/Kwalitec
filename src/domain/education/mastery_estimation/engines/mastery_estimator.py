"""MasteryEstimator — deterministic engine producing MasteryAssessment.

Architecture Source
    KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md
    STUDENT_DIGITAL_TWIN.md
    KNOWLEDGE_DEPENDENCY_MODEL.md
Concept
    Mastery Estimator

MasteryEstimator is the first educational reasoning engine of the
Education OS. It transforms ``EducationalEvidence``,
``StudentEducationalState``, and ``KnowledgeGraph`` into an immutable
``MasteryAssessment``. It reasons; it does not persist, orchestrate,
mutate its inputs, generate recommendations, generate missions, or call
AI. Every method is a pure function of its explicit, caller-supplied
inputs — the same inputs always produce the same output.

This engine legitimately depends on ``student_state``,
``educational_evidence``, and ``knowledge_graph``. Unlike those bounded
contexts, which deliberately stay isolated from one another, Mastery
Estimation exists specifically to reason across them.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime

from domain.education.educational_evidence.aggregates.educational_evidence import (
    EducationalEvidence,
)
from domain.education.knowledge_graph.aggregates.knowledge_graph import (
    KnowledgeGraph,
)
from domain.education.knowledge_graph.ids import KnowledgeNodeId
from domain.education.knowledge_graph.policies.relationship_policy import (
    RelationshipPolicy,
)
from domain.education.mastery_estimation.aggregates.mastery_assessment import (
    MasteryAssessment,
)
from domain.education.mastery_estimation.enums import (
    AssessmentReasonCode,
    KnowledgeGapKind,
    LearningStabilityBand,
)
from domain.education.mastery_estimation.ids import (
    AssessmentId,
    CompetencyId,
    SubjectId,
)
from domain.education.mastery_estimation.policies.confidence_policy import (
    ConfidencePolicy,
)
from domain.education.mastery_estimation.policies.evidence_weight_policy import (
    EvidenceWeightPolicy,
)
from domain.education.mastery_estimation.policies.mastery_policy import (
    MasteryPolicy,
)
from domain.education.mastery_estimation.policies.prerequisite_influence_policy import (  # noqa: E501
    PrerequisiteInfluencePolicy,
)
from domain.education.mastery_estimation.policies.stability_policy import (
    StabilityPolicy,
)
from domain.education.mastery_estimation.value_objects.assessment_reason import (
    AssessmentReason,
)
from domain.education.mastery_estimation.value_objects.assessment_snapshot import (
    AssessmentSnapshot,
)
from domain.education.mastery_estimation.value_objects.competency_assessment import (
    CompetencyAssessment,
)
from domain.education.mastery_estimation.value_objects.evidence_contribution import (
    EvidenceContribution,
)
from domain.education.mastery_estimation.value_objects.knowledge_gap import (
    KnowledgeGap,
)
from domain.education.mastery_estimation.value_objects.learning_stability import (
    LearningStability,
)
from domain.education.mastery_estimation.value_objects.mastery_confidence import (
    MasteryConfidence,
)
from domain.education.mastery_estimation.value_objects.mastery_score import (
    MasteryScore,
)
from domain.education.mastery_estimation.value_objects.subject_assessment import (
    SubjectAssessment,
)
from domain.education.student_state.aggregates.student_educational_state import (
    StudentEducationalState,
)

# Positive net signal at or above this weighted magnitude is called out
# explicitly as strong positive evidence; the mirrored negative threshold
# calls out strong negative evidence. Both are fixed, deterministic
# thresholds — never estimated.
_STRONG_POSITIVE_SIGNAL_THRESHOLD = 0.4
_STRONG_NEGATIVE_SIGNAL_THRESHOLD = -0.4
_DOMINANT_RECENCY_THRESHOLD = 0.8
_STALE_RECENCY_THRESHOLD = 0.2


class MasteryEstimator:
    """Deterministic engine estimating mastery from evidence and structure.

    Every public method accepts its inputs explicitly and returns a new
    value — no mutable engine state, no global state, and no wall-clock
    reads. Callers always supply ``as_of``/``assessed_at`` explicitly.
    """

    # --- top-level estimation ---

    @staticmethod
    def estimate(
        state: StudentEducationalState,
        evidence: Sequence[EducationalEvidence],
        knowledge_graph: KnowledgeGraph,
        *,
        assessment_id: AssessmentId,
        assessed_at: datetime,
    ) -> MasteryAssessment:
        """Produce a full mastery assessment across every tracked subject.

        Scope is bounded by what the student's own
        ``StudentEducationalState`` already tracks: every subject in
        ``state.subject_states`` and every competency in
        ``state.competency_states``. Discovering untracked curriculum
        content from the knowledge graph is out of scope for this engine.
        """
        subject_assessments = tuple(
            MasteryEstimator.estimate_subject(
                state,
                evidence,
                knowledge_graph,
                subject_id=SubjectId(subject_state.subject_id.value),
                as_of=assessed_at,
            )
            for subject_state in state.subject_states
        )
        overall_mastery = MasteryPolicy.aggregate_subject_scores(
            [assessment.mastery for assessment in subject_assessments]
        )
        overall_confidence = ConfidencePolicy.aggregate_subject_confidence(
            [assessment.confidence for assessment in subject_assessments]
        )
        overall_stability = StabilityPolicy.aggregate_subject_stability(
            [assessment.stability for assessment in subject_assessments]
        )
        knowledge_gaps = tuple(
            gap
            for subject_assessment in subject_assessments
            for gap in subject_assessment.knowledge_gaps()
        )
        supporting_evidence = tuple(
            contribution
            for subject_assessment in subject_assessments
            for contribution in subject_assessment.supporting_evidence()
        )
        reasons = tuple(
            reason
            for subject_assessment in subject_assessments
            for competency_assessment in subject_assessment.competency_assessments
            for reason in competency_assessment.reasons
        )
        return MasteryAssessment(
            assessment_id=assessment_id,
            student_id=state.student_id,
            assessed_at=assessed_at,
            overall_mastery=overall_mastery,
            overall_confidence=overall_confidence,
            overall_stability=overall_stability,
            subject_assessments=subject_assessments,
            knowledge_gaps=knowledge_gaps,
            supporting_evidence=supporting_evidence,
            reasons=reasons,
        )

    @staticmethod
    def estimate_subject(
        state: StudentEducationalState,
        evidence: Sequence[EducationalEvidence],
        knowledge_graph: KnowledgeGraph,
        *,
        subject_id: SubjectId,
        as_of: datetime,
    ) -> SubjectAssessment:
        """Estimate mastery for every competency tracked under one subject."""
        tracked = tuple(
            competency_state
            for competency_state in state.competency_states
            if competency_state.subject_id.value == subject_id.value
        )
        competency_assessments = tuple(
            MasteryEstimator.estimate_competency(
                evidence,
                knowledge_graph,
                competency_id=CompetencyId(competency_state.competency_id.value),
                subject_id=subject_id,
                as_of=as_of,
            )
            for competency_state in tracked
        )
        mastery = MasteryPolicy.aggregate_subject_scores(
            [assessment.mastery for assessment in competency_assessments]
        )
        confidence = ConfidencePolicy.aggregate_subject_confidence(
            [assessment.confidence for assessment in competency_assessments]
        )
        stability = StabilityPolicy.aggregate_subject_stability(
            [assessment.stability for assessment in competency_assessments]
        )
        return SubjectAssessment(
            subject_id=subject_id,
            mastery=mastery,
            confidence=confidence,
            stability=stability,
            competency_assessments=competency_assessments,
        )

    @staticmethod
    def estimate_competency(
        evidence: Sequence[EducationalEvidence],
        knowledge_graph: KnowledgeGraph,
        *,
        competency_id: CompetencyId,
        subject_id: SubjectId,
        as_of: datetime,
    ) -> CompetencyAssessment:
        """Estimate mastery for a single competency.

        Evidence influences only the competency it references; structural
        prerequisites discovered through the knowledge graph additionally
        dampen the resulting mastery when they are themselves weak.
        """
        contributions = MasteryEstimator._contributions_for(competency_id, evidence)
        raw_mastery = MasteryPolicy.aggregate_contributions(contributions)
        weak_prerequisites = MasteryEstimator.identify_prerequisite_weaknesses(
            competency_id, evidence, knowledge_graph
        )
        mastery = MasteryPolicy.apply_prerequisite_dampening(
            raw_mastery, weak_prerequisites
        )
        confidence = MasteryEstimator.calculate_confidence(
            contributions, as_of=as_of, weak_prerequisites=weak_prerequisites
        )
        stability = MasteryEstimator.calculate_learning_stability(contributions)
        direct_gaps = MasteryEstimator.identify_knowledge_gaps(competency_id, mastery)
        reasons = MasteryEstimator._build_reasons(
            subject_id=subject_id,
            competency_id=competency_id,
            contributions=contributions,
            confidence=confidence,
            stability=stability,
            weak_prerequisites=weak_prerequisites,
        )
        return CompetencyAssessment(
            competency_id=competency_id,
            subject_id=subject_id,
            mastery=mastery,
            confidence=confidence,
            stability=stability,
            supporting_evidence=contributions,
            gaps=(*direct_gaps, *weak_prerequisites),
            reasons=reasons,
        )

    # --- gap and weakness discovery ---

    @staticmethod
    def identify_knowledge_gaps(
        competency_id: CompetencyId, mastery: MasteryScore
    ) -> tuple[KnowledgeGap, ...]:
        """Direct knowledge gap for one competency's own computed mastery.

        Returns an empty tuple when the competency is not a gap — either
        it has no evidence at all, or its mastery already meets the
        secure threshold.
        """
        severity = MasteryPolicy.classify_gap_severity(mastery)
        if severity is None:
            return ()
        return (
            KnowledgeGap(
                competency_id=competency_id,
                kind=KnowledgeGapKind.WEAK_EVIDENCE,
                severity=severity,
                mastery_score=mastery,
            ),
        )

    @staticmethod
    def identify_prerequisite_weaknesses(
        competency_id: CompetencyId,
        evidence: Sequence[EducationalEvidence],
        knowledge_graph: KnowledgeGraph,
    ) -> tuple[KnowledgeGap, ...]:
        """Weak direct structural prerequisites of ``competency_id``.

        A prerequisite is identified purely by the same string identity
        value shared between this competency's node in the knowledge graph
        and evidence referencing it. Untracked or unregistered
        prerequisites are silently skipped rather than treated as
        weaknesses — this policy cannot judge what it has no data for.
        """
        node_id = KnowledgeNodeId(competency_id.value)
        if not knowledge_graph.has_node(node_id):
            return ()
        gaps: list[KnowledgeGap] = []
        for edge in knowledge_graph.edges_from(node_id):
            if not RelationshipPolicy.is_structural(edge.relationship_type):
                continue
            prerequisite_id = CompetencyId(edge.target_node_id.value)
            prerequisite_contributions = MasteryEstimator._contributions_for(
                prerequisite_id, evidence
            )
            prerequisite_score = MasteryPolicy.aggregate_contributions(
                prerequisite_contributions
            )
            if not PrerequisiteInfluencePolicy.is_weak(prerequisite_score):
                continue
            severity = PrerequisiteInfluencePolicy.classify_severity(
                prerequisite_score, edge.strength
            )
            gaps.append(
                KnowledgeGap(
                    competency_id=prerequisite_id,
                    kind=KnowledgeGapKind.WEAK_PREREQUISITE,
                    severity=severity,
                    mastery_score=prerequisite_score,
                    related_competency_id=competency_id,
                    dependency_strength=edge.strength,
                )
            )
        return tuple(gaps)

    # --- confidence and stability ---

    @staticmethod
    def calculate_confidence(
        contributions: Sequence[EvidenceContribution],
        *,
        as_of: datetime,
        weak_prerequisites: Sequence[KnowledgeGap] = (),
    ) -> MasteryConfidence:
        """Deterministic confidence in a set of evidence contributions."""
        return ConfidencePolicy.calculate(
            contributions, as_of=as_of, weak_prerequisites=weak_prerequisites
        )

    @staticmethod
    def calculate_learning_stability(
        contributions: Sequence[EvidenceContribution],
    ) -> LearningStability:
        """Deterministic learning stability of a set of evidence contributions."""
        return StabilityPolicy.calculate(contributions)

    # --- snapshot ---

    @staticmethod
    def produce_snapshot(assessment: MasteryAssessment) -> AssessmentSnapshot:
        """Produce an immutable, accurate snapshot of ``assessment``."""
        return assessment.produce_snapshot()

    # --- internals ---

    @staticmethod
    def _contributions_for(
        competency_id: CompetencyId, evidence: Sequence[EducationalEvidence]
    ) -> tuple[EvidenceContribution, ...]:
        relevant = [
            item for item in evidence if item.references_competency(competency_id.value)
        ]
        return tuple(EvidenceWeightPolicy.contribution_for(item) for item in relevant)

    @staticmethod
    def _build_reasons(
        *,
        subject_id: SubjectId,
        competency_id: CompetencyId,
        contributions: Sequence[EvidenceContribution],
        confidence: MasteryConfidence,
        stability: LearningStability,
        weak_prerequisites: Sequence[KnowledgeGap],
    ) -> tuple[AssessmentReason, ...]:
        reasons: list[AssessmentReason] = []
        if not contributions:
            reasons.append(
                AssessmentReason(
                    reason_code=AssessmentReasonCode.INSUFFICIENT_EVIDENCE,
                    subject_id=subject_id,
                    competency_id=competency_id,
                )
            )
            return tuple(reasons)
        if confidence.contradiction_ratio > 0.0:
            reasons.append(
                AssessmentReason(
                    reason_code=AssessmentReasonCode.CONTRADICTORY_EVIDENCE,
                    subject_id=subject_id,
                    competency_id=competency_id,
                    detail=confidence.contradiction_ratio,
                )
            )
        net_signal = sum(c.contribution * c.weight for c in contributions)
        if net_signal >= _STRONG_POSITIVE_SIGNAL_THRESHOLD:
            reasons.append(
                AssessmentReason(
                    reason_code=AssessmentReasonCode.STRONG_POSITIVE_EVIDENCE,
                    subject_id=subject_id,
                    competency_id=competency_id,
                    detail=net_signal,
                )
            )
        elif net_signal <= _STRONG_NEGATIVE_SIGNAL_THRESHOLD:
            reasons.append(
                AssessmentReason(
                    reason_code=AssessmentReasonCode.STRONG_NEGATIVE_EVIDENCE,
                    subject_id=subject_id,
                    competency_id=competency_id,
                    detail=net_signal,
                )
            )
        if weak_prerequisites:
            reasons.append(
                AssessmentReason(
                    reason_code=AssessmentReasonCode.WEAK_PREREQUISITE,
                    subject_id=subject_id,
                    competency_id=competency_id,
                    detail=float(len(weak_prerequisites)),
                )
            )
        if stability.band is LearningStabilityBand.STABLE:
            reasons.append(
                AssessmentReason(
                    reason_code=AssessmentReasonCode.STABLE_PERFORMANCE,
                    subject_id=subject_id,
                    competency_id=competency_id,
                )
            )
        elif stability.band is LearningStabilityBand.VOLATILE:
            reasons.append(
                AssessmentReason(
                    reason_code=AssessmentReasonCode.VOLATILE_PERFORMANCE,
                    subject_id=subject_id,
                    competency_id=competency_id,
                )
            )
        if confidence.recency_factor >= _DOMINANT_RECENCY_THRESHOLD:
            reasons.append(
                AssessmentReason(
                    reason_code=AssessmentReasonCode.RECENT_EVIDENCE_DOMINANT,
                    subject_id=subject_id,
                    competency_id=competency_id,
                )
            )
        elif confidence.recency_factor <= _STALE_RECENCY_THRESHOLD:
            reasons.append(
                AssessmentReason(
                    reason_code=AssessmentReasonCode.STALE_EVIDENCE,
                    subject_id=subject_id,
                    competency_id=competency_id,
                )
            )
        return tuple(reasons)
