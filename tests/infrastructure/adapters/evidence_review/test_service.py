"""Evidence Query Service tests (P4-MS003)."""

from __future__ import annotations

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.evidence_review import (
    EXPORT_FORMAT_CSV,
    EXPORT_FORMAT_JSON,
    INVALID_STATE,
    UNAVAILABLE,
    EvidenceQueryService,
    EvidenceReviewFilter,
    build_evidence_query_service,
    content_digest,
)
from app.infrastructure.adapters.longitudinal_evidence import (
    APPROVED_ADVISORY_FIELD,
    EVENT_ADVISORY_ACTIVATION,
    EVENT_MISSION,
    EVENT_REFLECTION,
    EVENT_STUDY_SESSION,
    SOURCE_CONTROLLED_ADVISORY,
    SOURCE_EDUCATIONAL_TRIAL,
    SOURCE_UNIFIED_JOURNEY,
    InMemoryLongitudinalEvidenceRepository,
    build_provenance,
    make_record,
    opaque_student_id_hash,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.diagnostics.dual_run import build_dual_run_status


def _seed_repo() -> InMemoryLongitudinalEvidenceRepository:
    repo = InMemoryLongitudinalEvidenceRepository(enabled=True)
    records = [
        make_record(
            record_id="lerec-a",
            student_id_hash=opaque_student_id_hash("student-1"),
            event_type=EVENT_STUDY_SESSION,
            event_timestamp="2026-07-25T08:00:00+00:00",
            source_component=SOURCE_UNIFIED_JOURNEY,
            policy_version="p3.ms004.1",
            advisory_field=APPROVED_ADVISORY_FIELD,
            trial_id="trial-alpha",
            provenance=build_provenance(
                originating_component=SOURCE_UNIFIED_JOURNEY,
                policy_version="p3.ms004.1",
                feature_flags={
                    "ENABLE_LONGITUDINAL_EVIDENCE": True,
                    "ENABLE_POLICY_WEIGHTING": True,
                },
                trial_context={"trial_id": "trial-alpha", "cohort": "treatment"},
                advisory_provenance={"field": APPROVED_ADVISORY_FIELD},
                collected_at="2026-07-25T08:00:00+00:00",
            ),
        ),
        make_record(
            record_id="lerec-b",
            student_id_hash=opaque_student_id_hash("student-1"),
            event_type=EVENT_MISSION,
            event_timestamp="2026-07-25T10:00:00+00:00",
            source_component=SOURCE_UNIFIED_JOURNEY,
            policy_version="p3.ms004.1",
            advisory_field=APPROVED_ADVISORY_FIELD,
            trial_id="trial-alpha",
            provenance=build_provenance(
                originating_component=SOURCE_UNIFIED_JOURNEY,
                policy_version="p3.ms004.1",
                feature_flags={"ENABLE_LONGITUDINAL_EVIDENCE": True},
                trial_context={"trial_id": "trial-alpha", "cohort": "control"},
                collected_at="2026-07-25T10:00:00+00:00",
            ),
        ),
        make_record(
            record_id="lerec-c",
            student_id_hash=opaque_student_id_hash("student-2"),
            event_type=EVENT_REFLECTION,
            event_timestamp="2026-07-25T12:00:00+00:00",
            source_component=SOURCE_UNIFIED_JOURNEY,
            policy_version="p3.ms003.1",
            trial_id="trial-beta",
            provenance=build_provenance(
                originating_component=SOURCE_UNIFIED_JOURNEY,
                policy_version="p3.ms003.1",
                feature_flags={"ENABLE_LONGITUDINAL_EVIDENCE": True},
                trial_context={"trial_id": "trial-beta"},
                collected_at="2026-07-25T12:00:00+00:00",
            ),
        ),
        make_record(
            record_id="lerec-d",
            student_id_hash=opaque_student_id_hash("student-2"),
            event_type=EVENT_ADVISORY_ACTIVATION,
            event_timestamp="2026-07-26T09:00:00+00:00",
            source_component=SOURCE_CONTROLLED_ADVISORY,
            policy_version="p3.ms004.1",
            advisory_field=APPROVED_ADVISORY_FIELD,
            trial_id="trial-alpha",
            provenance=build_provenance(
                originating_component=SOURCE_CONTROLLED_ADVISORY,
                policy_version="p3.ms004.1",
                feature_flags={
                    "ENABLE_LONGITUDINAL_EVIDENCE": True,
                    "ENABLE_CONTROLLED_ADVISORY": True,
                },
                trial_context={"trial_id": "trial-alpha"},
                advisory_provenance={"field": APPROVED_ADVISORY_FIELD},
                collected_at="2026-07-26T09:00:00+00:00",
            ),
        ),
        make_record(
            record_id="lerec-e",
            student_id_hash=opaque_student_id_hash("student-3"),
            event_type=EVENT_STUDY_SESSION,
            event_timestamp="2026-07-24T09:00:00+00:00",
            source_component=SOURCE_EDUCATIONAL_TRIAL,
            policy_version="p3.ms004.1",
            trial_id="trial-gamma",
            provenance=build_provenance(
                originating_component=SOURCE_EDUCATIONAL_TRIAL,
                policy_version="p3.ms004.1",
                feature_flags={"ENABLE_EDUCATIONAL_TRIALS": True},
                trial_context={"trial_id": "trial-gamma"},
                collected_at="2026-07-24T09:00:00+00:00",
            ),
        ),
    ]
    for item in records:
        assert repo.append(item).ok is True
    return repo


def _service(
    repo: InMemoryLongitudinalEvidenceRepository | None = None,
    *,
    enabled: bool = True,
) -> EvidenceQueryService:
    return EvidenceQueryService(
        enabled=enabled,
        repository=repo if repo is not None else _seed_repo(),
    )


def test_evidence_review_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_EVIDENCE_REVIEW is False
    dual = build_dual_run_status(flags=flags)
    assert dual.evidence_review is False


def test_evidence_review_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EVIDENCE_REVIEW": "1"}
    )
    assert flags.ENABLE_EVIDENCE_REVIEW is True
    dual = build_dual_run_status(flags=flags)
    assert dual.evidence_review is True


