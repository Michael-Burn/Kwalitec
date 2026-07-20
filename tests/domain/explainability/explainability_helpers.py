"""Shared helpers for Educational Explainability Engine domain tests (EDU-005)."""

from __future__ import annotations

from domain.education.foundation.enums import DiagnosisType
from domain.explainability import EducationalExplanation, ExplanationBuilder
from domain.mission_generation import MissionSpecification
from domain.progress_evaluation import ProgressReport
from domain.recommendation import RecommendationSpecification
from domain.study_planning import StudyPlan
from tests.domain.progress_evaluation.conftest import (
    evaluate_progress,
    make_completed_mission,
    make_evidence_batch,
)
from tests.domain.recommendation.conftest import (
    generate_recommendations,
    make_recommendation_inputs,
)


def make_explanation_inputs(
    *,
    diagnosis_type: DiagnosisType = DiagnosisType.PROCEDURAL_WEAKNESS,
    completed_success: bool = True,
    completed_mission_count: int = 1,
) -> tuple[
    MissionSpecification,
    StudyPlan,
    ProgressReport,
    RecommendationSpecification,
]:
    twin, mission, study_plan, _progress, diagnosis, priority, strategy = (
        make_recommendation_inputs(
            diagnosis_type=diagnosis_type,
            completed_success=completed_success,
        )
    )
    completed = (
        make_completed_mission(
            mission_id=mission.mission_id.value,
            completion_sequence=1,
            success=completed_success,
        ),
        *tuple(
            make_completed_mission(
                mission_id=f"mission-extra-{index:03d}",
                completion_sequence=index,
                success=completed_success,
            )
            for index in range(2, completed_mission_count + 1)
        ),
    )
    progress = evaluate_progress(
        twin=twin,
        evidence=make_evidence_batch(),
        completed_missions=completed,
        study_plans=(study_plan,),
    )
    recommendations = generate_recommendations(
        twin=twin,
        mission=mission,
        study_plan=study_plan,
        progress=progress,
        diagnosis=diagnosis,
        priority=priority,
        strategy=strategy,
    )
    return mission, study_plan, progress, recommendations


def generate_explanation(
    *,
    mission: MissionSpecification | None = None,
    study_plan: StudyPlan | None = None,
    progress: ProgressReport | None = None,
    recommendations: RecommendationSpecification | None = None,
    **input_kwargs: object,
) -> EducationalExplanation:
    if any(
        value is None
        for value in (mission, study_plan, progress, recommendations)
    ):
        mission, study_plan, progress, recommendations = make_explanation_inputs(
            **input_kwargs  # type: ignore[arg-type]
        )
    assert mission is not None
    assert study_plan is not None
    assert progress is not None
    assert recommendations is not None
    return ExplanationBuilder.build(
        mission,
        study_plan,
        progress,
        recommendations,
    )
