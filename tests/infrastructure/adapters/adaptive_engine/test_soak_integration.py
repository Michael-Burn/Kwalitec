"""Integration tests — Adaptive Shadow Soak (MS-003 A6).

Verifies stable observational soak, deterministic replay, explainability /
trace completeness, rollback, Runtime A read-only, and no Experience
behavioural change.
"""

from __future__ import annotations

import ast
from datetime import date
from pathlib import Path
from unittest import mock

import pytest

import app.infrastructure.adapters.adaptive_engine as adaptive_engine_pkg
from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.adaptive_engine import (
    AdaptiveEngineExecutor,
    AdaptiveInputAssembler,
    AdaptiveShadowOrchestrator,
    ShadowSoakOrchestrator,
    build_soak_ops_dashboard,
    verify_adaptive_rollback,
)
from app.infrastructure.adapters.adaptive_engine.gate import ExplainabilityGate
from app.infrastructure.adapters.adaptive_engine.traceability import (
    FeatureFlagSnapshot,
    TraceabilityService,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    ADAPTIVE_ENGINE_SHADOW_COMPARE,
    ADAPTIVE_SOAK_COMPARE,
    ADAPTIVE_SOAK_COMPLETED,
    ADAPTIVE_SOAK_HEALTH,
    ADAPTIVE_SOAK_LATENCY,
    ADAPTIVE_SOAK_REQUESTED,
    ADAPTIVE_SOAK_ROLLBACK_VERIFIED,
)
from app.services.recommendation_service import RecommendationService
from tests.conftest import (
    _make_curriculum,
    _make_mission,
    _make_study_attempt,
    _make_study_plan,
    _make_subject,
    _make_topic_progress,
    _make_user,
)

ADAPTER_ROOT = Path(adaptive_engine_pkg.__file__).resolve().parent


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


def _build_soak(*, events: EventRegistry | None = None) -> ShadowSoakOrchestrator:
    registry = events or EventRegistry()
    assembler = AdaptiveInputAssembler()
    executor = AdaptiveEngineExecutor()
    gate = ExplainabilityGate(events=registry, enabled=True)
    traceability = TraceabilityService(
        enabled=True,
        events=registry,
        feature_flags=FeatureFlagSnapshot(
            engine_enabled=True,
            shadow_enabled=True,
            authority_enabled=False,
        ),
        engine_version=executor.EXECUTOR_VERSION,
    )
    shadow = AdaptiveShadowOrchestrator(
        assembler=assembler,
        executor=executor,
        events=registry,
        enabled=True,
        explainability_gate=gate,
        traceability=traceability,
    )
    return ShadowSoakOrchestrator(
        shadow=shadow,
        events=registry,
        enabled=True,
    )


def test_soak_pipeline_stable_from_runtime_a(learner):
    events = EventRegistry()
    soak = _build_soak(events=events)
    as_of = date.today().isoformat()
    observation = soak.execute_soak(str(learner["user"].id), as_of=as_of)
    assert observation.ok is True
    assert observation.adaptive_output is not None
    assert observation.comparison is not None
    assert observation.comparison.comparable is True
    assert observation.explainability_passed is True
    assert observation.trace_created is True
    assert observation.determinism is not None
    assert observation.determinism.success is True
    types = [e.event_type for e in events.published()]
    assert ADAPTIVE_SOAK_REQUESTED in types
    assert ADAPTIVE_SOAK_COMPLETED in types
    assert ADAPTIVE_SOAK_COMPARE in types
    assert ADAPTIVE_ENGINE_SHADOW_COMPARE in types
    assert ADAPTIVE_SOAK_LATENCY in types
    assert ADAPTIVE_SOAK_HEALTH in types
    health = soak.health_snapshot()
    assert health.executions == 1
    assert health.deterministic_replay_success_rate == 1.0
    assert health.explainability_pass_rate == 1.0
    assert health.trace_creation_rate == 1.0


def test_soak_divergence_is_measurable(learner):
    soak = _build_soak()
    observation = soak.execute_soak(
        str(learner["user"].id), as_of=date.today().isoformat()
    )
    assert observation.ok is True
    assert observation.comparison is not None
    # Agreement may or may not hold vs RecommendationService — both rates measurable.
    snap = soak.health_snapshot()
    comparable = snap.agreement_count + snap.divergence_count
    assert comparable == 1
    assert (
        snap.recommendation_agreement_rate + snap.recommendation_divergence_rate
        == 1.0
    )


