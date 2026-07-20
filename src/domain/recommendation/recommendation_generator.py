"""RecommendationGenerator — deterministic recommendations from Educational OS.

Architecture Source
    EDUCATIONAL_LOGIC_REGISTRY.md (EL-008)
    EDUCATIONAL_PRIORITY_MODEL.md
    STUDENT_DIGITAL_TWIN.md
Concept
    Recommendation Generation

Rules
    No AI. No prompting. No randomness.
    Same educational state always yields the same RecommendationSpecification.
"""

from __future__ import annotations

from domain.education.diagnosis.aggregates.educational_diagnosis import (
    EducationalDiagnosis,
)
from domain.education.diagnosis.enums import DiagnosisSeverityLevel, DiagnosisStatus
from domain.education.digital_twin.aggregates.educational_digital_twin import (
    EducationalDigitalTwin,
)
from domain.education.digital_twin.enums import TwinStatus
from domain.education.foundation.enums import ConfidenceLevel, DiagnosisType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.priority.aggregates.educational_priority import (
    EducationalPriority,
)
from domain.education.priority.enums import (
    PriorityFactorKind,
    PriorityScoreBand,
    PriorityStatus,
    UrgencyLevel,
)
from domain.education.teaching_strategy.aggregates.teaching_strategy import (
    TeachingStrategy,
)
from domain.education.teaching_strategy.enums import ComplexityLevel, StrategyStatus
from domain.mission_generation.mission_specification import MissionSpecification
from domain.progress_evaluation.enums import (
    InterventionUrgency,
    RevisionEffectivenessBand,
    StabilityBand,
    TrendDirection,
    VelocityBand,
)
from domain.progress_evaluation.progress_report import ProgressReport
from domain.recommendation.enums import (
    RecommendationCategory,
    RecommendationPriorityBand,
    RecommendationReasonCode,
    SupportingEvidenceCode,
)
from domain.recommendation.ids import RecommendationId, RecommendationSpecificationId
from domain.recommendation.recommendation import (
    Recommendation,
    RecommendationConfidence,
    SupportingEvidence,
)
from domain.recommendation.recommendation_priority import RecommendationPriority
from domain.recommendation.recommendation_reason import RecommendationReason
from domain.recommendation.recommendation_specification import (
    RecommendationSpecification,
)
from domain.study_planning.study_plan import StudyPlan

# --- deterministic catalogues -----------------------------------------------

_PRIORITY_BAND_MAP: dict[PriorityScoreBand, RecommendationPriorityBand] = {
    PriorityScoreBand.NEGLIGIBLE: RecommendationPriorityBand.NEGLIGIBLE,
    PriorityScoreBand.LOW: RecommendationPriorityBand.LOW,
    PriorityScoreBand.MEDIUM: RecommendationPriorityBand.MEDIUM,
    PriorityScoreBand.HIGH: RecommendationPriorityBand.HIGH,
    PriorityScoreBand.CRITICAL: RecommendationPriorityBand.CRITICAL,
}

_BAND_RANK: dict[RecommendationPriorityBand, int] = {
    RecommendationPriorityBand.NEGLIGIBLE: 0,
    RecommendationPriorityBand.LOW: 1,
    RecommendationPriorityBand.MEDIUM: 2,
    RecommendationPriorityBand.HIGH: 3,
    RecommendationPriorityBand.CRITICAL: 4,
}

_URGENCY_RANK: dict[UrgencyLevel, int] = {
    UrgencyLevel.DEFERRED: 0,
    UrgencyLevel.ROUTINE: 1,
    UrgencyLevel.ELEVATED: 2,
    UrgencyLevel.IMMEDIATE: 3,
    UrgencyLevel.CRITICAL: 4,
}

# Fixed evaluation order for category ranking (higher = earlier when bands tie).
_CATEGORY_RANK: dict[RecommendationCategory, int] = {
    RecommendationCategory.PAUSE_FOR_CONSOLIDATION: 80,
    RecommendationCategory.REVISIT_PREREQUISITES: 70,
    RecommendationCategory.REDUCE_COGNITIVE_LOAD: 60,
    RecommendationCategory.REPEAT_ASSESSMENT: 50,
    RecommendationCategory.REVIEW_PREVIOUS_TOPIC: 40,
    RecommendationCategory.SCHEDULE_REVISION: 30,
    RecommendationCategory.INCREASE_DIFFICULTY: 20,
    RecommendationCategory.CONTINUE_MISSION: 10,
}

_CONFIDENCE_MILLIPOINTS: dict[ConfidenceLevel, int | None] = {
    ConfidenceLevel.UNKNOWN: None,
    ConfidenceLevel.VERY_LOW: 100,
    ConfidenceLevel.LOW: 300,
    ConfidenceLevel.MEDIUM: 500,
    ConfidenceLevel.HIGH: 700,
    ConfidenceLevel.VERY_HIGH: 900,
}

