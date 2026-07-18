"""Stateless rollout rules for Version 2 mission exposure.

Pure application policy — no UI, no controllers, no persistence.
"""

from __future__ import annotations

from app.application.mission_adapter.dto.adapter_request import AdapterRequest
from app.application.mission_adapter.migration_manager import MigrationPhase


class RolloutPolicy:
    """Deterministic V2 rollout eligibility (stateless)."""

    PRODUCTION_ENVIRONMENTS: frozenset[str] = frozenset(
        {"production", "prod", "live"}
    )
    NON_PRODUCTION_ENVIRONMENTS: frozenset[str] = frozenset(
        {"development", "dev", "test", "staging", "local"}
    )

    @staticmethod
    def normalise_environment(environment: str) -> str:
        """Lower-case strip environment label."""
        return (environment or "production").strip().lower()

    @staticmethod
    def is_non_production(environment: str) -> bool:
        """True when environment is a known non-production label."""
        env = RolloutPolicy.normalise_environment(environment)
        return env in RolloutPolicy.NON_PRODUCTION_ENVIRONMENTS

    @staticmethod
    def phase_allows_v2(phase: MigrationPhase) -> bool:
        """True when migration phase may expose or shadow V2."""
        return phase in {
            MigrationPhase.PARALLEL_VALIDATION,
            MigrationPhase.LIMITED_V2,
            MigrationPhase.FULL_V2,
            MigrationPhase.RETIRED_V1,
        }

    @staticmethod
    def phase_requires_v2(phase: MigrationPhase) -> bool:
        """True when V2 is mandatory for the phase."""
        return phase in {
            MigrationPhase.FULL_V2,
            MigrationPhase.RETIRED_V1,
        }

    @staticmethod
    def cohort_allows(
        request: AdapterRequest,
        *,
        allowed_cohorts: frozenset[str] | set[str] | None,
    ) -> bool:
        """True when cohort gate is open (empty allow-list = all cohorts)."""
        if not allowed_cohorts:
            return True
        if request.cohort_id is None:
            return False
        return request.cohort_id in allowed_cohorts

    @staticmethod
    def organisation_allows(
        request: AdapterRequest,
        *,
        allowed_organisations: frozenset[str] | set[str] | None,
    ) -> bool:
        """True when organisation gate is open (empty = all orgs)."""
        if not allowed_organisations:
            return True
        if request.organisation_id is None:
            return False
        return request.organisation_id in allowed_organisations

    @staticmethod
    def environment_allows(
        request: AdapterRequest,
        *,
        allowed_environments: frozenset[str] | set[str] | None,
    ) -> bool:
        """True when environment gate is open (empty = all environments)."""
        env = RolloutPolicy.normalise_environment(request.environment)
        if not allowed_environments:
            return True
        normalised = {
            RolloutPolicy.normalise_environment(e) for e in allowed_environments
        }
        return env in normalised

    @staticmethod
    def evaluate(
        request: AdapterRequest,
        *,
        phase: MigrationPhase,
        global_enabled: bool,
        allowed_cohorts: frozenset[str] | set[str] | None = None,
        allowed_organisations: frozenset[str] | set[str] | None = None,
        allowed_environments: frozenset[str] | set[str] | None = None,
    ) -> bool:
        """True when V2 may participate for this request.

        All configured gates must pass. Global disable short-circuits.
        ``phase_requires_v2`` still respects global_enabled so operators
        can hard-stop V2 even in FULL_V2 / RETIRED_V1 for emergency
        rollback (migration manager owns lawful phase rollback).
        """
        if not global_enabled:
            return False
        if not RolloutPolicy.phase_allows_v2(phase):
            return False
        if not RolloutPolicy.cohort_allows(
            request, allowed_cohorts=allowed_cohorts
        ):
            return False
        if not RolloutPolicy.organisation_allows(
            request, allowed_organisations=allowed_organisations
        ):
            return False
        if not RolloutPolicy.environment_allows(
            request, allowed_environments=allowed_environments
        ):
            return False
        return True
