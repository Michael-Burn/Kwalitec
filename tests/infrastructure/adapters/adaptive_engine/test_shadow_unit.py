"""Unit tests — Adaptive Engine Executor + Shadow (MS-003 A2)."""

from __future__ import annotations

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.adaptive_engine import (
    AdaptiveEngineAdapter,
    AdaptiveEngineExecutor,
    AdaptiveInputBundle,
    AdaptiveShadowOrchestrator,
    ExplanationBundle,
    build_adaptive_engine_executor,
    build_adaptive_shadow_orchestrator,
    explanation_is_complete,
    serialize_canonical,
)
from app.infrastructure.adapters.adaptive_engine.executor import (
    RULE_MISSION_ALIGNED,
    RULE_NEXT_INCOMPLETE_LEAF,
    RULE_WEAK_TOPIC_PRIORITY,
)
from app.infrastructure.adapters.adaptive_engine.provenance import (
    available_provenance,
    unavailable_provenance,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    ADAPTIVE_SHADOW_COMPLETED,
    ADAPTIVE_SHADOW_EVENT_TYPES,
    ADAPTIVE_SHADOW_FAILED,
    ADAPTIVE_SHADOW_LATENCY,
    ADAPTIVE_SHADOW_REQUESTED,
    EVENT_TYPES,
)


def _prov_map(available: tuple[str, ...], unavailable: tuple[str, ...] = ()) -> dict:
    collected_at = "2026-07-25"
    out = {
        name: available_provenance(
            source_service="stub",
            source_entity=name,
            collected_at=collected_at,
        ).to_canonical_dict()
        for name in available
    }
    for name in unavailable:
        out[name] = unavailable_provenance(
            source_service="stub",
            source_entity=name,
            collected_at=collected_at,
            reason="UNAVAILABLE",
        ).to_canonical_dict()
    return out


def _full_available_provenance() -> dict:
    return _prov_map(
        (
            "evidence",
            "topic_progress",
            "study_attempts",
            "mission",
            "readiness",
            "curriculum",
            "student_goals",
            "lifecycle_stage",
        )
    )


def test_executor_next_incomplete_leaf_is_deterministic():
    executor = AdaptiveEngineExecutor()
    inputs = AdaptiveInputBundle(
        student_id="7",
        as_of="2026-07-25",
        evidence={"attempt_count": 2, "authorised_count": 1, "attempts": []},
        topic_progress=(
            {
                "topic_id": "1",
                "topic_name": "Done",
                "completed": True,
                "mastery_score": 0.9,
            },
        ),
        curriculum={
            "leaves": [
                {"topic_id": "1", "topic_name": "Done", "order": 1},
                {"topic_id": "2", "topic_name": "Next Leaf", "order": 2},
            ],
            "leaf_count": 2,
        },
        lifecycle_stage="Learning",
        field_provenance=_full_available_provenance(),
    )
    first = executor.evaluate(inputs)
    second = executor.evaluate(inputs)
    assert first.serialize() == second.serialize()
    assert first.recommendation.topic_code == "2"
    assert first.recommendation.title == "Next Leaf"
    assert first.recommendation.decision_kind == "NEXT_FOCUS"
    assert first.explanation.rule_refs[0].rule_or_model_id == RULE_NEXT_INCOMPLETE_LEAF
    assert first.decision_id.startswith("a2-")
    assert explanation_is_complete(first)


