"""Unit tests — Adaptive Experience Port Cutover (MS-003 A4)."""

from __future__ import annotations

from types import SimpleNamespace
from unittest import mock

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.adaptive import ExperienceAdaptiveAdapter
from app.infrastructure.adapters.adaptive_engine import (
    AUTHORITY_ADAPTIVE_ENGINE,
    AdaptiveExperiencePortRouter,
    AdaptiveOutputBundle,
    ConfidencePlaceholder,
    EvidenceRef,
    ExplanationBundle,
    RecommendationPlaceholder,
    RuleRef,
    adaptive_experience_cutover_active,
    build_adaptive_experience_port_router,
    empty_adaptive_output,
    map_adaptive_output_to_recommendation,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    ADAPTIVE_ENGINE_FAILURE,
    ADAPTIVE_ENGINE_FALLBACK,
    ADAPTIVE_ENGINE_LATENCY,
    ADAPTIVE_ENGINE_REQUESTED,
    ADAPTIVE_ENGINE_SUCCESS,
)


def _complete_output(*, decision_id: str = "a4-test-1") -> AdaptiveOutputBundle:
    return AdaptiveOutputBundle(
        recommendation=RecommendationPlaceholder(
            topic_code="T1",
            title="Topic One",
            decision_kind="NEXT_FOCUS",
            label="Topic One",
        ),
        confidence=ConfidencePlaceholder(score=0.7, band="medium"),
        explanation=ExplanationBundle(
            evidence_refs=(
                EvidenceRef(kind="study_attempt", id="attempt-1"),
            ),
            rule_refs=(
                RuleRef(
                    rule_or_model_id="adaptive.shadow.mission_aligned",
                    version="1.0.0-a2",
                ),
            ),
            confidence=ConfidencePlaceholder(score=0.7, band="medium"),
            input_summary="student_id=1",
            recommendation_rationale="Mission-aligned next focus.",
            why_summary="Continue today's mission topic.",
            inputs_used=("mission", "curriculum"),
            inputs_unavailable=(),
            mission_aligned=True,
            mission_note="Aligned to today's mission.",
        ),
        decision_id=decision_id,
        authority=AUTHORITY_ADAPTIVE_ENGINE,
    )


def test_authority_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_ADAPTIVE_AUTHORITY is False
    assert adaptive_experience_cutover_active(
        engine_enabled=False,
        shadow_enabled=False,
        authority_enabled=False,
    ) is False


def test_cutover_requires_engine_shadow_and_authority():
    assert adaptive_experience_cutover_active(
        engine_enabled=True,
        shadow_enabled=True,
        authority_enabled=False,
    ) is False
    assert adaptive_experience_cutover_active(
        engine_enabled=True,
        shadow_enabled=False,
        authority_enabled=True,
    ) is False
    assert adaptive_experience_cutover_active(
        engine_enabled=True,
        shadow_enabled=True,
        authority_enabled=True,
    ) is True


def test_map_adaptive_output_to_recommendation_shape():
    projected = map_adaptive_output_to_recommendation(
        _complete_output(), student_id="42"
    )
    assert projected is not None
    assert projected["authority"] == AUTHORITY_ADAPTIVE_ENGINE
    assert projected["next_action_authority"] is True
    assert projected["fallback_used"] is False
    assert projected["topic_code"] == "T1"
    assert projected["recommendation_label"] == "Topic One"
    assert projected["mission_aligned"] is True
    assert projected["decision_id"] == "a4-test-1"
    assert "adaptive.shadow.mission_aligned" in projected["rule_or_model_ids"]


def test_map_rejects_empty_label():
    empty = empty_adaptive_output()
    assert map_adaptive_output_to_recommendation(empty, student_id="1") is None


def test_router_returns_none_when_cutover_inactive():
    router = AdaptiveExperiencePortRouter(cutover_active=False)
    assert router.try_adaptive_recommendation("1") is None
    assert router.last_fallback_reason == "cutover_inactive"


