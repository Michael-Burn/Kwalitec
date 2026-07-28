"""Architecture purity for Educational Intelligence pipeline orchestration."""

from __future__ import annotations

import ast
from pathlib import Path

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "application"
    / "educational_intelligence_pipeline"
)

FORBIDDEN_ROOT_MODULES = frozenset(
    {
        "flask",
        "sqlalchemy",
        "alembic",
        "jinja2",
        "wtforms",
        "openai",
        "anthropic",
        "numpy",
        "scipy",
        "sklearn",
        "celery",
        "redis",
    }
)

FORBIDDEN_PREFIXES = (
    "flask.",
    "sqlalchemy.",
    "openai.",
    "anthropic.",
    "app.auth.",
    "app.dashboard.",
    "app.founder.",
    "app.templates",
    "app.models.",
)

# Orchestrator must not invent educational algorithms.
FORBIDDEN_METHOD_NAMES = frozenset(
    {
        "estimate_mastery_score",
        "calculate_mastery",
        "compute_mastery",
        "score_mastery",
        "rank_recommendations",
        "prioritise_recommendations",
        "prioritize_recommendations",
        "select_recommendation",
        "diagnose",
        "choose_strategy",
        "generate_mission",
        "invoke_ai",
        "call_llm",
        "interpret_item",
        "update_mastery",
    }
)

# Must not auto-wire StudentReasoningService STOP breaches into this package
# beyond coordinating TwinUpdater as a stage (allowed). Must not import UI.
ALLOWED_STAGE_IMPORT_MARKERS = (
    "EvidenceInterpreter",
    "DecisionGenerator",
    "TwinUpdater",
    "TwinProjectionService",
    "MissionPlanningService",
    "TutorExplanationService",
)


def _python_files() -> list[Path]:
    return sorted(p for p in PACKAGE_ROOT.rglob("*.py") if p.is_file())


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def test_package_avoids_framework_and_ui_imports() -> None:
    for path in _python_files():
        for name in _imports(path):
            root = name.split(".", 1)[0]
            assert root not in FORBIDDEN_ROOT_MODULES, f"{path.name} imports {name}"
            assert not any(
                name.startswith(prefix) for prefix in FORBIDDEN_PREFIXES
            ), f"{path.name} imports forbidden {name}"


def test_no_educational_algorithm_methods() -> None:
    for path in _python_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                assert node.name not in FORBIDDEN_METHOD_NAMES, (
                    f"{path.name} defines educational method {node.name}"
                )


def test_orchestrator_coordinates_certified_stages_only() -> None:
    orch = PACKAGE_ROOT / "orchestrator.py"
    text = orch.read_text(encoding="utf-8")
    for marker in ALLOWED_STAGE_IMPORT_MARKERS:
        assert marker in text, f"orchestrator missing stage {marker}"
    # Must not breach StudentReasoningService by embedding its STOP callers.
    assert "StudentReasoningService" not in text
    assert "plan_from_decisions" not in text
    assert "explain_from_decisions" not in text
    assert "project_twin_decisions" not in text


def test_student_reasoning_stop_boundaries_still_hold() -> None:
    from tests.certification.educational_intelligence.authority import (
        audit_student_reasoning_stop_boundaries,
    )

    findings = audit_student_reasoning_stop_boundaries()
    assert findings == [], findings


def test_stage_order_matches_certified_pipeline() -> None:
    from app.application.educational_intelligence_pipeline.stages import PipelineStage
    from app.application.educational_intelligence_pipeline.versions import (
        PIPELINE_STAGE_ORDER,
    )

    assert PIPELINE_STAGE_ORDER == (
        "interpretation",
        "decision",
        "twin_update",
        "graph_projection",
        "mission_planning",
        "tutor_explanation",
    )
    assert tuple(s.value for s in PipelineStage.ordered()) == PIPELINE_STAGE_ORDER
