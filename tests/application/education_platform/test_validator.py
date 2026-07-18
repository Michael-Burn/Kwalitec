"""PlatformValidator tests."""

from __future__ import annotations

import pytest

from app.application.education_platform.composition_root import CompositionRoot
from app.application.education_platform.exceptions import ValidationError
from app.application.education_platform.platform_validator import (
    PlatformValidationResult,
    PlatformValidator,
)
from app.application.education_platform.policies.orchestration_policy import (
    DEPENDENCY_CHAIN,
    WORKFLOW_GENERATE_SUBJECT,
)
from tests.application.education_platform.helpers import (
    FakeCurriculum,
    FakeSession,
    make_full_ports,
)


def test_validate_complete_passes():
    reg = CompositionRoot.build_registry(**make_full_ports())
    result = PlatformValidator().validate(reg)
    assert result.passed is True
    assert result.issues == ()
    assert result.missing_ports == ()


def test_validate_incomplete_fails():
    reg = CompositionRoot.build_registry(curriculum=FakeCurriculum())
    result = PlatformValidator().validate(reg)
    assert result.passed is False
    assert result.missing_ports


def test_validation_result_frozen():
    from dataclasses import FrozenInstanceError

    reg = CompositionRoot.build_registry(**make_full_ports())
    result = PlatformValidator().validate(reg)
    with pytest.raises(FrozenInstanceError):
        result.passed = False  # type: ignore[misc]


def test_validation_result_readiness_proxy():
    from types import MappingProxyType

    reg = CompositionRoot.build_registry(**make_full_ports())
    result = PlatformValidator().validate(reg)
    assert isinstance(result.workflow_readiness, MappingProxyType)
    assert result.workflow_readiness["generate_subject"] is True


def test_require_valid_ok():
    reg = CompositionRoot.build_registry(**make_full_ports())
    result = PlatformValidator().require_valid(reg)
    assert isinstance(result, PlatformValidationResult)
    assert result.passed


def test_require_valid_raises():
    reg = CompositionRoot.build_registry()
    with pytest.raises(ValidationError):
        PlatformValidator().require_valid(reg)


def test_require_workflow_ok():
    reg = CompositionRoot.build_registry(curriculum=FakeCurriculum())
    PlatformValidator().require_workflow(reg, WORKFLOW_GENERATE_SUBJECT)


def test_require_workflow_missing_port():
    reg = CompositionRoot.build_registry()
    with pytest.raises(ValidationError):
        PlatformValidator().require_workflow(reg, WORKFLOW_GENERATE_SUBJECT)


def test_require_workflow_unavailable_port():
    curr = FakeCurriculum(available=False)
    reg = CompositionRoot.build_registry(curriculum=curr)
    with pytest.raises(ValidationError, match="unavailable"):
        PlatformValidator().require_workflow(reg, WORKFLOW_GENERATE_SUBJECT)


def test_validate_detects_unavailable():
    ports = make_full_ports()
    ports["session"] = FakeSession(available=False)
    reg = CompositionRoot.build_registry(**ports)
    result = PlatformValidator().validate(reg)
    assert result.passed is False
    assert "port_unavailable:session" in result.issues


def test_validate_workflow_readiness_partial():
    reg = CompositionRoot.build_registry(curriculum=FakeCurriculum())
    result = PlatformValidator().validate(reg)
    assert result.workflow_readiness["generate_subject"] is True
    assert result.workflow_readiness["generate_daily_missions"] is False
    assert result.workflow_readiness["validate_platform"] is True


def test_registered_ports_on_result():
    reg = CompositionRoot.build_registry(
        curriculum=FakeCurriculum(),
        session=FakeSession(),
    )
    result = PlatformValidator().validate(reg)
    assert result.registered_ports == ("curriculum", "session")


@pytest.mark.parametrize("name", list(DEPENDENCY_CHAIN))
def test_missing_each_port_fails_full_validation(name):
    ports = make_full_ports()
    ports[name] = None
    reg = CompositionRoot.build_registry(**ports)
    result = PlatformValidator().validate(reg)
    assert result.passed is False
    assert f"missing_port:{name}" in result.issues
