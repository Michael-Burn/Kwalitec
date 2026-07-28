"""Evidence / observation interpretation pipeline tests (AP-002D2)."""

from __future__ import annotations

from app.application.reasoning.dto.interpretation_dto import InterpretationRequestDTO
from app.application.reasoning.interpretation.evidence_interpreter import (
    EvidenceInterpreter,
)
from app.application.reasoning.interpretation.versions import INTERPRETATION_VERSION
from app.application.reasoning.mappers.evidence_mapper import map_interpretation_result
from app.domain.reasoning.observations.category import ObservationCategory
from tests.application.reasoning.conftest import FIXED_AT, make_bundle, make_item


def test_interpret_generates_item_and_bundle_observations() -> None:
    result = EvidenceInterpreter().interpret(
        InterpretationRequestDTO(
            bundle=make_bundle(),
            correlation_id="corr-1",
            reasoning_request_id="rrq-fixed",
        ),
        interpreted_at=FIXED_AT,
    )
    categories = {o.category for o in result.observation_set.observations}
    assert ObservationCategory.OBSERVED_CORRECTNESS in categories
    assert ObservationCategory.OBSERVED_CONFIDENCE in categories
    assert ObservationCategory.OBSERVED_HINT_DEPENDENCY in categories
    assert ObservationCategory.OBSERVED_RESPONSE_PERSISTENCE in categories
    assert ObservationCategory.OBSERVED_TIMING_PROFILE in categories
    assert ObservationCategory.OBSERVED_MISCONCEPTION_INDICATORS in categories
    assert ObservationCategory.OBSERVED_COVERAGE in categories
    assert ObservationCategory.OBSERVED_CONSISTENCY in categories
    assert result.context.interpreter_version == INTERPRETATION_VERSION
    assert result.observation_set.reasoning_request_id == "rrq-fixed"


def test_interpretation_is_deterministic() -> None:
    request = InterpretationRequestDTO(
        bundle=make_bundle(),
        correlation_id="corr-1",
        reasoning_request_id="rrq-fixed",
    )
    first = EvidenceInterpreter().interpret(request, interpreted_at=FIXED_AT)
    second = EvidenceInterpreter().interpret(request, interpreted_at=FIXED_AT)
    assert first.observation_ids == second.observation_ids
    assert [
        (o.category, o.value) for o in first.observation_set.observations
    ] == [
        (o.category, o.value) for o in second.observation_set.observations
    ]


def test_does_not_invent_missing_confidence() -> None:
    item = make_item(confidence=None, response_time_ms=None, misconception_tags=())
    result = EvidenceInterpreter().interpret_bundle(
        make_bundle(
            items=(item,),
            observation_ids=(item.observation_id,),
            question_ids=(item.question_id,),
        ),
        correlation_id="corr-1",
        reasoning_request_id="rrq-1",
        interpreted_at=FIXED_AT,
    )
    categories = {o.category for o in result.observation_set.observations}
    assert ObservationCategory.OBSERVED_CONFIDENCE not in categories
    assert ObservationCategory.OBSERVED_TIMING_PROFILE not in categories
    assert ObservationCategory.OBSERVED_MISCONCEPTION_INDICATORS not in categories
    assert ObservationCategory.OBSERVED_CORRECTNESS in categories


def test_traceability_identifiers_present() -> None:
    result = EvidenceInterpreter().interpret_bundle(
        make_bundle(),
        correlation_id="corr-trace",
        reasoning_request_id="rrq-trace",
        interpreted_at=FIXED_AT,
    )
    ctx = result.context
    assert ctx.correlation_id == "corr-trace"
    assert ctx.reasoning_request_id == "rrq-trace"
    assert ctx.evidence_bundle_id == "bundle-1"
    assert ctx.session_id == "sess-1"
    assert ctx.packaging_version == "AP-002C.1"
    for obs in result.observation_set.observations:
        assert obs.correlation_id == "corr-trace"
        assert obs.reasoning_request_id == "rrq-trace"
        assert obs.evidence_bundle_id == "bundle-1"
        assert obs.session_id == "sess-1"
        assert obs.learning_objective_reference == "lo-1"
        assert obs.concept_reference == "concept-bayes"
        assert obs.interpretation_version == INTERPRETATION_VERSION
        assert "reasoning_request_id" in obs.traceability


def test_mapper_projects_dto() -> None:
    result = EvidenceInterpreter().interpret_bundle(
        make_bundle(),
        correlation_id="corr-1",
        reasoning_request_id="rrq-1",
        interpreted_at=FIXED_AT,
    )
    dto = map_interpretation_result(result)
    assert dto.set_id == result.observation_set.set_id
    assert len(dto.observations) == result.observation_count
    assert dto.observation_ids == result.observation_ids
    assert dto.interpreter_version == INTERPRETATION_VERSION


def test_misconception_observation_value() -> None:
    result = EvidenceInterpreter().interpret_bundle(
        make_bundle(),
        correlation_id="corr-1",
        reasoning_request_id="rrq-1",
        interpreted_at=FIXED_AT,
    )
    misconceptions = result.observation_set.by_category(
        ObservationCategory.OBSERVED_MISCONCEPTION_INDICATORS.value
    )
    assert len(misconceptions) == 1
    assert misconceptions[0].value["misconception_tags"] == ("confuses_prior",)
