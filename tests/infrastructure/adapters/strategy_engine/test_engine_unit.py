"""Unit tests — Strategy Engine core orchestration (MS-005 S1)."""

from __future__ import annotations

import copy

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.strategy_engine import (
    KIND_FATIGUE_MANAGEMENT,
    KIND_RECOVERY_PLAN,
    KIND_REVISION_PLAN,
    KIND_SESSION_PLAN,
    StrategyContext,
    StrategyContextAssembler,
    StrategyEngine,
    StrategyEngineAdapter,
    StudyPlanner,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)


def _runtime_a(**overrides):
    base = {
        "mission": {
            "mission_id": "9",
            "topic_code": "T-MISSION",
            "status": "pending",
        },
        "lifecycle_stage": "Learning",
        "student_goals": {"daily_minutes": 50, "study_plan_id": "plan-1"},
        "evidence": {"evidence_id": "ev-1", "attempts": []},
        "topic_progress": [
            {"topic_id": "T-MISSION", "topic_name": "Mission", "mastery_score": 0.4},
            {"topic_id": "T-ALT", "topic_name": "Alt", "mastery_score": 0.2},
        ],
        "study_attempts": [
            {"id": "a1", "score": 0.3, "outcome": "pass"},
            {"id": "a2", "score": 0.5, "outcome": "pass"},
        ],
    }
    base.update(overrides)
    return base


def _twin(**overrides):
    profile = {
        "cognitive_load_indicators": {
            "label": "medium",
            "availability": "available",
        },
        "confidence_trend": {
            "label": "high confidence",
            "availability": "available",
        },
        "session_habits": {"label": "evening", "availability": "available"},
        "learning_rhythm": {"label": "steady", "availability": "available"},
        "persistence": {"label": "recovering", "availability": "available"},
        "revision_behaviour": {"label": "active", "availability": "available"},
        "consistency": {"label": "regular", "availability": "available"},
    }
    profile.update(overrides.get("profile", {}))
    payload = {
        "twin_id": "twin-1",
        "snapshot_version": "snap-1",
        "profile": profile,
    }
    for key, value in overrides.items():
        if key != "profile":
            payload[key] = value
    return payload


def _adaptive(**overrides):
    base = {
        "decision_id": "adaptive-7",
        "recommendation": {
            "topic_code": "T-ADAPTIVE",
            "title": "Adaptive Topic",
            "decision_kind": "NEXT_FOCUS",
        },
        "explanation": {
            "topic_refs": [
                {"topic_code": "T-ADAPTIVE", "role": "primary"},
                {"topic_code": "T-ALT", "role": "alternative"},
            ]
        },
        "alternatives": [{"topic_code": "T-ALT"}],
    }
    base.update(overrides)
    return base


def _full_context(**kwargs) -> StrategyContext:
    assembler = StrategyContextAssembler()
    return assembler.assemble(
        kwargs.pop("student_id", "42"),
        as_of=kwargs.pop("as_of", "2026-07-25T10:00:00+00:00"),
        runtime_a=kwargs.pop("runtime_a", _runtime_a()),
        twin=kwargs.pop("twin", _twin()),
        adaptive=kwargs.pop("adaptive", _adaptive()),
        **kwargs,
    )


def test_engine_produces_all_planner_components():
    intervention = StrategyEngine().evaluate(_full_context())
    assert intervention.strategy_version == "s1.0"
    assert intervention.study is not None
    assert intervention.session is not None
    assert intervention.revision is not None
    assert intervention.recovery is not None
    assert intervention.fatigue is not None
    assert intervention.confidence is not None
    assert intervention.sequencing.primary_kind == KIND_SESSION_PLAN
    assert intervention.session.available is True
    assert intervention.session.primary_topic == "T-MISSION"
    assert intervention.session.advisory_topic == "T-ADAPTIVE"
    assert intervention.session.mission_aligned is False
    assert intervention.fatigue.available is True
    assert intervention.authority == "strategy_engine"


def test_identical_context_yields_identical_intervention():
    context = _full_context()
    engine = StrategyEngine()
    first = engine.evaluate(context)
    second = engine.evaluate(context)
    assert first.serialize() == second.serialize()
    assert first.intervention_id.startswith("s1-")
    assert first.intervention_id == second.intervention_id


def test_assembler_does_not_mutate_inputs():
    runtime_a = _runtime_a()
    twin = _twin()
    adaptive = _adaptive()
    runtime_copy = copy.deepcopy(runtime_a)
    twin_copy = copy.deepcopy(twin)
    adaptive_copy = copy.deepcopy(adaptive)
    context = StrategyContextAssembler().assemble(
        "7",
        as_of="2026-07-25T10:00:00+00:00",
        runtime_a=runtime_a,
        twin=twin,
        adaptive=adaptive,
    )
    runtime_a["mission"]["topic_code"] = "MUTATED"
    twin["profile"]["confidence_trend"]["label"] = "MUTATED"
    adaptive["recommendation"]["topic_code"] = "MUTATED"
    assert context.runtime_a["mission"]["topic_code"] == runtime_copy["mission"][
        "topic_code"
    ]
    assert context.twin["profile"]["confidence_trend"]["label"] == twin_copy[
        "profile"
    ]["confidence_trend"]["label"]
    assert context.adaptive["recommendation"]["topic_code"] == adaptive_copy[
        "recommendation"
    ]["topic_code"]
    with pytest.raises(TypeError):
        context.runtime_a["mission"] = {}  # type: ignore[index]


