"""Architecture purity for AP-002D6 Tutor explainability."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

DOMAIN_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "domain"
    / "intelligent_tutor"
    / "explainability"
)
APPLICATION_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "application"
    / "intelligent_tutor"
    / "explainability"
)

FORBIDDEN_MODULES = frozenset(
    {
        "flask",
        "jinja2",
        "wtforms",
        "requests",
        "httpx",
    }
)
FORBIDDEN_PREFIXES = (
    "app.presentation.",
    "app.templates",
    "app.application.assessment",
    "app.application.student_digital_twin.student_reasoning_service",
    "app.application.reasoning.decisions",
    "app.application.mission_engine.planning.candidate_builder",
    "domain.assessment.packaging",
    "domain.assessment.aggregation",
)
FORBIDDEN_SUBSTRINGS = (
    "StudentReasoningService",
    "EvidenceBundle",
    "EvidencePackagingService",
    "TwinUpdater",
    "DecisionGenerator",
    "CandidateBuilder",
)


def _iter_python_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.py"))


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


def test_required_explainability_structure_exists() -> None:
    assert DOMAIN_ROOT.is_dir()
    assert APPLICATION_ROOT.is_dir()
    for name in (
        "context.py",
        "reference.py",
        "section.py",
        "explanation.py",
        "events.py",
        "result.py",
        "version.py",
        "errors.py",
    ):
        assert (DOMAIN_ROOT / name).is_file(), name
    for name in (
        "tutor_explanation_service.py",
        "explanation_builder.py",
        "validator.py",
        "persistence.py",
        "versions.py",
    ):
        assert (APPLICATION_ROOT / name).is_file(), name
    assert (
        Path(__file__).resolve().parents[3]
        / "app"
        / "application"
        / "intelligent_tutor"
        / "dto"
        / "explanation_dto.py"
    ).is_file()
    assert (
        Path(__file__).resolve().parents[3]
        / "app"
        / "application"
        / "intelligent_tutor"
        / "mappers"
        / "explanation_mapper.py"
    ).is_file()


@pytest.mark.parametrize(
    "path",
    _iter_python_files(DOMAIN_ROOT) + _iter_python_files(APPLICATION_ROOT),
    ids=lambda p: str(p.relative_to(p.parents[4])),
)
def test_explainability_packages_have_no_forbidden_authority_imports(
    path: Path,
) -> None:
    imported = _imported_modules(path)
    text = path.read_text(encoding="utf-8")
    for name in imported:
        root = name.split(".", 1)[0]
        assert root not in FORBIDDEN_MODULES, f"{path.name} imports {name}"
        for prefix in FORBIDDEN_PREFIXES:
            assert not name.startswith(prefix), f"{path.name} imports {name}"
    for needle in FORBIDDEN_SUBSTRINGS:
        if needle in ("EvidenceBundle",):
            if path.is_relative_to(APPLICATION_ROOT) and f"import {needle}" in text:
                pytest.fail(f"{path.name} must not import {needle}")
            continue
        if needle in text and (
            f"import {needle}" in text or f"{needle}(" in text
        ):
            pytest.fail(f"{path.name} must not reference {needle}")


def test_domain_explainability_does_not_import_application() -> None:
    for path in _iter_python_files(DOMAIN_ROOT):
        imported = _imported_modules(path)
        for name in imported:
            assert not name.startswith("app.application."), path.name


def test_explanation_service_does_not_write_twin_belief_or_reason() -> None:
    path = APPLICATION_ROOT / "tutor_explanation_service.py"
    text = path.read_text(encoding="utf-8")
    for banned in (
        "with_inferences",
        "TwinUpdater",
        "MasteryService",
        "KnowledgeGapService",
        "StudentReasoningService",
        "reason(",
        "DecisionGenerator",
    ):
        assert banned not in text


def test_explanation_builder_does_not_consume_assessment_authority() -> None:
    path = APPLICATION_ROOT / "explanation_builder.py"
    text = path.read_text(encoding="utf-8")
    for banned in (
        "EvidenceBundle",
        "AssessmentResponse",
        "QuestionAttempt",
        "ObservationService",
        "StudentReasoningService",
    ):
        assert banned not in text
