"""EvidenceAdvisory contract tests (P2-MS009)."""

from __future__ import annotations

import pytest

from app.infrastructure.adapters.evidence_platform.contracts import (
    AUTHORITY_EVIDENCE_PLATFORM,
    EVIDENCE_VERSION_ADVISORY,
    ConsistencySummary,
    EngagementSummary,
    EvidenceAdvisory,
    FactualConstraint,
    ObservedPattern,
)


def test_evidence_advisory_is_frozen():
    advisory = EvidenceAdvisory(
        advisory_id="evadv-test",
        reporting_period="this_week",
        generated_at="2026-08-07T12:00:00+00:00",
        student_id="42",
    )
    with pytest.raises(Exception):
        advisory.advisory_id = "mutated"  # type: ignore[misc]


def test_evidence_advisory_requires_traceable_fields():
    advisory = EvidenceAdvisory(
        advisory_id="evadv-1",
        reporting_period="this_week",
        observed_patterns=(
            ObservedPattern(
                pattern_key="session_completed",
                observation="session_completed observed 2 times",
                count=2,
                evidence_refs=("ev-1",),
                source_description="Derived from recorded study activity.",
            ),
        ),
        engagement_summary=EngagementSummary(
            completed_missions=2,
            study_sessions=2,
            completed_reflections=1,
            event_counts={"session_completed": 2, "reflection_completed": 1},
            source_description="Derived from recorded study activity.",
        ),
        consistency_summary=ConsistencySummary(
            active_streak=2,
            source_description="Derived from recorded study activity.",
        ),
        factual_constraints=(
            FactualConstraint(
                constraint_key="example",
                statement="Example factual constraint.",
                source_description="Derived from recorded study activity.",
            ),
        ),
        provenance={"source_service": "evidence_advisory_assembler"},
        generated_at="2026-08-07T12:00:00+00:00",
        student_id="42",
        evidence_summary_id="evfact-1",
        evidence_refs=("ev-1",),
        source_description="Derived from recorded study activity between 1–7 August.",
    )
    payload = advisory.to_canonical_dict()
    assert payload["advisory_id"] == "evadv-1"
    assert payload["authority"] == AUTHORITY_EVIDENCE_PLATFORM
    assert payload["advisory_version"] == EVIDENCE_VERSION_ADVISORY
    assert payload["observed_patterns"][0]["pattern_key"] == "session_completed"
    assert payload["engagement_summary"]["study_sessions"] == 2
    assert payload["consistency_summary"]["active_streak"] == 2
    assert payload["factual_constraints"][0]["constraint_key"] == "example"
    assert "provenance" in payload
    assert "August" in payload["source_description"]
    assert advisory.serialize() == EvidenceAdvisory(**{
        k: getattr(advisory, k)
        for k in (
            "advisory_id",
            "reporting_period",
            "observed_patterns",
            "engagement_summary",
            "consistency_summary",
            "factual_constraints",
            "provenance",
            "generated_at",
            "student_id",
            "evidence_summary_id",
            "evidence_refs",
            "source_description",
            "authority",
            "availability",
            "unavailable_reason",
            "advisory_version",
        )
    }).serialize()


def test_factual_constraint_rejects_empty_statement():
    with pytest.raises(ValueError, match="statement"):
        FactualConstraint(constraint_key="x", statement="")


def test_engagement_summary_rejects_negative():
    with pytest.raises(ValueError):
        EngagementSummary(study_sessions=-1)


def test_no_recommendation_fields_on_advisory():
    fields = set(EvidenceAdvisory.__dataclass_fields__)
    forbidden = {
        "recommendation",
        "next_action",
        "mastery",
        "prediction",
        "score",
        "suggested_topic",
    }
    assert fields.isdisjoint(forbidden)