def test_executor_mission_aligned_primary():
    executor = AdaptiveEngineExecutor()
    inputs = AdaptiveInputBundle(
        student_id="7",
        as_of="2026-07-25",
        evidence={
            "attempt_count": 3,
            "authorised_count": 2,
            "attempts": [
                {
                    "attempt_id": "11",
                    "study_date": "2026-07-24",
                    "authorised_structured_results": True,
                },
                {
                    "attempt_id": "12",
                    "study_date": "2026-07-25",
                    "authorised_structured_results": True,
                },
                {
                    "attempt_id": "13",
                    "study_date": "2026-07-25",
                    "authorised_structured_results": False,
                },
            ],
        },
        mission={
            "today": {
                "mission_id": "99",
                "mission_date": "2026-07-25",
                "title": "Study Compound Interest",
                "status": "Pending",
            },
            "history": [],
            "history_count": 0,
        },
        curriculum={
            "leaves": [
                {"topic_id": "2", "topic_name": "Next Leaf", "order": 1},
            ],
            "leaf_count": 1,
        },
        field_provenance=_full_available_provenance(),
    )
    output = executor.evaluate(inputs)
    assert output.recommendation.title == "Study Compound Interest"
    assert output.recommendation.decision_kind == "COMPOSITE"
    assert output.explanation.mission_aligned is True
    assert output.explanation.rule_refs[0].rule_or_model_id == RULE_MISSION_ALIGNED
    assert output.confidence.band == "high"
    assert any(ref.kind == "mission" for ref in output.explanation.evidence_refs)
    assert "mission" in output.explanation.inputs_used
    assert explanation_is_complete(output)


def test_executor_revision_weak_topic():
    executor = AdaptiveEngineExecutor()
    inputs = AdaptiveInputBundle(
        student_id="3",
        as_of="2026-07-25",
        evidence={"attempt_count": 1, "attempts": []},
        topic_progress=(
            {
                "topic_id": "10",
                "topic_name": "Strong",
                "completed": True,
                "mastery_score": 0.95,
            },
            {
                "topic_id": "9",
                "topic_name": "Weak",
                "completed": True,
                "mastery_score": 0.2,
            },
        ),
        curriculum={"leaves": [], "leaf_count": 0},
        lifecycle_stage="Revision",
        field_provenance=_full_available_provenance(),
    )
    output = executor.evaluate(inputs)
    assert output.recommendation.topic_code == "9"
    assert output.recommendation.decision_kind == "REVISION_SET"
    assert output.explanation.rule_refs[0].rule_or_model_id == RULE_WEAK_TOPIC_PRIORITY


def test_explanation_bundle_records_inputs_used_and_unavailable():
    executor = AdaptiveEngineExecutor()
    inputs = AdaptiveInputBundle(
        student_id="1",
        as_of="2026-07-25",
        evidence={"attempt_count": 0, "attempts": []},
        curriculum={
            "leaves": [{"topic_id": "1", "topic_name": "A", "order": 1}],
            "leaf_count": 1,
        },
        field_provenance=_prov_map(
            ("evidence", "curriculum", "lifecycle_stage"),
            (
                "mission",
                "readiness",
                "topic_progress",
                "study_attempts",
                "student_goals",
            ),
        ),
        lifecycle_stage="Learning",
    )
    output = executor.evaluate(inputs)
    assert "curriculum" in output.explanation.inputs_used
    assert "mission" in output.explanation.inputs_unavailable
    assert output.explanation.recommendation_rationale
    assert output.explanation.why_summary
    assert output.explanation.rule_refs
    assert output.explanation.confidence.band in {"low", "medium", "high"}


def test_shadow_orchestrator_emits_telemetry_and_discards_for_ux():
    events = EventRegistry()
    executor = AdaptiveEngineExecutor()
    inputs = AdaptiveInputBundle(
        student_id="42",
        as_of="2026-07-25",
        curriculum={
            "leaves": [{"topic_id": "1", "topic_name": "A", "order": 1}],
            "leaf_count": 1,
        },
        field_provenance=_full_available_provenance(),
    )

    class _Assembler:
        def assemble(self, student_id, *, as_of=None):
            assert student_id == "42"
            return inputs

    orch = AdaptiveShadowOrchestrator(
        assembler=_Assembler(),
        executor=executor,
        events=events,
        enabled=True,
    )
    result = orch.execute_shadow("42", as_of="2026-07-25")
    assert result.ok is True
    assert result.value is not None
    types = [e.event_type for e in events.published()]
    assert ADAPTIVE_SHADOW_REQUESTED in types
    assert ADAPTIVE_SHADOW_COMPLETED in types
    assert ADAPTIVE_SHADOW_LATENCY in types
    completed = next(
        e for e in events.published() if e.event_type == ADAPTIVE_SHADOW_COMPLETED
    )
    assert completed.payload["discarded_for_ux"] is True


