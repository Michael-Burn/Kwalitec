"""Pytest fixtures for APP-001/APP-002 application-layer tests."""

from __future__ import annotations

import pytest

from domain.education.digital_twin import EducationalDigitalTwin
from tests.education_os.application.fakes import (
    FixedClock,
    InMemoryEventPublisher,
    InMemoryTeachingPlanRepository,
    InMemoryUnitOfWork,
)
from tests.education_os.application.helpers import make_twin, make_uow


@pytest.fixture
def events() -> InMemoryEventPublisher:
    return InMemoryEventPublisher()


@pytest.fixture
def clock() -> FixedClock:
    return FixedClock()


@pytest.fixture
def teaching_plans() -> InMemoryTeachingPlanRepository:
    return InMemoryTeachingPlanRepository()


@pytest.fixture
def uow() -> InMemoryUnitOfWork:
    return make_uow()


@pytest.fixture
def student_id() -> str:
    return "student-ada"


@pytest.fixture
def twin(uow: InMemoryUnitOfWork, student_id: str) -> EducationalDigitalTwin:
    return make_twin(uow, student_id=student_id)
