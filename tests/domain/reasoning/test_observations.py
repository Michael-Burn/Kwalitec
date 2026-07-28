"""Domain educational observation model tests (AP-002D2)."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.domain.reasoning.interpretation.errors import (
    DuplicateInterpretedObservation,
    UnknownObservationCategory,
)
from app.domain.reasoning.observations.category import (
    ObservationCategory,
    parse_observation_category,
)
from app.domain.reasoning.observations.observation import EducationalObservation
from app.domain.reasoning.observations.observation_set import EducationalObservationSet

FIXED_AT = datetime(2026, 7, 28, 10, 0, 0)


def _observation(
    *,
    observation_id: str = "eo:obs-1:observed_correctness",
    category: ObservationCategory = ObservationCategory.OBSERVED_CORRECTNESS,
    value=None,
) -> EducationalObservation:
    return EducationalObservation(
        observation_id=observation_id,
        evidence_reference="evidence_bundle:bundle-1:item-1",
        learning_objective_reference="lo-1",
        concept_reference="concept-bayes",
        category=category,
        value=value if value is not None else {"correctness": "correct"},
        provenance="reasoning:interpretation:evidence_bundle:sess-1:bundle-1",
        interpretation_version="AP-002D2.interpretation.v1",
        recorded_at=FIXED_AT,
        reasoning_request_id="rrq-1",
        evidence_bundle_id="bundle-1",
        session_id="sess-1",
        correlation_id="corr-1",
        source_observation_id="obs-1",
        question_reference="q-1",
        traceability={"category": category.value},
    )


def test_parse_known_category() -> None:
    assert (
        parse_observation_category("observed_correctness")
        is ObservationCategory.OBSERVED_CORRECTNESS
    )


def test_parse_unknown_category_rejects() -> None:
    with pytest.raises(UnknownObservationCategory):
        parse_observation_category("mastery_score")


def test_observation_is_immutable() -> None:
    obs = _observation()
    with pytest.raises(Exception):
        obs.observation_id = "mutated"  # type: ignore[misc]
    with pytest.raises(TypeError):
        obs.traceability["x"] = 1  # type: ignore[index]


def test_observation_set_rejects_duplicates() -> None:
    obs = _observation()
    with pytest.raises(DuplicateInterpretedObservation):
        EducationalObservationSet(
            set_id="eos:1",
            observations=(obs, obs),
            interpretation_version="AP-002D2.interpretation.v1",
            evidence_bundle_id="bundle-1",
            reasoning_request_id="rrq-1",
        )


def test_observation_set_by_category() -> None:
    a = _observation()
    b = _observation(
        observation_id="eo:obs-1:observed_confidence",
        category=ObservationCategory.OBSERVED_CONFIDENCE,
        value={"confidence": 3},
    )
    observation_set = EducationalObservationSet(
        set_id="eos:1",
        observations=(a, b),
        interpretation_version="AP-002D2.interpretation.v1",
        evidence_bundle_id="bundle-1",
        reasoning_request_id="rrq-1",
    )
    assert len(observation_set) == 2
    assert len(observation_set.by_category("observed_confidence")) == 1


def test_observation_normalises_timezone() -> None:
    aware = datetime(2026, 7, 28, 12, 0, 0, tzinfo=UTC)
    obs = EducationalObservation(
        observation_id="eo:1:observed_correctness",
        evidence_reference="evidence_bundle:b:i",
        learning_objective_reference="lo-1",
        concept_reference="",
        category=ObservationCategory.OBSERVED_CORRECTNESS,
        value={"correctness": "correct"},
        provenance="reasoning:interpretation:evidence_bundle:s:b",
        interpretation_version="AP-002D2.interpretation.v1",
        recorded_at=aware,
        reasoning_request_id="rrq-1",
        evidence_bundle_id="bundle-1",
        session_id="sess-1",
        correlation_id="corr-1",
    )
    assert obs.recorded_at.tzinfo is None
