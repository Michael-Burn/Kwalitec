"""Integration + behavioural parity — Recommendation Read Bridge → Runtime A."""

from __future__ import annotations

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.adaptive import ExperienceAdaptiveAdapter
from app.infrastructure.adapters.educational_runtime_bridge import (
    AUTHORITY_RECOMMENDATION_BRIDGE,
    RECOMMENDATION_BRIDGE_SUCCESS,
    RecommendationAdapter,
)
from app.infrastructure.adapters.student_experience.composition import (
    StudentExperienceComposition,
    build_production_experience,
)
from app.infrastructure.adapters.student_experience.defaults import (
    seeded_demo_adaptive,
)
from app.infrastructure.events.registry import EventRegistry
from app.services.recommendation_service import RecommendationService
from tests.conftest import _make_mission, _make_study_plan, _make_subject, _make_user


def test_adapter_projects_from_runtime_a(ctx, db):
    user = _make_user()
    subject = _make_subject(user.id)
    plan = _make_study_plan(user.id)
    mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)
    events = EventRegistry()
    adapter = RecommendationAdapter(events=events)
    result = adapter.get_todays_recommendation(str(user.id))
    assert result.ok is True
    assert result.value is not None
    assert result.value["authority"] == AUTHORITY_RECOMMENDATION_BRIDGE
    assert result.value["mission_aligned"] is True
    assert result.value["topic_title"] == mission.title
    assert result.value["mission_id"] == str(mission.id)
    assert result.value["authority"] != "adaptive_decision_engine"
    assert any(
        e.event_type == RECOMMENDATION_BRIDGE_SUCCESS for e in events.published()
    )


def test_experience_adapter_uses_bridge(ctx, db):
    user = _make_user()
    subject = _make_subject(user.id)
    plan = _make_study_plan(user.id)
    mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)
    bridge = RecommendationAdapter()
    experience = ExperienceAdaptiveAdapter(recommendation_read=bridge)
    recommendation = experience.get_todays_recommendation(str(user.id))
    assert recommendation is not None
    assert recommendation["mission_id"] == str(mission.id)
    assert recommendation["topic_title"] == mission.title
    assert recommendation["authority"] == AUTHORITY_RECOMMENDATION_BRIDGE
    assert recommendation["topic_title"] != "Core methods"


def test_experience_bridge_no_demo_fallback_when_empty(ctx, db):
    user = _make_user()
    bridge = RecommendationAdapter()
    experience = ExperienceAdaptiveAdapter(
        recommendation_read=bridge, auto_provision=True
    )
    recommendation = experience.get_todays_recommendation(str(user.id))
    # May be None (no plan/mission/recs) — never seeded demo.
    if recommendation is not None:
        assert recommendation.get("topic_title") != "Core methods"
        assert recommendation.get("authority") == AUTHORITY_RECOMMENDATION_BRIDGE
    demo = seeded_demo_adaptive(str(user.id))["recommendation"]
    assert recommendation != demo


def test_composition_flag_off_preserves_seed_path(ctx, db):
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_RECOMMENDATION_BRIDGE is False
    composition = StudentExperienceComposition(seed_demo_learners=True)
    assert composition._recommendation_read is None
    composition.seed_learner("42", demo=True)
    recommendation = composition.adaptive.get_todays_recommendation("42")
    assert recommendation is not None
    assert recommendation["topic_title"] == "Today's topic"


def test_composition_flag_on_wires_bridge_without_seeded_adaptive(ctx, db):
    user = _make_user()
    subject = _make_subject(user.id)
    plan = _make_study_plan(user.id)
    mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_RECOMMENDATION_BRIDGE": "1"}
    )
    assert flags.ENABLE_RECOMMENDATION_BRIDGE is True
    assert flags.SEED_DEMO_LEARNERS is False
    composition, _service = build_production_experience(flags=flags)
    assert composition._recommendation_read is not None
    recommendation = composition.adaptive.get_todays_recommendation(str(user.id))
    assert recommendation is not None
    assert recommendation["mission_id"] == str(mission.id)
    assert recommendation["authority"] == AUTHORITY_RECOMMENDATION_BRIDGE
    demo = seeded_demo_adaptive(str(user.id))["recommendation"]
    assert recommendation["topic_title"] != demo["topic_title"]


def test_flag_on_seed_learner_skips_demo_adaptive(ctx, db):
    user = _make_user()
    bridge = RecommendationAdapter()
    composition = StudentExperienceComposition(
        seed_demo_learners=True,
        recommendation_read=bridge,
    )
    composition.seed_learner(str(user.id), demo=True)
    stored = composition.store.get(composition.store.adaptive, str(user.id))
    assert stored is None or stored.get("authority") != "adaptive_decision_engine"


def test_behavioural_parity_with_legacy_recommendation_service(ctx, db):
    """Bridged projection originates from RecommendationService + mission."""
    user = _make_user()
    subject = _make_subject(user.id)
    plan = _make_study_plan(user.id)
    mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)

    legacy = RecommendationService.generate_recommendations(user.id, limit=5)
    bridged = RecommendationAdapter().get_todays_recommendation(str(user.id))
    assert bridged.ok is True
    assert bridged.value is not None
    # Mission alignment is the product rule when a mission exists.
    assert bridged.value["topic_title"] == mission.title
    assert bridged.value["mission_aligned"] is True
    if legacy:
        # Narrative / alternatives remain Runtime A RecommendationService rows.
        assert bridged.value["summary"] == legacy[0]["reason"] or bridged.value[
            "summary"
        ].startswith("Today's mission")
        assert len(bridged.value["alternatives"]) == max(0, len(legacy) - 1)
        for alt, src in zip(
            bridged.value["alternatives"], legacy[1:], strict=True
        ):
            assert alt["title"] == src["title"]
            assert alt["category"] == src["category"]


def test_read_path_does_not_mutate_decision_journal(ctx, db):
    from app.models.decision import Decision

    user = _make_user()
    subject = _make_subject(user.id)
    plan = _make_study_plan(user.id)
    _make_mission(user.id, subject.id, study_plan_id=plan.id)
    before = Decision.query.filter_by(user_id=user.id).count()
    RecommendationAdapter().get_todays_recommendation(str(user.id))
    after = Decision.query.filter_by(user_id=user.id).count()
    assert after == before


def test_umbrella_flag_enables_recommendation_bridge(ctx, db):
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EDUCATIONAL_RUNTIME_BRIDGE": "1"}
    )
    assert flags.ENABLE_RECOMMENDATION_BRIDGE is True
    composition, _ = build_production_experience(flags=flags)
    assert composition._recommendation_read is not None
