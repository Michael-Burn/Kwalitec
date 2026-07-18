"""FeatureGate tests."""

from __future__ import annotations

from app.application.mission_adapter.feature_gate import FeatureGate
from app.application.mission_adapter.migration_manager import (
    MigrationManager,
    MigrationPhase,
)
from tests.application.mission_adapter.helpers import make_request


def _gate(
    *,
    phase: MigrationPhase = MigrationPhase.PARALLEL_VALIDATION,
    global_enabled: bool = True,
    cohorts=None,
    orgs=None,
    envs=None,
) -> FeatureGate:
    return FeatureGate(
        migration_manager=MigrationManager(initial_phase=phase),
        global_enabled=global_enabled,
        allowed_cohorts=cohorts,
        allowed_organisations=orgs,
        allowed_environments=envs,
    )


def test_global_disable():
    gate = _gate(global_enabled=False)
    assert gate.is_v2_enabled(make_request()) is False
    assert gate.reason(make_request()) == "global_disabled"


def test_phase_disallows():
    gate = _gate(phase=MigrationPhase.LEGACY_ONLY, global_enabled=True)
    assert gate.is_v2_enabled(make_request()) is False
    assert gate.reason(make_request()) == "phase_disallows_v2"


def test_cohort_denied():
    gate = _gate(cohorts={"alpha"})
    assert gate.is_v2_enabled(make_request(cohort_id="beta")) is False
    assert gate.reason(make_request(cohort_id="beta")) == "cohort_denied"


def test_organisation_denied():
    gate = _gate(orgs={"org-a"})
    assert gate.is_v2_enabled(make_request(organisation_id="org-b")) is False
    assert (
        gate.reason(make_request(organisation_id="org-b")) == "organisation_denied"
    )


def test_environment_denied():
    gate = _gate(envs={"staging"})
    assert gate.is_v2_enabled(make_request(environment="production")) is False
    assert (
        gate.reason(make_request(environment="production")) == "environment_denied"
    )


def test_all_gates_enabled():
    gate = _gate(
        cohorts={"alpha"},
        orgs={"org-a"},
        envs={"staging"},
    )
    req = make_request(
        cohort_id="alpha",
        organisation_id="org-a",
        environment="staging",
    )
    assert gate.is_v2_enabled(req) is True
    assert gate.reason(req) == "v2_enabled"


def test_set_global_enabled():
    gate = _gate(global_enabled=False)
    gate.set_global_enabled(True)
    assert gate.global_enabled is True
    assert gate.is_v2_enabled(make_request()) is True


def test_configure_cohorts():
    gate = _gate()
    gate.configure_cohorts({"x"})
    assert gate.is_v2_enabled(make_request(cohort_id="x")) is True
    assert gate.is_v2_enabled(make_request(cohort_id="y")) is False


def test_configure_organisations():
    gate = _gate()
    gate.configure_organisations({"o1"})
    assert gate.is_v2_enabled(make_request(organisation_id="o1")) is True


def test_configure_environments():
    gate = _gate()
    gate.configure_environments({"dev"})
    assert gate.is_v2_enabled(make_request(environment="dev")) is True
    assert gate.is_v2_enabled(make_request(environment="production")) is False


def test_phase_property():
    gate = _gate(phase=MigrationPhase.LIMITED_V2)
    assert gate.phase == MigrationPhase.LIMITED_V2


def test_empty_allow_lists_mean_all():
    gate = _gate(cohorts=set(), orgs=set(), envs=set())
    assert gate.is_v2_enabled(make_request()) is True
