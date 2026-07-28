"""Evidence ingress service integration tests (AP-002D1)."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from app.application.assessment_pipeline.evidence_ingress import (
    INGRESS_TRIGGERED_BY,
    DuplicateEvidenceSubmission,
    EvidenceIngressRequest,
    EvidenceIngressService,
    IncompleteEvidenceBundle,
    InMemoryEvidenceSubmissionRepository,
    InvalidEvidenceBundle,
    UnsupportedEvidenceVersion,
)
from app.application.student_digital_twin.observation_service import ObservationService
from app.application.student_digital_twin.student_digital_twin_service import (
    StudentDigitalTwinService,
)
from app.application.student_digital_twin.student_reasoning_service import (
    StudentReasoningService,
)
from app.domain.curriculum_retrieval.intent import QueryIntent
from app.domain.curriculum_retrieval.profile import RetrievalProfile
from app.domain.curriculum_retrieval.ranking import RankingBreakdown
from app.domain.curriculum_retrieval.result import (
    EvidenceItem,
    RankedEvidence,
    RetrievalResult,
)
from app.domain.student_digital_twin.observation import ObservationKind
from tests.application.assessment_pipeline.evidence_ingress.conftest import make_bundle


def _ranking() -> RankingBreakdown:
    return RankingBreakdown(
        semantic_similarity=0.5,
        graph_proximity=0.8,
        confidence=0.9,
        founder_verification=1.0,
        document_version=0.5,
        entity_freshness=0.5,
        relationship_strength=0.7,
        evidence_count=0.5,
        rank_score=0.88,
    )


def _make_retrieval_stub(*, concept_id: str = "concept-bayes") -> MagicMock:
    stub = MagicMock()
    evidence = (
        EvidenceItem(
            evidence_id="ev-ingress-1",
            role="definition",
            excerpt="Bayes theorem definition",
            entity_id=concept_id,
        ),
    )
    ranked = RankedEvidence(
        entity_id=concept_id,
        kind="concept",
        title="Bayes Theorem",
        body="definition",
        document_id=1,
        version_label="2026",
        confidence=0.9,
        confidence_band="high",
        verified=True,
        provenance_id="prov-ingress-1",
        rank_score=0.88,
        ranking=_ranking(),
        evidence=evidence,
        prerequisites=(),
        related_concepts=(),
        supporting_formulae=(),
        worked_examples=(),
        practice_questions=(),
        learning_objectives=(),
    )
    stub.retrieve.return_value = RetrievalResult(
        query_text=concept_id,
        intent=QueryIntent.DEFINITION,
        profile=RetrievalProfile.MISSION_ENGINE,
        results=(ranked,),
        concept_ids=(concept_id,),
        learning_objective_ids=(),
        definition_ids=(),
        formula_ids=(),
        example_ids=(),
        practice_question_ids=(),
        prerequisite_ids=(),
        related_concept_ids=(),
        retrieval_log_id="rl-ingress-1",
    )
    return stub


@pytest.fixture
def twin(ctx):
    return StudentDigitalTwinService().create(
        student_id="student-ingress-1",
        display_name="Ingress Student",
        subject_code="CS1",
        workspace_id="ws-ingress",
        twin_id="twin-ingress-1",
    )


@pytest.fixture
def reasoning(ctx):
    return StudentReasoningService(retrieval=_make_retrieval_stub())


@pytest.fixture
def ingress(reasoning) -> EvidenceIngressService:
    return EvidenceIngressService(
        reasoning=reasoning,
        submissions=InMemoryEvidenceSubmissionRepository(),
    )


def test_accept_maps_and_reasons_via_existing_pipeline(ctx, twin, ingress) -> None:
    bundle = make_bundle(bundle_id="bundle-ok")
    result = ingress.accept(
        EvidenceIngressRequest(
            twin_id=twin.twin_id,
            bundle=bundle,
            correlation_id="corr-ok",
            reasoning_request_id="rrq-pref",
        ),
        twin=twin,
        persist=True,
        reason=True,
    )
    assert result.twin_id == twin.twin_id
    assert result.triggered_by == INGRESS_TRIGGERED_BY
    assert result.twin_observation_ids == ("obs-1", "obs-2")
    assert result.traceability.assessment_session_id == "sess-1"
    assert result.traceability.evidence_bundle_id == "bundle-ok"
    assert result.traceability.correlation_id == "corr-ok"
    assert result.traceability.reasoning_request_id
    assert result.traceability.question_references
    assert result.traceability.learning_objective_references == ("lo-1",)

    reloaded = StudentDigitalTwinService().get(twin.twin_id)
    assert reloaded is not None
    assert len(reloaded.observations) >= 2
    assert any(
        o.observation_id == "obs-1" and o.kind is ObservationKind.QUESTION_ANSWERED
        for o in reloaded.observations
    )
    assert reloaded.reasoning_history
    assert reloaded.reasoning_history[-1].triggered_by == INGRESS_TRIGGERED_BY
    for obs in reloaded.observations:
        if obs.observation_id in {"obs-1", "obs-2"}:
            assert obs.metadata["correlation_id"] == "corr-ok"
            assert obs.metadata["evidence_bundle_id"] == "bundle-ok"


def test_duplicate_bundle_rejected(ctx, twin, ingress) -> None:
    request = EvidenceIngressRequest(
        twin_id=twin.twin_id,
        bundle=make_bundle(bundle_id="bundle-dup"),
        correlation_id="corr-1",
    )
    ingress.accept(request, twin=twin, persist=True, reason=True)
    twin2 = StudentDigitalTwinService().get(twin.twin_id)
    with pytest.raises(DuplicateEvidenceSubmission, match="bundle-dup"):
        ingress.accept(request, twin=twin2, persist=True, reason=True)


def test_unsupported_version_rejected(ctx, twin, ingress) -> None:
    with pytest.raises(UnsupportedEvidenceVersion):
        ingress.accept(
            EvidenceIngressRequest(
                twin_id=twin.twin_id,
                bundle=make_bundle(packaging_version="NOPE.0"),
                correlation_id="corr-v",
            ),
            twin=twin,
            persist=False,
            reason=False,
        )


def test_missing_correlation_rejected(ctx, twin, ingress) -> None:
    with pytest.raises(IncompleteEvidenceBundle, match="correlation_id"):
        ingress.accept(
            EvidenceIngressRequest(
                twin_id=twin.twin_id,
                bundle=make_bundle(),
                correlation_id="",
            ),
            twin=twin,
            persist=False,
            reason=False,
        )


def test_missing_twin_rejected(ctx, ingress) -> None:
    with pytest.raises(InvalidEvidenceBundle, match="not found"):
        ingress.accept(
            EvidenceIngressRequest(
                twin_id="twin-missing",
                bundle=make_bundle(),
                correlation_id="corr-x",
            ),
            persist=False,
            reason=False,
        )


def test_accept_without_reason_appends_facts_only(ctx, twin, ingress) -> None:
    before = len(twin.reasoning_history)
    result = ingress.accept(
        EvidenceIngressRequest(
            twin_id=twin.twin_id,
            bundle=make_bundle(bundle_id="bundle-facts"),
            correlation_id="corr-facts",
        ),
        twin=twin,
        persist=True,
        reason=False,
    )
    assert result.twin_observation_ids == ("obs-1", "obs-2")
    reloaded = StudentDigitalTwinService().get(twin.twin_id)
    assert reloaded is not None
    assert len(reloaded.observations) >= 2
    assert len(reloaded.reasoning_history) == before


def test_student_reasoning_service_entry_point(ctx, twin, reasoning) -> None:
    submissions = InMemoryEvidenceSubmissionRepository()
    result = reasoning.accept_assessment_evidence(
        twin,
        bundle=make_bundle(bundle_id="bundle-entry"),
        correlation_id="corr-entry",
        persist=True,
        submissions=submissions,
    )
    assert result.traceability.evidence_bundle_id == "bundle-entry"
    assert result.triggered_by == INGRESS_TRIGGERED_BY
    reloaded = StudentDigitalTwinService().get(twin.twin_id)
    assert reloaded is not None
    assert reloaded.reasoning_history[-1].triggered_by == INGRESS_TRIGGERED_BY


def test_regression_existing_reason_unchanged(ctx, twin, reasoning) -> None:
    """Existing reason() path still works without evidence ingress."""
    twin, _ = ObservationService().record(
        twin,
        kind=ObservationKind.QUESTION_ANSWERED,
        curriculum_entity_id="concept-bayes",
        curriculum_entity_kind="concept",
        evidence_reference="manual:1",
        provenance="test",
        metadata={"correct": True},
        persist=True,
    )
    updated = reasoning.reason(
        twin,
        triggered_by="manual",
        observation_ids=tuple(o.observation_id for o in twin.observations),
        persist=True,
    )
    assert updated.reasoning_history
    assert updated.reasoning_history[-1].triggered_by == "manual"