def test_study_planner_preserves_adaptive_topic_order():
    context = _full_context(
        adaptive=_adaptive(
            recommendation={"topic_code": "T1"},
            alternatives=[{"topic_code": "T2"}, {"topic_code": "T3"}],
            explanation={
                "topic_refs": [
                    {"topic_code": "T1"},
                    {"topic_code": "T2"},
                    {"topic_code": "T3"},
                ]
            },
        )
    )
    study = StudyPlanner().plan(context)
    assert list(study.focus_topics) == ["T1", "T2", "T3"]


def test_fatigue_critical_becomes_primary():
    context = _full_context(
        twin=_twin(
            profile={
                "cognitive_load_indicators": {
                    "label": "critical overload",
                    "availability": "available",
                }
            }
        )
    )
    intervention = StrategyEngine().evaluate(context)
    assert intervention.sequencing.primary_kind == KIND_FATIGUE_MANAGEMENT
    assert intervention.kind == KIND_FATIGUE_MANAGEMENT
    assert intervention.fatigue.severity_band == "critical"


def test_recovery_trigger_becomes_primary():
    context = _full_context(
        runtime_a=_runtime_a(
            mission={
                "mission_id": "9",
                "topic_code": "T-MISSION",
                "status": "abandoned",
            }
        ),
        twin=_twin(
            profile={
                "cognitive_load_indicators": {
                    "label": "low",
                    "availability": "available",
                }
            }
        ),
    )
    intervention = StrategyEngine().evaluate(context)
    assert intervention.sequencing.primary_kind == KIND_RECOVERY_PLAN
    assert intervention.recovery.trigger_kind == "abandoned_mission"
    assert intervention.recovery.restart_topic == "T-MISSION"


def test_revision_lifecycle_primary():
    context = _full_context(
        runtime_a=_runtime_a(lifecycle_stage="Revision"),
        twin=_twin(
            profile={
                "cognitive_load_indicators": {
                    "label": "",
                    "availability": "unavailable",
                }
            }
        ),
    )
    intervention = StrategyEngine().evaluate(context)
    assert intervention.sequencing.primary_kind == KIND_REVISION_PLAN
    assert intervention.revision.available is True


def test_missing_twin_and_adaptive_still_deterministic():
    assembler = StrategyContextAssembler()
    context = assembler.assemble(
        "1",
        as_of="2026-07-25T08:00:00+00:00",
        runtime_a=_runtime_a(),
    )
    assert context.twin_availability == "unavailable"
    assert context.adaptive_availability == "unavailable"
    engine = StrategyEngine()
    first = engine.evaluate(context)
    second = engine.evaluate(context)
    assert first.serialize() == second.serialize()
    assert "twin_unavailable" in first.limitations
    assert "adaptive_unavailable" in first.limitations
    assert first.session.primary_topic == "T-MISSION"
    assert first.session.advisory_topic == ""


def test_missing_all_inputs_empty_authentic():
    context = StrategyContextAssembler().assemble(
        "99", as_of="2026-07-25T08:00:00+00:00"
    )
    intervention = StrategyEngine().evaluate(context)
    assert intervention.sequencing.composition_rule == "empty_authentic"
    assert intervention.kind == ""
    assert "runtime_a_unavailable" in intervention.limitations


def test_adapter_orchestrate_with_inputs():
    adapter = StrategyEngineAdapter()
    result = adapter.orchestrate(
        "5",
        as_of="2026-07-25T10:00:00+00:00",
        runtime_a=_runtime_a(),
        twin=_twin(),
        adaptive=_adaptive(),
    )
    assert result.ok is True
    assert result.value is not None
    assert result.value.kind == KIND_SESSION_PLAN


def test_flag_default_off_and_di_wiring():
    flags_off = resolve_v2_feature_flags(environ={})
    assert flags_off.ENABLE_STRATEGY_ENGINE is False
    composition_off, _ = build_production_experience(flags=flags_off)
    assert composition_off.strategy_engine is None

    flags_on = resolve_v2_feature_flags(environ={"KWALITEC_STRATEGY_ENGINE": "1"})
    composition_on, _ = build_production_experience(flags=flags_on)
    assert isinstance(composition_on.strategy_engine, StrategyEngineAdapter)
    assert composition_on.strategy_engine.engine.engine_version == "s1.0"
    assert composition_on.strategy_engine.assembler.assembler_id == (
        "strategy_context_assembler"
    )
    # No Experience / Adaptive / Twin behavioural cutover from Strategy S1.
    assert composition_on.adaptive is not None
    assert composition_on.twin is not None