def test_long_running_shadow_replay_stable(learner):
    soak = _build_soak()
    sid = str(learner["user"].id)
    as_of = date.today().isoformat()
    observations = soak.execute_soak_batch(
        (sid,),
        as_of=as_of,
        iterations=25,
        run_determinism_replay=True,
    )
    assert len(observations) == 25
    assert all(obs.ok for obs in observations)
    decision_ids = {
        obs.adaptive_output.decision_id
        for obs in observations
        if obs.adaptive_output is not None
    }
    assert len(decision_ids) == 1
    snap = soak.health_snapshot()
    assert snap.executions == 25
    assert snap.deterministic_replay_success_rate == 1.0
    assert snap.explainability_pass_rate == 1.0
    assert snap.trace_creation_rate == 1.0
    assert snap.failure_count == 0
    # Same snapshot must not thrash topic codes across the soak window.
    unexpected = [
        s
        for obs in observations
        for s in obs.drift_signals
        if s.kind == "unexpected_recommendation_change"
    ]
    assert unexpected == []


def test_soak_adaptive_path_does_not_mutate_runtime_a(learner):
    """Adaptive soak path must not write educational state.

    Baseline RecommendationService is stubbed so incidental plan-binding side
    effects of RecommendationService itself are out of scope — A6 forbids
    Adaptive Engine / soak writes, not RecommendationService read behaviour.
    """
    from app.extensions import db
    from app.models.learning import StudyAttempt
    from app.models.mission import Mission
    from app.models.topic_progress import TopicProgress

    uid = learner["user"].id
    before_missions = Mission.query.filter_by(user_id=uid).count()
    before_attempts = StudyAttempt.query.filter_by(user_id=uid).count()
    before_progress = TopicProgress.query.filter_by(user_id=uid).count()
    before_status = learner["mission"].status

    stub = mock.Mock()
    stub.generate_recommendations.return_value = [
        {"title": "Stub baseline", "topic_code": "STUB", "category": "Review"}
    ]
    soak = _build_soak()
    soak._recommendation_service = stub
    observation = soak.execute_soak(str(uid), as_of=date.today().isoformat())
    assert observation.ok is True
    db.session.expire_all()
    assert Mission.query.filter_by(user_id=uid).count() == before_missions
    assert StudyAttempt.query.filter_by(user_id=uid).count() == before_attempts
    assert TopicProgress.query.filter_by(user_id=uid).count() == before_progress
    assert db.session.get(Mission, learner["mission"].id).status == before_status
    stub.generate_recommendations.assert_called()


def test_soak_does_not_change_experience_authority(learner, app, ctx):
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_ADAPTIVE_ENGINE": "1",
            "KWALITEC_ADAPTIVE_SHADOW": "1",
        }
    )
    composition, _ = build_production_experience(flags=flags)
    assert composition.adaptive_soak is not None
    assert composition.adaptive_port_router is None

    observation = composition.adaptive_soak.execute_soak(
        str(learner["user"].id),
        as_of=date.today().isoformat(),
    )
    assert observation.ok is True

    adaptive_view = composition.adaptive.get_todays_recommendation(
        str(learner["user"].id)
    )
    if adaptive_view is not None:
        authority = str(
            (adaptive_view.get("explanation") or {}).get("authority")
            or adaptive_view.get("authority")
            or ""
        )
        assert authority != "adaptive_engine"


def test_soak_calls_recommendation_service_for_baseline_only(learner):
    """Soak may read RecommendationService for baseline; Experience unchanged."""
    uid = learner["user"].id
    with mock.patch.object(
        RecommendationService,
        "generate_recommendations",
        wraps=RecommendationService.generate_recommendations,
    ) as wrapped:
        soak = _build_soak()
        observation = soak.execute_soak(str(uid), as_of=date.today().isoformat())
        assert observation.ok is True
        wrapped.assert_called()
        assert observation.baseline is not None or wrapped.call_count >= 1


def test_rollback_verification_emits_telemetry_and_restores_authority():
    events = EventRegistry()
    result = verify_adaptive_rollback(events=events)
    assert result.ok is True
    types = [e.event_type for e in events.published()]
    assert ADAPTIVE_SOAK_ROLLBACK_VERIFIED in types
    payload = next(
        e for e in events.published() if e.event_type == ADAPTIVE_SOAK_ROLLBACK_VERIFIED
    )
    assert payload.payload["ok"] is True


