"""Evidence review contract tests (P4-MS003)."""

from __future__ import annotations

from app.infrastructure.adapters.evidence_review import (
    AUTHORITY_EVIDENCE_REVIEW,
    AUTHORITY_RUNTIME_A,
    CSV_COLUMNS,
    EVIDENCE_REVIEW_SCHEMA_VERSION,
    EXPORT_FORMAT_CSV,
    EXPORT_FORMAT_JSON,
    EXPORT_FORMATS,
    EvidenceEventGroup,
    EvidenceProvenanceSummary,
    EvidenceReviewExport,
    EvidenceReviewFilter,
    EvidenceReviewResult,
    EvidenceTimeline,
    EvidenceTimeWindow,
    serialize_canonical,
)


def test_filter_normalises_and_serialises_deterministically():
    filt = EvidenceReviewFilter(
        start_timestamp=" 2026-07-25T00:00:00+00:00 ",
        end_timestamp="2026-07-26T00:00:00+00:00",
        event_type=" mission ",
        policy_version=" p3.ms004.1 ",
        trial_id=" trial-a ",
        advisory_field=" consistency_summary ",
        feature_flag=" ENABLE_LONGITUDINAL_EVIDENCE ",
        feature_flag_value=True,
    )
    assert filt.start_timestamp == "2026-07-25T00:00:00+00:00"
    assert filt.event_type == "mission"
    first = filt.serialize()
    second = EvidenceReviewFilter(**filt.to_canonical_dict()).serialize()
    assert first == second
    assert "advisory_field" in first


def test_timeline_is_immutable_and_read_only():
    timeline = EvidenceTimeline(
        timeline_id="evtl-test",
        observation_count=2,
        time_window=EvidenceTimeWindow(
            start_timestamp="2026-07-25T08:00:00+00:00",
            end_timestamp="2026-07-25T12:00:00+00:00",
        ),
        event_groups=(
            EvidenceEventGroup(
                event_type="mission",
                observation_count=1,
                record_ids=("a",),
            ),
            EvidenceEventGroup(
                event_type="study_session",
                observation_count=1,
                record_ids=("b",),
            ),
        ),
        provenance_summary=EvidenceProvenanceSummary(
            originating_components=("unified_journey",),
            policy_versions=("p3.ms004.1",),
            trial_ids=("trial-a",),
            advisory_fields=("consistency_summary",),
            feature_flags_observed={"ENABLE_LONGITUDINAL_EVIDENCE": True},
            schema_versions=("p4.ms002.1",),
        ),
        record_ids=("a", "b"),
        filter_snapshot={"event_type": "mission"},
    )
    assert timeline.read_only is True
    assert timeline.authority == AUTHORITY_EVIDENCE_REVIEW
    assert timeline.schema_version == EVIDENCE_REVIEW_SCHEMA_VERSION
    assert timeline.serialize() == serialize_canonical(timeline.to_canonical_dict())


def test_export_contract_defaults_and_formats():
    assert EXPORT_FORMAT_JSON in EXPORT_FORMATS
    assert EXPORT_FORMAT_CSV in EXPORT_FORMATS
    assert "record_id" in CSV_COLUMNS
    export = EvidenceReviewExport(
        export_id="evexp-test",
        format="csv",
        content="record_id\n",
        record_count=0,
        content_digest="abc",
    )
    assert export.read_only is True
    assert export.reproducible is True
    assert export.format == EXPORT_FORMAT_CSV
    # Unknown format coerced to json for contract safety.
    coerced = EvidenceReviewExport(format="xml")
    assert coerced.format == EXPORT_FORMAT_JSON


def test_result_envelope_serialises_nested_artefacts():
    result = EvidenceReviewResult(
        ok=True,
        timeline=EvidenceTimeline(timeline_id="evtl-x"),
        export=EvidenceReviewExport(export_id="evexp-x", content="{}"),
        filter_snapshot={"trial_id": "t1"},
    )
    payload = result.to_canonical_dict()
    assert payload["ok"] is True
    assert payload["timeline"]["timeline_id"] == "evtl-x"
    assert payload["export"]["export_id"] == "evexp-x"
    assert AUTHORITY_RUNTIME_A != AUTHORITY_EVIDENCE_REVIEW
