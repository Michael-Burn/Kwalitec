"""EducationPlatform public API tests."""

from __future__ import annotations

import pytest

from app.application.education_platform.dto.education_request import EducationRequest
from app.application.education_platform.platform import EducationPlatform
from tests.application.education_platform.helpers import (
    FakeCurriculum,
    FakeMission,
    make_full_ports,
    make_platform,
    make_request,
)


def test_platform_version_constant():
    assert EducationPlatform.PLATFORM_VERSION == "education-platform-1"


def test_generate_subject():
    platform = make_platform()
    resp = platform.generate_subject(make_request())
    assert resp.success
    assert resp.workflow == "generate_subject"
    assert resp.subject_plan is not None


def test_generate_journey():
    platform = make_platform()
    resp = platform.generate_journey(make_request())
    assert resp.success
    assert resp.journey_id
    assert resp.blueprint_id


def test_generate_learning_sessions():
    platform = make_platform()
    resp = platform.generate_learning_sessions(make_request())
    assert resp.success
    assert resp.sessions


def test_generate_learning_activities():
    platform = make_platform()
    resp = platform.generate_learning_activities(make_request())
    assert resp.success
    assert resp.activity_ids


def test_generate_daily_missions():
    platform = make_platform()
    resp = platform.generate_daily_missions(make_request())
    assert resp.success
    assert resp.missions
    assert resp.missions[0].learner_id == "learner-1"


def test_build_platform_snapshot():
    platform = make_platform()
    resp = platform.build_platform_snapshot(make_request())
    assert resp.success
    assert resp.snapshot is not None
    assert resp.snapshot.platform_version == EducationPlatform.PLATFORM_VERSION


def test_validate_platform():
    platform = make_platform()
    resp = platform.validate_platform()
    assert resp.success
    assert resp.validation_passed is True


def test_validate_platform_with_request():
    platform = make_platform()
    resp = platform.validate_platform(make_request(learner_id="l2"))
    assert resp.request_correlation_id == "corr-1"


def test_validate_incomplete_platform():
    platform = make_platform(omit={"mission", "activity"})
    resp = platform.validate_platform()
    assert resp.validation_passed is False


def test_workflow_overrides_request_workflow_field():
    """Facade methods force the correct workflow name."""
    platform = make_platform()
    req = EducationRequest(workflow="validate_platform", learner_id="l1")
    resp = platform.generate_subject(req)
    assert resp.workflow == "generate_subject"


def test_incomplete_workflow_returns_failed_response():
    platform = EducationPlatform.create(curriculum=FakeCurriculum())
    resp = platform.generate_daily_missions(make_request())
    assert resp.success is False
    assert resp.error


def test_health_status_shape():
    platform = make_platform()
    health = platform.health_status()
    assert health["platform_version"] == EducationPlatform.PLATFORM_VERSION
    assert health["platform_status"] == "healthy"
    assert "components" in health
    assert "workflow_readiness" in health


def test_diagnostics_report():
    platform = make_platform()
    platform.generate_subject(make_request())
    report = platform.diagnostics()
    assert report.platform_version == EducationPlatform.PLATFORM_VERSION
    assert report.validation_passed
    assert "generate_subject" in report.workflow_timings


def test_replace_port():
    platform = make_platform()
    new_mission = FakeMission(mission_type="revision")
    prev = platform.replace_port("mission", new_mission)
    assert prev is not None
    resp = platform.generate_daily_missions(make_request())
    assert resp.missions[0].mission_type == "revision"


def test_registry_property():
    platform = make_platform()
    assert len(platform.registry) == 6


def test_correlation_id_propagates():
    platform = make_platform()
    resp = platform.generate_subject(
        make_request(correlation_id="xyz-99")
    )
    assert resp.request_correlation_id == "xyz-99"


def test_deterministic_repeat():
    platform = make_platform()
    a = platform.generate_daily_missions(make_request())
    b = platform.generate_daily_missions(make_request())
    assert a.journey_id == b.journey_id
    assert a.missions[0].mission_id == b.missions[0].mission_id
    assert a.subject_plan.topic_ids == b.subject_plan.topic_ids


@pytest.mark.parametrize(
    "method",
    [
        "generate_subject",
        "generate_journey",
        "generate_learning_sessions",
        "generate_learning_activities",
        "generate_daily_missions",
        "build_platform_snapshot",
    ],
)
def test_all_generation_methods_succeed(method):
    platform = make_platform()
    resp = getattr(platform, method)(make_request())
    assert resp.success is True


def test_create_require_complete():
    with pytest.raises(Exception):
        EducationPlatform.create(require_complete=True)


def test_create_require_complete_full():
    platform = EducationPlatform.create(
        require_complete=True, **make_full_ports()
    )
    assert platform.validate_platform().validation_passed
