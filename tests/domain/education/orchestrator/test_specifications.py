"""Specification tests for Educational Orchestrator."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.orchestrator import (
    OrchestrationIsValidSpecification,
    StageIsExecutableSpecification,
)
from tests.domain.education.orchestrator.conftest import (
    make_orchestrator,
    make_started_orchestrator,
)


def test_valid_specification_on_create() -> None:
    orch = make_orchestrator()
    OrchestrationIsValidSpecification().assert_satisfied_by(orch)


def test_stage_executable_assert() -> None:
    orch = make_started_orchestrator()
    StageIsExecutableSpecification().assert_satisfied_by(orch)


def test_stage_executable_assert_fails_when_planned() -> None:
    orch = make_orchestrator()
    with pytest.raises(EducationalInvariantViolation):
        StageIsExecutableSpecification().assert_satisfied_by(orch)
