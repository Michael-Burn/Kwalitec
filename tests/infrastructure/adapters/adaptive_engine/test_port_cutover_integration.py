"""Integration tests — Adaptive Experience Port Cutover (MS-003 A4).

Verifies eligible PASS routing, FAIL fallback, RecommendationService stability,
Runtime A read-only behaviour, and Experience stability when Authority is OFF.
"""

from __future__ import annotations

import ast
from pathlib import Path
from unittest import mock

import pytest

import app.infrastructure.adapters.adaptive_engine as adaptive_engine_pkg
from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.adaptive_engine import (
    AUTHORITY_ADAPTIVE_ENGINE,
    AdaptiveEngineExecutor,
    AdaptiveExperiencePortRouter,
    AdaptiveInputAssembler,
    ExplainabilityGate,
    empty_adaptive_output,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    ADAPTIVE_ENGINE_FALLBACK,
    ADAPTIVE_ENGINE_REQUESTED,
    ADAPTIVE_ENGINE_SUCCESS,
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


def _cutover_flags(**extra: str) -> dict[str, str]:
    env = {
        "KWALITEC_ADAPTIVE_ENGINE": "1",
        "KWALITEC_ADAPTIVE_SHADOW": "1",
        "KWALITEC_ADAPTIVE_AUTHORITY": "1",
        "KWALITEC_RECOMMENDATION_BRIDGE": "1",
    }
    env.update(extra)
    return env


def test_pass_bundle_routed_through_experience_port(learner):
    flags = resolve_v2_feature_flags(environ=_cutover_flags())
    composition, _ = build_production_experience(flags=flags)
    assert composition.adaptive_port_router is not None

    sid = str(learner["user"].id)
    result = composition.adaptive.get_todays_recommendation(sid)
    assert result is not None
    assert result["authority"] == AUTHORITY_ADAPTIVE_ENGINE
    assert result["next_action_authority"] is True
    assert result["fallback_used"] is False
    assert result.get("decision_id")
    assert result.get("recommendation_label") or result.get("title")

    types = [e.event_type for e in composition.events.published()]
    assert ADAPTIVE_ENGINE_REQUESTED in types
    assert ADAPTIVE_ENGINE_SUCCESS in types


def test_fail_bundle_falls_back_to_recommendation_service(learner):
    flags = resolve_v2_feature_flags(environ=_cutover_flags())
    composition, _ = build_production_experience(flags=flags)
    router = composition.adaptive_port_router
    assert router is not None

    sid = str(learner["user"].id)
    with mock.patch.object(
        router._gate,
        "validate",
        return_value=ExplainabilityGate(events=EventRegistry()).validate(
            empty_adaptive_output(), student_id=sid
        ),
    ):
        result = composition.adaptive.get_todays_recommendation(sid)

    assert router.last_fallback_reason == "explainability_ineligible"
    # Fallback may be None (no rec) or Recommendation Bridge projection —
    # never adaptive_engine authority.
    if result is not None:
        assert result.get("authority") != AUTHORITY_ADAPTIVE_ENGINE

    types = [e.event_type for e in composition.events.published()]
    assert ADAPTIVE_ENGINE_FALLBACK in types


def test_recommendation_service_remains_functional_without_authority(learner):
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_ADAPTIVE_ENGINE": "1",
            "KWALITEC_ADAPTIVE_SHADOW": "1",
            "KWALITEC_RECOMMENDATION_BRIDGE": "1",
        }
    )
    composition, _ = build_production_experience(flags=flags)
    assert composition.adaptive_port_router is None
    assert composition.explainability_gate is not None

    sid = str(learner["user"].id)
    result = composition.adaptive.get_todays_recommendation(sid)
    if result is not None:
        assert result.get("authority") != AUTHORITY_ADAPTIVE_ENGINE


def test_runtime_a_unchanged_under_cutover(learner):
    from app.extensions import db
    from app.models.learning import StudyAttempt
    from app.models.mission import Mission
    from app.models.topic_progress import TopicProgress

    uid = learner["user"].id
    before_missions = Mission.query.filter_by(user_id=uid).count()
    before_attempts = StudyAttempt.query.filter_by(user_id=uid).count()
    before_progress = TopicProgress.query.filter_by(user_id=uid).count()
    before_mission_status = learner["mission"].status

    flags = resolve_v2_feature_flags(environ=_cutover_flags())
    composition, _ = build_production_experience(flags=flags)
    result = composition.adaptive.get_todays_recommendation(str(uid))
    assert result is not None

    db.session.expire_all()
    assert Mission.query.filter_by(user_id=uid).count() == before_missions
    assert StudyAttempt.query.filter_by(user_id=uid).count() == before_attempts
    assert TopicProgress.query.filter_by(user_id=uid).count() == before_progress
    assert (
        db.session.get(Mission, learner["mission"].id).status
        == before_mission_status
    )


def test_experience_stable_when_engine_shadow_without_authority(learner):
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_ADAPTIVE_ENGINE": "1",
            "KWALITEC_ADAPTIVE_SHADOW": "1",
        }
    )
    composition, _ = build_production_experience(flags=flags)
    assert composition.adaptive_port_router is None
    adaptive_view = composition.adaptive.get_todays_recommendation(
        str(learner["user"].id)
    )
    if adaptive_view is not None:
        authority = str(
            (adaptive_view.get("explanation") or {}).get("authority")
            or adaptive_view.get("authority")
            or ""
        )
        assert authority != AUTHORITY_ADAPTIVE_ENGINE


def test_router_pipeline_isolation_from_recommendation_service(learner):
    uid = str(learner["user"].id)
    events = EventRegistry()
    from app.infrastructure.adapters.adaptive_engine import AdaptiveEngineAdapter

    router = AdaptiveExperiencePortRouter(
        assembler=AdaptiveInputAssembler(),
        engine=AdaptiveEngineAdapter(
            input_assembler=AdaptiveInputAssembler(),
            executor=AdaptiveEngineExecutor(),
        ),
        gate=ExplainabilityGate(events=events, enabled=True),
        events=events,
        cutover_active=True,
    )
    with mock.patch.object(
        RecommendationService,
        "generate_recommendations",
        wraps=RecommendationService.generate_recommendations,
    ) as wrapped:
        projected = router.try_adaptive_recommendation(uid)
        assert projected is not None
        wrapped.assert_not_called()


def test_port_cutover_modules_forbid_educational_writes():
    for name in ("port_cutover.py", "port_cutover_telemetry.py"):
        path = ADAPTER_ROOT / name
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                module = node.module or ""
                assert "recommendation_service" not in module
                assert "planning_service" not in module
                assert "app.extensions" not in module
        source_lines = [
            line
            for line in path.read_text(encoding="utf-8").splitlines()
            if not line.lstrip().startswith("#")
            and '"""' not in line
            and "'''" not in line
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
        ):
            assert token not in joined


def test_default_flags_preserve_recommendation_authority(learner):
    flags = resolve_v2_feature_flags(environ={})
    composition, _ = build_production_experience(flags=flags)
    assert composition.adaptive_port_router is None
    assert flags.ENABLE_ADAPTIVE_AUTHORITY is False
    # Smoke: Experience adaptive port still callable.
    composition.adaptive.get_todays_recommendation(str(learner["user"].id))
