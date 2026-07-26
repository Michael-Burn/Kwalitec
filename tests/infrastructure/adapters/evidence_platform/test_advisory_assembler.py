"""EvidenceAdvisoryAssembler tests (P2-MS009)."""

from __future__ import annotations

from datetime import date

from app.infrastructure.adapters.evidence_platform.advisory_assembler import (
    EvidenceAdvisoryAssembler,
    build_evidence_advisory_assembler,
    deterministic_advisory_id,
    format_period_source_description,
)
from app.infrastructure.adapters.evidence_platform.contracts import (
    AUTHORITY_EVIDENCE_PLATFORM,
    EvidenceFactualSummary,
)


def _summary(**overrides):
    base = dict(
        summary_id="evfact-abc",
        student_id="42",
        reporting_period="this_week",
        completed_missions=2,
        completed_reflections=1,
        study_sessions=2,
        active_streak=2,
        generated_at="2026-08-07T12:00:00+00:00",
        evidence_refs=("ev-1", "ev-2"),
        event_counts={"session_completed": 2, "reflection_completed": 1},
        provenance={"source_service": "evidence_factual_query", "record_count": 3},
        source_description="Based on your recorded study activity.",
    )
    base.update(overrides)
    return EvidenceFactualSummary(**base)


def test_assembler_maps_factual_summary_to_advisory():
    assembler = EvidenceAdvisoryAssembler()
    advisory = assembler.assemble(_summary())
    assert advisory.student_id == "42"
    assert advisory.evidence_summary_id == "evfact-abc"
    assert advisory.engagement_summary.study_sessions == 2
    assert advisory.engagement_summary.completed_missions == 2
    assert advisory.engagement_summary.completed_reflections == 1
    assert advisory.consistency_summary.active_streak == 2
    assert advisory.authority == AUTHORITY_EVIDENCE_PLATFORM
    keys = {p.pattern_key for p in advisory.observed_patterns}
    assert "session_completed" in keys
    assert "reflection_completed" in keys


def test_assembler_preserves_provenance():
    assembler = EvidenceAdvisoryAssembler()
    advisory = assembler.assemble(_summary())
    assert advisory.provenance["evidence_summary_id"] == "evfact-abc"
    assert advisory.provenance["evidence_refs"] == ["ev-1", "ev-2"]
    assert advisory.provenance["evidence_provenance"]["record_count"] == 3
    assert "field_provenance" in advisory.provenance
    for field in (
        "observed_patterns",
        "engagement_summary",
        "consistency_summary",
        "factual_constraints",
    ):
        assert field in advisory.provenance["field_provenance"]
        assert advisory.provenance["field_provenance"][field]


def test_assembler_period_source_description():
    text = format_period_source_description(
        reporting_period="this_week",
        anchor_date=date(2026, 8, 7),
    )
    assert text == (
        "Derived from recorded study activity between 1–7 August."
    )
    assembler = EvidenceAdvisoryAssembler()
    advisory = assembler.assemble(
        _summary(generated_at="2026-08-07T12:00:00+00:00")
    )
    assert "1–7 August" in advisory.source_description
    assert advisory.engagement_summary.source_description == advisory.source_description


def test_assembler_emits_factual_constraints_for_empty_window():
    assembler = EvidenceAdvisoryAssembler()
    advisory = assembler.assemble(
        _summary(
            completed_missions=0,
            study_sessions=0,
            completed_reflections=0,
            active_streak=0,
            evidence_refs=(),
            event_counts={},
        )
    )
    keys = {c.constraint_key for c in advisory.factual_constraints}
    assert "no_study_sessions_in_period" in keys
    assert "no_reflections_in_period" in keys
    assert "empty_evidence_refs" in keys


def test_deterministic_advisory_id():
    a = deterministic_advisory_id(
        student_id="42",
        reporting_period="this_week",
        generated_at="2026-08-07T12:00:00+00:00",
        evidence_summary_id="evfact-abc",
        evidence_refs=("ev-1",),
    )
    b = deterministic_advisory_id(
        student_id="42",
        reporting_period="this_week",
        generated_at="2026-08-07T12:00:00+00:00",
        evidence_summary_id="evfact-abc",
        evidence_refs=("ev-1",),
    )
    assert a == b
    assert a.startswith("evadv-")


def test_build_assembler_respects_flag():
    assert build_evidence_advisory_assembler(enabled=False) is None
    assert isinstance(
        build_evidence_advisory_assembler(enabled=True),
        EvidenceAdvisoryAssembler,
    )


def test_assemble_is_deterministic():
    assembler = EvidenceAdvisoryAssembler()
    summary = _summary()
    first = assembler.assemble(summary)
    second = assembler.assemble(summary)
    assert first.serialize() == second.serialize()
