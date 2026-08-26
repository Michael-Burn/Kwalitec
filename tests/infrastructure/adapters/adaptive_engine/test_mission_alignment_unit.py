"""Unit tests — Adaptive mission-alignment delivery policy."""

from __future__ import annotations

from types import SimpleNamespace
from unittest import mock

from app.infrastructure.adapters.adaptive_engine import (
    AUTHORITY_ADAPTIVE_ENGINE,
    AdaptiveEngineExecutor,
    AdaptiveExperiencePortRouter,
    AdaptiveInputBundle,
    AdaptiveOutputBundle,
    ConfidencePlaceholder,
    EvidenceRef,
    ExplanationBundle,
    RecommendationComparisonMonitor,
    RecommendationPlaceholder,
    RuleRef,
    ShadowSoakOrchestrator,
    TopicRef,
    apply_mission_alignment_to_projection,
    map_adaptive_output_to_recommendation,
)
from app.infrastructure.adapters.adaptive_engine.contracts import AdaptiveDecisionResult
from app.infrastructure.adapters.adaptive_engine.executor import (
    RULE_WEAK_TOPIC_PRIORITY,
)
from app.infrastructure.adapters.adaptive_engine.mission_alignment import (
    apply_mission_alignment_to_output,
    mission_baseline_dict,
)
from app.infrastructure.adapters.adaptive_engine.provenance import (
    available_provenance,
    unavailable_provenance,
)
from app.infrastructure.events.registry import EventRegistry


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


def _independent_output(
    *, topic_code: str = "WEAK", title: str = "Weak Topic"
) -> AdaptiveOutputBundle:
    return AdaptiveOutputBundle(
        recommendation=RecommendationPlaceholder(
            topic_code=topic_code,
            title=title,
            decision_kind="NEXT_FOCUS",
            label=title,
        ),
        confidence=ConfidencePlaceholder(score=0.6, band="medium"),
        explanation=ExplanationBundle(
            evidence_refs=(EvidenceRef(kind="study_attempt", id="a1"),),
            rule_refs=(
                RuleRef(
                    rule_or_model_id="adaptive.shadow.next_incomplete_leaf",
                    version="1.0.0-a2",
                ),
            ),
            confidence=ConfidencePlaceholder(score=0.6, band="medium"),
            recommendation_rationale="Independent adaptive pick.",
            why_summary=f"Focus on {title}.",
            topic_refs=(
                TopicRef(topic_code=topic_code, title=title, role="primary"),
            ),
            inputs_used=("curriculum", "topic_progress"),
            inputs_unavailable=(),
            mission_aligned=False,
        ),
        decision_id="align-test-1",
        authority=AUTHORITY_ADAPTIVE_ENGINE,
    )


def test_map_forces_primary_to_mission_when_independent_differs():
    """(a) Mission exists + Adaptive differs → primary = mission; pick is alt."""
    output = _independent_output(topic_code="WEAK", title="Weak Topic")
    mission = SimpleNamespace(id="99", title="Study Compound Interest", topic_code="")
    projected = map_adaptive_output_to_recommendation(
        output, student_id="42", mission=mission
    )
    assert projected is not None
    assert projected["recommendation_label"] == "Study Compound Interest"
    assert projected["title"] == "Study Compound Interest"
    assert projected["topic_title"] == "Study Compound Interest"
    assert projected["mission_aligned"] is True
    assert projected["mission_id"] == "99"
    alt_titles = {
        str(a.get("title") or a.get("recommendation_label") or "")
        for a in projected["alternatives"]
    }
    assert "Weak Topic" in alt_titles


def test_map_keeps_independent_primary_when_no_mission():
    """(b) No mission → Adaptive independent pick remains primary."""
    output = _independent_output(topic_code="WEAK", title="Weak Topic")
    projected = map_adaptive_output_to_recommendation(
        output, student_id="42", mission=None
    )
    assert projected is not None
    assert projected["recommendation_label"] == "Weak Topic"
    assert projected["topic_code"] == "WEAK"
    assert projected["mission_aligned"] is False


def test_hard_override_applies_in_revision_when_mission_present():
    """(c) Revision Mode with mission → same hard override as Learning."""
    base = _independent_output(topic_code="9", title="Weak Revision Topic")
    output = AdaptiveOutputBundle(
        recommendation=RecommendationPlaceholder(
            topic_code="9",
            title="Weak Revision Topic",
            decision_kind="REVISION_SET",
            label="Weak Revision Topic",
        ),
        confidence=base.confidence,
        explanation=ExplanationBundle(
            evidence_refs=base.explanation.evidence_refs,
            rule_refs=(
                RuleRef(
                    rule_or_model_id="adaptive.shadow.weak_topic_priority",
                    version="1.0.0-a2",
                ),
            ),
            confidence=base.confidence,
            recommendation_rationale="Revision weak topic.",
            why_summary="Revise Weak Revision Topic.",
            inputs_used=("topic_progress", "lifecycle_stage"),
            inputs_unavailable=(),
            mission_aligned=False,
        ),
        decision_id="align-rev-1",
        authority=AUTHORITY_ADAPTIVE_ENGINE,
    )
    mission = SimpleNamespace(
        id="77", title="Revision: Mixed Practice Set", topic_code=""
    )
    projected = apply_mission_alignment_to_projection(
        map_adaptive_output_to_recommendation(output, student_id="3", mission=None),
        mission,
    )
    assert projected is not None
    assert projected["recommendation_label"] == "Revision: Mixed Practice Set"
    assert projected["mission_aligned"] is True
    assert any(
        (a.get("title") or "") == "Weak Revision Topic"
        for a in projected["alternatives"]
    )


