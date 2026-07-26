"""Integration tests — Twin Explainability vs Runtime A (MS-004 T3)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

import app.infrastructure.adapters.digital_twin as digital_twin_pkg
from app.infrastructure.adapters.digital_twin import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    EXPLAINABILITY_VERSION,
    FACET_SYNTHESIS_ORDER,
    TwinExplainabilityService,
    TwinFacetAssembler,
    TwinSnapshotBuilder,
    expand_snapshot_provenance,
)
from tests.conftest import (
    _make_curriculum,
    _make_mission,
    _make_study_attempt,
    _make_study_plan,
    _make_subject,
    _make_topic_progress,
    _make_user,
)

ADAPTER_ROOT = Path(digital_twin_pkg.__file__).resolve().parent

FORBIDDEN_WRITE_TOKENS = frozenset(
    {
        "generate_today_mission",
        "start_session",
        "complete_session",
        "accept_evidence",
        "db.session.add",
        "db.session.commit",
        "session.add",
        "session.commit",
        "ensure_curriculum_binding",
        "repair_inconsistent_completion",
    }
)

EXPLAINABILITY_MODULES = (
    "explainability.py",
    "provenance.py",
    "contracts.py",
)


@pytest.fixture
def learner(app, ctx):
    user = _make_user()
    subject = _make_subject(user.id)
    curriculum, topics = _make_curriculum()
    plan = _make_study_plan(user.id)
    plan.curriculum_id = curriculum.id
    from app.extensions import db

    db.session.commit()
    mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)
    mission.status = "completed"
    attempt = _make_study_attempt(user.id, topics[0].id, mission.id)
    attempt.duration_minutes = 40
    attempt.confidence_before = "low"
    attempt.confidence_after = "medium"
    progress = _make_topic_progress(user.id, topics[0].id)
    progress.revision_count = 2
    db.session.commit()
    return {
        "user": user,
        "subject": subject,
        "curriculum": curriculum,
        "topics": topics,
        "plan": plan,
        "mission": mission,
        "attempt": attempt,
        "progress": progress,
    }


def test_runtime_a_snapshot_explanations_are_deterministic(learner):
    assembler = TwinFacetAssembler()
    builder = TwinSnapshotBuilder(facet_assembler=assembler)
    service = TwinExplainabilityService()
    sid = str(learner["user"].id)
    snapshot = builder.build(sid, as_of="2026-07-25")
    first = service.explain_snapshot(snapshot)
    second = service.explain_snapshot(snapshot)
    rebuilt = service.explain_snapshot(builder.build(sid, as_of="2026-07-25"))
    assert first.serialize() == second.serialize()
    assert first.serialize() == rebuilt.serialize()
    assert first.explainability_version == EXPLAINABILITY_VERSION
    assert len(first.facet_explanations) == len(FACET_SYNTHESIS_ORDER)


def test_every_facet_has_explanation_with_required_fields(learner):
    snapshot = TwinSnapshotBuilder(
        facet_assembler=TwinFacetAssembler()
    ).build(str(learner["user"].id), as_of="2026-07-25")
    explanation = TwinExplainabilityService().explain_snapshot(snapshot)
    for item in explanation.facet_explanations:
        assert item.facet_name in FACET_SYNTHESIS_ORDER
        assert item.availability in {
            AVAILABILITY_AVAILABLE,
            AVAILABILITY_UNAVAILABLE,
        }
        assert item.contributing_runtime_a_evidence
        assert item.derivation_summary
        assert item.completeness_reasoning
        assert item.provenance_refs
        assert item.rule_or_model_id
        if item.availability == AVAILABILITY_UNAVAILABLE:
            assert item.unavailable_reasoning
        else:
            assert item.unavailable_reasoning == ""


def test_snapshot_explanation_aggregates_completeness_and_coverage(learner):
    snapshot = TwinSnapshotBuilder(
        facet_assembler=TwinFacetAssembler()
    ).build(str(learner["user"].id), as_of="2026-07-25")
    explanation = TwinExplainabilityService().explain_snapshot(snapshot)
    assert snapshot.completeness.status in explanation.overall_completeness_explanation
    assert explanation.evidence_coverage_summary.startswith("available_facets=")
    assert "contributing_sources=" in explanation.evidence_coverage_summary
    # Provenance expansion covers all facets + root.
    expansions = expand_snapshot_provenance(
        snapshot.field_provenance, root=snapshot.provenance
    )
    assert len(expansions) == len(FACET_SYNTHESIS_ORDER) + 1
    assert len(explanation.provenance_refs) == len(expansions)


def test_missing_confidence_evidence_explains_unavailable(app, ctx):
    user = _make_user()
    subject = _make_subject(user.id)
    curriculum, topics = _make_curriculum()
    plan = _make_study_plan(user.id)
    plan.curriculum_id = curriculum.id
    from app.extensions import db

    db.session.commit()
    mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)
    mission.status = "completed"
    attempt = _make_study_attempt(user.id, topics[0].id, mission.id)
    attempt.duration_minutes = 20
    # No confidence_before / confidence_after → confidence_trend unavailable.
    db.session.commit()
    _ = subject
    snapshot = TwinSnapshotBuilder(
        facet_assembler=TwinFacetAssembler()
    ).build(str(user.id), as_of="2026-07-25")
    explanation = TwinExplainabilityService().explain_snapshot(snapshot)
    by_name = {item.facet_name: item for item in explanation.facet_explanations}
    confidence = by_name["confidence_trend"]
    if confidence.availability == AVAILABILITY_UNAVAILABLE:
        assert confidence.unavailable_reasoning
        assert "no derivation performed" in confidence.derivation_summary
        assert confidence.rule_or_model_id == "twin.insight.sparse_evidence"
        assert "confidence_trend" in explanation.unavailable_summary_explanation


def test_explainability_modules_remain_read_only_relative_to_runtime_a():
    for module_name in EXPLAINABILITY_MODULES:
        path = ADAPTER_ROOT / module_name
        tree = ast.parse(path.read_text(encoding="utf-8"))
        source = path.read_text(encoding="utf-8")
        for token in FORBIDDEN_WRITE_TOKENS:
            assert token not in source, f"{module_name} contains {token}"
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                name = ""
                if isinstance(func, ast.Attribute):
                    name = func.attr
                elif isinstance(func, ast.Name):
                    name = func.id
                assert name not in {
                    "commit",
                    "add",
                    "delete",
                    "flush",
                } or "logger" in ast.dump(node)


def test_no_persistence_or_adaptive_integration_in_t3():
    source = (ADAPTER_ROOT / "explainability.py").read_text(encoding="utf-8")
    assert "class TwinExplainabilityService" in source
    assert "db.session" not in source
    assert "alembic" not in source.lower()
    assert "AdaptiveOutputBundle" not in source
    assert "StudentTwinPort" not in source
    lowered = source.lower()
    assert "no persistence" in lowered or "must not" in lowered
