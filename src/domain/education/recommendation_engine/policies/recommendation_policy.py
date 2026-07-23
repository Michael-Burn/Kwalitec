"""Recommendation policy — maps educational signals to recommendation intent.

Architecture Source
    PROJECT_CONTEXT.md
    KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md
Concept
    Recommendation Policy

Deterministic decision rules that turn mastery assessment signals into
educational recommendation categories. This policy decides educational
intent; it does not estimate mastery, mutate state, or generate missions.
"""

from __future__ import annotations

from domain.education.foundation.enums import ConfidenceLevel
from domain.education.mastery_estimation.enums import (
    AssessmentReasonCode,
    KnowledgeGapKind,
    LearningStabilityBand,
    MasteryBand,
)
from domain.education.mastery_estimation.value_objects.competency_assessment import (
    CompetencyAssessment,
)
from domain.education.mastery_estimation.value_objects.knowledge_gap import (
    KnowledgeGap,
)
from domain.education.recommendation_engine.enums import (
    RecommendationCategory,
    RecommendationReasonCode,
)
from domain.education.recommendation_engine.ids import CompetencyId, SubjectId
from domain.education.recommendation_engine.value_objects.recommendation_reason import (
    RecommendationReason,
)

# Fixed thresholds — never estimated, never randomised.
_HIGH_CONFIDENCE_THRESHOLD = 0.60
_LOW_CONFIDENCE_THRESHOLD = 0.40


