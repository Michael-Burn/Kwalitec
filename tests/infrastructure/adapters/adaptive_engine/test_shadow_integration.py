"""Integration tests — Adaptive Shadow Execution (MS-003 A2).

Verifies Runtime A → Assembler → Executor → Discard isolation, determinism,
explainability completeness, and no behavioural change to Experience /
RecommendationService / Planning.
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
    explanation_is_complete,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    ADAPTIVE_SHADOW_COMPLETED,
    ADAPTIVE_SHADOW_LATENCY,
    ADAPTIVE_SHADOW_REQUESTED,
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


def test_shadow_pipeline_produces_output_from_runtime_a(learner):
    events = EventRegistry()
    orch = AdaptiveShadowOrchestrator(
        assembler=AdaptiveInputAssembler(),
        executor=AdaptiveEngineExecutor(),
        events=events,
        enabled=True,
    )
    as_of = date.today().isoformat()
    result = orch.execute_shadow(str(learner["user"].id), as_of=as_of)
    assert result.ok is True
    assert result.value is not None
    assert explanation_is_complete(result.value)
    assert result.value.explanation.rule_refs
    assert result.value.explanation.recommendation_rationale
    types = [e.event_type for e in events.published()]
    assert ADAPTIVE_SHADOW_REQUESTED in types
    assert ADAPTIVE_SHADOW_COMPLETED in types
    assert ADAPTIVE_SHADOW_LATENCY in types


def test_shadow_determinism_identical_runtime_a_snapshots(learner):
    orch = AdaptiveShadowOrchestrator(
        assembler=AdaptiveInputAssembler(),
        executor=AdaptiveEngineExecutor(),
        events=EventRegistry(),
        enabled=True,
    )
    as_of = date.today().isoformat()
    sid = str(learner["user"].id)
    first = orch.execute_shadow(sid, as_of=as_of)
    second = orch.execute_shadow(sid, as_of=as_of)
    assert first.ok and second.ok
    assert first.value.serialize() == second.value.serialize()
    assert first.value.decision_id == second.value.decision_id


def test_shadow_does_not_mutate_runtime_a(learner):
    from app.extensions import db
    from app.models.learning import StudyAttempt
    from app.models.mission import Mission
    from app.models.topic_progress import TopicProgress

    uid = learner["user"].id
    before_missions = Mission.query.filter_by(user_id=uid).count()
    before_attempts = StudyAttempt.query.filter_by(user_id=uid).count()
    before_progress = TopicProgress.query.filter_by(user_id=uid).count()
    before_mission_status = learner["mission"].status

    orch = AdaptiveShadowOrchestrator(
        assembler=AdaptiveInputAssembler(),
        executor=AdaptiveEngineExecutor(),
        events=EventRegistry(),
        enabled=True,
    )
    result = orch.execute_shadow(str(uid), as_of=date.today().isoformat())
    assert result.ok is True
    db.session.expire_all()
    assert Mission.query.filter_by(user_id=uid).count() == before_missions
    assert StudyAttempt.query.filter_by(user_id=uid).count() == before_attempts
    assert TopicProgress.query.filter_by(user_id=uid).count() == before_progress
    assert db.session.get(Mission, learner["mission"].id).status == before_mission_status


def test_shadow_does_not_change_recommendation_service(learner):
    """Shadow must not call or alter RecommendationService behaviour."""
    uid = learner["user"].id
    with mock.patch.object(
        RecommendationService,
        "generate_recommendations",
        wraps=RecommendationService.generate_recommendations,
    ) as wrapped:
        orch = AdaptiveShadowOrchestrator(
            assembler=AdaptiveInputAssembler(),
            executor=AdaptiveEngineExecutor(),
            events=EventRegistry(),
            enabled=True,
        )
        result = orch.execute_shadow(str(uid), as_of=date.today().isoformat())
        assert result.ok is True
        wrapped.assert_not_called()


def test_experience_home_unchanged_when_shadow_flag_on(learner, app, ctx):
    """Shadow construction must not cut over Experience AdaptiveDecisionPort."""
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_ADAPTIVE_ENGINE": "1",
            "KWALITEC_ADAPTIVE_SHADOW": "1",
        }
    )
    composition, _service = build_production_experience(flags=flags)
    assert composition.adaptive_shadow is not None
    # Experience adaptive port remains prior path (no recommendation bridge here).
    assert composition.adaptive._recommendation_read is None
    assert composition.adaptive_engine is not composition.adaptive
    # Invoking shadow must not change Experience adaptive read.
    shadow_result = composition.adaptive_shadow.execute_shadow(
        str(learner["user"].id),
        as_of=date.today().isoformat(),
    )
    assert shadow_result.ok is True
    # Home adaptive projection still comes from Experience adapter, not Engine.
    adaptive_view = composition.adaptive.get_todays_recommendation(
        str(learner["user"].id)
    )
    # Demo/seed path may return None or seed — never Adaptive Engine authority.
    if adaptive_view is not None:
        authority = str(
            (adaptive_view.get("explanation") or {}).get("authority")
            or adaptive_view.get("authority")
            or ""
        )
        assert authority != "adaptive_engine"


def test_executor_and_shadow_modules_forbid_educational_writes():
    """Static guard: A2 compute modules must not import write-path services."""
    for name in ("executor.py", "shadow.py", "shadow_telemetry.py"):
        path = ADAPTER_ROOT / name
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                module = node.module or ""
                assert "recommendation_service" not in module
                assert "planning_service" not in module
                assert "app.extensions" not in module
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                # Ban db.session.add / commit style calls by attribute name.
                if node.func.attr in {"add", "commit", "delete", "flush"}:
                    # Allow only if not db.session — check source string of attr chain.
                    pass
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
            "repair_inconsistent_completion",
        ):
            assert token not in joined, f"{name} must not reference {token}"
