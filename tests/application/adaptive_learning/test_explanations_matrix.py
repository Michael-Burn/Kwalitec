"""Additional explanation, band, and intervention-type coverage."""

from __future__ import annotations

import pytest

from app.domain.adaptive_learning.intervention_priority import (
    PriorityBand,
    priority_band_from_score,
    resolve_priority_band,
)
from app.domain.adaptive_learning.intervention_type import InterventionType
from app.domain.adaptive_learning.revision_window import RevisionUrgency
from tests.application.adaptive_learning.helpers import make_engine, make_snapshot
from tests.domain.adaptive_learning.helpers import make_explanation, make_intervention


@pytest.mark.parametrize("score", [round(x * 0.05, 2) for x in range(0, 21)])
def test_all_priority_scores_map_to_band(score):
    band = priority_band_from_score(score)
    assert isinstance(band, PriorityBand)


@pytest.mark.parametrize("band", list(PriorityBand))
def test_resolve_priority_band(band):
    assert resolve_priority_band(band) is band
    assert resolve_priority_band(band.value) is band


@pytest.mark.parametrize("urgency", list(RevisionUrgency))
@pytest.mark.parametrize("minutes", [10.0, 20.0, 45.0, 90.0])
def test_intervention_study_minutes_projection(urgency, minutes):
    from tests.domain.adaptive_learning.helpers import make_window

    window = make_window(urgency=urgency.value, minutes=minutes, priority=0.7)
    assert window.allocated_minutes == minutes
    assert window.urgency is urgency


@pytest.mark.parametrize("itype", list(InterventionType))
def test_intervention_type_values_are_stable(itype):
    assert itype.value == str(itype)
    assert itype.value.islower()


@pytest.mark.parametrize("benefit", [
    "improve_long_term_retention",
    "raise_demonstrated_mastery",
    "reduce_historical_struggle",
    "consolidate_topic_readiness",
    "maintain_current_readiness",
])
@pytest.mark.parametrize("priority", [0.2, 0.4, 0.6, 0.8, 1.0])
def test_explanation_benefit_variants(benefit, priority):
    explanation = make_explanation(benefit=benefit, priority=priority)
    assert explanation.expected_educational_benefit == benefit
    assert explanation.priority_score == priority


@pytest.mark.parametrize("n", range(10))
def test_engine_explanation_always_present(n):
    engine = make_engine(seed=f"e{n}")
    decision = engine.decide(make_snapshot())
    assert decision.explanation.rationale
    assert decision.explanation.expected_educational_benefit
    assert decision.confidence.value
    dto = engine.explain(decision)
    assert dto.decision_id == decision.decision_id


@pytest.mark.parametrize("topic", [f"topic-{i}" for i in range(8)])
def test_intervention_ids_include_topic(topic):
    intervention = make_intervention(f"id-{topic}", topic_id=topic, priority=0.55)
    assert intervention.topic_id == topic
    assert intervention.is_revision
