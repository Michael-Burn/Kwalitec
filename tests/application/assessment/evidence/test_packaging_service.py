"""Application-layer evidence packaging service tests."""

from __future__ import annotations

from application.assessment.evidence import EvidenceMapper, EvidencePackagingService
from domain.assessment import (
    AssessmentObservationFactory,
    EvidenceSource,
    ObservationId,
    ObservationKind,
    QuestionId,
    SessionId,
)
from domain.assessment.packaging.ids import sequential_id_factory
from infrastructure.assessment.composition import build_assessment_delivery


def _obs(oid: str, qid: str):
    return AssessmentObservationFactory.create(
        observation_id=ObservationId(oid),
        session_id=SessionId("sess-app-1"),
        kind=ObservationKind.QUESTION_ANSWERED,
        evidence_source=EvidenceSource.STUDENT_RESPONSE,
        question_id=QuestionId(qid),
        provenance={
            "response_payload": {"selected_option": "b"},
            "confidence": 3,
            "response_time_ms": 1500,
            "hints_used": 0,
            "retries": 0,
        },
    )


def test_evidence_packaging_service_packages_and_exposes_ap001_boundary() -> None:
    composition = build_assessment_delivery(seed=True)
    service = EvidencePackagingService(
        results=composition.results,
        evidence_bundles=composition.evidence_bundles,
        id_factory=sequential_id_factory(),
    )
    result, dto = service.package_observations(
        [_obs("obs-1", "q-1"), _obs("obs-2", "q-2")],
        session_id="sess-app-1",
        instrument_id=composition.default_instrument_id,
        purpose="diagnostic",
        student_id="student-app",
        expected_question_count=2,
        persist_result=True,
    )
    assert dto.validated is True
    assert dto.bundle.session_id == "sess-app-1"
    assert len(dto.bundle.items) == 2
    assert dto.evidence_strength is not None
    exported = service.export_for_ap001(result)
    assert exported is not None
    assert exported.bundle.bundle_id == dto.bundle.bundle_id
    assert composition.results.get_by_session(SessionId("sess-app-1")) is not None
    saved_bundle = composition.evidence_bundles.get_by_session(
        SessionId("sess-app-1")
    )
    assert saved_bundle is not None


def test_evidence_mapper_round_trip_fields() -> None:
    service = EvidencePackagingService(id_factory=sequential_id_factory())
    result, dto = service.package_observations(
        [_obs("obs-x", "q-x"), _obs("obs-y", "q-y")],
        session_id="sess-app-1",
        expected_question_count=2,
    )
    mapped = EvidenceMapper.to_bundle_dto(result.evidence_bundle)  # type: ignore[arg-type]
    assert mapped.observation_ids == dto.bundle.observation_ids
    assert mapped.metadata.packaging_version.startswith("AP-002C")


def test_delivery_complete_attaches_evidence_bundle() -> None:
    from application.assessment.commands.commands import (
        CommitAssessmentResponseCommand,
        CreateAssessmentSessionCommand,
        StartAssessmentSessionCommand,
        SubmitAssessmentSessionCommand,
    )

    composition = build_assessment_delivery(seed=True)
    svc = composition.delivery_service
    student = "student-evidence"
    svc.create_session(
        CreateAssessmentSessionCommand(
            session_id="asess-ev-1",
            student_id=student,
            instrument_id=composition.default_instrument_id,
        )
    )
    svc.start(
        StartAssessmentSessionCommand(session_id="asess-ev-1"),
        student_id=student,
    )
    for qid, payload in (
        ("q-mc-force", {"selected_option": "a"}),
        ("q-numeric-mu", {"entered_value": "0.02"}),
        ("q-confidence-mu", {"confidence": 4}),
        ("q-reflection-mu", {"reflection_text": "Still learning."}),
    ):
        svc.commit_response(
            CommitAssessmentResponseCommand(
                session_id="asess-ev-1",
                question_id=qid,
                response_payload=payload,
                confidence=4 if qid.startswith("q-confidence") else None,
                response_time_ms=1000,
            ),
            student_id=student,
        )
    completed = svc.complete(
        SubmitAssessmentSessionCommand(session_id="asess-ev-1"),
        student_id=student,
    )
    assert completed.result is not None
    assert completed.result.evidence_strength is not None
    assert completed.result.evidence_bundle is not None
    assert completed.result.evidence_bundle.evidence_strength == (
        completed.result.evidence_strength
    )
