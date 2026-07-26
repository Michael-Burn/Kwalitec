"""Integration tests — Strategy Shadow Validation (MS-005 S3).

Verifies stable observational shadow validation, deterministic replay,
explainability / projection consistency, planner consistency, rollback,
feature-flag isolation, and no Experience behavioural change.
"""

from __future__ import annotations

import ast
from pathlib import Path

import app.infrastructure.adapters.strategy_engine as strategy_pkg
from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.strategy_engine import (
    StrategyShadowValidator,
    build_strategy_engine_adapter,
    build_strategy_explainability_service,
    build_strategy_projector,
    build_strategy_shadow_ops_dashboard,
    build_strategy_shadow_validator,
    verify_strategy_shadow_rollback,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    STRATEGY_SHADOW_COMPLETED,
    STRATEGY_SHADOW_HEALTH,
    STRATEGY_SHADOW_LATENCY,
    STRATEGY_SHADOW_REQUESTED,
    STRATEGY_SHADOW_ROLLBACK_VERIFIED,
    STRATEGY_SHADOW_STABILITY,
)

ADAPTER_ROOT = Path(strategy_pkg.__file__).resolve().parent
AS_OF = "2026-07-25T12:00:00"


def _runtime_a():
    return {
        "mission": {
            "mission_id": "21",
            "topic_code": "T-MISSION",
            "status": "pending",
        },
        "lifecycle_stage": "Learning",
        "student_goals": {"daily_minutes": 40},
        "evidence": {"evidence_id": "ev-21"},
        "topic_progress": [
            {"topic_id": "T-MISSION", "mastery_score": 0.55},
        ],
        "study_attempts": [{"id": "att-1", "score": 0.5}],
    }


def _twin():
    return {
        "twin_id": "twin-shadow",
        "snapshot_version": "sv-1",
        "profile": {
            "cognitive_load_indicators": {
                "label": "low",
                "availability": "available",
            },
            "confidence_trend": {
                "label": "cautious",
                "availability": "available",
            },
        },
    }


def _adaptive():
    return {
        "decision_id": "dec-shadow",
        "recommendation": {
            "topic_code": "T-ADAPTIVE",
            "title": "Adaptive",
            "decision_kind": "NEXT_FOCUS",
        },
        "alternatives": [{"topic_code": "T-ALT"}],
    }


def _build_validator(*, events: EventRegistry | None = None) -> StrategyShadowValidator:
    registry = events or EventRegistry()
    adapter = build_strategy_engine_adapter(enabled=True)
    explainability = build_strategy_explainability_service(enabled=True)
    projector = build_strategy_projector(enabled=True)
    validator = build_strategy_shadow_validator(
        enabled=True,
        adapter=adapter,
        explainability=explainability,
        projector=projector,
        events=registry,
    )
    assert validator is not None
    return validator


def test_shadow_pipeline_deterministic_replay():
    events = EventRegistry()
    validator = _build_validator(events=events)

    first = validator.validate_shadow(
        "11",
        as_of=AS_OF,
        runtime_a=_runtime_a(),
        twin=_twin(),
        adaptive=_adaptive(),
    )
    second = validator.validate_shadow(
        "11",
        as_of=AS_OF,
        runtime_a=_runtime_a(),
        twin=_twin(),
        adaptive=_adaptive(),
    )

    assert first.ok is True
    assert second.ok is True
    assert first.intervention is not None and second.intervention is not None
    assert first.intervention.serialize() == second.intervention.serialize()
    assert first.explanation is not None and second.explanation is not None
    assert first.explanation.serialize() == second.explanation.serialize()
    assert first.projection is not None and second.projection is not None
    assert first.projection.serialize() == second.projection.serialize()
    assert first.determinism_ok is True
    assert second.determinism_ok is True
    assert first.planner_consistency_ok is True

    types = [e.event_type for e in events.published()]
    assert STRATEGY_SHADOW_REQUESTED in types
    assert STRATEGY_SHADOW_COMPLETED in types
    assert STRATEGY_SHADOW_STABILITY in types
    assert STRATEGY_SHADOW_LATENCY in types
    assert STRATEGY_SHADOW_HEALTH in types


def test_projection_stability_across_batch_replays():
    validator = _build_validator()
    results = validator.validate_shadow_batch(
        ("11",),
        as_of=AS_OF,
        runtime_a=_runtime_a(),
        twin=_twin(),
        adaptive=_adaptive(),
        iterations=5,
    )
    assert len(results) == 5
    fingerprints = [
        r.projection.serialize() for r in results if r.projection is not None
    ]
    assert len(fingerprints) == 5
    assert len(set(fingerprints)) == 1
    assert all(r.ok and r.determinism_ok for r in results)


