"""Contract tests — Student Digital Twin Contracts (MS-004 T0)."""

from __future__ import annotations

import ast
from pathlib import Path

import app.infrastructure.adapters.digital_twin as digital_twin_pkg
from app.infrastructure.adapters.digital_twin import (
    AUTHORITY_DIGITAL_TWIN,
    TWIN_ERROR_CODES,
    TWIN_FACET_NAMES,
    CognitiveLoadIndicatorsFacet,
    ConfidenceTrendFacet,
    ConsistencyFacet,
    DigitalTwinAdapter,
    LearningRhythmFacet,
    PersistenceFacet,
    RevisionBehaviourFacet,
    SessionHabitsFacet,
    StudentDigitalTwinContract,
    TwinAdapter,
    TwinCompleteness,
    TwinProfile,
    TwinProvenance,
    TwinResult,
    TwinSnapshot,
    build_digital_twin_adapter,
    empty_twin_snapshot,
)

REQUIRED_SNAPSHOT_KEYS = frozenset(
    {
        "profile",
        "profile_version",
        "source_evidence_version",
        "generated_at",
        "provenance",
        "completeness",
        "twin_id",
        "authority",
        "field_provenance",
        "snapshot_version",
        "schema_version",
        "provenance_summary",
        "unavailable_summary",
    }
)

REQUIRED_PROFILE_KEYS = frozenset(
    {
        "student_id",
        "learning_rhythm",
        "consistency",
        "persistence",
        "revision_behaviour",
        "confidence_trend",
        "session_habits",
        "cognitive_load_indicators",
        "limitations_codes",
        "limitations_summary",
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

REQUIRED_COMPLETENESS_KEYS = frozenset(
    {
        "score",
        "facets_present",
        "facets_unavailable",
        "summary",
        "status",
    }
)

ADAPTER_ROOT = Path(digital_twin_pkg.__file__).resolve().parent

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


def test_adapter_satisfies_twin_contracts():
    adapter = DigitalTwinAdapter()
    assert isinstance(adapter, StudentDigitalTwinContract)
    assert isinstance(adapter, TwinAdapter)


def test_build_helper_respects_flag():
    assert build_digital_twin_adapter(enabled=False) is None
    wired = build_digital_twin_adapter(enabled=True)
    assert isinstance(wired, DigitalTwinAdapter)


def test_error_codes_catalogue_stable():
    expected = {
        "UNAVAILABLE",
        "NO_ACTIVE_PLAN",
        "NOT_FOUND",
        "FORBIDDEN",
        "INVALID_STATE",
        "STALE_SNAPSHOT",
        "TWIN_EXPLAINABILITY_INCOMPLETE",
        "BEHAVIOUR_MISMATCH",
    }
    assert set(TWIN_ERROR_CODES) == expected


def test_facet_catalogue_covers_directive_facets():
    expected = {
        "learning_rhythm",
        "consistency",
        "persistence",
        "revision_behaviour",
        "confidence_trend",
        "session_habits",
        "cognitive_load_indicators",
    }
    assert set(TWIN_FACET_NAMES) == expected


def test_profile_contract_keys():
    profile = TwinProfile(student_id="1")
    assert REQUIRED_PROFILE_KEYS.issubset(profile.to_canonical_dict().keys())


def test_snapshot_contract_keys():
    snapshot = empty_twin_snapshot(profile=TwinProfile(student_id="1"))
    payload = snapshot.to_canonical_dict()
    assert REQUIRED_SNAPSHOT_KEYS.issubset(payload.keys())
    assert snapshot.authority == AUTHORITY_DIGITAL_TWIN
    assert REQUIRED_PROVENANCE_KEYS.issubset(payload["provenance"].keys())
    assert REQUIRED_COMPLETENESS_KEYS.issubset(payload["completeness"].keys())


def test_all_facet_dto_types_construct():
    profile = TwinProfile(
        student_id="9",
        learning_rhythm=LearningRhythmFacet(label="placeholder"),
        consistency=ConsistencyFacet(label="placeholder"),
        persistence=PersistenceFacet(label="placeholder"),
        revision_behaviour=RevisionBehaviourFacet(label="placeholder"),
        confidence_trend=ConfidenceTrendFacet(label="placeholder"),
        session_habits=SessionHabitsFacet(label="placeholder"),
        cognitive_load_indicators=CognitiveLoadIndicatorsFacet(label="placeholder"),
    )
    facets = profile.to_canonical_dict()
    for name in TWIN_FACET_NAMES:
        assert name in facets
        assert "availability" in facets[name]


def test_assemble_result_envelope():
    result = DigitalTwinAdapter().assemble_snapshot("42")
    assert isinstance(result, TwinResult)
    assert result.ok is True
    assert isinstance(result.value, TwinSnapshot)
    assert result.value.profile.student_id == "42"
    assert isinstance(result.value.provenance, TwinProvenance)
    assert isinstance(result.value.completeness, TwinCompleteness)


def test_adapter_modules_forbid_runtime_a_write_calls():
    """Static contract: T0 modules must not invoke educational write entrypoints."""
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
