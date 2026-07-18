"""Feature gate for Version 2 mission engine participation.

Pure application service — no UI, no controllers, no persistence.
Supports enabling V2 via global mode, user cohort, organisation, and
environment.
"""

from __future__ import annotations

from app.application.mission_adapter.dto.adapter_request import AdapterRequest
from app.application.mission_adapter.migration_manager import (
    MigrationManager,
    MigrationPhase,
)
from app.application.mission_adapter.policies.rollout_policy import RolloutPolicy


class FeatureGate:
    """Evaluates whether Version 2 may participate for a request.

    Configuration is injected at construction. The gate never mutates
    migration state and never alters routing itself — callers combine
    ``is_v2_enabled`` with ``MissionRouter``.
    """

    def __init__(
        self,
        *,
        migration_manager: MigrationManager,
        global_enabled: bool = False,
        allowed_cohorts: frozenset[str] | set[str] | None = None,
        allowed_organisations: frozenset[str] | set[str] | None = None,
        allowed_environments: frozenset[str] | set[str] | None = None,
    ) -> None:
        self._migration = migration_manager
        self._global_enabled = global_enabled
        self._allowed_cohorts = (
            frozenset(allowed_cohorts) if allowed_cohorts else frozenset()
        )
        self._allowed_organisations = (
            frozenset(allowed_organisations)
            if allowed_organisations
            else frozenset()
        )
        self._allowed_environments = (
            frozenset(allowed_environments)
            if allowed_environments
            else frozenset()
        )

    @property
    def global_enabled(self) -> bool:
        """Whether the global V2 switch is on."""
        return self._global_enabled

    def set_global_enabled(self, enabled: bool) -> None:
        """Toggle the global V2 switch (operator control)."""
        self._global_enabled = bool(enabled)

    def configure_cohorts(self, cohorts: frozenset[str] | set[str]) -> None:
        """Replace the allowed cohort set (empty = all)."""
        self._allowed_cohorts = frozenset(cohorts)

    def configure_organisations(
        self, organisations: frozenset[str] | set[str]
    ) -> None:
        """Replace the allowed organisation set (empty = all)."""
        self._allowed_organisations = frozenset(organisations)

    def configure_environments(
        self, environments: frozenset[str] | set[str]
    ) -> None:
        """Replace the allowed environment set (empty = all)."""
        self._allowed_environments = frozenset(environments)

    @property
    def phase(self) -> MigrationPhase:
        """Current migration phase (read-through)."""
        return self._migration.phase

    def is_v2_enabled(self, request: AdapterRequest) -> bool:
        """True when V2 may participate for ``request``."""
        return RolloutPolicy.evaluate(
            request,
            phase=self._migration.phase,
            global_enabled=self._global_enabled,
            allowed_cohorts=self._allowed_cohorts or None,
            allowed_organisations=self._allowed_organisations or None,
            allowed_environments=self._allowed_environments or None,
        )

    def reason(self, request: AdapterRequest) -> str:
        """Stable machine-readable reason for the gate decision."""
        if not self._global_enabled:
            return "global_disabled"
        if not RolloutPolicy.phase_allows_v2(self._migration.phase):
            return "phase_disallows_v2"
        if not RolloutPolicy.cohort_allows(
            request, allowed_cohorts=self._allowed_cohorts or None
        ):
            return "cohort_denied"
        if not RolloutPolicy.organisation_allows(
            request, allowed_organisations=self._allowed_organisations or None
        ):
            return "organisation_denied"
        if not RolloutPolicy.environment_allows(
            request, allowed_environments=self._allowed_environments or None
        ):
            return "environment_denied"
        return "v2_enabled"
