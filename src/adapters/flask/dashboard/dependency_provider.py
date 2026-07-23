"""AdapterDependencies — injectable collaborators for Flask HTML adapters.

Resolves Educational OS collaborators for HTTP handlers without embedding
construction logic in routes. Controllers stay thin and unit-testable.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from typing import Any, Protocol

from flask import Flask, current_app, g, has_app_context, has_request_context, session

from adapters.flask.checkpoint_store import CheckpointStore
from adapters.flask.experience.gateway import (
    ExperienceGateway,
    MappingPriorReadinessStore,
)
from application.student_experience.integration.experience_integration_service import (
    ExperienceIntegrationService,
)

# Key used on Flask app.extensions / g for adapter dependency overrides.
ADAPTER_DEPS_EXTENSION = "eos_adapter_dependencies"
ADAPTER_DEPS_G_KEY = "eos_adapter_dependencies"
STUDENT_SESSION_KEY = "eos_student_id"


class PipelineResultLoader(Protocol):
    """Load an already-decided pipeline result for a student (no education here)."""

    def __call__(self, student_id: str) -> Any: ...


class EvidenceUpdater(Protocol):
    """Persist captured observational evidence (application service boundary)."""

    def __call__(self, captured: Any) -> Any: ...


def _null_pipeline_result(_student_id: str) -> None:
    """Default loader — presenters are null-safe when result is absent."""
    return None


def _null_evidence_update(_captured: Any) -> None:
    """Default updater — capture without persistence."""
    return None


def _empty_student_id() -> str:
    return ""


def _default_as_of() -> datetime:
    return datetime.now(UTC)


def _build_default_experience_gateway() -> ExperienceGateway:
    return ExperienceGateway(
        experience_service=ExperienceIntegrationService(),
        as_of_resolver=_default_as_of,
    )


@dataclass(frozen=True, slots=True)
class AdapterDependencies:
    """Explicit collaborators for Flask adapter controllers.

    All fields are injectable. Tests override loaders / factories without Flask.
    ``experience_gateway`` composes the live XP snapshot once per request.
    """

    load_pipeline_result: PipelineResultLoader = _null_pipeline_result
    student_id_resolver: Callable[[], str] = _empty_student_id
    update_evidence: EvidenceUpdater = _null_evidence_update
    checkpoint_store: CheckpointStore | None = None
    experience_gateway: ExperienceGateway = field(
        default_factory=_build_default_experience_gateway
    )


class FlaskDependencyProvider:
    """Resolve ``AdapterDependencies`` from Flask app context or explicit overrides.

    Production wiring may attach dependencies on ``app.extensions``. Tests may
    call ``override`` / ``bind`` without touching the Educational OS core.
    """

    def __init__(self, dependencies: AdapterDependencies | None = None) -> None:
        self._dependencies = dependencies or AdapterDependencies()

    @property
    def dependencies(self) -> AdapterDependencies:
        return self._dependencies

    def override(self, **kwargs: Any) -> AdapterDependencies:
        """Return a copy of dependencies with selected fields replaced."""
        self._dependencies = replace(self._dependencies, **kwargs)
        return self._dependencies

    def resolve(self) -> AdapterDependencies:
        """Resolve active dependencies for the current request / app / instance."""
        if has_request_context():
            bound = getattr(g, ADAPTER_DEPS_G_KEY, None)
            if isinstance(bound, AdapterDependencies):
                return bound
        if has_app_context():
            app_deps = current_app.extensions.get(ADAPTER_DEPS_EXTENSION)
            if isinstance(app_deps, AdapterDependencies):
                return app_deps
        return self._dependencies

    @staticmethod
    def bind(app: Flask, dependencies: AdapterDependencies) -> None:
        """Attach adapter dependencies to a Flask application."""
        app.extensions[ADAPTER_DEPS_EXTENSION] = dependencies

    @staticmethod
    def bind_request(dependencies: AdapterDependencies) -> None:
        """Override dependencies for the active request (tests / middleware)."""
        if not has_request_context():
            raise RuntimeError("bind_request requires an active request context")
        setattr(g, ADAPTER_DEPS_G_KEY, dependencies)

    @staticmethod
    def from_container(
        container: Any,
        *,
        request_builder: Callable[[str], Any] | None = None,
        student_id_resolver: Callable[[], str] | None = None,
        update_evidence: EvidenceUpdater | None = None,
        checkpoint_store: CheckpointStore | None = None,
        experience_integration_service: ExperienceIntegrationService | None = None,
        as_of_resolver: Callable[[], datetime] | None = None,
        experience_cargo_loader: Callable[[str], Any] | None = None,
        prior_readiness_mapping: dict[str, Any] | None = None,
    ) -> AdapterDependencies:
        """Build adapter dependencies from an ``ApplicationContainer``.

        ``request_builder`` supplies already-assembled ``PipelineRequest`` cargo
        (no educational decisions here). When omitted, the loader is null-safe.
        """
        pipeline = getattr(container, "educational_pipeline", None)

        def load(student_id: str) -> Any:
            if pipeline is None or request_builder is None:
                return None
            request = request_builder(student_id)
            if request is None:
                return None
            return pipeline.run(request)

        service = experience_integration_service or ExperienceIntegrationService()
        gateway = ExperienceGateway(
            experience_service=service,
            as_of_resolver=as_of_resolver or _default_as_of,
            cargo_loader=experience_cargo_loader,
            prior_readiness_store=MappingPriorReadinessStore(
                prior_readiness_mapping if prior_readiness_mapping is not None else {}
            ),
        )
        return AdapterDependencies(
            load_pipeline_result=load,
            student_id_resolver=student_id_resolver or flask_student_id_resolver,
            update_evidence=update_evidence or _null_evidence_update,
            checkpoint_store=checkpoint_store,
            experience_gateway=gateway,
        )


def flask_student_id_resolver() -> str:
    """Resolve learner identity from query args or Flask session."""
    if not has_request_context():
        return ""
    from flask import request

    query_id = (request.args.get("student_id") or "").strip()
    if query_id:
        return query_id
    return str(session.get(STUDENT_SESSION_KEY) or "").strip()


def get_dependencies() -> AdapterDependencies:
    """Module-level convenience for route handlers."""
    return FlaskDependencyProvider().resolve()
