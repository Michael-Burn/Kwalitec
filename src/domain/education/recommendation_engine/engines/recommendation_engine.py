"""RecommendationEngine — deterministic engine producing RecommendationSet.

Architecture Source
    PROJECT_CONTEXT.md
    KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md
    STUDENT_DIGITAL_TWIN.md
Concept
    Recommendation Engine

RecommendationEngine is the second educational reasoning engine of the
Education OS. It transforms ``StudentEducationalState``,
``MasteryAssessment``, ``EducationalEvidence``, and ``KnowledgeGraph``
into an immutable ``RecommendationSet``. It decides; it does not persist,
orchestrate, mutate its inputs, update the Digital Twin, generate
missions, or call AI. Every method is a pure function of its explicit,
caller-supplied inputs — the same inputs always produce the same output.

This engine legitimately depends on ``student_state``,
``mastery_estimation``, ``educational_evidence``, and
``knowledge_graph``. Cross-context reads happen through explicit, narrow
coercions at the boundary.
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
from domain.education.mastery_estimation.aggregates.mastery_assessment import (
    MasteryAssessment,
)
from domain.education.mastery_estimation.enums import (
    AssessmentReasonCode,
    KnowledgeGapKind,
    KnowledgeGapSeverity,
    MasteryBand,
)
from domain.education.mastery_estimation.value_objects.competency_assessment import (
    CompetencyAssessment,
)
from domain.education.mastery_estimation.value_objects.subject_assessment import (
    SubjectAssessment,
)
from domain.education.recommendation_engine.aggregates.recommendation_set import (
    RecommendationSet,
)
from domain.education.recommendation_engine.enums import (
    RecommendationCategory,
    RecommendationReasonCode,
)
from domain.education.recommendation_engine.ids import (
    CompetencyId,
    RecommendationId,
    RecommendationSetId,
    SubjectId,
)
from domain.education.recommendation_engine.policies.constraint_policy import (
    ConstraintPolicy,
)
from domain.education.recommendation_engine.policies.impact_policy import ImpactPolicy
from domain.education.recommendation_engine.policies.ordering_policy import (
    OrderingPolicy,
)
from domain.education.recommendation_engine.policies.priority_policy import (
    PriorityPolicy,
)
from domain.education.recommendation_engine.policies.recommendation_policy import (
    RecommendationPolicy,
)
from domain.education.recommendation_engine.value_objects.recommendation import (
    Recommendation,
)
from domain.education.recommendation_engine.value_objects.recommendation_confidence import (  # noqa: E501
    RecommendationConfidence,
)
from domain.education.recommendation_engine.value_objects.recommendation_constraint import (  # noqa: E501
    RecommendationConstraint,
)
from domain.education.recommendation_engine.value_objects.recommendation_explanation import (  # noqa: E501
    RecommendationExplanation,
)
from domain.education.recommendation_engine.value_objects.recommendation_ordering import (  # noqa: E501
    RecommendationOrdering,
)
from domain.education.recommendation_engine.value_objects.recommendation_reason import (
    RecommendationReason,
)
from domain.education.recommendation_engine.value_objects.recommendation_snapshot import (  # noqa: E501
    RecommendationSnapshot,
)
from domain.education.recommendation_engine.value_objects.recommendation_target import (
    RecommendationTarget,
)
from domain.education.student_state.aggregates.student_educational_state import (
    StudentEducationalState,
)

_SEVERITY_ORDER: tuple[KnowledgeGapSeverity, ...] = (
    KnowledgeGapSeverity.MINOR,
    KnowledgeGapSeverity.MODERATE,
    KnowledgeGapSeverity.SEVERE,
    KnowledgeGapSeverity.CRITICAL,
)


class RecommendationEngine:
    """Deterministic engine producing educational recommendations.

    Every public method accepts its inputs explicitly and returns a new
    value — no mutable engine state, no global state, and no wall-clock
    reads. Callers always supply ``recommended_at`` / ``as_of`` explicitly.
    """

    # --- top-level recommendation ---

    @staticmethod
    def recommend(
        state: StudentEducationalState,
        assessment: MasteryAssessment,
        evidence: Sequence[EducationalEvidence],
        knowledge_graph: KnowledgeGraph,
        *,
        set_id: RecommendationSetId,
        recommended_at: datetime,
    ) -> RecommendationSet:
        """Produce a full recommendation set across every assessed subject.

        Scope is bounded by what the mastery assessment already covers.
        The knowledge graph and evidence are consulted for structural and
        contradiction signals via the assessment; neither is mutated.
        Student educational state is read for mission/checkpoint context.
        """
        # Keep evidence and knowledge_graph on the public contract so the
        # engine signature mirrors the educational inputs it reasons over.
        # The mastery assessment already carries the derived signals those
        # inputs produced; consulting them again would re-estimate mastery.
        _ = (evidence, knowledge_graph)

        drafts: list[Recommendation] = []
        set_constraints: list[RecommendationConstraint] = []

        for subject_assessment in assessment.subject_assessments:
            subject_id = SubjectId(subject_assessment.subject_id.value)
            subject_recs, subject_constraints = (
                RecommendationEngine._recommend_subject_drafts(
                    subject_assessment,
                    set_id=set_id,
                    subject_id=subject_id,
                )
            )
            drafts.extend(subject_recs)
            set_constraints.extend(subject_constraints)

        drafts.extend(
            RecommendationEngine._mission_and_checkpoint_drafts(
                state,
                assessment,
                set_id=set_id,
            )
        )

        ranked = OrderingPolicy.rank(drafts)
        final = tuple(
            RecommendationEngine._with_deterministic_id(
                recommendation,
                set_id=set_id,
                ordinal=index,
            )
            for index, recommendation in enumerate(ranked, start=1)
        )
        constraints = ConstraintPolicy.aggregate_set_constraints(set_constraints)
        return RecommendationSet(
            set_id=set_id,
            student_id=state.student_id,
            recommended_at=recommended_at,
            recommendations=final,
            constraints=constraints,
        )

    @staticmethod
    def recommend_for_subject(
        state: StudentEducationalState,
        assessment: MasteryAssessment,
        evidence: Sequence[EducationalEvidence],
        knowledge_graph: KnowledgeGraph,
        *,
        subject_id: SubjectId,
        set_id: RecommendationSetId,
        recommended_at: datetime,
    ) -> RecommendationSet:
        """Produce recommendations scoped to one subject."""
        subject_assessment = assessment.subject_assessment_for(subject_id)
        if subject_assessment is None:
            return RecommendationSet(
                set_id=set_id,
                student_id=state.student_id,
                recommended_at=recommended_at,
                recommendations=(),
                constraints=(),
            )
        filtered = MasteryAssessment(
            assessment_id=assessment.assessment_id,
            student_id=assessment.student_id,
            assessed_at=assessment.assessed_at,
            overall_mastery=subject_assessment.mastery,
            overall_confidence=subject_assessment.confidence,
            overall_stability=subject_assessment.stability,
            subject_assessments=(subject_assessment,),
            knowledge_gaps=subject_assessment.knowledge_gaps(),
            supporting_evidence=subject_assessment.supporting_evidence(),
            reasons=tuple(
                reason
                for competency in subject_assessment.competency_assessments
                for reason in competency.reasons
            ),
        )
        return RecommendationEngine.recommend(
            state,
            filtered,
            evidence,
            knowledge_graph,
            set_id=set_id,
            recommended_at=recommended_at,
        )

    @staticmethod
    def recommend_for_competency(
        state: StudentEducationalState,
        assessment: MasteryAssessment,
        evidence: Sequence[EducationalEvidence],
        knowledge_graph: KnowledgeGraph,
        *,
        competency_id: CompetencyId,
        set_id: RecommendationSetId,
        recommended_at: datetime,
    ) -> RecommendationSet:
        """Produce recommendations scoped to one competency."""
        _ = (evidence, knowledge_graph)
        competency = assessment.competency_assessment_for(competency_id)
        if competency is None:
            return RecommendationSet(
                set_id=set_id,
                student_id=state.student_id,
                recommended_at=recommended_at,
                recommendations=(),
                constraints=(),
            )
        subject_id = SubjectId(competency.subject_id.value)
        drafts, constraints = RecommendationEngine._recommend_competency_drafts(
            competency,
            set_id=set_id,
            subject_id=subject_id,
        )
        ranked = OrderingPolicy.rank(drafts)
        final = tuple(
            RecommendationEngine._with_deterministic_id(
                recommendation,
                set_id=set_id,
                ordinal=index,
            )
            for index, recommendation in enumerate(ranked, start=1)
        )
        return RecommendationSet(
            set_id=set_id,
            student_id=state.student_id,
            recommended_at=recommended_at,
            recommendations=final,
            constraints=ConstraintPolicy.aggregate_set_constraints(constraints),
        )

    @staticmethod
    def prioritise(
        recommendations: Sequence[Recommendation],
    ) -> tuple[Recommendation, ...]:
        return OrderingPolicy.prioritise(recommendations)

    @staticmethod
    def rank(
        recommendations: Sequence[Recommendation],
    ) -> tuple[Recommendation, ...]:
        return OrderingPolicy.rank(recommendations)

    @staticmethod
    def identify_highest_impact_actions(
        recommendation_set: RecommendationSet,
        *,
        limit: int = 3,
    ) -> tuple[Recommendation, ...]:
        return recommendation_set.highest_impact_actions(limit=limit)

    @staticmethod
    def produce_snapshot(
        recommendation_set: RecommendationSet,
    ) -> RecommendationSnapshot:
        return recommendation_set.produce_snapshot()

    @staticmethod
    def generate_reasoning(
        category: RecommendationCategory,
        *,
        subject_id: SubjectId,
        competency_id: CompetencyId | None = None,
        detail: float | None = None,
        extra_reasons: Sequence[RecommendationReason] = (),
    ) -> RecommendationExplanation:
        """Build a structured explanation for a recommendation category."""
        primary = RecommendationPolicy.reason_for_category(
            category,
            subject_id=subject_id,
            competency_id=competency_id,
            detail=detail,
        )
        reasons = (primary, *tuple(extra_reasons))
        return RecommendationExplanation.from_reasons(reasons)

    # --- internal draft builders ---

    @staticmethod
    def _recommend_subject_drafts(
        subject_assessment: SubjectAssessment,
        *,
        set_id: RecommendationSetId,
        subject_id: SubjectId,
    ) -> tuple[list[Recommendation], list[RecommendationConstraint]]:
        drafts: list[Recommendation] = []
        constraints: list[RecommendationConstraint] = []
        for competency in subject_assessment.competency_assessments:
            competency_drafts, competency_constraints = (
                RecommendationEngine._recommend_competency_drafts(
                    competency,
                    set_id=set_id,
                    subject_id=subject_id,
                )
            )
            drafts.extend(competency_drafts)
            constraints.extend(competency_constraints)
        return drafts, constraints

    @staticmethod
    def _recommend_competency_drafts(
        assessment: CompetencyAssessment,
        *,
        set_id: RecommendationSetId,
        subject_id: SubjectId,
    ) -> tuple[list[Recommendation], list[RecommendationConstraint]]:
        drafts: list[Recommendation] = []
        constraints: list[RecommendationConstraint] = list(
            ConstraintPolicy.constraints_for_competency(
                assessment, subject_id=subject_id
            )
        )
        competency_id = CompetencyId(assessment.competency_id.value)

        for gap in assessment.gaps:
            if gap.kind is KnowledgeGapKind.WEAK_PREREQUISITE:
                prereq_id = CompetencyId(gap.competency_id.value)
                drafts.append(
                    RecommendationEngine._build_draft(
                        set_id=set_id,
                        category=RecommendationCategory.STUDY_PREREQUISITE,
                        subject_id=subject_id,
                        competency_id=prereq_id,
                        severity=gap.severity,
                        detail=gap.mastery_score.magnitude,
                        confidence_magnitude=assessment.confidence.score.magnitude,
                    )
                )
                if gap.related_competency_id is not None:
                    drafts.append(
                        RecommendationEngine._build_draft(
                            set_id=set_id,
                            category=RecommendationCategory.DELAY_ADVANCED_TOPIC,
                            subject_id=subject_id,
                            competency_id=CompetencyId(
                                gap.related_competency_id.value
                            ),
                            severity=gap.severity,
                            detail=gap.mastery_score.magnitude,
                            confidence_magnitude=(
                                assessment.confidence.score.magnitude
                            ),
                        )
                    )

        category = RecommendationPolicy.category_for_competency(assessment)
        if category is not None and category not in {
            RecommendationCategory.STUDY_PREREQUISITE,
            RecommendationCategory.DELAY_ADVANCED_TOPIC,
        }:
            severity = RecommendationEngine._worst_direct_severity(assessment)
            drafts.append(
                RecommendationEngine._build_draft(
                    set_id=set_id,
                    category=category,
                    subject_id=subject_id,
                    competency_id=competency_id,
                    severity=severity,
                    detail=assessment.mastery.magnitude,
                    confidence_magnitude=assessment.confidence.score.magnitude,
                    extra_reasons=RecommendationEngine._extra_reasons(
                        assessment, subject_id=subject_id
                    ),
                )
            )

        if (
            RecommendationPolicy.should_reduce_revision(assessment)
            and category is RecommendationCategory.MAINTAIN_MASTERY
        ):
            drafts.append(
                RecommendationEngine._build_draft(
                    set_id=set_id,
                    category=RecommendationCategory.REDUCE_REVISION_FREQUENCY,
                    subject_id=subject_id,
                    competency_id=competency_id,
                    detail=assessment.mastery.magnitude,
                    confidence_magnitude=assessment.confidence.score.magnitude,
                )
            )

        return drafts, constraints

    @staticmethod
    def _mission_and_checkpoint_drafts(
        state: StudentEducationalState,
        assessment: MasteryAssessment,
        *,
        set_id: RecommendationSetId,
    ) -> list[Recommendation]:
        drafts: list[Recommendation] = []
        has_blocking_prereq = any(
            gap.kind is KnowledgeGapKind.WEAK_PREREQUISITE
            for gap in assessment.knowledge_gaps
        )
        fallback_subject = (
            SubjectId(assessment.subject_assessments[0].subject_id.value)
            if assessment.subject_assessments
            else SubjectId("general")
        )

        if state.has_current_mission() and state.current_mission is not None:
            mission_id = str(state.current_mission.mission_id)
            drafts.append(
                RecommendationEngine._build_draft(
                    set_id=set_id,
                    category=RecommendationCategory.CONTINUE_CURRENT_MISSION,
                    subject_id=fallback_subject,
                    mission_id=mission_id,
                    confidence_magnitude=(
                        assessment.overall_confidence.score.magnitude
                    ),
                    preserve_mission=not has_blocking_prereq,
                )
            )

        if state.has_current_checkpoint() and state.current_checkpoint is not None:
            checkpoint_id = str(state.current_checkpoint.checkpoint_id)
            overall_band = assessment.overall_mastery.band
            if (
                overall_band in {MasteryBand.SECURE, MasteryBand.MASTERED}
                and not has_blocking_prereq
            ):
                category = RecommendationCategory.ATTEMPT_CHECKPOINT
            else:
                category = RecommendationCategory.PREPARE_ASSESSMENT
            drafts.append(
                RecommendationEngine._build_draft(
                    set_id=set_id,
                    category=category,
                    subject_id=fallback_subject,
                    checkpoint_id=checkpoint_id,
                    detail=assessment.overall_mastery.magnitude,
                    confidence_magnitude=(
                        assessment.overall_confidence.score.magnitude
                    ),
                )
            )
        return drafts

    @staticmethod
    def _extra_reasons(
        assessment: CompetencyAssessment,
        *,
        subject_id: SubjectId,
    ) -> tuple[RecommendationReason, ...]:
        extras: list[RecommendationReason] = []
        competency_id = CompetencyId(assessment.competency_id.value)
        for reason in assessment.reasons:
            if reason.reason_code is AssessmentReasonCode.CONTRADICTORY_EVIDENCE:
                extras.append(
                    RecommendationReason(
                        reason_code=RecommendationReasonCode.CONTRADICTORY_EVIDENCE,
                        subject_id=subject_id,
                        competency_id=competency_id,
                        detail=assessment.confidence.contradiction_ratio,
                    )
                )
            if reason.reason_code is AssessmentReasonCode.WEAK_PREREQUISITE:
                extras.append(
                    RecommendationReason(
                        reason_code=RecommendationReasonCode.WEAK_PREREQUISITE,
                        subject_id=subject_id,
                        competency_id=competency_id,
                    )
                )
        if any(gap.kind is KnowledgeGapKind.WEAK_EVIDENCE for gap in assessment.gaps):
            extras.append(
                RecommendationReason(
                    reason_code=RecommendationReasonCode.DIRECT_KNOWLEDGE_GAP,
                    subject_id=subject_id,
                    competency_id=competency_id,
                    detail=assessment.mastery.magnitude,
                )
            )
        return tuple(extras)

    @staticmethod
    def _worst_direct_severity(
        assessment: CompetencyAssessment,
    ) -> KnowledgeGapSeverity | None:
        direct = [
            gap
            for gap in assessment.gaps
            if gap.kind is KnowledgeGapKind.WEAK_EVIDENCE
        ]
        if not direct:
            return None
        return max(
            (gap.severity for gap in direct),
            key=lambda severity: _SEVERITY_ORDER.index(severity),
        )

    @staticmethod
    def _build_draft(
        *,
        set_id: RecommendationSetId,
        category: RecommendationCategory,
        subject_id: SubjectId,
        competency_id: CompetencyId | None = None,
        mission_id: str | None = None,
        checkpoint_id: str | None = None,
        severity: KnowledgeGapSeverity | None = None,
        detail: float | None = None,
        confidence_magnitude: float = 0.0,
        extra_reasons: Sequence[RecommendationReason] = (),
        preserve_mission: bool = False,
    ) -> Recommendation:
        priority = PriorityPolicy.priority_for(category, severity=severity)
        impact = ImpactPolicy.impact_for(category)
        confidence = RecommendationConfidence(
            magnitude=min(1.0, max(0.0, confidence_magnitude))
        )
        explanation = RecommendationEngine.generate_reasoning(
            category,
            subject_id=subject_id,
            competency_id=competency_id,
            detail=detail,
            extra_reasons=extra_reasons,
        )
        target = RecommendationTarget(
            subject_id=subject_id,
            competency_id=competency_id,
            mission_id=mission_id,
            checkpoint_id=checkpoint_id,
        )
        constraints: list[RecommendationConstraint] = []
        if preserve_mission:
            constraints.append(
                ConstraintPolicy.preserve_mission_constraint(subject_id=subject_id)
            )
        # Temporary id — replaced after ranking for dense ordinal identity.
        temp_id = RecommendationId(
            f"{set_id.value}:{category.value}:{target.correlation_key()}"
        )
        ordering = RecommendationOrdering(rank=1, priority=priority)
        return Recommendation(
            recommendation_id=temp_id,
            category=category,
            target=target,
            priority=priority,
            impact=impact,
            confidence=confidence,
            explanation=explanation,
            ordering=ordering,
            constraints=tuple(constraints),
        )

    @staticmethod
    def _with_deterministic_id(
        recommendation: Recommendation,
        *,
        set_id: RecommendationSetId,
        ordinal: int,
    ) -> Recommendation:
        new_id = RecommendationId(f"{set_id.value}:r{ordinal:04d}")
        return Recommendation(
            recommendation_id=new_id,
            category=recommendation.category,
            target=recommendation.target,
            priority=recommendation.priority,
            impact=recommendation.impact,
            confidence=recommendation.confidence,
            explanation=recommendation.explanation,
            ordering=recommendation.ordering,
            constraints=recommendation.constraints,
        )