_EXPECTED_OUTCOMES: dict[RecommendationCategory, str] = {
    RecommendationCategory.CONTINUE_MISSION: (
        "Complete the current mission sitting and capture attributable evidence"
    ),
    RecommendationCategory.REVIEW_PREVIOUS_TOPIC: (
        "Restore fragile prior understanding before advancing new material"
    ),
    RecommendationCategory.INCREASE_DIFFICULTY: (
        "Raise instructional challenge while preserving stable mastery gains"
    ),
    RecommendationCategory.REDUCE_COGNITIVE_LOAD: (
        "Lower instructional demand so understanding can stabilise"
    ),
    RecommendationCategory.REPEAT_ASSESSMENT: (
        "Re-probe understanding to calibrate confidence against performance"
    ),
    RecommendationCategory.SCHEDULE_REVISION: (
        "Schedule spaced revision to strengthen retention of learned concepts"
    ),
    RecommendationCategory.REVISIT_PREREQUISITES: (
        "Repair prerequisite gaps that block progress on the current target"
    ),
    RecommendationCategory.PAUSE_FOR_CONSOLIDATION: (
        "Pause new advancement so recent learning can consolidate"
    ),
}

_LOW_CONFIDENCE = frozenset({ConfidenceLevel.VERY_LOW, ConfidenceLevel.LOW})
_HIGH_COMPLEXITY = frozenset({ComplexityLevel.HIGH, ComplexityLevel.VERY_HIGH})
_STABLE_BANDS = frozenset({StabilityBand.STABLE, StabilityBand.DURABLE})
_FRAGILE_BANDS = frozenset({StabilityBand.UNSTABLE, StabilityBand.FRAGILE})
_ASSESSMENT_DIAGNOSES = frozenset(
    {DiagnosisType.FALSE_CONFIDENCE, DiagnosisType.LOW_CONFIDENCE}
)
_PREREQUISITE_DIAGNOSES = frozenset({DiagnosisType.PREREQUISITE_GAP})
_RETENTION_DIAGNOSES = frozenset({DiagnosisType.WEAK_RETENTION})