def test_shadow_orchestrator_failure_emits_failed():
    events = EventRegistry()

    class _BrokenAssembler:
        def assemble(self, student_id, *, as_of=None):
            raise RuntimeError("boom")

    orch = AdaptiveShadowOrchestrator(
        assembler=_BrokenAssembler(),
        executor=AdaptiveEngineExecutor(),
        events=events,
        enabled=True,
    )
    result = orch.execute_shadow("1", as_of="2026-07-25")
    assert result.ok is False
    types = [e.event_type for e in events.published()]
    assert ADAPTIVE_SHADOW_FAILED in types
    assert ADAPTIVE_SHADOW_LATENCY in types


def test_shadow_flag_aliases_and_defaults():
    flags_off = resolve_v2_feature_flags(environ={})
    assert flags_off.ENABLE_ADAPTIVE_ENGINE is False
    assert flags_off.ENABLE_ADAPTIVE_ENGINE_SHADOW is False

    alias = resolve_v2_feature_flags(environ={"KWALITEC_ADAPTIVE_SHADOW": "1"})
    assert alias.ENABLE_ADAPTIVE_ENGINE_SHADOW is True

    legacy = resolve_v2_feature_flags(
        environ={"KWALITEC_ADAPTIVE_ENGINE_SHADOW": "true"}
    )
    assert legacy.ENABLE_ADAPTIVE_ENGINE_SHADOW is True


def test_di_wires_shadow_without_experience_cutover():
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_ADAPTIVE_ENGINE": "1",
            "KWALITEC_ADAPTIVE_SHADOW": "1",
        }
    )
    composition, _ = build_production_experience(flags=flags)
    assert isinstance(composition.adaptive_engine, AdaptiveEngineAdapter)
    assert composition.adaptive_engine.executor is not None
    assert isinstance(composition.adaptive_shadow, AdaptiveShadowOrchestrator)
    # A2 must not cut over Experience AdaptiveDecisionPort.
    assert composition.adaptive._recommendation_read is None
    assert composition.adaptive_engine is not composition.adaptive


def test_shadow_only_flag_constructs_pipeline():
    flags = resolve_v2_feature_flags(environ={"KWALITEC_ADAPTIVE_SHADOW": "1"})
    composition, _ = build_production_experience(flags=flags)
    assert composition.adaptive_engine is not None
    assert composition.adaptive_shadow is not None
    assert composition.adaptive_input_assembler is not None


def test_build_helpers_respect_enabled_false():
    assert build_adaptive_engine_executor(enabled=False) is None
    assert (
        build_adaptive_shadow_orchestrator(
            enabled=False,
            assembler=object(),
            executor=AdaptiveEngineExecutor(),
        )
        is None
    )


def test_adaptive_shadow_events_registered():
    for event_type in ADAPTIVE_SHADOW_EVENT_TYPES:
        assert event_type in EVENT_TYPES


def test_adapter_uses_executor_when_wired():
    executor = AdaptiveEngineExecutor()
    adapter = AdaptiveEngineAdapter(executor=executor)
    inputs = AdaptiveInputBundle(
        student_id="5",
        curriculum={
            "leaves": [{"topic_id": "8", "topic_name": "X", "order": 1}],
            "leaf_count": 1,
        },
        field_provenance=_full_available_provenance(),
    )
    output = adapter.evaluate(inputs)
    assert output.recommendation.topic_code == "8"
    assert output.decision_id.startswith("a2-")


def test_explanation_serialize_includes_inputs_accounting():
    explanation = ExplanationBundle(
        inputs_used=("mission",),
        inputs_unavailable=("readiness",),
        recommendation_rationale="r",
        why_summary="w",
    )
    payload = explanation.to_canonical_dict()
    assert payload["inputs_used"] == ["mission"]
    assert payload["inputs_unavailable"] == ["readiness"]
    assert serialize_canonical(payload) == explanation.serialize()
