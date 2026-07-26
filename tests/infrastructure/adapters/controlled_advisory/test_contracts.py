"""Controlled Advisory Activation contract tests (P3-MS001)."""

from __future__ import annotations

import pytest

from app.infrastructure.adapters.controlled_advisory import (
    APPROVED_ADVISORY_FIELD_CONSISTENCY,
    REASON_FIELD_NOT_APPROVED,
    REASON_MULTIPLE_FIELDS,
    AdvisoryActivationDecision,
    AdvisoryPolicy,
    ControlledAdvisoryExplainability,
    build_default_advisory_policy,
    validate_advisory_policy,
)


def test_advisory_policy_immutable_and_single_field():
    policy = build_default_advisory_policy(rollout_percentage=25)
    assert policy.enabled_field == APPROVED_ADVISORY_FIELD_CONSISTENCY
    assert len(policy.enabled_advisory_fields) == 1
    assert policy.rollout_percentage == 25
    with pytest.raises(Exception):
        policy.rollout_percentage = 50  # type: ignore[misc]


def test_advisory_policy_rejects_multiple_fields():
    policy = AdvisoryPolicy(
        policy_id="bad",
        enabled_advisory_fields=("consistency_summary", "engagement_summary"),
        activation_conditions={"max_age_hours": 24},
        rollout_percentage=10,
        policy_version="x",
        effective_from="2026-01-01T00:00:00+00:00",
    )
    assert validate_advisory_policy(policy) == REASON_MULTIPLE_FIELDS


def test_advisory_policy_rejects_unapproved_field():
    policy = AdvisoryPolicy(
        policy_id="bad",
        enabled_advisory_fields=("engagement_summary",),
        activation_conditions={"max_age_hours": 24},
        rollout_percentage=10,
        policy_version="x",
        effective_from="2026-01-01T00:00:00+00:00",
    )
    assert validate_advisory_policy(policy) == REASON_FIELD_NOT_APPROVED


def test_activation_decision_canonical():
    decision = AdvisoryActivationDecision(
        allowed=True,
        reason="policy_allows_approved_field",
        policy_id="p",
        policy_version="v",
        advisory_field="consistency_summary",
        student_id="7",
        feature_flag_enabled=True,
        rollout_percentage=100,
        in_rollout=True,
        advisory_id="evadv-1",
        evidence_provenance={"advisory_id": "evadv-1"},
    )
    payload = decision.to_canonical_dict()
    assert payload["allowed"] is True
    assert payload["advisory_field"] == "consistency_summary"
    assert payload["evidence_provenance"]["advisory_id"] == "evadv-1"


def test_explainability_clears_rejection_when_activated():
    record = ControlledAdvisoryExplainability(
        activated=True,
        advisory_field_used="consistency_summary",
        policy_version="p3.ms001.1",
        activation_reason="policy_allows_approved_field",
        rejection_reason="should_clear",
        evidence_provenance={"k": "v"},
        advisory_id="evadv-1",
        policy_id="controlled-advisory-p3-ms001",
    )
    assert record.rejection_reason == ""
    assert record.advisory_field_used == "consistency_summary"
    denied = ControlledAdvisoryExplainability(
        activated=False,
        advisory_field_used="consistency_summary",
        activation_reason="should_clear",
        rejection_reason="rollout_percentage_excluded",
    )
    assert denied.advisory_field_used == ""
    assert denied.activation_reason == ""
    assert denied.rejection_reason == "rollout_percentage_excluded"
