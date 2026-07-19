"""Additional volume coverage for Experience integration (port × learner)."""

from __future__ import annotations

import pytest

from app.infrastructure.adapters.student_experience.composition import (
    StudentExperienceComposition,
)
from tests.infrastructure.adapters.student_experience.helpers import LEARNERS

READ_METHODS = (
    ("twin", "get_learner_summary"),
    ("twin", "get_readiness_summary"),
    ("twin", "get_learning_insights"),
    ("adaptive", "get_todays_recommendation"),
    ("adaptive", "get_revision_options"),
    ("adaptive", "get_decision_explanation"),
    ("mission", "get_todays_session"),
    ("journey", "get_journey_progress"),
    ("journey", "get_topic_list"),
    ("orchestrator", "get_activity_status"),
)

PRIORITIES = ("high", "medium", "low", "urgent", "normal")
MINUTE_BANDS = (15, 20, 25, 30, 45, 60)


@pytest.mark.parametrize("learner_id", LEARNERS)
@pytest.mark.parametrize("adapter_name,method_name", READ_METHODS)
def test_seeded_port_read_grid(learner_id, adapter_name, method_name):
    composition = StudentExperienceComposition(seed_demo_learners=False)
    composition.seed_learner(learner_id, demo=True)
    adapter = getattr(composition, adapter_name)
    method = getattr(adapter, method_name)
    if method_name == "get_decision_explanation":
        result = method(learner_id, decision_id="d1")
    else:
        result = method(learner_id)
    assert result is not None


@pytest.mark.parametrize("learner_id", LEARNERS)
@pytest.mark.parametrize("minutes", MINUTE_BANDS)
def test_mission_start_minute_bands(learner_id, minutes):
    composition = StudentExperienceComposition(
        seed_demo_learners=False, learning_loop=None
    )
    composition.seed_learner(learner_id, demo=True)
    mission_doc = composition.store.get(composition.store.mission, learner_id)
    today = dict(mission_doc.get("todays_session") or {})
    today["estimated_minutes"] = minutes
    mission_doc["todays_session"] = today
    composition.mission.put_projection(learner_id, mission_doc)
    result = composition.mission.start_session(learner_id)
    assert result["estimated_minutes"] == minutes
    assert result["status"] == "in_progress"


@pytest.mark.parametrize("learner_id", LEARNERS[:8])
@pytest.mark.parametrize("priority", PRIORITIES)
def test_adaptive_revision_priority_labels(learner_id, priority):
    composition = StudentExperienceComposition(seed_demo_learners=False)
    composition.seed_learner(learner_id, demo=True)
    doc = composition.store.get(composition.store.adaptive, learner_id)
    options = list(doc.get("revision_options") or [])
    if options:
        options[0] = {**options[0], "priority_label": priority}
        doc["revision_options"] = tuple(options)
        composition.adaptive.put_projection(learner_id, doc)
    loaded = composition.adaptive.get_revision_options(learner_id)
    assert loaded
    assert loaded[0]["priority_label"] == priority


@pytest.mark.parametrize("learner_id", LEARNERS)
@pytest.mark.parametrize("available", [True, False])
def test_port_unavailable_toggles(learner_id, available):
    composition = StudentExperienceComposition(seed_demo_learners=False)
    composition.seed_learner(learner_id, demo=True)
    for adapter in (
        composition.twin,
        composition.adaptive,
        composition.mission,
        composition.journey,
        composition.orchestrator,
    ):
        adapter.set_available(available)
        assert adapter.is_available() is available
