"""StudentReasoningService interpretation wiring + no Twin mutation (AP-002D2)."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from app.application.reasoning.dto.interpretation_dto import InterpretationResultDTO
from app.application.reasoning.interpretation.errors import (
    MissingLearningObjective,
    UnsupportedEvidenceSchema,
)
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
from app.domain.reasoning.interpretation.result import InterpretationResult
from app.domain.reasoning.observations.category import ObservationCategory
from tests.application.reasoning.conftest import FIXED_AT, make_bundle


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
            evidence_id="ev-interp-1",
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
        provenance_id="prov-interp-1",
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
        retrieval_log_id="rl-interp-1",
    )
    return stub


@pytest.fixture
def twin(ctx):
    return StudentDigitalTwinService().create(
        student_id="student-interp-1",
        display_name="Interp Student",
        subject_code="CS1",
        workspace_id="ws-interp",
        twin_id="twin-interp-1",
    )


@pytest.fixture
def reasoning(ctx) -> StudentReasoningService:
    return StudentReasoningService(retrieval=_make_retrieval_stub())


def test_interpret_assessment_evidence_returns_observation_set(reasoning) -> None:
    result = reasoning.interpret_assessment_evidence(
        bundle=make_bundle(),
        correlation_id="corr-svc",
        reasoning_request_id="rrq-svc",
        interpreted_at=FIXED_AT,
    )
    assert isinstance(result, InterpretationResult)
    assert result.observation_count > 0
    assert ObservationCategory.OBSERVED_COVERAGE in {
        o.category for o in result.observation_set.observations
    }


def test_interpret_as_dto(reasoning) -> None:
    dto = reasoning.interpret_assessment_evidence(
        bundle=make_bundle(),
        correlation_id="corr-svc",
        reasoning_request_id="rrq-svc",
        interpreted_at=FIXED_AT,
        as_dto=True,
    )
    assert isinstance(dto, InterpretationResultDTO)
    assert dto.correlation_id == "corr-svc"


def test_interpret_does_not_update_twin(reasoning, twin) -> None:
    before_obs_count = len(twin.observations)
    before_mastery_records = twin.mastery.records if twin.mastery else ()
    before_history_len = len(twin.reasoning_history)
    before_updated_at = twin.updated_at

    reasoning.interpret_assessment_evidence(
        bundle=make_bundle(),
        correlation_id="corr-svc",
        reasoning_request_id="rrq-svc",
        interpreted_at=FIXED_AT,
    )

    reloaded = StudentDigitalTwinService().get(twin.twin_id)
    assert reloaded is not None
    assert len(reloaded.observations) == before_obs_count
    assert len(reloaded.reasoning_history) == before_history_len
    assert reloaded.updated_at == before_updated_at
    after_mastery = reloaded.mastery.records if reloaded.mastery else ()
    assert after_mastery == before_mastery_records


def test_interpret_rejects_missing_learning_objectives(reasoning) -> None:
    with pytest.raises(MissingLearningObjective):
        reasoning.interpret_assessment_evidence(
            bundle=make_bundle(learning_objective_ids=()),
            correlation_id="corr-svc",
        )


def test_interpret_rejects_unsupported_schema(reasoning) -> None:
    with pytest.raises(UnsupportedEvidenceSchema):
        reasoning.interpret_assessment_evidence(
            bundle=make_bundle(packaging_version="nope"),
            correlation_id="corr-svc",
        )


def test_existing_reason_path_unaffected(reasoning, twin) -> None:
    """Regression: interpret does not replace the lawful reason() path."""
    updated = reasoning.reason(twin, triggered_by="manual", persist=True)
    assert updated.reasoning_history
    assert updated.reasoning_history[-1].triggered_by == "manual"