def test_evidence_review_flag_is_independent():
    longitudinal_only = resolve_v2_feature_flags(
        environ={"KWALITEC_LONGITUDINAL_EVIDENCE": "1"}
    )
    assert longitudinal_only.ENABLE_LONGITUDINAL_EVIDENCE is True
    assert longitudinal_only.ENABLE_EVIDENCE_REVIEW is False

    review_only = resolve_v2_feature_flags(
        environ={"KWALITEC_EVIDENCE_REVIEW": "1"}
    )
    assert review_only.ENABLE_EVIDENCE_REVIEW is True
    assert review_only.ENABLE_LONGITUDINAL_EVIDENCE is False
    assert review_only.ENABLE_EDUCATIONAL_TRIALS is False
    assert review_only.ENABLE_EVIDENCE_PLATFORM is False
    assert review_only.ENABLE_POLICY_WEIGHTING is False
    assert review_only.ENABLE_ADAPTIVE_ENGINE is False
    assert review_only.ENABLE_RECOMMENDATION_POLICY is False


def test_query_by_time_window_event_type_policy_trial_advisory():
    service = _service()

    window = service.query_by_time_window(
        start_timestamp="2026-07-25T09:00:00+00:00",
        end_timestamp="2026-07-25T13:00:00+00:00",
    )
    assert window.ok is True
    assert [item.record_id for item in window.records] == ["lerec-b", "lerec-c"]

    by_type = service.query_by_event_type(EVENT_MISSION)
    assert [item.record_id for item in by_type.records] == ["lerec-b"]

    by_policy = service.query_by_policy_version("p3.ms004.1")
    assert [item.record_id for item in by_policy.records] == [
        "lerec-a",
        "lerec-b",
        "lerec-d",
        "lerec-e",
    ]

    by_trial = service.query_by_trial("trial-beta")
    assert [item.record_id for item in by_trial.records] == ["lerec-c"]

    by_advisory = service.query_by_advisory_field(APPROVED_ADVISORY_FIELD)
    assert [item.record_id for item in by_advisory.records] == [
        "lerec-a",
        "lerec-b",
        "lerec-d",
    ]


def test_combined_filtering_including_feature_flag():
    service = _service()
    result = service.filter(
        EvidenceReviewFilter(
            policy_version="p3.ms004.1",
            trial_id="trial-alpha",
            event_type=EVENT_STUDY_SESSION,
            feature_flag="ENABLE_POLICY_WEIGHTING",
            feature_flag_value=True,
        )
    )
    assert result.ok is True
    assert [item.record_id for item in result.records] == ["lerec-a"]

    flag_only = service.filter(
        EvidenceReviewFilter(
            feature_flag="ENABLE_CONTROLLED_ADVISORY",
            feature_flag_value=True,
        )
    )
    assert [item.record_id for item in flag_only.records] == ["lerec-d"]


def test_filter_rejects_inverted_time_window():
    service = _service()
    result = service.filter(
        EvidenceReviewFilter(
            start_timestamp="2026-07-26T00:00:00+00:00",
            end_timestamp="2026-07-25T00:00:00+00:00",
        )
    )
    assert result.ok is False
    assert result.error_code == INVALID_STATE
    assert result.message == "time_window_start_after_end"


def test_timeline_construction_preserves_provenance_summary():
    service = _service()
    result = service.build_timeline(
        EvidenceReviewFilter(trial_id="trial-alpha")
    )
    assert result.ok is True
    timeline = result.timeline
    assert timeline is not None
    assert timeline.read_only is True
    assert timeline.observation_count == 3
    assert timeline.time_window.start_timestamp == "2026-07-25T08:00:00+00:00"
    assert timeline.time_window.end_timestamp == "2026-07-26T09:00:00+00:00"
    assert [group.event_type for group in timeline.event_groups] == [
        EVENT_ADVISORY_ACTIVATION,
        EVENT_MISSION,
        EVENT_STUDY_SESSION,
    ]
    summary = timeline.provenance_summary
    assert "unified_journey" in summary.originating_components
    assert "controlled_advisory" in summary.originating_components
    assert "p3.ms004.1" in summary.policy_versions
    assert "trial-alpha" in summary.trial_ids
    assert APPROVED_ADVISORY_FIELD in summary.advisory_fields
    assert summary.feature_flags_observed["ENABLE_LONGITUDINAL_EVIDENCE"] is True
    assert timeline.record_ids == ("lerec-a", "lerec-b", "lerec-d")

    # Deterministic timeline id for identical inputs.
    again = service.build_timeline(
        EvidenceReviewFilter(trial_id="trial-alpha")
    )
    assert again.timeline is not None
    assert again.timeline.timeline_id == timeline.timeline_id
    assert again.timeline.serialize() == timeline.serialize()


