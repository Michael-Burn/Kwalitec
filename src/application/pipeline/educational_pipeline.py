"""EducationalPipeline — orchestrate Educational OS engines end-to-end.

Architecture Source
    APP-002 Educational Pipeline Orchestrator

Rules
    No educational decisions. Pure orchestration.
    All decisions delegated to domain engines.
    No Flask. No SQLAlchemy. No persistence.
    No AI logic beyond calling injected enrichment ports.
    AI failures must not fail the pipeline.
"""

from __future__ import annotations

import logging
from enum import Enum
from typing import Protocol

from application.pipeline.pipeline_request import (
    PipelineRequest,
    PipelineSessionContext,
)
from application.pipeline.pipeline_result import (
    EnhancedMissionView,
    EnhancedRecommendationsView,
    PipelineResult,
    deterministic_enhanced_mission,
    deterministic_enhanced_recommendations,
)
from domain.education.evidence import EvidenceRecord
from domain.education.evidence.specifications.evidence_is_consistent import (
    EvidenceIsConsistentSpecification,
)
from domain.education.evidence.specifications.evidence_is_sufficient import (
    EvidenceIsSufficientSpecification,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.explainability import EducationalExplanation, ExplanationBuilder
from domain.mission_generation import MissionGenerator, MissionSpecification
from domain.progress_evaluation import ProgressEvaluator, ProgressReport
from domain.recommendation import RecommendationGenerator, RecommendationSpecification
from domain.student_experience import ExperienceGenerator, StudentExperience
from domain.study_planning import StudyPlan, StudyPlanner

logger = logging.getLogger(__name__)


class PipelineStage(str, Enum):
    """Canonical Educational Pipeline stage names in execution order."""

    ANALYSE_EVIDENCE = "analyse_evidence"
    GENERATE_MISSION = "generate_mission"
    BUILD_STUDY_PLAN = "build_study_plan"
    EVALUATE_PROGRESS = "evaluate_progress"
    GENERATE_RECOMMENDATIONS = "generate_recommendations"
    BUILD_EXPLANATION = "build_explanation"
    GENERATE_STUDENT_EXPERIENCE = "generate_student_experience"
    ENRICH_MISSION = "enrich_mission"
    ENRICH_RECOMMENDATIONS = "enrich_recommendations"


PIPELINE_STAGES: tuple[PipelineStage, ...] = tuple(PipelineStage)


class MissionEnrichmentPort(Protocol):
    """Outbound port for mission presentation enrichment."""

    def enrich(
        self,
        mission: MissionSpecification,
        experience: StudentExperience,
    ) -> EnhancedMissionView: ...


class RecommendationEnrichmentPort(Protocol):
    """Outbound port for recommendation presentation enrichment."""

    def enrich(
        self,
        recommendations: RecommendationSpecification,
        experience: StudentExperience,
    ) -> EnhancedRecommendationsView: ...


class EducationalPipeline:
    """Orchestrate the Educational Operating System from evidence to output.

    Idempotent and deterministic for domain stages. AI enrichment may vary;
    when the enricher is absent or raises, deterministic passthrough enrichment
    is returned so the pipeline still succeeds.
    """

    def __init__(
        self,
        *,
        mission_generator: type[MissionGenerator] = MissionGenerator,
        study_planner: type[StudyPlanner] = StudyPlanner,
        progress_evaluator: type[ProgressEvaluator] = ProgressEvaluator,
        recommendation_generator: type[
            RecommendationGenerator
        ] = RecommendationGenerator,
        explanation_builder: type[ExplanationBuilder] = ExplanationBuilder,
        experience_generator: type[ExperienceGenerator] = ExperienceGenerator,
        mission_enricher: MissionEnrichmentPort | None = None,
        recommendation_enricher: RecommendationEnrichmentPort | None = None,
    ) -> None:
        self._mission_generator = mission_generator
        self._study_planner = study_planner
        self._progress_evaluator = progress_evaluator
        self._recommendation_generator = recommendation_generator
        self._explanation_builder = explanation_builder
        self._experience_generator = experience_generator
        self._mission_enricher = mission_enricher
        self._recommendation_enricher = recommendation_enricher

    def run(self, request: PipelineRequest) -> PipelineResult:
        """Execute the full Educational Pipeline in canonical order.

        Args:
            request: Student identity, educational evidence, optional session
                context with Educational OS state for domain engines.

        Returns:
            PipelineResult with every stage artefact, including deterministic
            enrichment when AI is unavailable or fails.

        Raises:
            EducationalInvariantViolation: When evidence or session context is
                educationally insufficient for orchestration.
            ValueError: When ``student_id`` is empty.
        """
        if not isinstance(request.student_id, str) or not request.student_id.strip():
            raise ValueError("student_id must be a non-empty string")

        stages: list[str] = []

        evidence = self._analyse_evidence(request)
        stages.append(PipelineStage.ANALYSE_EVIDENCE.value)

        context = self._require_session_context(request)

        mission = self._generate_mission(request, context)
        stages.append(PipelineStage.GENERATE_MISSION.value)

        study_plan = self._build_study_plan(mission, context)
        stages.append(PipelineStage.BUILD_STUDY_PLAN.value)

        progress = self._evaluate_progress(evidence, study_plan, context)
        stages.append(PipelineStage.EVALUATE_PROGRESS.value)

        recommendations = self._generate_recommendations(
            mission, study_plan, progress, context
        )
        stages.append(PipelineStage.GENERATE_RECOMMENDATIONS.value)

        explanation = self._build_explanation(
            mission, study_plan, progress, recommendations
        )
        stages.append(PipelineStage.BUILD_EXPLANATION.value)

        experience = self._generate_student_experience(
            mission, study_plan, progress, recommendations
        )
        stages.append(PipelineStage.GENERATE_STUDENT_EXPERIENCE.value)

        enhanced_mission = self._enrich_mission(mission, experience)
        stages.append(PipelineStage.ENRICH_MISSION.value)

        enhanced_recommendations = self._enrich_recommendations(
            recommendations, experience
        )
        stages.append(PipelineStage.ENRICH_RECOMMENDATIONS.value)

        return PipelineResult(
            mission=mission,
            study_plan=study_plan,
            progress_report=progress,
            recommendations=recommendations,
            explanation=explanation,
            student_experience=experience,
            enhanced_mission=enhanced_mission,
            enhanced_recommendations=enhanced_recommendations,
            stages_completed=tuple(stages),
        )

    # --- Stages ----------------------------------------------------------------

    def _analyse_evidence(
        self, request: PipelineRequest
    ) -> tuple[EvidenceRecord, ...]:
        """Delegate sufficiency/consistency checks to domain specifications."""
        evidence = request.normalised_evidence()
        if not evidence:
            raise EducationalInvariantViolation(
                "educational_evidence must contain at least one record",
                invariant="EducationalPipeline.evidence.min_one",
            )
        sufficient = EvidenceIsSufficientSpecification()
        consistent = EvidenceIsConsistentSpecification()
        for record in evidence:
            if not isinstance(record, EvidenceRecord):
                raise EducationalInvariantViolation(
                    "educational_evidence items must be EvidenceRecord",
                    invariant="EducationalPipeline.evidence.item_type",
                )
            if record.student_id != request.student_id:
                raise EducationalInvariantViolation(
                    "evidence student_id must match pipeline request student_id",
                    invariant="EducationalPipeline.evidence.student_id",
                )
            sufficient.assert_satisfied_by(record)
            consistent.assert_satisfied_by(record)
        return evidence

    def _generate_mission(
        self,
        request: PipelineRequest,
        context: PipelineSessionContext,
    ) -> MissionSpecification:
        if context.twin.student_id != request.student_id:
            raise EducationalInvariantViolation(
                "session twin student_id must match pipeline request student_id",
                invariant="EducationalPipeline.twin.student_id",
            )
        return self._mission_generator.generate(
            context.twin,
            context.diagnosis,
            context.priority,
            context.strategy,
            trajectory=context.trajectory,
        )

    def _build_study_plan(
        self,
        mission: MissionSpecification,
        context: PipelineSessionContext,
    ) -> StudyPlan:
        trajectory = (
            context.trajectory
            if context.trajectory is not None
            else context.twin.trajectory
        )
        return self._study_planner.plan(
            (mission,),
            context.availability,
            trajectory,
            context.priority,
        )

    def _evaluate_progress(
        self,
        evidence: tuple[EvidenceRecord, ...],
        study_plan: StudyPlan,
        context: PipelineSessionContext,
    ) -> ProgressReport:
        plans = (*context.prior_study_plans, study_plan)
        return self._progress_evaluator.evaluate(
            context.twin,
            evidence,
            context.completed_missions,
            plans,
            trajectory=context.trajectory,
        )

    def _generate_recommendations(
        self,
        mission: MissionSpecification,
        study_plan: StudyPlan,
        progress: ProgressReport,
        context: PipelineSessionContext,
    ) -> RecommendationSpecification:
        return self._recommendation_generator.generate(
            context.twin,
            mission,
            study_plan,
            progress,
            context.diagnosis,
            context.priority,
            context.strategy,
        )

    def _build_explanation(
        self,
        mission: MissionSpecification,
        study_plan: StudyPlan,
        progress: ProgressReport,
        recommendations: RecommendationSpecification,
    ) -> EducationalExplanation:
        return self._explanation_builder.build(
            mission,
            study_plan,
            progress,
            recommendations,
        )

    def _generate_student_experience(
        self,
        mission: MissionSpecification,
        study_plan: StudyPlan,
        progress: ProgressReport,
        recommendations: RecommendationSpecification,
    ) -> StudentExperience:
        return self._experience_generator.generate(
            mission,
            study_plan,
            progress,
            recommendations,
        )

    def _enrich_mission(
        self,
        mission: MissionSpecification,
        experience: StudentExperience,
    ) -> EnhancedMissionView:
        if self._mission_enricher is None:
            return deterministic_enhanced_mission(mission)
        try:
            return self._mission_enricher.enrich(mission, experience)
        except Exception:
            logger.warning(
                "mission enrichment failed; returning deterministic enrichment",
                exc_info=True,
            )
            return deterministic_enhanced_mission(mission)

    def _enrich_recommendations(
        self,
        recommendations: RecommendationSpecification,
        experience: StudentExperience,
    ) -> EnhancedRecommendationsView:
        if self._recommendation_enricher is None:
            return deterministic_enhanced_recommendations(recommendations)
        try:
            return self._recommendation_enricher.enrich(recommendations, experience)
        except Exception:
            logger.warning(
                "recommendation enrichment failed; returning deterministic enrichment",
                exc_info=True,
            )
            return deterministic_enhanced_recommendations(recommendations)

    @staticmethod
    def _require_session_context(
        request: PipelineRequest,
    ) -> PipelineSessionContext:
        if request.session_context is None:
            raise EducationalInvariantViolation(
                "session_context is required to run domain engines",
                invariant="EducationalPipeline.session_context.required",
            )
        return request.session_context
