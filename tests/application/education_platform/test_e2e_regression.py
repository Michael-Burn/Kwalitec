"""End-to-end orchestration and regression tests."""

from __future__ import annotations

import pytest

from app.application.education_platform.platform import EducationPlatform
from app.application.education_platform.policies.orchestration_policy import (
    ALL_WORKFLOWS,
    DEPENDENCY_CHAIN,
)
from tests.application.education_platform.helpers import (
    FakeActivity,
    FakeBlueprint,
    FakeCurriculum,
    FakeJourney,
    FakeMission,
    FakeSession,
    make_platform,
    make_request,
)


def test_e2e_full_chain_mission_generation():
    log: list[str] = []
    platform = EducationPlatform.create(
        curriculum=FakeCurriculum(call_log=log),
        blueprint=FakeBlueprint(call_log=log, session_count=2),
        journey=FakeJourney(call_log=log),
        session=FakeSession(call_log=log),
        activity=FakeActivity(call_log=log),
        mission=FakeMission(call_log=log),
    )
    resp = platform.generate_daily_missions(
        make_request(
            learner_id="learner-42",
            curriculum_id="curr-cs1",
            subject_id="cs1",
            topic_id="topic-a",
        )
    )
    assert resp.success
    assert resp.subject_plan.curriculum_id == "curr-cs1"
    assert resp.journey_id
    assert len(resp.sessions) == 2
    assert resp.activity_ids
    assert resp.missions[0].learner_id == "learner-42"
    assert resp.workflow_result.steps == DEPENDENCY_CHAIN


def test_e2e_snapshot_includes_all_artefacts():
    platform = make_platform()
    resp = platform.build_platform_snapshot(make_request())
    snap = resp.snapshot
    assert snap.subject_plan is not None
    assert snap.journey_id is not None
    assert snap.sessions
    assert snap.missions
    assert snap.registered_ports == DEPENDENCY_CHAIN
    assert snap.missing_ports == ()


def test_e2e_validate_then_generate():
    platform = make_platform()
    v = platform.validate_platform()
    assert v.validation_passed
    m = platform.generate_daily_missions(make_request())
    assert m.success


def test_e2e_partial_composition_subject_only():
    platform = EducationPlatform.create(curriculum=FakeCurriculum())
    assert platform.generate_subject(make_request()).success
    assert not platform.generate_journey(make_request()).success


def test_e2e_health_then_diagnostics_consistency():
    platform = make_platform()
    health = platform.health_status()
    report = platform.diagnostics()
    assert health["registered_components"] == report.registered_engines
    assert health["missing_dependencies"] == report.missing_ports


@pytest.mark.parametrize("workflow", sorted(ALL_WORKFLOWS))
def test_e2e_every_workflow_runs_on_full_platform(workflow):
    platform = make_platform()
    req = make_request(workflow=workflow)
    if workflow == "generate_subject":
        resp = platform.generate_subject(req)
    elif workflow == "generate_journey":
        resp = platform.generate_journey(req)
    elif workflow == "generate_learning_sessions":
        resp = platform.generate_learning_sessions(req)
    elif workflow == "generate_learning_activities":
        resp = platform.generate_learning_activities(req)
    elif workflow == "generate_daily_missions":
        resp = platform.generate_daily_missions(req)
    elif workflow == "build_platform_snapshot":
        resp = platform.build_platform_snapshot(req)
    else:
        resp = platform.validate_platform(req)
    assert resp.success is True
    assert resp.workflow == workflow


def test_e2e_same_inputs_same_outputs():
    platform = make_platform()
    req = make_request()
    results = [
        platform.generate_daily_missions(req) for _ in range(5)
    ]
    ids = [(r.journey_id, r.missions[0].mission_id, r.sessions[0].session_id)
           for r in results]
    assert len(set(ids)) == 1


def test_regression_existing_engines_still_import():
    from app.application.instructional_blueprint.engine import (
        InstructionalBlueprintEngine,
    )
    from app.application.learning_activity.engine import LearningActivityEngine
    from app.application.learning_journey.engine import LearningJourneyEngine
    from app.application.learning_session.runtime import LearningSessionRuntime
    from app.application.mission_adapter.adapter import MissionAdapter
    from app.application.mission_engine_v2.engine import MissionEngineV2

    assert InstructionalBlueprintEngine is not None
    assert LearningJourneyEngine is not None
    assert LearningSessionRuntime is not None
    assert LearningActivityEngine is not None
    assert MissionEngineV2 is not None
    assert MissionAdapter.create() is not None


def test_regression_mission_adapter_untouched_health():
    from app.application.mission_adapter.adapter import MissionAdapter

    adapter = MissionAdapter.create()
    status = adapter.health_status()
    assert "invocations" in status


def test_regression_curriculum_domain_untouched():
    from app.domain.curriculum.graph.curriculum_graph import CurriculumGraph

    assert CurriculumGraph is not None


def test_regression_no_persistence_side_effects():
    """Composition layer must not import ORM/extensions."""
    import app.application.education_platform.platform as mod

    assert not hasattr(mod, "db")


@pytest.mark.parametrize(
    "omit,allowed,blocked",
    [
        (
            {"mission"},
            "generate_learning_activities",
            "generate_daily_missions",
        ),
        (
            {"activity", "mission"},
            "generate_learning_sessions",
            "generate_learning_activities",
        ),
        (
            {"session", "activity", "mission"},
            "generate_journey",
            "generate_learning_sessions",
        ),
        (
            {"blueprint", "journey", "session", "activity", "mission"},
            "generate_subject",
            "generate_journey",
        ),
    ],
)
def test_e2e_graceful_degradation(omit, allowed, blocked):
    platform = make_platform(omit=omit)
    assert getattr(platform, allowed)(make_request()).success
    assert not getattr(platform, blocked)(make_request()).success


def test_e2e_custom_ports_end_to_end():
    platform = EducationPlatform.create(
        curriculum=FakeCurriculum(
            subject_id="math",
            topic_ids=("algebra", "calculus"),
        ),
        blueprint=FakeBlueprint(blueprint_id="bp-deep", session_count=1),
        journey=FakeJourney(journey_id="j-math"),
        session=FakeSession(topic_id="algebra"),
        activity=FakeActivity(activity_ids=("read", "practice")),
        mission=FakeMission(mission_type="today"),
    )
    resp = platform.generate_daily_missions(
        make_request(subject_id="math", topic_id="algebra")
    )
    assert resp.success
    assert resp.subject_plan.topic_ids == ("algebra", "calculus")
    assert resp.blueprint_id == "bp-deep"
    assert resp.journey_id == "j-math"
    assert len(resp.activity_ids) == 2


def test_package_dir_exports():
    import app.application.education_platform as pkg

    names = dir(pkg)
    assert "EducationPlatform" in names
    assert "CompositionRoot" in names