def test_router_exposes_pass_bundle():
    events = EventRegistry()
    output = _complete_output()
    gate = mock.Mock()
    gate.validate.return_value = SimpleNamespace(
        passed=True,
        error_code=None,
        decision_id=output.decision_id,
    )
    engine = mock.Mock()
    engine.decide.return_value = SimpleNamespace(ok=True, value=output)
    assembler = mock.Mock()
    assembler.assemble.return_value = SimpleNamespace(student_id="1")

    router = AdaptiveExperiencePortRouter(
        assembler=assembler,
        engine=engine,
        gate=gate,
        events=events,
        cutover_active=True,
    )
    projected = router.try_adaptive_recommendation("1")
    assert projected is not None
    assert projected["authority"] == AUTHORITY_ADAPTIVE_ENGINE
    types = [e.event_type for e in events.published()]
    assert ADAPTIVE_ENGINE_REQUESTED in types
    assert ADAPTIVE_ENGINE_SUCCESS in types
    assert ADAPTIVE_ENGINE_LATENCY in types
    assert ADAPTIVE_ENGINE_FALLBACK not in types


def test_router_falls_back_when_gate_fails():
    events = EventRegistry()
    output = _complete_output()
    gate = mock.Mock()
    gate.validate.return_value = SimpleNamespace(
        passed=False,
        error_code="EXPLAINABILITY_INCOMPLETE",
        decision_id=output.decision_id,
    )
    engine = mock.Mock()
    engine.decide.return_value = SimpleNamespace(ok=True, value=output)
    assembler = mock.Mock()
    assembler.assemble.return_value = SimpleNamespace(student_id="1")

    router = AdaptiveExperiencePortRouter(
        assembler=assembler,
        engine=engine,
        gate=gate,
        events=events,
        cutover_active=True,
    )
    assert router.try_adaptive_recommendation("1") is None
    assert router.last_fallback_reason == "explainability_ineligible"
    types = [e.event_type for e in events.published()]
    assert ADAPTIVE_ENGINE_FALLBACK in types


def test_router_falls_back_on_exception():
    events = EventRegistry()
    assembler = mock.Mock()
    assembler.assemble.side_effect = RuntimeError("boom")
    router = AdaptiveExperiencePortRouter(
        assembler=assembler,
        engine=mock.Mock(),
        gate=mock.Mock(),
        events=events,
        cutover_active=True,
    )
    assert router.try_adaptive_recommendation("1") is None
    assert router.last_fallback_reason == "adaptive_exception"
    types = [e.event_type for e in events.published()]
    assert ADAPTIVE_ENGINE_FAILURE in types
    assert ADAPTIVE_ENGINE_FALLBACK in types


def test_experience_adapter_uses_adaptive_then_fallback():
    fallback_doc = {
        "recommendation": {
            "title": "From RecommendationService",
            "authority": "recommendation_bridge",
        }
    }
    store = mock.Mock()
    store.adaptive = "adaptive"
    store.get.return_value = fallback_doc

    router = mock.Mock()
    router.cutover_active = True
    router.try_adaptive_recommendation.return_value = {
        "title": "From Adaptive",
        "authority": AUTHORITY_ADAPTIVE_ENGINE,
    }
    adapter = ExperienceAdaptiveAdapter(
        store=store,
        adaptive_port_router=router,
        auto_provision=False,
    )
    assert (
        adapter.get_todays_recommendation("1")["authority"]
        == AUTHORITY_ADAPTIVE_ENGINE
    )

    router.try_adaptive_recommendation.return_value = None
    result = adapter.get_todays_recommendation("1")
    assert result["title"] == "From RecommendationService"


def test_di_wires_router_only_when_authority_on():
    flags_no_auth = resolve_v2_feature_flags(
        environ={
            "KWALITEC_ADAPTIVE_ENGINE": "1",
            "KWALITEC_ADAPTIVE_SHADOW": "1",
        }
    )
    composition_no_auth, _ = build_production_experience(flags=flags_no_auth)
    assert composition_no_auth.adaptive_port_router is None
    assert composition_no_auth.adaptive._adaptive_port_router is None

    flags_auth = resolve_v2_feature_flags(
        environ={
            "KWALITEC_ADAPTIVE_ENGINE": "1",
            "KWALITEC_ADAPTIVE_SHADOW": "1",
            "KWALITEC_ADAPTIVE_AUTHORITY": "1",
        }
    )
    composition_auth, _ = build_production_experience(flags=flags_auth)
    assert isinstance(
        composition_auth.adaptive_port_router, AdaptiveExperiencePortRouter
    )
    assert composition_auth.adaptive._adaptive_port_router is not None


def test_build_helper_respects_enabled_false():
    assert (
        build_adaptive_experience_port_router(
            enabled=False,
            assembler=object(),
            engine=object(),
            gate=object(),
        )
        is None
    )
