"""UnitOfWork lifecycle and protocol compliance tests (APP-002)."""

from __future__ import annotations

import pytest

from application.commands.start_learning_session import StartLearningSession
from application.errors import NotFoundError
from application.services.learning_application_service import LearningApplicationService
from tests.education_os.application.fakes import (
    FixedClock,
    InMemoryTransactionManager,
    InMemoryUnitOfWork,
    SequenceUUIDGenerator,
)
from tests.education_os.application.helpers import (
    make_clock,
    make_events,
    make_planned_episode,
    make_uow,
)


def test_unit_of_work_commit_lifecycle() -> None:
    uow = InMemoryUnitOfWork()
    with uow:
        assert uow.is_active is True
        assert uow.begin_count == 1
        uow.commit()
        assert uow.is_active is False
    assert uow.commit_count == 1
    assert uow.rollback_count == 0


def test_unit_of_work_rolls_back_uncommitted_on_exit() -> None:
    uow = InMemoryUnitOfWork()
    with uow:
        assert uow.is_active is True
    assert uow.rollback_count == 1
    assert uow.commit_count == 0
    assert uow.is_active is False


def test_unit_of_work_rolls_back_on_exception() -> None:
    uow = InMemoryUnitOfWork()
    with pytest.raises(RuntimeError, match="boom"):
        with uow:
            raise RuntimeError("boom")
    assert uow.rollback_count == 1
    assert uow.commit_count == 0


def test_unit_of_work_exposes_all_repositories() -> None:
    uow = InMemoryUnitOfWork()
    assert uow.digital_twins is not None
    assert uow.episodes is not None
    assert uow.evidence is not None
    assert uow.subject_knowledge is not None
    assert uow.diagnosis is not None
    assert uow.hypothesis is not None
    assert uow.priority is not None
    assert uow.teaching_intention is not None
    assert uow.teaching_strategy is not None
    assert uow.decision is not None
    assert uow.orchestrator is not None


def test_service_uses_unit_of_work_lifecycle() -> None:
    uow = make_uow()
    uow.episodes.save(make_planned_episode())
    service = LearningApplicationService(uow, make_events(), make_clock())

    service.start_learning_session(StartLearningSession(episode_id="episode-001"))

    assert uow.begin_count == 1
    assert uow.commit_count == 1
    assert uow.rollback_count == 0


def test_service_rolls_back_unit_of_work_on_not_found() -> None:
    uow = make_uow()
    service = LearningApplicationService(uow, make_events(), make_clock())

    with pytest.raises(NotFoundError):
        service.start_learning_session(StartLearningSession(episode_id="missing"))

    assert uow.begin_count == 1
    assert uow.commit_count == 0
    assert uow.rollback_count == 1


def test_clock_and_uuid_generator_fakes() -> None:
    clock = FixedClock()
    uuids = SequenceUUIDGenerator(prefix="gen")
    assert clock.now().year == 2026
    assert uuids.new_id() == "gen-0001"
    assert uuids.new_id() == "gen-0002"


def test_transaction_manager_lifecycle() -> None:
    tx = InMemoryTransactionManager()
    tx.begin()
    tx.commit()
    tx.begin()
    tx.rollback()
    assert tx.begun == 2
    assert tx.committed == 1
    assert tx.rolled_back == 1
