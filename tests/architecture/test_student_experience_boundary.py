"""Student Experience cannot change educational decisions (APP-003)."""

from __future__ import annotations

import pytest

from tests.architecture import (
    DOMAIN_ROOT,
    EDUCATIONAL_DECISION_METHODS,
    defined_function_names,
    imported_modules,
    iter_python_files,
)

EXPERIENCE_ROOT = DOMAIN_ROOT / "student_experience"

FORBIDDEN_ENGINE_IMPORTS = (
    "domain.mission_generation.mission_generator",
    "domain.recommendation.recommendation_generator",
    "domain.study_planning.study_planner",
    "domain.progress_evaluation.progress_evaluator",
    "domain.education.diagnosis",
    "domain.education.decision",
    "domain.education.priority",
    "domain.education.teaching_strategy",
)

FORBIDDEN_MUTATION_TOKENS = (
    "rewrite_mission",
    "mutate_recommendation",
    "change_recommendation",
    "MissionGenerator",
    "RecommendationGenerator",
    "StudyPlanner",
    "ProgressEvaluator",
)


@pytest.mark.parametrize(
    "path",
    iter_python_files(EXPERIENCE_ROOT),
    ids=lambda p: str(p.relative_to(EXPERIENCE_ROOT)),
)
def test_student_experience_defines_no_educational_decision_methods(path) -> None:
    defined = defined_function_names(path)
    for name in EDUCATIONAL_DECISION_METHODS:
        assert name not in defined, f"{path.name} defines educational method {name}"


@pytest.mark.parametrize(
    "path",
    iter_python_files(EXPERIENCE_ROOT),
    ids=lambda p: str(p.relative_to(EXPERIENCE_ROOT)),
)
def test_student_experience_does_not_import_decision_engines(path) -> None:
    imported = imported_modules(path)
    for name in imported:
        for forbidden in FORBIDDEN_ENGINE_IMPORTS:
            assert not (
                name == forbidden or name.startswith(forbidden + ".")
            ), f"{path.name} imports educational decision module {name}"


@pytest.mark.parametrize(
    "path",
    iter_python_files(EXPERIENCE_ROOT),
    ids=lambda p: str(p.relative_to(EXPERIENCE_ROOT)),
)
def test_student_experience_source_has_no_mutation_authority(path) -> None:
    source = path.read_text(encoding="utf-8")
    for token in FORBIDDEN_MUTATION_TOKENS:
        assert token not in source, (
            f"{path.name} references educational mutation authority ({token})"
        )
