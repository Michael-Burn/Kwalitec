"""Integration tests — Explainability Gate (MS-003 A3).

Verifies gate validation on shadow outputs, no mutation, no Runtime A writes,
and no Experience behavioural change.
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
    ExplainabilityGate,
    empty_adaptive_output,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    EXPLAINABILITY_GATE_FAILED,
    EXPLAINABILITY_GATE_LATENCY,
    EXPLAINABILITY_GATE_PASSED,
    EXPLAINABILITY_GATE_REQUESTED,
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


def test_shadow_pipeline_with_gate_passes_complete_bundle(learner):
    events = EventRegistry()
    gate = ExplainabilityGate(events=events, enabled=True)
    orch = AdaptiveShadowOrchestrator(
        assembler=AdaptiveInputAssembler(),
        executor=AdaptiveEngineExecutor(),
        events=events,
        enabled=True,
        explainability_gate=gate,
    )
    as_of = date.today().isoformat()
    result = orch.execute_shadow(str(learner["user"].id), as_of=as_of)
    assert result.ok is True
    assert result.value is not None
    assert orch.last_gate_result is not None
    assert orch.last_gate_result.passed is True
    assert orch.last_gate_result.eligible_for_future_authority is True
    assert orch.last_gate_result.observational_only is True
    types = [e.event_type for e in events.published()]
    assert EXPLAINABILITY_GATE_REQUESTED in types
    assert EXPLAINABILITY_GATE_PASSED in types
    assert EXPLAINABILITY_GATE_LATENCY in types


def test_gate_failure_keeps_bundle_observational():
    events = EventRegistry()
    gate = ExplainabilityGate(events=events, enabled=True)
    incomplete = empty_adaptive_output()
    before = incomplete.serialize()
    result = gate.validate(incomplete, student_id="1")
    assert result.passed is False
    assert result.eligible_for_future_authority is False
    assert result.observational_only is True
    assert incomplete.serialize() == before
    types = [e.event_type for e in events.published()]
    assert EXPLAINABILITY_GATE_FAILED in types


def test_gate_does_not_mutate_runtime_a(learner):
    from app.extensions import db
    from app.models.learning import StudyAttempt
    from app.models.mission import Mission
    from app.models.topic_progress import TopicProgress

    uid = learner["user"].id
    before_missions = Mission.query.filter_by(user_id=uid).count()
    before_attempts = StudyAttempt.query.filter_by(user_id=uid).count()
    before_progress = TopicProgress.query.filter_by(user_id=uid).count()
    before_mission_status = learner["mission"].status

    events = EventRegistry()
    orch = AdaptiveShadowOrchestrator(
        assembler=AdaptiveInputAssembler(),
        executor=AdaptiveEngineExecutor(),
        events=events,
        enabled=True,
        explainability_gate=ExplainabilityGate(events=events, enabled=True),
    )
    result = orch.execute_shadow(str(uid), as_of=date.today().isoformat())
    assert result.ok is True
    db.session.expire_all()
    assert Mission.query.filter_by(user_id=uid).count() == before_missions
    assert StudyAttempt.query.filter_by(user_id=uid).count() == before_attempts
    assert TopicProgress.query.filter_by(user_id=uid).count() == before_progress
    assert (
        db.session.get(Mission, learner["mission"].id).status
        == before_mission_status
    )


def test_gate_does_not_call_recommendation_service(learner):
    uid = learner["user"].id
    with mock.patch.object(
        RecommendationService,
        "generate_recommendations",
        wraps=RecommendationService.generate_recommendations,
    ) as wrapped:
        events = EventRegistry()
        orch = AdaptiveShadowOrchestrator(
            assembler=AdaptiveInputAssembler(),
            executor=AdaptiveEngineExecutor(),
            events=events,
            enabled=True,
            explainability_gate=ExplainabilityGate(events=events, enabled=True),
        )
        result = orch.execute_shadow(str(uid), as_of=date.today().isoformat())
        assert result.ok is True
        wrapped.assert_not_called()


def test_experience_unchanged_when_gate_flags_on(learner, app, ctx):
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_ADAPTIVE_ENGINE": "1",
            "KWALITEC_ADAPTIVE_SHADOW": "1",
        }
    )
    composition, _service = build_production_experience(flags=flags)
    assert composition.explainability_gate is not None
    assert composition.adaptive_shadow is not None
    assert composition.adaptive_engine is not composition.adaptive

    shadow_result = composition.adaptive_shadow.execute_shadow(
        str(learner["user"].id),
        as_of=date.today().isoformat(),
    )
    assert shadow_result.ok is True
    assert composition.adaptive_shadow.last_gate_result is not None

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


def test_gate_modules_forbid_educational_writes():
    for name in ("gate.py", "gate_telemetry.py", "quality_rules.py"):
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
