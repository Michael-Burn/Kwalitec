"""Regression: enrolment gate must use the same effective Runtime C allowlist
as RuntimeRoutingService.resolve (dogfood cutover when enrolment is ON).

Also covers legacy mission_facts / \"Today's topic\" refusal when CS1 packages
exist on disk, and stale-shell detection for existing sittings.
"""

from __future__ import annotations

from datetime import date, timedelta
from unittest.mock import MagicMock

import pytest

from app.application.educational_packages.guard import (
    certified_guidance_enforced,
    reset_certified_guidance_cache,
)
from app.application.educational_packages.loader import reset_educational_package_cache
from app.application.educational_runtime_engine import RuntimeAuthority
from app.application.educational_runtime_engine.service import (
    EducationalRuntimeEngineService,
)
from app.application.learning_session.substance_planner import (
    EducationalSubstancePlanner,
)
from app.application.platform_integration.enrolment_bridge import (
    FounderStudentEnrolmentBridge,
)
from app.application.platform_integration.flags import (
    effective_runtime_c_allowlist,
    resolve_founder_student_bridge_flags,
)
from app.application.platform_integration.routing import RuntimeRoutingService
from app.application.student_runtime import (
    SessionSpineUnavailable,
    StudentRuntimeCoordinator,
)
from app.infrastructure.adapters.learning_session.package_activity_engine import (
    PackageActivityEngine,
)
from app.infrastructure.adapters.learning_session.persistence import (
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.session.activity_adapter import SessionActivityAdapter
from app.infrastructure.session.store import SessionDocumentStore
from app.models.educational_runtime_engine import RuntimeEnrolment
from tests.application.platform_integration.helpers import (
    bridge_flags,
    make_user,
    publish_subject,
)


def setup_function() -> None:
    reset_educational_package_cache()
    reset_certified_guidance_cache()


def test_should_use_bridge_agrees_with_resolve_for_cs1_local_flags(ctx, monkeypatch):
    """Local posture: enrolment ON, empty static allowlist → CS1 on effective list."""
    monkeypatch.setenv("KWALITEC_RUNTIME_C_ENROLMENT", "1")
    monkeypatch.delenv("KWALITEC_RUNTIME_C_SUBJECT_ALLOWLIST", raising=False)
    monkeypatch.delenv("KWALITEC_FOUNDER_STUDENT_BRIDGE", raising=False)
    monkeypatch.delenv("KWALITEC_PUBLISHED_SUBJECT_DISCOVERY", raising=False)

    publish_subject("CS1", title="Actuarial Statistics", version_label="2026.1")
    flags = resolve_founder_student_bridge_flags()
    assert flags.ENABLE_RUNTIME_C_ENROLMENT is True
    assert flags.RUNTIME_C_SUBJECT_ALLOWLIST == frozenset()
    assert "CS1" in effective_runtime_c_allowlist(flags)

    bridge = FounderStudentEnrolmentBridge(flags=flags)
    router = RuntimeRoutingService(flags=flags)
    decision = router.resolve(subject_code="CS1", category_code="IFoA")

    assert bridge.should_use_bridge(category_code="IFoA", subject_code="CS1") is True
    assert decision.runtime_authority == RuntimeAuthority.PUBLISHED_CURRICULUM
    assert decision.reason == "dogfood_curriculum_cutover"
    assert decision.curriculum_identity == "CS1:2026.1"


def test_legacy_catalogue_cs1_enrolment_starts_real_runtime_c_session(
    ctx, monkeypatch
):
    """Genuine e2e: IFoA catalogue CS1 enrolment → Runtime C session with package."""
    monkeypatch.setenv("SR_SESSION_PRIMARY", "1")
    monkeypatch.setenv("SR_SESSION_SUBSTANCE", "1")

    flags = bridge_flags(enrolment=True, allowlist=frozenset())
    publish_subject("CS1", title="Actuarial Statistics", version_label="2026.1")
    user = make_user("runtime-c-gate@example.com")

    bridge = FounderStudentEnrolmentBridge(flags=flags)
    assert bridge.should_use_bridge(category_code="IFoA", subject_code="CS1") is True

    result = bridge.enrol(
        user_id=user.id,
        category_code="IFoA",
        subject_code="CS1",
        exam_date=date.today() + timedelta(days=120),
    )
    assert result.runtime_authority == RuntimeAuthority.PUBLISHED_CURRICULUM
    assert result.enrolment_id
    assert result.curriculum_identity == "CS1:2026.1"
    assert (
        RuntimeEnrolment.query.filter_by(user_id=user.id, subject_code="CS1").count()
        == 1
    )

    runtime = EducationalRuntimeEngineService()
    mission = runtime.generate_daily_mission(
        user_id=user.id,
        subject_code="CS1",
        mission_date=date(2026, 9, 10),
    )
    assert mission.status == "generated"
    assert (mission.topic_code or "").strip()
    assert (mission.educational_package_id or "").strip()
    assert (mission.title or "").strip().lower() not in {
        "today's topic",
        "core methods",
    }

    store = SessionDocumentStore()
    coordinator = StudentRuntimeCoordinator(
        persistence=LearningSessionPersistenceAdapter(store=store),
        flags=__import__(
            "app.application.config.v2_flags", fromlist=["resolve_v2_feature_flags"]
        ).resolve_v2_feature_flags(
            environ={"SR_SESSION_PRIMARY": "1", "SR_SESSION_SUBSTANCE": "1"}
        ),
    )
    binding = coordinator.accept_and_start_session(
        user_id=user.id,
        mission_instance_id=mission.mission_instance_id,
        topic_title=mission.title,
    )
    assert binding.session_id
    loaded = LearningSessionPersistenceAdapter(store=store).load(
        session_id=binding.session_id
    )
    assert loaded is not None
    assert (loaded.get("educational_package_id") or "").strip()
    assert (loaded.get("topic_id") or "").strip()
    topic = (loaded.get("topic_title") or binding.topic_title or "").strip().lower()
    assert topic not in {"", "today's topic", "core methods"}
    assert (loaded.get("curriculum_identity") or "").startswith("CS1:")


def test_mission_facts_placeholder_refused_when_cs1_packages_exist():
    """Legacy empty-identity path must not invent Today's topic when CS1 is live."""
    assert certified_guidance_enforced("CS1")

    planner = EducationalSubstancePlanner()
    substance = planner.plan_for_topic(
        curriculum_identity="",
        topic_id="",
        topic_title="Today's topic",
    )
    assert substance is None

    direct = planner._plan_from_mission_facts(
        curriculum_identity="",
        topic_id="orphan",
        topic_title="Today's topic",
        task_descriptions=(),
        educational_rationale="",
        objective_ids=(),
    )
    assert direct is None


def test_package_activity_engine_and_adapter_refuse_mission_facts_shell(ctx):
    """PackageActivityEngine + ActivityAdapter: honest None, not default shell."""
    assert certified_guidance_enforced("CS1")

    store = SessionDocumentStore()
    persistence = LearningSessionPersistenceAdapter(store=store)
    session_id = "sess-refuse-shell"
    student_id = "99"
    persistence.store.save(
        "runtime.overview",
        f"{student_id}::{session_id}",
        {
            "student_id": student_id,
            "session_id": session_id,
            "topic_title": "Today's topic",
            "curriculum_identity": "",
            "topic_id": "",
            "status": "in_progress",
        },
    )
    # Also persist a binding-shaped record the engine loads.
    persistence.save_binding = MagicMock()  # type: ignore[method-assign]
    persistence.load = MagicMock(  # type: ignore[method-assign]
        return_value={
            "student_id": student_id,
            "session_id": session_id,
            "topic_title": "Today's topic",
            "curriculum_identity": "",
            "topic_id": "",
            "estimated_minutes": 30,
        }
    )

    engine = PackageActivityEngine(store=store, persistence=persistence)
    seq = engine._ensure_sequence(
        student_id, session_id=session_id, topic_title="Today's topic"
    )
    assert seq is None
    opaque = engine.get_current_activity_opaque(
        student_id, session_id=session_id, topic_title="Today's topic"
    )
    assert opaque is None

    adapter = SessionActivityAdapter(
        store=store, activity_engine=engine, auto_provision=True
    )
    activity = adapter.get_current_activity(student_id, session_id=session_id)
    assert activity is None
    # Must not have provisioned a default "Today's topic" method-steps sequence.
    fallback = store.get("activity.sequence", f"{student_id}::{session_id}")
    assert fallback is None or not fallback.get("activities")


def test_todays_topic_stale_shell_is_detected_as_placeholder(ctx):
    store = SessionDocumentStore()
    persistence = LearningSessionPersistenceAdapter(store=store)
    student_id = "4"
    session_id = "sess-stale-today"
    store.save(
        "runtime.overview",
        f"{student_id}::{session_id}",
        {
            "student_id": student_id,
            "session_id": session_id,
            "topics": ["Today's topic"],
            "topic_title": "Today's topic",
            "status": "in_progress",
        },
    )
    persistence.load = MagicMock(  # type: ignore[method-assign]
        return_value={
            "student_id": student_id,
            "session_id": session_id,
            "topic_title": "Today's topic",
            "status": "in_progress",
        }
    )
    coordinator = StudentRuntimeCoordinator(
        persistence=persistence,
        flags=__import__(
            "app.application.config.v2_flags", fromlist=["resolve_v2_feature_flags"]
        ).resolve_v2_feature_flags(environ={"SR_SESSION_PRIMARY": "1"}),
    )
    assert (
        coordinator._open_session_is_placeholder(
            student_id=student_id, session_id=session_id
        )
        is True
    )


def test_coordinator_refuses_todays_topic_substance(ctx, monkeypatch):
    monkeypatch.setenv("SR_SESSION_PRIMARY", "1")
    monkeypatch.setenv("SR_SESSION_SUBSTANCE", "1")
    publish_subject("CS1", title="Actuarial Statistics", version_label="2026.1")
    user = make_user("refuse-today@example.com")
    bridge = FounderStudentEnrolmentBridge(flags=bridge_flags())
    bridge.enrol(
        user_id=user.id,
        category_code="IFoA",
        subject_code="CS1",
        exam_date=date.today() + timedelta(days=90),
    )
    runtime = EducationalRuntimeEngineService()
    mission = runtime.generate_daily_mission(
        user_id=user.id,
        subject_code="CS1",
        mission_date=date(2026, 9, 11),
    )

    store = SessionDocumentStore()
    coordinator = StudentRuntimeCoordinator(
        persistence=LearningSessionPersistenceAdapter(store=store),
        flags=__import__(
            "app.application.config.v2_flags", fromlist=["resolve_v2_feature_flags"]
        ).resolve_v2_feature_flags(
            environ={"SR_SESSION_PRIMARY": "1", "SR_SESSION_SUBSTANCE": "1"}
        ),
    )

    fake = MagicMock()
    fake.source = "mission_facts"
    fake.topic_title = "Today's topic"
    fake.learning_objectives = ()
    coordinator._plan_substance = MagicMock(return_value=fake)  # type: ignore[method-assign]

    with pytest.raises(
        SessionSpineUnavailable,
        match=r"placeholder|certified CMP guidance|fallback substance refused",
    ):
        coordinator.accept_and_start_session(
            user_id=user.id,
            mission_instance_id=mission.mission_instance_id,
            topic_title="Today's topic",
        )
