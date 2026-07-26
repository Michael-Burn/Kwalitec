"""Longitudinal evidence repository tests (P4-MS002)."""

from __future__ import annotations

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.longitudinal_evidence import (
    APPEND_ONLY_VIOLATION,
    APPROVED_ADVISORY_FIELD,
    EVENT_ADVISORY_ACTIVATION,
    EVENT_MISSION,
    EVENT_REFLECTION,
    EVENT_STUDY_SESSION,
    INVALID_STATE,
    LONGITUDINAL_EVIDENCE_SCHEMA_VERSION,
    SCHEMA_INCOMPATIBLE,
    SOURCE_CONTROLLED_ADVISORY,
    SOURCE_EDUCATIONAL_TRIAL,
    SOURCE_UNIFIED_JOURNEY,
    UNAVAILABLE,
    InMemoryLongitudinalEvidenceRepository,
    LearningEvidenceRecord,
    LongitudinalEvidenceRepository,
    build_longitudinal_evidence_repository,
    build_provenance,
    make_record,
    opaque_student_id_hash,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.diagnostics.dual_run import build_dual_run_status


def _sample_record(
    *,
    record_id: str = "lerec-sample",
    event_type: str = EVENT_STUDY_SESSION,
    event_timestamp: str = "2026-07-25T10:00:00+00:00",
    policy_version: str = "p3.ms004.1",
    source_component: str = SOURCE_UNIFIED_JOURNEY,
    trial_id: str = "educational-trial-p4-ms001",
) -> LearningEvidenceRecord:
    return make_record(
        record_id=record_id,
        student_id_hash=opaque_student_id_hash("student-42"),
        event_type=event_type,
        event_timestamp=event_timestamp,
        source_component=source_component,
        policy_version=policy_version,
        advisory_field=APPROVED_ADVISORY_FIELD,
        trial_id=trial_id,
        provenance=build_provenance(
            originating_component=source_component,
            policy_version=policy_version,
            feature_flags={"ENABLE_LONGITUDINAL_EVIDENCE": True},
            trial_context={"trial_id": trial_id, "cohort": "treatment"},
            advisory_provenance={"field": APPROVED_ADVISORY_FIELD},
            collected_at=event_timestamp,
        ),
    )


def test_longitudinal_evidence_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_LONGITUDINAL_EVIDENCE is False
    dual = build_dual_run_status(flags=flags)
    assert dual.longitudinal_evidence is False


def test_longitudinal_evidence_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_LONGITUDINAL_EVIDENCE": "1"}
    )
    assert flags.ENABLE_LONGITUDINAL_EVIDENCE is True
    dual = build_dual_run_status(flags=flags)
    assert dual.longitudinal_evidence is True


def test_longitudinal_evidence_flag_is_independent():
    trial_only = resolve_v2_feature_flags(
        environ={"KWALITEC_EDUCATIONAL_TRIALS": "1"}
    )
    assert trial_only.ENABLE_EDUCATIONAL_TRIALS is True
    assert trial_only.ENABLE_LONGITUDINAL_EVIDENCE is False

    evidence_only = resolve_v2_feature_flags(
        environ={"KWALITEC_LONGITUDINAL_EVIDENCE": "1"}
    )
    assert evidence_only.ENABLE_LONGITUDINAL_EVIDENCE is True
    assert evidence_only.ENABLE_EDUCATIONAL_TRIALS is False
    assert evidence_only.ENABLE_EVIDENCE_PLATFORM is False
    assert evidence_only.ENABLE_POLICY_WEIGHTING is False
    assert evidence_only.ENABLE_ADAPTIVE_ENGINE is False


def test_repository_protocol_satisfied_by_in_memory():
    repo = InMemoryLongitudinalEvidenceRepository(enabled=True)
    assert isinstance(repo, LongitudinalEvidenceRepository)


def test_append_and_retrieve_by_record_id():
    repo = InMemoryLongitudinalEvidenceRepository(enabled=True)
    record = _sample_record()
    result = repo.append(record)
    assert result.ok is True
    assert result.record is not None
    assert result.record.record_id == "lerec-sample"
    assert repo.count() == 1

    fetched = repo.get_by_record_id("lerec-sample")
    assert fetched.ok is True
    assert fetched.record is not None
    assert fetched.record.serialize() == record.serialize()


def test_append_only_rejects_duplicate_record_id():
    repo = InMemoryLongitudinalEvidenceRepository(enabled=True)
    first = _sample_record(record_id="lerec-dup")
    assert repo.append(first).ok is True

    mutated = _sample_record(
        record_id="lerec-dup",
        event_type=EVENT_MISSION,
        event_timestamp="2026-07-25T11:00:00+00:00",
    )
    second = repo.append(mutated)
    assert second.ok is False
    assert second.error_code == APPEND_ONLY_VIOLATION
    assert repo.count() == 1
    assert repo.get_by_record_id("lerec-dup").record.event_type == EVENT_STUDY_SESSION


