"""Contract tests — Learning Evidence Platform Contracts (MS-006 E0)."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

import app.infrastructure.adapters.evidence_platform as evidence_platform_pkg
from app.infrastructure.adapters.evidence_platform import (
    AUTHORITY_EVIDENCE_PLATFORM,
    CLAIM_BOUNDARIES,
    CLAIM_ORGANISATION,
    EVIDENCE_CLASSES,
    EVIDENCE_ERROR_CODES,
    AnalyticsExport,
    EvidenceAdapter,
    EvidenceContext,
    EvidencePlatformAdapter,
    EvidenceQuality,
    EvidenceRecord,
    EvidenceResult,
    ExperimentArm,
    ExperimentDefinition,
    LearningEvidenceContract,
    ObservationRef,
    OutcomeMetric,
    PolicyEvaluation,
    PolicyEvaluationExplanationPlaceholder,
    build_evidence_platform_adapter,
    empty_evidence_record,
    serialize_canonical,
)

REQUIRED_RECORD_KEYS = frozenset(
    {
        "evidence_id",
        "evidence_version",
        "student_id",
        "source_refs",
        "evidence_class",
        "event_type",
        "claim_boundary",
        "quality",
        "payload_summary",
        "provenance",
        "limitations",
        "engine_version",
        "observed_at",
        "ingested_at",
        "as_of",
        "authority",
        "availability",
        "unavailable_reason",
    }
)

REQUIRED_CONTEXT_KEYS = frozenset(
    {
        "student_id",
        "as_of",
        "source_refs",
        "claim_boundary",
        "evidence_class",
        "field_provenance",
        "limitations",
    }
)

REQUIRED_EXPERIMENT_KEYS = frozenset(
    {
        "experiment_id",
        "definition_version",
        "title",
        "hypothesis",
        "policy_id",
        "baseline_policy_version",
        "treatment_policy_version",
        "arms",
        "eligibility",
        "assignment_mechanism",
        "primary_outcomes",
        "secondary_outcomes",
        "guardrail_outcomes",
        "window",
        "pre_registration",
        "statistical_plan",
        "educational_rationale",
        "rollback_map",
        "status",
        "limitations",
        "authority",
    }
)

REQUIRED_POLICY_EVAL_KEYS = frozenset(
    {
        "evaluation_id",
        "evaluation_version",
        "policy_id",
        "policy_version",
        "baseline_policy_version",
        "experiment_id",
        "experiment_refs",
        "evidence_bundle_ids",
        "evidence_refs",
        "outcome_metrics",
        "statistical_summary",
        "explanation",
        "gate_result",
        "gate_codes",
        "recommendation",
        "limitations",
        "confidence_band",
        "confidence_rationale",
        "provenance",
        "created_at",
        "engine_version",
        "authority",
    }
)

REQUIRED_OUTCOME_METRIC_KEYS = frozenset(
    {
        "metric_id",
        "metric_version",
        "outcome_definition_id",
        "claim_boundary",
        "grain",
        "value",
        "uncertainty",
        "n",
        "subject_scope",
        "evidence_bundle_id",
        "limitations",
        "filters",
        "authority",
    }
)

REQUIRED_EXPLANATION_KEYS = frozenset(
    {
        "evidence_considered",
        "statistical_basis",
        "educational_rationale",
        "policy_version",
        "confidence",
    }
)

ADAPTER_ROOT = Path(evidence_platform_pkg.__file__).resolve().parent

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


def test_adapter_satisfies_evidence_contracts():
    adapter = EvidencePlatformAdapter()
    assert isinstance(adapter, LearningEvidenceContract)
    assert isinstance(adapter, EvidenceAdapter)


def test_build_helper_respects_flag():
    assert build_evidence_platform_adapter(enabled=False) is None
    wired = build_evidence_platform_adapter(enabled=True)
    assert isinstance(wired, EvidencePlatformAdapter)


def test_error_codes_catalogue_stable():
    expected = {
        "UNAVAILABLE",
        "NOT_FOUND",
        "FORBIDDEN",
        "INVALID_STATE",
        "EVIDENCE_QUALITY_INCOMPLETE",
        "CLAIM_BOUNDARY_LEAKAGE",
        "BEHAVIOUR_MISMATCH",
    }
    assert set(EVIDENCE_ERROR_CODES) == expected


def test_claim_boundaries_and_classes_catalogue():
    assert CLAIM_ORGANISATION in CLAIM_BOUNDARIES
    assert "learning_depth" in CLAIM_BOUNDARIES
    assert "FACT_EVENT" in EVIDENCE_CLASSES
    assert "AUTHORITATIVE_MASTERY" not in EVIDENCE_CLASSES


def test_context_contract_keys():
    context = EvidenceContext(student_id="1")
    assert REQUIRED_CONTEXT_KEYS.issubset(context.to_canonical_dict().keys())


def test_evidence_record_contract_keys():
    record = empty_evidence_record(context=EvidenceContext(student_id="1"))
    payload = record.to_canonical_dict()
    assert REQUIRED_RECORD_KEYS.issubset(payload.keys())
    assert record.authority == AUTHORITY_EVIDENCE_PLATFORM
    assert "result" in payload["quality"]


def test_experiment_definition_contract_keys():
    definition = ExperimentDefinition(
        experiment_id="exp-1",
        arms=(
            ExperimentArm(
                arm_id="control",
                label="control",
                exposure="shadow_only",
            ),
        ),
        primary_outcomes=("completion_rate",),
        status="draft",
    )
    assert REQUIRED_EXPERIMENT_KEYS.issubset(definition.to_canonical_dict().keys())


def test_policy_evaluation_contract_keys():
    evaluation = PolicyEvaluation(
        evaluation_id="eval-1",
        policy_id="pol-adaptive-shadow",
        policy_version="1.0.0",
        explanation=PolicyEvaluationExplanationPlaceholder(),
        outcome_metrics=(
            OutcomeMetric(
                metric_id="m1",
                claim_boundary="organisation",
                value=0.5,
                n=10,
            ),
        ),
        gate_result="ineligible",
        recommendation="inconclusive",
        confidence_band="insufficient",
    )
    payload = evaluation.to_canonical_dict()
    assert REQUIRED_POLICY_EVAL_KEYS.issubset(payload.keys())
    assert REQUIRED_EXPLANATION_KEYS.issubset(payload["explanation"].keys())


def test_outcome_metric_and_analytics_export_contract_keys():
    metric = OutcomeMetric(
        metric_id="org-completion",
        claim_boundary="organisation",
        grain="night",
        value=0.42,
        n=12,
    )
    assert REQUIRED_OUTCOME_METRIC_KEYS.issubset(metric.to_canonical_dict().keys())
    export = AnalyticsExport(
        export_id="export-1",
        audience="governance",
        metric_ids=("org-completion",),
    )
    assert export.audience == "governance"
    with pytest.raises(ValueError):
        AnalyticsExport(export_id="bad", audience="student_coaching")


def test_assemble_result_envelope():
    result = EvidencePlatformAdapter().assemble_record("42")
    assert isinstance(result, EvidenceResult)
    assert result.ok is True
    assert isinstance(result.value, EvidenceRecord)
    assert result.value.student_id == "42"
    assert result.value.authority == AUTHORITY_EVIDENCE_PLATFORM


def test_observe_returns_record():
    context = EvidenceContext(
        student_id="7",
        as_of="2026-07-25T00:00:00+00:00",
        source_refs=(
            ObservationRef(
                ref_kind="runtime_a",
                entity_kind="Mission",
                entity_id="m-1",
                claim_boundary="organisation",
                student_id="7",
            ),
        ),
        claim_boundary="organisation",
        evidence_class="FACT_EVENT",
    )
    record = EvidencePlatformAdapter().observe(context)
    assert isinstance(record, EvidenceRecord)
    assert record.student_id == "7"
    assert len(record.source_refs) == 1
    assert isinstance(record.quality, EvidenceQuality)
    assert record.evidence_id.startswith("ev-")
    assert record.observed_at == "2026-07-25T00:00:00+00:00"
    assert record.ingested_at == "2026-07-25T00:00:00+00:00"
    assert record.engine_version == "e1.0"


def test_dto_immutability():
    record = empty_evidence_record(context=EvidenceContext(student_id="1"))
    with pytest.raises(FrozenInstanceError):
        record.evidence_id = "mutated"  # type: ignore[misc]
    with pytest.raises(TypeError):
        record.payload_summary["x"] = 1  # type: ignore[index]
    with pytest.raises(FrozenInstanceError):
        ExperimentDefinition(experiment_id="e").title = "x"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        OutcomeMetric(metric_id="m").value = 9  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        PolicyEvaluation(evaluation_id="p").gate_result = "passed"  # type: ignore[misc]


def test_deterministic_serialization():
    context = EvidenceContext(
        student_id="9",
        as_of="2026-07-25T00:00:00+00:00",
        claim_boundary="organisation",
        field_provenance={"b": 2, "a": 1},
    )
    first = context.serialize()
    second = EvidenceContext(
        student_id="9",
        as_of="2026-07-25T00:00:00+00:00",
        claim_boundary="organisation",
        field_provenance={"a": 1, "b": 2},
    ).serialize()
    assert first == second
    assert first == serialize_canonical(context.to_canonical_dict())

    record_a = empty_evidence_record(context=context)
    record_b = empty_evidence_record(context=context)
    assert record_a.serialize() == record_b.serialize()


def test_claim_boundary_rejection():
    with pytest.raises(ValueError):
        OutcomeMetric(metric_id="m", claim_boundary="mastery_gain")
    with pytest.raises(ValueError):
        ObservationRef(ref_kind="not_a_layer")


def test_adapter_modules_forbid_runtime_a_write_calls():
    """Static contract: E0/E1 modules must not invoke educational write entrypoints."""
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
    """Dependency boundary: Evidence Platform must not import Experience internals.

    Exception: ``shadow_rollback.py`` may lazily import composition solely for
    observational KWALITEC_EVIDENCE_PLATFORM OFF drills (same pattern as Twin T6
    / Strategy S3 rollback). Core collection / evaluation / analytics / shadow
    validator modules remain Experience-import-free.
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
