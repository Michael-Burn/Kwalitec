"""Application composition root for the Educational Operating System.

This package is the single location where repositories, unit of work, domain
engines, application services, AI providers, explainability, and experience
generation are constructed and injected.
"""

from __future__ import annotations

from application.composition.application_factory import (
    assemble,
    create_application,
    create_request_scope,
)
from application.composition.container import ApplicationContainer, RequestScope
from application.composition.service_registry import (
    SERVICE_NAMES,
    CompositionError,
    ServiceRegistry,
)

__all__ = [
    "SERVICE_NAMES",
    "ApplicationContainer",
    "CompositionError",
    "RequestScope",
    "ServiceRegistry",
    "assemble",
    "create_application",
    "create_request_scope",
]
