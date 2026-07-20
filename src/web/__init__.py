"""Flask presentation layer for the Educational Operating System."""

from __future__ import annotations

from web.app import create_app
from web.lifecycle import (
    RequestScope,
    get_request_scope,
    get_services,
    get_unit_of_work,
)

__all__ = [
    "RequestScope",
    "create_app",
    "get_request_scope",
    "get_services",
    "get_unit_of_work",
]
