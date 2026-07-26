"""Contract tests — Adaptive Decision Contracts (MS-003 A0)."""

from __future__ import annotations

import ast
from pathlib import Path

import app.infrastructure.adapters.adaptive_engine as adaptive_engine_pkg
from app.infrastructure.adapters.adaptive_engine import (
    ADAPTIVE_ERROR_CODES,
    AUTHORITY_ADAPTIVE_ENGINE,
    AdaptiveDecisionContract,
    AdaptiveDecisionResult,
    AdaptiveEngineAdapter,
    AdaptiveEngineBridge,
    AdaptiveInputBundle,
    AdaptiveOutputBundle,
    ConfidencePlaceholder,
    EvidenceRef,
    ExplanationBundle,
    RecommendationPlaceholder,
    RuleRef,
    TopicRef,
    build_adaptive_engine_adapter,
    empty_adaptive_output,
)

REQUIRED_INPUT_KEYS = frozenset(
    {
        "student_id",
        "as_of",
        "evidence",
        "topic_progress",
        "study_attempts",
        "readiness",
        "mission",
        "curriculum",
        "student_goals",
        "authority_tags",
        "lifecycle_stage",
        "field_provenance",
    }
)

REQUIRED_OUTPUT_KEYS = frozenset(
    {
        "recommendation",
        "confidence",
        "explanation",
        "decision_id",
        "authority",
    }
)

REQUIRED_EXPLANATION_KEYS = frozenset(
    {
        "evidence_refs",
        "rule_refs",
        "confidence",
        "input_summary",
        "recommendation_rationale",
        "why_summary",
        "why_reason_codes",
        "topic_refs",
        "alternatives_rationale",
        "limitations_codes",
        "limitations_summary",
        "mission_aligned",
        "mission_note",
    }
)

ADAPTER_ROOT = Path(adaptive_engine_pkg.__file__).resolve().parent

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


def test_adapter_satisfies_decision_contract():
    adapter = AdaptiveEngineAdapter()
    assert isinstance(adapter, AdaptiveDecisionContract)
    assert isinstance(adapter, AdaptiveEngineBridge)


def test_build_helper_respects_flag():
    assert build_adaptive_engine_adapter(enabled=False) is None
    wired = build_adaptive_engine_adapter(enabled=True)
    assert isinstance(wired, AdaptiveEngineAdapter)


def test_error_codes_catalogue_stable():
    expected = {
        "UNAVAILABLE",
        "NO_ACTIVE_PLAN",
        "NOT_FOUND",
        "FORBIDDEN",
        "INVALID_STATE",
        "EXPLAINABILITY_INCOMPLETE",
        "BEHAVIOUR_MISMATCH",
    }
    assert set(ADAPTIVE_ERROR_CODES) == expected


def test_input_bundle_contract_keys():
    bundle = AdaptiveInputBundle(student_id="1")
    assert REQUIRED_INPUT_KEYS.issubset(bundle.to_canonical_dict().keys())


def test_output_bundle_contract_keys():
    output = empty_adaptive_output()
    assert REQUIRED_OUTPUT_KEYS.issubset(output.to_canonical_dict().keys())
    assert output.authority == AUTHORITY_ADAPTIVE_ENGINE


def test_explanation_bundle_structure_complete():
    explanation = ExplanationBundle(
        evidence_refs=(EvidenceRef(kind="attempt", id="9"),),
        rule_refs=(RuleRef(rule_or_model_id="compose.recommendation_service_v1"),),
        confidence=ConfidencePlaceholder(band="low"),
        topic_refs=(TopicRef(topic_code="T1", title="Topic", role="primary"),),
    )
    payload = explanation.to_canonical_dict()
    assert REQUIRED_EXPLANATION_KEYS.issubset(payload.keys())
    assert payload["evidence_refs"][0]["id"] == "9"
    assert payload["rule_refs"][0]["rule_or_model_id"] == (
        "compose.recommendation_service_v1"
    )


def test_decide_result_envelope():
    result = AdaptiveEngineAdapter().decide("42")
    assert isinstance(result, AdaptiveDecisionResult)
    assert result.ok is True
    assert isinstance(result.value, AdaptiveOutputBundle)
    assert result.value.recommendation == RecommendationPlaceholder()
    assert result.value.confidence == ConfidencePlaceholder()


def test_adapter_modules_forbid_runtime_a_write_calls():
    """Static contract: A0 modules must not invoke educational write entrypoints."""
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
