"""Product composition factories — BR-004.5 production dependency graph.

Constructs Authentication, Onboarding, Student Initialization, Evidence Update,
and Checkpoint collaborators on ``SqlAlchemyProductUnitOfWork``. Never installs
in-memory repositories or recording doubles.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from application.auth.auth_service import AuthenticationService
from application.auth.ports import (
    Clock as AuthClock,
    EmailSender,
    PasswordHasher,
    RateLimiter,
    TokenHasher,
)
from application.evidence_update.evidence_update_service import EvidenceUpdateService
from application.onboarding.onboarding_service import OnboardingService
from application.onboarding.ports import (
    Clock as OnboardingClock,
    OnboardingIdGenerator,
)
from application.ports.event_publisher import ApplicationEventPublisher
from domain.onboarding.ids import OnboardingId
from infrastructure.persistence.product_checkpoint_store import ProductCheckpointStore
from infrastructure.persistence.sqlalchemy.unit_of_work import SessionFactory
from infrastructure.persistence.sqlalchemy_uow import SqlAlchemyProductUnitOfWork
from infrastructure.security.argon2_password_hasher import Argon2PasswordHasher
from infrastructure.security.auth_adapters import (
    HmacStubPasswordHasher,
    LoggingEmailSender,
    ProcessRateLimiter,
    Sha256TokenHasher,
)


class UtcClock(AuthClock, OnboardingClock):
    """Shared wall-clock UTC source for product application services."""

    def now(self) -> datetime:
        return datetime.now(UTC)


class UuidOnboardingIdGenerator(OnboardingIdGenerator):
    """Allocate opaque onboarding identities."""

    def next_identity(self) -> OnboardingId:
        return OnboardingId(f"ob-{uuid4().hex}")


def build_product_unit_of_work(
    session_factory: SessionFactory,
) -> SqlAlchemyProductUnitOfWork:
    """Construct the BR-004 product transactional boundary."""
    return SqlAlchemyProductUnitOfWork(session_factory)


def build_production_password_hasher() -> PasswordHasher:
    """Prefer Argon2; fall back only when the optional package is absent."""
    try:
        return Argon2PasswordHasher()
    except Exception:  # pragma: no cover - import/runtime guard
        return HmacStubPasswordHasher()  # type: ignore[return-value]


class TransactionalAuthenticationService:
    """Open a product UoW for each authentication use-case.

    Preserves ``AuthenticationService`` domain behaviour while ensuring
    SQLAlchemy repositories share one transactional session per call.
    """

    def __init__(
        self,
        session_factory: SessionFactory,
        *,
        hasher: PasswordHasher,
        token_hasher: TokenHasher,
        email_sender: EmailSender,
        rate_limiter: RateLimiter,
        clock: AuthClock,
        require_verified_email: bool = True,
        expose_tokens: bool = False,
    ) -> None:
        self._session_factory = session_factory
        self._hasher = hasher
        self._token_hasher = token_hasher
        self._email_sender = email_sender
        self._rate_limiter = rate_limiter
        self._clock = clock
        self._require_verified_email = require_verified_email
        self._expose_tokens = expose_tokens

    def _service(self, uow: SqlAlchemyProductUnitOfWork) -> AuthenticationService:
        return AuthenticationService(
            users=uow.users,
            tokens=uow.tokens,
            hasher=self._hasher,
            token_hasher=self._token_hasher,
            email_sender=self._email_sender,
            rate_limiter=self._rate_limiter,
            clock=self._clock,
            require_verified_email=self._require_verified_email,
            expose_tokens=self._expose_tokens,
        )

    def _run(self, operation: Callable[[AuthenticationService], Any]) -> Any:
        uow = SqlAlchemyProductUnitOfWork(self._session_factory)
        with uow:
            result = operation(self._service(uow))
            uow.commit()
            return result

    def register(self, request: Any) -> Any:
        return self._run(lambda service: service.register(request))

    def login(self, request: Any) -> Any:
        return self._run(lambda service: service.login(request))

    def logout(self, user_id: str | None) -> Any:
        return self._run(lambda service: service.logout(user_id))

    def verify_email(self, request: Any) -> Any:
        return self._run(lambda service: service.verify_email(request))

    def request_password_reset(self, request: Any) -> Any:
        return self._run(lambda service: service.request_password_reset(request))

    def reset_password(self, request: Any) -> Any:
        return self._run(lambda service: service.reset_password(request))

    def change_password(self, request: Any) -> Any:
        return self._run(lambda service: service.change_password(request))

    def validate_session(self, request: Any) -> Any:
        return self._run(lambda service: service.validate_session(request))

    def touch_session(self, claims: Any) -> Any:
        return self._run(lambda service: service.touch_session(claims))


class TransactionalOnboardingService:
    """Open a product UoW for each onboarding use-case."""

    def __init__(
        self,
        session_factory: SessionFactory,
        *,
        twin_initializer: Any,
        clock: OnboardingClock,
        id_generator: OnboardingIdGenerator,
    ) -> None:
        self._session_factory = session_factory
        self._twin_initializer = twin_initializer
        self._clock = clock
        self._id_generator = id_generator

    def _service(self, uow: SqlAlchemyProductUnitOfWork) -> OnboardingService:
        return OnboardingService(
            repository=uow.onboarding,
            twin_initializer=self._twin_initializer,
            clock=self._clock,
            id_generator=self._id_generator,
        )

    def _run(self, operation: Callable[[OnboardingService], Any]) -> Any:
        uow = SqlAlchemyProductUnitOfWork(self._session_factory)
        with uow:
            result = operation(self._service(uow))
            uow.commit()
            return result

    def start(self, request: Any) -> Any:
        return self._run(lambda service: service.start(request))

    def resume(self, request: Any) -> Any:
        return self._run(lambda service: service.resume(request))

    def save_step(self, request: Any) -> Any:
        return self._run(lambda service: service.save_step(request))

    def advance(self, request: Any) -> Any:
        return self._run(lambda service: service.advance(request))

    def go_back(self, request: Any) -> Any:
        return self._run(lambda service: service.go_back(request))

    def skip_optional(self, request: Any) -> Any:
        return self._run(lambda service: service.skip_optional(request))

    def complete(self, request: Any) -> Any:
        return self._run(lambda service: service.complete(request))


@dataclass(frozen=True, slots=True)
class ProductServices:
    """Product-surface collaborators assembled on SqlAlchemyProductUnitOfWork."""

    unit_of_work: SqlAlchemyProductUnitOfWork
    authentication: TransactionalAuthenticationService
    onboarding: TransactionalOnboardingService
    student_initialization: Any
    evidence_update: EvidenceUpdateService
    checkpoint_store: ProductCheckpointStore


def build_product_services(
    session_factory: SessionFactory,
    *,
    events: ApplicationEventPublisher,
    clock: Any | None = None,
    educational_pipeline: object | None = None,
    hasher: PasswordHasher | None = None,
    token_hasher: TokenHasher | None = None,
    email_sender: EmailSender | None = None,
    rate_limiter: RateLimiter | None = None,
    require_verified_email: bool = True,
    expose_tokens: bool = False,
) -> ProductServices:
    """Assemble the full BR-004 production product dependency graph."""
    # Local imports keep package import graphs free of composition cycles.
    from application.student_initialization.onboarding_adapter import (
        StudentTwinInitializerAdapter,
    )
    from application.student_initialization.student_initialization_service import (
        EducationalPipelineAdapter,
        StudentInitializationService,
    )

    resolved_clock = clock or UtcClock()
    product_uow = build_product_unit_of_work(session_factory)

    if educational_pipeline is None:
        from application.pipeline.educational_pipeline import EducationalPipeline

        educational_pipeline = EducationalPipeline()

    student_initialization = StudentInitializationService(
        uow=product_uow,  # type: ignore[arg-type]
        events=events,
        clock=resolved_clock,
        pipeline=EducationalPipelineAdapter(
            educational_pipeline  # type: ignore[arg-type]
        ),
    )
    twin_initializer = StudentTwinInitializerAdapter(
        student_initialization,
        resolved_clock,
    )

    authentication = TransactionalAuthenticationService(
        session_factory,
        hasher=hasher or build_production_password_hasher(),
        token_hasher=token_hasher or Sha256TokenHasher(),
        email_sender=email_sender or LoggingEmailSender(),
        rate_limiter=rate_limiter or ProcessRateLimiter(),
        clock=resolved_clock,
        require_verified_email=require_verified_email,
        expose_tokens=expose_tokens,
    )
    onboarding = TransactionalOnboardingService(
        session_factory,
        twin_initializer=twin_initializer,
        clock=resolved_clock,
        id_generator=UuidOnboardingIdGenerator(),
    )
    evidence_update = EvidenceUpdateService(
        product_uow,  # type: ignore[arg-type]
        events,
        resolved_clock,
    )
    checkpoint_store = ProductCheckpointStore(session_factory)

    return ProductServices(
        unit_of_work=product_uow,
        authentication=authentication,
        onboarding=onboarding,
        student_initialization=student_initialization,
        evidence_update=evidence_update,
        checkpoint_store=checkpoint_store,
    )


__all__ = [
    "ProductServices",
    "TransactionalAuthenticationService",
    "TransactionalOnboardingService",
    "UtcClock",
    "UuidOnboardingIdGenerator",
    "build_product_services",
    "build_product_unit_of_work",
    "build_production_password_hasher",
]
