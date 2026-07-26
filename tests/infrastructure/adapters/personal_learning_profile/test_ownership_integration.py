"""Constitutional ownership + service consumption tests (EP-004.1)."""

from __future__ import annotations

from datetime import date

from app.infrastructure.adapters.learning_feedback import (
    LearningFeedbackRecorder,
    bind_learning_feedback_recorder,
)
from app.infrastructure.adapters.personal_learning_profile import (
    PersonalLearningProfilePort,
    PersonalLearningProfileStore,
    bind_personal_learning_profile_store,
    build_personal_learning_profile_adapter,
)
from app.services.planning_service import PlanningService
from app.services.readiness_service import ReadinessService
from app.services.recommendation_service import RecommendationService


def setup_function() -> None:
    bind_learning_feedback_recorder(None)
    bind_personal_learning_profile_store(None)


def teardown_function() -> None:
    bind_learning_feedback_recorder(None)
    bind_personal_learning_profile_store(None)


def test_adapter_satisfies_port_protocol():
    adapter = build_personal_learning_profile_adapter(enabled=True)
    assert adapter is not None
    assert isinstance(adapter, PersonalLearningProfilePort)


def test_services_depend_on_port_surface_not_aggregator():
    """Services import consumer helpers — not aggregator internals."""
    import inspect

    for service in (RecommendationService, ReadinessService, PlanningService):
        src = inspect.getsource(service.consume_personal_learning_profile)
        assert "PersonalLearningProfileAggregator" not in src
        assert "consume_personal_learning_profile" in src


def test_recommendation_consume_does_not_alter_decision(ctx):
    feedback = LearningFeedbackRecorder(enabled=True)
    bind_learning_feedback_recorder(feedback)
    store = PersonalLearningProfileStore(enabled=True)
    bind_personal_learning_profile_store(store)
    from tests.conftest import _make_user

    user = _make_user()
    recommendation = {
        "title": "Review Fractions",
        "category": "review",
        "priority": "high",
        "reason": "Due review",
        "expected_benefit": "Retention",
        "generated_at": "2026-07-26T09:00:00",
    }
    decision = RecommendationService.record_decision(
        user.id, recommendation, accepted=True
    )
    assert decision is not None
    assert decision.accepted is True
    view = RecommendationService.consume_personal_learning_profile(user.id)
    assert view is not None
    assert view["authority"] == "personal_learning_profile"
    # Preference-journal attribute must not claim mastery.
    resp = view["attributes"]["recommendation_responsiveness"]
    assert resp["claim_boundary"] == "preference_summary"
    assert "mastery" not in (resp.get("value") or {})


def test_profile_failure_does_not_break_decision_recording(ctx):
    class Boom:
        enabled = True

        def resolve(self, *args, **kwargs):  # noqa: ANN002, ANN003
            raise RuntimeError("profile down")

        def get_cached(self, student_id):  # noqa: ANN001
            raise RuntimeError("profile down")

    bind_personal_learning_profile_store(Boom())
    from tests.conftest import _make_user

    user = _make_user()
    recommendation = {
        "title": "Keep going",
        "category": "motivation",
        "priority": "medium",
        "reason": "Consistency",
        "expected_benefit": "Habit",
        "generated_at": date.today().isoformat(),
    }
    decision = RecommendationService.record_decision(
        user.id, recommendation, accepted=True
    )
    assert decision is not None
    assert (
        RecommendationService.consume_personal_learning_profile(user.id)
        is None
    )


def test_readiness_collector_path_has_no_profile_dependency():
    """get_overall_readiness must remain collector-safe (no profile consume)."""
    import inspect

    src = inspect.getsource(ReadinessService.get_overall_readiness)
    assert "consume_personal_learning_profile" not in src
    assert "personal_learning_profile" not in src


def test_planning_consume_does_not_change_plan_body():
    store = PersonalLearningProfileStore(enabled=True)
    bind_personal_learning_profile_store(store)
    view = PlanningService.consume_personal_learning_profile(42)
    assert view is not None
    # No planning fields on consumer view.
    assert "mission_slots" not in view
    assert "plan_slots" not in view
    assert view["authority"] == "personal_learning_profile"


def test_profile_is_not_allowed_as_educational_source_authority():
    """Profile must not appear as a Learning Feedback source authority."""
    from app.infrastructure.adapters.learning_feedback.contracts import (
        ALLOWED_SOURCE_AUTHORITIES,
    )

    assert "personal_learning_profile" not in ALLOWED_SOURCE_AUTHORITIES
    assert ALLOWED_SOURCE_AUTHORITIES == frozenset(
        {
            "recommendation_service",
            "readiness_service",
            "planning_service",
        }
    )