def test_soak_agrees_when_mission_baseline_and_aligned_output():
    """(d) Soak with mission baseline + post-alignment Adaptive → agreed."""
    events = EventRegistry()
    raw = _independent_output(topic_code="T99", title="Independent Leaf")
    shadow = mock.Mock()
    shadow.execute_shadow.return_value = AdaptiveDecisionResult(ok=True, value=raw)
    shadow.last_gate_result = SimpleNamespace(passed=True)
    shadow.last_trace = SimpleNamespace(decision_id="align-test-1")
    shadow._assembler = None
    shadow._executor = None
    shadow._traceability = None

    baseline_svc = SimpleNamespace(
        generate_recommendations=mock.Mock(
            return_value=[
                {"title": "Other Rec", "topic_code": "OTHER", "category": "Weak"}
            ]
        )
    )
    inputs = AdaptiveInputBundle(
        student_id="42",
        as_of="2026-07-25",
        mission={
            "today": {
                "mission_id": "55",
                "mission_date": "2026-07-25",
                "title": "Study Compound Interest",
                "status": "Pending",
            },
            "history": [],
            "history_count": 0,
        },
        curriculum={"leaves": [], "leaf_count": 0},
        field_provenance=_full_available_provenance(),
    )
    soak = ShadowSoakOrchestrator(
        shadow=shadow,
        events=events,
        enabled=True,
        recommendation_service=baseline_svc,
        emit_health_on_complete=False,
    )
    observation = soak.execute_soak(
        "42", as_of="2026-07-25", inputs=inputs, run_determinism_replay=False
    )
    assert observation.ok is True
    assert observation.baseline is not None
    assert observation.baseline.get("baseline_kind") == "mission"
    assert observation.baseline["title"] == "Study Compound Interest"
    assert observation.comparison is not None
    assert observation.comparison.agreed is True
    assert observation.comparison.divergence_reason == ""
    assert observation.comparison.adaptive_label == "Study Compound Interest"


def test_comparison_monitor_mission_baseline_prefers_label():
    """Mission baseline agrees on title even when Adaptive topic_code differs."""
    monitor = RecommendationComparisonMonitor()
    baseline = mission_baseline_dict(
        SimpleNamespace(id="1", title="Study Compound Interest", topic_code="")
    )
    aligned = apply_mission_alignment_to_output(
        _independent_output(topic_code="T99", title="Independent Leaf"),
        SimpleNamespace(id="1", title="Study Compound Interest", topic_code=""),
    )
    comparison = monitor.compare(baseline, aligned)
    assert comparison.agreed is True
    assert comparison.baseline_label == "Study Compound Interest"
    assert comparison.adaptive_label == "Study Compound Interest"


def test_executor_revision_lowercase_triggers_weak_topic_priority():
    """(e) Assembler-normalized 'revision' hits RULE_WEAK_TOPIC_PRIORITY."""
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
        lifecycle_stage="revision",
        field_provenance=_full_available_provenance(),
    )
    output = executor.evaluate(inputs)
    assert output.recommendation.topic_code == "9"
    assert output.recommendation.decision_kind == "REVISION_SET"
    assert (
        output.explanation.rule_refs[0].rule_or_model_id == RULE_WEAK_TOPIC_PRIORITY
    )


def test_authority_router_passes_as_of_and_applies_mission_override():
    """Authority assemble receives as_of; delivery forces mission primary."""
    events = EventRegistry()
    output = _independent_output(topic_code="WEAK", title="Weak Topic")
    gate = mock.Mock()
    gate.validate.return_value = SimpleNamespace(
        passed=True, error_code=None, decision_id=output.decision_id
    )
    engine = mock.Mock()
    engine.decide.return_value = SimpleNamespace(ok=True, value=output)
    assembler = mock.Mock()
    assembler.assemble.return_value = AdaptiveInputBundle(
        student_id="1",
        as_of="2026-07-25",
        mission={
            "today": {
                "mission_id": "88",
                "title": "Tonight's Mission Topic",
                "mission_date": "2026-07-25",
            },
            "history": [],
            "history_count": 0,
        },
        field_provenance=_full_available_provenance(),
    )

    router = AdaptiveExperiencePortRouter(
        assembler=assembler,
        engine=engine,
        gate=gate,
        events=events,
        cutover_active=True,
    )
    with mock.patch(
        "app.infrastructure.adapters.adaptive_engine.port_cutover.resolve_today_as_of",
        return_value="2026-07-25",
    ):
        projected = router.try_adaptive_recommendation("1")

    assert projected is not None
    assembler.assemble.assert_called_once_with("1", as_of="2026-07-25")
    assert projected["recommendation_label"] == "Tonight's Mission Topic"
    assert projected["mission_aligned"] is True
    assert any(
        (a.get("title") or "") == "Weak Topic" for a in projected["alternatives"]
    )
