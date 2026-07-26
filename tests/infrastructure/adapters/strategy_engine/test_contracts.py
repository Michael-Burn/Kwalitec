"""Contract tests — Learning Strategy Contracts (MS-005 S0)."""

from __future__ import annotations

import ast
from pathlib import Path

import app.infrastructure.adapters.strategy_engine as strategy_engine_pkg
from app.infrastructure.adapters.strategy_engine import (
    AUTHORITY_STRATEGY_ENGINE,
    INTERVENTION_KINDS,
    STRATEGY_ERROR_CODES,
    InterventionStep,
    LearningIntervention,
    LearningStrategyContract,
    StrategyAdapter,
    StrategyContext,
    StrategyEngineAdapter,
    StrategyExplanationPlaceholder,
    StrategyProvenancePlaceholder,
    StrategyResult,
    build_strategy_engine_adapter,
    empty_learning_intervention,
)

REQUIRED_CONTEXT_KEYS = frozenset(
    {
        "student_id",
        "as_of",
        "adaptive_recommendation_ref",
        "twin_ref",
        "runtime_a_evidence_ref",
        "adaptive_availability",
        "twin_availability",
        "runtime_a_availability",
        "adaptive_unavailable_reason",
        "twin_unavailable_reason",
        "runtime_a_unavailable_reason",
        "intervention_kinds",
        "lifecycle_stage",
        "mission_id",
        "field_provenance",
        "authority_tags",
        "runtime_a",
        "twin",
        "adaptive",
    }
)

REQUIRED_INTERVENTION_KEYS = frozenset(
    {
        "intervention_id",
        "strategy_version",
        "adaptive_recommendation_ref",
        "twin_ref",
        "runtime_a_evidence_ref",
        "educational_objective",
        "explanation",
        "provenance",
        "kind",
        "steps",
        "topic_refs",
        "educational_principle_ids",
        "runtime_a_refs",
        "minutes_budget",
        "authority",
        "limitations",
        "study",
        "session",
        "revision",
        "recovery",
        "fatigue",
        "confidence",
        "sequencing",
    }
)

REQUIRED_STEP_KEYS = frozenset(
    {
        "order",
        "action_code",
        "summary",
        "minutes",
        "intent",
    }
)

REQUIRED_EXPLANATION_KEYS = frozenset(
    {
        "why_summary",
        "educational_principle_ids",
        "limitations_codes",
        "limitations_summary",
        "input_summary",
    }
)

REQUIRED_PROVENANCE_KEYS = frozenset(
    {
        "source_service",
        "source_entity",
        "collected_at",
        "availability",
        "unavailable_reason",
        "kind",
    }
)

ADAPTER_ROOT = Path(strategy_engine_pkg.__file__).resolve().parent

FORBIDDEN_WRITE_CALLS = frozenset(
    {
        "generate_today_mission",
        "start_session",
        "complete_session",
        "accept_evidence",
        "db.session.add",
        "db.session.commit",
    }
)

FORBIDDEN_IMPORT_PREFIXES = (
    "app.infrastructure.adapters.student_experience",
    "app.presentation",
    "flask",
)


def test_adapter_satisfies_strategy_contracts():
    adapter = StrategyEngineAdapter()
    assert isinstance(adapter, LearningStrategyContract)
    assert isinstance(adapter, StrategyAdapter)


def test_build_helper_respects_flag():
    assert build_strategy_engine_adapter(enabled=False) is None
    wired = build_strategy_engine_adapter(enabled=True)
    assert isinstance(wired, StrategyEngineAdapter)


def test_error_codes_catalogue_stable():
    expected = {
        "UNAVAILABLE",
        "NO_ACTIVE_PLAN",
        "NOT_FOUND",
        "FORBIDDEN",
        "INVALID_STATE",
        "STRATEGY_EXPLAINABILITY_INCOMPLETE",
        "STRATEGY_INPUT_UNAVAILABLE",
        "BEHAVIOUR_MISMATCH",
    }
    assert set(STRATEGY_ERROR_CODES) == expected


def test_intervention_kinds_catalogue_covers_model():
    expected = {
        "STUDY_PLAN",
        "SESSION_PLAN",
        "REVISION_PLAN",
        "RECOVERY_PLAN",
        "FATIGUE_MANAGEMENT",
        "CONFIDENCE_INTERVENTION",
        "CONTINUE",
        "BREAK",
        "ASSESS",
        "",
    }
    assert set(INTERVENTION_KINDS) == expected