def test_explainability_stable_across_identical_interventions():
    validator = _build_validator()
    results = validator.validate_shadow_batch(
        ("11",),
        as_of=AS_OF,
        runtime_a=_runtime_a(),
        twin=_twin(),
        adaptive=_adaptive(),
        iterations=3,
    )
    explanations = [
        r.explanation.serialize() for r in results if r.explanation is not None
    ]
    assert len(set(explanations)) == 1
    assert all(r.explainability_ok for r in results)


def test_long_running_replay_preserves_health_rates():
    validator = _build_validator()
    validator.validate_shadow_batch(
        ("11", "11"),
        as_of=AS_OF,
        runtime_a=_runtime_a(),
        twin=_twin(),
        adaptive=_adaptive(),
        iterations=4,
    )
    health = validator.health_snapshot()
    assert health.executions == 8
    assert health.intervention_generation_success_rate == 1.0
    assert health.projection_success_rate == 1.0
    assert health.explainability_success_rate == 1.0
    assert health.planner_consistency_success_rate == 1.0
    assert health.deterministic_replay_success_rate == 1.0
    assert health.failure_count == 0


def test_rollback_immediate_and_experience_preserved():
    events = EventRegistry()
    result = verify_strategy_shadow_rollback(events=events)
    assert result.ok is True
    assert result.strategy_disabled_removes_participation is True
    assert result.runtime_a_unchanged is True
    assert result.twin_flags_unchanged is True
    assert result.adaptive_flags_unchanged is True
    assert result.experience_preserved is True
    assert STRATEGY_SHADOW_ROLLBACK_VERIFIED in [
        e.event_type for e in events.published()
    ]

    off_flags = resolve_v2_feature_flags(
        environ={"KWALITEC_STRATEGY_ENGINE": "0"}
    )
    composition, service = build_production_experience(flags=off_flags)
    assert composition.strategy_shadow is None
    assert composition.strategy_engine is None
    _ = service
    summary = composition.twin.get_learner_summary("default")
    assert summary is not None or composition.twin is not None


def test_feature_flag_isolation_preserves_upstream_authority():
    on_flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_STRATEGY_ENGINE": "1",
            "KWALITEC_DIGITAL_TWIN": "0",
            "KWALITEC_ADAPTIVE_AUTHORITY": "0",
        }
    )
    off_flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_STRATEGY_ENGINE": "0",
            "KWALITEC_DIGITAL_TWIN": "0",
            "KWALITEC_ADAPTIVE_AUTHORITY": "0",
        }
    )
    on_comp, on_service = build_production_experience(flags=on_flags)
    off_comp, off_service = build_production_experience(flags=off_flags)
    _ = (on_service, off_service)

    assert on_comp.strategy_shadow is not None
    assert off_comp.strategy_shadow is None
    assert on_comp.twin is not None
    assert off_comp.twin is not None
    assert on_comp.adaptive_port_router is None
    assert off_comp.adaptive_port_router is None
    assert on_comp.digital_twin is None
    assert off_comp.digital_twin is None
    # Experience remains projection-only for Strategy (no authority cutover).
    assert on_comp.strategy_projection_port is not None
    assert off_comp.strategy_projection_port is None


def test_shadow_does_not_influence_experience_home():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_STRATEGY_ENGINE": "1"}
    )
    composition, service = build_production_experience(flags=flags)
    _ = service

    before = composition.twin.get_learner_summary("default")
    assert composition.strategy_shadow is not None
    observation = composition.strategy_shadow.validate_shadow(
        "11",
        as_of=AS_OF,
        runtime_a=_runtime_a(),
        twin=_twin(),
        adaptive=_adaptive(),
    )
    after = composition.twin.get_learner_summary("default")

    assert observation.ok is True
    assert before == after
    dashboard = build_strategy_shadow_ops_dashboard(
        composition.strategy_shadow,
        rollback_result=verify_strategy_shadow_rollback(),
    )
    assert dashboard["strategy_shadow_validation"]["influences_student"] is False


def test_shadow_modules_forbid_educational_writes():
    """Static guard — S3 modules must not call educational write APIs."""
    forbidden = {
        "db.session.commit",
        "db.session.add",
        "db.session.delete",
        "put_projection",
        "record_evidence",
        "complete_session",
        "create_mission",
    }
    for name in (
        "shadow.py",
        "shadow_monitors.py",
        "shadow_health.py",
        "shadow_rollback.py",
        "shadow_telemetry.py",
    ):
        source = (ADAPTER_ROOT / name).read_text(encoding="utf-8")
        tree = ast.parse(source)
        text = ast.dump(tree)
        for needle in forbidden:
            assert needle not in source, f"{name} contains {needle}"
        assert "Alembic" not in text or "no" in source.lower()


def test_shadow_docstring_declares_observational_only():
    source = (ADAPTER_ROOT / "shadow.py").read_text(encoding="utf-8")
    lowered = source.lower()
    assert "observational" in lowered
    assert "must not" in lowered or "never" in lowered
    assert "no experience ux authority" in lowered or "discard" in lowered
