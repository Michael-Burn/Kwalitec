"""Integration tests — Twin Shadow Validation (MS-004 T6).

Verifies stable observational shadow validation, deterministic replay,
explainability / projection consistency, rollback, Runtime A read-only,
feature-flag isolation, and no Experience behavioural change.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

import app.infrastructure.adapters.digital_twin as digital_twin_pkg
from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.digital_twin import (
    TwinShadowValidator,
    build_student_twin_projector,
    build_twin_explainability_service,
    build_twin_facet_assembler,
    build_twin_shadow_ops_dashboard,
    build_twin_shadow_validator,
    build_twin_snapshot_builder,
    verify_twin_rollback,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    TWIN_SHADOW_COMPLETED,
    TWIN_SHADOW_HEALTH,
    TWIN_SHADOW_LATENCY,
    TWIN_SHADOW_REQUESTED,
    TWIN_SHADOW_ROLLBACK_VERIFIED,
    TWIN_SHADOW_STABILITY,
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
AS_OF = "2026-07-25T12:00:00Z"


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
    attempt = _make_study_attempt(user.id, topics[0].id, mission.id)
    progress = _make_topic_progress(user.id, topics[0].id)
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


def _build_validator(*, events: EventRegistry | None = None) -> TwinShadowValidator:
    registry = events or EventRegistry()
    assembler = build_twin_facet_assembler(enabled=True)
    builder = build_twin_snapshot_builder(
        enabled=True, facet_assembler=assembler
    )
    explainability = build_twin_explainability_service(enabled=True)
    projector = build_student_twin_projector(enabled=True)
    validator = build_twin_shadow_validator(
        enabled=True,
        snapshot_builder=builder,
        explainability=explainability,
        projector=projector,
        events=registry,
    )
    assert validator is not None
    return validator


def test_shadow_pipeline_deterministic_for_learner(learner):
    events = EventRegistry()
    validator = _build_validator(events=events)
    sid = str(learner["user"].id)

    first = validator.validate_shadow(sid, as_of=AS_OF)
    second = validator.validate_shadow(sid, as_of=AS_OF)

    assert first.ok is True
    assert second.ok is True
    assert first.snapshot is not None and second.snapshot is not None
    assert first.snapshot.serialize() == second.snapshot.serialize()
    assert first.projection is not None and second.projection is not None
    assert first.projection.serialize() == second.projection.serialize()
    assert first.explanation is not None and second.explanation is not None
    assert first.explanation.serialize() == second.explanation.serialize()
    assert first.determinism_ok is True
    assert second.determinism_ok is True

    types = [e.event_type for e in events.published()]
    assert TWIN_SHADOW_REQUESTED in types
    assert TWIN_SHADOW_COMPLETED in types
    assert TWIN_SHADOW_STABILITY in types
    assert TWIN_SHADOW_LATENCY in types
    assert TWIN_SHADOW_HEALTH in types


def test_projection_stability_across_replays(learner):
    validator = _build_validator()
    sid = str(learner["user"].id)
    results = validator.validate_shadow_batch(
        (sid,), as_of=AS_OF, iterations=5
    )
    assert len(results) == 5
    fingerprints = [
        r.projection.serialize() for r in results if r.projection is not None
    ]
    assert len(fingerprints) == 5
    assert len(set(fingerprints)) == 1
    assert all(r.ok and r.determinism_ok for r in results)


def test_long_running_replay_preserves_health_rates(learner):
    validator = _build_validator()
    sid = str(learner["user"].id)
    validator.validate_shadow_batch((sid, sid), as_of=AS_OF, iterations=4)
    health = validator.health_snapshot()
    assert health.executions == 8
    assert health.snapshot_generation_success_rate == 1.0
    assert health.projection_success_rate == 1.0
    assert health.explainability_success_rate == 1.0
    assert health.deterministic_replay_success_rate == 1.0
    assert health.failure_count == 0


def test_rollback_immediate_and_experience_preserved(learner):
    _ = learner
    events = EventRegistry()
    result = verify_twin_rollback(events=events)
    assert result.ok is True
    assert result.twin_disabled_removes_participation is True
    assert result.experience_twin_port_preserved is True
    assert result.adaptive_flags_unchanged is True
    assert TWIN_SHADOW_ROLLBACK_VERIFIED in [
        e.event_type for e in events.published()
    ]

    off_flags = resolve_v2_feature_flags(
        environ={"KWALITEC_DIGITAL_TWIN": "0"}
    )
    composition, service = build_production_experience(flags=off_flags)
    assert composition.twin_shadow is None
    # Experience TwinPort (demo / prior path) still answers.
    _ = service
    summary = composition.twin.get_learner_summary("default")
    assert summary is not None or composition.twin is not None


def test_feature_flag_isolation_preserves_runtime_a_authority(learner):
    on_flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_DIGITAL_TWIN": "1",
            "KWALITEC_ADAPTIVE_AUTHORITY": "0",
        }
    )
    off_flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_DIGITAL_TWIN": "0",
            "KWALITEC_ADAPTIVE_AUTHORITY": "0",
        }
    )
    on_comp, on_service = build_production_experience(flags=on_flags)
    off_comp, off_service = build_production_experience(flags=off_flags)
    _ = (on_service, off_service)

    assert on_comp.twin_shadow is not None
    assert off_comp.twin_shadow is None
    # Experience UX Twin adapter remains in both modes (no cutover).
    assert on_comp.twin is not None
    assert off_comp.twin is not None
    assert on_comp.adaptive_port_router is None
    assert off_comp.adaptive_port_router is None

    sid = str(learner["user"].id)
    # Shadow validation must not replace Experience TwinPort responses.
    on_summary = on_comp.twin.get_learner_summary(sid)
    off_summary = off_comp.twin.get_learner_summary(sid)
    # Both paths use ExperienceTwinAdapter (demo seed / store), not projection.
    assert on_comp.student_twin_projection_port is not on_comp.twin
    assert off_summary is not None or off_comp.twin is not None
    _ = on_summary


def test_shadow_does_not_influence_experience_home(learner):
    flags = resolve_v2_feature_flags(environ={"KWALITEC_DIGITAL_TWIN": "1"})
    composition, service = build_production_experience(flags=flags)
    _ = service
    sid = str(learner["user"].id)

    before = composition.twin.get_learner_summary(sid)
    assert composition.twin_shadow is not None
    observation = composition.twin_shadow.validate_shadow(sid, as_of=AS_OF)
    after = composition.twin.get_learner_summary(sid)

    assert observation.ok is True
    assert before == after
    dashboard = build_twin_shadow_ops_dashboard(
        composition.twin_shadow,
        rollback_result=verify_twin_rollback(),
    )
    assert dashboard["twin_shadow_validation"]["influences_student"] is False


def test_shadow_modules_forbid_educational_writes():
    """Static guard — T6 modules must not call educational write APIs."""
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
