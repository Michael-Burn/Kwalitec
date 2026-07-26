"""Unit tests — Strategy Experience Projection (MS-005 S2)."""

from __future__ import annotations

from types import MappingProxyType

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.strategy_engine import (
    AUTHORITY_STRATEGY_ENGINE,
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    LearningIntervention,
    StrategyContextAssembler,
    StrategyEngine,
    StrategyExperienceProjectionPort,
    StrategyExplainabilityService,
    StrategyExplanationSummaryProjection,
    StrategyProjection,
    StrategyProjectionPort,
    StrategyProjectionProvenance,
    StrategyProjector,
    build_strategy_projection_port,
    build_strategy_projector,
    serialize_canonical,
)
from app.infrastructure.adapters.strategy_engine.projection import (
    REASON_STRATEGY_FLAG_OFF,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)


def _runtime_a():
    return {
        "mission": {
            "mission_id": "9",
            "topic_code": "T-MISSION",
            "status": "pending",
        },
        "lifecycle_stage": "Learning",
        "student_goals": {"daily_minutes": 45},
        "evidence": {"evidence_id": "ev-1"},
        "topic_progress": [{"topic_id": "T-MISSION", "mastery_score": 0.4}],
        "study_attempts": [{"id": "a1", "score": 0.5}],
    }


def _twin():
    return {
        "twin_id": "twin-1",
        "snapshot_version": "snap-1",
        "profile": {
            "session_habits": {"label": "evening", "availability": "available"},
            "learning_rhythm": {"label": "steady", "availability": "available"},
            "cognitive_load_indicators": {
                "label": "low",
                "availability": "available",
            },
            "confidence_trend": {"label": "cautious", "availability": "available"},
            "persistence": {"label": "steady", "availability": "available"},
            "revision_behaviour": {"label": "active", "availability": "available"},
            "consistency": {"label": "regular", "availability": "available"},
        },
    }


def _adaptive():
    return {
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


def _full_intervention() -> LearningIntervention:
    context = StrategyContextAssembler().assemble(
        "42",
        as_of="2026-07-25T10:00:00",
        runtime_a=_runtime_a(),
        twin=_twin(),
        adaptive=_adaptive(),
    )
    return StrategyEngine().evaluate(context)


def test_projection_dtos_are_immutable():
    summary = StrategyExplanationSummaryProjection(
        why_summary="because",
        educational_objective="session",
        principle_ids=("ep.director.nightly_topic",),
    )
    provenance = StrategyProjectionProvenance(
        intervention_id="s1-abc",
        adaptive_decision_id="adaptive-7",
        twin_snapshot_ref="twin-1",
        provenance_refs=("mission:9",),
    )
    projection = StrategyProjection(
        student_id="42",
        intervention_id="s1-abc",
        strategy_decision_id="s1-abc",
        projection_version="s2.0",
        primary_intervention_kind="SESSION_PLAN",
        session_plan={"primary_topic": "T-MISSION"},
        explanation_summary=summary,
        provenance=provenance,
        availability="available",
    )
    assert isinstance(projection.session_plan, MappingProxyType)
    with pytest.raises((TypeError, AttributeError)):
        projection.student_id = "x"  # type: ignore[misc]
    with pytest.raises((TypeError, AttributeError)):
        projection.session_plan["x"] = 1  # type: ignore[index]


def test_project_exposes_allowed_fields_only():
    projector = StrategyProjector()
    intervention = _full_intervention()
    explanation = StrategyExplainabilityService().explain(intervention)
    projection = projector.project(
        intervention, explanation=explanation, student_id="42"
    )

    assert isinstance(projection, StrategyProjection)
    assert projection.availability == AVAILABILITY_AVAILABLE
    assert projection.authority == AUTHORITY_STRATEGY_ENGINE
    assert projection.student_id == "42"
    assert projection.primary_intervention_kind == intervention.kind
    assert projection.topic_code == intervention.session.primary_topic
    assert projection.adaptive_decision_id
    assert projection.twin_snapshot_ref == intervention.twin_ref
    assert projection.explanation_summary.why_summary
    assert projection.explanation_summary.runtime_a_ref_count > 0
    assert "LearningIntervention" not in projection.serialize()
    assert "StrategyEngine" not in projection.serialize()
    payload = projection.to_canonical_dict()
    assert "db.session" not in serialize_canonical(payload)


def test_project_is_deterministic():
    projector = StrategyProjector()
    intervention = _full_intervention()
    explanation = StrategyExplainabilityService().explain(intervention)
    left = projector.project(
        intervention, explanation=explanation, student_id="42"
    ).serialize()
    right = projector.project(
        intervention, explanation=explanation, student_id="42"
    ).serialize()
    assert left == right


def test_projection_port_implements_protocol():
    port = StrategyExperienceProjectionPort(
        explainability=StrategyExplainabilityService()
    )
    assert isinstance(port, StrategyProjectionPort)
    intervention = _full_intervention()
    projection = port.serve_projection(intervention, student_id="42")
    assert projection.student_id == "42"

    result = port.get_tonight_projection("42")
    assert result.ok is True
    assert result.value is not None
    opaque = port.get_tonight_opaque("42")
    assert opaque is not None
    assert opaque["authority"] == AUTHORITY_STRATEGY_ENGINE
    assert opaque["primary_intervention_kind"] == intervention.kind
    assert "LearningIntervention" not in serialize_canonical(opaque)


def test_projection_port_unknown_student_returns_none():
    port = StrategyExperienceProjectionPort()
    assert port.get_projection("missing") is None
    result = port.get_tonight_projection("missing")
    assert result.ok is False
    assert result.error_code == "NOT_FOUND"


def test_projection_port_flag_off_unavailable():
    port = StrategyExperienceProjectionPort(enabled=False)
    projection = port.get_projection("42")
    assert projection is not None
    assert projection.availability == AVAILABILITY_UNAVAILABLE
    assert projection.unavailable_reason == REASON_STRATEGY_FLAG_OFF


def test_projection_port_provider_path():
    intervention = _full_intervention()

    def provider(student_id: str) -> LearningIntervention | None:
        return intervention if student_id == "42" else None

    port = StrategyExperienceProjectionPort(
        explainability=StrategyExplainabilityService(),
        intervention_provider=provider,
    )
    projection = port.get_projection("42")
    assert projection is not None
    assert projection.primary_intervention_kind == intervention.kind
    assert port.get_projection("99") is None


def test_build_helpers_respect_flag():
    assert build_strategy_projector(enabled=False) is None
    assert build_strategy_projection_port(enabled=False) is None
    projector = build_strategy_projector(enabled=True)
    port = build_strategy_projection_port(enabled=True, projector=projector)
    assert projector is not None
    assert port is not None


def test_flag_on_wires_projection_di():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_STRATEGY_ENGINE": "1"}
    )
    composition, _ = build_production_experience(flags=flags)
    assert composition.strategy_projector is not None
    assert composition.strategy_projection_port is not None
    assert composition.strategy_projection_port.is_available()
