"""BR-004.5 — production composition root integration tests.

Proves Authentication, Onboarding, Student Initialization, Checkpoints,
Evidence, Student Twin, and UnitOfWork are wired through
``SqlAlchemyProductUnitOfWork`` with no in-memory or recording repositories.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from application.auth.requests import RegisterRequest
from application.composition import assemble
from application.onboarding.requests import StartOnboardingRequest
from domain.auth.email_address import EmailAddress
from domain.onboarding.ids import OnboardingId
from infrastructure.composition.product_factories import (
    ProductServices,
    TransactionalAuthenticationService,
    TransactionalEvidenceUpdateService,
    TransactionalOnboardingService,
    TransactionalStudentInitializationService,
    build_product_services,
)
from infrastructure.persistence.product_checkpoint_store import ProductCheckpointStore
from infrastructure.persistence.sqlalchemy.base import metadata
from infrastructure.persistence.sqlalchemy.models import (  # noqa: F401 — register tables
    AuthTokenModel,
    DigitalTwinModel,
    EvidenceModel,
    OnboardingSessionModel,
    SessionCheckpointModel,
    UserAccountModel,
)
from infrastructure.persistence.sqlalchemy_uow import SqlAlchemyProductUnitOfWork
from infrastructure.security.auth_adapters import (
    LoggingEmailSender,
    ProcessRateLimiter,
)
from tests.education_os.application.auth.conftest import STRONG_PASSWORD
from tests.education_os.application.fakes import InMemoryEventPublisher
from web.app import WebConfig, create_app

SRC_ROOT = Path(__file__).resolve().parents[4] / "src"
PRODUCT_FACTORIES = (
    SRC_ROOT / "infrastructure" / "composition" / "product_factories.py"
)
AUTH_FACTORY = SRC_ROOT / "adapters" / "flask" / "auth" / "factory.py"
ONBOARDING_FACTORY = SRC_ROOT / "adapters" / "flask" / "onboarding" / "factory.py"
AUTH_ROUTES = SRC_ROOT / "adapters" / "flask" / "auth" / "routes.py"
ONBOARDING_ROUTES = SRC_ROOT / "adapters" / "flask" / "onboarding" / "routes.py"

FORBIDDEN_IN_MEMORY_NAMES = frozenset(
    {
        "InMemoryUserAccountRepository",
        "InMemoryAuthTokenRepository",
        "InMemoryOnboardingRepository",
        "InMemoryCheckpointStore",
        "InMemoryRateLimiter",
        "RecordingEmailSender",
        "RecordingTwinInitializer",
    }
)


@pytest.fixture()
def session_factory():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False, class_=Session)
    yield factory
    engine.dispose()


def test_assemble_wires_product_services_on_sqlalchemy_product_uow(
    session_factory,
) -> None:
    container = assemble(session_factory)
    product = container.product

    assert isinstance(product, ProductServices)
    assert isinstance(product.authentication, TransactionalAuthenticationService)
    assert isinstance(product.onboarding, TransactionalOnboardingService)
    assert isinstance(
        product.student_initialization, TransactionalStudentInitializationService
    )
    assert isinstance(product.evidence_update, TransactionalEvidenceUpdateService)
    assert isinstance(product.checkpoint_store, ProductCheckpointStore)

    uow = product.new_unit_of_work()
    assert isinstance(uow, SqlAlchemyProductUnitOfWork)
    with uow:
        assert uow.users is not None
        assert uow.tokens is not None
        assert uow.onboarding is not None
        assert uow.twins is not None
        assert uow.evidence is not None
        assert uow.checkpoints is not None
        uow.commit()


def test_create_application_product_graph_has_no_in_memory_repositories(
    session_factory,
) -> None:
    container = assemble(session_factory)
    product = container.product

    auth = product.authentication
    assert not type(auth._hasher).__name__.startswith("InMemory")
    assert isinstance(auth._email_sender, LoggingEmailSender)
    assert isinstance(auth._rate_limiter, ProcessRateLimiter)

    # Fresh UoW repositories are SQLAlchemy adapters.
    with product.new_unit_of_work() as uow:
        assert type(uow.users).__name__.startswith("SqlAlchemy")
        assert type(uow.tokens).__name__.startswith("SqlAlchemy")
        assert type(uow.onboarding).__name__.startswith("SqlAlchemy")
        assert type(uow.twins).__name__.startswith("SqlAlchemy")
        assert type(uow.evidence).__name__.startswith("SqlAlchemy")
        assert type(uow.checkpoints).__name__.startswith("SqlAlchemy")
        uow.commit()


def test_authentication_persists_across_product_units_of_work(
    session_factory,
) -> None:
    events = InMemoryEventPublisher()
    product = build_product_services(
        session_factory,
        events=events,
        require_verified_email=False,
        expose_tokens=False,
    )

    registered = product.authentication.register(
        RegisterRequest(
            email="learner@example.com",
            password=STRONG_PASSWORD,
            client_key="test",
        )
    )
    assert registered.success is True

    with product.new_unit_of_work() as uow:
        loaded = uow.users.get_by_email(EmailAddress("learner@example.com"))
        assert loaded is not None
        assert loaded.email.value == "learner@example.com"
        uow.commit()


def test_onboarding_persists_across_product_units_of_work(session_factory) -> None:
    events = InMemoryEventPublisher()
    product = build_product_services(session_factory, events=events)

    started = product.onboarding.start(
        StartOnboardingRequest(student_id="student-br0045")
    )
    assert started.success is True
    onboarding_id = started.snapshot.onboarding_id

    with product.new_unit_of_work() as uow:
        loaded = uow.onboarding.get(OnboardingId(onboarding_id))
        assert loaded is not None
        assert str(loaded.student_id) == "student-br0045"
        uow.commit()


def test_checkpoint_store_uses_sqlalchemy_product_uow(session_factory) -> None:
    events = InMemoryEventPublisher()
    product = build_product_services(session_factory, events=events)
    store = product.checkpoint_store

    events_payload: list[dict[str, object]] = [
        {"type": "started", "session_id": "sess-1"},
        {"type": "paused", "session_id": "sess-1"},
    ]
    store.save("sess-1", events_payload)
    assert store.load("sess-1") == events_payload

    store.clear("sess-1")
    assert store.load("sess-1") is None


def test_create_app_binds_production_product_collaborators(session_factory) -> None:
    container = assemble(session_factory)
    app = create_app(
        WebConfig(testing=True, secret_key="br0045-secret"),
        container=container,
    )

    from adapters.flask.auth.dependency_provider import AUTH_DEPS_EXTENSION
    from adapters.flask.dashboard.dependency_provider import ADAPTER_DEPS_EXTENSION
    from adapters.flask.onboarding.dependency_provider import ONBOARDING_DEPS_EXTENSION

    auth_deps = app.extensions[AUTH_DEPS_EXTENSION]
    onboarding_deps = app.extensions[ONBOARDING_DEPS_EXTENSION]
    adapter_deps = app.extensions[ADAPTER_DEPS_EXTENSION]

    assert isinstance(
        auth_deps.auth_service, TransactionalAuthenticationService
    )
    assert isinstance(
        onboarding_deps.onboarding_service, TransactionalOnboardingService
    )
    assert isinstance(adapter_deps.checkpoint_store, ProductCheckpointStore)
    assert app.extensions["eos_evidence_updater"] is not None


def _instantiated_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                names.add(func.id)
            elif isinstance(func, ast.Attribute):
                names.add(func.attr)
    return names


@pytest.mark.parametrize(
    "path",
    [
        PRODUCT_FACTORIES,
        AUTH_FACTORY,
        ONBOARDING_FACTORY,
        AUTH_ROUTES,
        ONBOARDING_ROUTES,
    ],
    ids=lambda p: p.name,
)
def test_production_factories_do_not_instantiate_in_memory_or_recording(
    path: Path,
) -> None:
    instantiated = _instantiated_names(path)
    offenders = instantiated.intersection(FORBIDDEN_IN_MEMORY_NAMES)
    assert not offenders, f"{path.name} instantiates {sorted(offenders)}"


def test_product_factories_source_imports_no_memory_modules() -> None:
    source = PRODUCT_FACTORIES.read_text(encoding="utf-8")
    assert "application.auth.memory" not in source
    assert "application.onboarding.memory" not in source
    assert "InMemoryCheckpointStore" not in source
    assert "RecordingEmailSender" not in source
    assert "RecordingTwinInitializer" not in source
