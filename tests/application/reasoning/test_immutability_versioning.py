"""Immutability and versioning regression for AP-002D2 interpretation."""

from __future__ import annotations

import pytest

from app.application.reasoning.interpretation.evidence_interpreter import (
    EvidenceInterpreter,
)
from app.application.reasoning.interpretation.versions import INTERPRETATION_VERSION
from app.domain.reasoning.observations.category import ObservationCategory
from tests.application.reasoning.conftest import FIXED_AT, make_bundle


def test_observation_set_and_observations_immutable() -> None:
    result = EvidenceInterpreter().interpret_bundle(
        make_bundle(),
        correlation_id="corr-1",
        reasoning_request_id="rrq-1",
        interpreted_at=FIXED_AT,
    )
    observation_set = result.observation_set
    with pytest.raises(Exception):
        observation_set.observations = ()  # type: ignore[misc]
    obs = observation_set.observations[0]
    with pytest.raises(Exception):
        obs.category = ObservationCategory.OBSERVED_COVERAGE  # type: ignore[misc]
    with pytest.raises(TypeError):
        obs.traceability["injected"] = True  # type: ignore[index]


def test_version_stamped_everywhere() -> None:
    result = EvidenceInterpreter().interpret_bundle(
        make_bundle(),
        correlation_id="corr-1",
        reasoning_request_id="rrq-1",
        interpreted_at=FIXED_AT,
    )
    assert result.context.interpreter_version == INTERPRETATION_VERSION
    assert result.observation_set.interpretation_version == INTERPRETATION_VERSION
    for obs in result.observation_set.observations:
        assert obs.interpretation_version == INTERPRETATION_VERSION