def test_retrieval_by_time_window_event_type_and_policy_version():
    repo = InMemoryLongitudinalEvidenceRepository(enabled=True)
    records = [
        _sample_record(
            record_id="lerec-a",
            event_type=EVENT_STUDY_SESSION,
            event_timestamp="2026-07-25T08:00:00+00:00",
            policy_version="p3.ms004.1",
        ),
        _sample_record(
            record_id="lerec-b",
            event_type=EVENT_MISSION,
            event_timestamp="2026-07-25T10:00:00+00:00",
            policy_version="p3.ms004.1",
        ),
        _sample_record(
            record_id="lerec-c",
            event_type=EVENT_REFLECTION,
            event_timestamp="2026-07-25T12:00:00+00:00",
            policy_version="p3.ms003.1",
        ),
        _sample_record(
            record_id="lerec-d",
            event_type=EVENT_ADVISORY_ACTIVATION,
            event_timestamp="2026-07-26T09:00:00+00:00",
            policy_version="p3.ms004.1",
            source_component=SOURCE_CONTROLLED_ADVISORY,
        ),
    ]
    for item in records:
        assert repo.append(item).ok is True

    window = repo.get_by_time_window(
        start_timestamp="2026-07-25T09:00:00+00:00",
        end_timestamp="2026-07-25T13:00:00+00:00",
    )
    assert window.ok is True
    assert [item.record_id for item in window.records] == ["lerec-b", "lerec-c"]

    by_type = repo.get_by_event_type(EVENT_MISSION)
    assert [item.record_id for item in by_type.records] == ["lerec-b"]

    by_policy = repo.get_by_policy_version("p3.ms004.1")
    assert [item.record_id for item in by_policy.records] == [
        "lerec-a",
        "lerec-b",
        "lerec-d",
    ]

    by_trial = repo.get_by_trial_id("educational-trial-p4-ms001")
    assert [item.record_id for item in by_trial.records] == [
        "lerec-a",
        "lerec-b",
        "lerec-c",
        "lerec-d",
    ]

    by_advisory = repo.get_by_advisory_field(APPROVED_ADVISORY_FIELD)
    assert [item.record_id for item in by_advisory.records] == [
        "lerec-a",
        "lerec-b",
        "lerec-c",
        "lerec-d",
    ]

    listed = repo.list_all()
    assert listed.ok is True
    assert [item.record_id for item in listed.records] == [
        "lerec-a",
        "lerec-b",
        "lerec-c",
        "lerec-d",
    ]


def test_provenance_preserved_on_append():
    repo = InMemoryLongitudinalEvidenceRepository(enabled=True)
    record = _sample_record(
        record_id="lerec-prov",
        source_component=SOURCE_EDUCATIONAL_TRIAL,
    )
    stored = repo.append(record).record
    assert stored is not None
    assert stored.provenance.originating_component == SOURCE_EDUCATIONAL_TRIAL
    assert stored.provenance.policy_version == "p3.ms004.1"
    assert stored.provenance.feature_flags["ENABLE_LONGITUDINAL_EVIDENCE"] is True
    assert stored.provenance.trial_context["cohort"] == "treatment"
    assert stored.provenance.advisory_provenance["field"] == APPROVED_ADVISORY_FIELD


def test_schema_compatibility_reject_unknown_version():
    repo = InMemoryLongitudinalEvidenceRepository(enabled=True)
    record = LearningEvidenceRecord(
        record_id="lerec-schema",
        student_id_hash="stuhash-x",
        event_type=EVENT_STUDY_SESSION,
        event_timestamp="2026-07-25T10:00:00+00:00",
        source_component=SOURCE_UNIFIED_JOURNEY,
        provenance=build_provenance(originating_component=SOURCE_UNIFIED_JOURNEY),
        schema_version="p4.ms999.0",
    )
    # LearningEvidenceRecord keeps the provided schema string for evolution checks.
    assert record.schema_version == "p4.ms999.0"
    result = repo.append(record)
    assert result.ok is False
    assert result.error_code in {SCHEMA_INCOMPATIBLE, INVALID_STATE}
    assert result.message == "schema_version_unsupported"


def test_schema_compatible_current_version_appends():
    repo = InMemoryLongitudinalEvidenceRepository(enabled=True)
    record = _sample_record(record_id="lerec-schema-ok")
    assert record.schema_version == LONGITUDINAL_EVIDENCE_SCHEMA_VERSION
    assert repo.append(record).ok is True


def test_disabled_repository_rejects_traffic():
    repo = InMemoryLongitudinalEvidenceRepository(enabled=False)
    result = repo.append(_sample_record())
    assert result.ok is False
    assert result.error_code == UNAVAILABLE
    assert repo.get_by_event_type(EVENT_STUDY_SESSION).error_code == UNAVAILABLE


def test_build_repository_returns_none_when_disabled():
    assert build_longitudinal_evidence_repository(enabled=False) is None
    built = build_longitudinal_evidence_repository(enabled=True)
    assert built is not None
    assert built.is_enabled() is True


def test_composition_wires_repository_only_when_flag_on(ctx):
    off_composition, _ = build_production_experience(
        flags=resolve_v2_feature_flags(environ={})
    )
    assert off_composition.longitudinal_evidence is None

    on_composition, _ = build_production_experience(
        flags=resolve_v2_feature_flags(
            environ={"KWALITEC_LONGITUDINAL_EVIDENCE": "1"}
        )
    )
    assert on_composition.longitudinal_evidence is not None
    assert on_composition.longitudinal_evidence.is_enabled() is True
    # Independent: longitudinal evidence ON does not enable trial / Runtime A gates.
    assert on_composition.educational_trial is None


def test_opaque_student_hash_is_stable_and_non_identifying():
    first = opaque_student_id_hash("learner-7")
    second = opaque_student_id_hash("learner-7")
    assert first == second
    assert first.startswith("stuhash-")
    assert "learner-7" not in first
