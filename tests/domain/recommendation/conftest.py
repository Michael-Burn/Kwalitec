"""Shared factories for Recommendation Engine domain tests (EDU-004)."""

from __future__ import annotations

import pytest

from domain.education.diagnosis import (
    DiagnosisSeverity,
    DiagnosisSeverityLevel,
    EducationalDiagnosis,
)
from domain.education.digital_twin import EducationalDigitalTwin
from domain.education.foundation.enums import (
    DiagnosisType,
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.ids import DiagnosisId
from domain.education.priority import (
    EducationalPriority,
    PriorityFactorKind,
    PriorityScoreBand,
    UrgencyLevel,
)
from domain.education.teaching_strategy import (
    ComplexityLevel,
    InstructionalComplexity,
    TeachingStrategy,
)
from domain.mission_generation import MissionSpecification
from domain.progress_evaluation import ProgressReport
from domain.recommendation import RecommendationGenerator, RecommendationSpecification
from domain.study_planning import StudyPlan
from tests.domain.education.diagnosis.conftest import make_diagnosis, make_severity
from tests.domain.education.priority.conftest import (
    make_diagnosis_ref as make_priority_diagnosis_ref,
)
from tests.domain.education.priority.conftest import (
    make_factor,
    make_priority,
    make_score,
    make_urgency,
)
from tests.domain.education.teaching_strategy.conftest import (
    INTENTION_DIAGNOSIS,
    INTENTION_STRATEGY,
    make_complexity,
    make_strategy,
)
from tests.domain.education.teaching_strategy.conftest import (
    make_diagnosis_ref as make_strategy_diagnosis_ref,
)
from tests.domain.mission_generation.conftest import generate_mission
from tests.domain.progress_evaluation.conftest import (
    evaluate_progress,
    make_completed_mission,
    make_evidence_batch,
    make_progress_twin,
)
from tests.domain.study_planning.conftest import plan_study

DEFAULT_DIAGNOSIS_TYPE = DiagnosisType.PROCEDURAL_WEAKNESS
DEFAULT_INTENTION = TeachingIntentionType.INCREASE_PROCEDURAL_FLUENCY
DEFAULT_STRATEGY = TeachingStrategyType.PROGRESSIVE_SCAFFOLDING
DEFAULT_PRIORITY_FACTOR = PriorityFactorKind.CONCEPT_CENTRALITY

_DIAGNOSIS_INTENTION: dict[DiagnosisType, TeachingIntentionType] = {
    diagnosis: intention for intention, diagnosis in INTENTION_DIAGNOSIS.items()
}


@pytest.fixture
def student_id() -> str:
    return "student-ada"


def intention_for(diagnosis_type: DiagnosisType) -> TeachingIntentionType:
    return _DIAGNOSIS_INTENTION.get(diagnosis_type, DEFAULT_INTENTION)


def strategy_for(diagnosis_type: DiagnosisType) -> TeachingStrategyType:
    return INTENTION_STRATEGY[intention_for(diagnosis_type)]


def make_aligned_diagnosis(
    *,
    diagnosis_id: str = "diag-001",
    student_id: str = "student-ada",
    diagnosis_type: DiagnosisType = DEFAULT_DIAGNOSIS_TYPE,
    severity: DiagnosisSeverity | None = None,
) -> EducationalDiagnosis:
    return make_diagnosis(
        diagnosis_id=diagnosis_id,
        student_id=student_id,
        diagnosis_type=diagnosis_type,
        severity=severity or make_severity(DiagnosisSeverityLevel.MODERATE),
    )


def make_aligned_priority(
    *,
    priority_id: str = "prio-001",
    student_id: str = "student-ada",
    diagnosis_id: str | DiagnosisId = "diag-001",
    diagnosis_type: DiagnosisType = DEFAULT_DIAGNOSIS_TYPE,
    score_band: PriorityScoreBand = PriorityScoreBand.HIGH,
    urgency_level: UrgencyLevel = UrgencyLevel.ELEVATED,
    peak_factor_kind: PriorityFactorKind = DEFAULT_PRIORITY_FACTOR,
) -> EducationalPriority:
    return make_priority(
        priority_id=priority_id,
        student_id=student_id,
        diagnosis_references=[
            make_priority_diagnosis_ref(
                diagnosis_id=diagnosis_id,
                diagnosis_type=diagnosis_type,
            )
        ],
        factors=[
            make_factor(
                kind=peak_factor_kind,
                contribution=0.85,
            )
        ],
        score=make_score(score_band),
        urgency=make_urgency(urgency_level),
        calculate=False,
    )


def make_aligned_strategy(
    *,
    strategy_id: str = "ts-001",
    student_id: str = "student-ada",
    diagnosis_id: str | DiagnosisId = "diag-001",
    diagnosis_type: DiagnosisType = DEFAULT_DIAGNOSIS_TYPE,
    primary_strategy: TeachingStrategyType | None = None,
    intention_type: TeachingIntentionType | None = None,
    complexity: InstructionalComplexity | None = None,
) -> TeachingStrategy:
    intention = intention_type or intention_for(diagnosis_type)
    return make_strategy(
        strategy_id=strategy_id,
        student_id=student_id,
        primary_strategy=primary_strategy or INTENTION_STRATEGY[intention],
        intention_type=intention,
        diagnosis_references=[
            make_strategy_diagnosis_ref(
                diagnosis_id=diagnosis_id,
                diagnosis_type=diagnosis_type,
            )
        ],
        complexity=complexity or make_complexity(ComplexityLevel.MODERATE),
        select=True,
    )


def make_recommendation_inputs(
    *,
    diagnosis_type: DiagnosisType = DEFAULT_DIAGNOSIS_TYPE,
    severity: DiagnosisSeverityLevel = DiagnosisSeverityLevel.MODERATE,
    score_band: PriorityScoreBand = PriorityScoreBand.HIGH,
    urgency_level: UrgencyLevel = UrgencyLevel.ELEVATED,
    peak_factor_kind: PriorityFactorKind = DEFAULT_PRIORITY_FACTOR,
    complexity: ComplexityLevel = ComplexityLevel.MODERATE,
    with_misconception: bool = False,
    evidence_strengths: tuple[str, ...] = ("strong", "strong", "strong", "strong"),
    completed_success: bool = True,
) -> tuple[
    EducationalDigitalTwin,
    MissionSpecification,
    StudyPlan,
    ProgressReport,
    EducationalDiagnosis,
    EducationalPriority,
    TeachingStrategy,
]:
    twin = make_progress_twin(with_misconception=with_misconception)
    diagnosis = make_aligned_diagnosis(
        diagnosis_type=diagnosis_type,
        severity=make_severity(severity),
    )
    priority = make_aligned_priority(
        diagnosis_type=diagnosis_type,
        score_band=score_band,
        urgency_level=urgency_level,
        peak_factor_kind=peak_factor_kind,
    )
    strategy = make_aligned_strategy(
        diagnosis_type=diagnosis_type,
        complexity=make_complexity(complexity),
    )
    mission = generate_mission(
        twin=twin,
        diagnosis=diagnosis,
        priority=priority,
        strategy=strategy,
    )
    study_plan = plan_study(
        missions=(mission,),
        priority=priority,
    )
    progress = evaluate_progress(
        twin=twin,
        evidence=make_evidence_batch(strengths=evidence_strengths),
        completed_missions=(
            make_completed_mission(success=completed_success),
        ),
        study_plans=(study_plan,),
    )
    return twin, mission, study_plan, progress, diagnosis, priority, strategy


def generate_recommendations(
    *,
    twin: EducationalDigitalTwin | None = None,
    mission: MissionSpecification | None = None,
    study_plan: StudyPlan | None = None,
    progress: ProgressReport | None = None,
    diagnosis: EducationalDiagnosis | None = None,
    priority: EducationalPriority | None = None,
    strategy: TeachingStrategy | None = None,
    **input_kwargs: object,
) -> RecommendationSpecification:
    if any(
        value is None
        for value in (
            twin,
            mission,
            study_plan,
            progress,
            diagnosis,
            priority,
            strategy,
        )
    ):
        (
            twin,
            mission,
            study_plan,
            progress,
            diagnosis,
            priority,
            strategy,
        ) = make_recommendation_inputs(**input_kwargs)  # type: ignore[arg-type]
    assert twin is not None
    assert mission is not None
    assert study_plan is not None
    assert progress is not None
    assert diagnosis is not None
    assert priority is not None
    assert strategy is not None
    return RecommendationGenerator.generate(
        twin,
        mission,
        study_plan,
        progress,
        diagnosis,
        priority,
        strategy,
    )