class RecommendationPolicy:
    """Deterministically selects educational recommendation categories."""

    @staticmethod
    def category_for_prerequisite_gap(
        gap: KnowledgeGap,
    ) -> RecommendationCategory:
        """Weak prerequisite → study the prerequisite first."""
        if gap.kind is not KnowledgeGapKind.WEAK_PREREQUISITE:
            raise ValueError("expected a weak_prerequisite gap")
        return RecommendationCategory.STUDY_PREREQUISITE

    @staticmethod
    def category_for_competency(
        assessment: CompetencyAssessment,
    ) -> RecommendationCategory | None:
        """Select the primary category for one competency assessment.

        Decision table (first match wins, deterministic order):

        1. Contradictory evidence → ReviewConcept
        2. Low mastery + high confidence → StrengthenWeakArea
        3. Low mastery + low confidence + not assessed/not started
           → RevisitFoundation
        4. Low mastery + low/medium confidence → FocusCompetency
        5. Developing mastery → ConsolidateKnowledge
        6. Volatile stability → IncreaseRevisionFrequency
        7. Stable high mastery → MaintainMastery
        8. Stable high mastery (revision load) also yields
           ReduceRevisionFrequency via a separate helper
        9. Secure + high confidence → PrepareAssessment
        """
        mastery_band = assessment.mastery.band
        confidence_magnitude = assessment.confidence.score.magnitude
        stability_band = assessment.stability.band

        if RecommendationPolicy._has_contradictory_evidence(assessment):
            return RecommendationCategory.REVIEW_CONCEPT

        if mastery_band in {
            MasteryBand.NOT_ASSESSED,
            MasteryBand.NOT_STARTED,
            MasteryBand.DEVELOPING,
        }:
            if confidence_magnitude >= _HIGH_CONFIDENCE_THRESHOLD:
                return RecommendationCategory.STRENGTHEN_WEAK_AREA
            if mastery_band in {
                MasteryBand.NOT_ASSESSED,
                MasteryBand.NOT_STARTED,
            }:
                return RecommendationCategory.REVISIT_FOUNDATION
            if confidence_magnitude < _LOW_CONFIDENCE_THRESHOLD:
                return RecommendationCategory.FOCUS_COMPETENCY
            return RecommendationCategory.CONSOLIDATE_KNOWLEDGE

        if stability_band is LearningStabilityBand.VOLATILE:
            return RecommendationCategory.INCREASE_REVISION_FREQUENCY

        if mastery_band in {MasteryBand.SECURE, MasteryBand.MASTERED}:
            if stability_band is LearningStabilityBand.STABLE:
                return RecommendationCategory.MAINTAIN_MASTERY
            if confidence_magnitude >= _HIGH_CONFIDENCE_THRESHOLD:
                return RecommendationCategory.PREPARE_ASSESSMENT

        return None

    @staticmethod
    def should_reduce_revision(assessment: CompetencyAssessment) -> bool:
        """Stable high mastery warrants reducing revision frequency."""
        return (
            assessment.mastery.band
            in {MasteryBand.SECURE, MasteryBand.MASTERED}
            and assessment.stability.band is LearningStabilityBand.STABLE
            and assessment.confidence.score.magnitude >= _HIGH_CONFIDENCE_THRESHOLD
        )

    @staticmethod
    def should_delay_advanced(
        assessment: CompetencyAssessment,
    ) -> bool:
        """Delay advanced work when the competency has prerequisite gaps."""
        return any(
            gap.kind is KnowledgeGapKind.WEAK_PREREQUISITE
            for gap in assessment.gaps
        )

    @staticmethod
    def reason_for_category(
        category: RecommendationCategory,
        *,
        subject_id: SubjectId,
        competency_id: CompetencyId | None = None,
        detail: float | None = None,
    ) -> RecommendationReason:
        """Map a category to its primary structured reason code."""
        mapping: dict[RecommendationCategory, RecommendationReasonCode] = {
            RecommendationCategory.STUDY_PREREQUISITE: (
                RecommendationReasonCode.WEAK_PREREQUISITE
            ),
            RecommendationCategory.STRENGTHEN_WEAK_AREA: (
                RecommendationReasonCode.LOW_MASTERY_HIGH_CONFIDENCE
            ),
            RecommendationCategory.REVISIT_FOUNDATION: (
                RecommendationReasonCode.LOW_MASTERY_LOW_CONFIDENCE
            ),
            RecommendationCategory.FOCUS_COMPETENCY: (
                RecommendationReasonCode.LOW_MASTERY_LOW_CONFIDENCE
            ),
            RecommendationCategory.REVIEW_CONCEPT: (
                RecommendationReasonCode.CONTRADICTORY_EVIDENCE
            ),
            RecommendationCategory.MAINTAIN_MASTERY: (
                RecommendationReasonCode.STABLE_HIGH_MASTERY
            ),
            RecommendationCategory.INCREASE_REVISION_FREQUENCY: (
                RecommendationReasonCode.VOLATILE_MASTERY
            ),
            RecommendationCategory.REDUCE_REVISION_FREQUENCY: (
                RecommendationReasonCode.STABLE_REVISION_LOAD
            ),
            RecommendationCategory.CONSOLIDATE_KNOWLEDGE: (
                RecommendationReasonCode.DEVELOPING_MASTERY
            ),
            RecommendationCategory.DELAY_ADVANCED_TOPIC: (
                RecommendationReasonCode.ADVANCED_WITHOUT_FOUNDATION
            ),
            RecommendationCategory.PREPARE_ASSESSMENT: (
                RecommendationReasonCode.SECURE_READY_FOR_CHECKPOINT
            ),
            RecommendationCategory.ATTEMPT_CHECKPOINT: (
                RecommendationReasonCode.ACTIVE_CHECKPOINT
            ),
            RecommendationCategory.CONTINUE_CURRENT_MISSION: (
                RecommendationReasonCode.ACTIVE_MISSION
            ),
        }
        reason_code = mapping.get(
            category, RecommendationReasonCode.DIRECT_KNOWLEDGE_GAP
        )
        return RecommendationReason(
            reason_code=reason_code,
            subject_id=subject_id,
            competency_id=competency_id,
            detail=detail,
        )

    @staticmethod
    def _has_contradictory_evidence(assessment: CompetencyAssessment) -> bool:
        if assessment.confidence.is_contradicted():
            return True
        if assessment.confidence.contradiction_ratio > 0.0:
            return True
        return any(
            reason.reason_code is AssessmentReasonCode.CONTRADICTORY_EVIDENCE
            for reason in assessment.reasons
        )

    @staticmethod
    def is_high_confidence(level: ConfidenceLevel) -> bool:
        return level in {ConfidenceLevel.HIGH, ConfidenceLevel.VERY_HIGH}

    @staticmethod
    def is_low_confidence(level: ConfidenceLevel) -> bool:
        return level in {ConfidenceLevel.VERY_LOW, ConfidenceLevel.LOW}
