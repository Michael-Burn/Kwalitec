"""AI cannot change educational decisions (APP-003)."""

from __future__ import annotations

import pytest

from tests.architecture import (
    EDUCATIONAL_DECISION_METHODS,
    INFRASTRUCTURE_ROOT,
    defined_function_names,
    imported_modules,
    iter_python_files,
)

AI_ROOT = INFRASTRUCTURE_ROOT / "ai"

FORBIDDEN_DECISION_ENGINE_IMPORTS = (
    "domain.mission_generation.mission_generator",
    "domain.recommendation.recommendation_generator",
    "domain.study_planning.study_planner",
    "domain.progress_evaluation.progress_evaluator",
    "domain.education.diagnosis",
    "domain.education.decision",
    "domain.education.priority",
    "domain.education.orchestrator",
    "domain.education.teaching_strategy",
)

FORBIDDEN_AUTHORITY_TOKENS = (
    "MissionGenerator",
    "RecommendationGenerator",
    "StudyPlanner",
    "ProgressEvaluator",
    "ExperienceGenerator",
)


@pytest.mark.parametrize(
    "path",
    iter_python_files(AI_ROOT),
    ids=lambda p: str(p.relative_to(AI_ROOT)),
)
def test_ai_defines_no_educational_decision_methods(path) -> None:
    defined = defined_function_names(path)
    for name in EDUCATIONAL_DECISION_METHODS:
        assert name not in defined, f"{path.name} defines educational method {name}"


@pytest.mark.parametrize(
    "path",
    iter_python_files(AI_ROOT),
    ids=lambda p: str(p.relative_to(AI_ROOT)),
)
def test_ai_does_not_import_educational_decision_engines(path) -> None:
    for name in imported_modules(path):
        for forbidden in FORBIDDEN_DECISION_ENGINE_IMPORTS:
            assert not (
                name == forbidden or name.startswith(forbidden + ".")
            ), f"{path.name} imports educational decision module {name}"


@pytest.mark.parametrize(
    "path",
    iter_python_files(AI_ROOT),
    ids=lambda p: str(p.relative_to(AI_ROOT)),
)
def test_ai_source_has_no_decision_engine_authority(path) -> None:
    source = path.read_text(encoding="utf-8")
    for token in FORBIDDEN_AUTHORITY_TOKENS:
        assert token not in source, (
            f"{path.name} references educational decision authority ({token})"
        )
