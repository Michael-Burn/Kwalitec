"""SQLAlchemy UnitOfWork transaction and repository wiring tests (INF-004)."""

from __future__ import annotations

from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from application.ports.unit_of_work import UnitOfWork
from infrastructure.persistence.sqlalchemy import SqlAlchemyUnitOfWork
from infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlchemyDecisionRepository,
    SqlAlchemyDiagnosisRepository,
    SqlAlchemyDigitalTwinRepository,
    SqlAlchemyEvidenceRepository,
    SqlAlchemyHypothesisRepository,
    SqlAlchemyLearningEpisodeRepository,
    SqlAlchemyOrchestratorRepository,
    SqlAlchemyPriorityRepository,
    SqlAlchemySubjectKnowledgeRepository,
    SqlAlchemyTeachingIntentionRepository,
    SqlAlchemyTeachingPlanRepository,
    SqlAlchemyTeachingStrategyRepository,
)


def make_session() -> Mock:
    return Mock(spec=Session)


def test_implements_application_unit_of_work_interface() -> None:
    assert issubclass(SqlAlchemyUnitOfWork, UnitOfWork)
    assert not SqlAlchemyUnitOfWork.__abstractmethods__


def test_context_manager_begins_rolls_back_and_closes_session() -> None:
    session = make_session()
    uow = SqlAlchemyUnitOfWork(Mock(return_value=session))

    with uow as entered:
        assert entered is uow
        assert uow.is_active is True

    session.begin.assert_called_once_with()
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()
    assert uow.is_active is False


def test_commit_persists_without_exit_rollback() -> None:
    session = make_session()
    uow = SqlAlchemyUnitOfWork(Mock(return_value=session))

    with uow:
        uow.commit()

    session.commit.assert_called_once_with()
    session.rollback.assert_not_called()
    session.close.assert_called_once_with()


def test_explicit_rollback_is_not_repeated_on_exit() -> None:
    session = make_session()
    uow = SqlAlchemyUnitOfWork(Mock(return_value=session))

    with uow:
        uow.rollback()

    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_exception_rolls_back_closes_and_propagates() -> None:
    session = make_session()
    uow = SqlAlchemyUnitOfWork(Mock(return_value=session))

    with pytest.raises(RuntimeError, match="boom"):
        with uow:
            raise RuntimeError("boom")

    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_failed_commit_rolls_back_and_closes_session() -> None:
    session = make_session()
    session.commit.side_effect = RuntimeError("database unavailable")
    uow = SqlAlchemyUnitOfWork(Mock(return_value=session))

    with pytest.raises(RuntimeError, match="database unavailable"):
        with uow:
            uow.commit()

    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()
    assert uow.is_active is False


def test_repositories_share_the_unit_of_work_session() -> None:
    session = make_session()
    uow = SqlAlchemyUnitOfWork(Mock(return_value=session))
    expected = (
        ("digital_twins", SqlAlchemyDigitalTwinRepository),
        ("episodes", SqlAlchemyLearningEpisodeRepository),
        ("evidence", SqlAlchemyEvidenceRepository),
        ("subject_knowledge", SqlAlchemySubjectKnowledgeRepository),
        ("diagnosis", SqlAlchemyDiagnosisRepository),
        ("hypothesis", SqlAlchemyHypothesisRepository),
        ("priority", SqlAlchemyPriorityRepository),
        ("teaching_intention", SqlAlchemyTeachingIntentionRepository),
        ("teaching_strategy", SqlAlchemyTeachingStrategyRepository),
        ("decision", SqlAlchemyDecisionRepository),
        ("orchestrator", SqlAlchemyOrchestratorRepository),
        ("teaching_plan", SqlAlchemyTeachingPlanRepository),
    )

    with uow:
        for property_name, repository_type in expected:
            repository = getattr(uow, property_name)
            assert isinstance(repository, repository_type)
            assert repository._session is session


def test_each_context_owns_and_closes_a_new_session() -> None:
    first_session = make_session()
    second_session = make_session()
    session_factory = Mock(side_effect=(first_session, second_session))
    uow = SqlAlchemyUnitOfWork(session_factory)

    with uow:
        first_repository = uow.digital_twins
    with uow:
        second_repository = uow.digital_twins

    assert session_factory.call_count == 2
    first_session.close.assert_called_once_with()
    second_session.close.assert_called_once_with()
    assert first_repository is not second_repository


def test_repository_access_requires_an_open_unit() -> None:
    uow = SqlAlchemyUnitOfWork(Mock(return_value=make_session()))

    with pytest.raises(RuntimeError, match="not active"):
        _ = uow.digital_twins