def test_ops_dashboard_hook_from_composition(learner, app, ctx):
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_ADAPTIVE_ENGINE": "1",
            "KWALITEC_ADAPTIVE_SHADOW": "1",
        }
    )
    composition, _ = build_production_experience(flags=flags)
    composition.adaptive_soak.execute_soak(
        str(learner["user"].id), as_of=date.today().isoformat()
    )
    dashboard = build_soak_ops_dashboard(composition.adaptive_soak)
    assert dashboard["adaptive_shadow_soak"]["enabled"] is True
    assert dashboard["adaptive_shadow_soak"]["influences_student"] is False
    assert dashboard["adaptive_shadow_soak"]["health"]["executions"] >= 1


def test_home_recommendation_triggers_shadow_observation(learner, app, ctx):
    """Engine + Shadow ON, Authority OFF: Home read runs soak compare fail-open."""
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_ADAPTIVE_ENGINE": "1",
            "KWALITEC_ADAPTIVE_SHADOW": "1",
        }
    )
    composition, _ = build_production_experience(flags=flags)
    assert composition.adaptive_soak is not None
    assert composition.adaptive._adaptive_soak is composition.adaptive_soak
    assert composition.explainability_gate is not None
    assert composition.adaptive_port_router is None

    sid = str(learner["user"].id)
    before_health = composition.adaptive_soak.health_snapshot().executions

    served = composition.adaptive.get_todays_recommendation(sid)

    observation = composition.adaptive_soak.last_observation
    assert observation is not None
    assert observation.student_id == sid
    assert observation.comparison is not None
    # Minimum observation fields for shadow soak.
    assert "agreed" in observation.comparison.to_canonical_dict()
    assert isinstance(observation.explainability_passed, bool)
    # Served path remains Runtime A / Experience — never Adaptive authority.
    if served is not None:
        authority = str(
            (served.get("explanation") or {}).get("authority")
            or served.get("authority")
            or ""
        )
        assert authority != "adaptive_engine"
    assert composition.adaptive_soak.health_snapshot().executions == before_health + 1

    types = [e.event_type for e in composition.events.published()]
    assert ADAPTIVE_SOAK_COMPARE in types or ADAPTIVE_ENGINE_SHADOW_COMPARE in types


def test_home_shadow_observation_fail_open_never_changes_served(learner, app, ctx):
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_ADAPTIVE_ENGINE": "1",
            "KWALITEC_ADAPTIVE_SHADOW": "1",
        }
    )
    composition, _ = build_production_experience(flags=flags)
    sid = str(learner["user"].id)

    with mock.patch.object(
        composition.adaptive._adaptive_soak,
        "execute_soak",
        side_effect=RuntimeError("soak boom"),
    ):
        served = composition.adaptive.get_todays_recommendation(sid)

    # Request must succeed; served result is still a dict or None (not an error).
    assert served is None or isinstance(served, dict)


def test_default_flags_home_has_no_shadow_observation_hook():
    """Production defaults: no soak wired into AdaptiveDecisionPort."""
    flags = resolve_v2_feature_flags(environ={})
    composition, _ = build_production_experience(flags=flags)
    assert composition.adaptive_soak is None
    assert composition.adaptive._adaptive_soak is None


def test_soak_modules_forbid_educational_writes():
    """Static guard: soak compute must not write educational state."""
    for name in (
        "soak.py",
        "soak_monitors.py",
        "soak_health.py",
        "soak_telemetry.py",
        "soak_rollback.py",
    ):
        path = ADAPTER_ROOT / name
        source_lines = [
            line
            for line in path.read_text(encoding="utf-8").splitlines()
            if not line.lstrip().startswith("#")
        ]
        joined = "\n".join(source_lines)
        for token in (
            "generate_today_mission",
            "start_session",
            "complete_session",
            "accept_evidence",
            "db.session.add",
            "db.session.commit",
            "ensure_curriculum_binding",
            "repair_inconsistent_completion",
        ):
            assert token not in joined, f"{name} must not reference {token}"

        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                module = node.module or ""
                assert "planning_service" not in module
                assert "app.extensions" not in module
