"""Tests for APP-002 Educational Pipeline Orchestrator."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

import pytest

from application.pipeline import (
    PIPELINE_STAGES,
    EducationalPipeline,
    PipelineRequest,
    PipelineResult,
    PipelineSessionContext,
    PipelineStage,
    deterministic_enhanced_mission,
    deterministic_enhanced_recommendations,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.explainability import EducationalExplanation
from domain.mission_generation import MissionSpecification
from domain.progress_evaluation import ProgressReport
from domain.recommendation import RecommendationSpecification
from domain.student_experience import StudentExperience
from domain.study_planning import StudyPlan
from infrastructure.ai.enrichment.mission_enricher import MissionEnricher
from infrastructure.ai.enrichment.recommendation_enricher import RecommendationEnricher
from infrastructure.ai.providers.ai_provider import AIProviderError
from tests.domain.mission_generation.conftest import (
    make_aligned_diagnosis,
    make_aligned_priority,
    make_aligned_strategy,
)
from tests.domain.progress_evaluation.conftest import (
    make_completed_mission,
    make_evidence_batch,
    make_progress_twin,
)
from tests.domain.study_planning.conftest import make_availability, make_trajectory
from tests.education_os.infrastructure.ai.helpers import FakeAIProvider

PIPELINE_ROOT = (
    Path(__file__).resolve().parents[4] / "src" / "application" / "pipeline"
)

FORBIDDEN_MODULES = frozenset(
    {
        "flask",
        "sqlalchemy",
        "alembic",
        "jinja2",
        "wtforms",
        "requests",
        "httpx",
        "celery",
        "redis",
        "boto3",
    }
)

FORBIDDEN_PREFIXES = (
    "flask.",
    "sqlalchemy.",
    "app.",
    "infrastructure.",
)


def make_session_context(
    *,
    student_id: str = "student-ada",
    completed_success: bool = True,
) -> PipelineSessionContext:
    twin = make_progress_twin(student_id=student_id)
    diagnosis = make_aligned_diagnosis(student_id=student_id)
    priority = make_aligned_priority(student_id=student_id)
    strategy = make_aligned_strategy(student_id=student_id)
    return PipelineSessionContext(
        twin=twin,
        diagnosis=diagnosis,
        priority=priority,
        strategy=strategy,
        availability=make_availability(student_id=student_id),
        trajectory=make_trajectory(),
        completed_missions=(
            make_completed_mission(
                mission_id="mission-prior-001",
                completion_sequence=1,
                success=completed_success,
            ),
        ),
        prior_study_plans=(),
    )


def make_pipeline_request(
    *,
    student_id: str = "student-ada",
    session_context: PipelineSessionContext | None = None,
    include_context: bool = True,
) -> PipelineRequest:
    evidence = make_evidence_batch(student_id=student_id)
    context = session_context
    if include_context and context is None:
        context = make_session_context(student_id=student_id)
    return PipelineRequest(
        student_id=student_id,
        educational_evidence=evidence,
        session_context=context,
    )


class FailingMissionEnricher:
    def enrich(self, mission: MissionSpecification, experience: StudentExperience):
        raise AIProviderError("mission enrichment unavailable")


class FailingRecommendationEnricher:
    def enrich(
        self,
        recommendations: RecommendationSpecification,
        experience: StudentExperience,
    ):
        raise AIProviderError("recommendation enrichment unavailable")


class RecordingPipeline(EducationalPipeline):
    """Pipeline that records stage entry order for orchestration assertions."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.entered: list[str] = []

    def _analyse_evidence(self, request: PipelineRequest):
        self.entered.append(PipelineStage.ANALYSE_EVIDENCE.value)
        return super()._analyse_evidence(request)

    def _generate_mission(
        self, request: PipelineRequest, context: PipelineSessionContext
    ):
        self.entered.append(PipelineStage.GENERATE_MISSION.value)
        return super()._generate_mission(request, context)

    def _build_study_plan(self, mission, context):
        self.entered.append(PipelineStage.BUILD_STUDY_PLAN.value)
        return super()._build_study_plan(mission, context)

    def _evaluate_progress(self, evidence, study_plan, context):
        self.entered.append(PipelineStage.EVALUATE_PROGRESS.value)
        return super()._evaluate_progress(evidence, study_plan, context)

    def _generate_recommendations(self, mission, study_plan, progress, context):
        self.entered.append(PipelineStage.GENERATE_RECOMMENDATIONS.value)
        return super()._generate_recommendations(
            mission, study_plan, progress, context
        )

    def _build_explanation(self, mission, study_plan, progress, recommendations):
        self.entered.append(PipelineStage.BUILD_EXPLANATION.value)
        return super()._build_explanation(
            mission, study_plan, progress, recommendations
        )

    def _generate_student_experience(
        self, mission, study_plan, progress, recommendations
    ):
        self.entered.append(PipelineStage.GENERATE_STUDENT_EXPERIENCE.value)
        return super()._generate_student_experience(
            mission, study_plan, progress, recommendations
        )

    def _enrich_mission(self, mission, experience):
        self.entered.append(PipelineStage.ENRICH_MISSION.value)
        return super()._enrich_mission(mission, experience)

    def _enrich_recommendations(self, recommendations, experience):
        self.entered.append(PipelineStage.ENRICH_RECOMMENDATIONS.value)
        return super()._enrich_recommendations(recommendations, experience)