def test_context_contract_keys():
    context = StrategyContext(student_id="1")
    assert REQUIRED_CONTEXT_KEYS.issubset(context.to_canonical_dict().keys())


def test_intervention_contract_keys():
    intervention = empty_learning_intervention()
    payload = intervention.to_canonical_dict()
    assert REQUIRED_INTERVENTION_KEYS.issubset(payload.keys())
    assert intervention.authority == AUTHORITY_STRATEGY_ENGINE
    assert REQUIRED_EXPLANATION_KEYS.issubset(payload["explanation"].keys())
    assert REQUIRED_PROVENANCE_KEYS.issubset(payload["provenance"].keys())


def test_intervention_step_contract_keys():
    step = InterventionStep(order=1, action_code="orient", summary="Confirm topic")
    assert REQUIRED_STEP_KEYS.issubset(step.to_canonical_dict().keys())


def test_intervention_exposes_required_contributing_refs():
    intervention = LearningIntervention(
        intervention_id="int-1",
        strategy_version="s0.1",
        adaptive_recommendation_ref="adaptive-9",
        twin_ref="twin-3",
        runtime_a_evidence_ref="evidence-2",
        educational_objective="Complete tonight's session shell",
        explanation=StrategyExplanationPlaceholder(why_summary="placeholder"),
        provenance=StrategyProvenancePlaceholder(
            source_service="strategy_engine",
            kind="strategy_derived",
        ),
        steps=(InterventionStep(order=1, action_code="orient", summary="Start"),),
    )
    payload = intervention.to_canonical_dict()
    assert payload["intervention_id"] == "int-1"
    assert payload["strategy_version"] == "s0.1"
    assert payload["adaptive_recommendation_ref"] == "adaptive-9"
    assert payload["twin_ref"] == "twin-3"
    assert payload["runtime_a_evidence_ref"] == "evidence-2"
    assert payload["educational_objective"] == "Complete tonight's session shell"
    assert "explanation" in payload
    assert "provenance" in payload


def test_orchestrate_result_envelope():
    result = StrategyEngineAdapter().orchestrate("42")
    assert isinstance(result, StrategyResult)
    assert result.ok is True
    assert isinstance(result.value, LearningIntervention)
    assert result.value.authority == AUTHORITY_STRATEGY_ENGINE


def test_evaluate_returns_intervention():
    context = StrategyContext(student_id="7")
    intervention = StrategyEngineAdapter().evaluate(context)
    assert isinstance(intervention, LearningIntervention)
    assert "student_id=7" in intervention.explanation.input_summary
    assert intervention.strategy_version == "s1.0"


def test_adapter_modules_forbid_runtime_a_write_calls():
    """Static contract: S0 modules must not invoke educational write entrypoints."""
    for path in ADAPTER_ROOT.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        text = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_WRITE_CALLS:
            assert forbidden not in text, f"{path.name} must not contain {forbidden}"
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                name = node.func.attr
                assert name not in {
                    "generate_today_mission",
                    "start_session",
                    "complete_session",
                    "accept_evidence",
                }, f"{path.name} calls forbidden write API {name}"


def test_adapter_modules_forbid_experience_imports():
    """Dependency boundary: Strategy must not import Experience internals.

    Exception: ``shadow_rollback.py`` may lazily import composition solely for
    observational KWALITEC_STRATEGY_ENGINE OFF drills (same pattern as Twin T6
    rollback). Core orchestration / explainability / projection modules remain
    Experience-import-free.
    """
    allowlist = frozenset({"shadow_rollback.py"})
    for path in ADAPTER_ROOT.glob("*.py"):
        if path.name in allowlist:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                module = node.module
                assert not any(
                    module == prefix or module.startswith(prefix + ".")
                    for prefix in FORBIDDEN_IMPORT_PREFIXES
                ), f"{path.name} imports forbidden module {module}"
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.name
                    assert not any(
                        name == prefix or name.startswith(prefix + ".")
                        for prefix in FORBIDDEN_IMPORT_PREFIXES
                    ), f"{path.name} imports forbidden module {name}"
