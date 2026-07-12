"""Shared TwinRepository for product Integration wiring.

Birth persistence and Twin retrieval must share one TwinRepository instance
within a process. Capability 3.8.2 uses the durable SQLAlchemy-backed
TwinRepository — snapshots survive process restart.

This module only owns the shared handle — never Twin content, educational
reasoning, or Calibration / Orchestrator logic.

See Capabilities 3.7.1–3.7.3 and 3.8.2.
"""

from __future__ import annotations

from app.application.twin_repository.twin_repository import TwinRepository

_PROCESS_REPOSITORY: TwinRepository | None = None


def get_shared_twin_repository() -> TwinRepository:
    """Return the process-shared durable TwinRepository singleton.

    Creates the repository on first use. Callers that persist Birth Twins and
    callers that retrieve them must use this same instance so that durable
    snapshots are visible across Application wiring within a process;
    durability itself is provided by SQLAlchemy / SQLite.
    """
    global _PROCESS_REPOSITORY
    if _PROCESS_REPOSITORY is None:
        _PROCESS_REPOSITORY = TwinRepository()
    return _PROCESS_REPOSITORY


def reset_shared_twin_repository() -> TwinRepository:
    """Replace the shared repository handle (tests / isolated process reset).

    Does not delete durable TwinSnapshot rows — tests that need an empty store
    should truncate the ``twin_snapshots`` table (or use the ``db`` fixture).

    Returns the new TwinRepository instance.
    """
    global _PROCESS_REPOSITORY
    _PROCESS_REPOSITORY = TwinRepository()
    return _PROCESS_REPOSITORY