def test_json_and_csv_exports_are_reproducible():
    service = _service()
    filt = EvidenceReviewFilter(policy_version="p3.ms004.1", trial_id="trial-alpha")

    first_json = service.export(filt, format=EXPORT_FORMAT_JSON)
    second_json = service.export(filt, format=EXPORT_FORMAT_JSON)
    assert first_json.ok is True
    assert second_json.ok is True
    assert first_json.export is not None
    assert second_json.export is not None
    assert first_json.export.content == second_json.export.content
    assert first_json.export.export_id == second_json.export.export_id
    assert first_json.export.content_digest == content_digest(
        first_json.export.content
    )
    assert first_json.export.reproducible is True
    assert first_json.export.read_only is True
    assert '"record_id":"lerec-a"' in first_json.export.content

    first_csv = service.export(filt, format=EXPORT_FORMAT_CSV)
    second_csv = service.export(filt, format=EXPORT_FORMAT_CSV)
    assert first_csv.export is not None
    assert second_csv.export is not None
    assert first_csv.export.content == second_csv.export.content
    assert first_csv.export.export_id == second_csv.export.export_id
    assert first_csv.export.content.startswith("record_id,")
    assert "lerec-a" in first_csv.export.content
    assert first_csv.export.format == EXPORT_FORMAT_CSV


def test_export_rejects_unsupported_format():
    service = _service()
    result = service.export(format="xml")
    assert result.ok is False
    assert result.error_code == INVALID_STATE
    assert result.message == "export_format_unsupported"


def test_service_disabled_returns_unavailable():
    service = _service(enabled=False)
    result = service.query_by_event_type(EVENT_MISSION)
    assert result.ok is False
    assert result.error_code == UNAVAILABLE
    assert result.message == "ENABLE_EVIDENCE_REVIEW is OFF"


def test_service_without_repository_returns_unavailable():
    service = EvidenceQueryService(enabled=True, repository=None)
    result = service.filter()
    assert result.ok is False
    assert result.error_code == UNAVAILABLE
    assert result.message == "longitudinal_evidence_repository_unavailable"


def test_disabled_repository_returns_unavailable():
    repo = InMemoryLongitudinalEvidenceRepository(enabled=False)
    service = EvidenceQueryService(enabled=True, repository=repo)
    result = service.query_by_trial("trial-alpha")
    assert result.ok is False
    assert result.error_code == UNAVAILABLE
    assert result.message == "ENABLE_LONGITUDINAL_EVIDENCE is OFF"


def test_repository_remains_read_only_through_review_service():
    repo = _seed_repo()
    before = repo.count()
    service = EvidenceQueryService(enabled=True, repository=repo)
    assert service.filter().ok is True
    assert service.build_timeline().ok is True
    assert service.export().ok is True
    assert repo.count() == before
    # Service exposes no mutation API.
    assert not hasattr(service, "append")
    assert not hasattr(service, "update")
    assert not hasattr(service, "delete")


def test_build_evidence_query_service_returns_none_when_disabled():
    assert build_evidence_query_service(enabled=False) is None
    built = build_evidence_query_service(enabled=True, repository=_seed_repo())
    assert built is not None
    assert built.is_enabled() is True


def test_composition_wires_review_only_when_flag_on(ctx):
    off_composition, _ = build_production_experience(
        flags=resolve_v2_feature_flags(environ={})
    )
    assert off_composition.evidence_review is None
    assert off_composition.longitudinal_evidence is None

    review_only, _ = build_production_experience(
        flags=resolve_v2_feature_flags(
            environ={"KWALITEC_EVIDENCE_REVIEW": "1"}
        )
    )
    assert review_only.evidence_review is not None
    assert review_only.evidence_review.is_enabled() is True
    # Independent: review ON without longitudinal store → gated unavailable.
    assert review_only.longitudinal_evidence is None
    gated = review_only.evidence_review.filter()
    assert gated.ok is False
    assert gated.error_code == UNAVAILABLE

    both, _ = build_production_experience(
        flags=resolve_v2_feature_flags(
            environ={
                "KWALITEC_EVIDENCE_REVIEW": "1",
                "KWALITEC_LONGITUDINAL_EVIDENCE": "1",
            }
        )
    )
    assert both.evidence_review is not None
    assert both.longitudinal_evidence is not None
    assert both.evidence_review.repository is both.longitudinal_evidence
    # Independent: does not enable trials / policy / adaptive.
    assert both.educational_trial is None