class RecommendationGenerator:
    """Pure domain service that generates RecommendationSpecifications.

    Generation is fully deterministic and explainable from Educational OS
    inputs. No AI, no prompting, no randomness, no wall-clock dependence.
    """

    @classmethod
    def generate(
        cls,
        twin: EducationalDigitalTwin,
        mission: MissionSpecification,
        study_plan: StudyPlan,
        progress: ProgressReport,
        diagnosis: EducationalDiagnosis,
        priority: EducationalPriority,
        strategy: TeachingStrategy,
    ) -> RecommendationSpecification:
        """Generate a RecommendationSpecification from Educational OS state.

        Args:
            twin: Educational Digital Twin (learner memory).
            mission: Current MissionSpecification to advise against.
            study_plan: Active StudyPlan including review windows.
            progress: ProgressReport evaluating recent learning signals.
            diagnosis: Named educational deficiency in force.
            priority: Instructional ordering of the diagnosed need.
            strategy: Selected teaching strategy commitment.

        Returns:
            Immutable RecommendationSpecification with ordered educational
            recommendations, each carrying reason, priority, expected outcome,
            supporting evidence, and confidence.

        Raises:
            EducationalInvariantViolation: When inputs are educationally
                inconsistent or not ready for recommendation generation.
        """
        cls._assert_inputs(
            twin, mission, study_plan, progress, diagnosis, priority, strategy
        )

        categories = cls._select_categories(
            diagnosis=diagnosis,
            priority=priority,
            strategy=strategy,
            progress=progress,
            study_plan=study_plan,
        )
        recommendations = tuple(
            cls._build_recommendation(
                index=index,
                category=category,
                twin=twin,
                mission=mission,
                study_plan=study_plan,
                progress=progress,
                diagnosis=diagnosis,
                priority=priority,
                strategy=strategy,
            )
            for index, category in enumerate(categories, start=1)
        )
        specification_id = cls._specification_id(
            twin, mission, study_plan, progress, diagnosis, priority, strategy
        )
        rationale = cls._build_rationale(
            twin=twin,
            mission=mission,
            progress=progress,
            diagnosis=diagnosis,
            priority=priority,
            strategy=strategy,
            recommendations=recommendations,
        )
        return RecommendationSpecification(
            specification_id=specification_id,
            student_id=twin.student_id,
            recommendations=recommendations,
            educational_rationale=rationale,
            twin_id=twin.twin_id,
            mission_id=mission.mission_id,
            plan_id=study_plan.plan_id,
            progress_report_id=progress.report_id,
            diagnosis_id=diagnosis.diagnosis_id,
            priority_id=priority.priority_id,
            strategy_id=strategy.strategy_id,
        )

    # --- validation ---------------------------------------------------------

    @staticmethod
    def _assert_inputs(
        twin: EducationalDigitalTwin,
        mission: MissionSpecification,
        study_plan: StudyPlan,
        progress: ProgressReport,
        diagnosis: EducationalDiagnosis,
        priority: EducationalPriority,
        strategy: TeachingStrategy,
    ) -> None:
        if not isinstance(twin, EducationalDigitalTwin):
            raise EducationalInvariantViolation(
                "twin must be an EducationalDigitalTwin",
                invariant="RecommendationGenerator.twin.type",
            )
        if not isinstance(mission, MissionSpecification):
            raise EducationalInvariantViolation(
                "mission must be a MissionSpecification",
                invariant="RecommendationGenerator.mission.type",
            )
        if not isinstance(study_plan, StudyPlan):
            raise EducationalInvariantViolation(
                "study_plan must be a StudyPlan",
                invariant="RecommendationGenerator.study_plan.type",
            )
        if not isinstance(progress, ProgressReport):
            raise EducationalInvariantViolation(
                "progress must be a ProgressReport",
                invariant="RecommendationGenerator.progress.type",
            )
        if not isinstance(diagnosis, EducationalDiagnosis):
            raise EducationalInvariantViolation(
                "diagnosis must be an EducationalDiagnosis",
                invariant="RecommendationGenerator.diagnosis.type",
            )
        if not isinstance(priority, EducationalPriority):
            raise EducationalInvariantViolation(
                "priority must be an EducationalPriority",
                invariant="RecommendationGenerator.priority.type",
            )
        if not isinstance(strategy, TeachingStrategy):
            raise EducationalInvariantViolation(
                "strategy must be a TeachingStrategy",
                invariant="RecommendationGenerator.strategy.type",
            )

        student_ids = {
            twin.student_id,
            mission.student_id,
            study_plan.student_id,
            progress.student_id,
            diagnosis.student_id,
            priority.student_id,
            strategy.student_id,
        }
        if len(student_ids) != 1:
            raise EducationalInvariantViolation(
                "all recommendation inputs must share student_id",
                invariant="RecommendationGenerator.student_alignment",
            )

        if twin.status is TwinStatus.ARCHIVED:
            raise EducationalInvariantViolation(
                "cannot generate recommendations from an archived twin",
                invariant="RecommendationGenerator.twin.active",
            )
        if diagnosis.status is DiagnosisStatus.INVALIDATED:
            raise EducationalInvariantViolation(
                "cannot generate recommendations from an invalidated diagnosis",
                invariant="RecommendationGenerator.diagnosis.active",
            )
        if priority.status not in {
            PriorityStatus.ASSIGNED,
            PriorityStatus.REVISED,
            PriorityStatus.STABILISED,
        }:
            raise EducationalInvariantViolation(
                "priority must be assigned, revised, or stabilised",
                invariant="RecommendationGenerator.priority.status",
            )
        if strategy.status not in {
            StrategyStatus.SELECTED,
            StrategyStatus.REVISED,
        }:
            raise EducationalInvariantViolation(
                "strategy must be selected or revised before recommendation",
                invariant="RecommendationGenerator.strategy.committed",
            )

        if twin.twin_id != mission.twin_id or twin.twin_id != progress.twin_id:
            raise EducationalInvariantViolation(
                "mission and progress must reference the provided twin",
                invariant="RecommendationGenerator.twin.link",
            )
        if (
            diagnosis.diagnosis_id != mission.diagnosis_id
            or not any(
                ref.diagnosis_id == diagnosis.diagnosis_id
                for ref in priority.diagnosis_references
            )
            or not any(
                ref.diagnosis_id == diagnosis.diagnosis_id
                for ref in strategy.diagnosis_references
            )
        ):
            raise EducationalInvariantViolation(
                "mission, priority, and strategy must reference the diagnosis",
                invariant="RecommendationGenerator.diagnosis.link",
            )
        if (
            priority.priority_id != mission.priority_id
            or priority.priority_id != study_plan.priority_id
        ):
            raise EducationalInvariantViolation(
                "mission and study plan must reference the provided priority",
                invariant="RecommendationGenerator.priority.link",
            )
        if strategy.strategy_id != mission.strategy_id:
            raise EducationalInvariantViolation(
                "mission must reference the provided teaching strategy",
                invariant="RecommendationGenerator.strategy.link",
            )
        if mission.mission_id not in study_plan.mission_ids:
            raise EducationalInvariantViolation(
                "study plan must include the provided mission",
                invariant="RecommendationGenerator.plan.mission_link",
            )
        if study_plan.plan_id not in progress.plan_ids:
            raise EducationalInvariantViolation(
                "progress report must reference the provided study plan",
                invariant="RecommendationGenerator.progress.plan_link",
            )

    # --- identity -----------------------------------------------------------

    @staticmethod
    def _specification_id(
        twin: EducationalDigitalTwin,
        mission: MissionSpecification,
        study_plan: StudyPlan,
        progress: ProgressReport,
        diagnosis: EducationalDiagnosis,
        priority: EducationalPriority,
        strategy: TeachingStrategy,
    ) -> RecommendationSpecificationId:
        return RecommendationSpecificationId(
            f"rec-{twin.twin_id.value}-{mission.mission_id.value}"
            f"-{study_plan.plan_id.value}-{progress.report_id.value}"
            f"-{diagnosis.diagnosis_id.value}-{priority.priority_id.value}"
            f"-{strategy.strategy_id.value}"
        )

    # --- category selection -------------------------------------------------

    @classmethod
    def _select_categories(
        cls,
        *,
        diagnosis: EducationalDiagnosis,
        priority: EducationalPriority,
        strategy: TeachingStrategy,
        progress: ProgressReport,
        study_plan: StudyPlan,
    ) -> tuple[RecommendationCategory, ...]:
        matched: list[RecommendationCategory] = []

        if cls._matches_revisit_prerequisites(diagnosis, priority):
            matched.append(RecommendationCategory.REVISIT_PREREQUISITES)
        if cls._matches_pause(progress):
            matched.append(RecommendationCategory.PAUSE_FOR_CONSOLIDATION)
        if cls._matches_reduce_load(strategy, progress):
            matched.append(RecommendationCategory.REDUCE_COGNITIVE_LOAD)
        if cls._matches_repeat_assessment(diagnosis, progress):
            matched.append(RecommendationCategory.REPEAT_ASSESSMENT)
        if cls._matches_review_previous(progress):
            matched.append(RecommendationCategory.REVIEW_PREVIOUS_TOPIC)
        if cls._matches_schedule_revision(diagnosis, progress, study_plan):
            matched.append(RecommendationCategory.SCHEDULE_REVISION)
        if cls._matches_increase_difficulty(diagnosis, strategy, progress):
            matched.append(RecommendationCategory.INCREASE_DIFFICULTY)

        # CONTINUE_MISSION is the lawful default; excluded when pause blocks
        # advancement or when prerequisite repair must take precedence alone
        # with critical urgency.
        pause = RecommendationCategory.PAUSE_FOR_CONSOLIDATION in matched
        revisit_critical = (
            RecommendationCategory.REVISIT_PREREQUISITES in matched
            and priority.urgency.level is UrgencyLevel.CRITICAL
        )
        if not pause and not revisit_critical:
            matched.append(RecommendationCategory.CONTINUE_MISSION)
        elif not matched:
            matched.append(RecommendationCategory.CONTINUE_MISSION)

        # Mutual exclusions for educational coherence.
        if RecommendationCategory.PAUSE_FOR_CONSOLIDATION in matched:
            matched = [
                category
                for category in matched
                if category
                not in {
                    RecommendationCategory.INCREASE_DIFFICULTY,
                    RecommendationCategory.CONTINUE_MISSION,
                }
            ]
        if RecommendationCategory.REDUCE_COGNITIVE_LOAD in matched:
            matched = [
                category
                for category in matched
                if category is not RecommendationCategory.INCREASE_DIFFICULTY
            ]
        if not matched:
            matched.append(RecommendationCategory.CONTINUE_MISSION)

        return tuple(
            sorted(
                matched,
                key=lambda category: (
                    -_CATEGORY_RANK[category],
                    category.value,
                ),
            )
        )

    @staticmethod
    def _matches_revisit_prerequisites(
        diagnosis: EducationalDiagnosis,
        priority: EducationalPriority,
    ) -> bool:
        if diagnosis.diagnosis_type in _PREREQUISITE_DIAGNOSES:
            return True
        peak = priority.peak_factor()
        return peak.kind is PriorityFactorKind.PREREQUISITE_IMPORTANCE

    @staticmethod
    def _matches_pause(progress: ProgressReport) -> bool:
        if progress.intervention_signal.urgency is InterventionUrgency.CRITICAL:
            return True
        return (
            progress.knowledge_stability is StabilityBand.UNSTABLE
            and progress.mastery_trend.direction is TrendDirection.DECLINING
        )

    @staticmethod
    def _matches_reduce_load(
        strategy: TeachingStrategy,
        progress: ProgressReport,
    ) -> bool:
        if strategy.complexity.level not in _HIGH_COMPLEXITY:
            return False
        return (
            progress.confidence_level in _LOW_CONFIDENCE
            or progress.mastery_trend.direction is TrendDirection.DECLINING
            or progress.intervention_signal.required
        )

    @staticmethod
    def _matches_repeat_assessment(
        diagnosis: EducationalDiagnosis,
        progress: ProgressReport,
    ) -> bool:
        if diagnosis.diagnosis_type in _ASSESSMENT_DIAGNOSES:
            return True
        return (
            progress.mastery_trend.direction is TrendDirection.IMPROVING
            and progress.confidence_trend.direction is TrendDirection.DECLINING
        )

    @staticmethod
    def _matches_review_previous(progress: ProgressReport) -> bool:
        if progress.mastery_trend.direction is TrendDirection.DECLINING:
            return True
        return (
            progress.knowledge_stability in _FRAGILE_BANDS
            and progress.mastery_trend.direction
            in {TrendDirection.STABLE, TrendDirection.DECLINING}
        )

    @staticmethod
    def _matches_schedule_revision(
        diagnosis: EducationalDiagnosis,
        progress: ProgressReport,
        study_plan: StudyPlan,
    ) -> bool:
        if diagnosis.diagnosis_type in _RETENTION_DIAGNOSES:
            return True
        if (
            progress.revision_effectiveness.band
            is RevisionEffectivenessBand.INEFFECTIVE
        ):
            return True
        return bool(study_plan.review_windows) and (
            progress.knowledge_stability in _FRAGILE_BANDS
            or progress.revision_effectiveness.band
            is RevisionEffectivenessBand.MIXED
        )

    @staticmethod
    def _matches_increase_difficulty(
        diagnosis: EducationalDiagnosis,
        strategy: TeachingStrategy,
        progress: ProgressReport,
    ) -> bool:
        if progress.intervention_signal.required:
            return False
        if strategy.complexity.level is not ComplexityLevel.LOW:
            return False
        if diagnosis.severity.level not in {
            DiagnosisSeverityLevel.MILD,
            DiagnosisSeverityLevel.MODERATE,
        }:
            return False
        return (
            progress.mastery_trend.direction is TrendDirection.IMPROVING
            and progress.learning_velocity.band is VelocityBand.FAST
            and progress.knowledge_stability in _STABLE_BANDS
        )

    # --- recommendation construction ----------------------------------------

    @classmethod
    def _build_recommendation(
        cls,
        *,
        index: int,
        category: RecommendationCategory,
        twin: EducationalDigitalTwin,
        mission: MissionSpecification,
        study_plan: StudyPlan,
        progress: ProgressReport,
        diagnosis: EducationalDiagnosis,
        priority: EducationalPriority,
        strategy: TeachingStrategy,
    ) -> Recommendation:
        rec_priority = cls._map_priority(category, priority, progress)
        reason = cls._build_reason(category, diagnosis, priority, progress, strategy)
        evidence = cls._build_supporting_evidence(
            category=category,
            twin=twin,
            mission=mission,
            study_plan=study_plan,
            progress=progress,
            diagnosis=diagnosis,
            priority=priority,
            strategy=strategy,
        )
        confidence = cls._calculate_confidence(
            category=category,
            twin=twin,
            progress=progress,
            diagnosis=diagnosis,
            evidence_count=len(evidence),
        )
        return Recommendation(
            recommendation_id=RecommendationId(
                f"recitem-{mission.mission_id.value}-{index:02d}-{category.value}"
            ),
            category=category,
            reason=reason,
            priority=rec_priority,
            expected_outcome=_EXPECTED_OUTCOMES[category],
            supporting_evidence=evidence,
            confidence=confidence,
        )

    @classmethod
    def _map_priority(
        cls,
        category: RecommendationCategory,
        priority: EducationalPriority,
        progress: ProgressReport,
    ) -> RecommendationPriority:
        band = _PRIORITY_BAND_MAP[priority.score.band]
        urgency = priority.urgency.level

        # Category-specific educational boosts (deterministic, non-random).
        if category is RecommendationCategory.PAUSE_FOR_CONSOLIDATION:
            band = cls._max_band(band, RecommendationPriorityBand.HIGH)
            if progress.intervention_signal.urgency is InterventionUrgency.CRITICAL:
                band = RecommendationPriorityBand.CRITICAL
                urgency = UrgencyLevel.CRITICAL
        elif category is RecommendationCategory.REVISIT_PREREQUISITES:
            band = cls._max_band(band, RecommendationPriorityBand.HIGH)
        elif category is RecommendationCategory.REDUCE_COGNITIVE_LOAD:
            band = cls._max_band(band, RecommendationPriorityBand.MEDIUM)
            if progress.intervention_signal.required:
                band = cls._max_band(band, RecommendationPriorityBand.HIGH)
        elif category is RecommendationCategory.CONTINUE_MISSION:
            if band is RecommendationPriorityBand.CRITICAL:
                band = RecommendationPriorityBand.HIGH
        elif category is RecommendationCategory.INCREASE_DIFFICULTY:
            band = cls._min_band(band, RecommendationPriorityBand.MEDIUM)

        peak = priority.peak_factor()
        rationale = (
            f"Mapped from educational priority {priority.score.band.value} "
            f"with urgency {priority.urgency.level.value}; category "
            f"{category.value}; peak factor {peak.kind.value}; "
            f"resolved band {band.value}"
        )
        return RecommendationPriority.of(
            band,
            urgency,
            ratio=priority.score.ratio,
            rationale=rationale,
        )

    @staticmethod
    def _max_band(
        left: RecommendationPriorityBand,
        right: RecommendationPriorityBand,
    ) -> RecommendationPriorityBand:
        return left if _BAND_RANK[left] >= _BAND_RANK[right] else right

    @staticmethod
    def _min_band(
        left: RecommendationPriorityBand,
        right: RecommendationPriorityBand,
    ) -> RecommendationPriorityBand:
        return left if _BAND_RANK[left] <= _BAND_RANK[right] else right

    @classmethod
    def _build_reason(
        cls,
        category: RecommendationCategory,
        diagnosis: EducationalDiagnosis,
        priority: EducationalPriority,
        progress: ProgressReport,
        strategy: TeachingStrategy,
    ) -> RecommendationReason:
        code, statement = cls._reason_for_category(
            category, diagnosis, priority, progress, strategy
        )
        return RecommendationReason(statement=statement, code=code)

    @staticmethod
    def _reason_for_category(
        category: RecommendationCategory,
        diagnosis: EducationalDiagnosis,
        priority: EducationalPriority,
        progress: ProgressReport,
        strategy: TeachingStrategy,
    ) -> tuple[RecommendationReasonCode, str]:
        if category is RecommendationCategory.REVISIT_PREREQUISITES:
            return (
                RecommendationReasonCode.DIAGNOSIS_TYPE,
                (
                    f"Prerequisite work is required because diagnosis "
                    f"{diagnosis.diagnosis_type.value} and priority peak "
                    f"{priority.peak_factor().kind.value} block advancement"
                ),
            )
        if category is RecommendationCategory.PAUSE_FOR_CONSOLIDATION:
            return (
                RecommendationReasonCode.INTERVENTION_SIGNAL,
                (
                    f"Consolidation pause is warranted by intervention "
                    f"{progress.intervention_signal.urgency.value} with "
                    f"stability {progress.knowledge_stability.value}"
                ),
            )
        if category is RecommendationCategory.REDUCE_COGNITIVE_LOAD:
            return (
                RecommendationReasonCode.STRATEGY_COMPLEXITY,
                (
                    f"Cognitive load should reduce because strategy complexity "
                    f"{strategy.complexity.level.value} coincides with "
                    f"confidence {progress.confidence_level.value}"
                ),
            )
        if category is RecommendationCategory.REPEAT_ASSESSMENT:
            return (
                RecommendationReasonCode.CONFIDENCE_TREND,
                (
                    f"Assessment should repeat to reconcile diagnosis "
                    f"{diagnosis.diagnosis_type.value} with mastery "
                    f"{progress.mastery_trend.direction.value} and confidence "
                    f"{progress.confidence_trend.direction.value}"
                ),
            )
        if category is RecommendationCategory.REVIEW_PREVIOUS_TOPIC:
            return (
                RecommendationReasonCode.MASTERY_TREND,
                (
                    f"Previous topic review is needed because mastery trend is "
                    f"{progress.mastery_trend.direction.value} and stability is "
                    f"{progress.knowledge_stability.value}"
                ),
            )
        if category is RecommendationCategory.SCHEDULE_REVISION:
            return (
                RecommendationReasonCode.REVISION_EFFECTIVENESS,
                (
                    f"Revision should be scheduled because retention signals "
                    f"show effectiveness "
                    f"{progress.revision_effectiveness.band.value} under "
                    f"stability {progress.knowledge_stability.value}"
                ),
            )
        if category is RecommendationCategory.INCREASE_DIFFICULTY:
            return (
                RecommendationReasonCode.LEARNING_VELOCITY,
                (
                    f"Difficulty may increase because mastery is "
                    f"{progress.mastery_trend.direction.value}, velocity is "
                    f"{progress.learning_velocity.band.value}, and complexity "
                    f"is {strategy.complexity.level.value}"
                ),
            )
        return (
            RecommendationReasonCode.MISSION_READY,
            (
                f"Continue the current mission under priority "
                f"{priority.score.band.value} while diagnosis "
                f"{diagnosis.diagnosis_type.value} remains actionable"
            ),
        )

    @classmethod
    def _build_supporting_evidence(
        cls,
        *,
        category: RecommendationCategory,
        twin: EducationalDigitalTwin,
        mission: MissionSpecification,
        study_plan: StudyPlan,
        progress: ProgressReport,
        diagnosis: EducationalDiagnosis,
        priority: EducationalPriority,
        strategy: TeachingStrategy,
    ) -> tuple[SupportingEvidence, ...]:
        evidence: list[SupportingEvidence] = [
            SupportingEvidence(
                code=SupportingEvidenceCode.DIAGNOSIS,
                statement=(
                    f"Diagnosis {diagnosis.diagnosis_type.value} "
                    f"(severity {diagnosis.severity.level.value}, "
                    f"confidence {diagnosis.confidence.level.value})"
                ),
                source_id=diagnosis.diagnosis_id.value,
            ),
            SupportingEvidence(
                code=SupportingEvidenceCode.PRIORITY,
                statement=(
                    f"Educational priority band {priority.score.band.value} "
                    f"with urgency {priority.urgency.level.value}"
                ),
                source_id=priority.priority_id.value,
            ),
            SupportingEvidence(
                code=SupportingEvidenceCode.PROGRESS_MASTERY,
                statement=(
                    f"Mastery trend {progress.mastery_trend.direction.value} "
                    f"from {progress.mastery_trend.sample_size} samples"
                ),
                source_id=progress.report_id.value,
            ),
            SupportingEvidence(
                code=SupportingEvidenceCode.MISSION,
                statement=(
                    f"Active mission {mission.mission_id.value} with "
                    f"{mission.task_count()} ordered tasks"
                ),
                source_id=mission.mission_id.value,
            ),
        ]

        if category in {
            RecommendationCategory.PAUSE_FOR_CONSOLIDATION,
            RecommendationCategory.REDUCE_COGNITIVE_LOAD,
            RecommendationCategory.REVIEW_PREVIOUS_TOPIC,
        }:
            evidence.append(
                SupportingEvidence(
                    code=SupportingEvidenceCode.PROGRESS_INTERVENTION,
                    statement=(
                        "Intervention "
                        + (
                            "required"
                            if progress.intervention_signal.required
                            else "not required"
                        )
                        + " at urgency "
                        + progress.intervention_signal.urgency.value
                    ),
                    source_id=progress.report_id.value,
                )
            )
            evidence.append(
                SupportingEvidence(
                    code=SupportingEvidenceCode.PROGRESS_STABILITY,
                    statement=(
                        f"Knowledge stability {progress.knowledge_stability.value}"
                    ),
                    source_id=progress.report_id.value,
                )
            )

        if category in {
            RecommendationCategory.REDUCE_COGNITIVE_LOAD,
            RecommendationCategory.INCREASE_DIFFICULTY,
            RecommendationCategory.CONTINUE_MISSION,
        }:
            evidence.append(
                SupportingEvidence(
                    code=SupportingEvidenceCode.STRATEGY,
                    statement=(
                        f"Teaching strategy {strategy.primary_strategy.value} "
                        f"at complexity {strategy.complexity.level.value}"
                    ),
                    source_id=strategy.strategy_id.value,
                )
            )

        if category in {
            RecommendationCategory.REPEAT_ASSESSMENT,
            RecommendationCategory.INCREASE_DIFFICULTY,
        }:
            evidence.append(
                SupportingEvidence(
                    code=SupportingEvidenceCode.PROGRESS_CONFIDENCE,
                    statement=(
                        f"Confidence level {progress.confidence_level.value} "
                        f"with trend {progress.confidence_trend.direction.value}"
                    ),
                    source_id=progress.report_id.value,
                )
            )
            evidence.append(
                SupportingEvidence(
                    code=SupportingEvidenceCode.TWIN,
                    statement=(
                        f"Twin confidence posture {twin.confidence.overall.value}"
                    ),
                    source_id=twin.twin_id.value,
                )
            )

        if category is RecommendationCategory.SCHEDULE_REVISION:
            evidence.append(
                SupportingEvidence(
                    code=SupportingEvidenceCode.PROGRESS_REVISION,
                    statement=(
                        f"Revision effectiveness "
                        f"{progress.revision_effectiveness.band.value}"
                    ),
                    source_id=progress.report_id.value,
                )
            )
            evidence.append(
                SupportingEvidence(
                    code=SupportingEvidenceCode.STUDY_PLAN,
                    statement=(
                        f"Study plan declares {len(study_plan.review_windows)} "
                        f"review window(s)"
                    ),
                    source_id=study_plan.plan_id.value,
                )
            )

        if category is RecommendationCategory.INCREASE_DIFFICULTY:
            evidence.append(
                SupportingEvidence(
                    code=SupportingEvidenceCode.PROGRESS_VELOCITY,
                    statement=(
                        f"Learning velocity {progress.learning_velocity.band.value}"
                    ),
                    source_id=progress.report_id.value,
                )
            )

        return tuple(evidence)

    # --- confidence ---------------------------------------------------------

    @classmethod
    def _calculate_confidence(
        cls,
        *,
        category: RecommendationCategory,
        twin: EducationalDigitalTwin,
        progress: ProgressReport,
        diagnosis: EducationalDiagnosis,
        evidence_count: int,
    ) -> RecommendationConfidence:
        samples: list[int] = []
        for level in (
            diagnosis.confidence.level,
            progress.confidence_level,
            twin.confidence.overall,
        ):
            millipoints = _CONFIDENCE_MILLIPOINTS.get(level)
            if millipoints is not None:
                samples.append(millipoints)

        if not samples:
            samples.append(500)

        total = sum(samples)
        # Agreement bonus: each supporting evidence citation beyond the base
        # four adds a fixed educational millipoint increment (capped).
        agreement_bonus = min(120, max(0, evidence_count - 4) * 30)
        # Trend sufficiency penalty when mastery data is thin.
        trend_penalty = 0
        if progress.mastery_trend.direction is TrendDirection.INSUFFICIENT_DATA:
            trend_penalty += 100
        if progress.confidence_trend.direction is TrendDirection.INSUFFICIENT_DATA:
            trend_penalty += 80
        # Category fit: pause/prerequisite under critical intervention raises
        # recommendation confidence; increase-difficulty under advisory only.
        fit_bonus = 0
        if (
            category is RecommendationCategory.PAUSE_FOR_CONSOLIDATION
            and progress.intervention_signal.urgency is InterventionUrgency.CRITICAL
        ):
            fit_bonus += 80
        if (
            category is RecommendationCategory.REVISIT_PREREQUISITES
            and diagnosis.diagnosis_type in _PREREQUISITE_DIAGNOSES
        ):
            fit_bonus += 60

        millipoints = (total // len(samples)) + agreement_bonus + fit_bonus
        millipoints = max(0, min(1000, millipoints - trend_penalty))
        level = cls._millipoints_to_level(millipoints)
        ratio = millipoints / 1000.0
        return RecommendationConfidence.of(
            level, ratio=ratio, millipoints=millipoints
        )

    @staticmethod
    def _millipoints_to_level(millipoints: int) -> ConfidenceLevel:
        if millipoints < 200:
            return ConfidenceLevel.VERY_LOW
        if millipoints < 400:
            return ConfidenceLevel.LOW
        if millipoints < 600:
            return ConfidenceLevel.MEDIUM
        if millipoints < 800:
            return ConfidenceLevel.HIGH
        return ConfidenceLevel.VERY_HIGH

    # --- rationale ----------------------------------------------------------

    @classmethod
    def _build_rationale(
        cls,
        *,
        twin: EducationalDigitalTwin,
        mission: MissionSpecification,
        progress: ProgressReport,
        diagnosis: EducationalDiagnosis,
        priority: EducationalPriority,
        strategy: TeachingStrategy,
        recommendations: tuple[Recommendation, ...],
    ) -> str:
        categories = ", ".join(item.category.value for item in recommendations)
        primary = recommendations[0]
        peak = priority.peak_factor()
        return (
            f"Recommendation set for student {twin.student_id} addresses "
            f"diagnosis {diagnosis.diagnosis_type.value} "
            f"(severity {diagnosis.severity.level.value}) under priority "
            f"{priority.score.band.value} (peak {peak.kind.value}) with "
            f"strategy {strategy.primary_strategy.value}. Active mission "
            f"{mission.mission_id.value} and progress "
            f"{progress.report_id.value} (intervention "
            f"{progress.intervention_signal.urgency.value}, mastery "
            f"{progress.mastery_trend.direction.value}) yield ordered "
            f"decisions [{categories}]. Primary decision "
            f"{primary.category.value} at priority {primary.priority.band.value} "
            f"with confidence {primary.confidence.level.value}."
        )


def map_priority_band(band: PriorityScoreBand) -> RecommendationPriorityBand:
    """Map an Educational Priority score band to a RecommendationPriorityBand."""
    try:
        return _PRIORITY_BAND_MAP[band]
    except KeyError as exc:
        raise EducationalInvariantViolation(
            "unknown priority score band",
            invariant="RecommendationGenerator.priority_band.unknown",
        ) from exc


def category_rank(category: RecommendationCategory) -> int:
    """Return the fixed educational ranking weight for a recommendation category."""
    try:
        return _CATEGORY_RANK[category]
    except KeyError as exc:
        raise EducationalInvariantViolation(
            "unknown recommendation category",
            invariant="RecommendationGenerator.category.unknown",
        ) from exc


def confidence_from_millipoints(millipoints: int) -> ConfidenceLevel:
    """Map recommendation confidence millipoints to a ConfidenceLevel."""
    if isinstance(millipoints, bool) or not isinstance(millipoints, int):
        raise EducationalInvariantViolation(
            "millipoints must be an integer",
            invariant="RecommendationGenerator.confidence.millipoints.type",
        )
    if millipoints < 0 or millipoints > 1000:
        raise EducationalInvariantViolation(
            "millipoints must be between 0 and 1000 inclusive",
            invariant="RecommendationGenerator.confidence.millipoints.range",
        )
    return RecommendationGenerator._millipoints_to_level(millipoints)
