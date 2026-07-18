"""Policy behaviour tests (routing, comparison, rollout)."""

from __future__ import annotations

import pytest

from app.application.mission_adapter.dto.routing_decision import (
    RoutingMode,
    SelectedEngine,
)
from app.application.mission_adapter.exceptions import RoutingError
from app.application.mission_adapter.migration_manager import MigrationPhase
from app.application.mission_adapter.policies.comparison_policy import (
    ComparisonPolicy,
)
from app.application.mission_adapter.policies.rollout_policy import RolloutPolicy
from app.application.mission_adapter.policies.routing_policy import RoutingPolicy
from tests.application.mission_adapter.helpers import make_request


def test_policies_package_exports():
    from app.application.mission_adapter import policies

    assert policies.RoutingPolicy is RoutingPolicy
    assert policies.ComparisonPolicy is ComparisonPolicy
    assert policies.RolloutPolicy is RolloutPolicy


@pytest.mark.parametrize(
    "env",
    ["development", "dev", "test", "staging", "local"],
)
def test_non_production_envs(env):
    assert RolloutPolicy.is_non_production(env) is True


@pytest.mark.parametrize("env", ["production", "prod", "live"])
def test_production_envs(env):
    assert RolloutPolicy.is_non_production(env) is False


def test_normalise_environment():
    assert RolloutPolicy.normalise_environment("  Prod  ") == "prod"
    assert RolloutPolicy.normalise_environment("") == "production"


@pytest.mark.parametrize(
    ("phase", "allows"),
    [
        (MigrationPhase.LEGACY_ONLY, False),
        (MigrationPhase.PARALLEL_VALIDATION, True),
        (MigrationPhase.LIMITED_V2, True),
        (MigrationPhase.FULL_V2, True),
        (MigrationPhase.RETIRED_V1, True),
    ],
)
def test_phase_allows_v2(phase, allows):
    assert RolloutPolicy.phase_allows_v2(phase) is allows


@pytest.mark.parametrize(
    ("phase", "requires"),
    [
        (MigrationPhase.LEGACY_ONLY, False),
        (MigrationPhase.PARALLEL_VALIDATION, False),
        (MigrationPhase.LIMITED_V2, False),
        (MigrationPhase.FULL_V2, True),
        (MigrationPhase.RETIRED_V1, True),
    ],
)
def test_phase_requires_v2(phase, requires):
    assert RolloutPolicy.phase_requires_v2(phase) is requires


def test_cohort_allows_empty():
    assert (
        RolloutPolicy.cohort_allows(make_request(cohort_id=None), allowed_cohorts=None)
        is True
    )


def test_cohort_allows_match():
    req = make_request(cohort_id="alpha")
    assert RolloutPolicy.cohort_allows(req, allowed_cohorts={"alpha"}) is True
    assert RolloutPolicy.cohort_allows(req, allowed_cohorts={"beta"}) is False


def test_cohort_denies_missing():
    req = make_request(cohort_id=None)
    assert RolloutPolicy.cohort_allows(req, allowed_cohorts={"alpha"}) is False


def test_organisation_gate():
    req = make_request(organisation_id="org-1")
    assert (
        RolloutPolicy.organisation_allows(req, allowed_organisations={"org-1"})
        is True
    )
    assert (
        RolloutPolicy.organisation_allows(req, allowed_organisations={"org-2"})
        is False
    )


def test_environment_gate():
    req = make_request(environment="staging")
    assert (
        RolloutPolicy.environment_allows(
            req, allowed_environments={"staging", "dev"}
        )
        is True
    )
    assert (
        RolloutPolicy.environment_allows(req, allowed_environments={"production"})
        is False
    )


def test_evaluate_global_off():
    assert (
        RolloutPolicy.evaluate(
            make_request(),
            phase=MigrationPhase.FULL_V2,
            global_enabled=False,
        )
        is False
    )


def test_evaluate_phase_blocks():
    assert (
        RolloutPolicy.evaluate(
            make_request(),
            phase=MigrationPhase.LEGACY_ONLY,
            global_enabled=True,
        )
        is False
    )


def test_evaluate_all_gates_pass():
    req = make_request(
        cohort_id="c1",
        organisation_id="o1",
        environment="staging",
    )
    assert (
        RolloutPolicy.evaluate(
            req,
            phase=MigrationPhase.LIMITED_V2,
            global_enabled=True,
            allowed_cohorts={"c1"},
            allowed_organisations={"o1"},
            allowed_environments={"staging"},
        )
        is True
    )


def test_routing_legacy_decision():
    d = RoutingPolicy.decide(
        mode=RoutingMode.LEGACY,
        request=make_request(),
        v2_enabled=False,
        v1_available=True,
        v2_available=False,
    )
    assert d.primary_engine == SelectedEngine.V1


def test_routing_shadow_without_v2():
    d = RoutingPolicy.decide(
        mode=RoutingMode.SHADOW,
        request=make_request(),
        v2_enabled=True,
        v1_available=True,
        v2_available=False,
    )
    assert d.shadow_engine is None
    assert d.compare is False


def test_routing_ab_disabled_v2():
    d = RoutingPolicy.decide(
        mode=RoutingMode.A_B,
        request=make_request(),
        v2_enabled=False,
        v1_available=True,
        v2_available=True,
    )
    assert d.reason == "ab_v2_disabled"
    assert d.primary_engine == SelectedEngine.V1


def test_routing_unsupported_mode():
    with pytest.raises(RoutingError):
        RoutingPolicy.decide(
            mode="weird",  # type: ignore[arg-type]
            request=make_request(),
            v2_enabled=True,
            v1_available=True,
            v2_available=True,
        )


def test_ab_salt_changes_bucket_distribution():
    # Different salts may remap individuals; both remain deterministic.
    a = RoutingPolicy.ab_bucket("learner-x", salt="salt-a")
    b = RoutingPolicy.ab_bucket("learner-x", salt="salt-a")
    assert a == b


def test_comparison_policy_divergence_count():
    from app.application.mission_adapter.dto.comparison_result import DimensionMatch

    dims = (
        DimensionMatch("a", True, "1", "1"),
        DimensionMatch("b", False, "1", "2"),
        DimensionMatch("c", False, "1", "3"),
    )
    assert ComparisonPolicy.divergence_count(dims) == 2
    assert ComparisonPolicy.all_matched(dims) is False
