"""Framework independence and package isolation tests."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

APP_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "application"
    / "education_platform"
)

FORBIDDEN_MODULES = (
    "flask",
    "sqlalchemy",
    "app.extensions",
    "app.models",
    "app.services",
    "app.curriculum",
    "app.domain.curriculum",
    "app.application.instructional_blueprint",
    "app.application.learning_journey",
    "app.application.learning_session",
    "app.application.learning_activity",
    "app.application.mission_engine",
    "app.application.mission_engine_v2",
    "app.application.mission_adapter",
)


def _offenders(root: Path) -> list[str]:
    found: list[str] = []
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if any(
                        alias.name == f or alias.name.startswith(f + ".")
                        for f in FORBIDDEN_MODULES
                    ):
                        found.append(f"{path}: import {alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                if any(
                    node.module == f or node.module.startswith(f + ".")
                    for f in FORBIDDEN_MODULES
                ):
                    found.append(f"{path}: from {node.module}")
    return found


def test_no_forbidden_imports():
    assert _offenders(APP_ROOT) == []


def test_no_flask_sqlalchemy_in_source():
    for path in APP_ROOT.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith("flask")
                    assert not alias.name.startswith("sqlalchemy")
            elif isinstance(node, ast.ImportFrom) and node.module:
                assert not node.module.startswith("flask")
                assert not node.module.startswith("sqlalchemy")


def test_import_platform_without_app_context():
    from app.application.education_platform.platform import EducationPlatform

    platform = EducationPlatform.create()
    assert platform.health_status()["platform_status"] == "degraded"


def test_ports_are_protocol_only():
    from typing import Protocol

    from app.application.education_platform.ports.curriculum_port import (
        CurriculumPort,
    )

    assert issubclass(CurriculumPort, Protocol)


def test_no_engine_instantiation_in_package():
    forbidden_snippets = (
        "InstructionalBlueprintEngine(",
        "LearningJourneyEngine(",
        "LearningSessionRuntime(",
        "LearningActivityEngine(",
        "MissionEngineV2(",
        "MissionEngine(",
        "MissionAdapter(",
        "CurriculumNavigationService(",
    )
    for path in APP_ROOT.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for snippet in forbidden_snippets:
            assert snippet not in text, f"{path} contains {snippet}"


def test_exceptions_hierarchy():
    from app.application.education_platform.exceptions import (
        CompositionError,
        DependencyError,
        EducationPlatformError,
        OrchestrationError,
        PortUnavailable,
        ValidationError,
        WorkflowError,
    )

    for cls in (
        DependencyError,
        ValidationError,
        WorkflowError,
        OrchestrationError,
        CompositionError,
        PortUnavailable,
    ):
        assert issubclass(cls, EducationPlatformError)


@pytest.mark.parametrize(
    "name",
    [
        "EducationPlatform",
        "CompositionRoot",
        "DependencyRegistry",
        "EducationRequest",
        "EducationResponse",
        "OrchestrationPolicy",
        "ValidationPolicy",
        "CurriculumPort",
        "BlueprintPort",
        "JourneyPort",
        "SessionPort",
        "ActivityPort",
        "MissionPort",
    ],
)
def test_package_exports(name):
    import app.application.education_platform as pkg

    assert hasattr(pkg, name)


def test_no_ai_or_content_generation_markers():
    for path in APP_ROOT.rglob("*.py"):
        text = path.read_text(encoding="utf-8").lower()
        for banned in ("openai", "anthropic", "langchain", "llm_client"):
            assert banned not in text


def test_required_files_exist():
    required = [
        "__init__.py",
        "platform.py",
        "composition_root.py",
        "platform_context.py",
        "orchestration_service.py",
        "dependency_registry.py",
        "platform_validator.py",
        "workflow_executor.py",
        "health_service.py",
        "diagnostics.py",
        "exceptions.py",
        "ports/curriculum_port.py",
        "ports/blueprint_port.py",
        "ports/journey_port.py",
        "ports/session_port.py",
        "ports/activity_port.py",
        "ports/mission_port.py",
        "dto/education_request.py",
        "dto/education_response.py",
        "dto/subject_plan.py",
        "dto/generated_session.py",
        "dto/generated_mission.py",
        "dto/platform_snapshot.py",
        "dto/workflow_result.py",
        "policies/orchestration_policy.py",
        "policies/validation_policy.py",
    ]
    for rel in required:
        assert (APP_ROOT / rel).is_file(), rel
