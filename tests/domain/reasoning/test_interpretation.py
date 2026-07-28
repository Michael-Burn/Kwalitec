"""Domain interpretation context / result / version tests (AP-002D2)."""

from __future__ import annotations

from datetime import datetime

import pytest

from app.domain.reasoning.interpretation.context import InterpretationContext
from app.domain.reasoning.interpretation.result import InterpretationResult
from app.domain.reasoning.interpretation.version import (
    INTERPRETATION_VERSION,
    InterpretationVersion,
)
from app.domain.reasoning.observations.category import ObservationCategory
from app.domain.reasoning.observations.observation import EducationalObservation
from app.domain.reasoning.observations.observation_set import EducationalObservationSet


def test_interpretation_version_constant() -> None:
    assert INTERPRETATION_VERSION == "AP-002D2.interpretation.v1"
    assert str(InterpretationVersion()) == INTERPRETATION_VERSION


def test_context_requires_trace_fields() -> None:
    with pytest.raises(ValueError, match="correlation_id"):
        InterpretationContext.create(
            reasoning_request_id="rrq-1",
            evidence_bundle_id="bundle-1",
            session_id="sess-1",
            packaging_version="AP-002C.1",
            correlation_id="",
        )


def test_result_rejects_version_mismatch() -> None:
    context = InterpretationContext.create(
        reasoning_request_id="rrq-1",
        evidence_bundle_id="bundle-1",
        session_id="sess-1",
        packaging_version="AP-002C.1",
        correlation_id="corr-1",
    )
    obs = EducationalObservation(
        observation_id="eo:1:observed_coverage",
        evidence_reference="evidence_bundle:bundle-1",
        learning_objective_reference="lo-1",
        concept_reference="c-1",
        category=ObservationCategory.OBSERVED_COVERAGE,
        value={"observation_count": 1},
        provenance="reasoning:interpretation:evidence_bundle:sess-1:bundle-1",
        interpretation_version="AP-002D2.interpretation.v1",
        recorded_at=datetime(2026, 7, 28, 10, 0, 0),
        reasoning_request_id="rrq-1",
        evidence_bundle_id="bundle-1",
        session_id="sess-1",
        correlation_id="corr-1",
    )
    observation_set = EducationalObservationSet(
        set_id="eos:1",
        observations=(obs,),
        interpretation_version="other-version",
        evidence_bundle_id="bundle-1",
        reasoning_request_id="rrq-1",
    )
    with pytest.raises(ValueError, match="interpretation_version"):
        InterpretationResult(
            context=context,
            observation_set=observation_set,
            interpreted_at=datetime(2026, 7, 28, 10, 0, 0),
        )