def _assert_result_complete(result: PipelineResult) -> None:
    assert isinstance(result.mission, MissionSpecification)
    assert isinstance(result.study_plan, StudyPlan)
    assert isinstance(result.progress_report, ProgressReport)
    assert isinstance(result.recommendations, RecommendationSpecification)
    assert isinstance(result.explanation, EducationalExplanation)
    assert isinstance(result.student_experience, StudentExperience)
    assert result.enhanced_mission.specification is result.mission
    assert result.enhanced_recommendations.specification is result.recommendations
    assert result.recommendation_specifications == (result.recommendations,)
    assert result.stages_completed == tuple(stage.value for stage in PIPELINE_STAGES)


def test_happy_path_with_ai_enrichment() -> None:
    provider = FakeAIProvider(name="fake-pipeline")
    pipeline = EducationalPipeline(
        mission_enricher=MissionEnricher(provider),
        recommendation_enricher=RecommendationEnricher(provider),
    )

    result = pipeline.run(make_pipeline_request())

    _assert_result_complete(result)
    assert result.enhanced_mission.provider_name == "fake-pipeline"
    assert result.enhanced_recommendations.provider_name == "fake-pipeline"
    assert result.enhanced_mission.improved_wording
    assert result.enhanced_recommendations.improved_wording
    assert len(provider.prompts) == 2


def test_no_ai_provider_returns_deterministic_enrichment() -> None:
    pipeline = EducationalPipeline()

    result = pipeline.run(make_pipeline_request())

    _assert_result_complete(result)
    assert result.enhanced_mission.provider_name == "none"
    assert result.enhanced_recommendations.provider_name == "none"
    expected_mission = deterministic_enhanced_mission(result.mission)
    expected_recs = deterministic_enhanced_recommendations(result.recommendations)
    assert result.enhanced_mission.improved_wording == expected_mission.improved_wording
    assert (
        result.enhanced_recommendations.improved_wording
        == expected_recs.improved_wording
    )


def test_ai_provider_failure_does_not_fail_pipeline() -> None:
    pipeline = EducationalPipeline(
        mission_enricher=FailingMissionEnricher(),
        recommendation_enricher=FailingRecommendationEnricher(),
    )

    result = pipeline.run(make_pipeline_request())

    _assert_result_complete(result)
    assert result.enhanced_mission.provider_name == "none"
    assert result.enhanced_recommendations.provider_name == "none"
    assert result.enhanced_mission.specification is result.mission
    assert result.enhanced_recommendations.specification is result.recommendations


def test_deterministic_domain_outputs() -> None:
    request = make_pipeline_request()
    pipeline = EducationalPipeline()

    first = pipeline.run(request)
    second = pipeline.run(request)

    assert first.mission == second.mission
    assert first.study_plan == second.study_plan
    assert first.progress_report == second.progress_report
    assert first.recommendations == second.recommendations
    assert first.explanation == second.explanation
    assert first.student_experience == second.student_experience
    assert first.enhanced_mission == second.enhanced_mission
    assert first.enhanced_recommendations == second.enhanced_recommendations
    assert first.stages_completed == second.stages_completed


def test_correct_orchestration_order() -> None:
    pipeline = RecordingPipeline()

    result = pipeline.run(make_pipeline_request())

    expected = [stage.value for stage in PIPELINE_STAGES]
    assert pipeline.entered == expected
    assert result.stages_completed == tuple(expected)


def test_pipeline_result_completeness() -> None:
    result = EducationalPipeline().run(make_pipeline_request())

    _assert_result_complete(result)
    assert result.mission.student_id == "student-ada"
    assert result.study_plan.student_id == "student-ada"
    assert result.progress_report.student_id == "student-ada"
    assert result.recommendations.student_id == "student-ada"
    assert result.explanation.student_id == "student-ada"
    assert result.student_experience.student_id == "student-ada"
    assert result.recommendations.recommendations


def test_missing_session_context_raises() -> None:
    request = make_pipeline_request(include_context=False)
    with pytest.raises(EducationalInvariantViolation, match="session_context"):
        EducationalPipeline().run(request)


def test_empty_student_id_raises() -> None:
    request = PipelineRequest(
        student_id="  ",
        educational_evidence=make_evidence_batch(),
        session_context=make_session_context(),
    )
    with pytest.raises(ValueError, match="student_id"):
        EducationalPipeline().run(request)


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


@pytest.mark.parametrize(
    "path",
    sorted(PIPELINE_ROOT.rglob("*.py")),
    ids=lambda p: str(p.relative_to(PIPELINE_ROOT)),
)
def test_architecture_purity(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    assert "from __future__ import annotations" in source
    assert "flask.request" not in source
    assert "Blueprint(" not in source
    assert "create_engine" not in source.lower()
    assert "sessionmaker" not in source.lower()

    imported = _imported_modules(path)
    for name in imported:
        assert name not in FORBIDDEN_MODULES, f"{path.name} imports {name}"
        assert not any(
            name == prefix.rstrip(".") or name.startswith(prefix)
            for prefix in FORBIDDEN_PREFIXES
        ), f"{path.name} imports forbidden module {name}"


def test_pipeline_defines_no_educational_intelligence_methods() -> None:
    forbidden = {
        "diagnose",
        "calculate_mastery",
        "prioritise",
        "prioritize",
        "choose_strategy",
        "select_strategy",
        "interpret_evidence",
        "create_hypothesis",
    }
    for path in PIPELINE_ROOT.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        defined = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        }
        for name in forbidden:
            assert name not in defined, f"{path.name} defines {name}"
