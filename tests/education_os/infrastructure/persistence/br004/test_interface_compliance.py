"""Repository interface compliance tests for BR-004 adapters."""

from __future__ import annotations

import inspect

import pytest

from application.auth.ports import AuthTokenRepository, UserAccountRepository
from application.onboarding.ports import OnboardingRepository
from infrastructure.persistence.checkpoint_repository import SqlAlchemyCheckpointRepository
from infrastructure.persistence.onboarding_repository import SqlAlchemyOnboardingRepository
from infrastructure.persistence.user_repository import (
    SqlAlchemyAuthTokenRepository,
    SqlAlchemyUserRepository,
)

ADAPTER_PORT_PAIRS = (
    (SqlAlchemyUserRepository, UserAccountRepository),
    (SqlAlchemyAuthTokenRepository, AuthTokenRepository),
    (SqlAlchemyOnboardingRepository, OnboardingRepository),
)


@pytest.mark.parametrize(
    ("adapter", "port"),
    ADAPTER_PORT_PAIRS,
    ids=[pair[0].__name__ for pair in ADAPTER_PORT_PAIRS],
)
def test_adapter_implements_port(adapter: type, port: type) -> None:
    assert issubclass(adapter, port)
    abstract_methods = getattr(port, "__abstractmethods__", frozenset())
    for name in abstract_methods:
        assert hasattr(adapter, name)
        assert not getattr(getattr(adapter, name), "__isabstractmethod__", False)


@pytest.mark.parametrize(
    ("adapter", "port"),
    ADAPTER_PORT_PAIRS,
    ids=[pair[0].__name__ for pair in ADAPTER_PORT_PAIRS],
)
def test_adapter_method_signatures_match_port(adapter: type, port: type) -> None:
    for name in getattr(port, "__abstractmethods__", frozenset()):
        port_params = list(inspect.signature(getattr(port, name)).parameters)
        adapter_params = list(inspect.signature(getattr(adapter, name)).parameters)
        assert adapter_params == port_params


def test_twin_and_evidence_adapters_implement_ports() -> None:
    from application.ports.repositories import DigitalTwinRepository, EvidenceRepository
    from infrastructure.persistence.evidence_repository import (
        SqlAlchemyEvidenceRepository,
    )
    from infrastructure.persistence.twin_repository import SqlAlchemyTwinRepository

    assert issubclass(SqlAlchemyTwinRepository, DigitalTwinRepository)
    assert issubclass(SqlAlchemyEvidenceRepository, EvidenceRepository)


def test_checkpoint_repository_exposes_store_protocol() -> None:
    required = {"load", "save", "clear"}
    assert required.issubset(set(dir(SqlAlchemyCheckpointRepository)))
